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

from aqt import mw
from aqt.utils import tooltip

from .utils import get_json


class LegacyImporter(object):
    def __init__(self, conf_key: str = "pokemanki"):
        self.conf = {}
        self.conf_key = conf_key
        self.legacy_files = [
            "_alolanlist.json",
            "_decksortags.json",
            "_everstonelist.json",
            "_everstonepokemonlist.json",
            "_megastonelist.json",
            "_pokemankisettings.json",
            "_pokemanki.json",
            "_prestigelist.json",
            "_tagmon.json",
            "_tagmonsettings.json",
            "_tags.json",
            "_trades.json",
        ]
        self.default_conf = {
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

    def import_legacy_conf(self) -> None:
        """Import legacy config and progress directly to collection

        Set missing keys to default value in case of partial import.
        """

        self._conf_from_legacy_files()
        if self.conf != {}:
            for key, val in self.default_conf.items():
                self.conf.setdefault(key, val)
            for key, val in self.default_conf["evolution_thresholds"].items():
                self.conf["evolution_thresholds"].setdefault(key, val)
            mw.col.set_config(self.conf_key, self.conf)
            tooltip("Legacy Pokémanki settings and progress imported.")
            print("Legacy Pokémanki settings and progress imported.")

    def _conf_from_legacy_files(self) -> None:
        for lfile in self.legacy_files:
            if not get_json(lfile):
                continue
            if lfile == "_alolanlist.json":
                self.conf["alolanlist"] = get_json(lfile)
            elif lfile == "_decksortags.json":
                self.conf["decks_or_tags"] = get_json(lfile)
                if self.conf["decks_or_tags"] == "":
                    self.conf["decks_or_tags"] = "decks"
                if self.conf["decks_or_tags"] == "Tags":
                    self.conf["decks_or_tags"] = "tags"
            elif lfile == "_everstonelist.json":
                self.conf["everstonelist"] = get_json(lfile)
            elif lfile == "_everstonepokemonlist.json":
                self.conf["everstonepokemonlist"] = get_json(lfile)
            elif lfile == "_megastonelist.json":
                self.conf["everstonepokemonlist"] = get_json(lfile)
            elif lfile == "_pokemankisettings.json":
                if not self.conf.get("evolution_thresholds", None):
                    self.conf["evolution_thresholds"] = {}
                self.conf["evolution_thresholds"]["decks"] = get_json(lfile)
            elif lfile == "_pokemanki.json":
                self.conf["pokemon_list"] = get_json(lfile)
            elif lfile == "_prestigelist.json":
                self.conf["prestigelist"] = get_json(lfile)
            elif lfile == "_tagmon.json":
                self.conf["tagmon_list"] = get_json(lfile)
            elif lfile == "_tagmonsettings.json":
                if not self.conf.get("evolution_thresholds", None):
                    self.conf["evolution_thresholds"] = {}
                self.conf["evolution_thresholds"]["tags"] = get_json(lfile)
            elif lfile == "_tags.json":
                self.conf["tags"] = get_json(lfile)
            elif lfile == "_trades.json":
                self.conf["trades"] = get_json(lfile)

        if self.conf != {} and not self.conf.get("decks_or_tags", None):
            self.conf["decks_or_tags"] = "decks"
