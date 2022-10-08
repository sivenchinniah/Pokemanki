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

from .._wrappers.typing import NamedTuple

from ..anki import ANKI
from ..util.filesystem import ensureExists

__all__ = ["__version__", "AddonData", "ADDON"]


class AddonData(NamedTuple):

    # Set by add-on
    NAME: str = ""
    DEFAULT_MODULE: str = ""  # != actual module name in AnkiWeb releases
    REPO: str = ""
    ID: str = ""
    VERSION: str = ""
    LICENSE: str = ""
    AUTHORS: tuple = ()
    AUTHOR_MAIL: str = ""
    LIBRARIES: tuple = ()
    CONTRIBUTORS: tuple = ()
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
ADDON = AddonData("ADDON")


def registerAddon(addon: AddonData):
    global ADDON
    ADDON = addon
