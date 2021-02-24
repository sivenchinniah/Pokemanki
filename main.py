import os

from aqt import mw, gui_hooks
from aqt.qt import *

from .display import pokemonDisplay
from .tagmon import tagmonDisplay
from .tags import Tags
from .trades import Trades
from .utils import *
from .pokemon import *


statsDialog = None

# Move Pokemon Image folder to collection.media folder if not already there (Anki reads from here when running anki.stats.py)
copy_directory("pokemon_images")

# Download threshold settings (or make from scratch if not already made)
set_default("_pokemankisettings.json", default=[100, 250, 500, 750, 1000])

tradeclass = Trades()
tags = Tags()

# Make actions for settings and reset
nicknameaction = QAction("Nicknames", mw)
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


f = get_json("_decksortags.json", "")
if f:
    mw.testmenu.addAction(tagsaction)
else:  # Not yet implemented for tagmon
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
    mw.testmenu.addAction(tradeaction)
mw.testmenu.addAction(resetaction)


# Wrap pokemonDisplay function of display.py with the todayStats function of anki.stats.py
# Note that above comment *may* be outdated

if f:
    display_func = tagmonDisplay
else:
    display_func = pokemonDisplay


def message_handler(handled, message, context):
    # context is not set to NewDeckStats, so don't check for it
    # maybe Anki bug?
    if not message.startswith("Pokemanki#"):
        return (False, None)
    if message == "Pokemanki#currentDeck":
        if f:
            html = tagmonDisplay().replace("`", "'")
        else:
            html = pokemonDisplay(wholeCollection=False).replace("`", "'")
    elif message == "Pokemanki#wholeCollection":
        if f:
            html = tagmonDisplay().replace("`", "'")
        else:
            html = pokemonDisplay(wholeCollection=True).replace("`", "'")
    else:
        starts = "Pokemanki#search#"
        term = message[len(starts):]
        # Todo: implement selective
        return (True, None)
    statsDialog.form.web.eval("Pokemanki.setPokemanki(`{}`)".format(html))
    return (True, None)


def _onStatsOpen(dialog):
    global statsDialog
    statsDialog = dialog
    js = (addon_dir / "web.js").read_text()
    statsDialog.form.web.eval(js)


def onStatsOpen(statsDialog):

    statsDialog.form.web.loadFinished.connect(
        lambda _: _onStatsOpen(statsDialog))


gui_hooks.stats_dialog_will_show.append(onStatsOpen)
gui_hooks.webview_did_receive_js_message.append(message_handler)
