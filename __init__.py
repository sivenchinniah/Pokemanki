# Copyright 2019 Siven Chinniah

# JK please feel free to use this however you would like.

from .display import pokemonDisplay
from .tagmon import tagmonDisplay

import anki.stats
import aqt.overview
from anki.hooks import wrap
import shutil
import inspect, os
from aqt.qt import *
from aqt import mw
import json
from datetime import date
import random

today = date.today()

# Find current directory
currentdirname = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# Assign Pokemon Image folder directory name
pkmnimgfolder = currentdirname + "/pokemon_images"
# Get to Anki2 folder
ankifolder = os.path.dirname(os.path.dirname(currentdirname))
# Get to profile folder
if not mw.pm.name:
    profs = mw.pm.profiles()
    mw.pm.load(profs[0])
if not mw.pm.name:
    mw.showProfileManager()
profilename = mw.pm.name
if os.path.exists("%s/%s" % (ankifolder, profilename)):
    profilefolder = ("%s/%s" % (ankifolder, profilename))
# Get to collection.media folder
if os.path.exists("%s/collection.media" % profilefolder):
    mediafolder = "%s/collection.media" % profilefolder
# Move Pokemon Image folder to collection.media folder if not already there (Anki reads from here when running anki.stats.py)
if os.path.exists("%s/pokemon_images" % mediafolder) == False and os.path.exists(pkmnimgfolder):
    shutil.copytree(pkmnimgfolder, "%s/pokemon_images" % mediafolder)
# Download threshold settings (or make from scratch if not already made)
if os.path.exists("%s/pokemankisettings.json" % mediafolder):
    thresholdlist = json.load(open("%s/pokemankisettings.json" % mediafolder))
    with open("%s/_pokemankisettings.json" % mediafolder, "w") as f:
        json.dump(thresholdlist, f)
else:
    thresholdlist = [100, 250, 500, 750, 1000]
    with open(("%s/_pokemankisettings.json" % mediafolder), "w") as f:
        json.dump(thresholdlist, f)
if os.path.exists("%s/prestigelist.json" % mediafolder) and not os.path.exists("%s/_prestigelist.json" % mediafolder):
    prestigelist = json.load(open("%s/prestigelist.json" % mediafolder))
    with open("%s/_prestigelist.json" % mediafolder, "w") as f:
        json.dump(prestigelist, f)
if os.path.exists("%s/tags.json" % mediafolder) and not os.path.exists("%s/_tags.json" % mediafolder):
    tags = json.load(open("%s/tags.json" % mediafolder))
    with open("%s/_tags.json" % mediafolder, "w") as f:
        json.dump(tags, f)
if os.path.exists("%s/decksortags.json" % mediafolder) and not os.path.exists("%s/_decksortags.json" % mediafolder):
    decksortags = json.load(open("%s/decksortags.json" % mediafolder))
    with open("%s/_decksortags.json" % mediafolder, "w") as f:
        json.dump(decksortags, f)
if os.path.exists("%s/tagmon.json" % mediafolder) and not os.path.exists("%s/_tagmon.json" % mediafolder):
    tagmon = json.load(open("%s/tagmon.json" % mediafolder))
    with open("%s/_tagmon.json" % mediafolder, "w") as f:
        json.dump(tagmon, f)
if os.path.exists("%s/pokemanki.json" % mediafolder) and not os.path.exists("%s/_pokemanki.json" % mediafolder):
    pokemanki = json.load(open("%s/pokemanki.json" % mediafolder))
    with open("%s/_pokemanki.json" % mediafolder, "w") as f:
        json.dump(pokemanki, f)
if os.path.exists("%s/toporbottom.json" % mediafolder) and not os.path.exists("%s/_toporbottom.json" % mediafolder):
    toporbottom = json.load(open("%s/toporbottom.json" % mediafolder))
    with open("%s/_toporbottom.json" % mediafolder, "w") as f:
        json.dump(toporbottom, f)
if os.path.exists("%s/trades.json" % mediafolder) and not os.path.exists("%s/_trades.json" % mediafolder):
    trades = json.load(open("%s/trades.json" % mediafolder))
    with open("%s/_trades.json" % mediafolder, "w") as f:
        json.dump(trades, f)

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
    inp, ok = QInputDialog.getItem(window, "Pokemanki", "Select a Pokemon you would like to prestige (decreases level by 50, only availabe for Pokemon with level > 60)", possibleprestiges, 0, False)
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
    inp, ok = QInputDialog.getItem(window, "Pokemanki", "Select a Pokemon you would like to unprestige", possibleunprestiges, 0, False)
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

class Trades:
    def __init__(self):
        self.tradewindow = QDialog()
        self.dirname = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        profilename = mw.pm.name
        ankifolder = os.path.dirname(os.path.dirname(self.dirname))
        if os.path.exists("%s/%s" % (ankifolder, profilename)):
            profilefolder = ("%s/%s" % (ankifolder, profilename))
        # Get to collection.media folder
        if os.path.exists("%s/collection.media" % profilefolder):
            mediafolder = "%s/collection.media" % profilefolder
        self.mediafolder = mediafolder
        self.allpokemon = [('Caterpie', 'D', 0, 7), ('Weedle', 'D', 0, 7), ('Pidgey', 'D', 0, 18), ('Rattata', 'E', 0, 20), ('Zubat', 'E', 0, 22), ('Spearow', 'E', 0, 20), ('Oddish', 'D', 0, 21), ('Paras', 'E', 0, 24), ('Venonat', 'E', 0, 31), ('Meowth', 'D', 0, 28), ('Bellsprout', 'D', 0, 21), ('Drowzee', 'D', 0, 26), ('Krabby', 'E', 0, 28), ('Horsea', 'E', 0, 32), ('Magikarp', 'B', 0, 40), ('Ekans', 'D', 0, 22), ('Nidoran F', 'D', 0, 16), ('Nidoran M', 'D', 0, 16), ('Clefairy', 'E', 0, 32), ('Jigglypuff', 'E', 0, 32), ('Diglett', 'E', 0, 26), ('Poliwag', 'D', 0, 25), ('Tentacool', 'E', 0, 30), ('Slowpoke', 'E', 0, 37), ('Magnemite', 'D', 0, 30), ('Doduo', 'E', 0, 31), ('Shellder', 'D', 0, 32), ('Gastly', 'B', 0, 25), ('Exeggcute', 'C', 0, 36), ('Cubone', 'D', 0, 28), ('Goldeen', 'E', 0, 33), ('Staryu', 'D', 0, 25), ('Eevee1', 'B', 0, 36), ('Eevee2', 'B', 0, 36), ('Eevee3', 'B', 0, 36), ('Sandshrew', 'E', 0, 22), ('Vulpix', 'D', 0, 32), ('Psyduck', 'E', 0, 33), ('Mankey', 'E', 0, 28), ('Growlithe', 'B', 0, 36), ('Abra', 'B', 0, 16), ('Machop', 'B', 0, 28), ('Geodude', 'B', 0, 25), ('Ponyta', 'C', 0, 40), ('Seel', 'E', 0, 34), ('Onix', 'D', 0, 100), ('Koffing', 'E', 0, 35), ('Scyther', 'C', 0, 100), ('Ditto', 'F', 0, 100), ('Bulbasaur', 'A', 0, 16), ('Charmander', 'A', 0, 16), ('Squirtle', 'A', 0, 16), ('Pikachu', 'D', 0, 32), ('Grimer', 'E', 0, 38), ('Lickitung', 'F', 0, 100), ('Rhyhorn', 'B', 0, 42), ('Tangela', 'F', 0, 100), ('Electabuzz', 'C', 0, 100), ('Magmar', 'C', 0, 100), ('Pinsir', 'C', 0, 100), ('Omanyte', 'D', 0, 40), ('Kabuto', 'D', 0, 40), ('Dratini', 'B', 0, 30), ("Farfetch'd", 'F', 0, 100), ('Voltorb', 'E', 0, 30), ('Hitmonlee', 'C', 0, 100), ('Hitmonchan', 'C', 0, 100), ('Chansey', 'F', 0, 100), ('Kangaskhan', 'C', 0, 100), ('Mr. Mime', 'F', 0, 100), ('Jynx', 'F', 0, 100), ('Tauros', 'C', 0, 100), ('Lapras', 'C', 0, 100), ('Porygon', 'F', 0, 100), ('Aerodactyl', 'C', 0, 100), ('Snorlax', 'C', 0, 100), ('Metapod', 'D', 7, 10), ('Kakuna', 'D', 7, 10), ('Pidgeotto', 'D', 18, 36), ('Raticate', 'E', 20, 100), ('Golbat', 'E', 22, 100), ('Fearow', 'E', 20, 100), ('Gloom', 'D', 21, 36), ('Parasect', 'E', 24, 100), ('Venomoth', 'E', 31, 100), ('Persian', 'D', 28, 100), ('Weepinbell', 'D', 21, 36), ('Hypno', 'D', 26, 100), ('Kingler', 'E', 28, 100), ('Seadra', 'E', 32, 100), ('Gyarados', 'B', 40, 100), ('Arbok', 'D', 22, 100), ('Nidorina', 'D', 16, 32), ('Nidorino', 'D', 16, 32), ('Clefable', 'E', 32, 100), ('Wigglytuff', 'E', 32, 100), ('Dugtrio', 'E', 26, 100), ('Poliwhirl', 'D', 25, 36), ('Tentacruel', 'E', 30, 100), ('Slowbro', 'E', 37, 100), ('Magneton', 'D', 30, 100), ('Dodrio', 'E', 31, 100), ('Cloyster', 'D', 32, 100), ('Haunter', 'B', 25, 40), ('Exeggutor', 'C', 36, 100), ('Marowak', 'D', 28, 100), ('Seaking', 'E', 33, 100), ('Starmie', 'D', 25, 100), ('Vaporeon', 'B', 36, 100), ('Jolteon', 'B', 36, 100), ('Flareon', 'B', 36, 100), ('Sandslash', 'E', 22, 100), ('Ninetales', 'D', 32, 100), ('Golduck', 'E', 33, 100), ('Primeape', 'E', 28, 100), ('Arcanine', 'B', 36, 100), ('Kadabra', 'B', 16, 40), ('Machoke', 'B', 28, 40), ('Graveler', 'B', 25, 40), ('Rapidash', 'C', 40, 100), ('Dewgong', 'E', 34, 100), ('Weezing', 'E', 35, 100), ('Ivysaur', 'A', 16, 32), ('Charmeleon', 'A', 16, 36), ('Wartortle', 'A', 16, 36), ('Raichu', 'D', 32, 100), ('Muk', 'E', 38, 100), ('Rhydon', 'B', 42, 100), ('Omastar', 'D', 40, 100), ('Kabutops', 'D', 40, 100), ('Dragonair', 'B', 30, 55), ('Electrode', 'E', 30, 100), ('Butterfree', 'D', 10, 100), ('Beedrill', 'D', 10, 100), ('Pidgeot', 'D', 36, 100), ('Vileplume', 'D', 36, 100), ('Victreebel', 'D', 36, 100), ('Nidoqueen', 'D', 32, 100), ('Nidoking', 'D', 32, 100), ('Poliwrath', 'D', 36, 100), ('Gengar', 'B', 40, 100), ('Alakazam', 'B', 40, 100), ('Machamp', 'B', 40, 100), ('Golem', 'B', 40, 100), ('Venusaur', 'A', 32, 100), ('Charizard', 'A', 36, 100), ('Blastoise', 'A', 36, 100), ('Dragonite', 'B', 55, 100)]
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
                    if (item[1] == "C" or item[1] == "B") and (item[2] < int(pokemon[2]) < item[3]):
                        possiblehaves.append(item)
            elif want[1] == "A":
                for item in self.allpokemon:
                    if item[1] == "A" and (item[2] < int(pokemon[2]) < item[3]):
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
        with open("trades.json", "w") as f:
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
