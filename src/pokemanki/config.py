# -*- coding: utf-8 -*-

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
