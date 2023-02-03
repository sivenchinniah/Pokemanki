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
Custom color-chooser
"""

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QColorDialog, QPushButton, QWidget

from ..._wrappers.typing import Optional


class QColorButton(QPushButton):
    def __init__(self, parent: Optional[QWidget] = None, color: str = "#000000"):
        super().__init__(parent=parent)
        self._updateButtonColor(color)
        self.clicked.connect(self._chooseColor)

    def _chooseColor(self) -> Optional[bool]:
        qcolour = QColor(self._color)
        dialog = QColorDialog(qcolour, parent=self)
        color = dialog.getColor()
        if not color.isValid():
            return False
        color = color.name()
        self._updateButtonColor(color)

    def _updateButtonColor(self, color: str):
        """Generate color preview pixmap and place it on button"""
        pixmap = QPixmap(128, 18)
        qcolour = QColor(0, 0, 0)
        qcolour.setNamedColor(color)
        pixmap.fill(qcolour)
        self.setIcon(QIcon(pixmap))
        self.setIconSize(QSize(128, 18))
        self._color = color

    def color(self) -> str:
        return self._color

    def setColor(self, color: str) -> None:
        self._updateButtonColor(color)
