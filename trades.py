import os
import inspect
import random
import csv
from datetime import date as dt

from aqt.qt import *
from aqt import mw

from .utils import *


def pokemonLevelRangesFromCsv(csv_fpath):
    pokemon_records = []

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

            pk1_lo_lv = 0
            if first_ev_lv:
                pk1_hi_lv = first_ev_lv
            else:
                pk1_hi_lv = 100
            pokemon_records.append((pokemon, tier, pk1_lo_lv, pk1_hi_lv))

            if first_ev is not None:
                pk2_lo_lv = pk1_hi_lv
                if second_ev_lv:
                    pk2_hi_lv = second_ev_lv
                else:
                    pk2_hi_lv = 100
                pokemon_records.append((first_ev, tier, pk2_lo_lv, pk2_hi_lv))

            if second_ev is not None:
                pk3_lo_lv = pk2_hi_lv
                pk3_hi_lv = 100
                pokemon_records.append((second_ev, tier, pk3_lo_lv, pk3_hi_lv))

    return pokemon_records


class Trades:
    def __init__(self):
        self.tradewindow = QDialog()
        self.dirname = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))
        self.mediafolder = mediafolder

        pokemon_records = []
        csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen1.csv"
        pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
        if config['gen2']:
            csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen2.csv"
            pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))

            if config['gen4_evolutions']:
                csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen1_plus2_plus4.csv"
                pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
                csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen2_plus4.csv"
                pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
            else:
                csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen1_plus2_no4.csv"
                pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
                csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen2_no4.csv"
                pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
        else:
            if config['gen4_evolutions']:
                # a lot of gen 4 evolutions that affect gen 1 also include gen 2 evolutions
                # so let's just include gen 2 for these evolution lines
                csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen1_plus2_plus4.csv"
                pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
            else:
                csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen1_no2_no4.csv"
                pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))

        if config['gen3']:
            csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen3.csv"
            pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
        if config['gen4']:
            csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen4.csv"
            pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
        if config['gen5']:
            csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen5.csv"
            pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))

        self.allpokemon = pokemon_records
        self.f = get_json("_decksortags.json", "")

    def newTrades(self):
        self.trades = []
        i = 0
        f = self.f
        if f:
            if os.path.exists("%s/_tagmon.json" % self.mediafolder):
                deckmonlist = get_json("_tagmon.json", [])
                sorteddeckmonlist = list(reversed(deckmonlist))
                noeggslist = []
                for item in sorteddeckmonlist:
                    if int(item[2]) >= 5:
                        noeggslist.append(item)
                deckmons = []
                for item in noeggslist:
                    for thing in deckmons:
                        if item[1] == thing[1]:
                            break
                    else:
                        deckmons.append(item)
                deckmonlist = deckmons
            else:
                nopokemon = QMessageBox()
                nopokemon.setWindowTitle("Pokemanki")
                nopokemon.setText(
                    "Please open the Stats window to get your Pokémon.")
                nopokemon.exec_()
                return
        else:
            deckmonlist = get_json("_pokemanki.json", None)
            if deckmonlist:
                sorteddeckmonlist = list(reversed(deckmonlist))
                noeggslist = []
                for item in sorteddeckmonlist:
                    if int(item[2]) >= 5:
                        noeggslist.append(item)
                deckmons = []
                for item in noeggslist:
                    for thing in deckmons:
                        if item[1] == thing[1]:
                            break
                    else:
                        deckmons.append(item)
                deckmonlist = deckmons
            else:
                nopokemon = QMessageBox()
                nopokemon.setWindowTitle("Pokemanki")
                nopokemon.setText(
                    "Please open the Stats window to get your Pokémon.")
                nopokemon.exec_()
                return
        possiblehaveslist = []
        while i < 3:
            randno = random.randint(0, len(deckmonlist)-1)
            pokemon = deckmonlist[randno]
            for item in self.allpokemon:
                if pokemon[0] == item[0]:
                    want = item
            possiblehaves = []
            if want[1] == "F":
                for item in self.allpokemon:
                    if (item[1] == "F" or item[1] == "E") and (item[2] < int(pokemon[2]) < item[3]):
                        possiblehaves.append(item)
            elif want[1] == "E":
                for item in self.allpokemon:
                    if (item[1] == "F" or item[1] == "E" or item[1] == "D") and (item[2] < int(pokemon[2]) < item[3]):
                        possiblehaves.append(item)
            elif want[1] == "D":
                for item in self.allpokemon:
                    if (item[1] == "C" or item[1] == "E" or item[1] == "D") and (item[2] < int(pokemon[2]) < item[3]):
                        possiblehaves.append(item)
            elif want[1] == "C":
                for item in self.allpokemon:
                    if (item[1] == "C" or item[1] == "B" or item[1] == "D") and (item[2] < int(pokemon[2]) < item[3]):
                        possiblehaves.append(item)
            elif want[1] == "B":
                for item in self.allpokemon:
                    if (item[1] == "C" or item[1] == "B" or item[1] == "A") and (item[2] < int(pokemon[2]) < item[3]):
                        possiblehaves.append(item)
            elif want[1] == "A":
                for item in self.allpokemon:
                    if (item[1] == "B" or item[1] == "A") and (item[2] < int(pokemon[2]) < item[3]):
                        possiblehaves.append(item)
            if len(possiblehaves) > 1:
                randno = random.randint(0, len(possiblehaves)-1)
                have = possiblehaves[randno]
            elif len(possiblehaves) == 1:
                have = possiblehaves[0]
            else:
                continue
            if have[0].startswith("Eevee") and want[0].startswith("Eevee"):
                self.trades.append(
                    (("Eevee", have[1], have[2], have[3]), ("Eevee", want[1], want[2], want[3])))
            elif have[0].startswith("Eevee"):
                self.trades.append(
                    (("Eevee", have[1], have[2], have[3]), want))
            elif want[0].startswith("Eevee"):
                self.trades.append(
                    (have, ("Eevee", want[1], want[2], want[3])))
            else:
                self.trades.append((have, want))
            possiblehaveslist.append(possiblehaves)
            i += 1
        date = dt.today().strftime("%d/%m/%Y")
        if f:
            tradeData = [date, self.trades, "tags"]
        else:
            tradeData = [date, self.trades, "decks"]
        testData = [date, self.trades, possiblehaveslist]
        write_json("_trades.json", tradeData)

    def tradeFunction(self):
        # show a message box
        f = self.f
        tradeData = get_json("_trades.json", None)
        if tradeData:
            date = dt.today().strftime("%d/%m/%Y")
            if date == tradeData[0] and len(tradeData) == 3:
                if f == tradeData[2]:
                    self.trades = tradeData[1]
                elif f == "" and tradeData[2] == "decks":
                    self.trades = tradeData[1]
                else:
                    self.newTrades()
                    tradeData = get_json("_trades.json")
            else:
                self.newTrades()
                tradeData = get_json("_trades.json")
        else:
            self.newTrades()
            tradeData = get_json("_trades.json")
        tradewindow = self.tradewindow
        tradewindow.setWindowTitle("Pokemanki")
        tradewindow.setWindowModality(Qt.ApplicationModal)
        table = """<table>
                   <tr>
                   <td height 50 width = 150 align = center></td>
                   <td height 50 width = 150 align = center><h1>Today's Trades</h1></td>
                   <td height 50 width = 150 align = center></td>
                   <tr>
                   <tr>
                   <td height 40 width = 150 align = center><h2>Trainer 1</h2></td>
                   <td height 40 width = 150 align = center><h2>Trainer 2</h2></td>
                   <td height 40 width = 150 align = center><h2>Trainer 3</h2></td>
                   <tr>
                   <tr>
                   <td height 30 width = 150 align = center><h3>Currently has</h3></td>
                   <td height 30 width = 150 align = center><h3>Currently has</h3></td>
                   <td height 30 width = 150 align = center><h3>Currently has</h3></td>
                   <tr>
                   <td height = 150 width = 150 align = center><img src = "%s/pokemon_images/%s.png" width = 150 height = 150></td>
                   <td height = 150 width = 150 align = center><img src = "%s/pokemon_images/%s.png" width = 150 height = 150></td>
                   <td height = 150 width = 150 align = center><img src = "%s/pokemon_images/%s.png" width = 150 height = 150></td>
                   </tr>
                   <tr>
                   <td height = 30 width = 150 align = center><b>%s</b></td>
                   <td height = 30 width = 150 align = center><b>%s</b></td>
                   <td height = 30 width = 150 align = center><b>%s</b></td>
                   </tr>
                   <tr>
                   <td height 1 width = 150 align = center></td>
                   <td height 1 width = 150 align = center></td>
                   <td height 1 width = 150 align = center></td>
                   <tr>
                   <tr>
                   <td height 30 width = 150 align = center><h3>And wants</h3></td>
                   <td height 30 width = 150 align = center><h3>And wants</h3></td>
                   <td height 30 width = 150 align = center><h3>And wants</h3></td>
                   <tr>
                   <td height = 150 width = 150 align = center><img src = "%s/pokemon_images/%s.png" width = 150 height = 150></td>
                   <td height = 150 width = 150 align = center><img src = "%s/pokemon_images/%s.png" width = 150 height = 150></td>
                   <td height = 150 width = 150 align = center><img src = "%s/pokemon_images/%s.png" width = 150 height = 150></td>
                   </tr>
                   <tr>
                   <td height = 30 width = 150 align = center><b>%s</b></td>
                   <td height = 30 width = 150 align = center><b>%s</b></td>
                   <td height = 30 width = 150 align = center><b>%s</b></td>
                   </tr>
                   </table>""" % (self.dirname, self.trades[0][0][0], self.dirname, self.trades[1][0][0], self.dirname, self.trades[2][0][0], self.trades[0][0][0], self.trades[1][0][0], self.trades[2][0][0], self.mediafolder, self.trades[0][1][0], self.mediafolder, self.trades[1][1][0], self.mediafolder, self.trades[2][1][0], self.trades[0][1][0], self.trades[1][1][0], self.trades[2][1][0])
        lbl1 = QLabel(table, tradewindow)
        lbl1.move(0, 0)
        lbl2 = QLabel("", tradewindow)
        lbl2.move(360, 420)
        btn1 = QPushButton("TRADE", tradewindow)
        btn1.move(50, 455)
        btn2 = QPushButton("TRADE", tradewindow)
        btn2.move(200, 455)
        btn3 = QPushButton("TRADE", tradewindow)
        btn3.move(350, 455)
        btn1.clicked.connect(self.trade1)
        btn2.clicked.connect(self.trade2)
        btn3.clicked.connect(self.trade3)
        tradewindow.exec_()

    def trade1(self):
        have = self.trades[0][0]
        want = self.trades[0][1]
        possiblefits = []
        f = self.f
        if f:
            deckmonlist = get_json("_tagmon.json")
            if deckmonlist:
                sorteddeckmonlist = list(reversed(deckmonlist))
                deckmons = []
                for item in sorteddeckmonlist:
                    for thing in deckmons:
                        if item[1] == thing[1]:
                            break
                    else:
                        deckmons.append(item)
                deckmonlist = deckmons
            else:
                nopokemon = QMessageBox()
                nopokemon.setWindowTitle("Pokemanki")
                nopokemon.setText(
                    "Please open the Stats window to get your Pokémon.")
                nopokemon.exec_()
                return
        else:
            deckmonlist = get_json("_pokemanki.json", None)
            if deckmonlist:
                sorteddeckmonlist = list(reversed(deckmonlist))
                deckmons = []
                for item in sorteddeckmonlist:
                    for thing in deckmons:
                        if item[1] == thing[1]:
                            break
                    else:
                        deckmons.append(item)
                deckmonlist = deckmons
            else:
                nopokemon = QMessageBox()
                nopokemon.setWindowTitle("Pokemanki")
                nopokemon.setText(
                    "Please open the Stats window to get your Pokémon.")
                nopokemon.exec_()
                return
        for item in deckmonlist:
            if item[0] == want[0] or (item[0].startswith("Eevee") and want[0] == "Eevee") and int(item[2]) >= 5:
                possiblefits.append(item)
        if possiblefits == []:
            novalidpokemon = QMessageBox()
            novalidpokemon.setWindowTitle("Pokemanki")
            novalidpokemon.setText(
                "Sorry, you do not have the Pokemon needed to complete this trade.")
            novalidpokemon.exec_()
            return
        displaylist = []
        for item in possiblefits:
            deckname = mw.col.decks.name(item[1])
            if len(item) == 4:
                if item[0].startswith("Eevee"):
                    displaytext = "%s - Eevee (Level %s) from %s" % (
                        item[3], int(item[2]), deckname)
                else:
                    displaytext = "%s - %s (Level %s) from %s" % (
                        item[3], item[0], int(item[2]), deckname)
            else:
                if item[0].startswith("Eevee"):
                    displaytext = "Eevee (Level %s) from %s" % (
                        int(item[2]), deckname)
                else:
                    displaytext = "%s (Level %s) from %s" % (
                        item[0], int(item[2]), deckname)
            displaylist.append(displaytext)
        totallist = list(zip(possiblefits, displaylist))
        possiblepokemon = QWidget()
        inp, ok = QInputDialog.getItem(
            possiblepokemon, "Pokemanki", "Choose a Pokemon to trade for %s" % have[0], displaylist, 0, False)
        tradepokemon = []
        if ok and inp:
            for thing in totallist:
                if inp in thing:
                    tradepokemon = thing[0]
                    displaytext = inp
        if not tradepokemon:
            return
        confirmation = QMessageBox()
        confirmation.setWindowTitle("Pokemanki")
        confirmation.setText(
            "Are you sure you want to trade your %s for a %s" % (displaytext, have[0]))
        confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmation.setDefaultButton(QMessageBox.No)
        result = confirmation.exec_()
        if result == QMessageBox.Yes:
            modifieddeckmonlist = []
            for item in deckmonlist:
                if item[1] == tradepokemon[1]:
                    if have[0] == "Eevee":
                        eevee = random.randint(1, 3)
                        newpokemon = ("Eevee%s" % eevee, item[1], item[2])
                    else:
                        newpokemon = (have[0], item[1], item[2])
                    modifieddeckmonlist.append(newpokemon)
                else:
                    modifieddeckmonlist.append(item)
            write_json("_pokemanki.json", modifieddeckmonlist)
            self.tradewindow.done(QDialog.Accepted)
            tradedone = QMessageBox()
            tradedone.setWindowTitle("Pokemanki")
            tradedone.setText("You have traded your %s for a %s" %
                              (displaytext, have[0]))
            tradedone.exec_()

    def trade2(self):
        have = self.trades[1][0]
        want = self.trades[1][1]
        possiblefits = []
        f = self.f
        if f:
            deckmonlist = get_json("_tagmon.json")
            if deckmonlist:
                sorteddeckmonlist = list(reversed(deckmonlist))
                deckmons = []
                for item in sorteddeckmonlist:
                    for thing in deckmons:
                        if item[1] == thing[1]:
                            break
                    else:
                        deckmons.append(item)
                deckmonlist = deckmons
            else:
                nopokemon = QMessageBox()
                nopokemon.setWindowTitle("Pokemanki")
                nopokemon.setText(
                    "Please open the Stats window to get your Pokémon.")
                nopokemon.exec_()
                return
        else:
            deckmonlist = get_json("_pokemanki.json", None)
            if deckmonlist:
                sorteddeckmonlist = list(reversed(deckmonlist))
                deckmons = []
                for item in sorteddeckmonlist:
                    for thing in deckmons:
                        if item[1] == thing[1]:
                            break
                    else:
                        deckmons.append(item)
                deckmonlist = deckmons
            else:
                nopokemon = QMessageBox()
                nopokemon.setWindowTitle("Pokemanki")
                nopokemon.setText(
                    "Please open the Stats window to get your Pokémon.")
                nopokemon.exec_()
                return
        for item in deckmonlist:
            if item[0] == want[0] or (item[0].startswith("Eevee") and want[0] == "Eevee") and int(item[2]) >= 5:
                possiblefits.append(item)
        if possiblefits == []:
            novalidpokemon = QMessageBox()
            novalidpokemon.setWindowTitle("Pokemanki")
            novalidpokemon.setText(
                "Sorry, you do not have the Pokémon needed to complete this trade.")
            novalidpokemon.exec_()
            return
        displaylist = []
        for item in possiblefits:
            deckname = mw.col.decks.name(item[1])
            if len(item) == 4:
                if item[0].startswith("Eevee"):
                    displaytext = "%s - Eevee (Level %s) from %s" % (
                        item[3], int(item[2]), deckname)
                else:
                    displaytext = "%s - %s (Level %s) from %s" % (
                        item[3], item[0], int(item[2]), deckname)
            else:
                if item[0].startswith("Eevee"):
                    displaytext = "Eevee (Level %s) from %s" % (
                        int(item[2]), deckname)
                else:
                    displaytext = "%s (Level %s) from %s" % (
                        item[0], int(item[2]), deckname)
            displaylist.append(displaytext)
        totallist = list(zip(possiblefits, displaylist))
        possiblepokemon = QWidget()
        inp, ok = QInputDialog.getItem(
            possiblepokemon, "Pokemanki", "Choose a Pokemon to trade for %s" % have[0], displaylist, 0, False)
        tradepokemon = []
        if ok and inp:
            for thing in totallist:
                if inp in thing:
                    tradepokemon = thing[0]
                    displaytext = inp
        if not tradepokemon:
            return
        confirmation = QMessageBox()
        confirmation.setWindowTitle("Pokemanki")
        confirmation.setText(
            "Are you sure you want to trade your %s for a %s" % (displaytext, have[0]))
        confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmation.setDefaultButton(QMessageBox.No)
        result = confirmation.exec_()
        if result == QMessageBox.Yes:
            modifieddeckmonlist = []
            for item in deckmonlist:
                if item[1] == tradepokemon[1]:
                    if have[0] == "Eevee":
                        eevee = random.randint(1, 3)
                        newpokemon = ("Eevee%s" % eevee, item[1], item[2])
                    else:
                        newpokemon = (have[0], item[1], item[2])
                    modifieddeckmonlist.append(newpokemon)
                else:
                    modifieddeckmonlist.append(item)
            write_json("_pokemanki.json", modifieddeckmonlist)
            self.tradewindow.done(QDialog.Accepted)
            tradedone = QMessageBox()
            tradedone.setWindowTitle("Pokemanki")
            tradedone.setText("You have traded your %s for a %s" %
                              (displaytext, have[0]))
            tradedone.exec_()

    def trade3(self):
        have = self.trades[2][0]
        want = self.trades[2][1]
        possiblefits = []
        f = self.f
        if f:
            deckmonlist = get_json("_tagmon.json", None)
            if deckmonlist:
                sorteddeckmonlist = list(reversed(deckmonlist))
                deckmons = []
                for item in sorteddeckmonlist:
                    for thing in deckmons:
                        if item[1] == thing[1]:
                            break
                    else:
                        deckmons.append(item)
                deckmonlist = deckmons
            else:
                nopokemon = QMessageBox()
                nopokemon.setWindowTitle("Pokemanki")
                nopokemon.setText(
                    "Please open the Stats window to get your Pokémon.")
                nopokemon.exec_()
                return
        else:
            deckmonlist = get_json("_pokemanki.json", None)
            if deckmonlist:
                sorteddeckmonlist = list(reversed(deckmonlist))
                deckmons = []
                for item in sorteddeckmonlist:
                    for thing in deckmons:
                        if item[1] == thing[1]:
                            break
                    else:
                        deckmons.append(item)
                deckmonlist = deckmons
            else:
                nopokemon = QMessageBox()
                nopokemon.setWindowTitle("Pokemanki")
                nopokemon.setText(
                    "Please open the Stats window to get your Pokémon.")
                nopokemon.exec_()
                return
        for item in deckmonlist:
            if item[0] == want[0] or (item[0].startswith("Eevee") and want[0] == "Eevee") and int(item[2]) >= 5:
                possiblefits.append(item)
        if possiblefits == []:
            novalidpokemon = QMessageBox()
            novalidpokemon.setWindowTitle("Pokemanki")
            novalidpokemon.setText(
                "Sorry, you do not have the Pokemon needed to complete this trade.")
            novalidpokemon.exec_()
            return
        displaylist = []
        for item in possiblefits:
            deckname = mw.col.decks.name(item[1])
            if len(item) == 4:
                if item[0].startswith("Eevee"):
                    displaytext = "%s - Eevee (Level %s) from %s" % (
                        item[3], int(item[2]), deckname)
                else:
                    displaytext = "%s - %s (Level %s) from %s" % (
                        item[3], item[0], int(item[2]), deckname)
            else:
                if item[0].startswith("Eevee"):
                    displaytext = "Eevee (Level %s) from %s" % (
                        int(item[2]), deckname)
                else:
                    displaytext = "%s (Level %s) from %s" % (
                        item[0], int(item[2]), deckname)
            displaylist.append(displaytext)
        totallist = list(zip(possiblefits, displaylist))
        possiblepokemon = QWidget()
        inp, ok = QInputDialog.getItem(
            possiblepokemon, "Pokemanki", "Choose a Pokemon to trade for %s" % have[0], displaylist, 0, False)
        tradepokemon = []
        if ok and inp:
            for thing in totallist:
                if inp in thing:
                    tradepokemon = thing[0]
                    displaytext = inp
        if not tradepokemon:
            return
        confirmation = QMessageBox()
        confirmation.setWindowTitle("Pokemanki")
        confirmation.setText(
            "Are you sure you want to trade your %s for a %s" % (displaytext, have[0]))
        confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmation.setDefaultButton(QMessageBox.No)
        result = confirmation.exec_()
        if result == QMessageBox.Yes:
            modifieddeckmonlist = []
            for item in deckmonlist:
                if item[1] == tradepokemon[1]:
                    if have[0] == "Eevee":
                        eevee = random.randint(1, 3)
                        newpokemon = ("Eevee%s" % eevee, item[1], item[2])
                    else:
                        newpokemon = (have[0], item[1], item[2])
                    modifieddeckmonlist.append(newpokemon)
                else:
                    modifieddeckmonlist.append(item)
            write_json("_pokemanki.json", modifieddeckmonlist)
            self.tradewindow.done(QDialog.Accepted)
            tradedone = QMessageBox()
            tradedone.setWindowTitle("Pokemanki")
            tradedone.setText("You have traded your %s for a %s" %
                              (displaytext, have[0]))
            tradedone.exec_()
