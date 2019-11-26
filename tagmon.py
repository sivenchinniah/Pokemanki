from aqt import *
from aqt.qt import *
import json
import random
import os, inspect

def tagmonDisplay(*args, **kwargs):
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
    if os.path.exists("_tags.json"):
        savedtags = json.load(open("_tags.json"))
    else:
        savedtags = []
    tagmon = TagPokemon()
    result = old(self)
    if tagmon:
        result += _show(self, tagmon, "Pokémon",
                    "Your Pokémon")
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
    profilename = mw.pm.name
    ankifolder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
    if os.path.exists("%s/%s" % (ankifolder, profilename)):
        profilefolder = ("%s/%s" % (ankifolder, profilename))
    if os.path.exists("%s/collection.media" % profilefolder):
        mediafolder = "%s/collection.media" % profilefolder
    table_text = ""
    _num_pokemon = len(data)
    pokemon_names = []
    pokemon_tags = []
    pokemon_levels = []
    pokemon_nicknames = []
    sorteddata = sorted(data, key = lambda k: k[2], reverse = True)
    for pokemon in sorteddata:
        if len(pokemon) == 4:
            pokemon_nicknames.append(pokemon[3])
        else:
            pokemon_nicknames.append(None)
        pokemon_names.append(pokemon[0])
        pokemon_tags.append(pokemon[1])
        pokemon_levels.append(str(pokemon[2]))
    pokemon_collection = tuple(zip(pokemon_names, pokemon_tags, pokemon_levels, pokemon_nicknames))
    pokemon_progress = []
    for level in pokemon_levels:
        if float(level) < 5:
            pokemon_progress.append(None)
        else:
            pokemon_progress.append(int(float(20*(float(level) - int(float(level))))))
        pokemon_progress_text = []
        for item in pokemon_progress:
            if item is not None:
                pokemon_progress_text.append("""<img src="/progress_bars/%s.png">""" % (item))
            else:
                pokemon_progress_text.append("")
    pokemon_text = []
    table_size = 0
    if os.path.exists("_prestigelist.json"):
        prestigelist = json.load(open("_prestigelist.json"))
    else:
        prestigelist = []
    for name, tag, level, nickname in pokemon_collection:
        if int(float(level)) < 5:
            if nickname:
                if int(float(level)) < 2:
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
            if tag in prestigelist:
                if nickname:
                    text = ("%s (Level %s) - Prestiged" % (nickname, int(float(level))))
                else:
                    text = ("%s (Level %s) - Prestiged" % (name, int(float(level))))
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
                               </tr>""") % (pokemon_names[table_size], pokemon_tags[table_size], pokemon_names[table_size+1], pokemon_tags[table_size+1], pokemon_names[table_size+2], pokemon_tags[table_size+2]))
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
    if len(pokemon_text) % 3 == 0:
        pass
    elif len(pokemon_text) % 3 == 1:
        table_text += (("""<tr>
                            <td height = 250 width = 250 align = center><img src="/pokemon_images/%s.png" title="%s"></td>
                           <td height = 250 width = 250 align = center></td>
                           <td height = 250 width = 250 align = center></td>
                           </tr>""") % (pokemon_names[table_size], pokemon_tags[table_size]))
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
                           </tr>""") % (pokemon_names[table_size], pokemon_tags[table_size], pokemon_names[table_size+1], pokemon_tags[table_size+1]))
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
    return txt
def TagPokemon():
    if os.path.exists("_tags.json"):
        savedtags = json.load(open("_tags.json"))
    else:
        savedtags = []
    if os.path.exists("_tagmon.json"):
        tagmon = json.load(open('_tagmon.json'))
        sortedtagmon = list(reversed(tagmon))
        modifiedtagmon = []
        for item in sortedtagmon:
            for thing in modifiedtagmon:
                if item[1] == thing[1]:
                    break
            else:
                if item[1] in savedtags:
                    modifiedtagmon.append(item)
    else:
        modifiedtagmon = []
    if os.path.exists("_tagmonsettings.json"):
        thresholdsettings = json.load(open("_tagmonsettings.json"))
    else:
        thresholdsettings = [50, 125, 250, 375, 500]
    pokemonlist = ['Caterpie', 'Weedle', 'Pidgey', 'Rattata', 'Zubat', 'Spearow', 'Oddish', 'Paras', 'Venonat', 'Meowth', 'Bellsprout', 'Drowzee', 'Krabby', 'Horsea', 'Magikarp', 'Ekans', 'Nidoran F', 'Nidoran M', 'Clefairy', 'Jigglypuff', 'Diglett', 'Poliwag', 'Tentacool', 'Slowpoke', 'Magnemite', 'Doduo', 'Shellder', 'Gastly', 'Exeggcute', 'Cubone', 'Goldeen', 'Staryu', 'Eevee1', 'Eevee2', 'Eevee3', 'Sandshrew', 'Vulpix', 'Psyduck', 'Mankey', 'Growlithe', 'Abra', 'Machop', 'Geodude', 'Ponyta', 'Seel', 'Onix', 'Koffing', 'Scyther', 'Ditto', 'Bulbasaur', 'Charmander', 'Squirtle', 'Pikachu', 'Grimer', 'Lickitung', 'Rhyhorn', 'Tangela', 'Electabuzz', 'Magmar', 'Pinsir', 'Omanyte', 'Kabuto', 'Dratini', "Farfetch'd", 'Voltorb', 'Hitmonlee', 'Hitmonchan', 'Chansey', 'Kangaskhan', 'Mr. Mime', 'Jynx', 'Tauros', 'Lapras', 'Porygon', 'Aerodactyl', 'Snorlax', 'Moltres', 'Zapdos', 'Articuno', 'Mewtwo', 'Mew']
    tiers = ['D', 'D', 'D', 'E', 'E', 'E', 'D', 'E', 'E', 'D', 'D', 'D', 'E', 'E', 'B', 'D', 'D', 'D', 'E', 'E', 'E', 'D', 'E', 'E', 'D', 'E', 'D', 'B', 'C', 'D', 'E', 'D', 'B', 'B', 'B', 'E', 'D', 'E', 'E', 'B', 'B', 'B', 'B', 'C', 'E', 'D', 'E', 'C', 'F', 'A', 'A', 'A', 'D', 'E', 'F', 'B', 'F', 'C', 'C', 'C', 'D', 'D', 'B', 'F', 'E', 'C', 'C', 'F', 'C', 'F', 'F', 'C', 'C', 'F', 'C', 'C', 'S', 'S', 'S', 'S', 'S']
    evolutionLevel1 = [7, 7, 18, 20, 22, 20, 21, 24, 31, 28, 21, 26, 28, 32, 40, 22, 16, 16, 32, 32, 26, 25, 30, 37, 30, 31, 32, 25, 36, 28, 33, 25, 36, 36, 36, 22, 32, 33, 28, 36, 16, 28, 25, 40, 34, None, 35, None, None, 16, 16, 16, 32, 38, None, 42, None, None, None, None, 40, 40, 30, None, 30, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    evolution1 = ['Metapod', 'Kakuna', 'Pidgeotto', 'Raticate', 'Golbat', 'Fearow', 'Gloom', 'Parasect', 'Venomoth', 'Persian', 'Weepinbell', 'Hypno', 'Kingler', 'Seadra', 'Gyarados', 'Arbok', 'Nidorina', 'Nidorino', 'Clefable', 'Wigglytuff', 'Dugtrio', 'Poliwhirl', 'Tentacruel', 'Slowbro', 'Magneton', 'Dodrio', 'Cloyster', 'Haunter', 'Exeggutor', 'Marowak', 'Seaking', 'Starmie', 'Vaporeon', 'Jolteon', 'Flareon', 'Sandslash', 'Ninetales', 'Golduck', 'Primeape', 'Arcanine', 'Kadabra', 'Machoke', 'Graveler', 'Rapidash', 'Dewgong', None, 'Weezing', None, None, 'Ivysaur', 'Charmeleon', 'Wartortle', 'Raichu', 'Muk', None, 'Rhydon', None, None, None, None, 'Omastar', 'Kabutops', 'Dragonair', None, 'Electrode', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    evolutionLevel2 = [10, 10, 36, None, None, None, 36, None, None, None, 36, None, None, None, None, None, 32, 32, None, None, None, 36, None, None, None, None, None, 40, None, None, None, None, None, None, None, None, None, None, None, None, 40, 40, 40, None, None, None, None, None, None, 32, 36, 36, None, None, None, None, None, None, None, None, None, None, 55, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    evolution2 = ['Butterfree', 'Beedrill', 'Pidgeot', None, None, None, 'Vileplume', None, None, None, 'Victreebel', None, None, None, None, None, 'Nidoqueen', 'Nidoking', None, None, None, 'Poliwrath', None, None, None, None, None, 'Gengar', None, None, None, None, None, None, None, None, None, None, None, None, 'Alakazam', 'Machamp', 'Golem', None, None, None, None, None, None, 'Venusaur', 'Charizard', 'Blastoise', None, None, None, None, None, None, None, None, None, None, 'Dragonite', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    pokemon_tuple = tuple(zip(pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2))
    tierdict = {"A": [], "B": [], "C": [], "D": [], "E": [], "F": []}

    for pokemon, tier, firstEL, firstEvol, secondEL, secondEvol in pokemon_tuple:
        if tier != "S":
            tierdict[tier].append(pokemon)

    # Have default message text here because of future for loop iterating through multideck results
    msgtxt = "Hello Pokémon Trainer!"
    # Assign empty list to multiData (to be returned at end)
    multiData = []
    results = TagStats()
    if len(results) == 0:
        return
    if os.path.exists("_prestigelist.json"):
        prestigelist = json.load(open("_prestigelist.json"))
    else:
        prestigelist = []
    for item in results:
        result = item[1]
        sumivl = 0
        for id, ivl in result:
            adjustedivl = (100 * (ivl/100)**(0.5))
            sumivl += adjustedivl
        if len(result) == 0:
            continue
        Level = round((sumivl/len(result)+0.5), 2)

        pokemontier = ""
    
        if len(result) < thresholdsettings[0]:
            pokemontier = "F"
        elif len(result) < thresholdsettings[1]:
            pokemontier = "E"
        elif len(result) < thresholdsettings[2]:
            pokemontier = "D"
        elif len(result) < thresholdsettings[3]:
            pokemontier = "C"
        elif len(result) < thresholdsettings[4]:
            pokemontier = "B"
        else:
            pokemontier = "A"
        tagmon = ""
        already_assigned = False
        details = ()
        for thing in modifiedtagmon:
            if thing[1] == item[0]:
                tagmon = thing[0]
                already_assigned = True
                previouslevel = thing[2]
                if len(thing) == 4:
                    nickname = thing[3]
                else:
                    nickname = ""
        if tagmon == "":
            if pokemontier == "A":
                msgbox = QMessageBox()
                msgbox.setWindowTitle("Pokemanki")
                msgbox.setText("Choose a starter Pokémon for the %s tag" % item[0])
                msgbox.addButton("Bulbasaur", QMessageBox.AcceptRole)
                msgbox.addButton("Charmander", QMessageBox.AcceptRole)
                msgbox.addButton("Squirtle", QMessageBox.AcceptRole)
                msgbox.exec_()
                tagmon = msgbox.clickedButton().text()
            else:
                tiernumber = len(tierdict[pokemontier])
                tierlabel = tierdict[pokemontier]
                randno = random.randint(0, tiernumber - 1)
                tagmon = tierlabel[randno]
        details = ()
        for pokemon, tier, firstEL, firstEvol, secondEL, secondEvol in pokemon_tuple:
            if tagmon == pokemon or tagmon == firstEvol or tagmon == secondEvol:
                details = (pokemon, firstEL, firstEvol, secondEL, secondEvol)

        name = details[0]
        firstEL = details[1]
        firstEvol = details[2]
        secondEL = details[3]
        secondEvol = details[4]        

        if Level > 100 and item[0] not in prestigelist:
            Level = 100
        if item[0] in prestigelist:
            Level -= 50
        if Level < 5:
            name = "Egg"
        if firstEL is not None:
            firstEL = int(firstEL)
            if Level > firstEL:
                name = firstEvol
        if secondEL is not None:
            secondEL = int(secondEL)
            if Level > secondEL:
                name = secondEvol
        if name.startswith("Eevee"):
            name = "Eevee"
        if already_assigned == False and name != "Eevee" and name != "Egg":
            tagmonData = (name, item[0], Level)
            modifiedtagmon.append(tagmonData)
        elif already_assigned == False:
            tagmonData = (tagmon, item[0], Level)
            modifiedtagmon.append(tagmonData)
        if already_assigned == True:
            if name == "Egg":
                if Level == 2 and previouslevel < 2:
                    if nickname:
                        msgtxt += "\n%s needs more time to hatch." % nickname
                    else:
                        msgtxt += "\nYour egg needs more time to hatch."
                elif Level == 3 and previouslevel < 3:
                    if nickname:
                        msgtxt += "\n%s moves occasionally. It should hatch soon." % nickname
                    else:
                        msgtxt += "\nYour egg moves occasionally. It should hatch soon."
                elif Level == 4 and previouslevel < 4:
                    if nickname:
                        msgtxt += "\n%s is making sounds! It's about to hatch!" % nickname
                    else:
                        msgtxt += "\nYour egg is making sounds! It's about to hatch!"
            elif previouslevel < 5:
                if nickname:
                    msgtxt += ("\n%s has hatched! It's a %s!" % (nickname, tagmon))
                else:
                    msgtxt += ("\nYour egg has hatched! It's a %s!" % tagmon)
                previouslevel = Level
            if name != tagmon and name != "Egg" and int(previouslevel) < int(Level):
                if nickname:
                    msgtxt += ("\n%s has evolved into a %s (Level %s)! (+%s)" % (nickname, name, int(Level), (int(Level) - int(previouslevel))))
                else:
                    msgtxt += ("\nYour %s has evolved into a %s (Level %s)! (+%s)" % (tagmon, name, int(Level), (int(Level) - int(previouslevel))))
            elif int(previouslevel) < int(Level) and name != "Egg":
                if nickname:
                    msgtxt += ("\n%s is now level %s! (+%s)" % (nickname, int(Level), (int(Level) - int(previouslevel))))
                else:
                    msgtxt += ("\nYour %s is now level %s! (+%s)" % (name, int(Level), (int(Level) - int(previouslevel))))
        if already_assigned == False:
            if name == "Egg":
                msgtxt += "\nYou found an egg!"
            else:
                msgtxt += ("\nYou caught a %s (Level %s)" % (name, int(Level)))
        if already_assigned == True:
            for thing in tagmon:
                if thing == item[0]:
                    if name == "Eevee" or name =="Egg":
                        if nickname:
                            if (thing[0], thing[1], Level, nickname) in modifiedtagmon:
                                pass
                            else:
                                modifiedtagmon.append((thing[0], thing[1], Level, nickname))
                        else:
                            if (thing[0], thing[1], Level) in modifiedtagmon:
                                pass
                            else:
                                modifiedtagmon.append((thing[0], thing[1], Level))
                    else:
                        if nickname:
                            if (name, thing[1], Level, nickname) in modifiedtagmon:
                                pass
                            else:
                                modifiedtagmon.append((name, thing[1], Level, nickname))
                        else:
                            if (name, thing[1], Level) in modifiedtagmon:
                                pass
                            else:
                                modifiedtagmon.append((name, thing[1], Level))
        displayData = (name, item[0], Level)
        multiData.append(displayData)

    # After iterating through each deck, store data into pokemanki.json
    with open("_tagmon.json", "w") as f:
        json.dump(modifiedtagmon, f)
    # Only display message if changes
    if msgtxt != "Hello Pokémon Trainer!":
        msgbox2 = QMessageBox()
        msgbox2.setWindowTitle("Pokemanki")
        msgbox2.setText(msgtxt)
        msgbox2.exec_()
    # Return multiData
    return multiData
def TagStats():
    if os.path.exists("_tags.json"):
        savedtags = json.load(open("_tags.json"))
    else:
        savedtags = []
    resultlist = []
    for item in savedtags:
        result = mw.col.db.all("select c.id, c.ivl from cards c, notes n where c.nid = n.id and n.tags LIKE '% " + item + " %'")
        resultlist.append(result)
    results = list(zip(savedtags, resultlist))
    return results
