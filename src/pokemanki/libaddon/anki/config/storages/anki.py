# -*- coding: utf-8 -*-

# Libaddon for Anki
#
# Copyright (C) 2018-2019  Aristotelis P. <https//glutanimate.com/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the license file that accompanied this program.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# NOTE: This program is subject to certain additional terms pursuant to
# Section 7 of the GNU Affero General Public License.  You should have
# received a copy of these additional terms immediately following the
# terms and conditions of the GNU Affero General Public License that
# accompanied this program.
#
# If not, please request a copy through one of the means of contact
# listed here: <https://glutanimate.com/contact/>.
#
# Any modifications to this file must keep this entire header intact.

"""
Add-on configuration storages
"""

from aqt.main import AnkiQt
from anki.hooks import addHook

from ...._wrappers.typing import Any, Optional, Hashable

from ...._vendor.packaging import version

from ....util.structures import deepMergeDicts

from ....anki.additions.hooks import HOOKS
from ....addon import ADDON

from ..errors import ConfigError, ConfigNotReadyError, ConfigFutureError

from .base import ConfigStorage

__all__ = [
    "AnkiConfigStorage",
    "ProfileConfigStorage",
    "MetaConfigStorage",
    "LibaddonMetaConfigStorage",
    "SyncedConfigStorage",
]


# TODO: SUBCLASS DOCSTRINGS

class AnkiConfigStorage(ConfigStorage):
    """abstract, never initialize directly"""

    name = "profile"

    def __init__(
        self, mw: AnkiQt, namespace: str, defaults: dict, native_gui: bool = True
    ):
        self._ensure_defaults_versioned(defaults)
        super().__init__(mw, namespace, defaults=defaults, native_gui=native_gui)
        self._deferred: bool = False

    def initialize(self) -> bool:
        if not self._isStorageReady():
            self._deferInitialization()
            return False
        return super().initialize()

    def _ensure_defaults_versioned(self, defaults):
        if not isinstance(defaults, dict) or not defaults.get("version"):
            raise ConfigError("Defaults need to include a 'version' key/value pair")

    @property
    def _configObject(self) -> dict:
        try:
            config_object = self._actualConfigObject()
        except AttributeError:
            config_object = None
        if config_object is None:
            raise ConfigNotReadyError(f"{self.name} storage is not ready")
        return self._getUpdatedConfig(config_object)

    def _actualConfigObject(self) -> dict:
        raise NotImplementedError

    def _getUpdatedConfig(self, config_object: dict) -> dict:
        conf_key = self._namespace
        defaults = self.defaults()

        # Initialize config
        if conf_key not in config_object:
            config_object[conf_key] = defaults

        storage_dict = config_object[conf_key]
        dict_version = str(storage_dict.get("version", "0.0.0"))
        default_version = str(defaults.get("version", "0.0.0"))

        parsed_version_current = version.parse(dict_version)
        parsed_version_default = version.parse(default_version)

        # Upgrade config version if necessary
        if parsed_version_current < parsed_version_default:
            config_object[conf_key] = deepMergeDicts(defaults, storage_dict, new=True)
            config_object[conf_key]["version"] = default_version
            self._flush()
        elif parsed_version_current > parsed_version_default:
            # TODO: Figure out where to handle
            raise ConfigFutureError("Config is newer than add-on release")

        return config_object[self._namespace]

    def load(self) -> bool:
        data = self._configObject.get(self._namespace)
        self.data = data or {}
        super().load()
        return data is not None

    def save(self) -> None:
        self._configObject[self._namespace] = self.data
        self._flush()
        super().save()

    def delete(self) -> None:
        try:
            del self._configObject[self._namespace]
        except KeyError:
            raise ConfigError("Attempted to delete non-existing config")
        self._flush()

    def _flush(self) -> None:
        try:
            self._mw.col.setMod()
        except AttributeError:
            raise ConfigNotReadyError(f"Anki collection is not loaded")

    def _isStorageReady(self) -> bool:
        try:
            _ = self._configObject  # noqa: F841
            return True
        except ConfigNotReadyError:
            return False

    def _deferInitialization(self):
        if self._deferred:
            raise ConfigError("Initialization already deferred")
        self._deferred = True
        addHook(HOOKS.PROFILE_LOADED, self.initialize)


class ProfileConfigStorage(AnkiConfigStorage):

    name = "profile"

    def _actualConfigObject(self) -> dict:
        return self._mw.pm.profile


class MetaConfigStorage(AnkiConfigStorage):

    name = "meta"

    def _actualConfigObject(self) -> dict:
        return self._mw.pm.meta


class LibaddonMetaConfigStorage(MetaConfigStorage):

    name = "libaddonmeta"

    def _actualConfigObject(self) -> dict:
        config_object = super()._actualConfigObject()
        if "libaddon" not in config_object:
            config_object["libaddon"] = {}
        return config_object["libaddon"]


class SyncedConfigStorage(AnkiConfigStorage):

    name = "synced"

    def _actualConfigObject(self) -> dict:
        return self._mw.col.conf
