# Class-Scheduler
python tkinter app


Just a simple class Scheduler.

You can add Teachers with subjects
You can add Time Slots
You can add Rooms

Select Date
Select Teachers For that date (whom are going to be teaching that day)
Then it'll ask start adding teacher for that day. Teacher will be teaching at which time slot and in which room. If teacher is busy in a specific time and your give the same time again it'll give error that "Teacher is busy" and if you try to alot a room to a specific time where the room is already assigned to someone else then it'll give error that room busy
You can also click on auto-generate and it will automatically pick teacher selected for that day and assign them time and room one by one. So the first time and first teacher and first room then first time, second teacher, second room and so on
At the end it wil create the excel file that can be pasted on Notice Board and also in the other sheed it shows you how many teachers were free that day (means haven't took any class)


You can either add teacher, time slots and room one by one or can directly import file. Sample file is given. All you need to do is when you press import it will automatically open an excel file. Fill the data (or copy paste accordingly) save the file and close the file then click import and will import that file

Bugs:
Removing teacher in the final screen where you are creating time table. sometimes it wont remove teacher or destroys the entire time table
Dont Use "-" symboe While saving time slots i.e: "09:00 - 10:00" dont use that instead use "09:00 TO 10:00". That symbol is reserved as I split string with that symbol for working.
Use 24Hrs system either wise when clicked on auto generate it'll schedule 03:00pm timing slot first and 09:00am timing slot below it so try using 15:00 instead of 03:00pm

Future Updates:
Teacher time reserve and room reserve. Currently that option is just collecting data but has no impact but in future when the a particular whom had given you a specific time and room then once that teacher is selected for teaching automatically that time and room will be assigned to him
All time tables are stored in an sql table file but you cannot access the old time table. In future will add option to view old time tables
