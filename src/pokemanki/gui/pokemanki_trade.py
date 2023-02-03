# -*- coding: utf-8 -*-

# Pokémanki
# Copyright (C) 2022 Exkywor and zjosua

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import ctypes
import platform

from aqt import QDialog
from aqt.webview import AnkiWebView
from PyQt6 import QtCore, QtWidgets

from .forms.qt6 import pokemanki_trade


class TradeWindow(QDialog):
    def __init__(self, parentObj, mw):
        super().__init__()
        self.dialog = pokemanki_trade.Ui_Dialog()
        self.dialog.setupUi(self)
        self.setupUi(parentObj, mw)

    def setupUi(self, parent, mw):
        self.dialog.webEngineView = AnkiWebView(parent=self, title="pokémanki trades")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.dialog.webEngineView.sizePolicy().hasHeightForWidth()
        )
        self.dialog.webEngineView.setSizePolicy(sizePolicy)
        self.dialog.webEngineView.setObjectName("webEngineView")
        self.dialog.verticalLayout_2.addWidget(self.dialog.webEngineView)

        self.dialog.webEngineView.set_bridge_command(parent.on_bridge_cmd, parent)

        # Set in the middle of the screen
        if platform.system() == "Windows":
            user32 = ctypes.windll.user32
            posX = int(user32.GetSystemMetrics(0) / 2 - self.width() / 2)
            posY = int(user32.GetSystemMetrics(1) / 2 - self.height() / 2)
        else:
            posX = int(mw.frameGeometry().width() / 2 - self.width() / 2)
            posY = int(mw.frameGeometry().height() / 2 - self.height() / 2)

        self.setGeometry(posX, posY, self.width(), self.height())

    def setup_trades(self, trades):
        """Set up the web view's html.

        :param list trades: List of trades to display
        """

        self.dialog.webEngineView.stdHtml(
            body=_trades_html(trades),
            css=["/pokemanki_css/view_trade.css", "/pokemanki_css/main.css"],
            context=self,
        )

    def open_trades(self, trades):
        """Set up the web view's html and opens the trade dialog.

        :param list trades: List of trades to display
        """

        self.setup_trades(trades)
        self.open()

    def finished_trade(self):
        self.done(QDialog.DialogCode.Accepted)


def _trades_html(trades):
    """Generate the html code for the trades window.

    :param list trades: List of trades to display
    :return: The html code.
    :rtype: str
    """

    # Write trade function
    txt = "<script>" "function callTrade(n) { pycmd(n); }" "</script>"

    # Open trades container
    txt += '<div class="pk-td-container">'

    # Generate each of the trades
    for i in range(len(trades)):
        txt += _trade_html(i, trades)

    # Close trades container
    txt += "</div>"

    return txt


def _trade_html(i, trades):
    """Generate the html code for a trade.

    :param int i: Trade number.
    :param list trades: List of trades to display
    :return: Trade's html.
    :rtype: str
    """

    # Open trade container
    trade = '<div class="pk-td-trade">'

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
        f'<span class="pk-td-offer-txt-name"><b>{trades[i][0][0]}</b></span>'
        "</div>"
        f'<img src="pokemon_images/{trades[i][0][0]}.png" class="pk-td-offer-img"/>'
        "</div>"
    )

    ##########
    # Wants
    ##########
    trade += (
        '<div class="pk-td-offer">'
        '<div class="pk-td-offer-txt">'
        '<span class="pk-td-offer-txt-title"><b>Wants:</b></span>'
        f'<span class="pk-td-offer-txt-name"><b>{trades[i][1][0]}</b></span>'
        "</div>"
        f'<img src="pokemon_images/{trades[i][1][0]}.png" class="pk-td-offer-img"/>'
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
