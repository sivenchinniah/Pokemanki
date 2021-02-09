# Copyright 2019 Siven Chinniah

# JK please feel free to use this however you would like.

from .display import pokemonDisplay
from .tagmon import tagmonDisplay

import anki.stats
import aqt.overview
from anki.hooks import wrap
import shutil
import distutils.dir_util
import inspect, os
from aqt.qt import *
from aqt import mw
import json
from datetime import date
import random
import csv

from pathlib import Path

config = mw.addonManager.getConfig(__name__)

today = date.today()

# Find current directory
addon_dir = Path(__file__).parents[0]
currentdirname = addon_dir
# Assign Pokemon Image folder directory name
pkmnimgfolder = addon_dir  / "pokemon_images"
# Get to Anki2 folder
# ankifolder = os.path.dirname(os.path.dirname(currentdirname))
# Get to profile folder
if not mw.pm.name:
    profs = mw.pm.profiles()
    mw.pm.load(profs[0])
if not mw.pm.name:
    mw.showProfileManager()
profilename = mw.pm.name
profilefolder = Path(mw.pm.profileFolder())
mediafolder = Path(mw.col.media.dir())

def copy_directory(dir_addon: str, dir_anki: str):
    if not dir_anki:
        dir_anki = dir_addon
    fromdir = addon_dir / dir_addon
    todir = mediafolder / dir_anki
    if not fromdir.is_dir():
        return
    if todir.is_dir():
        shutil.copytree(fromdir, todir)
    else:
        distutils.dir_util.copy_tree(fromdir, todir)

def set_default(path: str, default = None):
    if not (mediafolder / path).is_file():
        with open(mediafolder / path, "w") as f:
            json.dump(default, f)

# Move Pokemon Image folder to collection.media folder if not already there (Anki reads from here when running anki.stats.py)
copy_directory("pokemon_images")

# Download threshold settings (or make from scratch if not already made)
set_default("_pokemankisettings.json", default = [100, 250, 500, 750, 1000])


# Nickname Settings
def Nickname():
    global mediafolder
    if os.path.exists("%s/_decksortags.json" % mediafolder):
        f = json.load(open("%s/_decksortags.json" % mediafolder))
    else:
        f = ""
    if f:
        if os.path.exists("%s/_tagmon.json" % mediafolder):
            deckmonlist = json.load(open("%s/_tagmon.json" % mediafolder))
        else:
            nopokemon = QMessageBox()
            nopokemon.setWindowTitle("Pokemanki")
            nopokemon.setText("Please open the Stats window to get your Pokémon.")
            nopokemon.exec_()
            return    
    else:
        if os.path.exists("%s/_pokemanki.json" % mediafolder):
            deckmonlist = json.load(open("%s/_pokemanki.json" % mediafolder))
        else:
            nopokemon = QMessageBox()
            nopokemon.setWindowTitle("Pokemanki")
            nopokemon.setText("Please open the Stats window to get your Pokémon.")
            nopokemon.exec_()
            return
    displaylist = []
    for item in deckmonlist:
        deckname = mw.col.decks.name(item[1])
        if len(item) == 4:
            if item[2] < 5:
                displaytext = "%s - Egg from %s" % (item[3], deckname)
            elif item[0].startswith("Eevee"):
                displaytext = "%s - Eevee (Level %s) from %s" % (item[3], int(item[2]), deckname)
            else:
                displaytext = "%s - %s (Level %s) from %s" % (item[3], item[0], int(item[2]), deckname)
        else:
            if item[2] < 5:
                displaytext = "Egg from %s" % (deckname)
            elif item[0].startswith("Eevee"):
                displaytext = "Eevee (Level %s) from %s" % (int(item[2]), deckname)
            else:
                displaytext = "%s (Level %s) from %s" % (item[0], int(item[2]), deckname)
        displaylist.append(displaytext)
    totallist = list(zip(deckmonlist, displaylist))
    nicknamewindow = QWidget()
    inp, ok = QInputDialog.getItem(nicknamewindow, "Pokemanki", "Choose a Pokémon who you would like to give a new nickname", displaylist, 0, False)
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
    inp, ok = QInputDialog.getText(nicknamewindow, "Pokemanki", ("Enter a new nickname for %s (leave blank to remove nickname)" % displaytext))
    if ok:
        if inp:
            nickname = inp
            deckmon = [deckmon[0], deckmon[1], deckmon[2], nickname]
            newnickname = QMessageBox()
            newnickname.setWindowTitle("Pokemanki")
            if int(deckmon[2]) < 5:
                newnickname.setText("New nickname given to Egg - %s" % (nickname))
            elif deckmon[0].startswith("Eevee"):
                newnickname.setText("New nickname given to Eevee - %s" % (nickname))
            else:
                newnickname.setText("New nickname given to %s - %s" % (deckmon[0], nickname))
            newnickname.exec_()
        else:
            deckmon = [deckmon[0], deckmon[1], deckmon[2]]
            nicknameremoved = QMessageBox()
            nicknameremoved.setWindowTitle("Pokemanki")
            if int(deckmon[2]) < 5:
                nicknameremoved.setText("Nickname removed from Egg")
            elif deckmon[0].startswith("Eevee"):
                nicknameremoved.setText("Nickname removed from Eevee")
            else:
                nicknameremoved.setText("Nickname removed from %s" % deckmon[0])
            nicknameremoved.exec_()
    modifieddeckmonlist = []
    for item in deckmonlist:
        if item[1] == deckmon[1]:
            modifieddeckmonlist.append(deckmon)
        else:
            modifieddeckmonlist.append(item)
    if f:
        with open(("%s/_tagmon.json" % mediafolder), "w") as f:
            json.dump(modifieddeckmonlist, f)
    else:
        with open(("%s/_pokemanki.json" % mediafolder), "w") as f:
            json.dump(modifieddeckmonlist, f)

def Toggle():
    global mediafolder
    window = QWidget()
    items = ("Decks (Default)", "Tags")
    inp, ok = QInputDialog.getItem(window, "Pokemanki", "Choose how you would like Pokemanki to assign you Pokémon.", items, 0, False)
    if ok and inp:
        if inp == "Tags":
            with open(("%s/_decksortags.json" % mediafolder), "w") as f:
                json.dump(inp, f)
            tags = Tags()
            tags.tagMenu()
            settingschanged = QMessageBox()
            settingschanged.setWindowTitle("Pokemanki")
            settingschanged.setText("Please restart Anki to see your updated Pokémon.")
            settingschanged.exec_()
        else:
            with open(("%s/_decksortags.json" % mediafolder), "w") as f:
                json.dump("", f)
            settingschanged = QMessageBox()
            settingschanged.setWindowTitle("Pokemanki")
            settingschanged.setText("Please restart Anki to see your updated Pokémon.")
            settingschanged.exec_()

# Threshold Settings
def ThresholdSettings():
    global thresholdlist
    global mediafolder
    # Find recommended number of cards for starter Pokemon threshold (based on deck with highest number of cards).
    decklist = mw.col.decks.allIds()
    sumlist = []
    for deck in decklist:
        sumlist.append(len(mw.col.decks.cids(deck)))
    recommended = .797 * max(sumlist)
    # Refresh threshold settings
    thresholdlist = json.load(open("%s/_pokemankisettings.json" % mediafolder))
    # Make settings window (input dialog)
    window = QWidget()
    inp, ok = QInputDialog.getInt(window, "Pokemanki", ("Change number of cards needed in a deck to get a starter Pokémon (recommended %d)" % recommended), value = thresholdlist[4])
    if ok:
        # Make sure threshold is at least 10
        if inp < 10:
            error = QMessageBox()
            error.setWindowTitle("Pokemanki")
            error.setText("Number must be at least ten")
            error.exec_()
        # Change settings and save them if the threshold is changed
        elif inp != thresholdlist[4]:
            newthresholdlist = [int(0.1*inp), int(0.25*inp), int(0.5*inp), int(0.75*inp), int(inp)]
            with open(("%s/_pokemankisettings.json" % mediafolder), "w") as f:
                json.dump(newthresholdlist, f)
            # Message box confirming change
            settingschanged = QMessageBox()
            settingschanged.setWindowTitle("Pokemanki")
            settingschanged.setText("Your settings have been changed")
            settingschanged.exec_()
    # Show the window
    window.show()

# Reset Pokemon
def ResetPokemon():
    global mediafolder
    # Make message box
    resetwindow = QMessageBox()
    resetwindow.setWindowTitle("Pokemanki")
    resetwindow.setText("Are you sure you want to reset your Pokémon?")
    resetwindow.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    resetwindow.setDefaultButton(QMessageBox.No)
    resetresult = resetwindow.exec_()
    # Clear pokemanki.json if Yes
    if resetresult == QMessageBox.Yes:
        with open(("%s/_pokemanki.json" % mediafolder), "w") as f:
            json.dump([], f)
        if os.path.exists("%s/_tagmon.json" % mediafolder):
            with open(("%s/_tagmon.json" % mediafolder), "w") as f:
                json.dump([], f)
        # Message box confirming reset
        resetdone = QMessageBox()
        resetdone.setWindowTitle("Pokemanki")
        resetdone.setText("Pokemon reset")
        resetdone.exec_()

def MovetoBottom():
    global mediafolder
    with open("%s/_toporbottom.json" % mediafolder, "w") as f:
        json.dump("bottom", f)
    settingschanged = QMessageBox()
    settingschanged.setWindowTitle("Pokemanki")
    settingschanged.setText("Please restart Anki to see your updated settings.")
    settingschanged.exec_()

def MovetoTop():
    global mediafolder
    with open("%s/_toporbottom.json" % mediafolder, "w") as f:
        json.dump("", f)
    settingschanged = QMessageBox()
    settingschanged.setWindowTitle("Pokemanki")
    settingschanged.setText("Please restart Anki to see your updated settings.")
    settingschanged.exec_()

def giveEverstone():
    global mediafolder
    if os.path.exists("%s/_decksortags.json" % mediafolder):
        f = json.load(open("%s/_decksortags.json" % mediafolder))
    else:
        f = ""
    if f:
        if os.path.exists("%s/_tagmon.json" % mediafolder):
            pokemon = json.load(open("%s/_tagmon.json" % mediafolder))
    else:
        if os.path.exists("%s/_pokemanki.json" % mediafolder):
            pokemon = json.load(open("%s/_pokemanki.json" % mediafolder))
    if os.path.exists("%s/_everstonelist.json" % mediafolder):
        everstonelist = json.load(open("%s/_everstonelist.json" % mediafolder))
    else:
        everstonelist = []
    if os.path.exists("%s/_everstonepokemonlist.json" % mediafolder):
        everstonepokemonlist = json.load(open("%s/_everstonepokemonlist.json" % mediafolder))
    else:
        everstonepokemonlist = []

    everstoneables = []
    for item in pokemon:
        if f:
            cb = ("%s (Level %s) from %s" % (item[0], item[2], item[1]))
        else:
            cb = ("%s (Level %s) from %s" % (item[0], item[2], mw.col.decks.name(item[1])))
        if item[1] in everstonelist:
            continue
        elif cb in everstoneables:
            continue
        else:
            everstoneables.append(cb)


    window = QWidget()
    inp, ok = QInputDialog.getItem(window, "Pokemanki", "Select a Pokemon you would like to give an everstone to.", sorted(everstoneables), 0, False)
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
        settingschanged = QMessageBox()
        settingschanged.setWindowTitle("Pokemanki")
        settingschanged.setText("Please restart Anki to see changes.")
        settingschanged.exec_()
    with open("%s/_everstonelist.json" % mediafolder, "w") as f:
        json.dump(everstonelist, f)
    with open("%s/_everstonepokemonlist.json" % mediafolder, "w") as f:
        json.dump(everstonepokemonlist, f)

def takeEverstone():
    global mediafolder
    if os.path.exists("%s/_decksortags.json" % mediafolder):
        f = json.load(open("%s/_decksortags.json" % mediafolder))
    else:
        f = ""
    if f:
        if os.path.exists("%s/_tagmon.json" % mediafolder):
            pokemon = json.load(open("%s/_tagmon.json" % mediafolder))
    else:
        if os.path.exists("%s/_pokemanki.json" % mediafolder):
            pokemon = json.load(open("%s/_pokemanki.json" % mediafolder))
    if os.path.exists("%s/_everstonelist.json" % mediafolder):
        everstonelist = json.load(open("%s/_everstonelist.json" % mediafolder))
    else:
        everstonelist = []
    if os.path.exists("%s/_everstonepokemonlist.json" % mediafolder):
        everstonepokemonlist = json.load(open("%s/_everstonepokemonlist.json" % mediafolder))
    else:
        everstonepokemonlist = []
    if not everstonelist:
        noeverstone = QMessageBox()
        noeverstone.setWindowTitle("Pokemanki")
        noeverstone.setText("None of your Pokémon are holding everstones.")
        noeverstone.exec_()
        return
    possibleuneverstones = []
    for thing in everstonelist:
        for item in pokemon:
            if item[1] == thing:
                if f:
                    cb = ("%s from %s" % (item[0], item[1]))
                else:
                    cb = ("%s from %s" % (item[0], mw.col.decks.name(item[1])))
                if cb in possibleuneverstones:
                    continue
                else:
                    possibleuneverstones.append(cb)
        else:
            continue
    window = QWidget()
    inp, ok = QInputDialog.getItem(window, "Pokemanki", "Select a Pokemon whose everstone you would like to take.", sorted(possibleuneverstones), 0, False)
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        if f:
            everstonelist.remove(item)
            everstonepokemonlist.remove(textlist[0])
        else:
            everstonelist.remove(mw.col.decks.id(item))
            everstonepokemonlist.remove(textlist[0])
        settingschanged = QMessageBox()
        settingschanged.setWindowTitle("Pokemanki")
        settingschanged.setText("Please restart Anki to see your changes.")
        settingschanged.exec_()
    with open("%s/_everstonelist.json" % mediafolder, "w") as f:
        json.dump(everstonelist, f)

def giveMegastone():
    global mediafolder
    if os.path.exists("%s/_decksortags.json" % mediafolder):
        f = json.load(open("%s/_decksortags.json" % mediafolder))
    else:
        f = ""
    if f:
        if os.path.exists("%s/_tagmon.json" % mediafolder):
            pokemon = json.load(open("%s/_tagmon.json" % mediafolder))
    else:
        if os.path.exists("%s/_pokemanki.json" % mediafolder):
            pokemon = json.load(open("%s/_pokemanki.json" % mediafolder))
    if os.path.exists("%s/_megastonelist.json" % mediafolder):
        megastonelist = json.load(open("%s/_megastonelist.json" % mediafolder))
    else:
        megastonelist = []
    megastoneables = []
    for item in pokemon:
        if item[2] >= 70:
            if f:
                cb = ("%s (Level %s) from %s" % (item[0], item[2], item[1]))
            else:
                cb = ("%s (Level %s) from %s" % (item[0], item[2], mw.col.decks.name(item[1])))
            if item[1] in megastonelist:
                continue
            elif cb in megastoneables:
                continue
            else:
                megastoneables.append(cb)
        else:
            continue
    window = QWidget()
    inp, ok = QInputDialog.getItem(window, "Pokemanki", "Select a Pokemon you would like to give a mega stone to", sorted(megastoneables), 0, False)
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        if f:
            megastonelist.append(item)
        else:
            megastonelist.append(mw.col.decks.id(item))
        settingschanged = QMessageBox()
        settingschanged.setWindowTitle("Pokemanki")
        settingschanged.setText("Please restart Anki to see your changes.")
        settingschanged.exec_()
    with open("%s/_megastonelist.json" % mediafolder, "w") as f:
        json.dump(megastonelist, f)  

def takeMegastone():
    global mediafolder
    if os.path.exists("%s/_decksortags.json" % mediafolder):
        f = json.load(open("%s/_decksortags.json" % mediafolder))
    else:
        f = ""
    if f:
        if os.path.exists("%s/_tagmon.json" % mediafolder):
            pokemon = json.load(open("%s/_tagmon.json" % mediafolder))
    else:
        if os.path.exists("%s/_pokemanki.json" % mediafolder):
            pokemon = json.load(open("%s/_pokemanki.json" % mediafolder))
    if os.path.exists("%s/_megastonelist.json" % mediafolder):
        megastonelist = json.load(open("%s/_megastonelist.json" % mediafolder))
    else:
        megastonelist = []
    if not megastonelist:
        nomegastone = QMessageBox()
        nomegastone.setWindowTitle("Pokemanki")
        nomegastone.setText("None of your Pokémon are holding mega stones.")
        nomegastone.exec_()
        return
    possibleunmegastones = []
    for thing in megastonelist:
        for item in pokemon:
            if item[1] == thing:
                if f:
                    cb = ("%s from %s" % (item[0], item[1]))
                else:
                    cb = ("%s from %s" % (item[0], mw.col.decks.name(item[1])))
                if cb in possibleunmegastones:
                    continue
                else:
                    possibleunmegastones.append(cb)
        else:
            continue
    window = QWidget()
    inp, ok = QInputDialog.getItem(window, "Pokemanki", "Select a Pokemon whose mega stone you would like to take", sorted(possibleunmegastones), 0, False)
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        if f:
            megastonelist.remove(item)
        else:
            megastonelist.remove(mw.col.decks.id(item))
        settingschanged = QMessageBox()
        settingschanged.setWindowTitle("Pokemanki")
        settingschanged.setText("Please restart Anki to see your changes.")
        settingschanged.exec_()
    with open("%s/_megastonelist.json" % mediafolder, "w") as f:
        json.dump(megastonelist, f)


def giveAlolanPassport():
    global mediafolder
    if os.path.exists("%s/_decksortags.json" % mediafolder):
        f = json.load(open("%s/_decksortags.json" % mediafolder))
    else:
        f = ""
    if f:
        if os.path.exists("%s/_tagmon.json" % mediafolder):
            pokemon = json.load(open("%s/_tagmon.json" % mediafolder))
    else:
        if os.path.exists("%s/_pokemanki.json" % mediafolder):
            pokemon = json.load(open("%s/_pokemanki.json" % mediafolder))
    if os.path.exists("%s/_alolanlist.json" % mediafolder):
        alolanlist = json.load(open("%s/_alolanlist.json" % mediafolder))
    else:
        alolanlist = []

    alolanables = []
    for item in pokemon:
        if f:
            cb = ("%s (Level %s) from %s" % (item[0], item[2], item[1]))
        else:
            cb = ("%s (Level %s) from %s" % (item[0], item[2], mw.col.decks.name(item[1])))
        if item[1] in alolanlist:
            continue
        elif cb in alolanables:
            continue
        else:
            alolanables.append(cb)


    window = QWidget()
    inp, ok = QInputDialog.getItem(window, "Pokemanki", "Select a Pokemon you would like to give an Alolan Passport to.", sorted(alolanables), 0, False)
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        alolan_pokemon_name = inp.split(" (Level ")[0]
        if f:
            alolanlist.append(item)
        else:
            alolanlist.append(mw.col.decks.id(item))
        settingschanged = QMessageBox()
        settingschanged.setWindowTitle("Pokemanki")
        settingschanged.setText("Please restart Anki to see changes.")
        settingschanged.exec_()
    with open("%s/_alolanlist.json" % mediafolder, "w") as f:
        json.dump(alolanlist, f)

def takeAlolanPassport():
    global mediafolder
    if os.path.exists("%s/_decksortags.json" % mediafolder):
        f = json.load(open("%s/_decksortags.json" % mediafolder))
    else:
        f = ""
    if f:
        if os.path.exists("%s/_tagmon.json" % mediafolder):
            pokemon = json.load(open("%s/_tagmon.json" % mediafolder))
    else:
        if os.path.exists("%s/_pokemanki.json" % mediafolder):
            pokemon = json.load(open("%s/_pokemanki.json" % mediafolder))
    if os.path.exists("%s/_alolanlist.json" % mediafolder):
        alolanlist = json.load(open("%s/_alolanlist.json" % mediafolder))
    else:
        alolanlist = []
    if not alolanlist:
        noalolan = QMessageBox()
        noalolan.setWindowTitle("Pokemanki")
        noalolan.setText("None of your Pokémon are holding an Alolan Passport.")
        noalolan.exec_()
        return
    possibleunalolans = []
    for thing in alolanlist:
        for item in pokemon:
            if item[1] == thing:
                if f:
                    cb = ("%s from %s" % (item[0], item[1]))
                else:
                    cb = ("%s from %s" % (item[0], mw.col.decks.name(item[1])))
                if cb in possibleunalolans:
                    continue
                else:
                    possibleunalolans.append(cb)
        else:
            continue
    window = QWidget()
    inp, ok = QInputDialog.getItem(window, "Pokemanki", "Select a Pokemon whose Alolan Passport you would like to take.", sorted(possibleunalolans), 0, False)
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        if f:
            alolanlist.remove(item)
        else:
            alolanlist.remove(mw.col.decks.id(item))
        settingschanged = QMessageBox()
        settingschanged.setWindowTitle("Pokemanki")
        settingschanged.setText("Please restart Anki to see your changes.")
        settingschanged.exec_()
    with open("%s/_alolanlist.json" % mediafolder, "w") as f:
        json.dump(alolanlist, f)



def PrestigePokemon():
    global mediafolder
    if os.path.exists("%s/_decksortags.json" % mediafolder):
        f = json.load(open("%s/_decksortags.json" % mediafolder))
    else:
        f = ""
    if f:
        if os.path.exists("%s/_tagmon.json" % mediafolder):
            pokemon = json.load(open("%s/_tagmon.json" % mediafolder))
    else:
        if os.path.exists("%s/_pokemanki.json" % mediafolder):
            pokemon = json.load(open("%s/_pokemanki.json" % mediafolder))
    if os.path.exists("%s/_prestigelist.json" % mediafolder):
        prestigelist = json.load(open("%s/_prestigelist.json" % mediafolder))
    else:
        prestigelist = []
    possibleprestiges = []
    for item in pokemon:
        if item[2] >= 60:
            if f:
                cb = ("%s (Level %s) from %s" % (item[0], item[2], item[1]))
            else:
                cb = ("%s (Level %s) from %s" % (item[0], item[2], mw.col.decks.name(item[1])))
            if item[1] in prestigelist:
                continue
            elif cb in possibleprestiges:
                continue
            else:
                possibleprestiges.append(cb)
        else:
            continue
    window = QWidget()
    inp, ok = QInputDialog.getItem(window, "Pokemanki", "Select a Pokemon you would like to prestige (decreases level by 50, only availabe for Pokemon with level > 60)", sorted(possibleprestiges), 0, False)
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        if f:
            prestigelist.append(item)
        else:
            prestigelist.append(mw.col.decks.id(item))
        settingschanged = QMessageBox()
        settingschanged.setWindowTitle("Pokemanki")
        settingschanged.setText("Please restart Anki to see your prestiged Pokémon.")
        settingschanged.exec_()
    with open("%s/_prestigelist.json" % mediafolder, "w") as f:
        json.dump(prestigelist, f)

def UnprestigePokemon():
    global mediafolder
    if os.path.exists("%s/_decksortags.json" % mediafolder):
        f = json.load(open("%s/_decksortags.json" % mediafolder))
    else:
        f = ""
    if f:
        if os.path.exists("%s/_tagmon.json" % mediafolder):
            pokemon = json.load(open("%s/_tagmon.json" % mediafolder))
    else:
        if os.path.exists("%s/_pokemanki.json" % mediafolder):
            pokemon = json.load(open("%s/_pokemanki.json" % mediafolder))
    if os.path.exists("%s/_prestigelist.json" % mediafolder):
        prestigelist = json.load(open("%s/_prestigelist.json" % mediafolder))
    else:
        prestigelist = []
    if not prestigelist:
        noprestige = QMessageBox()
        noprestige.setWindowTitle("Pokemanki")
        noprestige.setText("You have no prestiged Pokémon.")
        noprestige.exec_()
        return
    possibleunprestiges = []
    for thing in prestigelist:
        for item in pokemon:
            if item[1] == thing:
                if f:
                    cb = ("%s from %s" % (item[0], item[1]))
                else:
                    cb = ("%s from %s" % (item[0], mw.col.decks.name(item[1])))
                if cb in possibleunprestiges:
                    continue
                else:
                    possibleunprestiges.append(cb)
        else:
            continue
    window = QWidget()
    inp, ok = QInputDialog.getItem(window, "Pokemanki", "Select a Pokemon you would like to unprestige", sorted(possibleunprestiges), 0, False)
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        if f:
            prestigelist.remove(item)
        else:
            prestigelist.remove(mw.col.decks.id(item))
        settingschanged = QMessageBox()
        settingschanged.setWindowTitle("Pokemanki")
        settingschanged.setText("Please restart Anki to see your unprestiged Pokémon.")
        settingschanged.exec_()
    with open("%s/_prestigelist.json" % mediafolder, "w") as f:
        json.dump(prestigelist, f)


def pokemonLevelRangesFromCsv(csv_fpath):
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

class Trades:
    def __init__(self):
        self.tradewindow = QDialog()
        self.dirname = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        profilename = mw.pm.name
        #ankifolder = os.path.dirname(os.path.dirname(self.dirname))
        if os.path.exists("%s/%s" % (ankifolder, profilename)):
            profilefolder = ("%s/%s" % (ankifolder, profilename))
        # Get to collection.media folder
        if os.path.exists("%s/collection.media" % profilefolder):
            mediafolder = "%s/collection.media" % profilefolder
        self.mediafolder = mediafolder

        pokemon_records = []
        csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen1.csv")
        pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
        if config['gen2']:
            csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen2.csv")
            pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))

            if config['gen4_evolutions']:
                csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen1_plus2_plus4.csv")
                pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
                csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen2_plus4.csv")
                pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
            else:
                csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen1_plus2_no4.csv")
                pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
                csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen2_no4.csv")
                pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
        else:
            if config['gen4_evolutions']:
                # a lot of gen 4 evolutions that affect gen 1 also include gen 2 evolutions
                # so let's just include gen 2 for these evolution lines
                csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen1_plus2_plus4.csv")
                pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
            else:
                csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen1_no2_no4.csv")
                pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
        
        if config['gen3']:
            csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen3.csv")
            pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
        if config['gen4']:
            csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen4.csv")
            pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
        if config['gen5']:
            csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen5.csv")
            pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))

        self.allpokemon = pokemon_records
        if os.path.exists("%s/_decksortags.json" % mediafolder):
            self.f = json.load(open("%s/_decksortags.json" % mediafolder))
        else:
            self.f = ""
        
    def newTrades(self):
        self.trades = []
        i = 0
        f = self.f
        if f:
            if os.path.exists("%s/_tagmon.json" % self.mediafolder):
                deckmonlist = json.load(open("%s/_tagmon.json" % self.mediafolder))
                sorteddeckmonlist = list(reversed(deckmonlist))
                noeggslist = []
                for item in sorteddeckmonlist:
                    if int(item[2]) >= 5:
                        noeggslist.append(item)
                deckmons = []
                for item in noeggslist:
                    for thing in deckmons:
                        if item[1] == thing[1]:
                            break
                    else:
                        deckmons.append(item)
                deckmonlist = deckmons
            else:
                nopokemon = QMessageBox()
                nopokemon.setWindowTitle("Pokemanki")
                nopokemon.setText("Please open the Stats window to get your Pokémon.")
                nopokemon.exec_()
                return
        else:
            if os.path.exists("%s/_pokemanki.json" % self.mediafolder):
                deckmonlist = json.load(open("%s/_pokemanki.json" % self.mediafolder))
                sorteddeckmonlist = list(reversed(deckmonlist))
                noeggslist = []
                for item in sorteddeckmonlist:
                    if int(item[2]) >= 5:
                        noeggslist.append(item)
                deckmons = []
                for item in noeggslist:
                    for thing in deckmons:
                        if item[1] == thing[1]:
                            break
                    else:
                        deckmons.append(item)
                deckmonlist = deckmons
            else:
                nopokemon = QMessageBox()
                nopokemon.setWindowTitle("Pokemanki")
                nopokemon.setText("Please open the Stats window to get your Pokémon.")
                nopokemon.exec_()
                return
        possiblehaveslist = []
        while i < 3:
            randno = random.randint(0, len(deckmonlist)-1)
            pokemon = deckmonlist[randno]
            for item in self.allpokemon:
                if pokemon[0] == item[0]:
                    want = item
            possiblehaves = []
            if want[1] == "F":
                for item in self.allpokemon:
                    if (item[1] == "F" or item[1] == "E") and (item[2] < int(pokemon[2]) < item[3]):
                        possiblehaves.append(item)
            elif want[1] == "E":
                for item in self.allpokemon:
                    if (item[1] == "F" or item[1] == "E" or item[1] == "D") and (item[2] < int(pokemon[2]) < item[3]):
                        possiblehaves.append(item)
            elif want[1] == "D":
                for item in self.allpokemon:
                    if (item[1] == "C" or item[1] == "E" or item[1] == "D") and (item[2] < int(pokemon[2]) < item[3]):
                        possiblehaves.append(item)
            elif want[1] == "C":
                for item in self.allpokemon:
                    if (item[1] == "C" or item[1] == "B" or item[1] == "D") and (item[2] < int(pokemon[2]) < item[3]):
                        possiblehaves.append(item)
            elif want[1] == "B":
                for item in self.allpokemon:
                    if (item[1] == "C" or item[1] == "B" or item[1] == "A") and (item[2] < int(pokemon[2]) < item[3]):
                        possiblehaves.append(item)
            elif want[1] == "A":
                for item in self.allpokemon:
                    if (item[1] == "B" or item[1] == "A") and (item[2] < int(pokemon[2]) < item[3]):
                        possiblehaves.append(item)
            if len(possiblehaves) > 1:
                randno = random.randint(0, len(possiblehaves)-1)
                have = possiblehaves[randno]
            elif len(possiblehaves) == 1:
                have = possiblehaves[0]
            else:
                continue
            if have[0].startswith("Eevee") and want[0].startswith("Eevee"):
                self.trades.append((("Eevee", have[1], have[2], have[3]), ("Eevee", want[1], want[2], want[3])))
            elif have[0].startswith("Eevee"):
                self.trades.append((("Eevee", have[1], have[2], have[3]), want))
            elif want[0].startswith("Eevee"):
                self.trades.append((have, ("Eevee", want[1], want[2], want[3])))
            else:
                self.trades.append((have, want))
            possiblehaveslist.append(possiblehaves)
            i += 1
        global today
        date = today.strftime("%d/%m/%Y")
        if f:
            tradeData = [date, self.trades, "tags"]
        else:
            tradeData = [date, self.trades, "decks"]
        testData = [date, self.trades, possiblehaveslist]
        with open("_trades.json", "w") as f:
            json.dump(tradeData, f)
    def tradeFunction(self):
        # show a message box
        f = self.f
        if os.path.exists("_trades.json"):
            tradeData = json.load(open("_trades.json"))
            global today
            date = today.strftime("%d/%m/%Y")
            if date == tradeData[0] and len(tradeData) == 3:
                if f == tradeData[2]:
                    self.trades = tradeData[1]
                elif f == "" and tradeData[2] == "decks":
                    self.trades = tradeData[1]
                else:
                    self.newTrades()
                    tradeData = json.load(open("_trades.json"))
            else:
                self.newTrades()
                tradeData = json.load(open("_trades.json"))
        else:
            self.newTrades()
            tradeData = json.load(open("_trades.json"))
        tradewindow = self.tradewindow
        tradewindow.setWindowTitle("Pokemanki")
        tradewindow.setWindowModality(Qt.ApplicationModal)
        table = """<table>
                   <tr>
                   <td height 50 width = 150 align = center></td>
                   <td height 50 width = 150 align = center><h1>Today's Trades</h1></td>
                   <td height 50 width = 150 align = center></td>
                   <tr>
                   <tr>
                   <td height 40 width = 150 align = center><h2>Trainer 1</h2></td>
                   <td height 40 width = 150 align = center><h2>Trainer 2</h2></td>
                   <td height 40 width = 150 align = center><h2>Trainer 3</h2></td>
                   <tr>
                   <tr>
                   <td height 30 width = 150 align = center><h3>Currently has</h3></td>
                   <td height 30 width = 150 align = center><h3>Currently has</h3></td>
                   <td height 30 width = 150 align = center><h3>Currently has</h3></td>
                   <tr>
                   <td height = 150 width = 150 align = center><img src = "%s/pokemon_images/%s.png" width = 150 height = 150></td>
                   <td height = 150 width = 150 align = center><img src = "%s/pokemon_images/%s.png" width = 150 height = 150></td>
                   <td height = 150 width = 150 align = center><img src = "%s/pokemon_images/%s.png" width = 150 height = 150></td>
                   </tr>
                   <tr>
                   <td height = 30 width = 150 align = center><b>%s</b></td>
                   <td height = 30 width = 150 align = center><b>%s</b></td>
                   <td height = 30 width = 150 align = center><b>%s</b></td>
                   </tr>
                   <tr>
                   <td height 1 width = 150 align = center></td>
                   <td height 1 width = 150 align = center></td>
                   <td height 1 width = 150 align = center></td>
                   <tr>
                   <tr>
                   <td height 30 width = 150 align = center><h3>And wants</h3></td>
                   <td height 30 width = 150 align = center><h3>And wants</h3></td>
                   <td height 30 width = 150 align = center><h3>And wants</h3></td>
                   <tr>
                   <td height = 150 width = 150 align = center><img src = "%s/pokemon_images/%s.png" width = 150 height = 150></td>
                   <td height = 150 width = 150 align = center><img src = "%s/pokemon_images/%s.png" width = 150 height = 150></td>
                   <td height = 150 width = 150 align = center><img src = "%s/pokemon_images/%s.png" width = 150 height = 150></td>
                   </tr>
                   <tr>
                   <td height = 30 width = 150 align = center><b>%s</b></td>
                   <td height = 30 width = 150 align = center><b>%s</b></td>
                   <td height = 30 width = 150 align = center><b>%s</b></td>
                   </tr>
                   </table>""" % (self.dirname, self.trades[0][0][0], self.dirname, self.trades[1][0][0], self.dirname, self.trades[2][0][0], self.trades[0][0][0], self.trades[1][0][0], self.trades[2][0][0], self.mediafolder, self.trades[0][1][0], self.mediafolder, self.trades[1][1][0], self.mediafolder, self.trades[2][1][0], self.trades[0][1][0], self.trades[1][1][0], self.trades[2][1][0])
        lbl1 = QLabel(table, tradewindow)
        lbl1.move(0, 0)
        lbl2 = QLabel("", tradewindow)
        lbl2.move(360, 420)
        btn1 = QPushButton("TRADE", tradewindow)
        btn1.move(50, 455)
        btn2 = QPushButton("TRADE", tradewindow)
        btn2.move(200, 455)
        btn3 = QPushButton("TRADE", tradewindow)
        btn3.move(350, 455)
        btn1.clicked.connect(self.trade1)
        btn2.clicked.connect(self.trade2)
        btn3.clicked.connect(self.trade3)
        tradewindow.exec_()

    def trade1(self):
        have = self.trades[0][0]
        want = self.trades[0][1]
        possiblefits = []
        f = self.f
        if f:
            if os.path.exists("%s/_tagmon.json" % self.mediafolder):
                deckmonlist = json.load(open("%s/_tagmon.json" % self.mediafolder))
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
                nopokemon = QMessageBox()
                nopokemon.setWindowTitle("Pokemanki")
                nopokemon.setText("Please open the Stats window to get your Pokémon.")
                nopokemon.exec_()
                return
        else:
            if os.path.exists("%s/_pokemanki.json" % self.mediafolder):
                deckmonlist = json.load(open("%s/_pokemanki.json" % self.mediafolder))
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
                nopokemon = QMessageBox()
                nopokemon.setWindowTitle("Pokemanki")
                nopokemon.setText("Please open the Stats window to get your Pokémon.")
                nopokemon.exec_()
                return
        for item in deckmonlist:
            if item[0] == want[0] or (item[0].startswith("Eevee") and want[0] == "Eevee") and int(item[2]) >= 5:
                possiblefits.append(item)
        if possiblefits == []:
            novalidpokemon = QMessageBox()
            novalidpokemon.setWindowTitle("Pokemanki")
            novalidpokemon.setText("Sorry, you do not have the Pokemon needed to complete this trade.")
            novalidpokemon.exec_()
            return
        displaylist = []
        for item in possiblefits:
            deckname = mw.col.decks.name(item[1])
            if len(item) == 4:
                if item[0].startswith("Eevee"):
                    displaytext = "%s - Eevee (Level %s) from %s" % (item[3], int(item[2]), deckname)
                else:
                    displaytext = "%s - %s (Level %s) from %s" % (item[3], item[0], int(item[2]), deckname)
            else:
                if item[0].startswith("Eevee"):
                    displaytext = "Eevee (Level %s) from %s" % (int(item[2]), deckname)
                else:
                    displaytext = "%s (Level %s) from %s" % (item[0], int(item[2]), deckname)
            displaylist.append(displaytext)
        totallist = list(zip(possiblefits, displaylist))
        possiblepokemon = QWidget()
        inp, ok = QInputDialog.getItem(possiblepokemon, "Pokemanki", "Choose a Pokemon to trade for %s" % have[0], displaylist, 0, False)
        tradepokemon = []
        if ok and inp:
            for thing in totallist:
                if inp in thing:
                    tradepokemon = thing[0]
                    displaytext = inp
        if not tradepokemon:
            return
        confirmation = QMessageBox()
        confirmation.setWindowTitle("Pokemanki")
        confirmation.setText("Are you sure you want to trade your %s for a %s" % (displaytext, have[0]))
        confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmation.setDefaultButton(QMessageBox.No)
        result = confirmation.exec_()
        if result == QMessageBox.Yes:
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
            with open(("%s/_pokemanki.json" % self.mediafolder), "w") as f:
                json.dump(modifieddeckmonlist, f)
            self.tradewindow.done(QDialog.Accepted)
            tradedone = QMessageBox()
            tradedone.setWindowTitle("Pokemanki")
            tradedone.setText("You have traded your %s for a %s" % (displaytext, have[0]))
            tradedone.exec_()

    def trade2(self):
        have = self.trades[1][0]
        want = self.trades[1][1]
        possiblefits = []
        f = self.f
        if f:
            if os.path.exists("%s/_tagmon.json" % self.mediafolder):
                deckmonlist = json.load(open("%s/_tagmon.json" % self.mediafolder))
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
                nopokemon = QMessageBox()
                nopokemon.setWindowTitle("Pokemanki")
                nopokemon.setText("Please open the Stats window to get your Pokémon.")
                nopokemon.exec_()
                return
        else:
            if os.path.exists("%s/_pokemanki.json" % self.mediafolder):
                deckmonlist = json.load(open("%s/_pokemanki.json" % self.mediafolder))
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
                nopokemon = QMessageBox()
                nopokemon.setWindowTitle("Pokemanki")
                nopokemon.setText("Please open the Stats window to get your Pokémon.")
                nopokemon.exec_()
                return
        for item in deckmonlist:
            if item[0] == want[0] or (item[0].startswith("Eevee") and want[0] == "Eevee") and int(item[2]) >= 5:
                possiblefits.append(item)
        if possiblefits == []:
            novalidpokemon = QMessageBox()
            novalidpokemon.setWindowTitle("Pokemanki")
            novalidpokemon.setText("Sorry, you do not have the Pokémon needed to complete this trade.")
            novalidpokemon.exec_()
            return
        displaylist = []
        for item in possiblefits:
            deckname = mw.col.decks.name(item[1])
            if len(item) == 4:
                if item[0].startswith("Eevee"):
                    displaytext = "%s - Eevee (Level %s) from %s" % (item[3], int(item[2]), deckname)
                else:
                    displaytext = "%s - %s (Level %s) from %s" % (item[3], item[0], int(item[2]), deckname)
            else:
                if item[0].startswith("Eevee"):
                    displaytext = "Eevee (Level %s) from %s" % (int(item[2]), deckname)
                else:
                    displaytext = "%s (Level %s) from %s" % (item[0], int(item[2]), deckname)
            displaylist.append(displaytext)
        totallist = list(zip(possiblefits, displaylist))
        possiblepokemon = QWidget()
        inp, ok = QInputDialog.getItem(possiblepokemon, "Pokemanki", "Choose a Pokemon to trade for %s" % have[0], displaylist, 0, False)
        tradepokemon = []
        if ok and inp:
            for thing in totallist:
                if inp in thing:
                    tradepokemon = thing[0]
                    displaytext = inp
        if not tradepokemon:
            return
        confirmation = QMessageBox()
        confirmation.setWindowTitle("Pokemanki")
        confirmation.setText("Are you sure you want to trade your %s for a %s" % (displaytext, have[0]))
        confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmation.setDefaultButton(QMessageBox.No)
        result = confirmation.exec_()
        if result == QMessageBox.Yes:
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
            with open(("%s/_pokemanki.json" % self.mediafolder), "w") as f:
                json.dump(modifieddeckmonlist, f)
            self.tradewindow.done(QDialog.Accepted)
            tradedone = QMessageBox()
            tradedone.setWindowTitle("Pokemanki")
            tradedone.setText("You have traded your %s for a %s" % (displaytext, have[0]))
            tradedone.exec_()

    def trade3(self):
        have = self.trades[2][0]
        want = self.trades[2][1]
        possiblefits = []
        f = self.f
        if f:
            if os.path.exists("%s/_tagmon.json" % self.mediafolder):
                deckmonlist = json.load(open("%s/_tagmon.json" % self.mediafolder))
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
                nopokemon = QMessageBox()
                nopokemon.setWindowTitle("Pokemanki")
                nopokemon.setText("Please open the Stats window to get your Pokémon.")
                nopokemon.exec_()
                return
        else:
            if os.path.exists("%s/_pokemanki.json" % self.mediafolder):
                deckmonlist = json.load(open("%s/_pokemanki.json" % self.mediafolder))
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
                nopokemon = QMessageBox()
                nopokemon.setWindowTitle("Pokemanki")
                nopokemon.setText("Please open the Stats window to get your Pokémon.")
                nopokemon.exec_()
                return
        for item in deckmonlist:
            if item[0] == want[0] or (item[0].startswith("Eevee") and want[0] == "Eevee") and int(item[2]) >= 5:
                possiblefits.append(item)
        if possiblefits == []:
            novalidpokemon = QMessageBox()
            novalidpokemon.setWindowTitle("Pokemanki")
            novalidpokemon.setText("Sorry, you do not have the Pokemon needed to complete this trade.")
            novalidpokemon.exec_()
            return
        displaylist = []
        for item in possiblefits:
            deckname = mw.col.decks.name(item[1])
            if len(item) == 4:
                if item[0].startswith("Eevee"):
                    displaytext = "%s - Eevee (Level %s) from %s" % (item[3], int(item[2]), deckname)
                else:
                    displaytext = "%s - %s (Level %s) from %s" % (item[3], item[0], int(item[2]), deckname)
            else:
                if item[0].startswith("Eevee"):
                    displaytext = "Eevee (Level %s) from %s" % (int(item[2]), deckname)
                else:
                    displaytext = "%s (Level %s) from %s" % (item[0], int(item[2]), deckname)
            displaylist.append(displaytext)
        totallist = list(zip(possiblefits, displaylist))
        possiblepokemon = QWidget()
        inp, ok = QInputDialog.getItem(possiblepokemon, "Pokemanki", "Choose a Pokemon to trade for %s" % have[0], displaylist, 0, False)
        tradepokemon = []
        if ok and inp:
            for thing in totallist:
                if inp in thing:
                    tradepokemon = thing[0]
                    displaytext = inp
        if not tradepokemon:
            return
        confirmation = QMessageBox()
        confirmation.setWindowTitle("Pokemanki")
        confirmation.setText("Are you sure you want to trade your %s for a %s" % (displaytext, have[0]))
        confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmation.setDefaultButton(QMessageBox.No)
        result = confirmation.exec_()
        if result == QMessageBox.Yes:
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
            with open(("%s/_pokemanki.json" % self.mediafolder), "w") as f:
                json.dump(modifieddeckmonlist, f)
            self.tradewindow.done(QDialog.Accepted)
            tradedone = QMessageBox()
            tradedone.setWindowTitle("Pokemanki")
            tradedone.setText("You have traded your %s for a %s" % (displaytext, have[0]))
            tradedone.exec_()

tradeclass = Trades()

class Tags:
    def __init__(self):
        self.parentwindow = QDialog()
        self.alltags = []
    def tagMenu(self):
        if os.path.exists("_tags.json"):
            self.savedtags = json.load(open("_tags.json"))
        else:
            self.savedtags = []
        rawtags = mw.col.tags.all()
        alltags = self.alltags
        for item in rawtags:
            taglist = item.split("::")
            alltags.append(taglist)
        tagdict = {}
        for item in alltags:
            if len(item) == 1:
                if item[0] in tagdict:
                    continue
                else:
                    tagdict[item[0]] = {}
            elif len(item) == 2:
                if item[0] in tagdict:
                    if item[1] in tagdict[item[0]]:
                        continue
                    else:
                        tagdict[item[0]][item[1]] = {}
                else:
                    tagdict[item[0]] = {}
                    tagdict[item[0]][item[1]] = {}
            elif len(item) == 3:
                if item[0] in tagdict:
                    if item[1] in tagdict[item[0]]:
                        if item[2] in tagdict[item[0]][item[1]]:
                            continue
                        else:
                            tagdict[item[0]][item[1]][item[2]] = {}
                    else:
                        tagdict[item[0]][item[1]] = {}
                        tagdict[item[0]][item[1]][item[2]] = {}
                else:
                    tagdict[item[0]] = {}
                    tagdict[item[0]][item[1]] = {}
                    tagdict[item[0]][item[1]][item[2]] = {}
            elif len(item) == 4:
                if item[0] in tagdict:
                    if item[1] in tagdict[item[0]]:
                        if item[2] in tagdict[item[0]][item[1]]:
                            if item[3] in tagdict[item[0]][item[1]][item[2]]:
                                continue
                            else:
                                tagdict[item[0]][item[1]][item[2]][item[3]] = {}
                        else:
                            tagdict[item[0]][item[1]][item[2]] = {}
                            tagdict[item[0]][item[1]][item[2]][item[3]] = {}
                    else:
                        tagdict[item[0]][item[1]] = {}
                        tagdict[item[0]][item[1]][item[2]] = {}
                        tagdict[item[0]][item[1]][item[2]][item[3]] = {}
                else:
                    tagdict[item[0]] = {}
                    tagdict[item[0]][item[1]] = {}
                    tagdict[item[0]][item[1]][item[2]] = {}
                    tagdict[item[0]][item[1]][item[2]][item[3]] = {}
        taglist = []
        for i in tagdict:
            if not tagdict[i]:
                taglist.append([i, []])
            else:
                childlist = []
                for j in tagdict[i]:
                    if not tagdict[i][j]:
                        childlist.append([j, []])
                    else:
                        grandchildlist = []
                        for k in tagdict[i][j]:
                            if not tagdict[i][j][k]:
                                grandchildlist.append([k, []])
                            else:
                                greatgrandchildlist = []
                                for l in tagdict[i][j][k]:
                                    greatgrandchildlist.append([l, []])
                                greatgrandchildlist = sorted(greatgrandchildlist, key = lambda x: x[0].lower())
                                grandchildlist.append([k, greatgrandchildlist])
                        grandchildlist = sorted(grandchildlist, key = lambda x: x[0].lower())
                        childlist.append([j, grandchildlist])
                childlist = sorted(childlist, key = lambda x: x[0].lower())
                taglist.append([i, childlist])
        taglist = sorted(taglist, key = lambda x: x[0].lower())
        parentwindow = self.parentwindow
        parentwindow.setMinimumWidth(255)
        parentwindow.setMinimumHeight(192)
        lbl = QLabel("Please select the tags for which you would like Pokemon assigned.", parentwindow)
        lbl.move(5, 5)
        widget = QWidget(parentwindow)
        widget.resize(255, 192)
        widget.move(0, 20)
        tree = QTreeWidget(widget)
        tree.setColumnCount(1)
        tree.setHeaderLabels(["Tags"])
        headerItem = QTreeWidgetItem()
        item = QTreeWidgetItem()
        parentlist = self.parentlist = []
        for i in taglist:
            if not i[1]:
                parent = QTreeWidgetItem(tree)
                parent.setText(0, i[0])
                parent.setFlags(parent.flags() | Qt.ItemIsUserCheckable)
                if i[0] in self.savedtags:
                    parent.setCheckState(0, Qt.Checked)
                else:
                    parent.setCheckState(0, Qt.Unchecked)
                parentlist.append([parent, []])
            else:
                parent = QTreeWidgetItem(tree)
                parent.setText(0, i[0])
                parent.setFlags(parent.flags() | Qt.ItemIsUserCheckable)
                if i[0] in self.savedtags:
                    parent.setCheckState(0, Qt.Checked)
                else:
                    parent.setCheckState(0, Qt.Unchecked)
                childlist = []
                for j in i[1]:
                    if not j[1]:
                        child = QTreeWidgetItem(parent)
                        child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                        child.setText(0, j[0])
                        if i[0] + "::" + j[0] in self.savedtags:
                            child.setCheckState(0, Qt.Checked)
                        else:
                            child.setCheckState(0, Qt.Unchecked)
                        childlist.append([child, []])
                    else:
                        child = QTreeWidgetItem(parent)
                        child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                        child.setText(0, j[0])
                        if i[0] + "::" + j[0] in self.savedtags:
                            child.setCheckState(0, Qt.Checked)
                        else:
                            child.setCheckState(0, Qt.Unchecked)
                        grandchildlist = []
                        for k in j[1]:
                            if not k[1]:
                                grandchild = QTreeWidgetItem(child)
                                grandchild.setFlags(grandchild.flags() | Qt.ItemIsUserCheckable)
                                grandchild.setText(0, k[0])
                                if i[0] + "::" + j[0] + "::" + k[0] in self.savedtags:
                                    grandchild.setCheckState(0, Qt.Checked)
                                else:
                                    grandchild.setCheckState(0, Qt.Unchecked)
                                grandchildlist.append([grandchild, []])
                            else:
                                grandchild = QTreeWidgetItem(child)
                                grandchild.setFlags(grandchild.flags() | Qt.ItemIsUserCheckable)
                                grandchild.setText(0, k[0])
                                if i[0] + "::" + j[0] + "::" + k[0] in self.savedtags:
                                    grandchild.setCheckState(0, Qt.Checked)
                                else:
                                    grandchild.setCheckState(0, Qt.Unchecked)
                                greatgrandchildlist = []
                                for l in k[1]:
                                    greatgrandchild = QTreeWidgetItem(grandchild)
                                    greatgrandchild.setFlags(greatgrandchild.flags() | Qt.ItemIsUserCheckable)
                                    greatgrandchild.setText(0, l[0])
                                    if i[0] + "::" + j[0] + "::" + k[0] + "::" + l[0] in self.savedtags:
                                        greatgrandchild.setCheckState(0, Qt.Checked)
                                    else:
                                        greatgrandchild.setCheckState(0, Qt.Unchecked)
                                    greatgrandchildlist.append([greatgrandchild, []])
                                grandchildlist.append([grandchild, greatgrandchildlist])
                        childlist.append([child, grandchildlist])
                parentlist.append([parent, childlist])
        btn = QPushButton("OK", parentwindow)
        btn.move(100, 220)
        btn.clicked.connect(self.tagAssign)
        parentwindow.exec_()
    def tagAssign(self):
        checked = self.checked = []
        for item in self.parentlist:
            if item[0].checkState(0) == Qt.Checked:
                checked.append(item[0].text(0))
            if item[1]:
                for jtem in item[1]:
                    if jtem[0].checkState(0) == Qt.Checked:
                        checked.append(item[0].text(0) + "::" + jtem[0].text(0))
                    if jtem[1]:
                        for ktem in jtem[1]:
                            if ktem[0].checkState(0) == Qt.Checked:
                                checked.append(item[0].text(0) + "::" + jtem[0].text(0) + "::" + ktem[0].text(0))
                            if ktem[1]:
                                for ltem in ktem[1]:
                                    if ltem[0].checkState(0) == Qt.Checked:
                                        checked.append(item[0].text(0) + "::" + jtem[0].text(0) + "::" + ktem[0].text(0) + "::" + ltem[0].text(0))
        with open("_tags.json", "w") as f:
            json.dump(checked, f)
        self.parentwindow.done(QDialog.Accepted)

tags = Tags()

# Make actions for settings and reset
nicknameaction = QAction("Nicknames", mw)
thresholdaction = QAction("Threshold Settings", mw)
resetaction = QAction("Reset", mw)
tradeaction = QAction("Trade", mw)
toggleaction = QAction("Decks vs. Tags", mw)
tagsaction = QAction("Tags", mw)
prestigeaction = QAction("Prestige Pokémon", mw)
unprestigeaction = QAction("Unprestige Pokémon", mw)
everstoneaction = QAction("Give Everstone", mw)
uneverstoneaction = QAction("Take Everstone", mw)
megastoneaction = QAction("Give Mega Stone", mw)
unmegastoneaction = QAction("Take Mega Stone", mw)
alolanaction = QAction("Give Alolan Passport", mw)
unalolanaction = QAction("Take Alolan Passport", mw)
bottomaction = QAction("Move Pokémon to Bottom", mw)
topaction = QAction("Move Pokémon to Top", mw)

# Connect actions to functions
nicknameaction.triggered.connect(Nickname)
resetaction.triggered.connect(ResetPokemon)
tradeaction.triggered.connect(tradeclass.tradeFunction)
toggleaction.triggered.connect(Toggle)
tagsaction.triggered.connect(tags.tagMenu)
prestigeaction.triggered.connect(PrestigePokemon)
unprestigeaction.triggered.connect(UnprestigePokemon)
everstoneaction.triggered.connect(giveEverstone)
uneverstoneaction.triggered.connect(takeEverstone)
megastoneaction.triggered.connect(giveMegastone)
unmegastoneaction.triggered.connect(takeMegastone)
alolanaction.triggered.connect(giveAlolanPassport)
unalolanaction.triggered.connect(takeAlolanPassport)
bottomaction.triggered.connect(MovetoBottom)
topaction.triggered.connect(MovetoTop)


# Make new Pokemanki menu under tools
mw.testmenu = QMenu(_('&Pokemanki'), mw)
mw.form.menubar.addMenu(mw.testmenu)
mw.testmenu.addAction(toggleaction)
mw.testmenu.addAction(nicknameaction)
mw.prestigemenu = QMenu(_('&Prestige Menu'), mw)
mw.testmenu.addMenu(mw.prestigemenu)
mw.prestigemenu.addAction(prestigeaction)
mw.prestigemenu.addAction(unprestigeaction)
mw.everstonemenu = QMenu(_('&Everstone'), mw)
mw.testmenu.addMenu(mw.everstonemenu)
mw.everstonemenu.addAction(everstoneaction)
mw.everstonemenu.addAction(uneverstoneaction)
mw.megastonemenu = QMenu(_('&Mega Stone'), mw)
mw.testmenu.addMenu(mw.megastonemenu)
mw.megastonemenu.addAction(megastoneaction)
mw.megastonemenu.addAction(unmegastoneaction)
mw.alolanmenu = QMenu(_('&Alolan Passport'), mw)
mw.testmenu.addMenu(mw.alolanmenu)
mw.alolanmenu.addAction(alolanaction)
mw.alolanmenu.addAction(unalolanaction)

# Wrap pokemonDisplay function of display.py with the todayStats function of anki.stats.py
addonsfolder = os.path.dirname(currentdirname)
if os.path.exists("%s/_decksortags.json" % mediafolder):
    f = json.load(open("%s/_decksortags.json" % mediafolder))
else:
    f = ""
if os.path.exists("%s/_toporbottom.json" % mediafolder):
    g = json.load(open("%s/_toporbottom.json" % mediafolder))
else:
    g = ""
if f:
    mw.testmenu.addAction(tagsaction)
    if g:
        mw.testmenu.addAction(topaction)
        anki.stats.CollectionStats.easeGraph = \
            wrap(anki.stats.CollectionStats.easeGraph, tagmonDisplay, pos="")
    elif os.path.exists("%s/923360400" % addonsfolder):
        mw.testmenu.addAction(bottomaction)
        anki.stats.CollectionStats.dueGraph = \
            wrap(anki.stats.CollectionStats.dueGraph, tagmonDisplay, pos="")
    else:
        mw.testmenu.addAction(bottomaction)
        anki.stats.CollectionStats.todayStats = \
            wrap(anki.stats.CollectionStats.todayStats, tagmonDisplay, pos="")
else:
    mw.testmenu.addAction(thresholdaction)
    mw.testmenu.addAction(tradeaction)
    if g:
        mw.testmenu.addAction(topaction)
        anki.stats.CollectionStats.easeGraph = \
            wrap(anki.stats.CollectionStats.easeGraph, pokemonDisplay, pos="")
    elif os.path.exists("%s/923360400" % addonsfolder):
        mw.testmenu.addAction(bottomaction)
        anki.stats.CollectionStats.dueGraph = \
            wrap(anki.stats.CollectionStats.dueGraph, pokemonDisplay, pos="")
    else:
        mw.testmenu.addAction(bottomaction)
        anki.stats.CollectionStats.todayStats = \
            wrap(anki.stats.CollectionStats.todayStats, pokemonDisplay, pos="")

mw.testmenu.addAction(resetaction)
