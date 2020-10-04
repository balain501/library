from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Treeview
from tkinter import messagebox
import psycopg2


class Author:
    root = Tk()
    root.title("Bala's tree")
    root.geometry("750x900")
    root.bind('<Control-u>', update_author)
    root.bind('<Control-a>', lambda e: add_new(e))
    root.bind('<Control-d>', delete_author)
    root.bind('<Control-s>', save_author)
    root.bind('<Control-e>', search)
    root.bind('<Control-c>', clear)
    root.bind('<Return>', key_press)
    q = StringVar()
    t1 = StringVar()
    t2 = StringVar()
    t3 = StringVar()
    t4 = StringVar()
    root.mainloop()


def update(self, rows):
    row = rows
    self.tree.delete(*self.tree.get_children())
    for i in rows:
        self.tree.insert('', 'end', values=i)


def search(*ignore):
    q2 = "'" + q.get() + "%'"
    # con.rollback()
    query = '''SELECT author_id, author_name, address, phone FROM author where author_name ilike ''' + q2
    cur.execute(query)
    row = cur.fetchall()
    update(row)


def clear(*ignore):
    query = '''SELECT author_id, author_name, address, phone from author order by author_name'''
    cur.execute(query)
    rows = cur.fetchall()
    update(rows)


def update_id():
    query = '''select max(author_id)+1 from author'''
    cur.execute(query)
    x = cur.fetchall()
    ent1.insert(0, str(x[0][0]))


def getrow(self, event):
    rowId = self.tree.identify_row(event.y)
    item = self.tree.item(self.tree.focus())
    self.t1.set(item['values'][0])
    self.t2.set(item['values'][1])
    self.t3.set(item['values'][2])
    self.t4.set(item['values'][3])


def update_author(*ignore):
    au_id = t1.get()
    au_name = t2.get()
    au_address = t3.get()
    au_phone = t4.get()
    if len(ent1.get()) > 0 and len(ent2.get()) > 0:
        if messagebox.askyesno("Update Confirm", "Do you really want to update?"):
            query = 'UPDATE author SET author_name=%s, address=%s, phone=%s WHERE author_id=' + ent1.get()
            cur.execute(query, (au_name, au_address, au_phone))
            con.commit()
            ent1.delete(0, END)
            ent2.delete(0, END)
            ent3.delete(0, END)
            ent4.delete(0, END)
            clear()

    else:
        messagebox.showinfo("No records are selected!")


def add_new(*ignore):
    global add_author_bool
    add_author_bool = True
    ent1.config(state=NORMAL)
    ent1.delete(0, END)
    ent2.delete(0, END)
    ent3.delete(0, END)
    ent4.delete(0, END)
    update_id()
    ent1.config(state=DISABLED)
    ent2.focus()


def delete_author(*ignore):
    au_id = t1.get()
    if len(ent1.get()) > 0:
        if messagebox.askyesno("Confirm Delete", "Do you really want to delete this record?"):
            query = 'DELETE FROM author where author_id=' + au_id
            cur.execute(query)
            con.commit()
            clear()
        else:
            return True
        ent1.delete(0, END)
        ent2.delete(0, END)
        ent3.delete(0, END)
        ent4.delete(0, END)
    else:
        messagebox.showinfo("Delete option", "Please select a record to delete")


def save_author(*ignore):
    global add_author_bool
    print(add_author_bool)
    if add_author_bool == True and len(ent1.get()) > 0 and len(ent2.get()) > 0:
        au_id = t1.get()
        au_name = t2.get()
        au_address = t3.get()
        au_phone = t4.get()
        query = 'INSERT INTO author(author_id, author_name, address, phone, email_id) values(%s, %s, %s, %s, NULL)'
        cur.execute(query, (au_id, au_name, au_address, au_phone))
        con.commit()
        add_author_bool = False
        clear()
        ent1.delete(0, END)
        ent2.delete(0, END)
        ent3.delete(0, END)
        ent4.delete(0, END)


def key_press(event):
    global add_author_bool
    x = str(event.widget)
    if x == ".!labelframe3.!entry":
        ent2.focus()
    elif x == ".!labelframe3.!entry2":
        ent3.focus()
    elif x == ".!labelframe3.!entry3":
        ent4.focus()
    elif x == ".!labelframe3.!entry4":
        # messagebox.showinfo("sdf",f'you pressed {event} and add_author_bool status = {add_author_bool}')
        if add_author_bool:
            event.widget.tk_focusNext().focus()
            save_btn.focus()
            return ("break")
        else:
            event.widget.tk_focusNext().focus()
            up_btn.focus()
            return ("break")

    con = psycopg2.connect(
        host="localhost",
        database="SakthiLibrary",
        user='postgres',
        password='ushabala1',
        port=5433,
    )
    cur = con.cursor()

    global add_author_bool
    add_author_bool = False

    wrapper1 = LabelFrame(root, text="Authors list", height=700)
    wrapper2 = LabelFrame(root, text="Search", height=100)
    wrapper3 = LabelFrame(root, text="Authors Data", height=400)
    wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
    wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
    wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

    tree = Treeview(wrapper1, columns=(1, 2, 3, 4), show="headings", height="29")
    tree.pack(side=LEFT)
    tree.place(x=0, y=0)
    tree.heading(1, text="Author Id")
    tree.heading(2, text="Author Name")
    tree.heading(3, text="Address")
    tree.heading(4, text="Phone")
    tree.column(1, minwidth=20, width=50)
    tree.column(2, minwidth=20, width=400)
    tree.column(3, minwidth=20, width=182)
    tree.column(4, minwidth=20, width=50)

    tree.bind('<Double 1>', getrow)
    cur.execute("SET search_path TO myschema,public;")
    query = 'SELECT author_id, author_name, address, phone FROM author order by author_name'
    cur.execute(query)
    rows = cur.fetchall()
    update(rows)

    # search section

    lbl = Label(wrapper2, text="Search")
    lbl.pack(side=tk.LEFT, padx=10)
    txt1 = Entry(wrapper2, textvariable=q)
    txt1.pack(side=tk.LEFT, padx=6)
    search_btn = Button(wrapper2, text="Search", underline=1, command=search)
    search_btn.pack(side=tk.LEFT, padx=6)
    clr_btn = Button(wrapper2, text="Clear", underline=0, command=clear)
    clr_btn.pack(side=tk.LEFT, padx=6)
    txt1.bind('<Return>', search)

    # User Data Section
    lbl1 = Label(wrapper3, text="Author_id")
    lbl1.grid(row=0, column=0, padx=5, pady=3)
    ent1 = Entry(wrapper3, textvariable=t1, relief="groove", justify="right", bd=5, bg="light blue", state=DISABLED)
    ent1.grid(row=0, column=1, padx=5, pady=3)
    lbl2 = Label(wrapper3, text="Author_Name")
    lbl2.grid(row=1, column=0, padx=5, pady=3)
    ent2 = Entry(wrapper3, textvariable=t2, relief="groove", bd=5)
    ent2.grid(row=1, column=1, padx=5, pady=3)
    lbl3 = Label(wrapper3, text="Address")
    lbl3.grid(row=2, column=0, padx=5, pady=3)
    ent3 = Entry(wrapper3, textvariable=t3, relief="groove", bd=5)
    ent3.grid(row=2, column=1, padx=5, pady=3)
    lbl4 = Label(wrapper3, text="Phone")
    lbl4.grid(row=3, column=0, padx=5, pady=3)
    ent4 = Entry(wrapper3, textvariable=t4, relief="groove", bd=5)
    ent4.grid(row=3, column=1, padx=5, pady=3)

    # vertical scroll
    yscroll = ttk.Scrollbar(wrapper1, orient="vertical", command=tree.yview)
    yscroll.pack(side=RIGHT, fill="y")
    tree.configure(yscrollcommand=yscroll.set)

    up_btn = Button(wrapper3, text="Update", underline=0, command=update_author)
    add_btn = Button(wrapper3, text="Add New", underline=0, command=add_new)
    delete_btn = Button(wrapper3, text="Delete Author", underline=0, command=delete_author)
    save_btn = Button(wrapper3, text="Save", underline=0, command=save_author)
    add_btn.grid(row=4, column=0, padx=5, pady=3)
    up_btn.grid(row=4, column=1, padx=5, pady=3)
    delete_btn.grid(row=4, column=2, padx=5, pady=3)
    save_btn.grid(row=4, column=4, padx=5, pady=3)

    ent4.bind('<Tab>', key_press)
    add_btn.bind('<space>', add_new)
    add_btn.bind('<Return>', add_new)
    up_btn.bind('<space>', update_author)
    up_btn.bind('<Return>', update_author)
    delete_btn.bind('<space>', delete_author)
    delete_btn.bind('<Return>', delete_author)
    save_btn.bind('<space>', save_author)
    save_btn.bind('<Return>', save_author)

    cur.close()
    con.close()
