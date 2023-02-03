from abc import abstractmethod, abstractproperty
from collections.abc import MutableMapping

from .signals import ConfigSignals


class ConfigInterface(MutableMapping):

    signals: ConfigSignals

    @abstractproperty
    def ready(self) -> bool:
        """Base storage object ready for I/O
        
        Returns:
            bool -- whether base storage object is ready
        """
        return False

    @abstractproperty
    def loaded(self) -> bool:
        """Config loaded from base storage object

        Returns:
            bool -- whether config is loaded in
        """
        return False

    @abstractproperty
    def dirty(self) -> bool:
        """Config representation diverges from base storage object

        Returns:
            bool -- whether config diverges from base storage object
        """
        return False

    @abstractmethod
    def initialize(self) -> bool:
        # should emit signals.initialized
        return

    @abstractmethod
    def load(self) -> bool:
        # should emit signals.loaded
        return

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def defaults(self) -> dict:
        return

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def delete(self):
        pass
