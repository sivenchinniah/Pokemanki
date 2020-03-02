from anki.utils import ids2str
import json
import os.path
import random
from aqt.qt import *
from aqt import mw
import csv
import inspect
import os

config = mw.addonManager.getConfig(__name__)
currentdirname = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

def cardIdsFromDeckIds(queryDb, deckIds):
    query = "select id from cards where did in {}".format(ids2str(deckIds))
    cardIds = [i[0] for i in queryDb.all(query)]
    return cardIds

def cardInterval(queryDb, cid):
    revLogIvl = queryDb.scalar(
                    "select ivl from revlog where cid = %s "
                    "order by id desc limit 1 offset 0" % cid)
    ctype = queryDb.scalar(
                "select type from cards where id = %s "
                "order by id desc limit 1 offset 0" % cid)

    # card interval is "New"
    if ctype == 0:
        ivl = 0
    elif revLogIvl is None:
        ivl = 0
    elif revLogIvl < 0:
        # Anki represents "learning" card review log intervals as negative minutes
        # So, convert to days
        ivl = revLogIvl * -1 / 60 / 1440
    else:
        ivl = revLogIvl

    return ivl

def loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2):
    with open(csv_fpath, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        for line in csv_reader:
            pokemon = line["pokemon"]
            tier = line["tier"]
            first_ev_lv = line["first_evolution_level"]
            if first_ev_lv.isnumeric():
                first_ev_lv = int(first_ev_lv)
            else:
                first_ev_lv = None
            first_ev = line["first_evolution"]
            if first_ev == "NA":
                first_ev = None
            second_ev_lv = line["second_evolution_level"]
            if second_ev_lv.isnumeric():
                second_ev_lv = int(second_ev_lv)
            else:
                second_ev_lv = None
            second_ev = line["second_evolution"]
            if second_ev == "NA":
                second_ev = None

            pokemonlist.append(pokemon)
            tiers.append(tier)
            evolutionLevel1.append(first_ev_lv)
            evolution1.append(first_ev)
            evolutionLevel2.append(second_ev_lv)
            evolution2.append(second_ev)
    return


def randomStarter():
    available_generations = [1]
    if config['gen2']:
        available_generations.append(2)
    if config['gen3']:
        available_generations.append(3)
    if config['gen4']:
        available_generations.append(4)
    if config['gen5']:
        available_generations.append(5)

    choice_generation = random.choice(available_generations)
    if choice_generation == 1:
        return ["Bulbasaur", "Charmander", "Squirtle"]
    elif choice_generation == 2:
        return ["Chikorita", "Cyndaquil", "Totodile"]
    elif choice_generation == 3:
        return ["Treecko", "Torchic", "Mudkip"]
    elif choice_generation == 4:
        return ["Turtwig", "Chimchar", "Piplup"]
    elif choice_generation == 5:
        return ["Snivy", "Tepig" "Oshawott"]

# Retrieve id and ivl for each card in a single deck
def DeckStats(*args, **kwargs):
    self = args[0]
    old = kwargs['_old']
    # result = self.col.db.all("""select id, ivl from cards where did in %s""" %
    #             ids2str(self.col.decks.active()))
    activeDeckIds = self.col.decks.active()
    cardIds = cardIdsFromDeckIds(self.col.db, activeDeckIds)

    result = []
    for cid in cardIds:
        ivl = cardInterval(self.col.db, cid)
        result.append((cid, ivl))

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
        # result = self.col.db.all("""select id, ivl from cards where did == %s""" % item)

        # cardIds = self.col.db.all("""select id from cards where did == %s""" % item)
        cardIds = cardIdsFromDeckIds(self.col.db, [item])

        result = []
        for cid in cardIds:
            ivl = cardInterval(self.col.db, cid)
            result.append((cid, ivl))

        resultlist.append(result)
    # Zip the deck ids with the results
    nograndchildresults = list(zip(nograndchildren, resultlist))

    return nograndchildresults

def FirstPokemon():
    global mediafolder
    deckmonlist = []
    deckmon = ""
    if os.path.exists("_pokemanki.json"):
        deckmonlist = json.load(open("_pokemanki.json"))
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
    decklist = sorted(decklist)
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
            # stats = mw.col.db.all("""select id, ivl from cards where did in (%s)""" % deck)
            
            # cardIds = mw.col.db.all("""select id from cards where did in (%s)""" % deck)
            cardIds = cardIdsFromDeckIds(mw.col.db, [deck])
            stats = []
            for cid in cardIds:
                for cid in cardIds:
                    ivl = cardInterval(mw.col.db, cid)
                    stats.append((cid, ivl))

            sumivl = 0
            for id, ivl in stats:
                adjustedivl = (100 * (ivl/100)**0.5)
                sumivl += adjustedivl
            if len(stats) != 0:
                Level = int(sumivl/len(stats)+0.5)
            else:
                Level = 0
            deckmondata = [(deckmon, deck, Level)]
            with open("_pokemanki.json", "w") as f:
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
        return

# Assign Pokemon and levels for single deck
def DeckPokemon(*args, **kwargs):
    self = args[0]
    old = kwargs['_old']

    FirstPokemon()
    # Get existing pokemon from pokemanki.json
    if os.path.exists("_pokemanki.json"):
        
        pokemontotal = json.load(open('_pokemanki.json'))
        # Sort list by deck id, reverse sorted to make sure that most recent additions come first
        sortedpokemontotal = list(reversed(pokemontotal))
        # Assign most recent Pokemon result for each deck id to modifiedpokemontotal
        modifiedpokemontotal = []
        for item in sortedpokemontotal:
            # Only assign if deck id not already in modifiedpokemontotal
            for thing in modifiedpokemontotal:
                if item[1] == thing[1]:
                    break
            else:
                if str(item[1]) in self.col.decks.allIds():
                    modifiedpokemontotal.append(item)
    # If no pokemanki.json, make empty pokemontotal and modifiedpokemontotal lists
    else:
        return

    # Download threshold settings if they exist, otherwise make from scratch
    if os.path.exists("_pokemankisettings.json"):
        thresholdsettings = json.load(open("_pokemankisettings.json"))
    else:
        thresholdsettings = [100, 250, 500, 750, 1000]

    # Lists containing Pokemon, tiers, first evolution level, first evolution, second evolution level, and second evolution

    pokemonlist = []
    tiers = []
    evolutionLevel1 =[]
    evolution1 = []
    evolutionLevel2 =[]
    evolution2 = []

    csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen1.csv")
    loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)

    if config['gen2']:
        csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen2.csv")
        loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)

        if config['gen4_evolutions']:
            csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen1_plus2_plus4.csv")
            loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)
            csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen2_plus4.csv")
            loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)
        else:
            csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen1_plus2_no4.csv")
            loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)
            csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen2_no4.csv")
            loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)
    else:
        if config['gen4_evolutions']:
            # a lot of gen 4 evolutions that affect gen 1 also include gen 2 evolutions
            # so let's just include gen 2 for these evolution lines
            csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen1_plus2_plus4.csv")
            loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)
        else:
            csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen1_no2_no4.csv")
            loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)

    if config['gen3']:
        csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen3.csv")
        loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)
    if config['gen4']:
        csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen4.csv")
        loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)
    if config['gen5']:
        csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen5.csv")
        loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)
        
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
    Level = round((sumivl/len(result)+0.5), 2)
    if Level < 1:
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
    if os.path.exists("_prestigelist.json"):
        prestigelist = json.load(open("_prestigelist.json"))
    else:
        prestigelist = []
    if os.path.exists("_everstonelist.json"):
        everstonelist = json.load(open("_everstonelist.json"))
    else:
        everstonelist = []
    if os.path.exists("_everstonepokemonlist.json"):
        everstonepokemonlist = json.load(open("_everstonepokemonlist.json"))
    else:
        everstonepokemonlist = []
    # Set max level to 100
    if Level > 100 and self.col.decks.active()[0] not in prestigelist:
        Level = 100.00
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
    if name.startswith("Slowpoke"):
        name = "Slowpoke"
    if name.startswith("Tyrogue"):
        name = "Tyrogue"

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
    with open("_pokemanki.json", "w") as f:
        json.dump(modifiedpokemontotal, f)

    # Generate message box
    msgtxt = "Hello Pokémon Trainer!"
    # Show changes in egg hatching, leveling up, and evolving
    if already_assigned == True:
        if name == "Egg":
            if int(Level) == 2 and previouslevel < 2:
                if nickname:
                    msgtxt += "\n%s needs more time to hatch." % nickname
                else:
                    msgtxt += "\nYour egg needs more time to hatch."
            elif int(Level) == 3 and previouslevel < 3:
                if nickname:
                    msgtxt += "\n%s moves occasionally. It should hatch soon." % nickname
                else:
                    msgtxt += "\nYour egg moves occasionally. It should hatch soon."
            elif int(Level) == 4 and previouslevel < 4:
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
        if name != deckmon and name != "Egg" and int(previouslevel) < int(Level):
            if nickname:
                msgtxt += ("\n%s has evolved into a %s (Level %s)! (+%s)" % (nickname, name, int(Level), (int(Level) - int(previouslevel))))
            else:
                msgtxt += ("\nYour %s has evolved into a %s (Level %s)! (+%s)" % (deckmon, name, int(Level), (int(Level) - int(previouslevel))))
        elif int(previouslevel) < int(Level) and name != "Egg" :
            if self.col.decks.active()[0] in prestigelist:
                if nickname:
                    msgtxt += ("\n%s is now level %s! (+%s)" % (nickname, int(Level) - 50, (int(Level) - int(previouslevel))))
                else:
                    msgtxt += ("\nYour %s is now level %s! (+%s)" % (name, int(Level) - 50, (int(Level) - int(previouslevel))))
            else:
                if nickname:
                    msgtxt += ("\n%s is now level %s! (+%s)" % (nickname, int(Level), (int(Level) - int(previouslevel))))
                else:
                    msgtxt += ("\nYour %s is now level %s! (+%s)" % (name, int(Level), (int(Level) - int(previouslevel))))
    # Show new Pokemon and eggs
    if already_assigned == False:
        if name == "Egg":
            msgtxt += "\nYou found an egg!"
        else:
            msgtxt += ("\nYou caught a %s (Level %s)" % (name, int(Level)))
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
    if os.path.exists("_pokemanki.json"):
        pokemontotal = json.load(open('_pokemanki.json'))
        sortedpokemontotal = list(reversed(pokemontotal))
        modifiedpokemontotal = []
        for item in sortedpokemontotal:
            for thing in modifiedpokemontotal:
                if item[1] == thing[1]:
                    break
            else:
                if str(item[1]) in self.col.decks.allIds():
                    modifiedpokemontotal.append(item)
    else:
        return
        
    if os.path.exists("_pokemankisettings.json"):
        thresholdsettings = json.load(open("_pokemankisettings.json"))
    else:
        thresholdsettings = [100, 250, 500, 750, 1000]

    pokemonlist = []
    tiers = []
    evolutionLevel1 =[]
    evolution1 = []
    evolutionLevel2 =[]
    evolution2 = []

    csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen1.csv")
    loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)
    if config['gen2']:
        csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen2.csv")
        loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)
        if config['gen4_evolutions']:
            csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen1_plus2_plus4.csv")
            loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)
            csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen2_plus4.csv")
            loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)
        else:
            csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen1_plus2_no4.csv")
            loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)
            csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen2_no4.csv")
            loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)
    else:
        if config['gen4_evolutions']:
            # a lot of gen 4 evolutions that affect gen 1 also include gen 2 evolutions
            # so let's just include gen 2 for these evolution lines
            csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen1_plus2_plus4.csv")
            loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)
        else:
            csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen1_no2_no4.csv")
            loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)
    if config['gen3']:
        csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen3.csv")
        loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)
    if config['gen4']:
        csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen4.csv")
        loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)
    if config['gen5']:
        csv_fpath = os.path.join(currentdirname, "pokemon_evolutions", "pokemon_gen5.csv")
        loadPokemonGenerations(csv_fpath, pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2)

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
    if os.path.exists("_prestigelist.json"):
        prestigelist = json.load(open("_prestigelist.json"))
    else:
        prestigelist = []
    if os.path.exists("_everstonelist.json"):
        everstonelist = json.load(open("_everstonelist.json"))
    else:
        everstonelist = []
    if os.path.exists("_everstonepokemonlist.json"):
        everstonepokemonlist = json.load(open("_everstonepokemonlist.json"))
    else:
        everstonepokemonlist = []
    # Do the following (basically DeckPokemon) for each deck in results
    for item in results:
        result = item[1]
        sumivl = 0
        for id, ivl in result:
            adjustedivl = (100 * (ivl/100)**(0.5))
            sumivl += adjustedivl
        if len(result) == 0:
            continue
        Level = round((sumivl/len(result)+0.5), 2)
        if Level < 1:
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

                starters = randomStarter()
                for starter in starters:
                    msgbox.addButton(starter, QMessageBox.AcceptRole)
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
        print(pokemon_tuple)

        name = details[0]
        firstEL = details[1]
        firstEvol = details[2]
        secondEL = details[3]
        secondEvol = details[4]        

        if Level > 100 and item[0] not in prestigelist:
            Level = 100
        if Level < 5:
            name = "Egg"
        if item[0] not in everstonelist:
            if firstEL is not None:
                firstEL = int(firstEL)
                if Level > firstEL:
                    name = firstEvol
            if secondEL is not None:
                secondEL = int(secondEL)
                if Level > secondEL:
                    name = secondEvol
        else:
            idx = everstonelist.index(item[0])
            name = everstonepokemonlist[idx]
        if name.startswith("Eevee"):
            name = "Eevee"
        
        if already_assigned == False and name != "Eevee" and name != "Egg":
            deckmonData = [name, item[0], Level]
            modifiedpokemontotal.append(deckmonData)
        elif already_assigned == False:
            deckmonData = [deckmon, item[0], Level]
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
            if name != deckmon and name != "Egg" and int(previouslevel) < int(Level):
                if nickname:
                    msgtxt += ("\n%s has evolved into a %s (Level %s)! (+%s)" % (nickname, name, int(Level), (int(Level) - int(previouslevel))))
                else:
                    msgtxt += ("\nYour %s has evolved into a %s (Level %s)! (+%s)" % (deckmon, name, int(Level), (int(Level) - int(previouslevel))))
            elif int(previouslevel) < int(Level) and name != "Egg":
                if item[0] in prestigelist:
                    if nickname:
                        msgtxt += ("\n%s is now level %s! (+%s)" % (nickname, int(Level) - 50, (int(Level) - int(previouslevel))))
                    else:
                        msgtxt += ("\nYour %s is now level %s! (+%s)" % (name, int(Level) - 50, (int(Level) - int(previouslevel))))
                else:
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
            for thing in pokemontotal:
                if thing[1] == item[0]:
                    if name == "Eevee" or name =="Egg":
                        if nickname:
                            if (thing[0], thing[1], Level, nickname) in modifiedpokemontotal:
                                pass
                            else:
                                modifiedpokemontotal.append([thing[0], thing[1], Level, nickname])
                        else:
                            if (thing[0], thing[1], Level) in modifiedpokemontotal:
                                pass
                            else:
                                modifiedpokemontotal.append([thing[0], thing[1], Level])
                    else:
                        if nickname:
                            if (name, thing[1], Level, nickname) in modifiedpokemontotal:
                                pass
                            else:
                                modifiedpokemontotal.append([name, thing[1], Level, nickname])
                        else:
                            if (name, thing[1], Level) in modifiedpokemontotal:
                                pass
                            else:
                                modifiedpokemontotal.append([name, thing[1], Level])
        if nickname:
            displayData = (name, item[0], Level, nickname)
        else:
            displayData = (name, item[0], Level)
        multiData.append(displayData)

    # After iterating through each deck, store data into pokemanki.json
    with open("_pokemanki.json", "w") as f:
        json.dump(modifiedpokemontotal, f)
    # Only display message if changes
    if msgtxt != "Hello Pokémon Trainer!":
        msgbox2 = QMessageBox()
        msgbox2.setWindowTitle("Pokemanki")
        msgbox2.setText(msgtxt)
        msgbox2.exec_()
    # Return multiData
    return multiData
