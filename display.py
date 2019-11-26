import inspect, os
import math
from .compute import DeckPokemon, MultiPokemon
from anki.lang import _
import json
from collections import namedtuple
from aqt import mw
import shutil

# Display function that gets wrapped into anki.stats.py
def pokemonDisplay(*args, **kwargs):
    self = args[0]
    old = kwargs['_old']
    profilename = mw.pm.name
    # Find current directory
    currentdirname = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    # Assign Pokemon Image and Progress Bar folder directory names
    pkmnimgfolder = currentdirname + "/pokemon_images"
    progressbarfolder = currentdirname + "/progress_bars"
    ankifolder = os.path.dirname(os.path.dirname(currentdirname))
    if os.path.exists("%s/%s" % (ankifolder, profilename)):
        profilefolder = ("%s/%s" % (ankifolder, profilename))
    # Get to collection.media folder
    if os.path.exists("%s/collection.media" % profilefolder):
        mediafolder = "%s/collection.media" % profilefolder
    # Move Pokemon Image folder to collection.media folder if not already there (Anki reads from here when running anki.stats.py)
    if os.path.exists("%s/pokemon_images" % mediafolder) == False and os.path.exists(pkmnimgfolder):
        shutil.copytree(pkmnimgfolder, "%s/pokemon_images" % mediafolder)
    if os.path.exists("%s/progress_bars" % mediafolder) == False and os.path.exists(progressbarfolder):
        shutil.copytree(progressbarfolder, "%s/progress_bars" % mediafolder)
    # Assign deckmon and multideckmon variables (either tuple or list of tuples)
    deckmon = ()
    multideckmon = []
    # Get id of active deck
    did = self.col.decks.active()
    # See if "Whole Collection" is selected - if so, get all assigned Pokemon and assign to multideckmon
    if self.wholeCollection:
        multideckmon = MultiPokemon(*args, **kwargs)
    # If "Whole Collection" not selected, show Pokemon for either single deck or all subdecks and store into multideckmon/deckmon
    elif len(did) > 1:
        multideckmon = MultiPokemon(*args, **kwargs)
    else:
        deckmon = DeckPokemon(*args, **kwargs)

    # Get old result and add new tables with Pokemon
    result = old(self)
    if deckmon:
        result += _show(self,
                    deckmon,
                    "Pokémon",
                    "Your Pokémon")
    elif multideckmon:
        result += _show(self,
                    multideckmon,
                    "Pokémon",
                    "Your Pokémon")
    # Return result
    return result

def _show(self, data, title, subtitle):

    # Return empty if no data
    if not data:
        return ""
    # Set text equal to title text to start
    txt = self._title(_(title), _(subtitle))
    # Line text variable, apparently needed for bottom line
    text_lines = []
    # Table text
    table_text = ""
    if os.path.exists("_prestigelist.json"):
        prestigelist = json.load(open("_prestigelist.json"))
    else:
        prestigelist = []
    # If single Pokemon, show centered picture with name and level below
    if type(data) == tuple:
        # Don't show level for egg
        if data[0] == "Egg":
            if len(data) == 4:
                if int(data[2]) == 1:
                    text = ("%s (needs a lot more time to hatch)" % data[3])
                elif int(data[2]) == 2:
                    text = ("%s (will take some time to hatch)" % data[3])
                elif int(data[2]) == 3:
                    text = ("%s (moves around inside sometimes)" % data[3])
                elif int(data[2]) == 4:
                    text = ("%s (making sounds inside)" % data[3])
            else:
                if int(data[2]) == 1:
                    text = ("%s (needs a lot more time to hatch)" % data[0])
                elif int(data[2]) == 2:
                    text = ("%s (will take some time to hatch)" % data[0])
                elif int(data[2]) == 3:
                    text = ("%s (moves around inside sometimes)" % data[0])
                elif int(data[2]) == 4:
                    text = ("%s (making sounds inside)" % data[0])
        else:
            if data[1] in prestigelist:
                if len(data) == 4:
                    text = ("%s (Level %s)" % (data[3], int(data[2]) - 50))
                else:
                    text = ("%s (Level %s)" % (data[0], int(data[2]) - 50))
            else:
                if len(data) == 4:
                    text = ("%s (Level %s)" % (data[3], int(data[2])))
                else:
                    text = ("%s (Level %s)" % (data[0], int(data[2])))
        table_text += (("""<tr>
                        <td height = 300 width = 300 align = center><img src="/pokemon_images/%s.png" title=%s></td>""") % (data[0], self.col.decks.name(data[1])))
        table_text += (("""<tr>
                           <td height = 30 width = 250 align = center><b>%s</b></td>
                           </tr>""") % text)
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
        sorteddata = sorted(data, key = lambda k: k[2], reverse = True)
        for pokemon in sorteddata:
            if len(pokemon) == 4:
                pokemon_nicknames.append(pokemon[3])
            else:
                pokemon_nicknames.append(None)
            pokemon_names.append(pokemon[0])
            pokemon_decks.append(pokemon[1])
            pokemon_levels.append(str(pokemon[2]))
        pokemon_collection = tuple(zip(pokemon_names, pokemon_decks, pokemon_levels, pokemon_nicknames))
        pokemon_progress = []
        for level in pokemon_levels:
            if float(level) < 5:
                pokemon_progress.append(None)
            else:
                pokemon_progress.append(int(float(20*(float(level) - int(float(level))))))
        pokemon_progress_text = []
        for item in pokemon_progress:
            if item is not None:
                pokemon_progress_text.append("""<img src="/progress_bars/%s.png">""" % item)
            else:
                pokemon_progress_text.append("")
        pokemon_text = []
        table_size = 0
        for name, deck, level, nickname in pokemon_collection:
            if int(float(level)) < 5:
                if nickname:
                    if int(float(level)) == 1:
                        text = ("%s (needs a lot more time to hatch)" % nickname)
                    elif int(float(level)) == 2:
                        text = ("%s (will take some time to hatch)" % nickname)
                    elif int(float(level)) == 3:
                        text = ("%s (moves around inside sometimes)" % nickname)
                    elif int(float(level)) == 4:
                        text = ("%s (making sounds inside)" % nickname)
                else:
                    if int(float(level)) == 1:
                        text = ("%s (needs a lot more time to hatch)" % name)
                    elif int(float(level)) == 2:
                        text = ("%s (will take some time to hatch)" % name)
                    elif int(float(level)) == 3:
                        text = ("%s (moves around inside sometimes)" % name)
                    elif int(float(level)) == 4:
                        text = ("%s (making sounds inside)" % name)
            else:
                if deck in prestigelist:
                    if nickname:
                        text = ("%s (Level %s) - Prestiged" % (nickname, int(float(level)) - 50))
                    else:
                        text = ("%s (Level %s) - Prestiged" % (name, int(float(level)) - 50))
                else:
                    if nickname:
                        text = ("%s (Level %s)" % (nickname, int(float(level))))
                    else:
                        text = ("%s (Level %s)" % (name, int(float(level))))
            pokemon_text.append(text)
            while table_size < (len(pokemon_text) - 2):
                table_text += (("""<tr>
                                   <td height = 250 width = 250 align = center><img src="/pokemon_images/%s.png" title="%s"></td>
                                   <td height = 250 width = 250 align = center><img src="/pokemon_images/%s.png" title="%s"></td>
                                   <td height = 250 width = 250 align = center><img src="/pokemon_images/%s.png" title="%s"></td>
                                   </tr>""") % (pokemon_names[table_size], self.col.decks.name(pokemon_decks[table_size]), pokemon_names[table_size+1], self.col.decks.name(pokemon_decks[table_size+1]), pokemon_names[table_size+2], self.col.decks.name(pokemon_decks[table_size+2])))
                table_text += (("""<tr>
                                   <td height = 30 width = 250 align = center><b>%s</b></td>
                                   <td height = 30 width = 250 align = center><b>%s</b></td>
                                   <td height = 30 width = 250 align = center><b>%s</b></td>
                                   </tr>""") % (pokemon_text[table_size], pokemon_text[table_size+1], pokemon_text[table_size+2]))
                table_text += (("""<tr>
                                   <td height = 30 width = 250 align = center>%s</td>
                                   <td height = 30 width = 250 align = center>%s</td>
                                   <td height = 30 width = 250 align = center>%s</td>
                                   </tr>""") % (pokemon_progress_text[table_size], pokemon_progress_text[table_size+1], pokemon_progress_text[table_size+2]))
                table_size += 3
        # Dealing with incomplete rows
        if len(pokemon_text) % 3 == 0:
            pass
        elif len(pokemon_text) % 3 == 1:
            table_text += (("""<tr>
                               <td height = 250 width = 250 align = center><img src="/pokemon_images/%s.png" title="%s"></td>
                               <td height = 250 width = 250 align = center></td>
                               <td height = 250 width = 250 align = center></td>
                               </tr>""") % (pokemon_names[table_size], self.col.decks.name(pokemon_decks[table_size])))
            table_text += (("""<tr>
                               <td height = 30 width = 250 align = center><b>%s</b></td>
                               <td height = 30 width = 250 align = center></td>
                               <td height = 30 width = 250 align = center></td>
                               </tr>""") % (pokemon_text[table_size]))
            table_text += (("""<tr>
                               <td height = 30 width = 250 align = center>%s</td>
                               <td height = 30 width = 250 align = center></td>
                               <td height = 30 width = 250 align = center></td>
                               </tr>""") % (pokemon_progress_text[table_size]))
        elif len(pokemon_text) % 3 == 2:
            table_text += (("""<tr>
                               <td height = 250 width = 250 align = center><img src="/pokemon_images/%s.png" title="%s"></td>
                               <td height = 250 width = 250 align = center><img src="/pokemon_images/%s.png" title="%s"></td>
                               <td height = 250 width = 250 align = center></td>
                               </tr>""") % (pokemon_names[table_size], self.col.decks.name(pokemon_decks[table_size]), pokemon_names[table_size+1], self.col.decks.name(pokemon_decks[table_size+1])))
            table_text += (("""<tr>
                               <td height = 30 width = 250 align = center><b>%s</b></td>
                               <td height = 30 width = 250 align = center><b>%s</b></td>
                               <td height = 30 width = 250 align = center></td>
                               </tr>""") % (pokemon_text[table_size], pokemon_text[table_size+1]))
            table_text += (("""<tr>
                               <td height = 30 width = 250 align = center>%s</td>
                               <td height = 30 width = 250 align = center>%s</td>
                               <td height = 30 width = 250 align = center></td>
                               </tr>""") % (pokemon_progress_text[table_size], pokemon_progress_text[table_size+1]))
        # Assign table_text to txt
        txt += "<table width = 750>" + table_text + "</table>"
        # Make bottom line using function from stats.py and assign to text_lines
        self._line(
            text_lines,
            _("<b>Total</b>"),
            _("</b>%s Pokémon<b>") % _num_pokemon)
        # Make table from bottom line and assign to txt
        txt += self._lineTbl(text_lines)
    # Return txt
    return txt
