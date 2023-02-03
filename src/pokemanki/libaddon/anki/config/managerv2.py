from collections import UserDict

from anki.hooks import addHook, runHook

from ..._wrappers.typing import Any, Callable, Hashable, List, Optional

from ..._vendor.packaging import version
from ...addon import ADDON
from ...util.structures import deepMergeDicts

from .errors import ConfigError
from .storages import ConfigStorage, STORAGE_REGISTRY
from .interface import ConfigInterface


class ConfigManager(UserDict, ConfigInterface):
    def __init__(
        self,
        mw,
        namespace,
        config_dict: Optional[dict] = None,
        config_action: Callable = None,
    ):
        super().__init__()
        self._mw = mw
        self._namespace = namespace

        if config_dict:
            self.load(config_dict)
        if config_action:
            self.setConfigAction(config_action)

    def __getitem__(self, key: str) -> ConfigStorage:
        return super().__getitem__(key)

    def __setitem__(self, key: str, value: ConfigStorage):
        try:
            assert isinstance(value, ConfigStorage)
        except AssertionError:
            raise ConfigError("Value to be set needs to be a valid ConfigStorage")

    def load(self, config_dict):
        for storage_name, default_values in self._defaults:
            try:
                StorageClass = STORAGE_REGISTRY[storage_name]
            except KeyError:
                raise ConfigError(f"Storage not implemented: {storage_name}")
            storage = StorageClass(
                self._mw,
                self._namespace,
                defaults=self._defaults,
                native_options=(not self._config_action),
            )
            if not storage.delay:
                storage.load()
            else:
                self._deferStorageLoading(storage)
            self.data[storage_name] = storage

    def save(self):
        for storage_name, storage in self.data:
            storage.save()

    def defaults(self):
        defaults = {}
        for storage_name, storage in self.data:
            defaults[storage_name] = storage.defaults()
        return defaults

    def reset(self):
        for storage_name, storage in self.data:
            storage.reset()

    def delete(self):
        for storage_name, storage in self.data:
            storage.delete()

    def _deferStorageLoading(self, storage):
        self._deferred_storages.append(storage)

    def _onProfileLoaded(self):
        for storage in self._deferred_storages:
            storage.load()
        self._deferred_storages = []

    def _setupHooks(self):
        pass
