from tkinter import *
from tkinter.ttk import Treeview
import tkinter as tk
from tkinter import ttk, messagebox, font
from datetime import date, datetime, timedelta
from dateutil.parser import parse
from PIL import ImageTk, Image
import psycopg2
from tkinter import simpledialog



class Lending_Books:
    def __init__(self, master, table_name, *args):
        self.master = master
        self.root = tk.Toplevel(self.master)
        self.root.configure(background="gray56")
        self.root.title('Lending Books')
        self.root.state("zoomed")

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
        global add_rec
        add_rec = False

        # wrapper1
        self.wrapper1 = LabelFrame(self.root, text="Lending", bg="gray56")
        self.wrapper2 = LabelFrame(self.root, text="Data Entry", font=("Helvetica, 12"), height=40, bg="RoyalBlue1")
        self.wrapper3 = LabelFrame(self.root, text="", bg="blue4")
        self.wrapper1.pack(fill="both", expand="yes", padx=5, pady=3)
        self.wrapper2.pack(fill="both", expand="yes", padx=5, pady=3)
        self.wrapper3.pack(fill="both", expand="yes", padx=5, pady=3)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 11))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
        style.configure('mystyle.Treeview', rowheight=30, background="green",
                        fieldbackground="grey35", foreground="black")

        self.tree = Treeview(self.wrapper1, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), height=15, style ="mystyle.Treeview", selectmode='none')
        #self.tree['show']='headings'

        self.tree.heading("#0", text="")
        self.tree.heading("#1", text="Trans_ID")
        self.tree.heading("#2", text="Trans_Date")
        self.tree.heading("#3", text="Sub_ID")
        self.tree.heading("4", text="Sub_Name")
        self.tree.heading("#5", text="Item_Type")
        self.tree.heading("#6", text="Item_ID")
        self.tree.heading("#7", text="Title")
        self.tree.heading("#8", text="Author")
        self.tree.heading("#9", text="Price")
        self.tree.heading("#10", text="Due_Date")
        self.tree.heading("#11", text="Return_Date")
        self.tree.heading("#12", text="Charge")
        self.tree.column("#0", minwidth=20, width=50, stretch=NO)
        self.tree.column("#1", minwidth=0, width=100, stretch=NO)
        self.tree.column("#2", minwidth=0, width=130, stretch=NO)
        self.tree.column("#3", minwidth=0, width=80, stretch=NO)
        self.tree.column("#4", minwidth=0, width=230, stretch=NO)
        self.tree.column("#5", minwidth=0, width=110, stretch=NO)
        self.tree.column("#6", minwidth=0, width=85, stretch=NO)
        self.tree.column("#7", minwidth=0, width=400, stretch=NO)
        self.tree.column("#8", minwidth=0, width=300, stretch=NO)
        self.tree.column("#9", minwidth=0, width=75, stretch=NO)
        self.tree.column("#10", minwidth=0, width=120, stretch=NO)
        self.tree.column("#11", minwidth=0, width=130, stretch=NO)
        self.tree.column("#12", minwidth=0, width=85, stretch=NO)
        self.yscroll = ttk.Scrollbar(self.wrapper1, orient="vertical", command=self.tree.yview)
        self.yscroll.pack(side="right", fill="y", expand=False)
        #    self.yscroll.place(x=1880)
        im_checked = ImageTk.PhotoImage(Image.open('E://Python_Classes//GUI_FormsTraining//icons//checked.png'))
        im_unchecked = ImageTk.PhotoImage(Image.open('E://Python_Classes//GUI_FormsTraining//icons//unchecked.png'))
        self.tree.configure(yscrollcommand=self.yscroll.set)
        self.tree.tag_configure('checked', image=im_checked)
        self.tree.tag_configure('unchecked', image=im_unchecked)
        self.tree.pack(fill="both")

        # textvariables:
        self.sub_id = IntVar()
        self.sub_name = StringVar()
        self.trans_date = StringVar()
        self.item_type = StringVar()
        self.auth_name = StringVar()
        self.book_name = StringVar()
        self.book_id = IntVar()
        self.book_price = DoubleVar()
        self.iid = 0
        # wrapper2
        self.sub_id_lbl = Label(self.wrapper2, text="Sub_Id", font=("Helvetica, 10"))
        self.sub_id_lbl.grid(row=0, column=0, padx=5, pady=3)
        self.sub_id_box = Entry(self.wrapper2, textvariable=self.sub_id)
        self.sub_id_box.grid(row=0, column=1, padx=5, pady=3)
        self.sub_name_lbl = Label(self.wrapper2, text="Sub_Name", font=("Helvetica, 10"))
        self.sub_name_lbl.grid(row=1, column=0, padx=5, pady=3)
        self.sub_name_box = Entry(self.wrapper2, textvariable=self.sub_name)
        self.sub_name_box.grid(row=1, column=1, padx=5, pady=3)
        self.trans_date_lbl = Label(self.wrapper2, text="Lending Date", font=("Helvetica, 10"))
        self.trans_date_lbl.grid(row=2, column=0, padx=5, pady=3)
        self.trans_date_box = Entry(self.wrapper2, textvariable=self.trans_date)
        self.trans_date_box.grid(row=2, column=1, padx=5, pady=3)
        self.item_type_lbl = Label(self.wrapper2, text="Type", font=("Helvetica, 10"))
        self.item_type_lbl.grid(row=3, column=0, padx=5, pady=3)
        self.item_type_box = Entry(self.wrapper2, textvariable=self.item_type)
        self.item_type_box.grid(row=3, column=1, padx=5, pady=3)

        self.auth_name_lbl = Label(self.wrapper2, text="Author Name", font=("Helvetica, 10"))
        self.auth_name_lbl.grid(row=0, column=2, padx=5, pady=3)
        self.auth_name_box = Entry(self.wrapper2, textvariable=self.auth_name)
        self.auth_name_box.grid(row=0, column=3, padx=5, pady=3)
        self.book_name_lbl = Label(self.wrapper2, text="Title", font=("Helvetica, 10"))
        self.book_name_lbl.grid(row=1, column=2, padx=5, pady=3)
        self.book_name_box = Entry(self.wrapper2, textvariable=self.book_name)
        self.book_name_box.grid(row=1, column=3, padx=5, pady=3)
        self.book_id_lbl = Label(self.wrapper2, text="Book Id", font=("Helvetica, 10"))
        self.book_id_lbl.grid(row=2, column=2, padx=5, pady=3)
        self.book_id_box = Entry(self.wrapper2, textvariable=self.book_id)
        self.book_id_box.grid(row=2, column=3, padx=5, pady=3)
        self.book_price_lbl = Label(self.wrapper2, text="Price", font=("Helvetica, 10"))
        self.book_price_lbl.grid(row=3, column=2, padx=5, pady=3)
        self.book_price_box = Entry(self.wrapper2, textvariable=self.book_price)
        self.book_price_box.grid(row=3, column=3, padx=5, pady=3)
        self.lst_frame = Frame(self.wrapper2)
        self.lst_frame.grid(row=0, column=4, rowspan=10, padx=10, sticky=NS)
        self.lst = Listbox(self.lst_frame, height=15, width=50, relief=SUNKEN)
        self.lst_scrl = Scrollbar(self.lst_frame)
        self.lst_scrl.config(command=self.lst.yview)
        self.lst.config(yscrollcommand=self.lst_scrl.set)
        self.lst_scrl.pack(side=RIGHT, fill=Y)
        self.lst.pack(side=LEFT, expand=YES, fill=BOTH)
        self.alerts_frame = Frame(self.wrapper2, background="RoyalBlue1")
        self.alerts_frame.grid(row=0, column=5, columnspan=5, rowspan=10, padx=5, sticky=NSEW)

        self.lst_books=Listbox(self.alerts_frame, height=10, width=40, relief=SUNKEN)
        self.lst_books_scrl=Scrollbar(self.alerts_frame)
        self.lst_books_scrl.config(command=self.lst_books.yview)
        self.lst_books.config(yscrollcommand=self.lst_books_scrl.set)
        self.lst_books_scrl.pack(side=RIGHT, fill=Y)
        self.lst_books.pack(side=RIGHT, fill="both")
        self.charge = Label(self.alerts_frame, text=" ", bg="RoyalBlue1", font=('Arial Unicode MS', 12))
        self.charge.pack(padx=5, pady=3)
        self.overdue = Label(self.alerts_frame, text="                                                                                      ", bg="RoyalBlue1", font=('Arial Unicode MS', 12))
        self.overdue.pack(padx=5, pady=3)

        # self.lst.config(yscrollcommand=self.lst_scrl.set)
        # self.lst_scrl.config(command=self.lst.yview)

        # wrapper3
        helv12 = font.Font(family='Helvetica', size=12, weight=font.BOLD)
        self.add_btn = Button(self.wrapper3, text="Add", underline=0, font=helv12, bg="gray56",
                              command= lambda: self.add_lending())
        self.add_btn.grid(row=0, column=1, padx=10, pady=10)
        self.save_btn = Button(self.wrapper3, text="Save", underline=0, font=helv12, bg="gray56", state=DISABLED,
                               command=lambda: self.save_lending(add_rec))
        self.save_btn.grid(row=0, column=2, padx=10, pady=10)
        self.return_btn = Button(self.wrapper3, text="Return Confirm", underline=0, font=helv12, bg="gray56", state=DISABLED,
                                 command=lambda: self.return_confirm())
        self.return_btn.grid(row=0, column=3, padx=10, pady=10)

        self.delete_btn = Button(self.wrapper3, text="Delete", underline=0, font=helv12, bg="gray56",
                                 command=lambda: self.delete_trans())
        self.delete_btn.grid(row=0, column=4, padx=10, pady=10)
        self.clr_btn = Button(self.wrapper3, text="Clear", underline=0, font=helv12, bg="gray56",
                              command=lambda: self.clr())
        self.clr_btn.grid(row=0, column=5, padx=10, pady=10)
        self.quit_btn = Button(self.wrapper3, text="Quit", underline=0, font=helv12, bg="gray56",
                               command=self.quit_window)
        self.quit_btn.grid(row=0, column=6, padx=10, pady=10)

        query = 'select max(trans_id) from lending'
        cur.execute(query)
        last_trans = cur.fetchall()
        query = 'select * from lending where trans_id=%s and return_date is NULL'
        cur.execute(query, last_trans)
        rows = cur.fetchall()
        self.update(rows)




        self.tree.bind('<Button 1>', self.togglecheck)
        self.root.bind('<Control-q>', self.quit_window)
        self.root.bind('<Control-c>', self.clr)
        self.root.bind('<Control-a>', self.add_lending)
        self.root.bind('<Control-s>', self.save_lending)
        self.root.bind('<Control-r>', self.return_confirm)
        self.sub_id_box.bind('<Return>', self.get_sub_name)
        self.trans_date_box.bind('<Return>', self.key_press)
        self.item_type_box.bind('<Return>', self.key_press)
        self.auth_name_box.bind('<Return>', self.key_press)
        self.book_name_box.bind('<Return>', self.key_press)
        self.auth_name_box.bind('<KeyRelease>', self.get_auth_list)
        self.book_name_box.bind('<KeyRelease>', self.get_title_list)
        self.root.bind('<Down>', self.lst_up)
        self.root.bind('<Up>', self.lst_up)
        self.root.bind('<Prior>', self.lst_up)
        self.root.bind('<Next>', self.lst_up)
        self.tree.bind('<Delete>', self.del_row)
        self.tree.bind('<Double-Button-1>', self.get_row)
        self.root.mainloop()




    def get_row(self, event):
        #rowId = self.tree.identify_row(event.y)
        item = self.tree.item(self.tree.focus())
        self.trans_date.set(item['values'][1])
        self.item_type.set(item['values'][4])
        self.book_name.set(item['values'][5])
        self.auth_name.set(item['values'][6])
        self.book_price.set(item['values'][7])


    def del_row(self, *ignore):
        selected_row = self.tree.selection()[0]
        self.tree.delete(selected_row)


    def lst_up(self, event):
        if self.lst.size() > 0:
            x = self.lst.index(self.lst.curselection())
            if event.keysym == "Down":
                if self.lst.index(self.lst.curselection()) + 1 < self.lst.size():
                    x += 1
                self.lst.select_clear(0, END)
                self.lst.select_set(self.lst.index(x))
                self.lst.see(self.lst.index(x))
            elif event.keysym == "Up":
                if self.lst.index(self.lst.curselection()) - 1 >= 0:
                    x -= 1
                    self.lst.select_clear(0, END)
                    self.lst.select_set(self.lst.index(x))
                    self.lst.see(self.lst.index(x))
            elif event.keysym == "Prior":
                if self.lst.index(self.lst.curselection()) - 15 >= 0:
                    x -= 15
                    self.lst.select_clear(0, END)
                    self.lst.select_set(self.lst.index(x))
                    # print(x)
                else:
                    x = 0
                    self.lst.select_clear(0, END)
                    self.lst.select_set(self.lst.index(0))
                self.lst.see(self.lst.index(x))
            elif event.keysym == "Next":
                x = self.lst.index(self.lst.curselection())
                if self.lst.index(self.lst.curselection()) + 15 < self.lst.size():
                    x += 15
                    self.lst.select_clear(0, END)
                    self.lst.select_set(self.lst.index(x))
                    # print(x)
                else:
                    x = self.lst.size() - 1
                    self.lst.select_clear(0, END)
                    self.lst.select_set(self.lst.index(x))
                self.lst.see(self.lst.index(x))

    def get_title_list(self, event, *ignore):
        if event.keysym not in ("Down", "Up", "Prior", "Next"):
            q = self.book_name_box.get()

            self.lst.delete(0, END)
            a = self.auth_name.get()
            query = f"select book_name from books where author_name='{a}' and booK_name ilike '{q}%' order by book_name"
            cur.execute(query)
            rows = cur.fetchall()
            for i in rows:
                self.lst.insert("end", i[0])
            self.lst.selection_set(0)

    def get_auth_list(self, event, *ignore):
        if event.keysym not in ("Down", "Up", "Prior", "Next"):
            q = self.auth_name_box.get()
            self.lst.delete(0, END)
            query = "select author_name from author where author_name ilike '" + q + "%'" + " order by author_name"
            cur.execute(query)
            rows = cur.fetchall()
            for i in rows:
                self.lst.insert("end", i[0])
            self.lst.selection_set(0)
        # children = self.tree.get_children()
        # self.tree.selection_set(children)
        # self.tree.selection_toggle(children[1:])

    def key_press(self, event):
        x = str(event.widget)
        self.trans_date.set(self.trans_date_box.get())
        if x == ".!toplevel.!labelframe2.!entry3":
            date_string = self.trans_date.get()
            date_format = "%Y-%m-%d"
            #if datetime.strptime(date_string, date_format):
            #if isinstance(self.trans_date.get(),(datetime.date)):
            if parse(self.trans_date.get(),fuzzy=False):
                self.item_type.set("Book")
                self.item_type_box.select_range(0, END)
                self.item_type_box.focus()
            else:
                messagebox.showinfo("", "Enter valid date", parent=self.root)
        elif x == ".!toplevel.!labelframe2.!entry4":
            if self.item_type_box.get() == "Book" or self.item_type_box.get() == "DVD":
                self.auth_name_box.focus()
            else:
                messagebox.showinfo("", "Select only Book or DVD", parent=self.root)
        elif x == ".!toplevel.!labelframe2.!entry5":
            self.auth_name.set(self.lst.selection_get())
            self.lst.delete(0, END)
            self.book_name_box.focus()
        elif x == ".!toplevel.!labelframe2.!entry6":
            self.book_name.set(self.lst.selection_get())
            query = f"select trans_date from lending where subscriber_id={self.sub_id.get()} and author_name='{self.auth_name.get()}' and book_name='{self.book_name.get()}'"
            query2 = f"select trans_date, subscriber_name from lending where author_name='{self.auth_name.get()}' and book_name='{self.book_name.get()}' and return_date is NULL"
            cur.execute(query)
            rows=cur.fetchall()
            cur.execute(query2)
            check_holder=cur.fetchall()
            if len(check_holder)>0:
                if messagebox.askyesno("", f"இந்தப் புத்தகத்தை {check_holder[0][1]} {((check_holder[0][0]).strftime('%d-%m-%y'))} அன்று எடுத்துள்ளார். இன்னும் திருப்பவில்லை; தொடரவா?", parent=self.root):
                    if len(rows)>0:
                        font1=font.Font(name='TkCaptionFont', exists=True)
                        font1.config(family='Arial Unicode MS', size=15)
                        if messagebox.askyesno("Read", f"இந்தப் புத்தகத்தை நீங்கள் {rows[0][0]} அன்று வாங்கிச் சென்றுள்ளீர்கள். திரும்பவும் வேண்டுமா?", parent=self.root):
                            self.book_details()
                        else:
                            self.auth_name_box.focus()
                    else:
                        self.book_details()
                else:
                    self.auth_name_box.focus()
            else:
                if len(rows) > 0:
                    font1 = font.Font(name='TkCaptionFont', exists=True)
                    font1.config(family='Arial Unicode MS', size=15)
                    if messagebox.askyesno("Read",
                                           f"இந்தப் புத்தகத்தை நீங்கள் {rows[0][0]} அன்று வாங்கிச் சென்றுள்ளீர்கள். திரும்பவும் வேண்டுமா?",
                                           parent=self.root):
                        self.book_details()
                    else:
                        self.auth_name_box.focus()
                else:
                    self.book_details()

    def book_details(self):
        self.lst.delete(0, END)
        query = f"select book_id, price from books where author_name='{self.auth_name.get()}' and book_name='{self.book_name.get()}'"
        cur.execute(query)
        id = cur.fetchall()
        self.book_id.set(id[0][0])
        self.book_price.set(id[0][1])
        query = f'select max(trans_id)+1 from lending'
        cur.execute(query)
        trans_id = cur.fetchall()
        self.tree.insert('', index='end', iid=self.iid, text="", values=(
            trans_id[0][0], self.trans_date.get(), self.sub_id.get(), self.sub_name.get(), self.item_type.get(),
            self.book_id.get(), self.book_name.get(), self.auth_name.get(), self.book_price.get(),
            (datetime.strptime(self.trans_date.get(), '%Y-%m-%d') + timedelta(days=30)).date(), 'None',
            (self.book_price.get()) / 10), tags="unchecked")
        self.iid += 1
        if self.save_btn["state"]== DISABLED:
            self.save_btn["state"]= NORMAL

        query = f"select book_id, book_name from books where author_name='{self.auth_name.get()}'"
        query2 = f"select item_id, book_name from lending where subscriber_id={self.sub_id.get()}"
        cur.execute(query)
        first_result = cur.fetchall()
        cur.execute(query2)
        second_result = cur.fetchall()
        if len(second_result)>0:
            self.lst_books.delete(0, END)
            lst_array =[]
            for i in first_result:
                read = False
                for j in second_result:
                    if i[0]==j[0]:
                        read=True
                        break
                if not read:
                    lst_array.append(i[1])
                    #self.lst_books.insert("end", i[1])
            lst_array.sort()
            self.lst_books.insert("end", *lst_array)
        else:
            self.lst_books.insert("end", "None read")

        self.auth_name.set("")
        self.book_name.set("")
        self.book_id.set("")
        self.book_price.set("")
        self.item_type_box.focus()
        self.item_type_box.select_range(0, END)


    def get_sub_name(self, event):
        global add_rec
        if int(self.sub_id_box.get()):
            query = 'select subscriber_name from subscriber where subscriber_id=' + self.sub_id_box.get()
            cur.execute(query)
            rows = cur.fetchall()
            if len(rows) == 0:
                messagebox.showinfo("","Invalid Subscriber ID", parent=self.root)
            else:
                self.return_btn["state"]=NORMAL
                self.overdue.config(text="", background="RoyalBlue1")
                self.charge.config(text="", background="RoyalBlue1")
                self.sub_name.set(rows[0][0])
                self.tree.delete(*self.tree.get_children())
                query=f'select * from lending where subscriber_id={self.sub_id_box.get()} and return_date is NULL'
                cur.execute(query)
                rows = cur.fetchall()

                if len(rows)>0:
                    self.update(rows)
                    children=self.tree.get_children()
                    counter=0
                    for child in children:
                        if (date.today()-parse(str(self.tree.item(child, "values")[9])).date()).days >0:
                            counter+=1
                    if counter>0:
                        self.overdue.config(text=f"கவனம்!!! {counter} புத்தகங்கள் கடைசிநாளைத் தாண்டிவிட்டன!", bg='firebrick1')
                    if add_rec == True:
                        self.trans_date.set(date.today())
                        self.trans_date_box.select_range(0, END)
                        self.trans_date_box.focus()
                else:
                    if add_rec==False:
                        messagebox.showinfo("","No record found", parent=self.root)
                    else:
                        self.trans_date.set(date.today())
                        self.trans_date_box.select_range(0, END)
                        self.trans_date_box.focus()

    def add_lending(self, *ignore):
        global add_rec
        add_rec=True
        self.overdue.config(text="")
        self.charge.config(text="")
        self.tree.delete(*self.tree.get_children())
        self.sub_id_box.delete(0, END)
        self.sub_name_box.delete(0, END)
        self.trans_date_box.delete(0, END)
        self.item_type_box.delete(0, END)
        self.auth_name_box.delete(0, END)
        self.book_name_box.delete(0, END)
        self.book_id_box.delete(0, END)
        self.book_price_box.delete(0, END)
        self.iid = 0
        self.return_btn["state"]=DISABLED
        self.sub_id_box.focus()

    def save_lending(self, add_record, *ignore):
        global add_rec
        if add_rec:
            if messagebox.askyesno("Confirm Save", "Do you really want to save?", parent=self.root):
                query=f"select max(trans_id)+1 from lending"
                cur.execute(query)
                trans_id=cur.fetchall()
                children = self.tree.get_children()
                for child in children:
                    tag = self.tree.item(child, "tags")[0]
                    if tag=="unchecked" and int(self.tree.item(child, 'values')[0])==int(trans_id[0][0]):
                        a=self.tree.item(child)
                        query="insert into lending(trans_id, trans_date, subscriber_id, subscriber_name, item_type, item_id, book_name, author_name, book_price, due_date, return_date, charge) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL, NULL)"
                        cur.execute(query, (a['values'][0], a['values'][1], a['values'][2], a['values'][3], a['values'][4], a['values'][5], a['values'][6], a['values'][7], a['values'][8], a['values'][9]))
                        con.commit()
                if self.return_btn["state"]==DISABLED:
                    self.return_btn["state"]=NORMAL
                self.tree.delete(*self.tree.get_children())
                self.sub_id.set(0)
                self.sub_name.set("")
                self.trans_date.set("")
                self.item_type.set("")
                self.auth_name.set("")
                self.book_name.set("")
                self.book_id.set(0)
                self.book_price.set(0)
                add_rec=False

    def clr(self, *ignore):
        self.tree.delete(*self.tree.get_children())

    def delete_trans(self, *ignore):
        if self.sub_id_box.get()!="0" and len(self.sub_id_box.get())>0 and self.sub_id_box.get().isnumeric():
            query =f"select * from lending where subscriber_id={self.sub_id.get()} and return_date is NULL"
            cur.execute(query)
            x=cur.fetchall()
            if len(x)>0:
                if messagebox.askyesno("Confirmation", "Do you really want to delete record?", parent=self.root):
                    children = self.tree.get_children()
                    check_counter=0
                    for child in children:
                        tag = self.tree.item(child, "tags")[0]
                        if tag == "checked":
                            check_counter+=1
                            query= f"delete from lending where trans_id={self.tree.item(child, 'values')[0]} and book_name='{self.tree.item(child,'values')[6]}'"
                            cur.execute(query)
                            con.commit()
                            query = f"select * from lending where subscriber_id={self.sub_id.get()} and return_date is NULL"
                            cur.execute(query)
                            x = cur.fetchall()
                            self.update(x)
                    if check_counter==0:
                        messagebox.showinfo("","You need to select record to delete", parent=self.root)

    def update(self, rows):

        self.tree.delete(*self.tree.get_children())

        self.tree.tag_configure(('unchecked', 'overdue'),  foreground='red', background='red')
        for i in rows:
            if i[11] is not None:
                tags="checked"
            else:
                if (parse(str(i[9])).date() - date.today()).days < 0:
                   tags=("unchecked", "overdue")
                else:
                    tags="unchecked"
            self.tree.insert('', 'end', values=i, tags=tags)

        for i in self.tree.get_children():
            if self.tree.item(i, "tags")[0]=="overdue":
                print("its unchecked")
            #if (parse(self.tree.item(i,tags='unchecked')[9]).date()-date.today()).days<0:
             #   self.tree.item(i,tags='overdue')


    def togglecheck(self, event):
        rowid = self.tree.identify_row(event.y)
        if len(rowid)>0:
            tag = self.tree.item(rowid, "tags")[0]
            tags = list(self.tree.item(rowid, "tags"))
            tags.remove(tag)
            self.tree.item(rowid, tags=tags)
            if tag == "checked":
                self.tree.item(rowid, tags="unchecked")
            else:
                self.tree.item(rowid, tags="checked")
            self.tree.selection_set(self.tree.get_children())
            for i in self.tree.selection():
                tag = self.tree.item(i, "tags")[0]
                if tag == 'unchecked':
                    self.tree.selection_toggle(i)


    def return_confirm(self, *ignore):
        # for i in self.tree.get_children():
        #   tag = self.tree.item(i, "tags")[0]
        valid_date=False
        while not valid_date:
            return_date = simpledialog.askstring(title="Return Date", prompt="திருப்பிய தேதியை உள்ளிடவும் (dd/mm/yy)",
                                                 initialvalue=f"{datetime.today().strftime('%d/%m/%y')}",
                                                 parent=self.root)
            try:
                if datetime.strptime(return_date, "%d/%m/%y"):
                    valid_date=True
                    total_charge=0.00
                    #return_date=date.today()
                    self.tree.selection_set(self.tree.tag_has("checked"))
                    if self.tree.selection():
                        for i in self.tree.selection():
                            itext = self.tree.item(i)
                            val = itext['values']
                            if val[10] =="None":
                                val[10] = date.today()
                                return_date=date.today()
                                borrow_date = parse(val[1]).date()
                                one_due=(float(val[8])/10)
                                additional_days = (date.today() - borrow_date).days - 30
                                if additional_days>0:
                                    additional_charge=(((float(val[8])*5)/100)/30)*additional_days
                                    val[11] =round(one_due+additional_charge,2)
                                else:
                                    val[11]=round(one_due,2)
                                total_charge=total_charge+val[11]
                                query = f'UPDATE lending SET trans_date=%s, subscriber_id=%s, subscriber_name=%s, item_type=%s, item_id=%s, book_name=%s, author_name=%s, book_price=%s, due_date=%s, return_date=%s, charge=%s WHERE trans_id={val[0]} and item_id={val[5]}'
                                cur.execute(query,
                                (val[1], int(val[2]), val[3], val[4], int(val[5]), val[6], val[7], float(val[8]), val[9],
                                val[10], val[11]))
                                con.commit()
                        self.charge.config(text=f"கட்டணம்: {total_charge}", bg='firebrick1')
                        query = f"select * from lending where subscriber_id={self.sub_id.get()} and (return_date is NULL or return_date='{return_date}')"
                        cur.execute(query)
                        rows=cur.fetchall()
                        self.update(rows)
                        self.tree.selection_set(self.tree.get_children())
                        for i in self.tree.selection():
                            tag = self.tree.item(i, "tags")[0]
                            if tag=='unchecked':
                                self.tree.selection_toggle(i)
                        break
                    else:
                        messagebox.showinfo("", "திருப்பும் புத்தகங்களை முதலில் தேர்வுசெய்க", parent=self.root)
            except:
                continue
            finally:
                if return_date is None:
                    messagebox.showinfo("திருப்பம்", "புத்தகம் எதுவும் திருப்பப்படவில்லை", parent=self.root)
                    break
                else:
                    if valid_date:
                        messagebox.showinfo("கட்டணம்", f"திருப்பிய புத்தகங்களுக்கான கட்டணம்: {total_charge}", parent=self.root)
                    else:
                        messagebox.showinfo("தேதி", "தேதி சரியான வடிவில் இல்லை!", parent=self.root)





    def quit_window(self, *ignore):
        # self.root.quit()
        self.root.destroy()
        cur.close()
        con.close()
