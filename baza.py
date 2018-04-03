import sqlite3 as sql

## crta a ne crtica
## format: naslov / autor; ostali. - mesto : izd., god. - str.
##              ibid. X izd. - god [[. - god ]; dr. izd.].
##              ibid. \[lat. izd.\] - X izd. - god. 
##              nasl. orig. : ...; prev. prema ...


# autori - _ID_, ime, ime_original (rucno)
# dela - _ID_, _ID_.autor, jezik, naslov, naslov originala, mesto izd.,
#        izadavac, godina, br. str., _ponovljeno izd._
#        (br. za skracen opis), pismo knjige (RAZMISLITI KAKO)


# posebna tabela za ispis
# autori - abecedno 
# naslovi - abecedno

# objekat za svaku knjigu i nesto poput linked list
