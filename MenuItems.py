import psycopg2
from tkinter import *
from tkinter import messagebox
import sys
from SakthiLibrary import records, lending, Cash_Book


class MenuBar():
    def __init__(self, master):
        self.master = master
        self.master.state('zoomed')
        self.master.title('Sakthi Lending Library')
        self.master.config(bg="#4E806A")

        # Add Author, Books, Publisher, Translator

        # Lending Menu

        self.status_bar = Label(self.master, text='', bd=1, relief=GROOVE, anchor=E)
        self.status_bar.pack(fill=X, side=BOTTOM, ipady=2)

        self.add_auth_btn = Button(self.master, text="Author", underline=0, width=8, justify=CENTER, bg="black",
                                   fg="green", bd=10, font=('Arial Unicode MS', 16, 'bold'), padx=30, pady=15, relief="sunken",
                                   command=self.add_author)
        self.add_auth_btn.place(x=1400, y=200)
        self.add_trans_btn = Button(self.master, text="Translator", underline=0, width=8, justify=CENTER, bg="black",
                                    fg="green", bd=10, relief="sunken",
                                    font=('Arial Unicode MS', 16, 'bold'), padx=30, pady=15,
                                    command=self.add_translator)
        self.add_trans_btn.place(x=1650, y=200)
        self.add_book_btn = Button(self.master, text="Books", bd=10,underline=0, width=8, justify=CENTER, bg="black",
                                   fg="green", relief="sunken",
                                   font=('Arial Unicode MS', 16, 'bold'), padx=30, pady=15, command=self.add_books)
        self.add_book_btn.place(x=1400, y=400)
        self.add_sub_btn = Button(self.master, text="Subscriber", bd=10,underline=0, width=8, justify=CENTER, bg="black",
                                  fg="green", relief="sunken",
                                  font=('Arial Unicode MS', 16, 'bold'), padx=30, pady=15, command=self.add_subscriber)
        self.add_sub_btn.place(x=1650, y=400)
        self.lend_btn = Button(self.master, text="Lending", bd=10,underline=0, width=8, justify=CENTER, bg="black",
                               fg="green", relief="sunken",
                               font=('Arial Unicode MS', 16, 'bold'), padx=30, pady=15, command=self.lending_books)
        self.lend_btn.place(x=1400, y=600)
        self.cash_btn = Button(self.master, text="Cash Book", bd=10,underline=0, width=8, justify=CENTER, bg="black",
                               fg="green", relief="sunken",
                               font=('Arial Unicode MS', 16, 'bold'), padx=30, pady=15, command=self.get_cash_book)
        self.cash_btn.place(x=1650, y=600)
        self.add_pub_btn = Button(self.master, text="Publisher", bd=10,underline=0, width=8, justify=CENTER, bg="black",
                                  fg="green", relief="sunken",
                                  font=('Arial Unicode MS', 16, 'bold'), padx=30, pady=15, command=self.add_publisher)
        self.add_pub_btn.place(x=1400, y=800)
        self.quit_btn = Button(self.master, text="Quit",bd=10, underline=0, width=8, justify=CENTER, bg="black",
                               relief="sunken",
                               fg="green",
                               font=('Arial Unicode MS', 16, 'bold'), padx=30, pady=15, command=self.master.destroy)
        self.quit_btn.place(x=1650, y=800)

        self.master.bind("<Control-q>", lambda e: quit(e))
        # self.master.bind_all('<Control-a>', lambda: self.add_records.focus_set(e))
        self.master.bind('<Control-a>', lambda e: self.add_author())
        self.master.bind('<Control-b>', lambda e: self.add_books())
        self.master.bind('<Control-p>', lambda e: self.add_publisher())
        self.master.bind('<Control-s>', lambda e: self.add_subscriber())
        self.master.bind('<Control-t>', lambda e: self.add_translator())
        self.master.bind('<Control-l>', lambda e: self.lending_books())
        self.master.bind('<Control-c>', lambda e: self.get_cash_book())

    def get_cash_book(self):
        cashbook = Cash_Book.CashBook(self.master, "cash_book")

    def add_author(self):
        author = records.TableEditor(self.master, "Author List", "Search", "Author Data", "Author Id", "Author Name",
                                     "Address", "Phone", "author")

    def add_books(self):
        books = records.TableEditor(self.master, "Books List", "Search", "Books Data", "Book Id",
                                    "Title", "Author", "Translator", "books", "Language", "Category", "Publisher",
                                    "Price", "Availability", "Purchased on", "Status")

    def add_publisher(self):
        publisher = records.TableEditor(self.master, "Publisher List", "Search", "Publisher Data", "Publisher Id",
                                        "Publisher Name", "Address", "Phone", "publisher")

    def add_subscriber(self):
        subscriber = records.TableEditor(self.master, "Subscriber List", "Search", "Subscriber Data", "Subscriber Id",
                                         "Subscriber Name", "Address", "Phone", "subscriber", "Email_id", "Plan",
                                         "Subscription", "ID Proof", "Join Date", "Closed Date", "Remarks")

    def add_translator(self):
        translator = records.TableEditor(self.master, "Translator List", "Search", "Translator Data", "Translator Id",
                                         "Translator Name", "Address", "Phone", "translator")

    def lending_books(self):
        print("Hi")
        lend = lending.Lending_Books(self.master, "lending")

    def hidden(self):
        pass

    def quit(*ignore):
        sys.exit(0)
