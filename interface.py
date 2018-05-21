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
        self.main_frame = tk.Frame(self)
        self.main_frame.pack()
        for i in range(0,10):
            self.main_frame.columnconfigure(i, weight=1)
            self.main_frame.rowconfigure(i, weight=1)
        self.create_menu()
        self.populate_frame()

    def create_menu(self):
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Bla", command=None)
        self.menu.add_cascade(label="File", menu=self.file_menu)

    def populate_frame(self):
        self.create_labels()
        self.create_entries()
        self.select_author_button = ttk.Button(self.main_frame, text="Izaberi autora", command=self.select_author_window)
        self.select_author_button.grid(row=1, column=3)
        self.submit_button = ttk.Button(self.main_frame, text="Unesi", command=self.submit)
        self.submit_button.grid(row=9, column=5)

    def create_labels(self):
        self.label_author = ttk.Label(self.main_frame, text="Autor: ", anchor=tk.W)
        self.label_author.grid(row=1, column=0, padx=20)

    def create_entries(self):
        self.entry_author = ttk.Entry(self.main_frame, state=tk.DISABLED, width=40)
        self.entry_author.grid(row=1, column=2, padx=10)

    def submit(self):
        print("Works!")

    def select_author_window(self):
        self.saw = tk.Toplevel(self)
        self.saw.title("Select author")
        self.saw_frame = tk.Frame(self.saw)
        self.saw_frame.pack()
        self.column_names = ["ID","Prezime", "Ime", "Pseudonim"]
        self.tw = ttk.Treeview(self.saw_frame, column=self.column_names, show='headings')
        self.tw.pack(side=tk.TOP)
        self.tw.column(0, minwidth=40, width=40)
        self.add_new_author_button = ttk.Button(self.saw_frame, text="Add new", command=self.add_new_author_window)
        self.add_new_author_button.pack(side=tk.LEFT)
        self.saw_select_author_button = ttk.Button(self.saw_frame, text="Izaberi autora", command=self.select_from_treeview)
        self.saw_select_author_button.pack(side=tk.RIGHT)
        for i in self.column_names:
            self.tw.heading(i, text=i)
        self.populate_treeview()

    def populate_treeview(self):
        for d in database.retrieve_authors():
            self.tw.insert('', tk.END, values=(d[0], d[1], d[2], d[3]))

    def clear_treeview(self):
        for i in self.tw.get_children():
            self.tw.delete(i)

    def select_from_treeview(self):
        try:
            print(self.tw.item(self.tw.focus())["values"][0])  # index of the selected author
        except:
            # if no author is selected
            pass

    def add_new_author_window(self):
        self.anaw = tk.Toplevel(self.saw)
        self.anaw.title("Add new author")
        self.anaw_frame = tk.Frame(self.anaw)
        self.anaw_frame.grid()
        for i in range(0,4):
            self.anaw_frame.columnconfigure(i, weight=1)
            self.anaw_frame.rowconfigure(i, weight=1)
        self.anaw_surname_label = ttk.Label(self.anaw_frame, text="Surname: ", anchor=tk.W)
        self.anaw_surname_entry = ttk.Entry(self.anaw_frame, width=40)
        self.anaw_name_label = ttk.Label(self.anaw_frame, text="Name: ", anchor=tk.W)
        self.anaw_name_entry = ttk.Entry(self.anaw_frame, width=40)
        self.anaw_pseudonym_label = ttk.Label(self.anaw_frame, text="Pseudonym: ", anchor=tk.W)
        self.anaw_pseudonym_entry = ttk.Entry(self.anaw_frame, width=40)
        self.anaw_surname_label.grid(row=0, column=0, padx=10)
        self.anaw_surname_entry.grid(row=0, column=1, padx=10)
        self.anaw_name_label.grid(row=1, column=0, padx=10)
        self.anaw_name_entry.grid(row=1, column=1, padx=10)
        self.anaw_pseudonym_label.grid(row=2, column=0, padx=10)
        self.anaw_pseudonym_entry.grid(row=2, column=1, padx=10)
        self.anaw_submit = ttk.Button(self.anaw_frame, text="Unesi", command=self.add_new_author_to_db, width=20)
        self.anaw_submit.grid(row=3, column=3)

    def add_new_author_to_db(self):
        print("Author added!")
        self.anaw.destroy()

database.create()
app = Interface()
app.mainloop()
