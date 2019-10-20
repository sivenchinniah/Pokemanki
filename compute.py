from anki.utils import ids2str
import json
import os.path
import random
from aqt.qt import *
from aqt import mw

# Retrieve id and ivl for each card in a single deck
def DeckStats(*args, **kwargs):
    self = args[0]
    old = kwargs['_old']
    result = self.col.db.all("""select id, ivl from cards where did in %s""" %
                ids2str(self.col.decks.active()))
    return result

# Retrieve id and ivl for each subdeck that does not have subdecks itself
def MultiStats(*args, **kwargs):
    self = args[0]
    old = kwargs['_old']
    # Get list of subdecks
    if self.wholeCollection:
        # Get results for all subdecks in collection
        alldecks = self.col.decks.allIds()
        # Determine which subdecks do not have their own subdecks
        nograndchildren = []
        for item in alldecks:
            if len(self.col.decks.children(int(item))) == 0 and item != "1":
                nograndchildren.append(int(item))
    else:
        # Get results only for all subdecks of selected deck
        children = self.col.decks.children(self.col.decks.active()[0])
        childlist = []
        for item in children:
            childlist.append(item[1])
        # Determine which subdecks do not have their own subdecks 
        nograndchildren = []
        for item in childlist:
            if len(self.col.decks.children(item)) == 0:
                nograndchildren.append(item)
    resultlist = []
    # Find results for each card in these decks
    for item in nograndchildren:
        result = self.col.db.all("""select id, ivl from cards where did == %s""" % item)
        resultlist.append(result)
    # Zip the deck ids with the results
    nograndchildresults = list(zip(nograndchildren, resultlist))

    return nograndchildresults

def FirstPokemon():
    global mediafolder
    deckmonlist = []
    deckmon = ""
    if os.path.exists("pokemanki.json"):
        deckmonlist = json.load(open("pokemanki.json"))
    if deckmonlist:
        return
    alldecks = mw.col.decks.allIds()
    # Determine which subdecks do not have their own subdecks
    nograndchildren = []
    for item in alldecks:
        if len(mw.col.decks.children(int(item))) == 0 and item != "1":
            nograndchildren.append(int(item))
    decklist = []
    for item in nograndchildren:
        decklist.append(mw.col.decks.name(item))
    window = QWidget()
    inp, ok = QInputDialog.getItem(window, "Pokemanki", "Choose a deck for your starter Pokémon", decklist, 0, False)
    if ok and inp:
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Pokemanki")
        msgbox.setText("Choose a starter Pokémon for %s" % inp)
        msgbox.addButton("Bulbasaur", QMessageBox.AcceptRole)
        msgbox.addButton("Charmander", QMessageBox.AcceptRole)
        msgbox.addButton("Squirtle", QMessageBox.AcceptRole)
        msgbox.exec_()
        deckmon = msgbox.clickedButton().text()
        if deckmon:
            deck = mw.col.decks.byName(inp)['id']
            stats = mw.col.db.all("""select id, ivl from cards where did in (%s)""" % deck)
            sumivl = 0
            for id, ivl in stats:
                adjustedivl = (100 * (ivl/100)**0.5)
                sumivl += adjustedivl
            Level = int(sumivl/len(stats)+0.5)
            deckmondata = [(deckmon, deck, Level)]
            with open("pokemanki.json", "w") as f:
                json.dump(deckmondata, f)
            firstpokemon = QMessageBox()
            firstpokemon.setWindowTitle("Pokemanki")
            if Level < 5:
                firstpokemon.setText("You've found a %s egg" % deckmon)
            else:
                firstpokemon.setText("You've caught a %s!" % deckmon)
            firstpokemon.exec_()
        else:
            FirstPokemon()
    else:
        FirstPokemon()

# Assign Pokemon and levels for single deck
def DeckPokemon(*args, **kwargs):
    self = args[0]
    old = kwargs['_old']

    FirstPokemon()
    # Get existing pokemon from pokemanki.json
    if os.path.exists("pokemanki.json"):
        
        pokemontotal = json.load(open('pokemanki.json'))
        # Sort list by deck id, reverse sorted to make sure that most recent additions come first
        sortedpokemontotal = sorted(list(reversed(pokemontotal)), key = lambda x: x[1])
        # Assign most recent Pokemon result for each deck id to modifiedpokemontotal
        modifiedpokemontotal = []
        for item in sortedpokemontotal:
            # Only assign if deck id not already in modifiedpokemontotal
            for thing in modifiedpokemontotal:
                if item[1] == thing[1]:
                    break
            else:
                 modifiedpokemontotal.append(item)
    # If no pokemanki.json, make empty pokemontotal and modifiedpokemontotal lists
    else:
        pokemontotal = []
        modifiedpokemontotal = []

    # Download threshold settings if they exist, otherwise make from scratch
    if os.path.exists("pokemankisettings.json"):
        thresholdsettings = json.load(open("pokemankisettings.json"))
    else:
        thresholdsettings = [100, 250, 500, 750, 1000]

    # Lists containing Pokemon, tiers, first evolution level, first evolution, second evolution level, and second evolution
    pokemonlist = ['Caterpie', 'Weedle', 'Pidgey', 'Rattata', 'Zubat', 'Spearow', 'Oddish', 'Paras', 'Venonat', 'Meowth', 'Bellsprout', 'Drowzee', 'Krabby', 'Horsea', 'Magikarp', 'Ekans', 'Nidoran F', 'Nidoran M', 'Clefairy', 'Jigglypuff', 'Diglett', 'Poliwag', 'Tentacool', 'Slowpoke', 'Magnemite', 'Doduo', 'Shellder', 'Gastly', 'Exeggcute', 'Cubone', 'Goldeen', 'Staryu', 'Eevee1', 'Eevee2', 'Eevee3', 'Sandshrew', 'Vulpix', 'Psyduck', 'Mankey', 'Growlithe', 'Abra', 'Machop', 'Geodude', 'Ponyta', 'Seel', 'Onix', 'Koffing', 'Scyther', 'Ditto', 'Bulbasaur', 'Charmander', 'Squirtle', 'Pikachu', 'Grimer', 'Lickitung', 'Rhyhorn', 'Tangela', 'Electabuzz', 'Magmar', 'Pinsir', 'Omanyte', 'Kabuto', 'Dratini', "Farfetch'd", 'Voltorb', 'Hitmonlee', 'Hitmonchan', 'Chansey', 'Kangaskhan', 'Mr. Mime', 'Jynx', 'Tauros', 'Lapras', 'Porygon', 'Aerodactyl', 'Snorlax', 'Moltres', 'Zapdos', 'Articuno', 'Mewtwo', 'Mew']
    tiers = ['D', 'D', 'D', 'E', 'E', 'E', 'D', 'E', 'E', 'D', 'D', 'D', 'E', 'E', 'B', 'D', 'D', 'D', 'E', 'E', 'E', 'D', 'E', 'E', 'D', 'E', 'D', 'B', 'C', 'D', 'E', 'D', 'B', 'B', 'B', 'E', 'D', 'E', 'E', 'B', 'B', 'B', 'B', 'C', 'E', 'D', 'E', 'C', 'F', 'A', 'A', 'A', 'D', 'E', 'F', 'B', 'F', 'C', 'C', 'C', 'D', 'D', 'B', 'F', 'E', 'C', 'C', 'F', 'C', 'F', 'F', 'C', 'C', 'F', 'C', 'C', 'S', 'S', 'S', 'S', 'S']
    evolutionLevel1 = [7, 7, 18, 20, 22, 20, 21, 24, 31, 28, 21, 26, 28, 32, 40, 22, 16, 16, 32, 32, 26, 25, 30, 37, 30, 31, 32, 25, 36, 28, 33, 25, 36, 36, 36, 22, 32, 33, 28, 36, 16, 28, 25, 40, 34, None, 35, None, None, 16, 16, 16, 32, 38, None, 42, None, None, None, None, 40, 40, 30, None, 30, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    evolution1 = ['Metapod', 'Kakuna', 'Pidgeotto', 'Raticate', 'Golbat', 'Fearow', 'Gloom', 'Parasect', 'Venomoth', 'Persian', 'Weepinbell', 'Hypno', 'Kingler', 'Seadra', 'Gyarados', 'Arbok', 'Nidorina', 'Nidorino', 'Clefable', 'Wigglytuff', 'Dugtrio', 'Poliwhirl', 'Tentacruel', 'Slowbro', 'Magneton', 'Dodrio', 'Cloyster', 'Haunter', 'Exeggutor', 'Marowak', 'Seaking', 'Starmie', 'Vaporeon', 'Jolteon', 'Flareon', 'Sandslash', 'Ninetales', 'Golduck', 'Primeape', 'Arcanine', 'Kadabra', 'Machoke', 'Graveler', 'Rapidash', 'Dewgong', None, 'Weezing', None, None, 'Ivysaur', 'Charmeleon', 'Wartortle', 'Raichu', 'Muk', None, 'Rhydon', None, None, None, None, 'Omastar', 'Kabutops', 'Dragonair', None, 'Electrode', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    evolutionLevel2 = [10, 10, 36, None, None, None, 36, None, None, None, 36, None, None, None, None, None, 32, 32, None, None, None, 36, None, None, None, None, None, 40, None, None, None, None, None, None, None, None, None, None, None, None, 40, 40, 40, None, None, None, None, None, None, 32, 36, 36, None, None, None, None, None, None, None, None, None, None, 55, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    evolution2 = ['Butterfree', 'Beedrill', 'Pidgeot', None, None, None, 'Vileplume', None, None, None, 'Victreebel', None, None, None, None, None, 'Nidoqueen', 'Nidoking', None, None, None, 'Poliwrath', None, None, None, None, None, 'Gengar', None, None, None, None, None, None, None, None, None, None, None, None, 'Alakazam', 'Machamp', 'Golem', None, None, None, None, None, None, 'Venusaur', 'Charizard', 'Blastoise', None, None, None, None, None, None, None, None, None, None, 'Dragonite', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    # Zip lists into list of tuples
    pokemon_tuple = tuple(zip(pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2))

    # Make dictionary based on tiers of Pokemon
    tierdict = {"A": [], "B": [], "C": [], "D": [], "E": [], "F": []}
    for pokemon, tier, firstEL, firstEvol, secondEL, secondEvol in pokemon_tuple:
        if tier != "S":
            tierdict[tier].append(pokemon)

    # Get results from DeckStats
    result = DeckStats(*args, **kwargs)
    # If no results, return
    if len(result) == 0:
        return
    # Determine level of Pokemon (if zero, do not assign Pokemon)
    sumivl = 0
    for id, ivl in result:
        adjustedivl = (100 * (ivl/100)**(0.5))
        sumivl += adjustedivl
    Level = int(sumivl/len(result)+0.5)
    if Level == 0:
        return

    # Determine tier of Pokemon based on deck size
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

    # Assign "Deckmon"
    deckmon = ""
    already_assigned = False
    details = ()
    nickname = ""
    # Assign Deckmon from modifiedpokemontotal if already assigned
    for item in modifiedpokemontotal:
        if item[1] == self.col.decks.active()[0]:
            deckmon = item[0]
            already_assigned = True
            previouslevel = item[2]
            if len(item) == 4:
                nickname = item[3]
    # Assign Deckmon if not already assigned
    if deckmon == "":
        # If starter Pokemon, allow choice
        if pokemontier == "A":
            msgbox = QMessageBox()
            msgbox.setWindowTitle("Pokemanki")
            msgbox.setText("Choose a starter Pokémon for the %s deck" % self.col.decks.name(self.col.decks.active()[0]))
            msgbox.addButton("Bulbasaur", QMessageBox.AcceptRole)
            msgbox.addButton("Charmander", QMessageBox.AcceptRole)
            msgbox.addButton("Squirtle", QMessageBox.AcceptRole)
            msgbox.exec_()
            deckmon = msgbox.clickedButton().text()
        # Else, randomize based on tier
        else:
            tiernumber = len(tierdict[pokemontier])
            tierlabel = tierdict[pokemontier]
            randno = random.randint(0, tiernumber - 1)
            deckmon = tierlabel[randno]
    # Get details for Deckmon from pokemon_tuple list
    details = ()
    for pokemon, tier, firstEL, firstEvol, secondEL, secondEvol in pokemon_tuple:
        if deckmon == pokemon or deckmon == firstEvol or deckmon == secondEvol:
            details = (pokemon, firstEL, firstEvol, secondEL, secondEvol)

    # Assign details for name, evolutions, and evolution levels
    name = details[0]
    firstEL = details[1]
    firstEvol = details[2]
    secondEL = details[3]
    secondEvol = details[4]        

    # Set max level to 100
    if Level > 100:
        Level = 100
    # Give egg if level < 5
    if Level < 5:
        name = "Egg"
    # Reassign name if Pokemon has evolved
    if firstEL is not None:
        firstEL = int(firstEL)
        if Level > firstEL:
            name = firstEvol
    if secondEL is not None:
        secondEL = int(secondEL)
        if Level > secondEL:
            name = secondEvol
    # Make display name Eevee if one of the Eevees
    if name.startswith("Eevee"):
        name = "Eevee"

    # Assign new name to modifiedpokemontotal if not already assigned (making sure to assign Deckmon original name if Eevee or Egg)
    if already_assigned == False and name != "Eevee" and name != "Egg":
        deckmonData = (name, self.col.decks.active()[0], Level)
        modifiedpokemontotal.append(deckmonData)
    elif already_assigned == False:
        deckmonData = (deckmon, self.col.decks.active()[0], Level)
        modifiedpokemontotal.append(deckmonData)
    # If already assigned, assign new level/name to modifiedpokemontotal if new level/name
    if already_assigned == True:
        for item in pokemontotal:
            if item[1] == self.col.decks.active()[0]:
                if name == "Eevee" or name == "Egg":
                    if nickname:
                        if (item[0], item[1], Level, nickname) in modifiedpokemontotal:
                            pass
                        else:
                            modifiedpokemontotal.append((item[0], item[1], Level, nickname))
                    else:
                        if (item[0], item[1], Level) in modifiedpokemontotal:
                            pass
                        else:
                            modifiedpokemontotal.append((item[0], item[1], Level))
                else:
                    if nickname:
                        if (name, item[1], Level, nickname) in modifiedpokemontotal:
                            pass
                        else:
                            modifiedpokemontotal.append((name, item[1], Level, nickname))
                    else:
                        if (name, item[1], Level) in modifiedpokemontotal:
                            pass
                        else:
                            modifiedpokemontotal.append((name, item[1], Level))
    # Save new Pokemon data
    with open("pokemanki.json", "w") as f:
        json.dump(modifiedpokemontotal, f)

    # Generate message box
    msgtxt = "Hello Pokémon Trainer!"
    # Show changes in egg hatching, leveling up, and evolving
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
                msgtxt += ("\n%s has hatched! It's a %s!" % (nickname, deckmon))
            else:
                msgtxt += ("\nYour egg has hatched! It's a %s!" % deckmon)
            previouslevel = Level
        if name != deckmon and name != "Egg" and previouslevel < Level:
            if nickname:
                msgtxt += ("\n%s has evolved into a %s (Level %s)! (+%s)" % (nickname, name, Level, (Level - previouslevel)))
            else:
                msgtxt += ("\nYour %s has evolved into a %s (Level %s)! (+%s)" % (deckmon, name, Level, (Level - previouslevel)))
        elif previouslevel < Level and name != "Egg" :
            if nickname:
                msgtxt += ("\n%s is now level %s! (+%s)" % (nickname, Level, (Level - previouslevel)))
            else:
                msgtxt += ("\nYour %s is now level %s! (+%s)" % (name, Level, (Level - previouslevel)))
    # Show new Pokemon and eggs
    if already_assigned == False:
        if name == "Egg":
            msgtxt += "\nYou found an egg!"
        else:
            msgtxt += ("\nYou caught a %s (Level %s)" % (name, Level))
    # Only show message box if there has been a change
    if msgtxt != "Hello Pokémon Trainer!":
        msgbox2 = QMessageBox()
        msgbox2.setWindowTitle("Pokemanki")
        msgbox2.setText(msgtxt)
        msgbox2.exec_()

    # Set displayData for pokemonDisplay function in display.py
    if nickname:
        displayData = (name, self.col.decks.active()[0], Level, nickname)
    else:
        displayData = (name, self.col.decks.active()[0], Level)
    # Return displayData
    return displayData

def MultiPokemon(*args, **kwargs):
    self = args[0]
    old = kwargs['_old']
    
    # Same deal as above
    FirstPokemon()
    if os.path.exists("pokemanki.json"):
        pokemontotal = json.load(open('pokemanki.json'))
        sortedpokemontotal = sorted(list(reversed(pokemontotal)), key = lambda x: x[1])
        modifiedpokemontotal = []
        for item in sortedpokemontotal:
            for thing in modifiedpokemontotal:
                if item[1] == thing[1]:
                    break
            else:
                 modifiedpokemontotal.append(item)
    else:
        pokemontotal = []
        modifiedpokemontotal = []
        
    if os.path.exists("pokemankisettings.json"):
        thresholdsettings = json.load(open("pokemankisettings.json"))
    else:
        thresholdsettings = [100, 250, 500, 750, 1000]
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
    # Get multideck results
    if self.wholeCollection:
        results = MultiStats(*args, **kwargs)
    else:
        results = MultiStats(*args, **kwargs)
    # If no results, return
    if len(results) == 0:
        return
    # Do the following (basically DeckPokemon) for each deck in results
    for item in results:
        result = item[1]
        sumivl = 0
        for id, ivl in result:
            adjustedivl = (100 * (ivl/100)**(0.5))
            sumivl += adjustedivl
        if len(result) == 0:
            continue
        Level = int(sumivl/len(result)+0.5)
        if Level == 0:
            continue

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
        deckmon = ""
        already_assigned = False
        details = ()
        nickname = ""
        for thing in modifiedpokemontotal:
            if thing[1] == item[0]:
                deckmon = thing[0]
                already_assigned = True
                previouslevel = thing[2]
                if len(thing) == 4:
                    nickname = thing[3]
        if deckmon == "":
            if pokemontier == "A":
                msgbox = QMessageBox()
                msgbox.setWindowTitle("Pokemanki")
                msgbox.setText("Choose a starter Pokémon for the %s deck" % self.col.decks.name(item[0]))
                msgbox.addButton("Bulbasaur", QMessageBox.AcceptRole)
                msgbox.addButton("Charmander", QMessageBox.AcceptRole)
                msgbox.addButton("Squirtle", QMessageBox.AcceptRole)
                msgbox.exec_()
                deckmon = msgbox.clickedButton().text()
            else:
                tiernumber = len(tierdict[pokemontier])
                tierlabel = tierdict[pokemontier]
                randno = random.randint(0, tiernumber - 1)
                deckmon = tierlabel[randno]
        details = ()
        for pokemon, tier, firstEL, firstEvol, secondEL, secondEvol in pokemon_tuple:
            if deckmon == pokemon or deckmon == firstEvol or deckmon == secondEvol:
                details = (pokemon, firstEL, firstEvol, secondEL, secondEvol)

        name = details[0]
        firstEL = details[1]
        firstEvol = details[2]
        secondEL = details[3]
        secondEvol = details[4]        

        if Level > 100:
            level = 100
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
            deckmonData = (name, item[0], Level)
            modifiedpokemontotal.append(deckmonData)
        elif already_assigned == False:
            deckmonData = (deckmon, item[0], Level)
            modifiedpokemontotal.append(deckmonData)
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
                    msgtxt += ("\n%s has hatched! It's a %s!" % (nickname, deckmon))
                else:
                    msgtxt += ("\nYour egg has hatched! It's a %s!" % deckmon)
                previouslevel = Level
            if name != deckmon and name != "Egg" and previouslevel < Level:
                if nickname:
                    msgtxt += ("\n%s has evolved into a %s (Level %s)! (+%s)" % (nickname, name, Level, (Level - previouslevel)))
                else:
                    msgtxt += ("\nYour %s has evolved into a %s (Level %s)! (+%s)" % (deckmon, name, Level, (Level - previouslevel)))
            elif previouslevel < Level and name != "Egg":
                if nickname:
                    msgtxt += ("\n%s is now level %s! (+%s)" % (nickname, Level, (Level - previouslevel)))
                else:
                    msgtxt += ("\nYour %s is now level %s! (+%s)" % (name, Level, (Level - previouslevel)))
        if already_assigned == False:
            if name == "Egg":
                msgtxt += "\nYou found an egg!"
            else:
                msgtxt += ("\nYou caught a %s (Level %s)" % (name, Level))
        if already_assigned == True:
            for thing in pokemontotal:
                if thing[1] == item[0]:
                    if name == "Eevee" or name =="Egg":
                        if nickname:
                            if (thing[0], thing[1], Level, nickname) in modifiedpokemontotal:
                                pass
                            else:
                                modifiedpokemontotal.append((thing[0], thing[1], Level, nickname))
                        else:
                            if (thing[0], thing[1], Level) in modifiedpokemontotal:
                                pass
                            else:
                                modifiedpokemontotal.append((thing[0], thing[1], Level))
                    else:
                        if nickname:
                            if (name, thing[1], Level, nickname) in modifiedpokemontotal:
                                pass
                            else:
                                modifiedpokemontotal.append((name, thing[1], Level, nickname))
                        else:
                            if (name, thing[1], Level) in modifiedpokemontotal:
                                pass
                            else:
                                modifiedpokemontotal.append((name, thing[1], Level))
        if nickname:
            displayData = (name, item[0], Level, nickname)
        else:
            displayData = (name, item[0], Level)
        multiData.append(displayData)

    # After iterating through each deck, store data into pokemanki.json
    with open("pokemanki.json", "w") as f:
        json.dump(modifiedpokemontotal, f)
    # Only display message if changes
    if msgtxt != "Hello Pokémon Trainer!":
        msgbox2 = QMessageBox()
        msgbox2.setWindowTitle("Pokemanki")
        msgbox2.setText(msgtxt)
        msgbox2.exec_()
    # Return multiData
    return multiData
