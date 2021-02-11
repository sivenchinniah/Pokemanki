import os

from aqt import mw, gui_hooks
from aqt.qt import *

from .display import pokemonDisplay
from .tagmon import tagmonDisplay
from .tags import Tags
from .trades import Trades
from .utils import *
from .pokemon import *


config = mw.addonManager.getConfig(__name__)


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
f = get_json("_decksortags.json", "")

if f:
    mw.testmenu.addAction(tagsaction)
    display_func = tagmonDisplay
else:
    mw.testmenu.addAction(thresholdaction)
    mw.testmenu.addAction(tradeaction)
    display_func = pokemonDisplay

mw.testmenu.addAction(resetaction)


def _onStatsOpen(statsDialog):
    display = display_func().replace("`", '"')
    js = """
    addPokemanki = function(){{
        console.log("run")
        divEl = document.createElement("div");
        divEl.className = "pokemanki";
        divEl.innerHTML = `{}`;
        mainEl = document.getElementById('main');
        mainEl.parentElement.insertBefore(divEl, mainEl);
    }}
    if(document.readyState === 'complete'){{
        addPokemanki();
    }}
    else{{
        window.addEventListener('load', addPokemanki);
    }}
    """.format(display)
    statsDialog.form.web.eval(js)


def onStatsOpen(statsDialog):

    statsDialog.form.web.loadFinished.connect(
        lambda _: _onStatsOpen(statsDialog))


gui_hooks.stats_dialog_will_show.append(onStatsOpen)
