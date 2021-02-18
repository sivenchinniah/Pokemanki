import json
import shutil
import distutils.dir_util
from pathlib import Path
from typing import List, Union

from aqt import mw
from aqt.qt import *

config = mw.addonManager.getConfig(__name__)

# Find current directory
addon_dir = Path(__file__).parents[0]
currentdirname = addon_dir
# Assign Pokemon Image folder directory name
pkmnimgfolder = addon_dir / "pokemon_images"

profilename = mw.pm.name
profilefolder = Path(mw.pm.profileFolder())
mediafolder = Path(mw.col.media.dir())


def copy_directory(dir_addon: str, dir_anki: str = None):
    if not dir_anki:
        dir_anki = dir_addon
    fromdir = addon_dir / dir_addon
    todir = mediafolder / dir_anki
    if not fromdir.is_dir():
        return
    if not todir.is_dir():
        shutil.copytree(str(fromdir), str(todir))
    else:
        distutils.dir_util.copy_tree(str(fromdir), str(todir))


def set_default(file_name: str, default):
    if not get_json(file_name, None):
        write_json(file_name, default)


def get_json(file_name: str, default=None):
    file_path = mediafolder / file_name
    value = None
    if file_path.exists():
        with open(file_path, "r") as f:
            value = json.load(f)
    if not value:  # includes json with falsy value
        value = default
    return value


def write_json(file_name: str, value):
    file_path = mediafolder / file_name
    with open(file_path, "w") as f:
        json.dump(value, f)


def no_pokemon():
    nopokemon = QMessageBox()
    nopokemon.setWindowTitle("Pokemanki")
    nopokemon.setText(
        "Please open the Stats window to get your Pokémon.")
    nopokemon.exec_()


def get_pokemons():
    f = get_json("_decksortags.json", "")
    if f:
        pokemons = get_json("_tagmon.json", None)
    else:
        pokemons = get_json("_pokemanki.json", None)
    if pokemons is None:
        no_pokemon()
        return (None, None)
    # patch - remove deplicates from pokemon json
    # TODO: fix the code duplicating pokemon
    ids = []
    ret_pokemons = []
    for pokemon in pokemons:
        if pokemon[1] not in ids:  # only one pokemon per id
            ret_pokemons.append(pokemon)
            ids.append(pokemon[1])
    return (ret_pokemons, f)


def line(
    i: List[str], a: str, b: Union[int, str], bold: bool = True
) -> None:
    # T: Symbols separating first and second column in a statistics table. Eg in "Total:    3 reviews".
    colon = ":"
    if bold:
        i.append(
            ("<tr><td width=200 align=right>%s%s</td><td><b>%s</b></td></tr>")
            % (a, colon, b)
        )
    else:
        i.append(
            ("<tr><td width=200 align=right>%s%s</td><td>%s</td></tr>")
            % (a, colon, b)
        )


def lineTbl(i: List[str]) -> str:
    return "<table width=400>" + "".join(i) + "</table>"


def table_image_html(image_name, title=None):
    if title is None:
        title = image_name
    image_el = ""
    if image_name:
        image_el = '<img src="/pokemon_images/{}.png" title="{}">'.format(
            image_name, title)
    return '<td height=250 width=250 align=center>{}</td>'.format(image_el)


def table_text_html(main_text, sub_text="", bold=False):
    bolded = "{}".format(main_text)
    if bold:
        bolded = "<b>{}</b>{}".format(main_text, sub_text)
    return '<td height=30 width=250 align=center>{}</td>'.format(bolded)
