from tkinter import *
import sqlite3
from employee import Employee
from tkinter import font
from tkinter import messagebox


# when removing  employees, check if employee exists before showing the success label

# also add the ability to remove employees with a right click in the listbox





#_______________________________________________________________________________________________________________tkinter window____#

window = Tk()
window.title("Employee Database")
window.iconbitmap('c:/Users/matol/Desktop/Databases/db.ico')
window.configure(bg="#9d9e91")#b8b8b8
window.resizable(False, False)
myFont = font.Font(family='OCR A Extended')


#___________________________________________________________________________________________________frame variable declaration____#

frameR = LabelFrame(window, background="#9e9e9e", relief=RAISED)

frameNW = LabelFrame(window, height=250, background="cornflower blue", relief=RAISED)

frameSW = LabelFrame(window, height=250, relief=RAISED, font=myFont, bg="violetRed4")

l1 = Label(frameSW, font=myFont, text="REMOVE EMPLOYEES", fg="violetRed4", bg="violetred4")
l11 = Label(frameSW, font=myFont, text="REMOVE EMPLOYEES", bg="violetred4")
l111 = Label(frameSW, font=myFont, text="REMOVE EMPLOYEES", fg="violetRed4", bg="violetred4")

l2 = Label(frameNW, font=myFont, text="  ADD EMPLOYEES ", fg="cornflower blue", bg="cornflower blue")
l22 = Label(frameNW, font=myFont, text="  ADD EMPLOYEES ", bg="cornflower blue")
l222 = Label(frameNW, font=myFont, text="  ADD EMPLOYEES ", fg="cornflower blue", bg="cornflower blue")


#_________________________________________________________________________________________________________________________________#

conn = sqlite3.connect('EMPDB.db')
c = conn.cursor()


def checkCreateTables():
    employeesTable = """ CREATE TABLE IF NOT EXISTS employees (
        [first] TEXT,
        [last] TEXT,
        [pay] INTEGER)"""
    c.execute(employeesTable)


checkCreateTables()

c.execute("SELECT * FROM employees")
allEmployees = c.fetchall()


def exit1():
    conn.close()
    exit()


def insert_emp(emp):
    with conn:
        c.execute("INSERT INTO employees VALUES (:first, :last, :pay)",
                  {'first': emp.first, 'last': emp.last, 'pay': emp.pay})


def get_emps_by_name(lastname):
    c.execute("SELECT * FROM employees WHERE last=:last", {'last': lastname})

    return c.fetchall()


def reload_list():
    listbox.delete(0, END)
    c.execute("SELECT * FROM employees")
    allEmployees = c.fetchall()
    for employees in allEmployees:
        listbox.insert(END, employees)


def clear_boxes():
    fname_box.delete(0, END)
    lname_box.delete(0, END)
    pay_box.delete(0, END)


def clear_rm_boxes():
    remove_box_first.delete(0, END)
    remove_box_last.delete(0, END)
    remove_box_pay.delete(0, END)


def next():

    first = fname_box.get()

    last = lname_box.get()

    pay = pay_box.get()

    empn = Employee(str(first), str(last), int(pay))
    print("Adding", empn)

    def insert_emp(emp):
        with conn:
            c.execute("INSERT INTO employees VALUES (:first, :last, :pay)",
                      {'first': emp.first, 'last': emp.last, 'pay': emp.pay})

    insert_emp(empn)
    hash_label = Label(frameNW, text="Success!")
    hash_label.grid(row=4, column=1, padx=5, pady=5)
    reload_list()
    clear_boxes()
    hash_label.after(2000, hash_label.destroy)


def refresh_list():
    listbox.delete(0, END)
    search_box.delete(0, END)

    c.execute("SELECT * FROM employees")
    allEmployees = c.fetchall()

    for employees in allEmployees:
        listbox.insert(END, employees)


def first():
    listbox.delete(0, END)

    c.execute('SELECT * FROM employees ORDER BY first')
    last = c.fetchall()

    for i in last:
        listbox.insert(END, i)


def last():
    listbox.delete(0, END)

    c.execute('SELECT * FROM employees ORDER BY last')
    last = c.fetchall()

    for i in last:
        listbox.insert(END, i)


def salary():
    listbox.delete(0, END)

    c.execute('SELECT * FROM employees ORDER BY pay')
    salary = c.fetchall()

    for i in salary:
        listbox.insert(END, i)


def salaryD():
    listbox.delete(0, END)

    c.execute('SELECT * FROM employees ORDER BY pay DESC')
    salary = c.fetchall()

    for i in salary:
        listbox.insert(END, i)


def selected(event):
    if clicked.get() == 'First':
        first()

    elif clicked.get() == 'Last':
        last()

    elif clicked.get() == 'Salary Ascending':
        salary()

    elif clicked.get() == 'Salary Decending':
        salaryD()


def search_first():
    listbox.delete(0, END)
    searched = search_box.get()

    c.execute("SELECT * FROM employees WHERE first=:first", {'first': searched})
    sr = c.fetchall()

    for i in sr:
        listbox.insert(END, i)
    

def search_last():
    listbox.delete(0, END)
    searched = search_box.get()

    c.execute("SELECT * FROM employees WHERE last=:last", {'last': searched})
    sr = c.fetchall()

    for i in sr:
        listbox.insert(END, i)


def search_salary():
    listbox.delete(0, END)
    searched = search_box.get()

    c.execute("SELECT * FROM employees WHERE pay=:pay", {'pay': searched})
    sr = c.fetchall()

    for i in sr:
        listbox.insert(END, i)


def search_now():
    if selected.get() == 'First Name':
        search_first()

    elif selected.get() == 'Last Name':
        search_last()

    elif selected.get() == 'Salary':
        search_salary()


def rm():
    rm_first = remove_box_first.get()
    rm_last = remove_box_last.get()
    rm_pay = remove_box_pay.get()

    if rm_first == "" or rm_last == "" or rm_pay == "":
        rm_label_blank = Label(frameSW, text="1 or more required fields are blank")
        rm_label_blank.grid(row=5, column=1, padx=5, pady=5)
        rm_label_blank.after(2000, rm_label_blank.destroy)
        
    else:
        empa = Employee(str(rm_first), str(rm_last), str(rm_pay))
        print("Removing", empa)

        def remove_emp(emp):
            with conn:
                c.execute('''DELETE FROM employees WHERE last = :last AND first = :first AND pay = :pay''',
                          {'first': emp.first, 'last': emp.last, 'pay': emp.pay})

        remove_emp(empa)
        rm_label_suc = Label(frameSW, text="Success!")
        rm_label_suc.grid(row=5, column=1, padx=5, pady=5)
        reload_list()
        clear_rm_boxes()
        rm_label_suc.after(2000, rm_label_suc.destroy)


#_________________________________________________________________________________________________________________Lists/Options___#

options = [
    "-- Sort List --",
    "First",
    "Last",
    "Salary Ascending",
    "Salary Decending"
]

search_options = [
    "First Name",
    "Last Name",
    "Salary"
]


scrollbar = Scrollbar(frameR, relief=SOLID)

listbox = Listbox(frameR, width=32, relief=SOLID)


clicked = StringVar()
clicked.set(options[0])
sort_drop = OptionMenu(frameR, clicked, *options, command=selected)

selected = StringVar()
selected.set(search_options[0])
search_drop_menu = OptionMenu(frameR, selected, *search_options)


for employees in allEmployees:
    listbox.insert(END, employees)


#_______________________________________________________________________________________________________________________Entry()___#

search_box = Entry(frameR)

fname_box = Entry(frameNW)
lname_box = Entry(frameNW)
pay_box = Entry(frameNW)

remove_box_first = Entry(frameSW)
remove_box_last = Entry(frameSW)
remove_box_pay = Entry(frameSW)


#_____________________________________________________________________________________________________________________.config()___#

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
sort_drop.config(bg="light grey")
search_drop_menu.config(bg="light grey")
frameR.config(borderwidth=5)
frameNW.config(borderwidth=5)
frameSW.config(borderwidth=5)
sort_drop["highlightthickness"]=0
search_drop_menu["highlightthickness"]=0


#_______________________________________________________________________________________________________________________Label()___#

search_box_label = Label(frameR, text="Search Employees by", background="#9e9e9e")
fname_label = Label(frameNW, text="First Name", bg="cornflowerblue")
lname_label = Label(frameNW, text="Last Name", bg="cornflowerblue")
pay_pabel = Label(frameNW, text="Salary", bg="cornflowerblue")

rm_first_label = Label(frameSW, text="First Name", bg="violetRed4")
rm_last_label = Label(frameSW, text="Last Name", bg="violetRed4")
rm_pay_pabel = Label(frameSW, text="Salary", bg="violetRed4")


#______________________________________________________________________________________________________________________Button()___#

quit_button = Button(frameR, text='Save & Quit', bg='brown4', fg='white', font="verdana", relief="raised", command=exit1)
search_button = Button(frameR, text='SEARCH', fg="blue", command=search_now)
clear_search = Button(frameR, text='Refresh List', bg="green", command=refresh_list)
next_button = Button(frameNW, text="Add New Employee", command=next)
rm_button = Button(frameSW, text="Remove Employee", command=rm)


#_______________________________________________________________________________________________________________________.pack()___#

frameR.pack(side=RIGHT, fill=Y, padx=5, pady=5)                       #--\
frameNW.pack(side=TOP, anchor=NW, fill=BOTH, padx=5, pady=5)          #---- Frames
frameSW.pack(side=TOP, fill=X, padx=5, pady=5)                        #--/

sort_drop.pack(side=TOP, fill=X, padx=5, pady=5) #filter              # \
scrollbar.pack(side=RIGHT, fill=Y,pady=5)                             #--\
listbox.pack(side=RIGHT, fill=Y, pady=5) #list                        #---\
search_box_label.pack(side=TOP, fill=X)                               #----\
search_drop_menu.pack(side=TOP, fill=X, padx=5, pady=5)               #------ frameR search and sort employees
search_box.pack(side=TOP, fill=BOTH, padx=5, pady=5) #text field      #----/
search_button.pack(side=TOP, anchor=N, fill=X, padx=5, pady=5)        #---/
clear_search.pack(side=TOP, fill=X, padx=5, pady=5) #reset            #--/
quit_button.pack(side=BOTTOM, anchor=SE, fill=X, padx=5, pady=5)      # /


#_______________________________________________________________________________________________________________________.grid()___#

l2.grid(row=0, column=0, padx=5, pady=10) #spacer
l22.grid(row=0, column=1, padx=5, pady=10)
l222.grid(row=0, column=2, padx=5, pady=10) #spacer

fname_box.grid(row=2, column=0, padx=5)                               #-\
fname_label.grid(row=1, column=0, padx=5, pady=3)                     #--\
lname_box.grid(row=2, column=1, padx=5)                               #---\
lname_label.grid(row=1, column=1, padx=5, pady=3)                     #----- frameNW add employee
pay_box.grid(row=2, column=2, padx=5)                                 #---/
pay_pabel.grid(row=1, column=2, padx=5, pady=3)                       #--/
next_button.grid(row=3, column=1, padx=5, pady=5)                     #-/

l1.grid(row=0, column=0, padx=5, pady=10) #spacer
l11.grid(row=0, column=1, padx=5, pady=10)
l111.grid(row=0, column=2, padx=5, pady=10) #spacer

remove_box_first.grid(row=2, column=0, padx=5)                        #-\
rm_first_label.grid(row=1, column=0, padx=5, pady=3)                  #--\
remove_box_last.grid(row=2, column=1, padx=5)                         #---\
rm_last_label.grid(row=1, column=1, padx=5, pady=3)                   #----- frameSW remove employee
remove_box_pay.grid(row=2, column=2, padx=5)                          #---/
rm_pay_pabel.grid(row=1, column=2, padx=5, pady=3)                    #--/
rm_button.grid(row=3, column=1, padx=5, pady=5)                       #-/

window.mainloop()
