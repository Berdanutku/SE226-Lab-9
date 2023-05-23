import mysql.connector
import tkinter as tk
from tkinter import *

root=tk.Tk()
root.title("Marvel")
ıdList=[]

database = mysql.connector.connect(
    host="localhost",
    user= "root",
    passwd= "root1234" )
cursorObject= database.cursor()

cursorObject.execute("DROP DATABASE Marvel")
cursorObject.execute("CREATE DATABASE Marvel")

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    database = 'Marvel',
    passwd="root1234" )
if connection.is_connected():
    db_Info = connection.get_server_info()
    print("Connected to the MySQL server", db_Info)
    cursor = connection.cursor()
    cursor.execute("select database() ")
    record = cursor.fetchone()
    print("Connected to the database", record)

try:
    connection = mysql.connector.connect(
        host="localhost",
        database="Marvel",
        user="root",
        password="root1234" )
    mysqlQuery = """
     CREATE TABLE marvel(
     ID int(30) NOT NULL,
     MOVIE varchar(250) NOT NULL,
     DATE varchar(250) NOT NULL,
     MCU_PHASE varchar(250) NOT NULL,
     PRIMARY KEY(ID))"""

    cursor = connection.cursor()
    result = cursor.execute(mysqlQuery)

    cursor.execute("SHOW TABLES")
    for tableName in cursor:
        print("Table name:",tableName)
except mysql.connector.Error as error:
    print("Fail!",error)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MYSQL is closed")

file = open(r"C:\Users\berda\PycharmProjects\pythonProject1\Marvel.txt")

try:
    connection = mysql.connector.connect(
        host="localhost",
        database="Marvel",
        user="root",
        password="root1234"
    )
    CursorObject = connection.cursor()
    while file:
        i = file.readline()
        if i == "":
            break
        a = i.split()
        Insert = """INSERT INTO marvel (ID, MOVIE, DATE, MCU_PHASE)
                 VALUES (%s, %s, %s, %s)"""
        record = (a[0], a[1], a[2], a[3])
        ıdList.append(a[0])
        CursorObject.execute(Insert, record)
        connection.commit()
    print("Records are added into table.")
    CursorObject.close()

    sql1 = "SELECT MOVIE FROM marvel"
    cursorObject = connection.cursor()
    cursorObject.execute(sql1)
    record = cursorObject.fetchall()
    for x in record:
        print(x)

    sql2 = "DELETE FROM marvel WHERE MOVIE= 'TheIncredibleHulk'"
    cursorObject = connection.cursor()
    cursorObject.execute(sql2)
    connection.commit()

    sql3 = "SELECT * FROM marvel WHERE MCU_PHASE='Phase2'"
    cursorObject = connection.cursor()
    cursorObject.execute(sql3)
    record2 = cursorObject.fetchall()
    for x in record2:
        print(x)

    sql4 = "UPDATE marvel SET DATE= 'November 3, 2017' WHERE MOVIE='Thor:Ragnarok'"
    cursorObject = connection.cursor()
    cursorObject.execute(sql4)
    connection.commit()

except mysql.connector.Error as error:
    print("Fail!",error)

finally:
    if connection.is_connected():
        cursorObject.close()
        connection.close()
        print("MySQL connection is closed.")

def listAll():
    textBox.delete("1.0", tk.END)
    list=[]
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="Marvel",
            user="root",
            password="root1234"
        )
        sql1 = "SELECT * FROM marvel"
        cursorObject = connection.cursor()
        cursorObject.execute(sql1)
        record = cursorObject.fetchall()
        for x in record:
            list.append(x)
    except mysql.connector.Error as error:
        print("Fail!", error)
    textBox.insert(END,list)


def addButtonFunc():
    popupWindow = tk.Toplevel(root)
    popupWindow.geometry("300x300")
    popupWindow.title("Add")
    label = tk.Label(popupWindow, text="Enter text:")
    textBox = tk.Entry(popupWindow)

    def okButtonFunc():
        try:
            connection = mysql.connector.connect(
                host="localhost",
                database="Marvel",
                user="root",
                password="root1234"
            )
            CursorObject = connection.cursor()
            text = textBox.get()
            split = text.split(" ")

            Insert = """INSERT INTO marvel (ID, MOVIE, DATE, MCU_PHASE)
                         VALUES (%s, %s, %s, %s)"""
            record = (split[0], split[1], split[2], split[3])
            CursorObject.execute(Insert, record)
            connection.commit()
            CursorObject.close()

        except mysql.connector.Error as error:
            print("Fail!", error)

        finally:
            if connection.is_connected():
                cursorObject.close()
                connection.close()

        popupWindow.destroy()

    def cancelButtonFunc():
        popupWindow.destroy()
    okButton=tk.Button(popupWindow, text="Ok", command=okButtonFunc)
    cancelButton=tk.Button(popupWindow, text="Cancel", command=cancelButtonFunc)

    label.grid(row=0, column=0)
    textBox.grid(row=0, column=1)
    okButton.grid(row=1, column=0)
    cancelButton.grid(row=1, column=1)

def show():
    textBox.delete("1.0", tk.END)
    try:
        list2=[]
        connection = mysql.connector.connect(
            host="localhost",
            database="Marvel",
            user="root",
            password="root1234"
        )
        sql = "SELECT * FROM marvel WHERE ID="+clicked.get()
        cursorObject = connection.cursor()
        cursorObject.execute(sql)
        record = cursorObject.fetchall()
        for x in record:
            list2.append(x)
    except mysql.connector.Error as error:
        print("Fail!", error)
    textBox.insert("end",list2)


textBox = tk.Text()
textBox.pack()

clicked=StringVar()
clicked.set("Select an ID")

dropDown=OptionMenu(root,clicked,*ıdList)
dropDown.pack()

b=tk.Button(text="Show",bg="red",fg="black",font="helvetica 10",command=show)
b.pack()
b1=tk.Button(text="List All",bg="orange",fg="black",font="helvetica 20",command=listAll)
b1.pack()
b2=tk.Button(root, text="Add",bg="orange",fg="black",font="helvetica 20",command=addButtonFunc)
b2.pack()

root.mainloop()