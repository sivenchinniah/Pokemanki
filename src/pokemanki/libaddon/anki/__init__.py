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
Code primarily interacting with Anki
"""

from aqt import mw

from anki import version as anki_version
from anki.utils import isMac, isWin

from .._wrappers.typing import Optional


class AnkiData:

    PLATFORM = "win" if isWin else "mac" if isMac else "lin"
    VERSION = anki_version
    JSBRIDGE = "pycmd"

    @property
    def SCHEDVER(self) -> Optional[int]:
        if not mw or not mw.col:
            return None
        return mw.col.schedVer()

    @property
    def PATH_ADDONS(self) -> Optional[str]:
        if not mw or not mw.pm:
            # profile loading not finished, this should never happen at
            # add-on run time
            raise AttributeError("Profile not loaded")
        return mw.pm.addonFolder()

    @property
    def PATH_MEDIA(self) -> Optional[str]:
        if not mw or not mw.col:
            # collection not loaded, could happen intermittently during
            # transitional states like init, sync, or exit
            return None
        return mw.col.media.dir()

    def __repr__(self):
        # TODO: automate
        return str(
            {
                "PLATFORM": self.PLATFORM,
                "VERSION": self.VERSION,
                "JSBRIDGE": self.JSBRIDGE,
                "SCHEDVER": self.SCHEDVER,
                "PATH_ADDONS": self.PATH_ADDONS,
                "PATH_MEDIA": self.PATH_MEDIA,
            }
        )


ANKI = AnkiData()
