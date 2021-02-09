from .utils import *
from .tags import Tags

import json

from aqt.qt import *

# Nickname Settings


def Nickname():
    f = get_json("_decksortags.json", "")
    if (mediafolder / "_tagmon.json").exists():
        deckmonlist = json.load(open(mediafolder / "_tagmon.json"))
    else:
        nopokemon = QMessageBox()
        nopokemon.setWindowTitle("Pokemanki")
        nopokemon.setText(
            "Please open the Stats window to get your Pokémon.")
        nopokemon.exec_()
        return

    displaylist = []
    for item in deckmonlist:
        deckname = mw.col.decks.name(item[1])
        if len(item) == 4:
            if item[2] < 5:
                displaytext = "%s - Egg from %s" % (item[3], deckname)
            elif item[0].startswith("Eevee"):
                displaytext = "%s - Eevee (Level %s) from %s" % (
                    item[3], int(item[2]), deckname)
            else:
                displaytext = "%s - %s (Level %s) from %s" % (
                    item[3], item[0], int(item[2]), deckname)
        else:
            if item[2] < 5:
                displaytext = "Egg from %s" % (deckname)
            elif item[0].startswith("Eevee"):
                displaytext = "Eevee (Level %s) from %s" % (
                    int(item[2]), deckname)
            else:
                displaytext = "%s (Level %s) from %s" % (
                    item[0], int(item[2]), deckname)
        displaylist.append(displaytext)
    totallist = list(zip(deckmonlist, displaylist))
    nicknamewindow = QWidget()
    inp, ok = QInputDialog.getItem(
        nicknamewindow, "Pokemanki", "Choose a Pokémon who you would like to give a new nickname", displaylist, 0, False)
    deckmon = []
    nickname = ""
    if ok and inp:
        for thing in totallist:
            if inp in thing:
                deckmon = thing[0]
                displaytext = inp
    if not deckmon:
        return
    if len(deckmon) == 4:
        nickname = deckmon[3]
    inp, ok = QInputDialog.getText(nicknamewindow, "Pokemanki", (
        "Enter a new nickname for %s (leave blank to remove nickname)" % displaytext))
    if ok:
        if inp:
            nickname = inp
            deckmon = [deckmon[0], deckmon[1], deckmon[2], nickname]
            newnickname = QMessageBox()
            newnickname.setWindowTitle("Pokemanki")
            if int(deckmon[2]) < 5:
                newnickname.setText(
                    "New nickname given to Egg - %s" % (nickname))
            elif deckmon[0].startswith("Eevee"):
                newnickname.setText(
                    "New nickname given to Eevee - %s" % (nickname))
            else:
                newnickname.setText(
                    "New nickname given to %s - %s" % (deckmon[0], nickname))
            newnickname.exec_()
        else:
            deckmon = [deckmon[0], deckmon[1], deckmon[2]]
            nicknameremoved = QMessageBox()
            nicknameremoved.setWindowTitle("Pokemanki")
            if int(deckmon[2]) < 5:
                nicknameremoved.setText("Nickname removed from Egg")
            elif deckmon[0].startswith("Eevee"):
                nicknameremoved.setText("Nickname removed from Eevee")
            else:
                nicknameremoved.setText(
                    "Nickname removed from %s" % deckmon[0])
            nicknameremoved.exec_()
    modifieddeckmonlist = []
    for item in deckmonlist:
        if item[1] == deckmon[1]:
            modifieddeckmonlist.append(deckmon)
        else:
            modifieddeckmonlist.append(item)
    if f:
        with open(mediafolder / "_tagmon.json", "w") as f:
            json.dump(modifieddeckmonlist, f)
    else:
        with open(mediafolder / "_pokemanki.json", "w") as f:
            json.dump(modifieddeckmonlist, f)


def Toggle():
    window = QWidget()
    items = ("Decks (Default)", "Tags")
    inp, ok = QInputDialog.getItem(
        window, "Pokemanki", "Choose how you would like Pokemanki to assign you Pokémon.", items, 0, False)
    if ok and inp:
        if inp == "Tags":
            with open(("%s/_decksortags.json" % mediafolder), "w") as f:
                json.dump(inp, f)
            tags = Tags()
            tags.tagMenu()
            settingschanged = QMessageBox()
            settingschanged.setWindowTitle("Pokemanki")
            settingschanged.setText(
                "Please restart Anki to see your updated Pokémon.")
            settingschanged.exec_()
        else:
            with open(("%s/_decksortags.json" % mediafolder), "w") as f:
                json.dump("", f)
            settingschanged = QMessageBox()
            settingschanged.setWindowTitle("Pokemanki")
            settingschanged.setText(
                "Please restart Anki to see your updated Pokémon.")
            settingschanged.exec_()

# Threshold Settings


def ThresholdSettings():
    global thresholdlist
    # Find recommended number of cards for starter Pokemon threshold (based on deck with highest number of cards).
    decklist = mw.col.decks.allIds()
    sumlist = []
    for deck in decklist:
        sumlist.append(len(mw.col.decks.cids(deck)))
    recommended = .797 * max(sumlist)
    # Refresh threshold settings
    thresholdlist = json.load(open("%s/_pokemankisettings.json" % mediafolder))
    # Make settings window (input dialog)
    window = QWidget()
    inp, ok = QInputDialog.getInt(window, "Pokemanki", (
        "Change number of cards needed in a deck to get a starter Pokémon (recommended %d)" % recommended), value=thresholdlist[4])
    if ok:
        # Make sure threshold is at least 10
        if inp < 10:
            error = QMessageBox()
            error.setWindowTitle("Pokemanki")
            error.setText("Number must be at least ten")
            error.exec_()
        # Change settings and save them if the threshold is changed
        elif inp != thresholdlist[4]:
            newthresholdlist = [
                int(0.1*inp), int(0.25*inp), int(0.5*inp), int(0.75*inp), int(inp)]
            with open(("%s/_pokemankisettings.json" % mediafolder), "w") as f:
                json.dump(newthresholdlist, f)
            # Message box confirming change
            settingschanged = QMessageBox()
            settingschanged.setWindowTitle("Pokemanki")
            settingschanged.setText("Your settings have been changed")
            settingschanged.exec_()
    # Show the window
    window.show()

# Reset Pokemon


def ResetPokemon():
    # Make message box
    resetwindow = QMessageBox()
    resetwindow.setWindowTitle("Pokemanki")
    resetwindow.setText("Are you sure you want to reset your Pokémon?")
    resetwindow.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    resetwindow.setDefaultButton(QMessageBox.No)
    resetresult = resetwindow.exec_()
    # Clear pokemanki.json if Yes
    if resetresult == QMessageBox.Yes:
        write_json("_pokemanki.json", [])
        write_json("_tagmon.json", [])
        # Message box confirming reset
        resetdone = QMessageBox()
        resetdone.setWindowTitle("Pokemanki")
        resetdone.setText("Pokemon reset")
        resetdone.exec_()


def MovetoBottom():
    with open("%s/_toporbottom.json" % mediafolder, "w") as f:
        json.dump("bottom", f)
    settingschanged = QMessageBox()
    settingschanged.setWindowTitle("Pokemanki")
    settingschanged.setText(
        "Please restart Anki to see your updated settings.")
    settingschanged.exec_()


def MovetoTop():

    with open("%s/_toporbottom.json" % mediafolder, "w") as f:
        json.dump("", f)
    settingschanged = QMessageBox()
    settingschanged.setWindowTitle("Pokemanki")
    settingschanged.setText(
        "Please restart Anki to see your updated settings.")
    settingschanged.exec_()


def giveEverstone():
    f = get_json("_decksortags.json", None)

    if f:
        pokemon = get_json("_tagmon.json")
    else:
        pokemon = get_json("_pokemanki.json")
    everstonelist = get_json("_everstonelist.json", default=[])
    everstonepokemonlist = get_json("_everstonepokemonlist.json", default=[])

    everstoneables = []
    for item in pokemon:
        if f:
            cb = ("%s (Level %s) from %s" % (item[0], item[2], item[1]))
        else:
            cb = ("%s (Level %s) from %s" %
                  (item[0], item[2], mw.col.decks.name(item[1])))
        if item[1] in everstonelist:
            continue
        elif cb in everstoneables:
            continue
        else:
            everstoneables.append(cb)

    window = QWidget()
    inp, ok = QInputDialog.getItem(
        window, "Pokemanki", "Select a Pokemon you would like to give an everstone to.", sorted(everstoneables), 0, False)
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        everstone_pokemon_name = inp.split(" (Level ")[0]
        if f:
            everstonelist.append(item)
            everstonepokemonlist.append(everstone_pokemon_name)
        else:
            everstonelist.append(mw.col.decks.id(item))
            everstonepokemonlist.append(everstone_pokemon_name)
        settingschanged = QMessageBox()
        settingschanged.setWindowTitle("Pokemanki")
        settingschanged.setText("Please restart Anki to see changes.")
        settingschanged.exec_()
    with open("%s/_everstonelist.json" % mediafolder, "w") as f:
        json.dump(everstonelist, f)
    with open("%s/_everstonepokemonlist.json" % mediafolder, "w") as f:
        json.dump(everstonepokemonlist, f)


def takeEverstone():
    f = get_json("_decksortags.json", None)
    if f:
        pokemon = get_json("_tagmon.json")
    else:
        pokemon = get_json("_pokemanki.json")
    everstonelist = get_json("_everstonelist.json", [])
    everstonepokemonlist = get_json("_everstonepokemonlist.json", [])
    if not everstonelist:
        noeverstone = QMessageBox()
        noeverstone.setWindowTitle("Pokemanki")
        noeverstone.setText("None of your Pokémon are holding everstones.")
        noeverstone.exec_()
        return
    possibleuneverstones = []
    for thing in everstonelist:
        for item in pokemon:
            if item[1] == thing:
                if f:
                    cb = ("%s from %s" % (item[0], item[1]))
                else:
                    cb = ("%s from %s" % (item[0], mw.col.decks.name(item[1])))
                if cb in possibleuneverstones:
                    continue
                else:
                    possibleuneverstones.append(cb)
        else:
            continue
    window = QWidget()
    inp, ok = QInputDialog.getItem(
        window, "Pokemanki", "Select a Pokemon whose everstone you would like to take.", sorted(possibleuneverstones), 0, False)
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        if f:
            everstonelist.remove(item)
            everstonepokemonlist.remove(textlist[0])
        else:
            everstonelist.remove(mw.col.decks.id(item))
            everstonepokemonlist.remove(textlist[0])
        settingschanged = QMessageBox()
        settingschanged.setWindowTitle("Pokemanki")
        settingschanged.setText("Please restart Anki to see your changes.")
        settingschanged.exec_()
    with open("%s/_everstonelist.json" % mediafolder, "w") as f:
        json.dump(everstonelist, f)


def giveMegastone():
    f = get_json("_decksortags.json", None)
    if f:
        pokemon = get_json("_tagmon.json")
    else:
        pokemon = get_json("_pokemanki.json")
    megastonelist = get_json("_megastonelist.json", [])
    megastoneables = []
    for item in pokemon:
        if item[2] >= 70:
            if f:
                cb = ("%s (Level %s) from %s" % (item[0], item[2], item[1]))
            else:
                cb = ("%s (Level %s) from %s" %
                      (item[0], item[2], mw.col.decks.name(item[1])))
            if item[1] in megastonelist:
                continue
            elif cb in megastoneables:
                continue
            else:
                megastoneables.append(cb)
        else:
            continue
    window = QWidget()
    inp, ok = QInputDialog.getItem(
        window, "Pokemanki", "Select a Pokemon you would like to give a mega stone to", sorted(megastoneables), 0, False)
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        if f:
            megastonelist.append(item)
        else:
            megastonelist.append(mw.col.decks.id(item))
        settingschanged = QMessageBox()
        settingschanged.setWindowTitle("Pokemanki")
        settingschanged.setText("Please restart Anki to see your changes.")
        settingschanged.exec_()
    with open("%s/_megastonelist.json" % mediafolder, "w") as f:
        json.dump(megastonelist, f)


def takeMegastone():
    f = get_json("_decksortags.json", None)
    if f:
        pokemon = get_json("_tagmon.json")
    else:
        pokemon = get_json("_pokemanki.json")
    megastonelist = get_json("_megastonelist.json", [])
    if not megastonelist:
        nomegastone = QMessageBox()
        nomegastone.setWindowTitle("Pokemanki")
        nomegastone.setText("None of your Pokémon are holding mega stones.")
        nomegastone.exec_()
        return
    possibleunmegastones = []
    for thing in megastonelist:
        for item in pokemon:
            if item[1] == thing:
                if f:
                    cb = ("%s from %s" % (item[0], item[1]))
                else:
                    cb = ("%s from %s" % (item[0], mw.col.decks.name(item[1])))
                if cb in possibleunmegastones:
                    continue
                else:
                    possibleunmegastones.append(cb)
        else:
            continue
    window = QWidget()
    inp, ok = QInputDialog.getItem(
        window, "Pokemanki", "Select a Pokemon whose mega stone you would like to take", sorted(possibleunmegastones), 0, False)
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        if f:
            megastonelist.remove(item)
        else:
            megastonelist.remove(mw.col.decks.id(item))
        settingschanged = QMessageBox()
        settingschanged.setWindowTitle("Pokemanki")
        settingschanged.setText("Please restart Anki to see your changes.")
        settingschanged.exec_()
    with open("%s/_megastonelist.json" % mediafolder, "w") as f:
        json.dump(megastonelist, f)


def giveAlolanPassport():
    f = get_json("_decksortags.json", None)
    if f:
        pokemon = get_json("_tagmon.json")
    else:
        pokemon = get_json("_pokemanki.json")
    if os.path.exists("%s/_alolanlist.json" % mediafolder):
        alolanlist = json.load(open("%s/_alolanlist.json" % mediafolder))
    else:
        alolanlist = []

    alolanables = []
    for item in pokemon:
        if f:
            cb = ("%s (Level %s) from %s" % (item[0], item[2], item[1]))
        else:
            cb = ("%s (Level %s) from %s" %
                  (item[0], item[2], mw.col.decks.name(item[1])))
        if item[1] in alolanlist:
            continue
        elif cb in alolanables:
            continue
        else:
            alolanables.append(cb)

    window = QWidget()
    inp, ok = QInputDialog.getItem(
        window, "Pokemanki", "Select a Pokemon you would like to give an Alolan Passport to.", sorted(alolanables), 0, False)
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        alolan_pokemon_name = inp.split(" (Level ")[0]
        if f:
            alolanlist.append(item)
        else:
            alolanlist.append(mw.col.decks.id(item))
        settingschanged = QMessageBox()
        settingschanged.setWindowTitle("Pokemanki")
        settingschanged.setText("Please restart Anki to see changes.")
        settingschanged.exec_()
    with open("%s/_alolanlist.json" % mediafolder, "w") as f:
        json.dump(alolanlist, f)


def takeAlolanPassport():
    f = get_json("_decksortags.json", None)
    if f:
        pokemon = get_json("_tagmon.json")
    else:
        pokemon = get_json("_pokemanki.json")
    if os.path.exists("%s/_alolanlist.json" % mediafolder):
        alolanlist = json.load(open("%s/_alolanlist.json" % mediafolder))
    else:
        alolanlist = []
    if not alolanlist:
        noalolan = QMessageBox()
        noalolan.setWindowTitle("Pokemanki")
        noalolan.setText(
            "None of your Pokémon are holding an Alolan Passport.")
        noalolan.exec_()
        return
    possibleunalolans = []
    for thing in alolanlist:
        for item in pokemon:
            if item[1] == thing:
                if f:
                    cb = ("%s from %s" % (item[0], item[1]))
                else:
                    cb = ("%s from %s" % (item[0], mw.col.decks.name(item[1])))
                if cb in possibleunalolans:
                    continue
                else:
                    possibleunalolans.append(cb)
        else:
            continue
    window = QWidget()
    inp, ok = QInputDialog.getItem(
        window, "Pokemanki", "Select a Pokemon whose Alolan Passport you would like to take.", sorted(possibleunalolans), 0, False)
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        if f:
            alolanlist.remove(item)
        else:
            alolanlist.remove(mw.col.decks.id(item))
        settingschanged = QMessageBox()
        settingschanged.setWindowTitle("Pokemanki")
        settingschanged.setText("Please restart Anki to see your changes.")
        settingschanged.exec_()
    with open("%s/_alolanlist.json" % mediafolder, "w") as f:
        json.dump(alolanlist, f)


def PrestigePokemon():
    f = get_json("_decksortags.json", None)
    if f:
        pokemon = get_json("_tagmon.json")
    else:
        pokemon = get_json("_pokemanki.json")
    if os.path.exists("%s/_prestigelist.json" % mediafolder):
        prestigelist = json.load(open("%s/_prestigelist.json" % mediafolder))
    else:
        prestigelist = []
    possibleprestiges = []
    for item in pokemon:
        if item[2] >= 60:
            if f:
                cb = ("%s (Level %s) from %s" % (item[0], item[2], item[1]))
            else:
                cb = ("%s (Level %s) from %s" %
                      (item[0], item[2], mw.col.decks.name(item[1])))
            if item[1] in prestigelist:
                continue
            elif cb in possibleprestiges:
                continue
            else:
                possibleprestiges.append(cb)
        else:
            continue
    window = QWidget()
    inp, ok = QInputDialog.getItem(
        window, "Pokemanki", "Select a Pokemon you would like to prestige (decreases level by 50, only availabe for Pokemon with level > 60)", sorted(possibleprestiges), 0, False)
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        if f:
            prestigelist.append(item)
        else:
            prestigelist.append(mw.col.decks.id(item))
        settingschanged = QMessageBox()
        settingschanged.setWindowTitle("Pokemanki")
        settingschanged.setText(
            "Please restart Anki to see your prestiged Pokémon.")
        settingschanged.exec_()
    with open("%s/_prestigelist.json" % mediafolder, "w") as f:
        json.dump(prestigelist, f)


def UnprestigePokemon():
    f = get_json("_decksortags.json", None)

    if f:
        pokemon = get_json("_tagmon.json")
    else:
        pokemon = get_json("_pokemanki.json")
    if os.path.exists("%s/_prestigelist.json" % mediafolder):
        prestigelist = json.load(open("%s/_prestigelist.json" % mediafolder))
    else:
        prestigelist = []
    if not prestigelist:
        noprestige = QMessageBox()
        noprestige.setWindowTitle("Pokemanki")
        noprestige.setText("You have no prestiged Pokémon.")
        noprestige.exec_()
        return
    possibleunprestiges = []
    for thing in prestigelist:
        for item in pokemon:
            if item[1] == thing:
                if f:
                    cb = ("%s from %s" % (item[0], item[1]))
                else:
                    cb = ("%s from %s" % (item[0], mw.col.decks.name(item[1])))
                if cb in possibleunprestiges:
                    continue
                else:
                    possibleunprestiges.append(cb)
        else:
            continue
    window = QWidget()
    inp, ok = QInputDialog.getItem(
        window, "Pokemanki", "Select a Pokemon you would like to unprestige", sorted(possibleunprestiges), 0, False)
    if inp and ok:
        textlist = inp.split(" from ")
        item = textlist[1]
        if f:
            prestigelist.remove(item)
        else:
            prestigelist.remove(mw.col.decks.id(item))
        settingschanged = QMessageBox()
        settingschanged.setWindowTitle("Pokemanki")
        settingschanged.setText(
            "Please restart Anki to see your unprestiged Pokémon.")
        settingschanged.exec_()
    with open("%s/_prestigelist.json" % mediafolder, "w") as f:
        json.dump(prestigelist, f)