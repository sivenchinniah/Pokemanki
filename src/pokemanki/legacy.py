# -*- coding: utf-8 -*-

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

    def import_legacy_conf(self) -> None:
        """Import legacy config and progress directly to collection"""

        self._conf_from_legacy_files()
        if self.conf != {}:
            mw.col.set_config(self.conf_key, self.conf)
            tooltip("Legacy Pokémanki settings and progress imported.")

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
