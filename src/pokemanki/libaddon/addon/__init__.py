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

import os

from ..._version import __version__

from .._wrappers.typing import NamedTuple

from ..anki import ANKI
from ..util.filesystem import ensureExists

__all__ = ["__version__", "AddonData", "ADDON"]


class AddonData(NamedTuple):

    # Set by add-on
    NAME: str = "Pokémanki"
    DEFAULT_MODULE: str = "pokemanki"  # != actual module name in AnkiWeb releases
    REPO: str = "https://github.com/zjosua/Pokemanki"
    ID = "1041307953"
    VERSION = __version__
    LICENSE = "GNU AGPLv3"
    AUTHORS = (
        {
            "name": "Exkywor",
            "years": "2022",
            "contact": "https://github.com/Exkywor",
        },
        {
            "name": "sivenchinniah",
            "years": "2019 - 2021",
            "contact": "https://github.com/sivenchinniah",
        },
        {
            "name": "zjosua",
            "years": "2022",
            "contact": "https://github.com/zjosua",
        },
    )
    AUTHOR_MAIL = ""
    LIBRARIES = ()
    CONTRIBUTORS = (
        "andyxang",
        "Kyle Mills (khonkhortisan)",
        "Yoonchae Lee (BlueGreenMagick)",
    )
    SPONSORS: tuple = ()
    MEMBERS_CREDITED: tuple = ()
    MEMBERS_TOP: tuple = ()
    LINKS: dict = {}

    # Set by libaddon
    _name_components = __name__.split(".")
    MODULE = _name_components[0]
    LIBADDON = _name_components[-1]
    print(ANKI.PATH_ADDONS, MODULE)
    PATH_ADDON = os.path.join(ANKI.PATH_ADDONS, MODULE)

    # Lazy-loaded attributes that are used more rarely
    @property
    def PATH_USER_FILES(self) -> str:
        user_files = os.path.join(self.PATH_ADDON, "user_files")
        return ensureExists(user_files)


# add-on properties "singleton"
ADDON = AddonData("Pokémanki")


def registerAddon(addon: AddonData):
    global ADDON
    ADDON = addon
