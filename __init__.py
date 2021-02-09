# Copyright 2019 Siven Chinniah

# JK please feel free to use this however you would like.

from aqt import gui_hooks


def startup():
    from . import main


gui_hooks.profile_did_open.append(startup)
