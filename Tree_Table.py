from tkinter import *
from tkinter import ttk
from SQLWorking import *



def table(master, x, y):
    def selectItem(a):
        curItem = my_tree.focus()
        Name = my_tree.set(curItem, 'Name')
        Subject = my_tree.set(curItem, 'Subjcet')
        Time_Slot = my_tree.set(curItem, 'Time Slot')
        Room = my_tree.set(curItem, 'Room')
        list = [Name, Subject, Time_Slot, Room]
        return list

    style = ttk.Style()
    style.configure("Treeview.Heading", font=(None,15))
    my_tree = ttk.Treeview(master, height=15)
    my_tree['columns'] = ("Name", "Subject", "Time Slot", "Room")
    my_tree.column("#0", minwidth=25, width=60)
    my_tree.column("Name", anchor=W, width=180)
    my_tree.column("Subject", anchor=W, width=180)
    my_tree.column("Time Slot", anchor=CENTER, width=120)
    my_tree.column("Room", anchor=CENTER, width=120)

    my_tree.heading("#0", text="S. No", anchor=W)
    my_tree.heading("Name", text="Teacher Name", anchor=W)
    my_tree.heading("Subject", text="Subject", anchor=W)
    my_tree.heading("Time Slot", text="Timings", anchor=CENTER)
    my_tree.heading("Room", text="Room", anchor=CENTER)
    my_tree.bind('<ButtonRelease-1>', selectItem)

    # my_tree.insert(parent="", index='end', iid=0, text="1", values=("Usman Mustafa Khawar", "Basic Programming", "03:00 To 06:00", "RM-05"))
    my_tree.place(x=x, rely=y)

    game = fetch_values_from_teachers_table()
    count = 0

    for value in game:
        list = value.split(" - ")
        my_tree.insert(parent="", index='end', iid=count, text=count+1,
                       values=(list[0], list[1], list[2], list[3]))
        count += 1