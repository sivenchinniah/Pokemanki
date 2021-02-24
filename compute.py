
import random
import csv

from aqt import mw
from aqt.qt import *

from .utils import *
from .stats import MultiStats, cardInterval, cardIdsFromDeckIds


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


def load_pokemon_gen_all(pokemonlist, tiers, evolutionLevel1, evolution1, evolutionLevel2, evolution2):
    def load_pokemon_gen(csv_name):
        csv_fpath = currentdirname / "pokemon_evolutions" / csv_name
        loadPokemonGenerations(csv_fpath, pokemonlist, tiers,
                               evolutionLevel1, evolution1, evolutionLevel2, evolution2)

    load_pokemon_gen("pokemon_gen1.csv")
    if config['gen2']:
        load_pokemon_gen("pokemon_gen2.csv")
        if config['gen4_evolutions']:
            load_pokemon_gen("pokemon_gen1_plus2_plus4.csv")
            load_pokemon_gen("pokemon_gen2_plus4.csv")
        else:
            load_pokemon_gen("pokemon_gen1_plus2_no4.csv")
            load_pokemon_gen("pokemon_gen2_no4.csv")
    else:
        if config['gen4_evolutions']:
            # a lot of gen 4 evolutions that affect gen 1 also include gen 2 evolutions
            # so let's just include gen 2 for these evolution lines
            load_pokemon_gen("pokemon_gen1_plus2_plus4.csv")
        else:
            load_pokemon_gen("pokemon_gen1_no2_no4.csv")
    if config['gen3']:
        load_pokemon_gen("pokemon_gen3.csv")
    if config['gen4']:
        load_pokemon_gen("pokemon_gen4.csv")
    if config['gen5']:
        load_pokemon_gen("pokemon_gen5.csv")


def alertMsgText(mon: str, id, name: str, level: int, previousLevel: int, nickname: str, already_assigned: bool):
    prestigelist = get_json("_prestigelist.json", [])
    msgtxt = ""
    if already_assigned == True:
        if name == "Egg":
            if level == 2 and previousLevel < 2:
                if nickname:
                    msgtxt = "%s needs more time to hatch." % nickname
                else:
                    msgtxt = "Your egg needs more time to hatch."
            elif level == 3 and previousLevel < 3:
                if nickname:
                    msgtxt = "%s moves occasionally. It should hatch soon." % nickname
                else:
                    msgtxt = "Your egg moves occasionally. It should hatch soon."
            elif level == 4 and previousLevel < 4:
                if nickname:
                    msgtxt = "%s is making sounds! It's about to hatch!" % nickname
                else:
                    msgtxt = "Your egg is making sounds! It's about to hatch!"
        elif previousLevel < 5:
            if nickname:
                msgtxt = ("%s has hatched! It's a %s!" %
                          (nickname, mon))
            else:
                msgtxt = ("Your egg has hatched! It's a %s!" % mon)
            previousLevel = level
        if name != mon and name != "Egg" and previousLevel < level:
            if nickname:
                msgtxt = ("%s has evolved into a %s (Level %s)! (+%s)" %
                          (nickname, name, level, (level - previousLevel)))
            else:
                msgtxt = ("Your %s has evolved into a %s (Level %s)! (+%s)" %
                          (mon, name, level, (level - previousLevel)))
        elif previousLevel < level and name != "Egg":
            displayName = name
            if nickname:
                displayName = nickname
            if id in prestigelist:
                msgtxt = "%s is now level %s! (+%s)" % (
                    displayName, level - 50, level - previousLevel)
            else:
                msgtxt = ("Your %s is now level %s! (+%s)" %
                          (displayName, level, (level - previousLevel)))
    else:
        if name == "Egg":
            msgtxt = "You found an egg!"
        else:
            msgtxt = "You caught a %s (Level %s)" % (name, level)
    if msgtxt:
        return "\n" + msgtxt
    else:
        return ""


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


def FirstPokemon():
    deckmonlist = []
    deckmon = ""
    deckmonlist = get_json("_pokemanki.json")
    if deckmonlist:
        return
    alldecks = mw.col.decks.allIds()
    # Determine which subdecks do not have their own subdecks
    nograndchildren = []
    for item in alldecks:
        if len(mw.col.decks.children(int(item))) == 0:
            nograndchildren.append(int(item))
    decklist = []
    for item in nograndchildren:
        decklist.append(mw.col.decks.name(item))
    decklist = sorted(decklist)
    window = QWidget()
    inp, ok = QInputDialog.getItem(
        window, "Pokemanki", "Choose a deck for your starter Pokémon", decklist, 0, False)
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
            write_json("_pokemanki.json", deckmondata)
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


def getPokemonIndex(pokemon_name, pokemons1, pokemons2, pokemons3):
    "Returns a string of integer because 0 is a falsey value, while '0' is truthy"
    def getIndex(pokemons):
        try:
            return str(pokemons.index(pokemon_name))
        except:
            return None
    return getIndex(pokemons1) or getIndex(pokemons2) or getIndex(pokemons3)


def MultiPokemon(wholeCollection):
    "Returns array of DeckPokemon"

    FirstPokemon()
    pokemontotal = get_json("_pokemanki.json", None)
    if not pokemontotal:
        return  # If no pokemanki.json, make empty pokemontotal and modifiedpokemontotal lists

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
            if str(item[1]) in mw.col.decks.allIds():
                modifiedpokemontotal.append(item)
    # Download threshold settings if they exist, otherwise make from scratch
    thresholdsettings = get_json("_pokemankisettings.json", [
                                 100, 250, 500, 750, 1000])
    pokemonlist = []
    tiers = []
    evolutionLevel1 = []
    evolution1 = []
    evolutionLevel2 = []
    evolution2 = []

    load_pokemon_gen_all(pokemonlist, tiers, evolutionLevel1,
                         evolution1, evolutionLevel2, evolution2)

    tierdict = {"A": [], "B": [], "C": [], "D": [], "E": [], "F": []}
    for i, tier in enumerate(tiers):
        if tier != "S":
            tierdict[tier].append(pokemonlist[i])

    # Have default message text here because of future for loop iterating through multideck results
    msgtxt = "Hello Pokémon Trainer!"
    # Assign empty list to multiData (to be returned at end)
    multiData = []
    # Get multideck results
    results = MultiStats(wholeCollection)
    # If no results, return
    if len(results) == 0:
        return
    prestigelist = get_json("_prestigelist.json", [])
    everstonelist = get_json("_everstonelist.json", [])
    everstonepokemonlist = get_json("_everstonepokemonlist.json", [])
    # Determine level of Pokemon (if zero, do not assign Pokemon)
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
        previouslevel = 0
        # Assign Deckmon from modifiedpokemontotal if already assigned
        for thing in modifiedpokemontotal:
            if thing[1] == item[0]:
                deckmon = thing[0]
                already_assigned = True
                previouslevel = thing[2]
                if len(thing) == 4:
                    nickname = thing[3]
        # Assign Deckmon if not already assigned or not valid
        if deckmon == "" or not getPokemonIndex(deckmon, pokemonlist, evolution1, evolution2):
            # If starter Pokemon, allow choice
            if pokemontier == "A":
                msgbox = QMessageBox()
                msgbox.setWindowTitle("Pokemanki")
                msgbox.setText("Choose a starter Pokémon for the %s deck" %
                               mw.col.decks.name(item[0]))

                starters = randomStarter()
                for starter in starters:
                    msgbox.addButton(starter, QMessageBox.AcceptRole)
                msgbox.exec_()
                deckmon = msgbox.clickedButton().text()
            # Else, randomize based on tier
            else:
                tiernumber = len(tierdict[pokemontier])
                tierlabel = tierdict[pokemontier]
                randno = random.randint(0, tiernumber - 1)
                deckmon = tierlabel[randno]

        idx = getPokemonIndex(deckmon, pokemonlist, evolution1, evolution2)
        idx = int(idx)
        # Assign details for name, evolutions, and evolution levels
        name = pokemonlist[idx]
        firstEL = evolutionLevel1[idx]
        firstEvol = evolution1[idx]
        secondEL = evolutionLevel2[idx]
        secondEvol = evolution2[idx]
        # Set max level to 100
        if Level > 100 and item[0] not in prestigelist:
            Level = 100
        # Give egg if level < 5
        if Level < 5:
            name = "Egg"
        if item[0] not in everstonelist:
            # Reassign name if Pokemon has evolved
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
            try:  # temporary patch
                name = everstonepokemonlist[idx]
                assert type(name) is str
            except Exception as e:
                print("ERROR(Pokemanki): while getting everstone list")
                print("Deleting entry from everstonelist")
                print(e)
                everstonelist.pop(idx)
                everstonepokemonlist.pop(idx)
        # Make display name Eevee if one of the Eevees
        if name.startswith("Eevee"):
            name = "Eevee"
        if name.startswith("Slowpoke"):
            name = "Slowpoke"
        if name.startswith("Tyrogue"):
            name = "Tyrogue"
        # Assign new name to modifiedpokemontotal if not already assigned (making sure to assign Deckmon original name if Eevee or Egg)
        if already_assigned == False and name != "Eevee" and name != "Egg":
            deckmonData = [name, item[0], Level]
            modifiedpokemontotal.append(deckmonData)
        elif already_assigned == False:
            deckmonData = [deckmon, item[0], Level]
            modifiedpokemontotal.append(deckmonData)
        msgtxt += alertMsgText(deckmon, item[0], name, int(
            Level), int(previouslevel), nickname, already_assigned)
        # If already assigned, assign new level/name to modifiedpokemontotal if new level/name
        if already_assigned == True:
            for thing in pokemontotal:
                if thing[1] == item[0]:
                    if name == "Eevee" or name == "Egg":
                        if nickname:
                            if (thing[0], thing[1], Level, nickname) in modifiedpokemontotal:
                                pass
                            else:
                                modifiedpokemontotal.append(
                                    [thing[0], thing[1], Level, nickname])
                        else:
                            if (thing[0], thing[1], Level) in modifiedpokemontotal:
                                pass
                            else:
                                modifiedpokemontotal.append(
                                    [thing[0], thing[1], Level])
                    else:
                        if nickname:
                            if (name, thing[1], Level, nickname) in modifiedpokemontotal:
                                pass
                            else:
                                modifiedpokemontotal.append(
                                    [name, thing[1], Level, nickname])
                        else:
                            if (name, thing[1], Level) in modifiedpokemontotal:
                                pass
                            else:
                                modifiedpokemontotal.append(
                                    [name, thing[1], Level])
        if nickname:
            displayData = (name, item[0], Level, nickname)
        else:
            displayData = (name, item[0], Level)
        multiData.append(displayData)

    # After iterating through each deck, store data into pokemanki.json
    write_json("_pokemanki.json", modifiedpokemontotal)
    # Only display message if changes
    if msgtxt != "Hello Pokémon Trainer!":
        msgbox2 = QMessageBox()
        msgbox2.setWindowTitle("Pokemanki")
        msgbox2.setText(msgtxt)
        msgbox2.exec_()
    # Return multiData
    return multiData
