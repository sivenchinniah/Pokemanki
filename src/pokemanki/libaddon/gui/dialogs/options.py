# -*- coding: utf-8 -*-

# Libaddon for Anki
#
# Copyright (C) 2018-2019  Aristotelis P. <https//glutanimate.com/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the license file that accompanied this program.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# NOTE: This program is subject to certain additional terms pursuant to
# Section 7 of the GNU Affero General Public License.  You should have
# received a copy of these additional terms immediately following the
# terms and conditions of the GNU Affero General Public License that
# accompanied this program.
#
# If not, please request a copy through one of the means of contact
# listed here: <https://glutanimate.com/contact/>.
#
# Any modifications to this file must keep this entire header intact.

"""
Main options dialog
"""

from PyQt5.QtCore import Qt, QUrl, QEvent
from PyQt5.QtWidgets import QApplication, QWidget

from aqt.utils import openLink, tooltip

from ..._wrappers.typing import Optional, Union, Any
from ..._wrappers.types import ModuleType

from ...addon import ADDON
from ...anki import ANKI
from ...anki.config.manager import ConfigManager

from ...util.logging import (
    toggleDebugging,
    isDebuggingOn,
    getLatestLog,
    openLog,
    clearLog,
)

from ..content.about import getAboutString
from ..helpers.label_formatter import formatLabels

from .mapped import MappedDialog


class OptionsDialog(MappedDialog):
    def __init__(
        self,
        mapped_widgets: Union[list, tuple],
        config: ConfigManager,
        form_module: Optional[ModuleType] = None,
        parent: Optional[QWidget] = None,
        **kwargs
    ):
        """
        Creates an options dialog with the provided Qt form and populates its
        widgets from a ConfigManager config object.

        Arguments:
            mapped_widgets {sequence} -- A list or tuple of mappings between
                                         widget names, config value names, and
                                         special methods to act as mediators
                                         (see MappedDialog docstring for specs)
            config {ConfigManager} -- ConfigManager object providing access to
                                      add-on config values

        Keyword Arguments:
            form_module {PyQt form module} -- Dialog form module generated
                                              through pyuic (default: {None})
            parent {QWidget} -- Parent Qt widget (default: {None})


        """
        # Mediator methods defined in mapped_widgets might need access to
        # certain instance attributes. As super().__init__ instantiates
        # all widget values it is important that we set these attributes
        # beforehand:
        self.config = config
        super().__init__(
            mapped_widgets,
            self.config.all,
            self.config.defaults,
            form_module=form_module,
            parent=parent,
        )
        # Instance methods that modify the initialized UI should either be
        # called from self._setupUI or from here

    # Static widget setup

    def _setupUI(self) -> None:
        formatLabels(self, self._linkHandler)
        self._setupAbout()
        self._setupLabDebug()

        if ANKI.PLATFORM != "mac":
            return

        # Decrease tab margins on macOS
        tab_widget = getattr(self.form, "tabWidget", None)
        if not tab_widget:
            return
        for idx in range(tab_widget.count()):
            tab = tab_widget.widget(idx)
            if not tab:
                continue
            layout = tab.layout()
            if not layout:
                continue
            layout.setContentsMargins(3, 3, 3, 3)

    def _setupAbout(self) -> None:
        """
        Fill out 'about' widget
        """
        if hasattr(self.form, "htmlAbout"):
            about_string = getAboutString(showDebug=True)
            self.form.htmlAbout.setHtml(about_string)
            self.form.htmlAbout.setOpenLinks(False)
            self.form.htmlAbout.anchorClicked.connect(self._linkHandler)

    def _setupLabDebug(self) -> None:
        label = getattr(self.form, "labDebug", None)
        if not label:
            return
        if isDebuggingOn():
            label.setText("<span style='color:#ff0000;'><b>DEBUG ACTIVE</b></span>")
        else:
            label.setText("")

    # Events

    def keyPressEvent(self, evt: QEvent) -> None:
        """
        Prevent accidentally closing dialog when editing complex widgets
        by ignoring Return and Escape
        """
        if evt.key() == Qt.Key_Enter or evt.key() == Qt.Key_Return:
            return evt.accept()
        super().keyPressEvent(evt)

    def _setupEvents(self) -> None:
        super()._setupEvents()
        for name, link in ADDON.LINKS.items():
            btn_widget = getattr(self.form, "btn" + name.capitalize(), None)
            if not btn_widget:
                continue
            btn_widget.clicked.connect(lambda _, link=link: openLink(link))

    # Link actions

    def _linkHandler(self, url: str) -> Optional[Any]:
        """Support for binding custom actions to text links"""
        if isinstance(url, QUrl):
            url = url.toString()
        if not url.startswith("action://"):
            return openLink(url)
        protocol, cmd = url.split("://")
        if cmd == "debug-toggle":
            self._toggleDebugging()
        elif cmd == "debug-open":
            self._openDebuglog()
        elif cmd == "debug-copy":
            self._copyDebuglog()
        elif cmd == "debug-clear":
            self._clearDebuglog()
        elif cmd == "changelog":
            self._openChangelog()

    def _toggleDebugging(self) -> None:
        if toggleDebugging():
            msg = "enabled"
        else:
            msg = "disabled"
        tooltip("Debugging {msg}".format(msg=msg))
        self._setupLabDebug()

    def _copyDebuglog(self) -> Optional[bool]:
        log = getLatestLog()
        if log is False:
            tooltip("No debug log has been recorded, yet")
            return False
        QApplication.clipboard().setText(log)
        tooltip("Copied to clipboard")

    def _openDebuglog(self) -> bool:
        ret = openLog()
        if ret is False:
            tooltip("No debug log has been recorded, yet")
            return False
        return ret

    def _openChangelog(self) -> None:
        changelog = ADDON.LINKS.get("changelog")
        if not changelog:
            return
        openLink(changelog)

    def _clearDebuglog(self) -> Optional[bool]:
        ret = clearLog()
        if ret is False:
            tooltip("No debug log has been recorded, yet")
            return False
        tooltip("Debug log cleared")

    # Exit handling

    def _onAccept(self) -> None:
        """Executed only if dialog confirmed"""
        self.getData()  # updates self.config in place
        self.config.save()
        super()._onAccept()
