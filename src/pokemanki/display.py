import os
import shutil
import random

from anki.lang import _
from aqt import mw

from .utils import *
from .compute import MultiPokemon, TagPokemon


def pokemon_display(istagmon, wholecollection=True):
    """
    Control the generation of the html code to display.

    :param bool istagmon: True to switch to use tag's displau, False for deck.
    :param bool wholecollection: True if multiple Pokémon, false if single.
    :return: The html text to display.
    :rtype: str
    """

    # Assign Pokémon Image and Progress Bar folder directory names
    pkmnimgfolder = currentdirname / "pokemon_images"
    progressbarfolder = currentdirname / "progress_bars"

    # Move Pokémon Image folder to collection.media folder if not already there
    # (Anki reads from here when running anki.stats.py)
    if (not os.path.exists(f"{mediafolder}/pokemon_images")) and os.path.exists(
        pkmnimgfolder
    ):
        shutil.copytree(pkmnimgfolder, f"{mediafolder}/pokemon_images")
    if (not os.path.exists(f"{mediafolder}/progress_bars")) and os.path.exists(
        progressbarfolder
    ):
        shutil.copytree(progressbarfolder, f"{mediafolder}/progress_bars")

    # Get list of Pokémon from tags or decks.
    #   For decks, if wholeCollection, get all assigned Pokémon and assign to Pokémon,
    #   else, show Pokémon for either single deck or all subdecks and store in Pokémon
    if istagmon == "tags":
        pokemon = TagPokemon()
    else:
        pokemon = MultiPokemon(wholecollection)

    result = _show(pokemon)

    return result


def _show(data):
    """
    Generate the html to inject into the new stats window.

    :param data: Pokémon information. Tuple if single Pokémon, list if collection.
    :return: The html code to display.
    :rtype: str
    """

    if not data:
        return ""

    # Pokemanki container header
    txt = (
        '<h1 style="text-align: center; font-weight: 700; margin-top: 40px;">Pokémon</h1>'
        '<div style="text-align: center;">Your Pokémon</div>'
    )

    # If single Pokémon, show centered card
    if type(data) == tuple:
        txt += '<div class="pk-st-single">'
        txt += _card_html(data[0], data[1], data[2], data[3] if len(data) == 4 else "")
    # If multiple Pokémon, show flex row of cards
    elif type(data) == list:
        if len(data) == 1:
            txt += '<div class="pk-st-single">'
            multi = False
        else:
            txt += '<div class="pk-st-container">'
            multi = True

        sortedData = sorted(data, key=lambda k: k[2], reverse=True)
        for pokemon in sortedData:
            txt += _card_html(
                pokemon[0],
                pokemon[1],
                pokemon[2],
                pokemon[3] if len(pokemon) == 4 else "",
                multi,
            )

    # Close cards container
    txt += "</div>"

    # Pokémon total
    txt += f'<h4 style="text-align: center; margin-top: 5px;"><b>Total:</b> {len(data)} Pokémon</h4>'

    # Return txt
    return txt


def _card_html(name, source, level, nickname="", multi=False):
    """
    Generate the html text for a Pokémon card.

    :param str name: Name of the Pokémon.
    :param source: Id of the deck or name of the tqg the Pokémon belongs to.
    :param int level: The Pokémon's lvl.
    :param str nickname: Pokémon's nickname, if it has any.
    :param bool multi: True if multiple Pokémon are being rendered.
    :return: The card html.
    :rtype: str
    """
    # Start card
    card = f'<div class="pk-st-card {"pk-st-shrink" if multi else ""}">'

    #############
    # Head info
    #############
    card += (
        '<div class="pk-st-card-info" style="margin-bottom: auto;">'
        '<div class="pk-st-card-top">'
    )
    # Name and deck
    card += (
        '<div class="pk-st-card-name">'
        f'<span><b>{nickname if nickname != "" else name}</b></span>'
        f"<span><i>{_get_source_name(source)}</i></span>"
        "</div>"
    )
    # Level
    card += (
        '<div class="pk-st-card-lvl">'
        '<span style="text-align: right;">Lvl</span>'
        '<span style="text-align: right;">'
        f'<b>{int(level-50) if _in_list("prestige", source) else int(level)}</b>'
        "</span>"
        "</div>"
        "</div>"
    )
    # Divider and end of top info
    card += '<div class="pk-st-divider" style="margin-top: 10px;"></div>' "</div>"

    #############
    # Image
    #############
    card += f'<img src="/pokemon_images/{_image_name(name, source)}.png" class="pk-st-card-img"/>'

    #############
    # Bottom info
    #############
    card += (
        '<div class="pk-st-card-info" style="margin-top: auto;">'
        '<div class="pk-st-divider" style="margin-bottom: 10px;"></div>'
    )
    # Held/SP
    held = _held_html(source)
    if held != "":
        card += '<div class="pk-st-card-sp">' "<span><b>SP: </b></span>"
        card += held
        card += "</div>"
    # Progress bar
    if name == "Egg":
        card += f'<span class="pk-st-card-xp">{_egg_hatch_text(level)}</span>'
    else:
        card += f'<img src="/progress_bars/{_calculate_xp_progress(level)}.png" class="pk-st-card-xp"/>'
    card += "</div>"

    # End card
    card += "</div>"

    # TODO: Add # of Pokémon
    # Make bottom line using function from stats.py and assign to text_lines
    # line( text_lines, "<b>Total</b>", "</b>%s Pokémon<b>" % _num_pokemon)

    return card


def _get_source_name(item):
    """
    Get the name of the tag or deck based on the input item.

    :param item: Element to find the source of
    :return: The name of the deck
    """

    if isinstance(item, int):
        return mw.col.decks.name(item)
    else:
        return item


def _in_list(listname, item):
    """
    Check if an item is in a list. Mainly used to avoid copy/pasting code
    to open the json files.

    :param str listname: Name of the list to check in.
    :param item: Item to find in the list
    :return: True if the list exists and the item is in it, otherwise false.
    :rtype: bool
    """

    if listname not in ["prestige", "everstone", "megastone", "alolan"]:
        return False

    return item in get_synced_conf()[f"{listname}list"]


def _image_name(name, source):
    """
    Get the image name based on the Pokémon's name and any special attributes.

    :param str name: Pokémon's name.
    :param source: Id of the deck or tag name the Pokémon belongs to.
    :return: The image name to be used to retrieve it.
    :rtype: str
    """

    pkmnimgfolder = currentdirname / "pokemon_images"

    fullname = name
    if _in_list("everstone", source):
        # FIX: name is never declared!u
        if name == "Pikachu":
            fullname += "_Ash" + str(random.randint(1, 5))
    if _in_list("megastone", source):
        if any([name + "_Mega" in imgname for imgname in os.listdir(pkmnimgfolder)]):
            fullname += "_Mega"
            if name == "Charizard" or name == "Mewtwo":
                fullname += config["X_or_Y_mega_evolutions"]
    if _in_list("alolan", source):
        if any([name + "_Alolan" in imgname for imgname in os.listdir(pkmnimgfolder)]):
            fullname += "_Alolan"

    return fullname


def _egg_hatch_text(level):
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


def _calculate_xp_progress(level):
    """
    Calculate the xp progress for the xp bar based on the given level.

    :param int level: The level to base the calculations on.
    :return: The progress in the xp bar.
    :rtype: int
    """
    return int(float(20 * (float(level) - int(float(level)))))


def _held_html(source):
    """
    Generate the held html code for the given Pokémon.

    :param source: Id of the deck or tag name the Pokémon belongs to.
    :return: The concatenation of all held items' html. Empty if it has no items.
    :rtype: str
    """

    held = ""
    everstone_html = '<img src="/pokemon_images/item_Everstone.png" height="20px"/>'
    megastone_html = '<img src="/pokemon_images/item_Mega_Stone.png" height="25px"/>'
    alolan_html = '<img src="/pokemon_images/item_Alolan_Passport.png" height="25px"/>'

    if _in_list("prestige", source):
        held += "<span>Prestiged </span>"
    if _in_list("everstone", source):
        held += everstone_html
    if _in_list("alolan", source):
        held += alolan_html
    if _in_list("megastone", source):
        held += megastone_html

    return held
