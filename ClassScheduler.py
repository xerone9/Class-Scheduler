from tkinter import *
import calendar
from babel.dates import format_date, parse_date, get_day_names, get_month_names
from babel.numbers import *
import time
from tkinter import font as tkFont
from tkinter import ttk
from tkcalendar import *
import webbrowser
from datetime import date
from SQLWorking import *
from Tree_Table import *
from ExcelImport import *
from ExcelExport import *
from subprocess import call
import sqlite3
import os
import re


def callback(url):
    webbrowser.open_new(url)


def footer():
    footer = Label(root, text="softwares.rubick.org", font=(14), cursor="hand2")
    footer.bind("<Button-1>", lambda e: callback("http://softwares.rubick.org"))
    footer.configure(foreground="white")
    footer.configure(bg="black")
    footer.place(relx=0.5, y=(root.winfo_height() - 30))
    root.mainloop()


def excel_export():
    global currentDate
    Excel_Export(currentDate)
    root.destroy()



def final_screen():
    root.unbind('<Delete>')
    root.unbind('<Return>')
    for widget in root.winfo_children():
        widget.destroy()

    global currentDate
    final_schedule_logo = PhotoImage(file='images\\finalSchedule_logo.png')
    final_schedule_label = Label(root, image=final_schedule_logo)
    final_schedule_label.configure(foreground="black")
    final_schedule_label.configure(bg="white")
    final_schedule_label.place(relx=0.5, y=40, anchor=CENTER)

    date_selected_label = Label(root, text="For The Date Of: " + currentDate, font=("Roboto", 18, 'bold'), bg="white")
    date_selected_label.place(relx=0.5, y=100, anchor=CENTER)

    xframe = Frame(root)
    xframe.place(x=100, rely=0.15)

    xfinal_time_table = ttk.Treeview(xframe, height=15, style="yourstyle.Treeview")
    xfinal_time_table['columns'] = ("Name", "Subject", "Time Slot", "Room")
    xfinal_time_table.column("#0", minwidth=25, width=0, stretch=NO)
    xfinal_time_table.column("Name", anchor=W, width=350)
    xfinal_time_table.column("Subject", anchor=W, width=350)
    xfinal_time_table.column("Time Slot", anchor=CENTER, width=200)
    xfinal_time_table.column("Room", anchor=CENTER, width=200)

    xfinal_time_table.heading("#0", text="S. No", anchor=W)
    xfinal_time_table.heading("Name", text="Teacher Name", anchor=W)
    xfinal_time_table.heading("Subject", text="Subject", anchor=W)
    xfinal_time_table.heading("Time Slot", text="Timings", anchor=CENTER)
    xfinal_time_table.heading("Room", text="Room", anchor=CENTER)

    # my_tree.insert(parent="", index='end', iid=0, text="1", values=("Usman Mustafa Khawar", "Basic Programming", "03:00 To 06:00", "RM-05"))
    xfinal_time_table.pack(side='left', fill='y')

    scrollbar = Scrollbar(xframe, orient="vertical", command=xfinal_time_table.yview)
    scrollbar.pack(side="right", fill="y")
    xfinal_time_table.configure(yscrollcommand=scrollbar.set)

    fianl_table = fetch_values_from_time_table(currentDate)
    count = 0

    for value in fianl_table:
        list = value.split(" - ")
        xfinal_time_table.insert(parent="", index='end', iid=count, text=count + 1,
                                values=(list[0], list[1], list[2], list[3]))
        count += 1

    export_excel_logo = PhotoImage(file='images\\exportExcel_logo.png')
    exportExcelFile = Button(root, image=export_excel_logo, text="N E X T", font=("Roboto", 20, 'bold'), justify='center', command=excel_export)
    exportExcelFile.configure(foreground="black")
    exportExcelFile.configure(bg="white")
    exportExcelFile.place(relx=0.5, rely=0.8, anchor=CENTER)

    footer()


def generate_class_schedule2():
    root.unbind('<Left>')
    root.unbind('<Right>')
    root.unbind('<Return>')
    def auto_generate():
        global currentDate
        delete_values_from_time_table(currentDate)
        temporary_table.sort()
        rooms = fetch_values_from_rooms_table()
        time_slots = fetch_values_from_time_slots_table()
        count = 0
        for room in rooms:
            for time in time_slots:
                if count <= len(temporary_table) - 1:
                    list = temporary_table[count].split(" - ")
                    entry_in_time_table(date, list[0], list[1], time, room)
                    count += 1
        final_screen()



    def generate_final_table():
        list = teacherSelected.get().split(" - ")
        global currentDate
        date = currentDate
        teacher = list[0]
        subject = list[1]
        time = timeSlotSelected.get()
        room = roomSelected.get()
        selected_time_room = time + " - " + room
        selected_teacher_time = teacher + " - " + time
        records = fetch_values_from_time_table(date)
        if len(records) == 0:
            entry_in_time_table(date, teacher, subject, time, room)
            temporary_table.remove(teacher + " - " + subject)
            busy_rooms_time.append(time + " - " + room)
            busy_teacher_time.append(teacher + " - " + time)
            entry_status.config(text="                          Entry Added Successfully :)                          ", fg="green")
            generate_class_schedule2()
        else:
            for record in records:
                list = record.split(" - ")
                busy_rooms = list[2] + " - " + list[3]
                busy_teacher = list[0] + " - " + list[2]
                if busy_rooms not in busy_rooms_time:
                    busy_rooms_time.append(busy_rooms)
                if busy_teacher not in busy_teacher_time:
                    busy_teacher_time.append(busy_teacher)
            if selected_time_room in busy_rooms_time:
                verifier = verify_rooms_available_from_Time_table(selected_time_room)
                entry_status.config(text=verifier + " - Room Busy :(", fg="red")
                generate_class_schedule2()
            elif selected_teacher_time in busy_teacher_time:
                verifier = verify_teacher_available_from_Time_table(selected_teacher_time)
                entry_status.config(text=verifier + " - Teacher Busy :(", fg="red")
                generate_class_schedule2()
            else:
                entry_in_time_table(date, teacher, subject, time, room)
                temporary_table.remove(teacher + " - " + subject)
                entry_status.config(text="                          Entry Added Successfully :)                          ", fg="green")
                generate_class_schedule2()



    def delete_entry_from_final_table():
        teachers_selected = final_time_table.focus()
        values = final_time_table.item(teachers_selected, "values")
        global currentDate
        date = currentDate
        teacher = values[0]
        subject = values[1]
        time = values[2]
        room = values[3]
        delete_values2_from_time_table(date, teacher, subject, time, room)
        temporary_table.append(teacher + " - " + subject)
        entry_status.config(text="                          Entry Deleted                          ", fg="black")
        busy_rooms_time.remove(time + " - " + room)
        busy_teacher_time.remove(teacher + " - " + time)
        generate_class_schedule2()



    if len(temporary_table) != 0:

        global currentDate
        date = currentDate

        # for value in data:
        #     list = value.split(" - ")
        #     date = list[0]


        for widget in root.winfo_children():
            if widget.winfo_class() != 'Label':
                widget.destroy()


        helv36 = tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD)
        helv20 = tkFont.Font(family='Helvetica', size=10)

        time = temporary_time_slots

        timeSlotSelected = StringVar(root)
        timeSlotSelected.set(time[0])

        # teacher_time_slot_label = Label(root, text="Teacher Reserved Time: ", font=("Roboto", 18), bg="white")
        # teacher_time_slot_label.grid(row=3, column=0, pady=7, padx=10, sticky='w')
        select_time_slot = OptionMenu(root, timeSlotSelected, *time)
        select_time_slot_dropdown = root.nametowidget(select_time_slot.menuname)
        select_time_slot_dropdown.config(font=helv20)
        select_time_slot.configure(font=helv36)
        select_time_slot.place(x=25, y=180)

        teachers = temporary_table

        teacherSelected = StringVar(root)
        teacherSelected.set(teachers[0])

        select_teacher = OptionMenu(root, teacherSelected, *teachers)
        select_teacher_dropdown = root.nametowidget(select_teacher.menuname)
        select_teacher_dropdown.config(font=helv20)
        select_teacher.configure(font=helv36)
        select_teacher.place(x=280, y=180)

        rooms = temporary_rooms

        roomSelected = StringVar(root)
        roomSelected.set(rooms[0])

        select_room = OptionMenu(root, roomSelected, *rooms)
        select_room_dropdown = root.nametowidget(select_room.menuname)
        select_room_dropdown.config(font=helv20)
        select_room.configure(font=helv36)
        select_room.place(x=825, y=180)

        addEntry = Button(root, text="ADD Entry", font=("Roboto", 15, 'bold'), justify='center', command=generate_final_table)
        addEntry.configure(foreground="black")
        addEntry.configure(bg="light green")
        addEntry.place(x=1010, y=180)

        deletEntry = Button(root, text="Delete", font=("Roboto", 15, 'bold'), justify='center',
                          command=delete_entry_from_final_table)
        deletEntry.configure(foreground="black")
        deletEntry.configure(bg="red")
        deletEntry.place(relx=0.5, rely=0.9)

        if len(fetch_values_from_time_table(date)) == 0:
            auto_generate_time_table = Button(root, text="AUTO GENERATE", font=("Roboto", 15, 'bold'), justify='center',
                                command=auto_generate)
            auto_generate_time_table.configure(foreground="black")
            auto_generate_time_table.configure(bg="yellow")
            auto_generate_time_table.place(relx=0.1, rely=0.9)





        # time_table = Listbox(root, font=("Courier", 16, 'bold'), width=85, height=18, bg="light blue")
        # time_table.place(x=25, y=300)

        frame = Frame(root)
        frame.place(x=30, rely=0.30)

        final_time_table = ttk.Treeview(frame, height=15, style="yourstyle.Treeview")
        final_time_table['columns'] = ("Name", "Subject", "Time Slot", "Room")
        final_time_table.column("#0", minwidth=25, width=0, stretch=NO)
        final_time_table.column("Name", anchor=W, width=350)
        final_time_table.column("Subject", anchor=W, width=350)
        final_time_table.column("Time Slot", anchor=CENTER, width=200)
        final_time_table.column("Room", anchor=CENTER, width=200)

        final_time_table.heading("#0", text="S. No", anchor=W)
        final_time_table.heading("Name", text="Teacher Name", anchor=W)
        final_time_table.heading("Subject", text="Subject", anchor=W)
        final_time_table.heading("Time Slot", text="Timings", anchor=CENTER)
        final_time_table.heading("Room", text="Room", anchor=CENTER)

        # my_tree.insert(parent="", index='end', iid=0, text="1", values=("Usman Mustafa Khawar", "Basic Programming", "03:00 To 06:00", "RM-05"))
        final_time_table.pack(side='left', fill='y')

        scrollbar = Scrollbar(frame, orient="vertical", command=final_time_table.yview)
        scrollbar.pack(side="right", fill="y")
        final_time_table.configure(yscrollcommand=scrollbar.set)

        fianl_table = fetch_values_from_time_table(date)
        count = 0

        for value in fianl_table:
            list = value.split(" - ")
            final_time_table.insert(parent="", index='end', iid=count, text=count + 1,
                           values=(list[0], list[1], list[2], list[3]))
            count += 1

        entry_status = Label(root, text="", font=("Roboto", 18, 'bold'),
                             bg="white")
        entry_status.place(relx=0.4, rely=0.26, anchor=CENTER)

        root.bind('<Delete>', lambda event: delete_entry_from_final_table())
        root.bind('<Return>', lambda event: generate_final_table())

        footer()
    else:
        final_screen()


def generate_class_schedule():
    for widget in root.winfo_children():
        widget.destroy()

    date_picker = date.today()
    day = date_picker.strftime('%d')
    month = date_picker.strftime('%m')
    year = date_picker.strftime('%Y')

    create_schedule_logo = PhotoImage(file='images\\createschedule_logo.png')
    create_schedule_label = Label(root, image=create_schedule_logo)
    create_schedule_label.configure(foreground="black")
    create_schedule_label.configure(bg="white")
    create_schedule_label.place(relx=0.5, y=40, anchor=CENTER)

    mainMenu_logo = PhotoImage(file='images\\mainMenu_logo.png')
    homeButton = Button(root, image=mainMenu_logo, font=("Roboto", 15, 'bold'), justify='center', command=main_menu)
    homeButton.configure(foreground="black")
    homeButton.place(x=10, y=10)

    cal = Calendar(root, selectmode="day", year=int(year), month=int(month), day=int(day), date_pattern='dd/mm/y')
    cal.place(relx=0.5, y=200, anchor=CENTER)

    def grab_date():
        root.unbind('<Return>')
        root.unbind('<Delete>')
        root.unbind('<Escape>')
        date_selected_label.config(text='For The Date Of: ' + cal.get_date())
        global currentDate
        currentDate = cal.get_date()
        cal.destroy()
        date_selected_label.place(relx=0.5, y=100, anchor=CENTER)
        get_date.destroy()
        teachers_label.place(relx=0.5, y=175, anchor=CENTER)
        teachers_library_left.pack(side='left', fill='y')
        teachers_library_right.pack(side='left', fill='y')
        teachers_to_right_box.place(relx=0.5, rely=0.4, anchor=CENTER)
        teachers_to_left_box.place(relx=0.5, rely=0.6, anchor=CENTER)
        create_class_timetable.place(relx=0.5, rely=0.9, anchor=CENTER)
        iframe.place(relx=0.22, y=550, anchor=CENTER)
        frame.place(relx=0.77, y=550, anchor=CENTER)
        delete_values_from_time_table(currentDate)
        homeButton.destroy()
        root.bind('<Left>', lambda event: send_teacher_to_left())
        root.bind('<Right>', lambda event: send_teacher_to_right())
        root.bind('<Return>', lambda event: save_to_tempory_table())


    def send_teacher_to_right():
        global max_teacher
        total_teacher_allowed = max_room() * max_time()
        if max_teacher >= total_teacher_allowed:
            max_teacher_label.place(relx=0.5, y=215, anchor=CENTER)
        else:
            date_selected_label.place()
            count = teachers_library_right.get_children()
            counter = 0
            if not count:
                counter = 1
            else:
                for game in count:
                    counter = int(game) + 1
            total_teacher_selected_label.place(relx=0.65, rely=0.86)
            teachers_selected = teachers_library_left.focus()
            values = teachers_library_left.item(teachers_selected, "values")
            sameTeacher = same_teachers.count(values[0])
            if sameTeacher >= max_time():
                max_teacher_label.config(text=str(values[0] + " Time Slot Full"))
                max_teacher_label.place(relx=0.5, y=215, anchor=CENTER)
            else:
                same_teachers.append(values[0])
                teachers_library_right.insert(parent="", index='end', iid=counter, text=counter, values=(values[0], values[1]))
                remove_value = teachers_library_left.selection()
                teachers_library_left.delete(remove_value)
                max_teacher += 1
                total_teacher_selected_label.config(text="Teacher Selected = " + str(max_teacher), fg='blue')
                max_teacher_label.place(x=1, y=99999)


    def send_teacher_to_left():
        global max_teacher
        count = teachers_library_left.get_children()
        for game in count:
            counter = int(game) + 1
        teachers_selected = teachers_library_right.focus()
        values = teachers_library_right.item(teachers_selected, "values")
        same_teachers.remove(values[0])
        teachers_library_left.insert(parent="", index='end', iid=counter, text=counter, values=(values[0], values[1]))
        remove_value = teachers_library_right.selection()
        teachers_library_right.delete(remove_value)
        total_teacher_selected_label.place(relx=0.65, rely=0.86)
        max_teacher -= 1
        total_teacher_selected_label.config(text="Teacher Selected = " + str(max_teacher), fg='blue')
        max_teacher_label.place(x=1, y=99999)

    def save_to_tempory_table():
        if len(teachers_library_right.get_children()) == 0:
            max_teacher_label.config(text="Add Teachers For Classes")
            max_teacher_label.place(relx=0.5, y=215, anchor=CENTER)
        else:
            teachers_label.destroy()
            max_teacher_label.destroy()
            total_teacher_selected_label.destroy()
            for row_id in teachers_library_right.get_children():
                teacher_with_subject = teachers_library_right.item(row_id)["values"]
                temporary_table.append(teacher_with_subject[0] + " - " + teacher_with_subject[1])
            rooms = fetch_values_from_rooms_table()
            time_slots = fetch_values_from_time_slots_table()
            for value in rooms:
                if value not in temporary_rooms:
                    temporary_rooms.append(value)
            for value in time_slots:
                if value not in temporary_time_slots:
                    temporary_time_slots.append(value)
            generate_class_schedule2()

    date_selected_label = Label(root, text="", font=("Roboto", 18, 'bold'), bg="white")
    date_selected_label.place()
    get_date = Button(root, text="SELECT DATE", font=("Roboto", 15, 'bold'), justify='center', command=grab_date)
    get_date.configure(foreground="black")
    get_date.configure(bg="light grey")
    get_date.place(relx=0.5, rely=0.42, anchor=CENTER)

    teachers_label = Label(root, text="Select Teachers For Classes", font=("Roboto", 22, 'bold'), bg="white", fg='brown')
    teachers_label.place()

    max_teacher_label = Label(root, text="ROOMS FULL", font=("Roboto", 22, 'bold'), bg="white",
                           fg='red')
    max_teacher_label.place()

    teachersToRIght_logo = PhotoImage(file='images\\to_right.png')
    teachers_to_right_box = Button(root, image=teachersToRIght_logo, font=("Roboto", 15, 'bold'), justify='center',
                                   command=send_teacher_to_right)
    teachers_to_right_box.configure(foreground="black")
    teachers_to_right_box.configure(bg="light grey")
    teachers_to_right_box.place()

    teachersToLeft_logo = PhotoImage(file='images\\to_left.png')
    teachers_to_left_box = Button(root, image=teachersToLeft_logo, font=("Roboto", 15, 'bold'), justify='center',
                                  command=send_teacher_to_left)
    teachers_to_left_box.configure(foreground="black")
    teachers_to_left_box.configure(bg="light grey")



    create_class_timetable = Button(root, text='N E X T', font=("Roboto", 15, 'bold'), justify='center',
                                    command=save_to_tempory_table)
    create_class_timetable.configure(foreground="black")
    create_class_timetable.configure(bg="light grey")
    create_class_timetable.place()

    iframe = Frame(root)

    teachers_library_left = ttk.Treeview(iframe, height=20, style="mystyle.Treeview")
    teachers_library_left['columns'] = ("Name", "Subject")
    teachers_library_left.column("#0", width=0, stretch=NO)
    teachers_library_left.column("Name", anchor=W, width=250)
    teachers_library_left.column("Subject", anchor=W, width=250)

    teachers_library_left.heading("#0", text="S. No", anchor=W)
    teachers_library_left.heading("Name", text="Teacher Name", anchor=W)
    teachers_library_left.heading("Subject", text="Subject", anchor=W)

    # my_tree.insert(parent="", index='end', iid=0, text="1", values=("Usman Mustafa Khawar", "Basic Programming", "03:00 To 06:00", "RM-05"))
    scrollbar = Scrollbar(iframe, orient="vertical", command=teachers_library_left.yview)
    scrollbar.pack(side="right", fill="y")
    teachers_library_left.configure(yscrollcommand=scrollbar.set)

    total_teacher_selected_label = Label(root, text="", font=("Roboto", 18, 'bold'), bg="white")
    total_teacher_selected_label.place()

    teacher_list = fetch_values_from_teachers_table()
    count = 0

    for value in teacher_list:
        list = value.split(" - ")
        teachers_library_left.insert(parent="", index='end', iid=count, text="",
                                      values=(list[0], list[1]))
        count += 1

    # teachers_library = Listbox(root, font=("Courier", 16, 'bold'), width=37, height=26, bg="light blue")
    # teachers_library.place()









    # for item in all_teachers_list:
    #     teachers_library.insert(END, item)
    #
    # selected_teachers = Listbox(root, font=("Courier", 16, 'bold'), width=37, height=26, bg="light blue")
    # selected_teachers.place()
    frame = Frame(root)

    teachers_library_right = ttk.Treeview(frame, height=20, style="mystyle.Treeview")
    teachers_library_right['columns'] = ("Name", "Subject")
    teachers_library_right.column("#0", width=0, stretch=NO)
    teachers_library_right.column("Name", anchor=W, width=250)
    teachers_library_right.column("Subject", anchor=W, width=250)

    teachers_library_right.heading("#0", text="S. No", anchor=W)
    teachers_library_right.heading("Name", text="Teacher Name", anchor=W)
    teachers_library_right.heading("Subject", text="Subject", anchor=W)

    # my_tree.insert(parent="", index='end', iid=0, text="1", values=("Usman Mustafa Khawar", "Basic Programming", "03:00 To 06:00", "RM-05"))


    scrollbar = Scrollbar(frame, orient="vertical", command=teachers_library_right.yview)
    scrollbar.pack(side="right", fill="y")
    teachers_library_right.configure(yscrollcommand=scrollbar.set)

    total_teacher_selected_label = Label(root, text="", font=("Roboto", 18, 'bold'), bg="white")
    total_teacher_selected_label.place()


    footer()





def add_teacher():
    root.unbind('<Return>')
    root.unbind('<Delete>')
    def update_teacher_status():
        teacher_name.delete(0, END)
        teacher_subject.delete(0, END)
        teacher_time_slot_option_selected.set("")
        teacher_reserved_room_option_selected.set("")
        for record in my_tree.get_children():
            my_tree.delete(record)
        teachers = fetch_values_from_teachers_table()
        count = 0

        for value in teachers:
            list = value.split(" - ")
            my_tree.insert(parent="", index='end', iid=count, text=count + 1,
                           values=(list[0], list[1], list[2], list[3]))
            count += 1
        teacher_name.focus()


    def save_teacher_in_database():
        if len(teacher_name.get()) == 0 or len(teacher_subject.get()) == 0:
            if len(teacher_name.get()) == 0 and len(teacher_subject.get()) == 0:
                status_label.config(text="Name and Subject are Mandatory Fields")
            elif len(teacher_name.get()) == 0:
                status_label.config(text="Enter Teacher Name")
            else:
                status_label.config(text="Enter Subject Name")
        else:
            status_label.config(text="Teacher Added Sucessfully :)", fg="green")
            entry_in_teachers_table(teacher_name.get(), teacher_subject.get(), teacher_time_slot_option_selected.get(), teacher_reserved_room_option_selected.get())
            update_teacher_status()



    def delete_teacher_in_database():
        status_label.config(text="Teacher Deleted Sucessfully", fg="Black")
        delete_values_from_teachers_table(selectItem())
        update_teacher_status()


    def edit_teacher_in_database():
        root.unbind('<Return>')
        root.unbind('<Delete>')
        root.unbind('<Escape>')
        root.bind('<Return>', lambda event: save_edited_teacher_in_database())
        edit_Values = modify_values_from_teachers_table(selectItem())
        teacher_name.insert(0, edit_Values[0])
        teacher_subject.insert(0, edit_Values[1])
        teacher_time_slot_option_selected.set(edit_Values[2])
        teacher_reserved_room_option_selected.set(edit_Values[3])
        teacher_oid.config(text=edit_Values[4])
        addTeacher.grid_remove()
        editTeacher.grid_remove()
        deleteTeacher.place_forget()
        my_tree.place_forget()
        saveEditedTeacher.place(relx=0.2, rely=0.42)


    def save_edited_teacher_in_database():
        save_modified_values_from_teachers_table(teacher_name.get(), teacher_subject.get(), teacher_time_slot_option_selected.get(), teacher_reserved_room_option_selected.get(), teacher_oid.cget("text"))
        saveEditedTeacher.place_forget()
        addTeacher.grid(row=5, column=0, pady=20)
        editTeacher.grid(row=5, column=1)
        my_tree.place(x=15, rely=0.5)
        deleteTeacher.place(relx=0.13, rely=0.88)
        update_teacher_status()
        root.bind('<Return>', lambda event: save_teacher_in_database())
        root.bind('<Delete>', lambda event: delete_teacher_in_database())
        root.bind('<Escape>', lambda event: main_menu())


    def selectItem():
        curItem = my_tree.focus()
        Name = my_tree.set(curItem, 'Name')
        Subject = my_tree.set(curItem, 'Subject')
        Time_Slot = my_tree.set(curItem, 'Time Slot')
        Room = my_tree.set(curItem, 'Room')
        list = [Name, Subject, Time_Slot, Room]
        return list

    for widget in root.winfo_children():
        widget.destroy()


    manage_teachers_logo = PhotoImage(file='images\\manageTeachers_logo.png')
    manage_teachers_label = Label(root, image=manage_teachers_logo)
    manage_teachers_label.configure(foreground="black")
    manage_teachers_label.configure(bg="white")
    manage_teachers_label.place(relx=0.5, rely=0.1, anchor=CENTER)

    mainMenu_logo = PhotoImage(file='images\\mainMenu_logo.png')
    homeButton = Button(root, image=mainMenu_logo, font=("Roboto", 15, 'bold'), justify='center', command=main_menu)
    homeButton.configure(foreground="black")
    homeButton.place(x=10, y=10)

    space_variable = Label(root, text="", font=("Roboto", 18), bg="white")
    space_variable.grid(row=0, column=0, pady=75)

    teacher_name_label = Label(root, text="Teacher Name: ", font=("Roboto", 18), bg="white")
    teacher_name_label.grid(row=1, column=0, pady=7, padx=10, sticky='w')
    teacher_name = Entry(root, width=30, font=("Roboto", 18), bg='light blue')
    teacher_name.grid(row=1, column=1)

    teacher_subject_label = Label(root, text="Teacher Subject: ", font=("Roboto", 18), bg="white")
    teacher_subject_label.grid(row=2, column=0, pady=7, padx=10, sticky='w')
    teacher_subject = Entry(root, width=30, font=("Roboto", 18), bg='light blue')
    teacher_subject.grid(row=2, column=1)

    teacher_time_allowed = fetch_values_from_time_slots_table()
    teacher_time_slot_option_selected = StringVar(root)
    teacher_time_slot_option_selected.set("")

    teacher_time_slot_label = Label(root, text="Teacher Reserved Time: ", font=("Roboto", 18), bg="white")
    teacher_time_slot_label.grid(row=3, column=0, pady=7, padx=10, sticky='w')
    teacher_time_slot = OptionMenu(root, teacher_time_slot_option_selected, *teacher_time_allowed)
    teacher_time_slot.grid(padx=50, row=3, column=1, sticky='w')

    teachers_room_available = fetch_values_from_rooms_table()
    teacher_reserved_room_option_selected = StringVar(root)
    teacher_reserved_room_option_selected.set("")


    teacher_room_label = Label(root, text="Teacher Reserved Room:", font=("Roboto", 18), bg="white")
    teacher_room_label.grid(row=4, column=0, pady=12, padx=10, sticky='w')
    teacher_room = OptionMenu(root, teacher_reserved_room_option_selected, *teachers_room_available)
    teacher_room.grid(padx=50, row=4, column=1, sticky='w')

    teacher_oid = Label(root, text="", font=("Roboto", 18), bg="white")
    teacher_oid.place()

    addTeacher = Button(root, text="ADD TEACHER", font=("Roboto", 15, 'bold'), justify='center', command=save_teacher_in_database)
    addTeacher.configure(foreground="black")
    addTeacher.configure(bg="light green")
    addTeacher.grid(row=5, column=0, pady=20)

    editTeacher = Button(root, text="EDIT TEACHER", font=("Roboto", 15, 'bold'), justify='center', command=edit_teacher_in_database)
    editTeacher.configure(foreground="black")
    editTeacher.configure(bg="light green")
    editTeacher.grid(row=5, column=1)

    frame = Frame(root)
    frame.place(x=15, rely=0.5)

    my_tree = ttk.Treeview(frame, height=10, style="mystyle.Treeview")
    my_tree['columns'] = ("Name", "Subject", "Time Slot", "Room")
    my_tree.column("#0", minwidth=25, width=60)
    my_tree.column("Name", anchor=W, width=220)
    my_tree.column("Subject", anchor=W, width=220)
    my_tree.column("Time Slot", anchor=CENTER, width=180)
    my_tree.column("Room", anchor=CENTER, width=180)

    my_tree.heading("#0", text="S. No", anchor=W)
    my_tree.heading("Name", text="Teacher Name", anchor=W)
    my_tree.heading("Subject", text="Subject", anchor=W)
    my_tree.heading("Time Slot", text="Timings", anchor=CENTER)
    my_tree.heading("Room", text="Room", anchor=CENTER)


    my_tree.pack(side='left', fill='y')

    scrollbar = Scrollbar(frame, orient="vertical", command=my_tree.yview)
    scrollbar.pack(side="right", fill="y")
    my_tree.configure(yscrollcommand=scrollbar.set)

    # my_tree.insert(parent="", index='end', iid=0, text="1", values=("Usman Mustafa Khawar", "Basic Programming", "03:00 To 06:00", "RM-05"))


    teacher_list = fetch_values_from_teachers_table()
    count = 0

    for value in teacher_list:
        list = value.split(" - ")
        my_tree.insert(parent="", index='end', iid=count, text=count + 1,
                       values=(list[0], list[1], list[2], list[3]))
        count += 1



    deleteTeacher = Button(root, text="DELETE TEACHER", font=("Roboto", 15, 'bold'), justify='center',
                           command=delete_teacher_in_database)
    deleteTeacher.configure(foreground="black")
    deleteTeacher.configure(bg="RED")
    deleteTeacher.place(relx=0.13, rely=0.88)

    saveEditedTeacher = Button(root, text="MODIFY TEACHER", font=("Roboto", 15, 'bold'), justify='center', command=save_edited_teacher_in_database)
    saveEditedTeacher.configure(foreground="black")
    saveEditedTeacher.configure(bg="light green")
    saveEditedTeacher.place()

    status_label = Label(root, text="", font=("Roboto", 18), bg="white", fg="red")
    status_label.place(relx=0.3, rely=0.48, anchor=CENTER)

    # teachers = fetch_values_from_teachers_table()
    #
    # for teacher in teachers:
    #     teachers_list.insert(END, teacher)

    teacher_name.focus()

    root.bind('<Return>', lambda event: save_teacher_in_database())
    root.bind('<Delete>', lambda event: delete_teacher_in_database())
    root.bind('<Escape>', lambda event: main_menu())

    # table(root, 0.5, 0.5)



    footer()


def add_room():
    root.unbind('<Return>')
    root.unbind('<Delete>')
    def update_room_status():
        room_name.delete(0, END)
        rooms_list.delete(0, END)
        rooms = fetch_values_from_rooms_table()
        for room in rooms:
            rooms_list.insert(END, room)
        room_name.focus()


    def save_room_in_database():
        new_room = room_name.get()
        duplicate_room = ""
        room_already_present = fetch_values_from_rooms_table()
        for room in room_already_present:
            if new_room == room:
                duplicate_room = room_name.get()

        if len(room_name.get()) == 0:
            status_label.config(text="Room Field Must Not Be Empty")
        elif new_room == duplicate_room:
            status_label.config(text="Room Already Present")
            room_name.delete(0, END)
        else:
            status_label.config(text="")
            entry_in_rooms_table(room_name.get())
            update_room_status()


    def delete_room_in_database():
        status_label.config(text="")
        for item in rooms_list.curselection():
            room_selected = str(rooms_list.get(item))
            delete_values_from_rooms_table(room_selected)
            update_room_status()


    for widget in root.winfo_children():
        widget.destroy()

    mainMenu_logo = PhotoImage(file='images\\mainMenu_logo.png')
    homeButton = Button(root, image=mainMenu_logo, font=("Roboto", 15, 'bold'), justify='center', command=main_menu)
    homeButton.configure(foreground="black")
    homeButton.place(x=10, y=10)

    frame = Frame(root)
    frame.place(relx=0.5, y=650, anchor=CENTER)



    add_room_logo = PhotoImage(file='images\\manageRooms_logo.png')
    add_room_label = Label(root, image=add_room_logo)
    add_room_label.configure(foreground="black")
    add_room_label.configure(bg="white")
    add_room_label.place(relx=0.5, rely=0.1, anchor=CENTER)

    room_name_label = Label(root, text="Room Name: ", font=("Roboto", 18), bg="white")
    room_name_label.place(relx=0.30, y=220)
    room_name = Entry(root, width=30, font=("Roboto", 18), bg='light blue')
    room_name.place(relx=0.45, y=220)

    addRoom = Button(root, text="ADD ROOM", font=("Roboto", 15, 'bold'), justify='center', command=save_room_in_database)
    addRoom.configure(foreground="black")
    addRoom.configure(bg="light green")
    addRoom.place(relx=0.38, y=320)

    deleteRoom = Button(root, text="DELETE ROOM", font=("Roboto", 15, 'bold'), justify='center', command=delete_room_in_database)
    deleteRoom.configure(foreground="black")
    deleteRoom.configure(bg="red")
    deleteRoom.place(relx=0.50, y=320)

    rooms_list = Listbox(frame, font=("Courier", 16, 'bold'), width=50, height=17, bg="light blue")
    rooms_list.pack(side='left', fill='y')

    scrollbar = Scrollbar(frame, orient="vertical", command=rooms_list.yview)
    scrollbar.pack(side="right", fill="y")
    rooms_list.config(yscrollcommand=scrollbar.set)





    rooms = fetch_values_from_rooms_table()

    for room in rooms:
        rooms_list.insert(END, room)

    room_name.focus()

    status_label = Label(root, text="", font=("Roboto", 30), bg="white", fg="red")
    status_label.place(relx=0.5, rely=0.9, anchor=CENTER)

    root.bind('<Return>', lambda event: save_room_in_database())
    root.bind('<Delete>', lambda event: delete_room_in_database())
    root.bind('<Escape>', lambda event: main_menu())

    footer()


def add_time_slot():
    root.unbind('<Return>')
    root.unbind('<Delete>')
    def update_time_slot_status():
        timeSlot_name.delete(0, END)
        timeSlot_list.delete(0, END)
        timeSlots = fetch_values_from_time_slots_table()
        for time in timeSlots:
            timeSlot_list.insert(END, time)
        timeSlot_name.focus()


    def save_time_slot_in_database():
        new_time = timeSlot_name.get()
        duplicate_time = ""
        time_already_present = fetch_values_from_time_slots_table()
        for time in time_already_present:
            if new_time == time:
                duplicate_time = new_time

        if len(new_time) == 0:
            status_label.config(text="Time Slot Field Must Not Be Empty")
        elif new_time == duplicate_time:
            status_label.config(text="Time Slot Already Present")
            timeSlot_name.delete(0, END)
        else:
            status_label.config(text="")
            entry_in_time_slots_table(timeSlot_name.get())
            update_time_slot_status()



    def delete_time_slot_in_database():
        status_label.config(text="")
        for item in timeSlot_list.curselection():
            timeSlot_selected = str(timeSlot_list.get(item))
            delete_values_from_time_slots_table(timeSlot_selected)
            update_time_slot_status()

    for widget in root.winfo_children():
        widget.destroy()

    mainMenu_logo = PhotoImage(file='images\\mainMenu_logo.png')
    homeButton = Button(root, image=mainMenu_logo, font=("Roboto", 15, 'bold'), justify='center', command=main_menu)
    homeButton.configure(foreground="black")
    homeButton.place(x=10, y=10)

    frame = Frame(root)
    frame.place(relx=0.5, y=650, anchor=CENTER)

    add_time_slot_logo = PhotoImage(file='images\\manageTimeSlots_logo.png')
    add_time_slot_label = Label(root, image=add_time_slot_logo)
    add_time_slot_label.configure(foreground="black")
    add_time_slot_label.configure(bg="white")
    add_time_slot_label.place(relx=0.5, rely=0.1, anchor=CENTER)

    timeSlot_name_label = Label(root, text="Add Time Slot: ", font=("Roboto", 18), bg="white")
    timeSlot_name_label.place(relx=0.30, y=220)
    timeSlot_name = Entry(root, width=30, font=("Roboto", 18), bg='light blue')
    timeSlot_name.place(relx=0.45, y=220)

    addTimeSlot = Button(root, text="ADD SLOT", font=("Roboto", 15, 'bold'), justify='center', command=save_time_slot_in_database)
    addTimeSlot.configure(foreground="black")
    addTimeSlot.configure(bg="light green")
    addTimeSlot.place(relx=0.38, y=320)

    deleteTimeSlot = Button(root, text="DELETE SLOT", font=("Roboto", 15, 'bold'), justify='center', command=delete_time_slot_in_database)
    deleteTimeSlot.configure(foreground="black")
    deleteTimeSlot.configure(bg="red")
    deleteTimeSlot.place(relx=0.50, y=320)

    timeSlot_list = Listbox(frame, font=("Courier", 16, 'bold'), width=50, height=17, bg="light blue")
    timeSlot_list.pack(side='left', fill='y')

    scrollbar = Scrollbar(frame, orient="vertical", command=timeSlot_list.yview)
    scrollbar.pack(side="right", fill="y")
    timeSlot_list.config(yscrollcommand=scrollbar.set)



    timeSlots = fetch_values_from_time_slots_table()

    for time in timeSlots:
        timeSlot_list.insert(END, time)

    timeSlot_name.focus()

    status_label = Label(root, text="", font=("Roboto", 30), bg="white", fg="red")
    status_label.place(relx=0.5, rely=0.9, anchor=CENTER)

    root.bind('<Return>', lambda event: save_time_slot_in_database())
    root.bind('<Delete>', lambda event: delete_time_slot_in_database())
    root.bind('<Escape>', lambda event: main_menu())

    footer()


def main_menu():
    root.unbind('<Return>')
    def importExcel():
        importData.place_forget()
        importExcelFile.place(relx=0.50, rely=0.75, anchor='s')
        OpenExcelFile()


    def importSavedExcel():
        Data_Imported_label.place(relx=0.50, rely=0.75, anchor='s')
        importExcelFile.place_forget()
        SaveToSQL()

    for widget in root.winfo_children():
        widget.destroy()

    class_scheduler_logo = PhotoImage(file='images\\classScheduler_logo.png')
    label = Label(root, image=class_scheduler_logo)
    label.configure(foreground="black")
    label.configure(bg="white")
    label.place(relx=0.5, rely=0.1, anchor=CENTER)

    add_teacher_logo = PhotoImage(file='images\\addTeacher_logo.png')
    addTeacher = Button(root, image=add_teacher_logo, text="N E X T", font=("Roboto", 20, 'bold'), justify='center',
                        command=add_teacher)
    addTeacher.configure(foreground="black")
    addTeacher.configure(bg="white")
    addTeacher.place(relx=0.75, rely=0.55, anchor='s')

    add_class_room_logo = PhotoImage(file='images\\classRoom_logo.png')
    addClassRoom = Button(root, image=add_class_room_logo, font=("Roboto", 20, 'bold'), justify='center',
                          command=add_room)
    addClassRoom.configure(foreground="black")
    addClassRoom.configure(bg="white")
    addClassRoom.place(relx=0.25, rely=0.55, anchor='s')

    add_time_slots_logo = PhotoImage(file='images\\timeSlots.png')
    addTimeSlots = Button(root, image=add_time_slots_logo, font=("Roboto", 20, 'bold'), justify='center',
                          command=add_time_slot)
    addTimeSlots.configure(foreground="black")
    addTimeSlots.configure(bg="white")
    addTimeSlots.place(relx=0.50, rely=0.55, anchor='s')

    importData = Button(root, text="Import Data", font=("Roboto", 20, 'bold'), justify='center', command=importExcel)
    importData.configure(foreground="black")
    importData.configure(bg="light grey")
    importData.place(relx=0.50, rely=0.75, anchor='s')

    generateClassSchedule = Button(root, text="Generate Class Schedule", font=("Roboto", 20, 'bold'), justify='center',
                                   command=generate_class_schedule)
    generateClassSchedule.configure(foreground="black")
    generateClassSchedule.configure(bg="light grey")
    generateClassSchedule.place(relx=0.50, rely=0.83, anchor='s')

    importExcelFile = Button(root, text="Upload Saved File", font=("Roboto", 20, 'bold'), justify='center',
                                   command=importSavedExcel)
    importExcelFile.configure(foreground="black")
    importExcelFile.configure(bg="light grey")
    importExcelFile.place()

    Data_Imported_label = Label(root, text="Data Imported Successfully :)", font=("Roboto", 30), bg="white", fg="Dark Green")
    Data_Imported_label.place()



    footer()


def startup_screen():

    def create_primary_table():
        if len(institution_name.get()) == 0:
            status_label.config(text="Insutitution Name Must Not Be Empty")
        else:
            create_main_table()
            entry_in_institution_table(institution_name.get(), department_name.get())
            main_menu()

    for widget in root.winfo_children():
        widget.destroy()

    welcome_logo = PhotoImage(file='images\\welcome_logo.png')
    label = Label(root, image=welcome_logo)
    label.configure(foreground="black")
    label.configure(bg="white")
    label.place(relx=0.5, rely=0.1, anchor=CENTER)

    institution_name_label = Label(root, text="Institution Name: ", font=("Roboto", 30), bg="white")
    institution_name_label.place(relx=0.43, rely=0.38, anchor="se")
    institution_name = Entry(root, width=25, font=("Roboto", 30), bg='light blue')
    institution_name.place(relx=0.65, rely=0.35, anchor=CENTER)

    department_name_label = Label(root, text="Department Name: ", font=("Roboto", 30), bg="white")
    department_name_label.place(relx=0.43, rely=0.48, anchor="se")
    department_name = Entry(root, width=25, font=("Roboto", 30), bg='light blue')
    department_name.place(relx=0.65, rely=0.45, anchor=CENTER)

    get_to_main_menu = Button(root, text="G O", font=("Roboto", 20, 'bold'), justify='center',
                                   command=create_primary_table)
    get_to_main_menu.configure(foreground="black")
    get_to_main_menu.configure(bg="light grey")
    get_to_main_menu.place(relx=0.5, rely=0.6, anchor=CENTER)

    status_label = Label(root, text="", font=("Roboto", 30), bg="white", fg="red")
    status_label.place(relx=0.5, rely=0.8, anchor=CENTER)

    root.bind('<Return>', lambda event: create_primary_table())



    footer()




root = Tk()

global style
style = ttk.Style()
global max_teacher
max_teacher = 0
style.configure("Treeview.Heading", font=(None, 10))
style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 15), rowheight=28)
style.configure("yourstyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 20), rowheight=35)
my_tree = ttk.Treeview(root, style="mystyle.Treeview")
root.resizable(0,0)
root.iconbitmap('icon.ico')
root.configure(bg="white")
root.state("zoomed")
global currentDate
currentDate = ""
temporary_table = []
temporary_rooms = []
temporary_time_slots = []
busy_rooms_time = []
busy_teacher_time = []
same_teachers = []

if os.path.exists("Class_Scheduler.db"):
    conn = sqlite3.connect("Class_Scheduler.db")
    c = conn.cursor()
    c.execute("SELECT institution_name, department_name, oid FROM Institution")
    institution = c.fetchone()
    institution_name = institution[0]
    department_name = institution[1]
    root.title(institution_name + " - " + department_name)
    main_menu()
    conn.commit()
    conn.close()
else:
    root.title('Class Scheduler')
    startup_screen()

