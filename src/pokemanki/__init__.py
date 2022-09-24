from aqt import gui_hooks
from aqt.utils import showWarning


opened = False


def startup():
    global opened
    if opened:
        warning_text = "\n".join((
            "Pokémanki does not support opening a second profile in one session.",
            "Please close Anki and reopen it again to the desired profile.",
            "Pokémanki may behave strangely"
        ))
        showWarning(warning_text, title="Pokémanki won't function properly")
        return

    opened = True
    from . import main


gui_hooks.profile_did_open.append(startup)
