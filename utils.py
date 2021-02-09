from aqt import mw
from pathlib import Path
import json

# Find current directory
addon_dir = Path(__file__).parents[0]
currentdirname = addon_dir
# Assign Pokemon Image folder directory name
pkmnimgfolder = addon_dir / "pokemon_images"

profilename = mw.pm.name
profilefolder = Path(mw.pm.profileFolder())
mediafolder = Path(mw.col.media.dir())


def copy_directory(dir_addon: str, dir_anki: str):
    if not dir_anki:
        dir_anki = dir_addon
    fromdir = addon_dir / dir_addon
    todir = mediafolder / dir_anki
    if not fromdir.is_dir():
        return
    if todir.is_dir():
        shutil.copytree(fromdir, todir)
    else:
        distutils.dir_util.copy_tree(fromdir, todir)


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
    with open(file_path) as f:
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
