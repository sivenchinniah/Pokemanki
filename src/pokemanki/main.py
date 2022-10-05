import os
import sys
from bs4 import BeautifulSoup

from aqt import mw, gui_hooks
from aqt.qt import *

from .config import get_synced_conf, init_config
from .display import pokemon_display
from .pokemon import *
from .tags import Tags
from .trades import Trades
from .utils import copy_directory


statsDialog = None

tradeclass = object()
tags = object()

# Move Pokemon Image folder to collection.media folder if not already there (Anki reads from here when running anki.stats.py)
copy_directory("pokemon_images")
copy_directory("pokemanki_css")


def build_menu():

    # Make actions for settings and reset
    nicknameaction = QAction("&Nicknames", mw)
    resetaction = QAction("&Reset", mw)
    tradeaction = QAction("&Trade", mw)
    toggleaction = QAction("&Decks vs. Tags", mw)
    tagsaction = QAction("&Tags", mw)
    prestigeaction = QAction("&Prestige Pokémon", mw)
    unprestigeaction = QAction("&Unprestige Pokémon", mw)
    everstoneaction = QAction("&Give Everstone", mw)
    uneverstoneaction = QAction("&Take Everstone", mw)
    megastoneaction = QAction("&Give Mega Stone", mw)
    unmegastoneaction = QAction("&Take Mega Stone", mw)
    alolanaction = QAction("&Give Alolan Passport", mw)
    unalolanaction = QAction("&Take Alolan Passport", mw)
    bottomaction = QAction("Move Pokémon to &Bottom", mw)
    topaction = QAction("Move Pokémon to &Top", mw)

    # Connect actions to functions
    tradeclass = Trades()
    tags = Tags()
    qconnect(nicknameaction.triggered, Nickname)
    qconnect(resetaction.triggered, reset_pokemanki)
    qconnect(tradeaction.triggered, tradeclass.tradeFunction)
    qconnect(toggleaction.triggered, Toggle)
    qconnect(tagsaction.triggered, tags.tagMenu)
    qconnect(prestigeaction.triggered, PrestigePokemon)
    qconnect(unprestigeaction.triggered, UnprestigePokemon)
    qconnect(everstoneaction.triggered, giveEverstone)
    qconnect(uneverstoneaction.triggered, takeEverstone)
    qconnect(megastoneaction.triggered, giveMegastone)
    qconnect(unmegastoneaction.triggered, takeMegastone)
    qconnect(alolanaction.triggered, giveAlolanPassport)
    qconnect(unalolanaction.triggered, takeAlolanPassport)
    qconnect(bottomaction.triggered, MovetoBottom)
    qconnect(topaction.triggered, MovetoTop)

    mw.pokemenu.clear()

    mw.form.menuTools.addMenu(mw.pokemenu)
    mw.pokemenu.addAction(toggleaction)
    mw.pokemenu.addAction(nicknameaction)
    mw.prestigemenu = QMenu("&Prestige Menu", mw)
    mw.pokemenu.addMenu(mw.prestigemenu)
    mw.prestigemenu.addAction(prestigeaction)
    mw.prestigemenu.addAction(unprestigeaction)

    f = get_synced_conf()["decks_or_tags"]
    if f == "tags":
        mw.pokemenu.addAction(tagsaction)
    else:  # Not yet implemented for tagmon
        mw.everstonemenu = QMenu("&Everstone", mw)
        mw.pokemenu.addMenu(mw.everstonemenu)
        mw.everstonemenu.addAction(everstoneaction)
        mw.everstonemenu.addAction(uneverstoneaction)
        mw.megastonemenu = QMenu("&Mega Stone", mw)
        mw.pokemenu.addMenu(mw.megastonemenu)
        mw.megastonemenu.addAction(megastoneaction)
        mw.megastonemenu.addAction(unmegastoneaction)
        mw.alolanmenu = QMenu("&Alolan Passport", mw)
        mw.pokemenu.addMenu(mw.alolanmenu)
        mw.alolanmenu.addAction(alolanaction)
        mw.alolanmenu.addAction(unalolanaction)
        mw.pokemenu.addAction(tradeaction)

    mw.pokemenu.addAction(resetaction)


# Wrap pokemon_display function of display.py with the todayStats function of anki.stats.py
# Note that above comment *may* be outdated
display_func = pokemon_display


def message_handler(handled, message, context):
    # context is not set to NewDeckStats, so don't check for it
    # maybe Anki bug?
    if not message.startswith("Pokemanki#"):
        return (False, None)
    f = get_synced_conf()["decks_or_tags"]
    if message == "Pokemanki#currentDeck":
        html = pokemon_display(f, False).replace("`", "'")
    elif message == "Pokemanki#wholeCollection":
        html = pokemon_display(f, True).replace("`", "'")
    else:
        starts = "Pokemanki#search#"
        term = message[len(starts) :]
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

    statsDialog.form.web.loadFinished.connect(lambda _: _onStatsOpen(statsDialog))


def replace_gears(deck_browser, content):
    conf = get_synced_conf()
    if not conf:
        return
    pokemons = conf["pokemon_list"]
    soup = BeautifulSoup(content.tree, "html.parser")
    for tr in soup.select("tr[id]"):
        deck_id = int(tr["id"])
        name = next((pokemon[0] for pokemon in pokemons if pokemon[1] == deck_id), None)
        if name:
            tr.select("img.gears")[0]["src"] = "pokemon_images/" + name + ".png"
    content.tree = soup


def pokemanki_init():
    init_config()
    mw.pokemenu = QMenu("&Pokémanki", mw)
    build_menu()
    gui_hooks.deck_browser_will_render_content.append(replace_gears)


def delayed_init():
    mw.progress.single_shot(50, pokemanki_init)


gui_hooks.profile_did_open.append(delayed_init)
gui_hooks.stats_dialog_will_show.append(onStatsOpen)
gui_hooks.webview_did_receive_js_message.append(message_handler)
