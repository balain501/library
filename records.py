from tkinter import *
from tkinter.ttk import Treeview
import tkinter as tk
from tkinter import ttk, messagebox, font
from datetime import date
import psycopg2


class TableEditor:

    def __init__(self, master, name_list, name_search, name_data, *args):
        self.master = master
        self.root = Toplevel(self.master)
        x = args[4].title()
        self.root.title(f'{x}s Entry')
        self.root.state("zoomed")
        self.q = StringVar()
        self.t1 = StringVar()
        self.t2 = StringVar()
        self.t3 = StringVar()
        self.t4 = StringVar()
        self.t5 = StringVar()
        self.t6 = StringVar()
        self.t7 = StringVar()
        self.t8 = StringVar()
        self.t9 = StringVar()
        self.t10 = StringVar()
        self.t11 = StringVar()
        self.planvar = StringVar()
        self.datevar = StringVar()
        self.planvar.set("Books Non subscriber")
        self.datevar.set(str(date.today()))
        self.entry_field1 = args[0]
        self.entry_field2 = args[1]
        self.entry_field3 = args[2]
        self.entry_field4 = args[3]
        self.table_name = args[4]
        self.add_author_bool = False
        self.adjust_tree = False
        global con
        con = psycopg2.connect(
            host="localhost",
            database="SakthiLibrary",
            user='postgres',
            password='ushabala1',
            port=5433,
        )
        global cur
        cur = con.cursor()

        self.wrapper1 = LabelFrame(self.root, text=name_list, height=300)
        self.wrapper2 = LabelFrame(self.root, text=name_search)
        self.wrapper3 = LabelFrame(self.root, text=name_data)
        self.wrapper1.pack(fill="both", expand="yes", padx=5, pady=3)

        # self.wrapper1.pack(padx=15,pady=3)
        self.wrapper2.pack(fill="both", padx=5, pady=3)
        self.wrapper3.pack(fill="both", expand="no", padx=5, pady=3)
        if self.table_name == "subscriber" or self.table_name == "books":
            self.entry_field5 = args[5]
            self.entry_field6 = args[6]
            self.entry_field7 = args[7]
            self.entry_field8 = args[8]
            self.entry_field9 = args[9]
            self.entry_field10 = args[10]
            self.entry_field11 = args[11]
            self.tree = Treeview(self.wrapper1, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), show="headings",
                                 height="30")
            self.tree.heading(5, text=self.entry_field5)
            self.tree.heading(6, text=self.entry_field6)
            self.tree.heading(7, text=self.entry_field7)
            self.tree.heading(8, text=self.entry_field8)
            self.tree.heading(9, text=self.entry_field9)
            self.tree.heading(10, text=self.entry_field10)
            self.tree.heading(11, text=self.entry_field11)
            self.tree.column(1, minwidth=0, width=70, stretch=NO)
            self.tree.column(2, minwidth=0, width=200, stretch=NO)
            self.tree.column(3, minwidth=0, width=400, stretch=NO)
            self.tree.column(4, minwidth=0, width=150, stretch=NO)
            self.tree.column(5, minwidth=0, width=150, stretch=NO)
            self.tree.column(6, minwidth=0, width=250, stretch=NO)
            self.tree.column(7, minwidth=0, width=150, stretch=NO)
            self.tree.column(8, minwidth=0, width=150, stretch=NO)
            self.tree.column(9, minwidth=0, width=150, stretch=NO)
            self.tree.column(10, minwidth=0, width=100, stretch=NO)
            self.tree.column(11, minwidth=0, width=200, stretch=NO)

        else:
            self.tree = Treeview(self.wrapper1, columns=(1, 2, 3, 4), show="headings", height="30")
        # vertical scroll
        self.yscroll = ttk.Scrollbar(self.wrapper1, orient="vertical", command=self.tree.yview)
        self.yscroll.pack(side="right", fill="y", expand=False)
        #    self.yscroll.place(x=1880)
        self.tree.configure(yscrollcommand=self.yscroll.set)
        self.tree.pack(fill="both")

        # self.tree.place(x=0, y=0)
        self.tree.heading(1, text=self.entry_field1)
        self.tree.heading(2, text=self.entry_field2)
        self.tree.heading(3, text=self.entry_field3)
        self.tree.heading(4, text=self.entry_field4)

        self.tree.bind('<Double 1>', self.getrow)
        # cur.execute("SET search_path TO myschema,public;")
        if self.table_name == "author":
            query = 'SELECT author_id, author_name, address, phone FROM author order by author_name'
        elif self.table_name == "books":
            query = 'SELECT * FROM books order by book_id'
        elif self.table_name == "publisher":
            query = 'SELECT publisher_id, publisher_name, address, phone FROM publisher order by publisher_name'
        elif self.table_name == "subscriber":
            query = 'SELECT * FROM subscriber order by subscriber_id'
        elif self.table_name == "translator":
            query = 'SELECT translator_id, translator_name, address, phone FROM translator order by translator_name'
        cur.execute(query)
        rows = cur.fetchall()
        self.update(rows)

        helv12 = font.Font(family='Helvetica', size=12, weight=font.BOLD)
        self.lbl = Label(self.wrapper2, text="Search")
        self.lbl.grid(row=0, column=0, padx=10, pady=10)
        self.txt1 = Entry(self.wrapper2, textvariable=self.q)
        self.txt1.grid(row=0, column=1, padx=10, pady=10)
        if self.table_name == "books":
            self.search_btn = Button(self.wrapper2, text="Search Title", underline=7, font=helv12,
                                     command=lambda: self.search(self.table_name, "title"))
            self.search_btn.grid(row=0, column=2, padx=10, pady=10)
            self.search_btn2 = Button(self.wrapper2, text="Search Author", underline=10, font=helv12,
                                      command=lambda: self.search(self.table_name, "author"))
            self.search_btn2.grid(row=0, column=3, padx=10, pady=10)
            self.clr_btn = Button(self.wrapper2, text="Clear", underline=0, font=helv12,
                                  command=lambda: self.clear(self.table_name))
            self.clr_btn.grid(row=0, column=4, padx=10, pady=10)
        else:
            self.search_btn = Button(self.wrapper2, text="Search", underline=1, font=helv12,
                                     command=lambda: self.search(self.table_name))
            self.search_btn.grid(row=0, column=2, padx=10, pady=10)
            self.clr_btn = Button(self.wrapper2, text="Clear", underline=0, font=helv12,
                                  command=lambda: self.clear(self.table_name))
            self.clr_btn.grid(row=0, column=3, padx=10, pady=10)
            self.txt1.bind('<Return>', self.search)
            self.search_btn.bind('<Return>', self.search)

        self.wrapper3.rowconfigure(5)
        self.lbl1 = Label(self.wrapper3, text=self.entry_field1)
        self.lbl1.grid(row=0, column=0, padx=1, pady=1)
        self.ent1 = Entry(self.wrapper3, textvariable=self.t1, relief="groove", justify="right", bd=5, bg="light blue",
                          state=DISABLED)
        self.ent1.grid(row=0, column=1, padx=1, pady=1)
        self.lbl2 = Label(self.wrapper3, text=self.entry_field2)
        self.lbl2.grid(row=1, column=0, padx=1, pady=1)
        self.ent2 = Entry(self.wrapper3, textvariable=self.t2, relief="groove", bd=5)
        self.ent2.grid(row=1, column=1, padx=1, pady=1)
        self.lbl3 = Label(self.wrapper3, text=self.entry_field3)
        self.lbl3.grid(row=2, column=0, padx=1, pady=1)
        self.ent3 = Entry(self.wrapper3, textvariable=self.t3, relief="groove", bd=5)
        self.ent3.grid(row=2, column=1, padx=1, pady=1)
        self.lbl4 = Label(self.wrapper3, text=self.entry_field4)
        self.lbl4.grid(row=3, column=0, padx=1, pady=1)
        self.ent4 = Entry(self.wrapper3, textvariable=self.t4, relief="groove", bd=5)
        self.ent4.grid(row=3, column=1, padx=1, pady=1)

        # condition for subscriber's table:
        if self.table_name == "subscriber" or self.table_name == "books":
            self.lbl5 = Label(self.wrapper3, text=self.entry_field5)
            self.lbl5.grid(row=0, column=2, padx=1, pady=1)
            self.ent5 = Entry(self.wrapper3, textvariable=self.t5, relief="groove", bd=5)
            self.ent5.grid(row=0, column=3, padx=1, pady=1)
            self.lbl6 = Label(self.wrapper3, text=self.entry_field6)
            self.lbl6.grid(row=1, column=2, padx=1, pady=1)
            self.ent6 = Entry(self.wrapper3, textvariable=self.t6, relief="groove", bd=5)
            self.ent6.grid(row=1, column=3, padx=1, pady=1)
            self.combo = ttk.Combobox(self.wrapper3,textvariable=self.t6, width=18)
            self.combo.grid(row=1, column=3, padx=1, pady=1)
            if self.table_name == "subscriber":
                self.combo.grid_forget()
            else:
                self.ent6.grid_forget()
            self.lbl7 = Label(self.wrapper3, text=self.entry_field7)
            self.lbl7.grid(row=2, column=2, padx=1, pady=1)
            self.ent7 = Entry(self.wrapper3, textvariable=self.t7, relief="groove", bd=5)
            self.ent7.grid(row=2, column=3, padx=1, pady=1)
            self.lbl8 = Label(self.wrapper3, text=self.entry_field8)
            self.lbl8.grid(row=3, column=2, padx=1, pady=1)
            self.ent8 = Entry(self.wrapper3, textvariable=self.t8, relief="groove", bd=5)
            self.ent8.grid(row=3, column=3, padx=1, pady=1)
            self.lbl9 = Label(self.wrapper3, text=self.entry_field9)
            self.lbl9.grid(row=0, column=4, padx=1, pady=1)
            self.ent9 = Entry(self.wrapper3, textvariable=self.t9, relief="groove", bd=5)
            self.ent9.grid(row=0, column=5, padx=1, pady=1)
            self.lbl10 = Label(self.wrapper3, text=self.entry_field10)
            self.lbl10.grid(row=1, column=4, padx=1, pady=1)
            self.ent10 = Entry(self.wrapper3, textvariable=self.t10, relief="groove", bd=5)
            self.ent10.grid(row=1, column=5, padx=1, pady=1)
            self.lbl11 = Label(self.wrapper3, text=self.entry_field11)
            self.lbl11.grid(row=2, column=4, padx=1, pady=1)
            self.ent11 = Entry(self.wrapper3, textvariable=self.t11, relief="groove", bd=5)
            self.ent11.grid(row=2, column=5, padx=1, pady=1)


        self.btn_frame = Frame(self.wrapper3, bg="DeepSkyBlue4")
        self.btn_frame.grid(row=4, columnspan=10, sticky=EW)
        self.add_btn = Button(self.btn_frame, text="Add New", underline=0, font=helv12,
                              command=lambda: self.add_new(True, self.table_name))
        self.add_btn.grid(column=0, row=0, padx=2, pady=2)
        self.up_btn = Button(self.btn_frame, text="Update", underline=0, font=helv12,
                             command= self.update_author)
        self.up_btn.grid(column=1, row=0, padx=2, pady=2)
        self.save_btn = Button(self.btn_frame, text="Save", underline=0, font=helv12, command=self.save_author(True))
        self.save_btn.grid(column=2, row=0, padx=2, pady=2)
        self.delete_btn = Button(self.btn_frame, text="Delete " + str(self.table_name), underline=0, font=helv12,
                                 command=lambda: self.delete_author(self.table_name))
        self.delete_btn.grid(row=0, column=3, padx=10)
        self.exit_btn = Button(self.btn_frame, text="Quit", underline=0, font=helv12, command=self.quit_window)
        self.exit_btn.grid(row=0, column=4, padx=20)

        self.ent4.bind('<Tab>', self.key_press)
        self.add_btn.bind('<space>', self.add_new)
        self.add_btn.bind('<Return>', self.add_new)
        self.up_btn.bind('<space>', self.update_author)
        self.up_btn.bind('<Return>', self.update_author)
        self.delete_btn.bind('<space>', self.delete_author)
        self.delete_btn.bind('<Return>', self.delete_author)
        self.save_btn.bind('<space>', self.save_author)
        self.save_btn.bind('<Return>', self.save_author)
        self.root.bind('<Control-q>', self.quit_window)
        self.root.bind('<Control-u>', self.update_author)
        self.root.bind('<Control-a>', lambda e: self.add_new(True, self.table_name, e))
        self.root.bind('<Control-d>', self.delete_author)
        self.root.bind('<Control-s>', self.save_author)
        self.root.bind('<Control-e>', self.search)
        self.txt1.bind('<Control-t>', lambda e: self.search(self.table_name, "title"))
        self.txt1.bind('<Control-h>', lambda e: self.search(self.table_name, "author"))
        if self.table_name == "books":
            self.ent3.bind('<KeyRelease>', lambda e: self.search_author_for_books(e))
            self.ent3.bind('<Return>', self.set_author)
            self.ent3.bind('<Down>', self.set_author_arrow)
            self.ent4.bind('<KeyRelease>', lambda e: self.search_trans_for_books(e))
            self.ent4.bind('<Return>', self.set_trans)
            self.ent4.bind('<Down>', self.set_author_arrow)
            self.ent5.bind('<Up>', self.arrow)
            self.ent5.bind('<Down>', self.arrow)
            self.combo.bind('<Return>', self.set_publish_for_books)
            self.ent7.bind('<Return>', self.set_publish)
        self.root.bind('<Control-c>', self.clear)
        self.root.bind('<Return>', self.key_press)

        self.root.mainloop()

    def set_publish_for_books(self, event):
        if event.keysym != "Down":
            q = self.ent7.get()
            query = "select distinct on (publisher_name) publisher_name, * from books where publisher_name ilike '" + q + "%'" + " order by publisher_name"
            cur.execute(query)
            row = cur.fetchall()
            self.adjust_tree=True
            self.update(row)
            children = self.tree.get_children()
            self.tree.selection_set(children)
            self.tree.selection_toggle(children[1:])

    def set_publish(self, *ignore):
        self.tree.focus()
        cursel = self.tree.selection()
        x=self.tree.item(cursel)
        self.t7.set(x['values'][6])


    def arrow(self, *ignore):
        if self.t5.get()=="Tamil":
            self.t5.set("English")
            self.ent5.selection_range(0,END)
        else:
            self.t5.set("Tamil")
            self.ent5.selection_range(0, END)


    def set_author(self, *ignore):
        self.tree.focus()
        cursel = self.tree.selection()
        x=self.tree.item(cursel)
        self.t3.set(x['values'][2])

    def set_author_arrow(self, e,*ignore):
#        print(e.keysym)
        if self.tree.index(self.tree.selection())<len(self.tree.get_children()):
            #cursel = self.tree.selection()
            selint=self.tree.index(self.tree.selection())
            children = self.tree.get_children()
            #self.tree.selection_toggle(cursel)
            self.tree.selection_set(children)
            self.tree.selection_toggle(children[selint+2:])
            self.tree.selection_toggle(children[:selint+1])
            #self.tree.selection_toggle(children[self.tree.index(cursel)+2:])
            #self.tree.selection_remove(self.tree.index(cursel))
            #self.tree.index(cursel) + 1
            #children[self.tree.index(cursel)+1:]
            #self.tree.selection_remove(children[self.tree.index(cursel)+1:])




    def set_trans(self, *ignore):
        self.tree.focus()
        cursel = self.tree.selection()
        x = self.tree.item(cursel)
        self.t4.set(x['values'][3])
        self.t5.set("Tamil")
        self.ent5.selection_range(0, END)

    def quit_window(self, *ignore):
        self.root.destroy()
        cur.close()
        con.close()

    def update(self, rows):
        if self.table_name == "author":
            self.root.configure(background='#85886C')
        elif self.table_name == "publisher":
            self.root.configure(background='#3960B1')
        elif self.table_name == "translator":
            self.root.configure(background='#13C7C6')
        elif self.table_name == "subscriber":
            self.root.configure(background='#C45A22')
        elif self.table_name == "books":
            self.root.configure(background='Indian red')
        row = rows
        self.tree.delete(*self.tree.get_children())
        if self.adjust_tree:
            for i in rows:
                self.tree.insert('', 'end', values=i[1:])
            # for i in auth_row:
            #   self.tree.insert('', 'end', values=i)
            # self.tree.selection_set(self.tree.tag_has(rows[0][3]))
            # print(rows[0][3])
        else:
            for i in rows:
                self.tree.insert('', 'end', values=i)

    def search(self, table, searchby):
        q2 = "'" + self.q.get() + "%'"
        # con.rollback()
        if self.table_name == "author":
            query = '''SELECT author_id, author_name, address, phone FROM author where author_name ilike ''' + q2 + ''' order by author_name'''
            return ("break")
        if table == "books":
            if searchby == "author":
                query = '''select distinct on (author_name) author_name, * from books where author_name ilike ''' + q2 + ''' order by author_name'''
                self.adjust_tree = True
            elif searchby == "title":
                query = '''SELECT * FROM books where book_name ilike ''' + q2 + ''' order by book_name'''
        elif self.table_name == "publisher":
            query = '''SELECT publisher_id, publisher_name, address, phone FROM publisher where publisher_name ilike ''' + q2 + ''' order by publisher_name'''
        elif self.table_name == "translator":
            query = '''SELECT translator_id, translator_name, address, phone FROM translator where translator_name ilike ''' + q2 + ''' order by translator_name'''
        elif self.table_name == "subscriber":
            query = '''SELECT * FROM subscriber where subscriber_name ilike ''' + q2 + ''' order by subscriber_name'''
        cur.execute(query)
        row = cur.fetchall()
        self.update(row)
        if table == "books" and searchby == "author" or searchby == "title":
            return ("break")

    def search_author_for_books(self, event, *ignore):
        if event.keysym!="Down":
            q = self.ent3.get()
            query = "select distinct on (author_name) author_name, * from books where author_name ilike '" + q + "%'" + " order by author_name"
            cur.execute(query)
            row = cur.fetchall()
            self.update(row)
            children=self.tree.get_children()
            self.tree.selection_set(children)
            self.tree.selection_toggle(children[1:])
        #print(self.tree.winfo_parent()
        #self.tree.focus(self.tree.tag_has('bala'))


    def search_trans_for_books(self, event, *ignore):
        if event.keysym != "Down":
            q = self.ent4.get()
            query = "select distinct on (translator_name) translator_name, * from books where translator_name ilike '" + q + "%'" + " order by translator_name"
            cur.execute(query)
            row = cur.fetchall()
            self.adjust_tree=True
            self.update(row)
            children = self.tree.get_children()
            self.tree.selection_set(children)
            self.tree.selection_toggle(children[1:])



    def clear(self, *ignore):
        if self.table_name == "author":
            query = '''SELECT author_id, author_name, address, phone from author order by author_name'''
        elif self.table_name == "publisher":
            query = '''SELECT publisher_id, publisher_name, address, phone from publisher order by publisher_name'''
        elif self.table_name == "subscriber":
            query = '''SELECT * from subscriber order by subscriber_name'''
        elif self.table_name == "books":
            query = '''SELECT * from books order by book_id'''
        elif self.table_name == "translator":
            query = '''SELECT translator_id, translator_name, address, phone from translator order by translator_name'''
        cur.execute(query)
        rows = cur.fetchall()
        self.adjust_tree=False
        self.update(rows)

    def update_id(self):
        if self.table_name == "author":
            query = '''select max(author_id)+1 from author'''
        if self.table_name == "books":
            query = '''select max(book_id)+1 from books'''
            self.adjust_tree = True
        if self.table_name == "publisher":
            query = '''select max(publisher_id)+1 from publisher'''
        if self.table_name == "subscriber":
            query = '''select max(subscriber_id)+1 from subscriber'''
        if self.table_name == "translator":
            query = '''select max(translator_id)+1 from translator'''
        cur.execute(query)
        x = cur.fetchall()
        self.ent1.insert(0, str(x[0][0]))

    def getrow(self, event):
        self.add_author_bool = False
        rowId = self.tree.identify_row(event.y)
        item = self.tree.item(self.tree.focus())
        self.t1.set(item['values'][0])
        self.t2.set(item['values'][1])
        self.t3.set(item['values'][2])
        self.t4.set(item['values'][3])
        if self.table_name == "subscriber" or self.table_name == "books":
            if self.table_name=="subscriber":
                self.ent6.config(textvariable=self.t6)
            else:
                self.combo.config(textvariable=self.t6)
            self.ent9.config(textvariable=self.t9)
            self.t5.set(item['values'][4])
            self.t6.set(item['values'][5])
            self.t7.set(item['values'][6])
            self.t8.set(item['values'][7])
            self.t9.set(item['values'][8])
            self.t10.set(item['values'][9])
            self.t11.set(item['values'][10])

    def update_author(self, event):
        au_id = self.t1.get()
        au_name = self.t2.get()
        au_address = self.t3.get()
        au_phone = self.t4.get()

        if len(self.ent1.get()) > 0 and len(self.ent2.get()) > 0:
            print(self.ent1.get())
            if messagebox.askyesno("Update Confirm", "Do you really want to update?", parent=self.root):
                self.root.focus_force()
                if self.table_name == "author":
                    query = 'UPDATE author SET author_name=%s, address=%s, phone=%s WHERE author_id=' + self.ent1.get()
                if self.table_name == "publisher":
                    query = 'UPDATE publisher SET publisher_name=%s, address=%s, phone=%s WHERE publisher_id=' + self.ent1.get()
                if self.table_name == "subscriber":
                    a = lambda x: self.t5.get() if (self.t5.get() != 'None') else None
                    sub_email = a(self.t5.get())
                    sub_plan = self.t6.get()
                    sub_subscription = self.t7.get()
                    a = lambda x: self.t8.get() if self.t8.get() != 'None' else None
                    sub_idproof = a(self.t8.get())
                    sub_join = self.t9.get()
                    a = lambda x: self.t10.get() if self.t10.get() != 'None' else None
                    sub_closed = a(self.t10.get())
                    a = lambda x: self.t11.get() if self.t11.get() != 'None' else None
                    sub_remarks = a(self.t11.get())
                    '''if sub_closed == None:
                        query = 'UPDATE subscriber SET subscriber_name=%s, address=%s, phone=%s, email_id=%s, plan=%s, subscription_amt=%s, id_proof=%s, join_date=%s, remarks=%s WHERE subscriber_id=' + self.ent1.get()
                        cur.execute(query, (
                            au_name, au_address, au_phone, sub_email, sub_plan, sub_subscription, sub_idproof, sub_join,
                            sub_remarks))
                    else:'''
                    query = 'UPDATE subscriber SET subscriber_name=%s, address=%s, phone=%s, email_id=%s, plan=%s, subscription_amt=%s, id_proof=%s, join_date=%s, closed_date=%s, remarks=%s WHERE subscriber_id=' + self.ent1.get()
                    cur.execute(query, (
                        au_name, au_address, au_phone, sub_email, sub_plan, sub_subscription, sub_idproof, sub_join,
                        sub_closed, sub_remarks))
                    con.commit()
                    self.ent5.delete(0, END)
                    self.ent6.delete(0, END)
                    self.ent7.delete(0, END)
                    self.ent8.delete(0, END)
                    self.ent9.delete(0, END)
                    self.ent10.delete(0, END)
                    self.ent11.delete(0, END)
                if self.table_name == "books":
                    a = lambda x: self.t4.get() if (len(self.t4.get()) > 0) else None
                    booK_translator = a(self.t4.get())
                    a = lambda x: self.t5.get() if (len(self.t5.get()) > 0) else None
                    booK_language = a(self.t5.get())
                    a = lambda x: self.t6.get() if (len(self.t6.get()) > 0) else None
                    booK_category = a(self.t6.get())
                    a = lambda x: self.t7.get() if (len(self.t7.get()) > 0) else None
                    booK_publisher = a(self.t7.get())
                    a = lambda x: self.t10.get() if (len(self.t10.get()) > 0) else None
                    booK_inv_date = a(self.t10.get())
                    book_price = self.t8.get()
                    book_avail = self.t9.get()
                    book_status = self.t11.get()
                    query = 'UPDATE books SET book_name=%s, author_name=%s, translator_name=%s, language=%s, book_category=%s, publisher_name=%s, price=%s, availability=%s, inv_date=%s, book_status=%s WHERE book_id=' + self.ent1.get()
                    cur.execute(query, (
                        au_name, au_address, booK_translator, booK_language, booK_category, booK_publisher, book_price,
                        book_avail, booK_inv_date, book_status))
                    con.commit()
                    self.ent5.delete(0, END)
                    self.combo.delete(0, END)
                    #self.ent6.delete(0, END)
                    self.ent7.delete(0, END)
                    self.ent8.delete(0, END)
                    self.ent9.delete(0, END)
                    self.ent10.delete(0, END)
                    self.ent11.delete(0, END)
                if self.table_name == "translator":
                    query = 'UPDATE translator SET translator_name=%s, address=%s, phone=%s WHERE translator_id=' + self.ent1.get()
                if self.table_name != "subscriber" and self.table_name != "books":
                    cur.execute(query, (au_name, au_address, au_phone))
                    con.commit()
                self.ent1.delete(0, END)
                self.ent2.delete(0, END)
                self.ent3.delete(0, END)
                self.ent4.delete(0, END)
                self.clear()
        else:
            messagebox.showinfo("!", "No records are selected!", parent=self.root)
            self.root.focus_force()

    def add_new(self, *ignore):
        self.add_author_bool = True
        self.ent1.config(state=NORMAL)
        self.ent1.delete(0, END)
        self.ent2.delete(0, END)
        self.ent3.delete(0, END)
        self.ent4.delete(0, END)
        if self.table_name == "subscriber" or self.table_name == "books":
            self.ent5.delete(0, END)
            if self.table_name=="subscriber":
                self.ent6.delete(0, END)
            else:
                self.combo.delete(0, END)
            self.ent7.delete(0, END)
            self.ent8.delete(0, END)
            self.ent9.delete(0, END)
            self.ent10.delete(0, END)
            self.ent11.delete(0, END)
        self.update_id()
        self.ent1.config(state=DISABLED)
        self.ent2.focus()

    def delete_author(self, *ignore):
        au_id = self.t1.get()
        query = ""
        if len(self.ent1.get()) > 0:
            if messagebox.askyesno("Confirm Delete", "Do you really want to delete this record?", parent=self.root):
                self.root.focus_force()
                if self.table_name == "author":
                    query = 'DELETE FROM author where author_id=' + au_id
                elif self.table_name == "publisher":
                    query = 'DELETE FROM publisher where publisher_id=' + au_id
                if self.table_name == "translator":
                    query = 'DELETE FROM translator where translator_id=' + au_id
                elif self.table_name == "subscriber":
                    query = f'DELETE FROM subscribers where subscriber_id=' + au_id
                elif self.table_name == "books":
                    query = f'DELETE FROM books where book_id=' + au_id
                if self.table_name=="subscribers" or self.table_name=="books":
                    self.ent5.delete(0, END)
                    if self.table_name=="subscriber":
                        self.ent6.delete(0, END)
                    else:
                        self.combo.delete(0, END)
                    self.ent7.delete(0, END)
                    self.ent8.delete(0, END)
                    self.ent9.delete(0, END)
                    self.ent10.delete(0, END)
                    self.ent11.delete(0, END)

                cur.execute(query)
                con.commit()
                self.clear()
            else:
                return True
            self.ent1.delete(0, END)
            self.ent2.delete(0, END)
            self.ent3.delete(0, END)
            self.ent4.delete(0, END)
        else:
            messagebox.showinfo("Delete option", "Please select a record to delete", parent=self.root)
            self.root.focus_force()

    def save_author(self, event):
        if self.add_author_bool == True and len(self.ent1.get()) > 0 and len(self.ent2.get()) > 0:
            if messagebox.askyesno("Update Confirm", "Do you really want to save?", parent=self.root):
                au_id = self.t1.get()
                au_name = self.t2.get()
                au_address = self.t3.get()
                au_phone = self.t4.get()

                if self.table_name == "author":
                    query = 'INSERT INTO author(author_id, author_name, address, phone, email_id) values(%s, %s, %s, %s, NULL)'
                if self.table_name == "publisher":
                    query = 'INSERT INTO publisher(publisher_id, publisher_name, address, phone, email_id) values(%s, %s, %s, %s, NULL)'
                if self.table_name == "subscriber":
                    a = lambda x: self.t5.get() if (self.t5.get() != '') else None
                    sub_email = a(self.t5.get())
                    sub_plan = self.t6.get()
                    sub_subscription = self.t7.get()
                    a = lambda x: self.t8.get() if self.t8.get() != '' else None
                    sub_idproof = a(self.t8.get())
                    sub_join = self.t9.get()
                    a = lambda x: self.t10.get() if self.t10.get() != '' else None
                    sub_closed = a(self.t10.get())
                    a = lambda x: self.t11.get() if self.t11.get() != '' else None
                    sub_remarks = a(self.t11.get())
                    query = 'INSERT INTO subscriber(subscriber_id, subscriber_name, address, phone, email_id, plan, subscription_amt, id_proof, join_date, closed_date, remarks) values(%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s)'
                    cur.execute(query, (
                        au_id, au_name, au_address, au_phone, sub_email, sub_plan, sub_subscription, sub_idproof,
                        sub_join,
                        sub_closed, sub_remarks))
                    con.commit()
                    self.ent5.delete(0, END)
                    self.ent6.delete(0, END)
                    self.ent7.delete(0, END)
                    self.ent8.delete(0, END)
                    self.ent9.delete(0, END)
                    self.ent10.delete(0, END)
                    self.ent11.delete(0, END)
                if self.table_name == "books":
                    a = lambda x: self.t4.get() if (len(self.t4.get()) > 0) else None
                    booK_translator = a(self.t4.get())
                    a = lambda x: self.t5.get() if (len(self.t5.get()) > 0) else None
                    booK_language = a(self.t5.get())
                    a = lambda x: self.t6.get() if (len(self.t6.get()) > 0) else None
                    booK_category = a(self.t6.get())
                    a = lambda x: self.t7.get() if (len(self.t7.get()) > 0) else None
                    booK_publisher = a(self.t7.get())
                    a = lambda x: self.t10.get() if (len(self.t10.get()) > 0) else None
                    booK_inv_date = a(self.t10.get())
                    book_price = self.t8.get()
                    book_avail = self.t9.get()
                    book_status = self.t11.get()
                    query = 'INSERT INTO books(book_id, book_name, author_name, translator_name, language, book_category, publisher_name, price, availability, inv_date, book_status) values(%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s)'
                    cur.execute(query, (au_id, au_name, au_address, booK_translator, booK_language, booK_category, booK_publisher,
                    book_price, book_avail, booK_inv_date, book_status))
                    con.commit()
                    self.ent5.delete(0, END)
                    self.combo.delete(0, END)
                    #self.ent6.delete(0, END)
                    self.ent7.delete(0, END)
                    self.ent8.delete(0, END)
                    self.ent9.delete(0, END)
                    self.ent10.delete(0, END)
                    self.ent11.delete(0, END)
                if self.table_name == "translator":
                    query = 'INSERT INTO translator(translator_id, translator_name, address, phone, email_id) values(%s, %s, %s, %s, NULL)'
                if self.table_name not in ("subscriber", "books"):
                    cur.execute(query, (au_id, au_name, au_address, au_phone))
                    con.commit()
                self.add_author_bool = False
                self.adjust_tree=False
                self.clear()
                self.ent1.delete(0, END)
                self.ent2.delete(0, END)
                self.ent3.delete(0, END)
                self.ent4.delete(0, END)

    def key_press(self, event):
        x = str(event.widget)
        if x == ".!toplevel.!labelframe3.!entry":
            self.ent2.focus()
        elif x == ".!toplevel.!labelframe3.!entry2":
            self.ent3.focus()
        elif x == ".!toplevel.!labelframe3.!entry3":
            self.ent4.focus()
            self.adjust_tree = False
        elif x == ".!toplevel.!labelframe3.!entry4":
            if self.table_name == "subscriber" or self.table_name == "books":
                self.ent5.focus()
            else:
                if self.add_author_bool:
                    event.widget.tk_focusNext().focus()
                    self.save_btn.focus()
                    return ("break")
                else:
                    event.widget.tk_focusNext().focus()
                    self.up_btn.focus()
                    return ("break")
        elif x == ".!toplevel.!labelframe3.!entry5":
            if self.table_name == "subscriber":
                self.ent6.config(textvariable=self.planvar)
                self.ent6.select_range(0, END)
                self.ent6.focus()
            else:
                category = ['Short Stories', 'Articles','History','Modern Literature','Poems','Children','Comics','Self Development','Devotional','Family Novel','Crime Novel','Old Literature','Language','Astrology','Health','Romance','Thriller','Autobiography','Biography','Philosophy','Cooking','Travel','Sports','Drama','Business','Politics','Translated Novel','Translated Short Stories','Investment','Cinema','Interviews', 'Criticism']
                self.combo['values']=sorted(category)
                self.combo.current(1)
                self.combo.focus()
        elif x == ".!toplevel.!labelframe3.!combobox":
            self.ent7.focus()
        elif x == ".!toplevel.!labelframe3.!entry6":
            self.ent7.focus()
        elif x == ".!toplevel.!labelframe3.!entry7":
            self.ent8.focus()
        elif x == ".!toplevel.!labelframe3.!entry8":
            if self.table_name=="books" and (self.ent8.get()).isnumeric():
                self.t9.set("True")
                self.t10.set(date.today())
                self.ent10.selection_range(0, END)
                self.ent10.focus()
            else:
                if self.table_name == "subscriber":
                    self.ent9.config(textvariable=self.datevar)
                    self.ent9.select_range(0, END)
                    self.ent9.focus()
        elif x == ".!toplevel.!labelframe3.!entry9":
            self.ent10.focus()
        elif x == ".!toplevel.!labelframe3.!entry10":
            if self.table_name=="books":
                self.t11.set("Good")
                self.ent11.select_range(0,END)
            self.ent11.focus()
        elif x == ".!toplevel.!labelframe3.!entry11":
            if self.add_author_bool:
                event.widget.tk_focusNext().focus()
                self.save_btn.focus()
                return ("break")
            else:
                event.widget.tk_focusNext().focus()
                self.up_btn.focus()
                return ("break")
