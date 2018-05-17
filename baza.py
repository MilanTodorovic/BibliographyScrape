import sqlite3 as sql

## crta a ne crtica
## PSEUDONIM
## [Pseudonim za IME]
## format: naslov / autor; ostali. - mesto : izd., god. - str.
##              ibid. X izd. - god [[. - god ]; dr. izd.].
##              ibid. \[lat. izd.\] - X izd. - god. 
##              nasl. orig. : ...; prev. prema ...


# autori - _ID_, ime, ime_original (rucno), pseudonim
# dela - _ID_, _ID_.autor, jezik, naslov, naslov originala, mesto izd.,
#        izadavac, godina, br. str., _ponovljeno izd._
#        (br. za skracen opis), pismo knjige (RAZMISLITI KAKO),
#       strucna/lepa/narodna knj/ANTOLOGIJA., vise autora za jednu knj.


# posebna tabela za ispis
# autori - abecedno 
# naslovi - abecedno


def create():
    with sql.connect("knjige.sqlite") as conn:
        c = conn.cursor()
        # conn is used to connect the two author tables
        c.execute("CREATE TABLE IF NOT EXISTS authors(surname TEXT NOT NULL, name TEXT NOT NULL, pseudonym TEXT NOT NULL"
                  ", conn INT, PRIMARY KEY(surname, name, pseudonym))")
        c.execute("CREATE TABLE IF NOT EXISTS authors_original(surname TEXT NOT NULL, name TEXT NOT NULL, "
                  "pseudonym TEXT NOT NULL, conn INT, PRIMARY KEY(surname, name, pseudonym))")
        # authors separated with semicolons
        # script: 0 - lat., 1 - cir.
        # types: 0 - anthology, 1 - folklore, 2 - belletristic, 3 - monography
        # republished - rowid of the original book
        c.execute("CREATE TABLE IF NOT EXISTS books(authors TEXT, lang TEXT, title TEXT, o_title TEXT, place TEXT, "
                  "publisher TEXT, year TEXT, pages TEXT, republished INT, script INT, type INT)")
        c.close()
        conn.commit()

def insert_authors(surname: str, name: str, pseudonym: str, o_surname: str, o_name: str, o_pseudonym: str) -> int:
    """All parameters must be strings
    Return: rowid for further connecting"""

    for para in ((surname, "surname"), (name, "name"), (pseudonym, "pseudonym"),
                     (o_surname, "o_surname"), (o_name, "o_name"), (o_pseudonym, "o_pseudonym")):
        assert type(para[0]) is str, "Parameter is not of type STRING: {} - {}".format(para[1], para[0])

    with sql.connect("knjige.sqlite") as conn:
        _id, __id = None, None
        c = conn.cursor()
        # check if exists
        res = c.execute("SELECT _rowid_ FROM authors WHERE surname=? AND name=?", (surname, name)).fetchone()
        o_res = c.execute("SELECT _rowid_ FROM authors WHERE surname=? AND name=?", (o_surname, o_name)).fetchone()
        if res or o_res:
            return res[0] if res else o_res[0]
        else:
            # create entries
            if surname or name or pseudonym:
                c.execute("INSERT OR IGNORE INTO authors(surname, name, pseudonym) VALUES(?,?,?)", (surname, name, pseudonym))
                _id = c.lastrowid
            if o_surname or o_name or o_pseudonym:
                c.execute("INSERT OR IGNORE INTO authors_original VALUES(?,?,?)", (o_surname, o_name, o_pseudonym))
                __id = c.lastrowid
            conn.commit()
            # connect entries or create placeholders
            if _id:
                if __id:
                    c.execute("INSERT INTO authors_original(conn) VALUES(?) WHERE _rowid_=?",
                              (_id, __id))
                else:
                    c.execute("INSERT INTO authors_original(conn) VALUES(?)",
                              (_id,))
            if __id:
                if _id:
                    c.execute("INSERT INTO authors(conn) VALUES(?) WHERE _rowid_=?", (_id, __id))
                else:
                    c.execute("INSERT INTO authors(conn) VALUES(?)", (_id,))
            conn.commit()
            c.close()
            return __id if __id else _id

def insert_book(authors: str, lang: str, title: str, o_title: str, place: str, publisher: str, year: str, pages: str,
                script: int, _type: int) -> int:
    """All parameters except script and _type are of type string.
    authors - may be NULL/empty
    year - [s.a.]
    pages - XI, 150 str. / 1500-1670 str.
    script - 0-lat., 1-cir.
    _type - 0 - anthology, 1 - folklore, 2 - belletristic, 3 - monography
    Return: rowid for editing"""

    for para in ((authors, "authors"), (lang, "lang"), (title, "title"),
                     (o_title, "o_title"), (place, "place"), (publisher, "publisher"), (year, "year"), (pages, "pages")):
        assert type(para[0]) is str, "Parameter is not of type STRING: {} - {}".format(para[1], para[0])

    for para in ((script, "script"), (_type, "_type")):
        assert type(para[0]) is int, "Parameter is not of type INT: {} - {}".format(para[1], para[0])

    with sql.connect("knjige.sqlite") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO books(authors, lang, title, o_title, place, published, year, pages, script, _type) VALUES"
                  "(?,?,?,?,?,?,?,?,?,?)", (authors, lang, title, o_title, place, publisher, year, pages, script, _type))
        _id = c.lastrowid
        c.close()
        conn.commit()
        return _id

def retrieve_book(**kwargs):
    # " ".join("{}={}".format(k,v) for (k,v) in d.items())
    query = ""
    for k,v in kwargs:
        query += k + "=" + v + "AND "
    with sql.connect("knjige.sqlite") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM books WHERE ?", (,))
        c.close()
