import tkinter as tk
from tkinter import ttk
import database
import language_file

# lista polja za autore, za svaki elemnet u toj listi pokrenuti for-loop za insert authori rezultat cuvati u listi

# insert_authors vraca INT!!!

# check input before pressing SUBMIT
# 0 - mixed, 1 - danski, 2 - norveski...


class Interface(tk.Tk):

    def __init__(self, master=None):
        tk.Tk.__init__(self)
        self.PADY = 3
        self.PADX = 20
        self.LANGUAGES = ["sk", "dan", "nor", "swe", "fin", "lap", "esk", "ice", "far"]
        self.TYPES = ["beletristika", "strucna", "narodna", "antologija"]
        self.main_frame = tk.Frame(self)
        self.main_frame.pack()
        for i in range(0, 10):
            self.main_frame.columnconfigure(i, weight=1)
            self.main_frame.rowconfigure(i, weight=1)
        self.x_frame = tk.Frame(self.main_frame)  # contains 3 entries
        self.x_frame.grid(row=8, column=1)
        self.y_frame = tk.Frame(self.main_frame)  # contains 3 entries
        self.y_frame.grid(row=9, column=1)
        self.create_menu()
        self.populate_frame()

    def create_menu(self):
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Bla", command=None)
        self.menu.add_cascade(label="File", menu=self.file_menu)

    def populate_frame(self):
        self.create_variables()
        self.create_labels()
        self.create_entries()
        self.create_buttons()

    def create_variables(self):
        self.language_var = tk.StringVar(self)
        self.language_var.set(self.LANGUAGES[0])
        self.type_var = tk.StringVar(self)
        self.type_var.set(self.TYPES[0])
        self.script_var = tk.StringVar(self)
        self.script_var.set("lat.")

    def create_labels(self):
        self.author_label = ttk.Label(self.main_frame, text="Autor:", anchor=tk.NW)
        self.author_label.grid(row=1, column=0, padx=self.PADX, pady=self.PADY, sticky=tk.NW)
        self.title_label = ttk.Label(self.main_frame, text="Naslov:", anchor=tk.NW)
        self.title_label.grid(row=2, column=0, padx=self.PADX, pady=self.PADY, sticky=tk.NW)
        self.others_label = ttk.Label(self.main_frame, text="Prvi pod. o odg.:", anchor=tk.NW)
        self.others_label.grid(row=4, column=0, padx=self.PADX, pady=self.PADY, sticky=tk.NW)
        self.language_label = ttk.Label(self.main_frame, text="Jezik:", anchor=tk.W)
        self.language_label.grid(row=2, column=2, padx=self.PADX, pady=self.PADY, sticky=tk.W)
        self.type_label = ttk.Label(self.main_frame, text="Tip knj.:", anchor=tk.W)
        self.type_label.grid(row=3, column=2, padx=self.PADX, pady=self.PADY, sticky=tk.W)
        self.o_title_label = ttk.Label(self.main_frame, text="Orig. nasl.:", anchor=tk.NW)
        self.o_title_label.grid(row=6, column=0, padx=self.PADX, pady=self.PADY, sticky=tk.NW)
        self.places_publishers_year = ttk.Label(self.main_frame, text="Mesto, izd. i god.:", anchor=tk.NW)
        self.places_publishers_year.grid(row=8, column=0, padx=self.PADX, pady=self.PADY, sticky=tk.NW)
        self.pages_script_label = ttk.Label(self.main_frame, text="Br. str. i pismo:", anchor=tk.NW)
        self.pages_script_label.grid(row=9, column=0, padx=self.PADX, pady=self.PADY, sticky=tk.NW)
        self.notes_label = ttk.Label(self.main_frame, text="Napomene:", anchor=tk.NW)
        self.notes_label.grid(row=10, column=0, padx=self.PADX, pady=self.PADY, sticky=tk.NW)
        """CREATE LABELS AND ENTRIES FOR OTHER AUTHORS"""
        self.other_authors_label = ttk.Label(self.main_frame, text="Drugi autori:", anchor=tk.NW)

    def create_entries(self):
        self.author_entry = ttk.Entry(self.main_frame, state=tk.DISABLED, width=40)
        self.author_entry.grid(row=1, column=1, padx=self.PADX - 10, pady=self.PADY)
        self.title_text = tk.Text(self.main_frame, width=30, height=2)
        self.title_text.grid(row=2, column=1, rowspan=2, padx=self.PADX - 10, pady=self.PADY)
        self.others_text = tk.Text(self.main_frame, width=30, height=2)  # author, translator, etc.
        self.others_text.grid(row=4, column=1, rowspan=2, padx=self.PADX - 10, pady=self.PADY)
        self.language_drop = ttk.OptionMenu(self.main_frame, self.language_var, self.LANGUAGES[0], *self.LANGUAGES)
        self.language_drop.grid(row=2, column=3, pady=self.PADY, sticky=tk.W)
        self.type_drop = ttk.OptionMenu(self.main_frame, self.type_var, *self.TYPES)
        self.type_drop.grid(row=3, column=3, pady=self.PADY, sticky=tk.W)
        self.o_title_text = tk.Text(self.main_frame, width=30, height=2)
        self.o_title_text.grid(row=6, column=1, rowspan=2, padx=self.PADX - 10, pady=self.PADY)
        self.places_entry = ttk.Entry(self.x_frame, width=13)
        self.places_entry.pack(side="left")
        self.publishers_entry = ttk.Entry(self.x_frame, width=13)
        self.publishers_entry.pack(side="left")
        self.year_entry = ttk.Entry(self.x_frame, width=13)
        self.year_entry.pack(side="left")
        self.pages_entry = ttk.Entry(self.y_frame)
        self.pages_entry.pack(side="left")
        self.script_entry = ttk.OptionMenu(self.y_frame, self.script_var, "lat.", *["ćir.", "lat."])
        self.script_entry.pack(side="left")
        self.notes_text = tk.Text(self.main_frame, width=30, height=2)
        self.notes_text.grid(row=10, column=1, rowspan=2, padx=self.PADX - 10, pady=self.PADY)
        self.other_authors_entry = ttk.Entry(self.main_frame)

    def create_buttons(self):
        self.select_author_button = ttk.Button(self.main_frame, text="Izaberi autora",
                                               command=self.select_author_window)
        self.select_author_button.grid(row=1, column=2)
        self.submit_button = ttk.Button(self.main_frame, text="Unesi", command=self.submit)
        self.submit_button.grid(row=10, column=5)

    def submit(self):
        # database.insert_book()
        print(self.language_var.get())
        print("Works!")

    def select_author_window(self):
        self.tp_window = tk.Toplevel(self.master)
        self.tp_window.title("Select author")
        self.frame = tk.Frame(self.tp_window)
        self.frame.pack()
        self.column_names = ["ID", "Prezime", "Ime", "Pseudonim"]
        self.tw = ttk.Treeview(self.frame, column=self.column_names, show='headings')
        self.tw.pack(side=tk.TOP)
        self.tw.column(0, minwidth=40, width=40)
        self.add_new_author_button = ttk.Button(self.frame, text="Add new", command=self.add_new_author_window)
        self.add_new_author_button.pack(side=tk.LEFT)
        self.saw_select_author_button = ttk.Button(self.frame, text="Izaberi autora", command=self.select_from_treeview)
        self.saw_select_author_button.pack(side=tk.RIGHT)
        for i in self.column_names:
            self.tw.heading(i, text=i)
        self.populate_treeview()

    def populate_treeview(self):
        self.clear_treeview()
        for d in database.retrieve_authors():
            self.tw.insert('', tk.END, values=(d[0], d[1], d[2], d[3]))

    def clear_treeview(self):
        for i in self.tw.get_children():
            self.tw.delete(i)

    def select_from_treeview(self):
        try:
            self.author_entry.config(state=tk.ACTIVE)
            self.author_entry.delete(0, "end")
            print(self.tw.item(self.tw.focus())["values"])  # index of the selected author
            index, surname, name, pseu = self.tw.item(self.tw.focus())["values"]
            self.author_entry.insert(0, surname + ", " + name + " (" + pseu + ")")
            self.author_entry.config(state=tk.DISABLED)
            self.tp_window.destroy()
        except:
            # if no author is selected
            pass

    def add_new_author_window(self):
        self.tp_add_new = tk.Toplevel(self.tp_window)
        self.tp_add_new.title("Add new author")
        self._frame = tk.Frame(self.tp_add_new)
        self._frame.grid()
        for i in range(0, 4):
            self._frame.columnconfigure(i, weight=1)
            self._frame.rowconfigure(i, weight=1)
        self.anaw_surname_label = ttk.Label(self._frame, text="Surname: ", anchor=tk.W)
        self.anaw_surname_entry = ttk.Entry(self._frame, width=40)
        self.anaw_name_label = ttk.Label(self._frame, text="Name: ", anchor=tk.W)
        self.anaw_name_entry = ttk.Entry(self._frame, width=40)
        self.anaw_pseudonym_label = ttk.Label(self._frame, text="Pseudonym: ", anchor=tk.W)
        self.anaw_pseudonym_entry = ttk.Entry(self._frame, width=40)
        self.anaw_surname_label.grid(row=0, column=0, padx=10)
        self.anaw_surname_entry.grid(row=0, column=1, padx=10)
        self.anaw_name_label.grid(row=1, column=0, padx=10)
        self.anaw_name_entry.grid(row=1, column=1, padx=10)
        self.anaw_pseudonym_label.grid(row=2, column=0, padx=10)
        self.anaw_pseudonym_entry.grid(row=2, column=1, padx=10)
        self.anaw_submit = ttk.Button(self._frame, text="Unesi", command=self.add_new_author_to_db, width=20)
        self.anaw_submit.grid(row=3, column=3)

    def add_new_author_to_db(self):
        print("Author added!")
        database.insert_authors(self.anaw_surname_entry.get(), self.anaw_name_entry.get(),
                                self.anaw_pseudonym_entry.get())
        self.populate_treeview()
        self.tp_add_new.destroy()


database.create()
app = Interface()
app.mainloop()
