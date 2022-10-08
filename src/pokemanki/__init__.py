# -*- coding: utf-8 -*-

# Pokémanki
# Copyright (C) 2022 Exkywor and zjosua

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from aqt import gui_hooks
from aqt.utils import showWarning


opened = False


def startup():
    global opened
    if opened:
        warning_text = "\n".join(
            (
                "Pokémanki does not support opening a second profile in one session.",
                "Please close Anki and reopen it again to the desired profile.",
                "Pokémanki may behave strangely",
            )
        )
        showWarning(warning_text, title="Pokémanki won't function properly")
        return

    opened = True
    from . import main


gui_hooks.profile_did_open.append(startup)
