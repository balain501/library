from tkinter import *
from tkinter.ttk import Treeview
import tkinter as tk
from tkinter import ttk, messagebox, font
from datetime import date, datetime, timedelta
from dateutil.parser import parse
from PIL import ImageTk, Image
import psycopg2
from tkinter import simpledialog
from tkcalendar import Calendar


class CashBook:
    def __init__(self, master, table_name, *args):
        self.master = master
        self.root = tk.Toplevel(self.master)
        self.root.configure(background="gray56")
        self.root.title('Cash Book')
        x = self.master.winfo_x()
        y = self.master.winfo_y()
        self.root.geometry("1320x755+%d+%d" % (x, y + 212))

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
        global get_key
        get_key = ''
        global add_record
        add_record = True

        self.wrapper1 = LabelFrame(self.root, text="Today's entries", bg="red2")
        self.wrapper2 = LabelFrame(self.root, text="Search", bg="light goldenrod")
        self.wrapper3 = LabelFrame(self.root, text="Data Entry", bg="purple4")
        self.wrapper1.pack(fill="both", expand="yes", padx=3, pady=3)
        self.wrapper2.pack(fill="both", expand="yes", padx=3, pady=3)
        self.wrapper3.pack(fill="both", expand="yes", padx=3, pady=3)

        #Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 11))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
        style.configure('mystyle.Treeview', rowheight=20, background="green",
                        fieldbackground="grey35", foreground="black")
        self.tree = Treeview(self.wrapper1, columns=(1, 2, 3, 4, 5, 6), height=10,
                             style="mystyle.Treeview")
        self.tree['show'] = 'headings'
        self.tree.heading(1, text="Trans_ID")
        self.tree.heading(2, text="Trans_Date")
        self.tree.heading(3, text="Heading")
        self.tree.heading(4, text="Sub_Heading")
        self.tree.heading(5, text="Debit")
        self.tree.heading(6, text="Credit")

        self.yscroll = ttk.Scrollbar(self.wrapper1, orient="vertical", command=self.tree.yview)
        self.yscroll.pack(side="right", fill="y", expand=False)
        self.tree.configure(yscrollcommand=self.yscroll.set)

        # wrapper2
        self.trans_date = StringVar()
        self.trans_id = IntVar()
        self.main_head = StringVar()
        self.sub_head = StringVar()
        self.debit = DoubleVar()
        self.credit = DoubleVar()
        self.search_name = StringVar()
        self.search_date = StringVar()

        helv12 = font.Font(family='Helvetica', size=12, weight=font.BOLD)
        self.lbl = Label(self.wrapper2, text="Sub Head")
        self.lbl.grid(row=0, column=0, padx=3, pady=3)
        self.txt1 = Entry(self.wrapper2, textvariable=self.search_name)
        self.txt1.grid(row=0, column=1, padx=3, pady=3)
        self.lbl2 = Label(self.wrapper2, text="Date")
        self.lbl2.grid(row=1, column=0, padx=3, pady=3)
        self.txt2 = Entry(self.wrapper2, textvariable=self.search_date)
        self.txt2.grid(row=1, column=1, padx=3, pady=3)
        self.search_btn = Button(self.wrapper2, text="Search", underline=0, font=helv12, bg="gray56",
                                 command=lambda: self.search_entries())
        self.search_btn.grid(row=1, column=2, padx=3, pady=3)
        self.tree.pack(fill="both", expand=TRUE)
        self.cal = Calendar(self.wrapper2,
                            font="Arial 14", selectmode='day',
                            cursor="hand1", year=date.today().year, month=date.today().month, day=date.today().day)
        self.cal.grid(row=0, column=3, padx=1, pady=1, rowspan=15, columnspan=3)
        self.month_btn = Button(self.wrapper2, text="Monthly Total", underline=0, font=helv12, bg="gray56",
                                command=lambda: self.monthly_entries())
        self.month_btn.grid(row=2, column=6, padx=3, pady=3)
        self.year_btn = Button(self.wrapper2, text="Yearly Total", underline=0, font=helv12, bg="gray56",
                               command=lambda: self.yearly_entries())
        self.year_btn.grid(row=3, column=6, padx=3, pady=3)

        # wrapper3
        self.lbl1 = Label(self.wrapper3, text="Trans_Id")
        self.lbl1.grid(row=0, column=0, sticky=W)
        self.ent1 = Entry(self.wrapper3, textvariable=self.trans_id, relief="groove", justify="right", bd=5,
                          bg="light blue",
                          state=DISABLED)
        self.ent1.grid(row=0, column=1, padx=1, pady=1)
        self.lbl2 = Label(self.wrapper3, text="Trans_Date")
        self.lbl2.grid(row=1, column=0, padx=1, pady=1, sticky=W)
        self.ent2 = Entry(self.wrapper3, textvariable=self.trans_date, relief="groove", bd=5)
        self.ent2.grid(row=1, column=1, padx=1, pady=1)
        self.lbl3 = Label(self.wrapper3, text="Header")
        self.lbl3.grid(row=2, column=0, padx=1, pady=1, sticky=W)
        self.combo = ttk.Combobox(self.wrapper3, textvariable=self.main_head, width=18, state="readonly")
        self.combo.grid(row=2, column=1, padx=1, pady=1)
        self.category = ['Library', 'Browsing', 'Books sales', 'Comics', 'Project works', 'General exp.',
                         'Capital exp.', 'Other source income', 'Drawings']
        self.combo['values'] = sorted(self.category)

        # self.ent3 = Entry(self.wrapper3, textvariable=self.main_head, relief="groove", bd=5)
        # self.ent3.grid(row=2, column=1, padx=1, pady=1)
        self.lbl4 = Label(self.wrapper3, text="Sub Head")
        self.lbl4.grid(row=3, column=0, padx=1, pady=1, sticky=W)
        self.ent4 = Entry(self.wrapper3, textvariable=self.sub_head, relief="groove", bd=5)
        self.ent4.grid(row=3, column=1, padx=1, pady=1)
        self.lbl5 = Label(self.wrapper3, text="Debit")
        self.lbl5.grid(row=0, column=2, padx=1, pady=1, sticky=W)
        self.ent5 = Entry(self.wrapper3, textvariable=self.debit, relief="groove", bd=5)
        self.ent5.grid(row=0, column=3, padx=1, pady=1)
        self.lbl6 = Label(self.wrapper3, text="Credit")
        self.lbl6.grid(row=1, column=2, padx=1, pady=1, sticky=W)
        self.ent6 = Entry(self.wrapper3, textvariable=self.credit, relief="groove", bd=5)
        self.ent6.grid(row=1, column=3, padx=1, pady=1)

        # buttons-wrapper3
        self.add_btn = Button(self.wrapper3, text="Add New", underline=0, font=helv12,
                              command=self.add_new)
        self.add_btn.grid(column=5, row=0, padx=2, pady=2, sticky=EW)
        self.up_btn = Button(self.wrapper3, text="Update", underline=0, font=helv12,
                             command=self.update_cash)
        self.up_btn.grid(column=6, row=0, padx=2, pady=2, sticky=EW)
        self.save_btn = Button(self.wrapper3, text="Save", underline=0, font=helv12, command=self.save_cash)
        self.save_btn.grid(column=7, row=0, padx=2, pady=2, sticky=EW)
        self.delete_btn = Button(self.wrapper3, text="Delete ", underline=0, font=helv12,
                                 command=self.delete_entry)
        self.delete_btn.grid(column=5, row=1, padx=2, pady=2, sticky=EW)
        self.exit_btn = Button(self.wrapper3, text="Quit", underline=0, font=helv12,
                               command= self.root.destroy)
        self.exit_btn.grid(column=6, row=1, padx=2, pady=2, sticky=EW)

        self.root.bind('<Control-e>', self.search_entries)
        self.root.bind('<Control-q>', lambda e: self.root.destroy())
        self.ent2.bind('<Tab>', self.key_press)
        self.ent5.bind('<KeyRelease>', self.debit_credit_condition)
        self.ent6.bind('<KeyRelease>', self.debit_credit_condition)
        self.root.bind('<Return>', self.key_press)
        self.root.bind('<Control-s>', self.save_cash)
        self.root.bind('<Control-a>', self.add_new)
        self.root.bind('<Control-u>', lambda e: self.update_cash)
        self.root.bind('<Control-d>', lambda e: self.delete_entry())
        self.add_btn.bind('<space>', self.add_new)
        self.add_btn.bind('<Return>', self.add_new)
        self.save_btn.bind('<space>', self.save_cash)
        self.save_btn.bind('<Return>', self.save_cash)
        self.up_btn.bind('<space>', self.update_cash)
        self.up_btn.bind('<Return>', self.update_cash)
        self.delete_btn.bind('<space>', self.delete_entry)
        self.delete_btn.bind('<Return>', self.delete_entry)
        self.combo.bind('<Key>', self.key_press)
        self.tree.bind('<Double 1>', self.get_row)
        self.cal.bind('<<CalendarSelected>>', self.date_pick)

        self.add_new()
        self.root.mainloop()

    def key_press(self, event):
        global get_key
        global add_record
        x = str(event.widget)
        if x == '.!toplevel.!labelframe3.!entry2':
            self.combo.current(1)
            self.combo.focus()
            get_key = ''
        if x == '.!toplevel.!labelframe3.!combobox':
            if event.keycode == 8:
                get_key = get_key[:-1]
            if event.keycode != 16:
                if (event.keycode > 64 and event.keycode < 91) or (event.keycode > 96 and event.keycode < 123):
                    get_key = get_key + event.char
                    # result = [i for i in self.category if i.startswith(event.char.upper())]
                    result = [i for i in self.category if i.lower().startswith(get_key)]
                    if len(result) > 0:
                        self.combo.set(result[0])
                    else:
                        self.combo.current(1)
            if event.keycode == 13:
                get_key=''
                self.ent4.focus()
        if x == '.!toplevel.!labelframe3.!entry3' and len(self.ent4.get()) > 0:
            self.ent5.select_range(0, END)
            self.ent5.focus()
        if x == '.!toplevel.!labelframe3.!entry4' and len(self.ent5.get())>0:
            self.ent6.select_range(0, END)
            self.ent6.focus()
        if x == '.!toplevel.!labelframe3.!entry5' and len(self.ent6.get())>0:
            if self.credit.get() > 0:
                if add_record==False:
                    self.up_btn.focus()
                else:
                    self.save_btn.focus()
            else:
                if self.debit.get() == 0:
                    messagebox.showinfo("", "பற்றும் வரவும் சுழியமாக இருக்கமுடியாது", parent=self.root)
                else:
                    if add_record == False:
                        self.up_btn.focus()
                    else:
                        self.save_btn.focus()


    def debit_credit_condition(self, event):
        x=str(event.widget)
        if x == '.!toplevel.!labelframe3.!entry4':
            if (event.keycode > 64 and event.keycode < 91) or (event.keycode > 96 and event.keycode < 123):
                self.debit.set(0.00)
                self.ent5.select_range(0, END)
        elif x == '.!toplevel.!labelframe3.!entry5':
            if (event.keycode > 64 and event.keycode < 91) or (event.keycode > 96 and event.keycode < 123):
                self.credit.set(0.00)
                self.ent6.select_range(0, END)



    def date_pick(self, *ignore):
        self.search_name.set("")
        self.search_date.set("")
        query = f"select * from cash_book where trans_date='{self.cal.selection_get()}'"
        cur.execute(query)
        rows = cur.fetchall()
        self.update(rows)

    def monthly_entries(self):
        query = f"select header, sum(debit), sum(credit) from cash_book where extract (month from trans_date) = '{self.cal.get_displayed_month()[0]}' and extract (year from trans_date) = '{self.cal.get_displayed_month()[1]}' group by header"
        cur.execute(query)
        rows = cur.fetchall()
        # print(rows)
        self.month_year(rows)

    def yearly_entries(self):
        query = f"select header, sum(debit), sum(credit) from cash_book where extract (year from trans_date) = '{self.cal.get_displayed_month()[1]}' group by header"
        cur.execute(query)
        rows = cur.fetchall()
        # print(rows)
        self.month_year(rows)

    def month_year(self, rows):
        debit_sum = 0.00
        credit_sum = 0.00
        self.tree.delete(*self.tree.get_children())
        for i in rows:
            self.tree.insert('', 'end', values=('', '', '', i[0], i[1], i[2]))
            debit_sum += float(i[1])
            credit_sum += float(i[2])
        self.tree.insert('', 'end', values=('', '', '', 'Total', debit_sum, credit_sum))

    def search_entries(self):
        if len(self.txt2.get()) == 0:
            query = f"select * from cash_book where sub_head ilike '{self.search_name.get()}%' order by trans_id desc"
        else:
            query = f"select * from cash_book where sub_head ilike '{self.search_name.get()}%' and trans_date= TO_DATE('{self.search_date.get()}', 'dd/mm/yy') order by trans_id desc"
        cur.execute(query)
        rows = cur.fetchall()
        self.update(rows)

    def update(self, rows):
        self.tree.delete(*self.tree.get_children())
        debit_sum = 0.00
        credit_sum = 0.00
        for i in rows:
            self.tree.insert('', 'end', values=i)
            debit_sum += float(i[4])
            credit_sum += float(i[5])
        self.tree.insert('', 'end', values=('', '', '', 'Total', debit_sum, credit_sum))

    def add_new(self, *ignore):
        self.save_btn["state"]=NORMAL
        self.up_btn["state"]=DISABLED
        query = f"select max(trans_id)+1 from cash_book"
        cur.execute(query)
        id = cur.fetchone()
        self.trans_id.set(id[0])
        self.trans_date.set(date.today().strftime("%d/%m/%y"))
        self.ent2.select_range(0, END)
        self.ent2.focus()

    def update_cash(self):
        query = f"update cash_book set trans_date='{datetime.strptime(self.trans_date.get(), '%d/%m/%y').date()}', header='{self.main_head.get()}', sub_head='{self.sub_head.get()}', debit={self.debit.get()}, credit={self.credit.get()} where trans_id={self.trans_id.get()}"
        cur.execute(query)
        con.commit()
        query = f"select * from cash_book where trans_date=current_date"
        cur.execute(query)
        rows = cur.fetchall()
        self.update(rows)

    def save_cash(self, *ignore):
        global add_record
        if add_record==True:
            if self.debit.get()>0 or self.credit.get()>0 and len(self.ent5.get())>0 and len(self.ent6.get()>0):
                query = f"insert into cash_book(trans_id, trans_date, header, sub_head, debit, credit) values(%s, %s, %s, %s, %s, %s)"
                cur.execute(query, (
                self.trans_id.get(), datetime.strptime(self.trans_date.get(), "%d/%m/%y").date(), self.main_head.get(),
                self.sub_head.get(), self.debit.get(), self.credit.get()))
                con.commit()
                query = f"select * from cash_book where trans_date=current_date"
                cur.execute(query)
                rows = cur.fetchall()
                self.update(rows)
                add_record = False
            else:
                messagebox.showinfo("", "பத்திகளை முழுமையாக நிரப்பிவிட்டு முயலவும்", parent=self.root)

    def get_row(self, event):
        global add_record
        add_record = False
        self.save_btn["state"]=DISABLED
        self.up_btn["state"]=NORMAL
        item = self.tree.item(self.tree.focus())
        self.trans_id.set(item['values'][0])
        self.trans_date.set(datetime.strptime(item['values'][1], ('%Y-%m-%d')).strftime('%d/%m/%y'))
        self.main_head.set(item['values'][2])
        self.sub_head.set(item['values'][3])
        self.debit.set(item['values'][4])
        self.credit.set(item['values'][5])
        self.ent1["state"] = DISABLED
        self.ent2.select_range(0, END)
        self.ent2.focus()

    def delete_entry(self):
        if self.trans_id.get()>0:
            query=f'select * from cash_book where trans_id={self.trans_id.get()}'
            cur.execute(query)
            rows=cur.fetchall()
            if len(rows)>0:
                if messagebox.askyesno("Confirmation", "இந்தப் பதிவை நிச்சயமாக நீக்க வேண்டுமா?", parent=self.root):
                    query=f'delete from cash_book where trans_id={self.trans_id.get()}'
                    cur.execute(query)
                    con.commit()
                    query=f'select * from cash_book where trans_date=current_date'
                    cur.execute(query)
                    rows=cur.fetchall()
                    self.update(rows)
            else:
                messagebox.showinfo("", "இந்த எண்ணில் எந்தப் பதிவும் இல்லை", parent=self.root)
