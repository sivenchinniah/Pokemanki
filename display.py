import inspect, os
import math
from .compute import DeckPokemon, MultiPokemon
from anki.lang import _
import json
from collections import namedtuple

# Display function that gets wrapped into anki.stats.py
def pokemonDisplay(*args, **kwargs):
    self = args[0]
    old = kwargs['_old']
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
    # If single Pokemon, show centered picture with name and level below
    if type(data) == tuple:
        # Don't show level for egg
        if data[0] == "Egg":
            text = data[0]
        else:
            text = ("%s (Level %s)" % (data[0], data[2]))
        table_text += (("""<tr>
                        <td height = 300 width = 300 align = center><img src="/pokemon_images/%s.png" title=%s></td>""") % (data[0], self.col.decks.name(data[1])))
        table_text += (("""<tr>
                           <td height = 30 width = 250 align = center><b>%s</b></td>
                           </tr>""") % text)
        # Add table_text to txt
        txt += "<table width = 300>" + table_text + "</table>"
    # If multiple Pokemon, show table of Pokemon with name and level below
    elif type(data) == list:
        _num_pokemon = len(data)
        pokemon_names = []
        pokemon_decks = []
        pokemon_levels = []
        sorteddata = sorted(data, key = lambda k: k[2], reverse = True)
        for pokemon in sorteddata:
            pokemon_names.append(pokemon[0])
            pokemon_decks.append(pokemon[1])
            pokemon_levels.append(str(pokemon[2]))
        pokemon_collection = tuple(zip(pokemon_names, pokemon_levels))
        pokemon_text = []
        table_size = 0
        for name, level in pokemon_collection:
            if name == "Egg":
                text = name
            else:
                text = ("%s (Level %s)" % (name, level))
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
