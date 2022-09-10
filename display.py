import os
import shutil
import random

from anki.lang import _
from aqt import mw

from .utils import *
from .compute import MultiPokemon


def pokemonDisplay(wholeCollection):
    """
    Control the generation of the html code to displau.

    :param bool wholeCollection: True if multiple Pokemon, false if single.
    :return: The html text to display.
    :rtype: str
    """

    # Assign Pokemon Image and Progress Bar folder directory names
    pkmnimgfolder = currentdirname / "pokemon_images"
    progressbarfolder = currentdirname / "progress_bars"

    # Move Pokemon Image folder to collection.media folder if not already there (Anki reads from here when running anki.stats.py)
    if os.path.exists("%s/pokemon_images" % mediafolder) == False and os.path.exists(pkmnimgfolder):
        shutil.copytree(pkmnimgfolder, "%s/pokemon_images" % mediafolder)
    if os.path.exists("%s/progress_bars" % mediafolder) == False and os.path.exists(progressbarfolder):
        shutil.copytree(progressbarfolder, "%s/progress_bars" % mediafolder)

    # See if "Whole Collection" is selected - if so, get all assigned Pokemon and assign to multideckmon
    if wholeCollection:
        multideckmon = MultiPokemon(wholeCollection=True)
    # If "Whole Collection" not selected, show Pokemon for either single deck or all subdecks
    # and store into multideckmon/deckmon
    else:
        multideckmon = MultiPokemon(wholeCollection=False)

    # Get the html code to display
    result = _show(multideckmon)

    return result


def _show(data):
    """
    Generate the html to inject into the new stats window.

    :param data: Pokemon information. Tuple if single Pokemon, list if collection.
    :return: The html code to display.
    :rtype: str
    """

    if not data:
        return ""

    txt = '<h1 style="text-align: center; font-weight: 700; margin-top: 40px;">Pokemanki</h1>' \
          '<div style="text-align: center;">Your pokemon</div>'

    # If single Pokemon, show centered picture with name and level below
    if type(data) == tuple:
        txt += '<div class="pk-st-single">'
        txt += card_html(data[0], data[1], data[2], data[3] if len(data) == 4 else "")
    # If multiple Pokemon, show table of Pokemon with name and level below
    elif type(data) == list:
        if len(data) == 1:
            txt += '<div class="pk-st-single">'
            multi = False
        else:
            txt += '<div class="pk-st-container">'
            multi = True

        _num_pokemon = len(data)
        sortedData = sorted(data, key=lambda k: k[2], reverse=True)
        for pokemon in sortedData:
            txt += card_html(pokemon[0], pokemon[1], pokemon[2], pokemon[3] if len(pokemon) == 4 else "", multi)

    txt += '</div>'

    # Return txt
    return txt


def card_html(name, deckid, level, nickname="", multi=False):
    """
    Generate the html text for a Pokemon card.

    :param str name: Name of the Pokemon.
    :param int deckid: Id of the deck the Pokemon belongs to.
    :param int level: The Pokemon's lvl.
    :param str nickname: Pokemon's nickname, if it has any.
    :param bool multi: True if multiple Pokemon are being rendered.
    :return: The card html.
    :rtype: str
    """
    # Start card
    card = '<div class="pk-st-card {}">'.format('pk-st-shrink' if multi else "")

    #############
    # Head info
    #############
    card += '<div class="pk-st-card-info" style="margin-bottom: auto;">' \
            '<div class="pk-st-card-top">'
    # Name and deck
    card += '<div class="pk-st-card-name">' \
            '<span><b>{}</b></span>' \
            '<span><i>{}</i></span>' \
            '</div>'.format(nickname if nickname != "" else name, get_deck_name(deckid))
    # Level
    card += '<div class="pk-st-card-lvl">' \
            '<span style="text-align: right;">Lvl</span>' \
            '<span style="text-align: right;"><b>{}</b></span>' \
            '</div>' \
            '</div>'.format(int(level))
    # Divider and end of top info
    card += '<div class="pk-st-divider" style="margin-top: 10px;"></div>' \
            '</div>'

    #############
    # Image
    #############
    card += '<img src="/pokemon_images/{}.png" class="pk-st-card-img"/>'.format(image_name(name, deckid))

    #############
    # Bottom info
    #############
    card += '<div class="pk-st-card-info" style="margin-top: auto;">' \
            '<div class="pk-st-divider" style="margin-bottom: 10px;"></div>'
    # Held/SP
    held = held_html(deckid)
    if held != "":
        card += '<div class="pk-st-card-sp">' \
                '<span><b>SP: </b></span>'
        card += held
        card += '</div>'
    # Progress bar
    if name == "Egg":
        card += '<span class="pk-st-card-xp">{}</span>'.format(egg_hatch_text(level))
    else:
        card += '<img src="/progress_bars/{}.png" class="pk-st-card-xp"/>'.format(calculate_xp_progress(level))
    card += '</div>'

    # End card
    card += '</div>'

    return card


def get_deck_name(deckid):
    """
    Get the name of the deck based on its id.

    :param int deckid: Deck's id.
    :return: The name of the deck
    :rtype: str
    """

    return mw.col.decks.name(deckid)


def image_name(name, deckid):
    """
    Get the image name based on the Pokemon's name and any special attributes.

    :param str name: Pokemon's name.
    :param int deckid: Id of the deck the Pokemon belongs to.
    :return: The image name to be used to retrieve it.
    :rtype: str
    """

    everstonelist = get_json("_everstonelist.json", [])
    megastonelist = get_json("_megastonelist.json", [])
    alolanlist = get_json("_alolanlist.json", [])
    pkmnimgfolder = currentdirname / "pokemon_images"

    fullname = name
    if deckid in everstonelist:
        # FIX: name is never declared!u
        if name == "Pikachu":
            fullname += "_Ash" + str(random.randint(1, 5))
    if deckid in megastonelist:
        if any([name + "_Mega" in imgname for imgname in os.listdir(pkmnimgfolder)]):
            fullname += "_Mega"
            if name == "Charizard" or name == "Mewtwo":
                fullname += config["X_or_Y_mega_evolutions"]
    if deckid in alolanlist:
        if any([name + "_Alolan" in imgname for imgname in os.listdir(pkmnimgfolder)]):
            fullname += "_Alolan"

    return fullname


def egg_hatch_text(level):
    """
    Get the egg's hatch text.

    :param int level: The level of the egg.
    :return: The hatch text.
    :rtype: str
    """
    if level < 2:
        return "Needs a lot more time to hatch"
    elif level < 3:
        return "Will take some time to hatch"
    elif level < 4:
        return "Moves around inside sometimes"
    else:
        return "Making sounds inside"


def calculate_xp_progress(level):
    """
    Calculate the xp progress for the xp bar based on the given level.

    :param int level: The level to base the calculations on.
    :return: The progress in the xp bar.
    :rtype: int
    """
    return int(float(20*(float(level) - int(float(level)))))


def held_html(deckid):
    """
    Generate the held html code for the given Pokemon.

    :param int deckId: Id of the deck the Pokemon belongs to.
    :return: The concatenation of all held items' html. Empty if it has no items.
    :rtype: str
    """
    """Generate the held html code for the given Pokemon"""
    prestigelist = get_json("_prestigelist.json", [])
    everstonelist = get_json("_everstonelist.json", [])
    megastonelist = get_json("_megastonelist.json", [])
    alolanlist = get_json("_alolanlist.json", [])

    held = ""
    everstone_html = '<img src="/pokemon_images/item_Everstone.png" height="20px"/>'
    megastone_html = '<img src="/pokemon_images/item_Mega_Stone.png" height="25px"/>'
    alolan_html = '<img src="/pokemon_images/item_Alolan_Passport.png" height="25px"/>'

    if deckid in prestigelist:
        held += '<span>Prestiged </span>'
    if deckid in everstonelist:
        held += everstone_html
    if deckid in alolanlist:
        held += alolan_html
    if deckid in megastonelist:
        held += megastone_html

    return held


# Deprecated: For tagmon.py only
def eggHatchText(level, name):
    if level < 2:
        text = ("%s (needs a lot more time to hatch)" % name)
    elif level < 3:
        text = ("%s (will take some time to hatch)" % name)
    elif level < 4:
        text = ("%s (moves around inside sometimes)" % name)
    else:
        text = ("%s (making sounds inside)" % name)
    return text


def pokemonDisplayText(name, id, level, nickname):
    prestigelist = get_json("_prestigelist.json", [])
    everstonelist = get_json("_everstonelist.json", [])
    megastonelist = get_json("_megastonelist.json", [])
    alolanlist = get_json("_alolanlist.json", [])

    held = ""
    special = ""
    everstone_html = '<img src="/pokemon_images/item_Everstone.png" hspace="10">'
    megastone_html = '<img src="/pokemon_images/item_Mega_Stone.png" hspace="10">'
    alolan_html = '<img src="/pokemon_images/item_Alolan_Passport.png" hspace="10">'
    pkmnimgfolder = currentdirname / "pokemon_images"

    level = int(float(level))  # float string such as "1.2"

    displayname = name
    if nickname:
        displayname = nickname
    if name == "Egg":
        text = eggHatchText(level, displayname)
    else:
        if id in prestigelist:
            text = ("%s (Level %s) - Prestiged" %
                    (displayname, level - 50))
        else:
            text = ("%s (Level %s)" % (displayname, level))
        if id in everstonelist:
            held += everstone_html
            # FIX: name is never declared!
            if name == "Pikachu":
                special += "_Ash" + str(random.randint(1, 5))
        if id in megastonelist:
            held += megastone_html

            if any([name + "_Mega" in imgname for imgname in os.listdir(pkmnimgfolder)]):
                special += "_Mega"
                if name == "Charizard" or name == "Mewtwo":
                    special += config["X_or_Y_mega_evolutions"]
        if id in alolanlist:
            held += alolan_html
            if any([name + "_Alolan" in imgname for imgname in os.listdir(pkmnimgfolder)]):
                special += "_Alolan"

    return (text, held, special)