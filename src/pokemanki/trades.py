import ctypes
import csv
import inspect
import platform
import random
from datetime import date as dt

from aqt.utils import showInfo
from aqt.qt import *
from aqt.webview import AnkiWebView

from .config import get_local_conf, get_synced_conf, save_synced_conf
from .utils import *


class Trades:
    _trade_window = None

    def __init__(self, mw):
        self.mw = mw
        self.dirname = os.path.dirname(
            os.path.abspath(inspect.getfile(inspect.currentframe()))
        )
        self.mediafolder = mediafolder
        self.allpokemon = get_pokemon_records()
        self.f = get_synced_conf()["decks_or_tags"]

    def open(self):
        """
        Set up and open a new Trade QDialog
        """
        updated_trades = self._update_trades()
        if not updated_trades:
            showInfo(
                text="No trades are possible at the moment.",
                parent=mw,
                title="Pokémanki",
            )
            return

        self._trade_window = QDialog()
        self.mw.garbage_collect_on_dialog_finish(self._trade_window)
        self._create_gui()
        self._setup_web_view()
        self._trade_window.show()

    def _create_gui(self):
        """
        Create the basic trade gui.
        """
        width = 800
        height = 600

        self._trade_window.setWindowTitle("Trade Pokémon")

        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self._web = AnkiWebView(title="pokémanki trades")
        self.vbox.addWidget(self._web)
        self._trade_window.setLayout(self.vbox)
        self._trade_window.setWindowModality(Qt.WindowModality.ApplicationModal)

        # Set in the middle of the screen
        if platform.system() == "Windows":
            user32 = ctypes.windll.user32
            posX = int(user32.GetSystemMetrics(0) / 2 - width / 2)
            posY = int(user32.GetSystemMetrics(1) / 2 - height / 2)
        else:
            posX = int(mw.frameGeometry().width() / 2 - width / 2)
            posY = int(mw.frameGeometry().height() / 2 - height / 2)

        self._trade_window.setGeometry(posX, posY, width, height)
        self._trade_window.setMinimumWidth(250)
        self._trade_window.setMinimumHeight(100)

        qconnect(self._trade_window.finished, self._on_finished)

    def _on_finished(self):
        """
        Clean up after the trade is finished to avoid having copies of the object remaining.
        """
        self._web.cleanup()
        self._web = None

    def _setup_web_view(self):
        print(self.trades)
        self._web.stdHtml(
            body=self._trades_html(),
            css=["/pokemanki_css/view_trade.css", "/pokemanki_css/main.css"],
            context=self,
        )
        self._web.set_bridge_command(self._on_bridge_cmd, self)

    def _on_bridge_cmd(self, cmd):
        if cmd in ["0", "1", "2"]:
            self._make_trade(self.trades[int(cmd)][0], self.trades[int(cmd)][1])

    def _get_new_trades(self):
        """
        Get new trades.
        """
        self.trades = []
        i = 0
        f = self.f
        if f == "tags":
            if os.path.exists("%s/_tagmon.json" % self.mediafolder):
                deckmonlist = get_synced_conf()["tagmon_list"]
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
                no_pokemon()
                return
        else:
            deckmonlist = get_synced_conf()["pokemon_list"]
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
                no_pokemon()
                return

        possiblehaveslist = []
        while i < 3:
            randno = random.randint(0, len(deckmonlist) - 1)
            pokemon = deckmonlist[randno]
            for item in self.allpokemon:
                if pokemon[0] == item[0]:
                    want = item
            possiblehaves = []
            if want[1] == "F":
                for item in self.allpokemon:
                    if (item[1] == "F" or item[1] == "E") and (
                        item[2] < int(pokemon[2]) < item[3]
                    ):
                        possiblehaves.append(item)
            elif want[1] == "E":
                for item in self.allpokemon:
                    if (item[1] == "F" or item[1] == "E" or item[1] == "D") and (
                        item[2] < int(pokemon[2]) < item[3]
                    ):
                        possiblehaves.append(item)
            elif want[1] == "D":
                for item in self.allpokemon:
                    if (item[1] == "C" or item[1] == "E" or item[1] == "D") and (
                        item[2] < int(pokemon[2]) < item[3]
                    ):
                        possiblehaves.append(item)
            elif want[1] == "C":
                for item in self.allpokemon:
                    if (item[1] == "C" or item[1] == "B" or item[1] == "D") and (
                        item[2] < int(pokemon[2]) < item[3]
                    ):
                        possiblehaves.append(item)
            elif want[1] == "B":
                for item in self.allpokemon:
                    if (item[1] == "C" or item[1] == "B" or item[1] == "A") and (
                        item[2] < int(pokemon[2]) < item[3]
                    ):
                        possiblehaves.append(item)
            elif want[1] == "A":
                for item in self.allpokemon:
                    if (item[1] == "B" or item[1] == "A") and (
                        item[2] < int(pokemon[2]) < item[3]
                    ):
                        possiblehaves.append(item)
            if len(possiblehaves) > 1:
                randno = random.randint(0, len(possiblehaves) - 1)
                have = possiblehaves[randno]
            elif len(possiblehaves) == 1:
                have = possiblehaves[0]
            else:
                i += 1
                continue
            if have[0].startswith("Eevee") and want[0].startswith("Eevee"):
                self.trades.append(
                    (
                        ("Eevee", have[1], have[2], have[3]),
                        ("Eevee", want[1], want[2], want[3]),
                    )
                )
            elif have[0].startswith("Eevee"):
                self.trades.append((("Eevee", have[1], have[2], have[3]), want))
            elif want[0].startswith("Eevee"):
                self.trades.append((have, ("Eevee", want[1], want[2], want[3])))
            else:
                self.trades.append((have, want))
            possiblehaveslist.append(possiblehaves)
            i += 1

        date = dt.today().strftime("%d/%m/%Y")
        if f == "tags":
            tradeData = [date, self.trades, "tags"]
        else:
            tradeData = [date, self.trades, "decks"]
        testData = [date, self.trades, possiblehaveslist]
        save_synced_conf("trades", tradeData)

    def _update_trades(self):
        # show a message box
        f = self.f
        tradeData = get_synced_conf()["trades"]
        if tradeData:
            date = dt.today().strftime("%d/%m/%Y")
            if date == tradeData[0] and len(tradeData) == 3:
                if f == tradeData[2]:
                    self.trades = tradeData[1]
                elif f == "" and tradeData[2] == "decks":
                    self.trades = tradeData[1]
                else:
                    self._get_new_trades()
                    tradeData = get_synced_conf()["trades"]
            else:
                self._get_new_trades()
                tradeData = get_synced_conf()["trades"]
        else:
            self._get_new_trades()
            tradeData = get_synced_conf()["trades"]

        return not (tradeData == [] or tradeData[1] == [])

    def _make_trade(self, have, want):
        """
        Make a trade.
        :param tuple have: Pokémon available to trade.
        :param tuple want: Pokémon wanted for trade.
        """
        possiblefits = []
        f = self.f

        if f == "tags":
            deckmonlist = get_synced_conf()["tagmon_list"]
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
                no_pokemon()
                return
        else:
            deckmonlist = get_synced_conf()["pokemon_list"]
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
                no_pokemon()
                return
        for item in deckmonlist:
            if (
                item[0] == want[0]
                or (item[0].startswith("Eevee") and want[0] == "Eevee")
                and int(item[2]) >= 5
            ):
                possiblefits.append(item)
        if possiblefits == []:
            showInfo(
                "Sorry, you do not have the Pokemon needed to complete this trade.",
                parent=mw,
                title="Pokémanki",
            )
            return
        displaylist = []
        for item in possiblefits:
            deckname = mw.col.decks.name(item[1])
            if len(item) == 4:
                if item[0].startswith("Eevee"):
                    displaytext = "%s - Eevee (Level %s) from %s" % (
                        item[3],
                        int(item[2]),
                        deckname,
                    )
                else:
                    displaytext = "%s - %s (Level %s) from %s" % (
                        item[3],
                        item[0],
                        int(item[2]),
                        deckname,
                    )
            else:
                if item[0].startswith("Eevee"):
                    displaytext = "Eevee (Level %s) from %s" % (int(item[2]), deckname)
                else:
                    displaytext = "%s (Level %s) from %s" % (
                        item[0],
                        int(item[2]),
                        deckname,
                    )
            displaylist.append(displaytext)

        totallist = list(zip(possiblefits, displaylist))
        possiblepokemon = QWidget()
        inp, ok = QInputDialog.getItem(
            possiblepokemon,
            "Pokémanki",
            "Choose a Pokemon to trade for %s" % have[0],
            displaylist,
            0,
            False,
        )
        tradepokemon = []
        if ok and inp:
            for thing in totallist:
                if inp in thing:
                    tradepokemon = thing[0]
                    displaytext = inp
        if not tradepokemon:
            return

        confirmation = QMessageBox()
        confirmation.setWindowTitle("Pokémanki")
        confirmation.setText(
            "Are you sure you want to trade your %s for a %s" % (displaytext, have[0])
        )

        confirmation.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        confirmation.setDefaultButton(QMessageBox.StandardButton.No)
        result = confirmation.exec()
        if result == QMessageBox.StandardButton.Yes:
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
            save_synced_conf("pokemon_list", modifieddeckmonlist)
            self._trade_window.done(QDialog.Accepted)
            showInfo(
                f"You have traded your {displaytext} for a {have[0]}",
                parent=mw,
                title="Pokémanki",
            )

    def _trades_html(self):
        """
        Generate the html code for the trades window.
        :return: The html code.
        :rtype: str
        """
        # Header
        txt = '<h1 style="text-align: center;">Today\'s Trades</h1>'

        # Open trades container
        txt += '<div class="pk-td-container">'

        # Generate each of the trades
        for i in range(len(self.trades)):
            txt += self._trade_html(i)

        # Close trades container
        txt += "</div>"

        return txt

    def _trade_html(self, i):
        """
        Generate the html code for a trade.

        :param int i: Trade number.
        :return: Trade's html.
        :rtype: str
        """

        trade = "<script>" "function callTrade(n) { pycmd(n); }" "</script>"

        # Open trade container
        trade += '<div class="pk-td-trade">'

        ###########
        # Head info
        ###########
        trade += (
            '<div class="pk-td-trainer" style="margin-bottom: auto;">'
            f'<h2 style="text-align: center;"><b>Trainer {i + 1}</b></h2>'
            '<div class="pk-divider" style="margin-top: 10px;"></div>'
            "</div>"
        )

        ##########
        # Has
        ##########
        trade += (
            '<div class="pk-td-offer">'
            '<div class="pk-td-offer-txt">'
            '<span class="pk-td-offer-txt-title"><b>Has:</b></span>'
            f'<span class="pk-td-offer-txt-name"><b>{self.trades[i][0][0]}</b></span>'
            "</div>"
            f'<img src="pokemon_images/{self.trades[i][0][0]}.png" class="pk-td-offer-img"/>'
            "</div>"
        )

        ##########
        # Wants
        ##########
        trade += (
            '<div class="pk-td-offer">'
            '<div class="pk-td-offer-txt">'
            '<span class="pk-td-offer-txt-title"><b>Wants:</b></span>'
            f'<span class="pk-td-offer-txt-name"><b>{self.trades[i][1][0]}</b></span>'
            "</div>"
            f'<img src="pokemon_images/{self.trades[i][1][0]}.png" class="pk-td-offer-img"/>'
            "</div>"
        )

        ##########
        # Bottom
        ##########
        trade += (
            '<div class="pk-td-bottom">'
            '<div class="pk-divider" style="margin-bottom: 10px"></div>'
            f'<button class"pk-button" onclick="callTrade({i})">Trade</button>'
            "</div>"
        )

        # Close trade
        trade += "</div>"

        return trade


def get_pokemon_records():
    """
    Generate a list of all Pokémon based on the user's generation configuration.
    :return: List of pokemon records.
    :rtype: List
    """
    pokemon_records = []
    csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen1.csv"
    pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))

    if get_local_conf()["gen2"]:
        csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen2.csv"
        pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))

        if get_local_conf()["gen4_evolutions"]:
            csv_fpath = (
                currentdirname / "pokemon_evolutions" / "pokemon_gen1_plus2_plus4.csv"
            )
            pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
            csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen2_plus4.csv"
            pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
        else:
            csv_fpath = (
                currentdirname / "pokemon_evolutions" / "pokemon_gen1_plus2_no4.csv"
            )
            pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
            csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen2_no4.csv"
            pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
    else:
        if get_local_conf()["gen4_evolutions"]:
            # a lot of gen 4 evolutions that affect gen 1 also include gen 2 evolutions
            # so let's just include gen 2 for these evolution lines
            csv_fpath = (
                currentdirname / "pokemon_evolutions" / "pokemon_gen1_plus2_plus4.csv"
            )
            pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
        else:
            csv_fpath = (
                currentdirname / "pokemon_evolutions" / "pokemon_gen1_no2_no4.csv"
            )
            pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))

    if get_local_conf()["gen3"]:
        csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen3.csv"
        pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
    if get_local_conf()["gen4"]:
        csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen4.csv"
        pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))
    if get_local_conf()["gen5"]:
        csv_fpath = currentdirname / "pokemon_evolutions" / "pokemon_gen5.csv"
        pokemon_records.extend(pokemonLevelRangesFromCsv(csv_fpath))

    return pokemon_records


def pokemonLevelRangesFromCsv(csv_fpath):
    """
    Get the list of evolution level ranges for all Pokémon.
    :param str csv_fpath: Path of the csv containing the evolution list
    :return: List of pokemon ranges.
    :rtype: List
    """
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
