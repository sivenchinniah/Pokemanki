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

from aqt.qt import *
from aqt.utils import showInfo, tooltip

from .config import (
    get_synced_conf,
    save_synced_conf,
    setup_default_synced_conf,
)
from .tags import Tags
from .utils import *

# Nickname Settings


def Nickname():
    deckmonlist, f = get_pokemons()
    if deckmonlist is None:
        return

    displaylist = []
    for item in deckmonlist:
        deckname = mw.col.decks.name(item[1])
        if len(item) == 4:
            if item[2] < 5:
                displaytext = "%s - Egg from %s" % (item[3], deckname)
            elif item[0].startswith("Eevee"):
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
            if item[2] < 5:
                displaytext = "Egg from %s" % (deckname)
            elif item[0].startswith("Eevee"):
                displaytext = "Eevee (Level %s) from %s" % (int(item[2]), deckname)
            else:
                displaytext = "%s (Level %s) from %s" % (
                    item[0],
                    int(item[2]),
                    deckname,
                )
        displaylist.append(displaytext)
    totallist = list(zip(deckmonlist, displaylist))
    nicknamewindow = QWidget()
    inp, ok = QInputDialog.getItem(
        nicknamewindow,
        "Pokémanki",
        "Choose a Pokémon who you would like to give a new nickname",
        displaylist,
        0,
        False,
    )
    deckmon = []
    nickname = ""
    if ok and inp:
        for thing in totallist:
            if inp in thing:
                deckmon = thing[0]
                displaytext = inp
    if not deckmon:
        return
    if len(deckmon) == 4:
        nickname = deckmon[3]
    inp, ok = QInputDialog.getText(
        nicknamewindow,
        "Pokémanki",
        ("Enter a new nickname for %s (leave blank to remove nickname)" % displaytext),
    )
    if ok:
        if inp:
            nickname = inp
            deckmon = [deckmon[0], deckmon[1], deckmon[2], nickname]
            if int(deckmon[2]) < 5:
                showInfo(
                    f"New nickname given to Egg - {nickname}.",
                    parent=mw,
                    title="Pokémanki",
                )
            elif deckmon[0].startswith("Eevee"):
                showInfo(
                    f"New nickname given to Eevee - {nickname}.",
                    parent=mw,
                    title="Pokémanki",
                )
            else:
                showInfo(
                    f"New nickname given to {deckmon[0]} - {nickname}.",
                    parent=mw,
                    title="Pokémanki",
                )
        else:
            deckmon = [deckmon[0], deckmon[1], deckmon[2]]
            if int(deckmon[2]) < 5:
                showInfo("Nickname removed from Egg", parent=mw, title="Pokémanki")
            elif deckmon[0].startswith("Eevee"):
                showInfo("Nickname removed from Eevee", parent=mw, title="Pokémanki")
            else:
                showInfo(
                    f"Nickname removed from {deckmon[0]}", parent=mw, title="Pokémanki"
                )
    modifieddeckmonlist = []
    for item in deckmonlist:
        if item[1] == deckmon[1]:
            modifieddeckmonlist.append(deckmon)
        else:
            modifieddeckmonlist.append(item)
    if f == "tags":
        save_synced_conf("tagmon_list", modifieddeckmonlist)
    else:
        save_synced_conf("pokemanki_list", modifieddeckmonlist)


def Toggle():
    window = QWidget()
    items = ("Decks (Default)", "Tags")
    by = get_synced_conf()["decks_or_tags"]
    default = 0
    if by == "tags":
        default = 1
    inp, ok = QInputDialog.getItem(
        window,
        "Pokémanki",
        "Choose how you would like Pokémanki to assign you Pokémon.",
        items,
        default,
        False,
    )
    if ok and inp:
        if inp == "Tags":
            save_synced_conf("decks_or_tags", "tags")
            tags = Tags()
            tags.tagMenu()
        else:
            save_synced_conf("decks_or_tags", "decks")

        from .main import build_menu

        build_menu()


# Threshold Settings


def ThresholdSettings():
    global thresholdlist
    # Find recommended number of cards for starter Pokemon threshold (based on deck with highest number of cards).
    decklist = mw.col.decks.allIds()
    sumlist = []
    for deck in decklist:
        sumlist.append(len(mw.col.decks.cids(deck)))
    recommended = 0.797 * max(sumlist)
    # Refresh threshold settings
    thresholdlist = get_synced_conf()["evolution_thresholds"]["decks"]
    # Make settings window (input dialog)
    window = QWidget()
    inp, ok = QInputDialog.getInt(
        window,
        "Pokémanki",
        (
            "Change number of cards needed in a deck to get a starter Pokémon (recommended %d)"
            % recommended
        ),
        value=thresholdlist[4],
    )
    if ok:
        # Make sure threshold is at least 10
        if inp < 10:
            showInfo(
                "Number must be at least ten",
                parent=mw,
                type="critical",
                title="Pokémanki",
            )
        # Change settings and save them if the threshold is changed
        elif inp != thresholdlist[4]:
            newthresholdlist = [
                int(0.1 * inp),
                int(0.25 * inp),
                int(0.5 * inp),
                int(0.75 * inp),
                int(inp),
            ]
            conf = get_synced_conf()["evolution_thresholds"]
            conf["decks"] = newthresholdlist
            save_synced_conf("evolution_thresholds", conf)
            # Message box confirming change
            showInfo("Your settings have been changed", parent=mw, title="Pokémanki")
    # Show the window
    window.show()


def reset_pokemanki():
    # Make message box
    resetwindow = QMessageBox()
    resetwindow.setWindowTitle("Pokémanki")
    resetwindow.setText(
        """
        Are you sure you want to reset your Pokémon?
        This will reset all your synced settings.
        All your Pokémon will be lost - both in deck and tag mode.
        """
    )
    resetwindow.setStandardButtons(
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    resetwindow.setDefaultButton(QMessageBox.StandardButton.No)
    resetresult = resetwindow.exec()
    # Reset synced Pokémanki config if Yes
    if resetresult == QMessageBox.StandardButton.Yes:
        setup_default_synced_conf()
        # TODO reset everstone? and other stuff?
        # Message box confirming reset
        showInfo("Pokémanki config reset", parent=mw, title="Pokémanki")


def MovetoBottom():
    showInfo(
        "Please restart Anki to see your updated settings.",
        parent=mw,
        title="Pokémanki",
    )


def MovetoTop():
    showInfo(
        "Please restart Anki to see your updated settings.",
        parent=mw,
        title="Pokémanki",
    )


def giveEverstone():
    pokemon, f = get_pokemons()
    if pokemon is None:
        return
    everstonelist = get_synced_conf()["everstonelist"]
    everstonepokemonlist = get_synced_conf()["everstonepokemonlist"]

    everstoneables = []
    for item in pokemon:
        if f:
            cb = "%s (Level %s) from %s" % (item[0], item[2], item[1])
        else:
            cb = "%s (Level %s) from %s" % (
                item[0],
                item[2],
                mw.col.decks.name(item[1]),
            )
        if item[1] in everstonelist:
            continue
        elif cb in everstoneables:
            continue
        else:
            everstoneables.append(cb)
    if not everstoneables:
        tooltip("You don't have any pokemons that can get an everstone")
        return
    window = QWidget()
    inp, ok = QInputDialog.getItem(
        window,
        "Pokémanki",
        "Select a Pokemon you would like to give an everstone to.",
        sorted(everstoneables),
        0,
        False,
    )
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        everstone_pokemon_name = inp.split(" (Level ")[0]
        if f:
            everstonelist.append(item)
            everstonepokemonlist.append(everstone_pokemon_name)
        else:
            everstonelist.append(mw.col.decks.id(item))
            everstonepokemonlist.append(everstone_pokemon_name)
        showInfo("Please restart Anki to see changes.", parent=mw, title="Pokémanki")
    save_synced_conf("everstonelist", everstonelist)
    save_synced_conf("everstonepokemonlist", everstonepokemonlist)


def takeEverstone():
    pokemon, f = get_pokemons()
    if pokemon is None:
        return
    everstonelist = get_synced_conf()["everstonelist"]
    everstonepokemonlist = get_synced_conf()["everstonepokemonlist"]
    if not everstonelist:
        showInfo(
            "None of your Pokémon are holding everstones.", parent=mw, title="Pokémanki"
        )
        return
    possibleuneverstones = []
    for thing in everstonelist:
        for item in pokemon:
            if item[1] == thing:
                if f:
                    cb = "%s from %s" % (item[0], item[1])
                else:
                    cb = "%s from %s" % (item[0], mw.col.decks.name(item[1]))
                if cb in possibleuneverstones:
                    continue
                else:
                    possibleuneverstones.append(cb)
        else:
            continue
    window = QWidget()
    inp, ok = QInputDialog.getItem(
        window,
        "Pokémanki",
        "Select a Pokemon whose everstone you would like to take.",
        sorted(possibleuneverstones),
        0,
        False,
    )
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        if f:
            everstonelist.remove(item)
            everstonepokemonlist.remove(textlist[0])
        else:
            everstonelist.remove(mw.col.decks.id(item))
            everstonepokemonlist.remove(textlist[0])
        showInfo(
            "Please restart Anki to see your changes.", parent=mw, title="Pokémanki"
        )
    save_synced_conf("everstonelist", everstonelist)


def giveMegastone():
    pokemon, f = get_pokemons()
    if pokemon is None:
        return
    megastonelist = get_synced_conf()["megastonelist"]
    megastoneables = []
    for item in pokemon:
        if item[2] >= 70:
            if f:
                cb = "%s (Level %s) from %s" % (item[0], item[2], item[1])
            else:
                cb = "%s (Level %s) from %s" % (
                    item[0],
                    item[2],
                    mw.col.decks.name(item[1]),
                )
            if item[1] in megastonelist:
                continue
            elif cb in megastoneables:
                continue
            else:
                megastoneables.append(cb)
        else:
            continue
    if not megastoneables:
        tooltip("You don't have any pokemons that can get a mega stone")
        return
    window = QWidget()
    inp, ok = QInputDialog.getItem(
        window,
        "Pokémanki",
        "Select a Pokemon you would like to give a mega stone to",
        sorted(megastoneables),
        0,
        False,
    )
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        if f:
            megastonelist.append(item)
        else:
            megastonelist.append(mw.col.decks.id(item))
        showInfo(
            "Please restart Anki to see your changes.", parent=mw, title="Pokémanki"
        )
    save_synced_conf("megastonelist", megastonelist)


def takeMegastone():
    pokemon, f = get_pokemons()
    if pokemon is None:
        return
    megastonelist = get_synced_conf()["megastonelist"]
    if not megastonelist:
        showInfo(
            "None of your Pokémon are holding mega stones.",
            parent=mw,
            title="Pokémanki",
        )
        return
    possibleunmegastones = []
    for thing in megastonelist:
        for item in pokemon:
            if item[1] == thing:
                if f:
                    cb = "%s from %s" % (item[0], item[1])
                else:
                    cb = "%s from %s" % (item[0], mw.col.decks.name(item[1]))
                if cb in possibleunmegastones:
                    continue
                else:
                    possibleunmegastones.append(cb)
        else:
            continue
    window = QWidget()
    inp, ok = QInputDialog.getItem(
        window,
        "Pokémanki",
        "Select a Pokemon whose mega stone you would like to take",
        sorted(possibleunmegastones),
        0,
        False,
    )
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        if f:
            megastonelist.remove(item)
        else:
            megastonelist.remove(mw.col.decks.id(item))
        showInfo(
            "Please restart Anki to see your changes.", parent=mw, title="Pokémanki"
        )
    save_synced_conf("megastonelist", megastonelist)


def giveAlolanPassport():
    pokemon, f = get_pokemons()
    if pokemon is None:
        return
    alolanlist = get_synced_conf()["alolanlist"]

    alolanables = []
    for item in pokemon:
        if f:
            cb = "%s (Level %s) from %s" % (item[0], item[2], item[1])
        else:
            cb = "%s (Level %s) from %s" % (
                item[0],
                item[2],
                mw.col.decks.name(item[1]),
            )
        if item[1] in alolanlist:
            continue
        elif cb in alolanables:
            continue
        else:
            alolanables.append(cb)

    if not alolanables:
        tooltip("You don't have any pokemons that you can give Alolan Passport to")
        return
    window = QWidget()
    inp, ok = QInputDialog.getItem(
        window,
        "Pokémanki",
        "Select a Pokemon you would like to give an Alolan Passport to.",
        sorted(alolanables),
        0,
        False,
    )
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        alolan_pokemon_name = inp.split(" (Level ")[0]
        if f:
            alolanlist.append(item)
        else:
            alolanlist.append(mw.col.decks.id(item))
        showInfo("Please restart Anki to see changes.", parent=mw, title="Pokémanki")
    save_synced_conf("alolanlist", alolanlist)


def takeAlolanPassport():
    pokemon, f = get_pokemons()
    if pokemon is None:
        return
    alolanlist = get_synced_conf()["alolanlist"]
    if not alolanlist:
        showInfo(
            "None of your Pokémon are holding an Alolan Passport.",
            parent=mw,
            title="Pokémanki",
        )
        return
    possibleunalolans = []
    for thing in alolanlist:
        for item in pokemon:
            if item[1] == thing:
                if f:
                    cb = "%s from %s" % (item[0], item[1])
                else:
                    cb = "%s from %s" % (item[0], mw.col.decks.name(item[1]))
                if cb in possibleunalolans:
                    continue
                else:
                    possibleunalolans.append(cb)
        else:
            continue
    window = QWidget()
    inp, ok = QInputDialog.getItem(
        window,
        "Pokémanki",
        "Select a Pokemon whose Alolan Passport you would like to take.",
        sorted(possibleunalolans),
        0,
        False,
    )
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        if f:
            alolanlist.remove(item)
        else:
            alolanlist.remove(mw.col.decks.id(item))
        showInfo(
            "Please restart Anki to see your changes.", parent=mw, title="Pokémanki"
        )
    save_synced_conf("alolanlist", alolanlist)


def PrestigePokemon():
    pokemon, f = get_pokemons()
    if pokemon is None:
        return
    prestigelist = get_synced_conf()["prestigelist"]
    possibleprestiges = []
    for item in pokemon:
        if item[2] >= 60:
            if f:
                cb = "%s (Level %s) from %s" % (item[0], item[2], item[1])
            else:
                cb = "%s (Level %s) from %s" % (
                    item[0],
                    item[2],
                    mw.col.decks.name(item[1]),
                )
            if item[1] in prestigelist:
                continue
            elif cb in possibleprestiges:
                continue
            else:
                possibleprestiges.append(cb)
        else:
            continue
    window = QWidget()
    if not possibleprestiges:
        tooltip("You don't have any pokemons with level > 60")
        return
    inp, ok = QInputDialog.getItem(
        window,
        "Pokémanki",
        "Select a Pokemon you would like to prestige (decreases level by 50, only availabe for Pokemon with level > 60)",
        sorted(possibleprestiges),
        0,
        False,
    )
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        if f:
            prestigelist.append(item)
        else:
            prestigelist.append(mw.col.decks.id(item))
        showInfo(
            "Please restart Anki to see your prestiged Pokémon.",
            parent=mw,
            title="Pokémanki",
        )
    save_synced_conf("prestigelist", prestigelist)


def UnprestigePokemon():
    pokemon, f = get_pokemons()
    if pokemon is None:
        return
    prestigelist = get_synced_conf()["prestigelist"]
    if not prestigelist:
        showInfo("You have no prestiged Pokémon.", parent=mw, title="Pokémanki")
        return
    possibleunprestiges = []
    for thing in prestigelist:
        for item in pokemon:
            if item[1] == thing:
                if f:
                    cb = "%s from %s" % (item[0], item[1])
                else:
                    cb = "%s from %s" % (item[0], mw.col.decks.name(item[1]))
                if cb in possibleunprestiges:
                    continue
                else:
                    possibleunprestiges.append(cb)
        else:
            continue
    if not possibleunprestiges:
        tooltip("You don't have any pokemons with prestige")
        return
    window = QWidget()
    inp, ok = QInputDialog.getItem(
        window,
        "Pokémanki",
        "Select a Pokemon you would like to unprestige",
        sorted(possibleunprestiges),
        0,
        False,
    )
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        if f:
            prestigelist.remove(item)
        else:
            prestigelist.remove(mw.col.decks.id(item))
        showInfo(
            "Please restart Anki to see your unprestiged Pokémon.",
            parent=mw,
            title="Pokémanki",
        )
    save_synced_conf("prestigelist", prestigelist)
