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

from libaddon.util.filesystem import ensureExists
from pathlib import Path

import json

from .base import ConfigStorage
from ..errors import ConfigError

__all__ = ["JSONConfigStorage"]


class JSONConfigStorage(ConfigStorage):
    """e.g. JSON file in user_data folder"""

    name = "json"

    def __init__(self, *args, path: str = "", **kwargs):
        super().__init__(*args, **kwargs)
        self._path = path

    def _safePath(self, path: str) -> str:
        path_obj = Path(path)
        if not path_obj.is_file():
            ensureExists(str(path_obj.parent))
            with path_obj.open("w", encoding="utf-8") as f:
                json.dump({}, f)
        return str(path_obj)

    def _readData(self, path: str) -> dict:
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except (IOError, OSError, ValueError) as e:
            # log
            raise ConfigError(
                f"Could not read {self.name} storage at {path}:\n{str(e)}"
            )

    def _writeData(self, path: str, data: dict) -> None:
        try:
            with open(path, encoding="utf-8") as f:
                json.dump(data, f)
        except (IOError, OSError, ValueError) as e:
            # log
            raise ConfigError(
                f"Could not write to {self.name} storage at {path}:\n{str(e)}"
            )

    def _removeFile(self) -> None:
        path = self._safePath(self._path)
        Path(path).unlink()

    def load(self) -> bool:
        path = self._safePath(self._path)
        data = self._readData(path)
        super().load()
        return data is not None

    def save(self) -> None:
        path = self._safePath(self._path)
        self._writeData(path, self.data)
        super().save()

    def delete(self):
        self._removeFile()
        super().delete()
