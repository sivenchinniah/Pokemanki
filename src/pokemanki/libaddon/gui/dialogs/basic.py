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
Basic QDialog, extended with some quality-of-life improvements
"""

from PyQt5.QtWidgets import QDialog, QWidget

from ..helpers.common_interface import CommonWidgetInterface

from ..._wrappers.types import ModuleType
from ..._wrappers.typing import Optional

__all__ = ["BasicDialog"]


class BasicDialog(QDialog):
    def __init__(
        self,
        form_module: Optional[ModuleType] = None,
        parent: Optional[QWidget] = None,
        **kwargs
    ):
        super().__init__(parent=parent, **kwargs)
        self.parent = parent  # type: ignore FIXME: don't overwrite
        self.interface = CommonWidgetInterface(self)
        # Set up UI from pre-generated UI form:
        if form_module:
            self.form = form_module.Ui_Dialog()
            self.form.setupUi(self)
        self._setupUI()
        self._setupEvents()
        self._setupShortcuts()

    # WIDGET SET-UP

    def _setupUI(self) -> None:
        """
        Set up any type of subsequent UI modifications
        (e.g. adding custom widgets on top of form)
        """
        pass

    def _setupEvents(self) -> None:
        """Set up any type of event bindings"""
        pass

    def _setupShortcuts(self) -> None:
        """Set up any type of keyboard shortcuts"""
        pass

    # DIALOG OPEN/CLOSE

    def _onClose(self) -> None:
        """Executed whenever dialog closed"""
        pass

    def _onAccept(self) -> None:
        """Executed only if dialog confirmed"""
        pass

    def _onReject(self) -> None:
        """Executed only if dialog dismissed"""
        pass

    def accept(self) -> None:
        """Overwrites default accept() to control close actions"""
        self._onClose()
        self._onAccept()
        super().accept()

    def reject(self) -> None:
        """Overwrites default reject() to control close actions"""
        self._onClose()
        self._onReject()
        super().reject()
