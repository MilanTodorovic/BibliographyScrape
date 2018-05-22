import sqlite3 as sql
import typing


# crta a ne crtica
# PSEUDONIM
# [Pseudonim za IME]
# format: naslov / autor; ostali. - mesto : izd., god. - str.
#              ibid. X izd. - god [[. - god ]; dr. izd.].
#              ibid. \[lat. izd.\] - X izd. - god.
#              nasl. orig. : ...; prev. prema ...
#              [Sadrzi: ....]


# autori - _ROWID_, ime_original, pseudonim
# dela - _ROWID_, _ROWID_.autor, jezik, naslov, naslov originala, mesto izd.,
#        izadavac, godina, br. str., _ponovljeno izd._
#        (br. za skracen opis), pismo knjige (RAZMISLITI KAKO),
#       strucna/lepa/narodna knj/ANTOLOGIJA., vise autora za jednu knj.


# posebna tabela za ispis
# autori - abecedno
# naslovi - abecedno


def create():
    with sql.connect("knjige.sqlite") as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS authors(surname TEXT NOT NULL, name TEXT NOT NULL, pseudonym TEXT"
                  ", PRIMARY KEY(surname, name, pseudonym));")
        # lang: rowid
        c.execute("CREATE TABLE IF NOT EXISTS languages(language TEXT)")
        c.executemany("INSERT OR IGNORE INTO languages VALUES(?)", [("sk",), ("dan",), ("nor",), ("swe",), ("fin",),
                                                                    ("lap",), ("esk",), ("ice",), ("far",)])
        # type of literature: 0 - anthology, 1 - folklore, 2 - belletristic, 3 - monography
        c.execute("CREATE TABLE IF NOT EXISTS literature(type TEXT)")
        c.executemany("INSERT OR IGNORE INTO literature VALUES(?)", [("anthology",), ("folklore",), ("belletristic",),
                                                                     ("monography",)])
        # script: 0 - lat., 1 - cir.
        # types: rowid from literature table
        # republished - manually set to 1 if needed
        # o_authors - semicolon separated TEXT of rowids
        c.execute("CREATE TABLE IF NOT EXISTS books(author TEXT, others TEXT, lang INT NOT NULL, title TEXT NOT NULL, "
                  "o_title TEXT, trans_title TEXT, places TEXT, publishers TEXT, year TEXT, pages TEXT, republished INT, "
                  "script INT NOT NULL, type INT NOT NULL, o_authors TEXT, notes TEXT);")
        c.close()
        conn.commit()


def insert_authors(surname: str, name: str, pseudonym: str) -> int:
    """All parameters must be strings
    Return: rowid for further connecting"""

    for para in ((surname, "surname"), (name, "name"), (pseudonym, "pseudonym")):
        assert type(para[0]) is str, "Parameter is not of type STRING: {} - {}".format(para[1], para[0])

    with sql.connect("knjige.sqlite") as conn:
        c = conn.cursor()
        # check if exists
        res = c.execute("SELECT _rowid_ FROM authors WHERE surname=? AND name=? AND pseudonym=?;",
                        (surname, name, pseudonym)).fetchone()
        if res:
            c.close()
            return res[0]
        else:
            # create entries
            if surname or name or pseudonym:
                c.execute("INSERT OR IGNORE INTO authors(surname, name, pseudonym) VALUES(?,?,?);",
                          (surname, name, pseudonym))
                rowid = c.lastrowid
                conn.commit()
                c.close()
                return rowid
            else:
                return -1


def retrieve_authors(**kwargs) -> typing.List[typing.Tuple[int, str, str, str]]:
    """Return a list of authors or just one if parameters supplied.
    kwargs: surname, name, pseudonym"""
    with sql.connect("knjige.sqlite") as conn:
        c = conn.cursor()
        if kwargs:
            query = " AND ".join("{}='{}'".format(k, v) for (k, v) in kwargs.items())
            lst = c.execute("SELECT _rowid_, surname, name, pseudonym FROM authors WHERE {};".format(query)).fetchall()
        else:
            lst = c.execute("SELECT _rowid_, surname, name, pseudonym FROM authors;").fetchall()
        c.close()
        return lst


def insert_book(author: str, others: str, o_authors: str, lang: int, title: str, o_title: str, trans_title: str,
                place: str, publisher: str, year: str, pages: str, script: int, _type: int, notes: str,
                republished: int = 0) -> int:
    """All parameters except script and _type are of type STRING.
    authors - may be NULL/empty
    lang - rowid from languages table
    year - [s.a.]
    pages - XI, 150 str. / 1500-1670 str.
    script - 0-lat., 1-cir.
    _type - 0 - anthology, 1 - folklore, 2 - belletristic, 3 - monography
    republished - defaults to 0
    Return: rowid for editing"""

    for para in ((o_authors, "o_authors"), (author, "author"), (others, "other_authors"), (title, "title"),
                 (o_title, "o_title"), (trans_title, "rans_title"), (place, "places"), (publisher, "publishers"),
                 (year, "year"), (pages, "pages"), (notes, "notes")):
        assert type(para[0]) is str, "Parameter is not of type STRING: {} - {}".format(para[1], para[0])

    for para in ((lang, "lang"), (script, "script"), (_type, "_type")):
        assert type(para[0]) is int, "Parameter is not of type INT: {} - {}".format(para[1], para[0])

    with sql.connect("knjige.sqlite") as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO books(author, others, lang, title, o_title, trans_title, places, publishers, year, pages, "
            "script, type, o_authors, republished, notes) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
            (author, others, lang, title, o_title, trans_title, place, publisher, year, pages, script, _type,
             o_authors, republished, notes))
        rowid = c.lastrowid
        c.close()
        conn.commit()
        return rowid


def retrieve_book(**kwargs) -> typing.Tuple:
    query = " AND ".join("{}={}".format(k, v) for (k, v) in kwargs.items())
    with sql.connect("knjige.sqlite") as conn:
        c = conn.cursor()
        _id = c.execute("SELECT * FROM books WHERE {};".format(query)).fetchone()
        c.close()
        return _id


def list_all_books() -> typing.List[typing.Tuple[str, str, int, str, str, str, str, str, str, int, int, int, str]]:
    with sql.connect("knjige.sqlite") as conn:
        c = conn.cursor()
        _id = c.execute("SELECT * FROM books;").fetchall()
        c.close()
        return _id
