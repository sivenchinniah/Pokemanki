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

import os
import ctypes
import csv
import inspect
import platform
import random
from datetime import date as dt

from aqt.utils import showInfo
from aqt.qt import *
from aqt.webview import AnkiWebView

from .config import get_local_conf, get_synced_conf, save_synced_conf
from .utils import *

from .gui.pokemanki_trade import *


class Trades:
    _trade_window = None

    def __init__(self, mw):
        self.mw = mw
        self.dirname = os.path.dirname(
            os.path.abspath(inspect.getfile(inspect.currentframe()))
        )
        self.mediafolder = mediafolder
        self.allpokemon = get_pokemon_records()
        self.f = get_synced_conf()["decks_or_tags"]

        self._trade_window = TradeWindow(mw, self)

    def open(self):
        """
        Open the Trade window
        """
        updated_trades = self._update_trades()
        if not updated_trades:
            showInfo(
                text="No trades are possible at the moment.",
                parent=mw,
                title="Pokémanki",
            )
            return
        self._trade_window.open(self.trades)

    def on_bridge_cmd(self, cmd):
        if cmd in ["0", "1", "2"]:
            self._make_trade(self.trades[int(cmd)][0], self.trades[int(cmd)][1])

    def _get_new_trades(self):
        """
        Get new trades.
        """
        self.trades = []
        i = 0
        f = self.f
        want = []

        deckmonlist = get_synced_conf()[
            "tagmon_list" if f == "tags" else "pokemon_list"
        ]
        if deckmonlist:
            sorteddeckmonlist = list(reversed(deckmonlist))
            noeggslist = []
            for item in sorteddeckmonlist:
                if int(item[2]) >= 5:
                    noeggslist.append(item)
            deckmons = []
            # Avoid duplicate Pokémon
            for item in noeggslist:
                for thing in deckmons:
                    if item[1] == thing[1]:
                        break
                else:
                    deckmons.append(item)
            deckmonlist = deckmons
        else:
            no_pokemon()
            return

        possiblehaveslist = []
        graderanges = {
            "F": ["E", "F"],
            "E": ["D", "E", "F"],
            "D": ["C", "D", "E"],
            "C": ["B", "C", "D"],
            "B": ["A", "B", "C"],
            "A": ["A", "B"],
        }
        while i < 3:
            randno = random.randint(0, len(deckmonlist) - 1)
            pokemon = deckmonlist[randno]
            for item in self.allpokemon:
                if pokemon[0] == item[0]:
                    want = item

            possiblehaves = []
            for item in self.allpokemon:
                if item[1] in graderanges[want[1]] and (
                    item[2] < int(pokemon[2]) < item[3]
                ):
                    possiblehaves.append(item)

            if len(possiblehaves) > 1:
                randno = random.randint(0, len(possiblehaves) - 1)
                have = possiblehaves[randno]
            elif len(possiblehaves) == 1:
                have = possiblehaves[0]
            else:
                i += 1
                continue

            if have[0].startswith("Eevee") and want[0].startswith("Eevee"):
                self.trades.append(
                    (
                        ("Eevee", have[1], have[2], have[3]),
                        ("Eevee", want[1], want[2], want[3]),
                    )
                )
            elif have[0].startswith("Eevee"):
                self.trades.append((("Eevee", have[1], have[2], have[3]), want))
            elif want[0].startswith("Eevee"):
                self.trades.append((have, ("Eevee", want[1], want[2], want[3])))
            else:
                self.trades.append((have, want))

            possiblehaveslist.append(possiblehaves)
            i += 1

        date = dt.today().strftime("%d/%m/%Y")
        if f == "tags":
            tradeData = [date, self.trades, "tags"]
        else:
            tradeData = [date, self.trades, "decks"]
        testData = [date, self.trades, possiblehaveslist]
        save_synced_conf("trades", tradeData)

    def _update_trades(self):
        f = self.f
        tradeData = get_synced_conf()["trades"]
        if tradeData:
            date = dt.today().strftime("%d/%m/%Y")

            # Get new trades if either the date or "decks vs tags" mode have changed
            if len(tradeData) == 3 and date == tradeData[0]:
                if f == tradeData[2]:
                    self.trades = tradeData[1]
                else:
                    self._get_new_trades()
                    tradeData = get_synced_conf()["trades"]
            else:
                self._get_new_trades()
                tradeData = get_synced_conf()["trades"]
        else:
            self._get_new_trades()
            tradeData = get_synced_conf()["trades"]

        return not (tradeData == [] or tradeData[1] == [])

    def _make_trade(self, have, want):
        """
        Make a trade.
        :param tuple have: Pokémon available to trade.
        :param tuple want: Pokémon wanted for trade.
        """
        possiblefits = []
        f = self.f

        if f == "tags":
            deckmonlist = get_synced_conf()["tagmon_list"]
            if deckmonlist:
                sorteddeckmonlist = list(reversed(deckmonlist))
                deckmons = []
                for item in sorteddeckmonlist:
                    for thing in deckmons:
                        if item[1] == thing[1]:
                            break
                    else:
                        deckmons.append(item)
                deckmonlist = deckmons
            else:
                no_pokemon()
                return
        else:
            deckmonlist = get_synced_conf()["pokemon_list"]
            if deckmonlist:
                sorteddeckmonlist = list(reversed(deckmonlist))
                deckmons = []
                for item in sorteddeckmonlist:
                    for thing in deckmons:
                        if item[1] == thing[1]:
                            break
                    else:
                        deckmons.append(item)
                deckmonlist = deckmons
            else:
                no_pokemon()
                return
        for item in deckmonlist:
            if (
                item[0] == want[0]
                or (item[0].startswith("Eevee") and want[0] == "Eevee")
                and int(item[2]) >= 5
            ):
                possiblefits.append(item)
        if possiblefits == []:
            showInfo(
                "Sorry, you do not have the Pokemon needed to complete this trade.",
                parent=mw,
                title="Pokémanki",
            )
            return
        displaylist = []
        for item in possiblefits:
            deckname = mw.col.decks.name(item[1])
            if len(item) == 4:
                if item[0].startswith("Eevee"):
                    displaytext = "%s - Eevee (Level %s) from %s" % (
                        item[3],
                        int(item[2]),
                        deckname,
                    )
                else:
                    displaytext = "%s - %s (Level %s) from %s" % (
                        item[3],
                        item[0],
                        int(item[2]),
                        deckname,
                    )
            else:
                if item[0].startswith("Eevee"):
                    displaytext = "Eevee (Level %s) from %s" % (int(item[2]), deckname)
                else:
                    displaytext = "%s (Level %s) from %s" % (
                        item[0],
                        int(item[2]),
                        deckname,
                    )
            displaylist.append(displaytext)

        totallist = list(zip(possiblefits, displaylist))
        possiblepokemon = QWidget()
        inp, ok = QInputDialog.getItem(
            possiblepokemon,
            "Pokémanki",
            "Choose a Pokemon to trade for %s" % have[0],
            displaylist,
            0,
            False,
        )
        tradepokemon = []
        if ok and inp:
            for thing in totallist:
                if inp in thing:
                    tradepokemon = thing[0]
                    displaytext = inp
        if not tradepokemon:
            return

        confirmation = QMessageBox()
        confirmation.setWindowTitle("Pokémanki")
        confirmation.setText(
            "Are you sure you want to trade your %s for a %s" % (displaytext, have[0])
        )

        confirmation.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        confirmation.setDefaultButton(QMessageBox.StandardButton.No)
        result = confirmation.exec()
        if result == QMessageBox.StandardButton.Yes:
            modifieddeckmonlist = []
            for item in deckmonlist:
                if item[1] == tradepokemon[1]:
                    if have[0] == "Eevee":
                        eevee = random.randint(1, 3)
                        newpokemon = ("Eevee%s" % eevee, item[1], item[2])
                    else:
                        newpokemon = (have[0], item[1], item[2])
                    modifieddeckmonlist.append(newpokemon)
                else:
                    modifieddeckmonlist.append(item)
            save_synced_conf("pokemon_list", modifieddeckmonlist)
            self._trade_window.done()
            showInfo(
                f"You have traded your {displaytext} for a {have[0]}",
                parent=mw,
                title="Pokémanki",
            )


def get_pokemon_records():
    """
    Generate a list of all Pokémon based on the user's generation configuration.
    :return: List of pokemon records.
    :rtype: List
    """
    pokemon_records = []
    csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen1.csv"
    pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))

    if get_local_conf()["gen2"]:
        csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen2.csv"
        pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))

        if get_local_conf()["gen4_evolutions"]:
            csv_fpath = (
                currentdirname / "pokemon_evolutions" / "pokemon_gen1_plus2_plus4.csv"
            )
            pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
            csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen2_plus4.csv"
            pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
        else:
            csv_fpath = (
                currentdirname / "pokemon_evolutions" / "pokemon_gen1_plus2_no4.csv"
            )
            pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
            csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen2_no4.csv"
            pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
    else:
        if get_local_conf()["gen4_evolutions"]:
            # a lot of gen 4 evolutions that affect gen 1 also include gen 2 evolutions
            # so let's just include gen 2 for these evolution lines
            csv_fpath = (
                currentdirname / "pokemon_evolutions" / "pokemon_gen1_plus2_plus4.csv"
            )
            pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
        else:
            csv_fpath = (
                currentdirname / "pokemon_evolutions" / "pokemon_gen1_no2_no4.csv"
            )
            pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))

    if get_local_conf()["gen3"]:
        csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen3.csv"
        pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
    if get_local_conf()["gen4"]:
        csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen4.csv"
        pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
    if get_local_conf()["gen5"]:
        csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen5.csv"
        pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))

    return pokemon_records


def pokemonLevelRangesFromCsv(csv_fpath):
    """
    Get the list of evolution level ranges for all Pokémon.
    :param str csv_fpath: Path of the csv containing the evolution list
    :return: List of pokemon ranges.
    :rtype: List
    """
    pokemon_records = []

    with open(csv_fpath, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")

        for line in csv_reader:
            pokemon = line["pokemon"]
            tier = line["tier"]
            first_ev_lv = line["first_evolution_level"]
            if first_ev_lv.isnumeric():
                first_ev_lv = int(first_ev_lv)
            else:
                first_ev_lv = None
            first_ev = line["first_evolution"]
            if first_ev == "NA":
                first_ev = None
            second_ev_lv = line["second_evolution_level"]
            if second_ev_lv.isnumeric():
                second_ev_lv = int(second_ev_lv)
            else:
                second_ev_lv = None
            second_ev = line["second_evolution"]
            if second_ev == "NA":
                second_ev = None

            pk1_lo_lv = 0
            if first_ev_lv:
                pk1_hi_lv = first_ev_lv
            else:
                pk1_hi_lv = 100
            pokemon_records.append((pokemon, tier, pk1_lo_lv, pk1_hi_lv))

            if first_ev is not None:
                pk2_lo_lv = pk1_hi_lv
                if second_ev_lv:
                    pk2_hi_lv = second_ev_lv
                else:
                    pk2_hi_lv = 100
                pokemon_records.append((first_ev, tier, pk2_lo_lv, pk2_hi_lv))

            if second_ev is not None:
                pk3_lo_lv = pk2_hi_lv
                pk3_hi_lv = 100
                pokemon_records.append((second_ev, tier, pk3_lo_lv, pk3_hi_lv))

    return pokemon_records
