import os
import shutil
import random

from anki.lang import _
from aqt import mw

from .utils import *
from .compute import MultiPokemon


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


def pokemonDisplay(wholeCollection):
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
    # If "Whole Collection" not selected, show Pokemon for either single deck or all subdecks and store into multideckmon/deckmon
    else:
        multideckmon = MultiPokemon(wholeCollection=False)
    # Get old result and add new tables with Pokemon
    result = _show(
        multideckmon,
        "Pokémon",
        "Your Pokémon")
    # Return result
    return result


def _show(data, title, subtitle):

    # Return empty if no data
    if not data:
        return ""
    # Set text equal to title text to start
    txt = "<h1 style='text-align: center;'>{}</h1>{}".format(
        title, subtitle)
    # Line text variable, apparently needed for bottom line
    text_lines = []
    # Table text
    table_text = ""

    # If single Pokemon, show centered picture with name and level below
    if type(data) == tuple:
        nickname = ""
        if len(data) == 4:
            nickname = data[3]
        (text, held, special) = pokemonDisplayText(
            data[0], data[1], data[2], nickname)

        table_text += (("""<tr>
                        <td height = 300 width = 300 align = center><img src="/pokemon_images/%s.png" title=%s></td>""") % (data[0] + special, mw.col.decks.name(data[1])))
        table_text += (("""<tr>
                           <td height = 30 width = 250 align = center><b>%s</b>%s</td>
                           </tr>""") % (text, held))
        if int(data[2]) > 5:
            table_text += (("""<tr>
                               <td height = 30 width = 250 align = center><img src="/progress_bars/%s.png"></td>
                               </tr>""") % int(20*(data[2] - int(data[2]))))
        # Add table_text to txt
        txt += "<table width = 300>" + table_text + "</table>"
    # If multiple Pokemon, show table of Pokemon with name and level below
    elif type(data) == list:
        _num_pokemon = len(data)
        pokemon_names = []
        pokemon_decks = []
        pokemon_levels = []
        pokemon_nicknames = []
        sorteddata = sorted(data, key=lambda k: k[2], reverse=True)
        for pokemon in sorteddata:
            if len(pokemon) == 4:
                pokemon_nicknames.append(pokemon[3])
            else:
                pokemon_nicknames.append(None)
            pokemon_names.append(pokemon[0])
            pokemon_decks.append(pokemon[1])
            pokemon_levels.append(str(pokemon[2]))
        pokemon_collection = tuple(
            zip(pokemon_names, pokemon_decks, pokemon_levels, pokemon_nicknames))
        pokemon_progress = []
        for level in pokemon_levels:
            if float(level) < 5:
                pokemon_progress.append(None)
            else:
                pokemon_progress.append(
                    int(float(20*(float(level) - int(float(level))))))
        pokemon_progress_text = []
        for item in pokemon_progress:
            if item is not None:
                pokemon_progress_text.append(
                    """<img src="/progress_bars/%s.png">""" % item)
            else:
                pokemon_progress_text.append("")
        pokemon_text = []
        pokemon_held_items = []
        pokemon_is_special = []
        table_size = 0
        for name, deckid, level, nickname in pokemon_collection:
            (text, held, special) = pokemonDisplayText(
                name, deckid, level, nickname)
            pokemon_text.append(text)
            pokemon_held_items.append(held)
            pokemon_is_special.append(special)

        def format_table_image(index):
            image_name = ""
            title = ""
            if index < len(pokemon_names) and index < len(pokemon_is_special) and index < len(pokemon_decks):
                image_name = pokemon_names[index] + \
                    pokemon_is_special[index]
                title = mw.col.decks.name(pokemon_decks[index])
            return table_image_html(image_name, title)

        def format_table_text(index):
            bolded = ""
            subtext = ""
            if index < len(pokemon_text):
                bolded = pokemon_text[index]
                subtext = pokemon_held_items[index]

            return table_text_html(bolded, subtext, True)

        def format_table_progress(index):
            text = ""
            if index < len(pokemon_progress_text):
                text = pokemon_progress_text[index]

            return table_text_html(text)

        while table_size < len(pokemon_text):
            #   style="position:absolute; top: 1000; right: 1000"
            table_text += "\n".join((
                "<tr>",
                format_table_image(table_size),
                format_table_image(table_size + 1),
                format_table_image(table_size + 2),
                "</tr>"
            ))
            table_text += "\n".join((
                "<tr>",
                format_table_text(table_size),
                format_table_text(table_size + 1),
                format_table_text(table_size + 2),
                "</tr>"
            ))
            table_text += "\n".join((
                "<tr>",
                format_table_progress(table_size),
                format_table_progress(table_size + 1),
                format_table_progress(table_size + 2),
                "</tr>"
            ))
            table_size += 3
        # Assign table_text to txt
        txt += "<table width = 750>" + table_text + "</table>"
        # Make bottom line using function from stats.py and assign to text_lines
        line(
            text_lines,
            "<b>Total</b>",
            "</b>%s Pokémon<b>" % _num_pokemon)
        # Make table from bottom line and assign to txt
        txt += lineTbl(text_lines)
    # Return txt
    return txt
