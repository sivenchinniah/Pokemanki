from .display import pokemonDisplay
from .tagmon import tagmonDisplay
from .tags import Tags
from .trades import Trades
from .utils import *
from .pokemon import *

import anki.stats
from anki.hooks import wrap
from aqt import gui_hooks
import os
from aqt.qt import *
from aqt import mw
import json
from datetime import date

config = mw.addonManager.getConfig(__name__)

today = date.today()


# Move Pokemon Image folder to collection.media folder if not already there (Anki reads from here when running anki.stats.py)
copy_directory("pokemon_images")

# Download threshold settings (or make from scratch if not already made)
set_default("_pokemankisettings.json", default=[100, 250, 500, 750, 1000])

tradeclass = Trades()
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
mw.testmenu = QMenu('&Pokemanki', mw)
mw.form.menubar.addMenu(mw.testmenu)
mw.testmenu.addAction(toggleaction)
mw.testmenu.addAction(nicknameaction)
mw.prestigemenu = QMenu('&Prestige Menu', mw)
mw.testmenu.addMenu(mw.prestigemenu)
mw.prestigemenu.addAction(prestigeaction)
mw.prestigemenu.addAction(unprestigeaction)
mw.everstonemenu = QMenu('&Everstone', mw)
mw.testmenu.addMenu(mw.everstonemenu)
mw.everstonemenu.addAction(everstoneaction)
mw.everstonemenu.addAction(uneverstoneaction)
mw.megastonemenu = QMenu('&Mega Stone', mw)
mw.testmenu.addMenu(mw.megastonemenu)
mw.megastonemenu.addAction(megastoneaction)
mw.megastonemenu.addAction(unmegastoneaction)
mw.alolanmenu = QMenu('&Alolan Passport', mw)
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
            wrap(anki.stats.CollectionStats.todayStats,
                 pokemonDisplay, pos="")

mw.testmenu.addAction(resetaction)
