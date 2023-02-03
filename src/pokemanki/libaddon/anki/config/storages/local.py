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

from anki.hooks import wrap

from ....addon import ADDON

from .base import ConfigStorage

__all__ = ["LocalConfigStorage"]


class LocalConfigStorage(ConfigStorage):

    name = "local"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._defaults = self._mw.addonManager.addonConfigDefaults(ADDON.MODULE) or {}
        self._namespace = ADDON.MODULE  # no custom namespaces supported

    def initialize(self) -> bool:
        initialized = super().initialize()
        if initialized and self._native_gui:
            self._ensureSaveBeforeConfigGUILoaded()
            self._ensureLoadAfterConfigGUIFinished()
        return initialized

    def delete(self):
        self.data = {}
        self.save()
        super().delete()

    def load(self) -> bool:
        data = self._mw.addonManager.getConfig(self._namespace)
        self.data = data or {}
        super().load()
        return data is not None

    def save(self) -> None:
        self._mw.addonManager.writeConfig(self._namespace, self.data)
        super().save()

    def _ensureLoadAfterConfigGUIFinished(self) -> None:
        self._mw.addonManager.setConfigUpdatedAction(self._namespace, self.load)

    def _ensureSaveBeforeConfigGUILoaded(self) -> None:
        """ugly workaround, drop as soon as possible"""

        from aqt.addons import AddonsDialog

        def wrappedOnConfig(addonsDialog: AddonsDialog, *args, **kwargs):
            """Save before config editor is invoked"""
            addon = addonsDialog.onlyOneSelected()
            if not addon or addon != self._namespace:
                return
            self.save()

        AddonsDialog.onConfig = wrap(AddonsDialog.onConfig, wrappedOnConfig, "before")
