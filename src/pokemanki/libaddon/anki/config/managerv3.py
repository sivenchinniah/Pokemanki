from ..._wrappers.typing import Callable, List

from libaddon.anki.config.storages import ConfigStorage


class ConfigManager:
    def __init__(self) -> None:
        self._storages = {}

    def __getitem__(self, name):
        return self._storages[name]

    def __setitem__(self, name, value):
        pass

    def registerStorages(self, storages: List[ConfigStorage]):
        pass

    def setConfigAction(self, action: Callable):
        pass
