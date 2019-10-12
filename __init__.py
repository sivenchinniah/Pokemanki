# Copyright 2019 Siven Chinniah

# JK please feel free to use this however you would like.

from .display import pokemonDisplay

import anki.stats
from anki.hooks import wrap
import shutil
import inspect, os
from aqt.qt import *
from aqt import mw
import json

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
    shutil.move(pkmnimgfolder, mediafolder)
# Download threshold settings (or make from scratch if not already made)
if os.path.exists("%s/pokemankisettings.json" % mediafolder):
    thresholdlist = json.load(open("%s/pokemankisettings.json" % mediafolder))
else:
    thresholdlist = [100, 250, 500, 750, 1000]
    with open(("%s/pokemankisettings.json" % mediafolder), "w") as f:
        json.dump(thresholdlist, f)

# Nickname Settings
def Nickname():
    global mediafolder
    deckmonlist = json.load(open("%s/pokemanki.json" % mediafolder))
    displaylist = []
    for item in deckmonlist:
        deckname = mw.col.decks.name(item[1])
        if len(item) == 4:
            if item[2] < 5:
                displaytext = "%s - Egg from %s" % (item[3], deckname)
            elif item[0].startswith("Eevee"):
                displaytext = "%s - Eevee (Level %s) from %s" % (item[3], item[2], deckname)
            else:
                displaytext = "%s - %s (Level %s) from %s" % (item[3], item[0], item[2], deckname)
        else:
            if item[2] < 5:
                displaytext = "Egg from %s" % (deckname)
            elif item[0].startswith("Eevee"):
                displaytext = "Eevee (Level %s) from %s" % (item[2], deckname)
            else:
                displaytext = "%s (Level %s) from %s" % (item[0], item[2], deckname)
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
    with open(("%s/pokemanki.json" % mediafolder), "w") as f:
        json.dump(modifieddeckmonlist, f)

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
    thresholdlist = json.load(open("%s/pokemankisettings.json" % mediafolder))
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
            with open(("%s/pokemankisettings.json" % mediafolder), "w") as f:
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
        with open(("%s/pokemanki.json" % mediafolder), "w") as f:
            json.dump([], f)
        # Message box confirming reset
        resetdone = QMessageBox()
        resetdone.setWindowTitle("Pokemanki")
        resetdone.setText("Pokemon reset")
        resetdone.exec_()

# Make actions for settings and reset
nicknameaction = QAction("Nicknames", mw)
thresholdaction = QAction("Threshold Settings", mw)
resetaction = QAction("Reset", mw)

# Connect actions to functions
nicknameaction.triggered.connect(Nickname)
thresholdaction.triggered.connect(ThresholdSettings)
resetaction.triggered.connect(ResetPokemon)

# Make new Pokemanki menu under tools
mw.testmenu = QMenu(_('&Pokemanki'), mw)
mw.form.menuTools.addMenu(mw.testmenu)
mw.testmenu.addAction(nicknameaction)
mw.testmenu.addAction(thresholdaction)
mw.testmenu.addAction(resetaction)

# Wrap pokemonDisplay function of display.py with the todayStats function of anki.stats.py
anki.stats.CollectionStats.todayStats = \
    wrap(anki.stats.CollectionStats.todayStats, pokemonDisplay, pos="")
