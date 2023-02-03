# -*- coding: utf-8 -*-

# Pokémanki
# Copyright (C) 2022 Exkywor and zjosua
#
# This file is based on options_global.py from
# Cloze Overlapper Add-on for Anki
#
# Copyright (C) 2016-2019  Aristotelis P. <https://glutanimate.com/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the license file that accompanied this program
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
Config dialog
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from aqt import mw
from aqt.qt import *

from ..libaddon.gui.content.about import getAboutString

from .forms import pokemanki_options


class PokemankiOptions(QDialog):
    """Options dialog"""

    def __init__(self, mw):
        super(PokemankiOptions, self).__init__(parent=mw)
        # load qt-designer form:
        self.f = pokemanki_options.Ui_Dialog()
        self.f.setupUi(self)
        self.setup_ui()

    def setup_ui(self):
        self.f.buttonBox.accepted.connect(self.on_accept)
        self.f.buttonBox.rejected.connect(self.on_reject)

        about_string = getAboutString(title=True)
        self.f.htmlAbout.setHtml(about_string)

    def on_accept(self):
        self.close()

    def on_reject(self):
        self.close()


def invoke_pokemanki_options():
    """Invoke options dialog"""
    dialog = PokemankiOptions(mw)
    return dialog.exec()


def initialize_options():
    mw.addonManager.setConfigAction(ADDON.MODULE, invoke_pokemanki_options)
    # Set up menu entry:
    options_action = QAction("&Pokemanki Options...", mw)
    options_action.triggered.connect(invoke_pokemanki_options)
    mw.form.menuTools.addAction(options_action)
