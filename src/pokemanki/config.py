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

from typing import Any

from aqt import mw


def init_config():
    if not get_synced_conf():

        from .legacy import LegacyImporter

        importer = LegacyImporter()
        importer.import_legacy_conf()
        if not get_synced_conf():
            setup_default_synced_conf()


def get_local_conf() -> dict:
    return mw.addonManager.getConfig(__name__)


def save_local_conf(config: str) -> None:
    mw.addonManager.writeConfig(__name__, config)


def get_synced_conf() -> Any:
    return mw.col.get_config("pokemanki", default=None)


def save_synced_conf(key: str, value: Any) -> None:
    """Write a single key of the "pokemanki" config of the collection.

    :param str key: Config key
    :param value: New config value
    :rtype: None
    """
    conf = get_synced_conf()
    conf[key] = value
    mw.col.set_config("pokemanki", conf)


def setup_default_synced_conf() -> None:
    default = {
        "alolanlist": [],
        "decks_or_tags": "decks",
        "everstonelist": [],
        "everstonepokemonlist": [],
        "evolution_thresholds": {
            "decks": [100, 250, 500, 750, 1000],
            "tags": [50, 125, 250, 375, 500],
        },
        "megastonelist": [],
        "pokemon_list": [],
        "prestigelist": [],
        "tagmon_list": [],
        "tags": [],
        "trades": [],
    }
    mw.col.set_config("pokemanki", default)
