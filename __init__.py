# Copyright 2019 Siven Chinniah

# JK I'm probably violating some intellectual property of Nintendo by doing this.

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

# Threshold Settings
def Settings():
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
settingsaction = QAction("Threshold Settings", mw)
resetsettingsaction = QAction("Reset", mw)

# Connect actions to functions
settingsaction.triggered.connect(Settings)
resetsettingsaction.triggered.connect(ResetPokemon)

# Make new Pokemanki menu under tools
mw.testmenu = QMenu(_('&Pokemanki'), mw)
mw.form.menuTools.addMenu(mw.testmenu)
mw.testmenu.addAction(settingsaction)
mw.testmenu.addAction(resetsettingsaction)

# Wrap pokemonDisplay function of display.py with the todayStats function of anki.stats.py
anki.stats.CollectionStats.todayStats = \
    wrap(anki.stats.CollectionStats.todayStats, pokemonDisplay, pos="")
