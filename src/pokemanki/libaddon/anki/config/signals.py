from PyQt5.QtCore import pyqtSignal, QObject


class ConfigSignals(QObject):
    initialized = pyqtSignal()
    saved = pyqtSignal()
    loaded = pyqtSignal()
    reset = pyqtSignal()
    deleted = pyqtSignal()
    unloaded = pyqtSignal()
