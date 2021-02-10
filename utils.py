from aqt import mw
from pathlib import Path
import json
import shutil
import distutils.dir_util
from typing import List, Union


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


def set_default(path: str, default=None):
    if not (mediafolder / path).is_file():
        with open(mediafolder / path, "w") as f:
            json.dump(default, f)


def get_json(file_name: str, default=None):
    file_path = mediafolder / file_name
    if file_path.exists():
        return json.load(open(file_path))
    else:
        return default


def write_json(file_name: str, value={}):
    file_path = mediafolder / file_name
    with open(file_path, "w") as f:
        json.dump(value, f)


def media_exists(file_name: str):
    return (mediafolder / file_name).exists()


def media(file_name: str):
    return mediafolder / file_name


def get_pokemon():
    f = get_json("_decksortags.json", None)
    if f:
        pokemon = get_json("_tagmon.json")
    else:
        pokemon = get_json("_pokemanki.json")
    return pokemon


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
