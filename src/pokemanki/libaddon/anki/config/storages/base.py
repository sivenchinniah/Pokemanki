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

from collections import UserDict
from typing import Any, Optional, Hashable  # FIXME: import from _vendor

from aqt.main import AnkiQt
from anki.hooks import addHook

from ....anki.additions.hooks import HOOKS

from ..interface import ConfigInterface
from ..signals import ConfigSignals
from ..errors import ConfigNotReadyError

__all__ = ["ConfigStorage"]


class ConfigStorage(UserDict, ConfigInterface):
    """abstract, never initialize directly"""

    name: str = ""

    def __init__(
        self,
        mw: AnkiQt,
        namespace: str,
        defaults: Optional[dict] = None,
        native_gui: bool = True,
    ):
        defaults = defaults or {}

        self._mw = mw
        self._namespace = namespace
        self._defaults = defaults
        self._native_gui = native_gui

        self._ready: bool = False
        self._loaded: bool = False
        self._dirty: bool = False

        self.signals = ConfigSignals()

        # calls in __setitem__ might not be ready, so set data manually rather
        # than letting it be set by super().__init__ which uses __setitem__
        super().__init__()
        self.data = defaults

    def __getitem__(self, key: Hashable) -> Any:
        self._checkReadyAndLoaded()
        return super().__getitem__(key)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self._checkReadyAndLoaded()
        super().__setitem__(key, value)
        self._dirty = True

    @property
    def ready(self) -> bool:
        return self._ready

    @property
    def loaded(self) -> bool:
        return self._loaded

    @property
    def dirty(self) -> bool:
        return self._dirty

    # TODO: CRUCIAL – perform config validation
    # if invalid:
    #   config.reset()
    #   and perhaps notify user
    # CONSIDER: perform these only at load/save time or with every access?
    # (expensive!)

    def initialize(self) -> bool:
        self._ready = True
        if self._loaded:
            return True
        self.load()
        addHook(HOOKS.PROFILE_UNLOAD, self.unload)
        self.signals.initialized.emit()
        return True

    def load(self) -> bool:
        # should set self.data from base storage
        self._loaded = True
        self.signals.loaded.emit()
        return True

    def save(self) -> None:
        # should set base storage from self.data
        self._checkReadyAndLoaded()
        self._dirty = False
        self.signals.saved.emit()

    def defaults(self) -> dict:
        return self._defaults

    def reset(self) -> None:
        self.data = self.defaults()
        self.save()
        self.signals.reset.emit()

    def delete(self) -> None:
        # base storage object is deleted, data representation is set to an empty
        # dict
        self.data = {}
        self._loaded = self._dirty = False
        self.signals.deleted.emit()

    def unload(self):
        self.signals.unloaded.emit()
        self.signals.disconnect()
        if not self._loaded or not self._dirty:
            return

        try:
            self.save()
        except FileNotFoundError as e:
            # Corner case: Closing Anki after add-on uninstall
            print(e)

    def _checkReadyAndLoaded(self) -> bool:
        if self._loaded:
            return True
        elif self._ready:
            return self.load()
        else:
            raise ConfigNotReadyError(f"{self.name} storage not ready to load")
