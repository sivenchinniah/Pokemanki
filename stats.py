from aqt import mw
from anki.utils import ids2str

from .utils import *


def cardIdsFromDeckIds(queryDb, deckIds):
    query = "select id from cards where did in {}".format(ids2str(deckIds))
    cardIds = [i[0] for i in queryDb.all(query)]
    return cardIds


def cardInterval(queryDb, cid):
    revLogIvl = queryDb.scalar(
        "select ivl from revlog where cid = %s "
        "order by id desc limit 1 offset 0" % cid)
    ctype = queryDb.scalar(
        "select type from cards where id = %s "
        "order by id desc limit 1 offset 0" % cid)

    # card interval is "New"
    if ctype == 0:
        ivl = 0
    elif revLogIvl is None:
        ivl = 0
    elif revLogIvl < 0:
        # Anki represents "learning" card review log intervals as negative minutes
        # So, convert to days
        ivl = revLogIvl * -1 / 60 / 1440
    else:
        ivl = revLogIvl

    return ivl


def DeckStats():
    "Retrieve id and ivl for each card in a single deck"
    # result = self.col.db.all("""select id, ivl from cards where did in %s""" %
    #             ids2str(self.col.decks.active()))
    activeDeckIds = mw.col.decks.active()
    cardIds = cardIdsFromDeckIds(mw.col.db, activeDeckIds)

    result = []
    for cid in cardIds:
        ivl = cardInterval(mw.col.db, cid)
        result.append((cid, ivl))

    return result


def MultiStats():
    "Retrieve id and ivl for each subdeck that does not have subdecks itself"
    # Get list of subdecks
    if mw.col.stats().wholeCollection:
        # Get results for all subdecks in collection
        alldecks = mw.col.decks.allIds()
        # Determine which subdecks do not have their own subdecks
        nograndchildren = []
        for item in alldecks:
            if len(mw.col.decks.children(int(item))) == 0 and item != "1":
                nograndchildren.append(int(item))
    else:
        # Get results only for all subdecks of selected deck
        children = mw.col.decks.children(mw.col.decks.active()[0])
        childlist = []
        for item in children:
            childlist.append(item[1])
        # Determine which subdecks do not have their own subdecks
        nograndchildren = []
        for item in childlist:
            if len(mw.col.decks.children(item)) == 0:
                nograndchildren.append(item)
    resultlist = []
    # Find results for each card in these decks
    for item in nograndchildren:
        # result = self.col.db.all("""select id, ivl from cards where did == %s""" % item)

        # cardIds = self.col.db.all("""select id from cards where did == %s""" % item)
        cardIds = cardIdsFromDeckIds(mw.col.db, [item])

        result = []
        for cid in cardIds:
            ivl = cardInterval(mw.col.db, cid)
            result.append((cid, ivl))

        resultlist.append(result)
    # Zip the deck ids with the results
    nograndchildresults = list(zip(nograndchildren, resultlist))

    return nograndchildresults


def TagStats():
    "Returns List[[tag_name, card_id, card_interval], ...]"
    savedtags = get_json("_tags.json", [])
    resultlist = []
    for item in savedtags:
        result = mw.col.db.all(
            "select c.id, c.ivl from cards c, notes n where c.nid = n.id and n.tags LIKE '%" + item + "%'")
        resultlist.append(result)
    results = list(zip(savedtags, resultlist))
    return results
