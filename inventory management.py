import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from tkinter import *
import os
import socket
import sys
from time import sleep
import csv
from datetime import date
from datetime import datetime
import xlsxwriter
import pandas as pd
import openpyxl
import pyodbc
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle


class MainClass(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Inventory Management System")
        self.wm_geometry("750x550")
        self.wm_resizable(False, False)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Login, SecondPage, ThirdPage, SignUp, MainPage, Inventory, Assign_items, View_Record, Developer):
            frame = F(container, self)

            self.frames[F] = frame
            

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Label(self, text="Welcome to Inventory Management System",
              font=("Times New Roman", 25, "bold"), bg="black", fg="white").pack(fill=X)
        photo = PhotoImage(file = 'img.png')
        l = Label(self, image=photo)
        l.image=photo
        l.pack() 
        button_main = ttk.Button(self, text="Login as Admin",command= lambda: controller.show_frame(SecondPage))
        button_main.place(x=250, y=70, width=150, height=40)

        button = ttk.Button(self, text="Login",
                           command=lambda: controller.show_frame(Login))
        button.place(x=250, y=130, width=150, height=40)

        Label(self, text="                                             Inventory Management System                               ", font=("Times New Roman", 15, 'bold'), bg="black", fg="white").place(x=0, y=515)

        conn = sqlite3.connect("Inventory.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS assigned(id integer unique primary key autoincrement, person_name TEXT, item_name TEXT, item_quantity INT, assigned_time TEXT, assigned_date TEXT)")
        c.execute('CREATE TABLE IF NOT EXISTS Login(id integer unique primary key autoincrement, Username TEXT, Password TEXT)')
        c.execute("CREATE TABLE IF NOT EXISTS Signup(id integer unique primary key autoincrement, frist_name TEXT, last_name TEXT, Username TEXT)")
        c.execute('CREATE TABLE IF NOT EXISTS Login(id integer unique primary key autoincrement, Username TEXT, Password TEXT)')
        c.execute("CREATE TABLE IF NOT EXISTS inventory(id integer unique primary key autoincrement, item_name TEXT, item_price INT, item_quantity INT)")
        
class SecondPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        Label(self, text="Admin Login Page", font=("Times New Roman",20, 'bold'), bg='black', fg='white').pack(fill=X)
        photo = PhotoImage(file = 'img.png')
        l = Label(self, image=photo)
        l.image=photo
        l.pack()
        Label(self, text="Admin Username", font=("Times new Roman", 14, 'bold'), bg='black', fg='white').place(x=100, y=70)
        admin_user = StringVar()
        admin_name = ttk.Entry(self, width=20, textvariable=admin_user)
        admin_name.place(x=260, y=76)

        Label(self, text="Admin Password", font=("Times New Roman", 14, 'bold'), bg='black', fg='white').place(x=100, y=100)
        admin_pass = StringVar()
        admin_password = ttk.Entry(self, width=20, textvariable=admin_pass, show="*")
        admin_password.place(x=260, y=105)

        btn_admin = ttk.Button(self, text="Login", command= lambda: checker())
        btn_admin.place(x=275, y=135)

        btn_back = ttk.Button(self, text="Back", command= lambda: controller.show_frame(StartPage))
        btn_back.place(x=5, y=55)
        Label(self, text="                                             Inventory Management System                               ", font=("Times New Roman", 15, 'bold'), bg="black", fg="white").place(x=0, y=515)

        def checker():
            admin_name_error = admin_user.get()
            admin_pass_error = admin_pass.get()
            if admin_name_error == "":
                messagebox.showerror("Error", "Please Fill The Fields First")
            elif admin_pass_error == "":
                messagebox.showerror("Error","Please Fill The Fields First")
            elif admin_name_error == "Ali" and admin_pass_error == "Ali@UE":
                controller.show_frame(ThirdPage)
            else:
                messagebox.showerror("Error", "Invalid Username or Password")
                admin_name.delete(0, END)
                admin_password.delete(0, END)
                
class ThirdPage(tk.Frame):
    
    def __init__(self, parent, controller):
        

        tk.Frame.__init__(self, parent)
        Label(self, text="SignUp or Login", font=("Times New Roman", 20, 'bold'), bg="black", fg="white").pack(fill=X)
        photo = PhotoImage(file = 'img.png')
        l = Label(self, image=photo)
        l.image=photo
        l.pack()
        btn_signUp = ttk.Button(self, text="Signup", command= lambda: controller.show_frame(SignUp))
        btn_signUp.place(x=490, y=70, width=150, height=40)

        btn_login = ttk.Button(self, text="Login", command = lambda: controller.show_frame(Login))
        btn_login.place(x=490, y=130, width=150, height=40)
        Label(self, text="                                  Facial Recoginition Attendance System                               ", font=("Times New Roman", 15, 'bold'), bg="black", fg="white").place(x=0, y=515)


class Login(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Label(self, text="Login", font=("Times new Roman", 20, "bold"), bg="black", fg="white").pack(fill=X)

        photo = PhotoImage(file = 'img.png')
        l = Label(self, image=photo)
        l.image=photo
        l.pack()

        Label(self, text="Username", font=("Times New Roman", 14, "bold"), bg='black', fg='white').place(x=100, y=100)
        user_var = StringVar()
        user = ttk.Entry(self, width=20, textvariable=user_var)
        user.place(x=200, y=101)
        user.focus()

        Label(self, text="Password", font=("Times New Roman", 14, "bold"), bg='black', fg='white').place(x=100, y=130)

        pass_var = StringVar()
        password = ttk.Entry(self, width=20, textvariable=pass_var, show="*")
        password.place(x=200, y=130)

        button2 = ttk.Button(self, text="Login", command=lambda: check())
        button2.place(x=220, y=165)


        button1 = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(StartPage))
        button1.place(x=5, y=50)
        Label(self, text="                                             Inventory Management System                               ", font=("Times New Roman", 15, 'bold'), bg="black", fg="white").place(x=0, y=515)

        def check():
            conn = sqlite3.connect("Inventory.db")
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS Login(id integer unique primary key autoincrement, Username TEXT, Password TEXT)')
            conn.commit()
            a = user.get()
            b = password.get()
            if a == "":
                 messagebox.showerror("Invalid Input", "Please Enter Username")
            elif b == "":
                messagebox.showerror("Invalid Input", "Please Enter Password")
            else:
                with sqlite3.connect("Inventory.db") as db:
                    cursor=db.cursor()
                
                find_user= ("SELECT * FROM Login WHERE Username = ? AND Password = ?")
                cursor.execute(find_user,[(a),(b)])
                results=cursor.fetchall()
                if results:
                    for i in results:
                        controller.show_frame(MainPage)
                else:
                    messagebox.showerror("Invalid", "Invalid Username or Password.")

              
class SignUp(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        conn = sqlite3.connect("Inventory.db")
        c = conn.cursor()
        Label(self, text="Sign Up", font=("Times New Roman", 20, 'bold'), bg="black", fg="white").pack(fill=X)

        photo = PhotoImage(file = 'img.png')
        l = Label(self, image=photo)
        l.image=photo
        l.pack()

        Label(self, text="First Name", font=("Times New Roman", 12, 'bold'), bg="black", fg="white").place(x=150, y=70)

        fname_var = StringVar()
        frist_name = ttk.Entry(self, width=20, textvariable=fname_var)
        frist_name.place(x=240, y=70)
        frist_name.focus()

        Label(self, text="Last Name", font=("Times New Roman", 12, 'bold'), bg="black", fg="white").place(x=150, y=100)

        lname_var = StringVar()
        last_name = ttk.Entry(self, width=20, textvariable=lname_var)
        last_name.place(x=240, y=100)
        Label(self, text="Username", font=("Times New Roman", 12, 'bold'), bg="black", fg="white").place(x=150, y=130)

        usr_var = StringVar()
        user_name = ttk.Entry(self, width=20, textvariable=usr_var)
        user_name.place(x=240, y=130)

        Label(self, text="Password", font=("Times New Roman", 12, 'bold'), bg="black", fg="white").place(x=150, y=160)

        pass_var = StringVar()
        passwor = ttk.Entry(self, width=20, textvariable=pass_var, show="*")
        passwor.place(x=240, y=160)

        Label(self, text="Confirm Password", font=("Times New Roman", 12, 'bold'), bg="black", fg="white").place(x=100, y=190)

        conpass_var = StringVar()
        con_pass = ttk.Entry(self, width=20, textvariable=conpass_var, show="*")
        con_pass.place(x=240, y=190)

        btn_sign = ttk.Button(self, text="Signup", command = lambda: save())
        btn_sign.place(x=240, y=220,width=110, height=40)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.place(x=5, y=50)

        button2 = ttk.Button(self, text="Go to Login Page",
                            command=lambda: controller.show_frame(Login))
        button2.place(x=240, y=270, width=110, height=40)
        Label(self, text="                                             Inventory Management System                               ", font=("Times New Roman", 15, 'bold'), bg="black", fg="white").place(x=0, y=515)
        def save():
            user_error = usr_var.get()
            lname_error = lname_var.get()
            fname_error = fname_var.get()
            pass_error = pass_var.get()
            conpass_error = conpass_var.get()

            if fname_error == "":
                messagebox.showerror("Invalid Input", "Please Enter First Name")
            elif lname_error == "":
                messagebox.showerror("Invalid Input", "Please Enter Last Name")
            elif user_error == "":
                messagebox.showerror("Invalid Input", "Please Enter Username")
            elif pass_error == "":
                messagebox.showerror("Invalid Input", "Please Enter Password")
            elif conpass_error == "":
                messagebox.showerror("Invalid Input", "Please Enter Confirm Password")
            elif pass_error != conpass_error:
                messagebox.showerror("Invalid Input", "Password Does Not Matches")
            else:
                conn=sqlite3.connect('Inventory.db')
                c=conn.cursor()
                c.execute("CREATE TABLE IF NOT EXISTS Signup(id integer unique primary key autoincrement, frist_name TEXT, last_name TEXT, Username TEXT)")
                c.execute("INSERT INTO Signup(frist_name, last_name, Username) VALUES (?,?,?)", (fname_var.get(), lname_var.get(), usr_var.get()))
                c.execute('CREATE TABLE IF NOT EXISTS Login(id integer unique primary key autoincrement, Username TEXT, Password TEXT)')
                c.execute('INSERT INTO Login(Username, Password) VALUES(?,?)', (usr_var.get(), pass_var.get()))
                conn.commit()
                messagebox.showinfo("Saved", "Data Saved Successfully!")
                frist_name.delete(0, END)
                last_name.delete(0,END)
                user_name.delete(0,END)
                passwor.delete(0,END)
                con_pass.delete(0,END)

class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Label(self, text="Manage Inventory Or Assign Items", font=("Times New Roman", 20, 'bold'), bg="black", fg="white").pack(fill=X)

        photo = PhotoImage(file = 'img.png')
        l = Label(self, image=photo)
        l.image=photo
        l.pack()

        button_main = ttk.Button(self, text="Inventory",command= lambda: controller.show_frame(Inventory))
        button_main.place(x=250, y=70, width=150, height=40)

        button = ttk.Button(self, text="Assign Items",
                           command=lambda: controller.show_frame(Assign_items))
        button.place(x=250, y=130, width=150, height=40)

        button_main = ttk.Button(self, text="View Assigned Items",command= lambda: controller.show_frame(View_Record))
        button_main.place(x=250, y=190, width=150, height=40)

        button_main = ttk.Button(self, text="About Developer",command= lambda: controller.show_frame(Developer))
        button_main.place(x=250, y=250, width=150, height=40)
        Label(self, text="                                             Inventory Management System                               ", font=("Times New Roman", 15, 'bold'), bg="black", fg="white").place(x=0, y=515)


class Assign_items(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        Label(self, text="Assign Inventory Item To Peoples", font=("Times New Roman", 20, 'bold'), bg="black", fg="white").pack(fill=X)

        photo = PhotoImage(file = 'img.png')
        l = Label(self, image=photo)
        l.image=photo
        l.pack()

        Label(self, text=" Assigned To", font=("Times new Roman", 12, 'bold'), bg="black", fg="white").place(x=150, y=70)
        
        assigned_to_var = StringVar()
        assigned_to_name = ttk.Entry(self, width=20, textvariable=assigned_to_var)
        assigned_to_name.place(x=270, y=70)
        assigned_to_name.focus()

        Label(self, text="Item Name", font=("Times New Roman", 12, 'bold'), bg="black", fg="white").place(x=150, y=100)

        conn = sqlite3.connect("Inventory.db")
        c = conn.cursor()
        find_data= ("SELECT item_name FROM inventory")
        c.execute(find_data)
        resultss=c.fetchall()


        item_name_var = StringVar()
        assigned_item_name = ttk.Combobox(self, width=17, textvariable=item_name_var,font=("Times New Roman", 10), state='readonly')
        assigned_item_name['values'] = resultss
        assigned_item_name.place(x=270, y=100)


        Label(self, text="Item Quantity", font=("Times New Roman", 12, 'bold'), bg="black", fg="white").place(x=150, y=130)

        item_quantity_var = StringVar()
        assigned_item_quantitiy = ttk.Entry(self, width=20, textvariable=item_quantity_var)
        assigned_item_quantitiy.place(x=270, y=130)

        btn_emp = ttk.Button(self, text="Assign Item", command= lambda: save_assigned_data())
        btn_emp.place(x=270, y=160,width=140, height=40)

        btn_emp = ttk.Button(self, text="Refresh", command= lambda: refresh())
        btn_emp.place(x=270, y=210,width=140, height=40)
        btn_back = ttk.Button(self, text="Back", command= lambda: controller.show_frame(MainPage))
        btn_back.place(x=5, y=50)
        Label(self, text="                                             Inventory Management System                               ", font=("Times New Roman", 15, 'bold'), bg="black", fg="white").place(x=0, y=515)


        def refresh():
            a = assigned_item_name.get()
            conn = sqlite3.connect("Inventory.db")
            c = conn.cursor()
            find_data= ("SELECT item_name FROM inventory")
            c.execute(find_data)
            resultss=c.fetchall()
            assigned_item_name['values'] = resultss

        def save_assigned_data():
            assigned_name_error = assigned_to_var.get()
            assigned_item_name_error = item_name_var.get()
            assigned_quantity_error = item_quantity_var.get()
            try:
                item_assigned_quantity = int(float(assigned_quantity_error))
            except ValueError:
                messagebox.showerror("Invalid", "Please Enter Only Integer In Quantity")
            if assigned_name_error == "":
                messagebox.showerror("Invalid", "Please Enter Name Of the Person.")
            elif len(assigned_item_name_error) == 0:
                messagebox.showerror("Invalid", "Please Select An Item")
            elif assigned_quantity_error == "":
                messagebox.showerror("Invalid", "Please Enter Quantity Of Item.")
            elif True:
                    try:
                        int(assigned_quantity_error)
                    except ValueError:
                        pass
                    else:
                        date_object = datetime.now()
                        date_now = date_object.strftime("%Y-%m-%d")
                        time_now = date_object.strftime("%H:%M:%S")
    
                        conn = sqlite3.connect("Inventory.db")
                        c = conn.cursor()
                        c.execute("CREATE TABLE IF NOT EXISTS assigned(id integer unique primary key autoincrement, person_name TEXT, item_name TEXT, item_quantity INT, assigned_time TEXT, assigned_date TEXT)")
                        c.execute('SELECT item_quantity FROM inventory WHERE item_name = :item', {'item': str(assigned_item_name.get())})
                        i = c.fetchall()
                        try:
                            item_availble_quantity = i[0][0]
                        except IndexError:
                            messagebox.showerror("Invalid", "Item Is No Longer Availble In Inventory Please Refresh")
                        try:
                            remaining_quantity = item_availble_quantity - item_assigned_quantity
                        except UnboundLocalError:
                            pass
                        try:                        
                            if remaining_quantity == 0:
                                c.execute('SELECT item_name FROM inventory WHERE item_name = :item', {'item': str(assigned_item_name.get())})
                                i = c.fetchall()
                                try:
                                    item_name_availble = i[0][0]
                                except IndexError:
                                    messagebox.showerror("Invalid", "Item Is No Longer Availble In Inventory Please Refresh")
                                print(item_name_availble)
                                c.execute("DELETE FROM inventory WHERE item_name = (?) ", [item_name_availble])
                                conn.commit()
                                assigned_to_name.delete(0, END)
                                print([assigned_item_name.get()])
                                assigned_item_quantitiy.delete(0, END)
                                messagebox.showinfo("Quantity", "All the items of this "+str(item_name_var.get())+" Are Assigned No More Quantity Is Availble")
                        
                        # elif item_availble_quantity == 0:
                        #     c.execute("DELETE FROM inventory WHERE item_name = :item",{'item': str(assigned_item_name.get())})

                            elif remaining_quantity < 0:
                                messagebox.showerror("Invalid", "Item Quantity Exceeds From Availble Quantity Please Check Availble Quantity From Inventory")
                        
                            else:
                                c.execute('INSERT INTO assigned (person_name, item_name, item_quantity, assigned_time, assigned_date) VALUES (?,?,?,?,?)',(assigned_to_name.get(), assigned_item_name.get(), assigned_item_quantitiy.get(), time_now, date_now ))
                                c.execute('UPDATE inventory SET item_quantity = :quantity WHERE item_name = :item',{'item': str(assigned_item_name.get()), "quantity": remaining_quantity})
                                conn.commit()
                                assigned_to_name.delete(0, END)
                                assigned_item_quantitiy.delete(0, END)
                                messagebox.showinfo("Success", "Items Are Assigned Successfully")
                        except IndexError:
                            messagebox.showerror("Invalid", "Item No Longer Availble Please Refresh")

class Inventory(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        photo = PhotoImage(file = 'img.png')
        l = Label(self, image=photo)
        l.image=photo
        l.pack()
        Label(self, text="Item Name", font=("Times new Roman", 12, 'bold'), bg="black", fg="white").place(x=5, y=50)
        item_name_var = StringVar()
        item_name_inventory = ttk.Entry(self, width=20, textvariable=item_name_var)
        item_name_inventory.place(x=120, y=50)
        item_name_inventory.focus()

        Label(self, text="Item Price", font=("Times new Roman", 12, 'bold'), bg="black", fg="white").place(x=5, y=80)
        
        item_price_var = StringVar()
        item_price_inventory = ttk.Entry(self,width=20, textvariable=item_price_var)
        item_price_inventory.place(x=120, y=80)

        Label(self, text="Item Quantity", font=("Times New Roman", 12, 'bold'), bg="black", fg="white").place(x=5, y=120)

        item_quantity_var = StringVar()
        item_quantity_inventory = ttk.Entry(self,width=20, textvariable=item_quantity_var)
        item_quantity_inventory.place(x=120, y=120)

        btn_emp = ttk.Button(self, text="Add Item", command= lambda: inventory_save())
        btn_emp.place(x=70, y=160,width=140, height=40)

        btn_emp = ttk.Button(self, text="Show Item", command= lambda: show_data())
        btn_emp.place(x=70, y=210,width=140, height=40)

        btn_emp = ttk.Button(self, text="Refresh", command= lambda: refresh())
        btn_emp.place(x=70, y=260,width=140, height=40)

        btn_emp = ttk.Button(self, text="Delete Record", command= lambda: dlt())
        btn_emp.place(x=70, y=310,width=140, height=40)

        btn_emp = ttk.Button(self, text="Save To Excel", command= lambda: xlsx())
        btn_emp.place(x=70, y=360,width=140, height=40)

        btn_emp = ttk.Button(self, text="Save To PDF", command= lambda: pdf())
        btn_emp.place(x=70, y=410,width=140, height=40)

        Label(self, text="Search By Item Name Here",font=("Times New Roman", 15, 'bold'), bg="black", fg="white").place(x=150, y=10)
        search_var = StringVar()
        search = ttk.Entry(self,width=20, textvariable=search_var)
        search.place(x=400, y=10)

        btn_back = ttk.Button(self, text="Search", command= lambda: search_by_item_name())
        btn_back.place(x=550, y=10)

        btn_back = ttk.Button(self, text="Back", command= lambda: controller.show_frame(MainPage))
        btn_back.place(x=5, y=10)
        Label(self, text="                                             Inventory Management System                               ", font=("Times New Roman", 15, 'bold'), bg="black", fg="white").place(x=0, y=515)

        tree = ttk.Treeview(self)
        tree["columns"]=("one","two","three", "four")
        tree.column("#0", width=0, minwidth=50, stretch=tk.NO)
        tree.column("one", width=50, minwidth=50, stretch=tk.NO)
        tree.column("two", width=120, minwidth=120)
        tree.column("three", width=120, minwidth=120, stretch=tk.NO)
        tree.column("four", width=120, minwidth=120, stretch=tk.NO)
        tree.heading("#0",text="index",anchor=tk.W)
        tree.heading("one", text="ID",anchor=tk.W)
        tree.heading("two", text="Item Name",anchor=tk.W)
        tree.heading("three", text="Item Price",anchor=tk.W)
        tree.heading("four", text="Item Quantity", anchor= tk.W)
        tree.place(x=300, y=40, width=420, height=450)


        def inventory_save():
            item_name_error = item_name_var.get()
            item_quantity_error = item_quantity_var.get()
            item_price_error = item_price_var.get()

            if item_name_error == "":
                messagebox.showerror("Invalid", "Please Enter Item Name")
            
            elif item_price_error == "":
                messagebox.showerror("Invalid", "Please Enter Item Price")
            elif True:
                try:
                    int(item_price_error)
                except ValueError:
                    messagebox.showerror("Invalid", "Please Enter Only Integer In Price")
                
                else:
                    if item_quantity_error == "":
                        messagebox.showerror("Invalid", "Please Enter Item Quantity")
            
                    elif True:
                        try:
                            int(item_quantity_error)
                        except ValueError:
                            messagebox.showerror("Invalid", "Please Enter Only Integer In Quantity")
                        else:
                            conn = sqlite3.connect("Inventory.db")
                            c = conn.cursor()
                            c.execute("CREATE TABLE IF NOT EXISTS inventory(id integer unique primary key autoincrement, item_name TEXT, item_price INT, item_quantity INT)")
                            c.execute('INSERT INTO inventory (item_name, item_price, item_quantity) VALUES (?,?,?)',(item_name_var.get(), item_price_var.get(), item_quantity_var.get()))
                            conn.commit()
                            item_name_inventory.delete(0, END)
                            item_price_inventory.delete(0, END)
                            item_quantity_inventory.delete(0, END)
                            messagebox.showinfo("Success", "Item added Successfully Please Refresh")

        def show_data():
            conn = sqlite3.connect("Inventory.db")
            c = conn.cursor()
            c.execute('SELECT * FROM inventory')
            data_inventory = c.fetchall()
            counter = len(tree.get_children())

            if counter == 0:
                for items in data_inventory:
                    tree.insert("", tk.END, values= items)
                conn.close()
            else:
                messagebox.showerror("Error", "Data Already Shown")

        def refresh():
            for i in tree.get_children():
                tree.delete(i)
            conn = sqlite3.connect("Inventory.db")
            c = conn.cursor()
            c.execute('SELECT * FROM inventory')
            data_inventory = c.fetchall()
            for items in data_inventory:
                tree.insert("", tk.END, values= items)
            conn.close()


        def dlt():
            conn = sqlite3.connect("Inventory.db")
            c = conn.cursor()
            try:
                id = tree.item(tree.selection())['values']
                dlt_id = id[1]
                c.execute("DELETE FROM inventory WHERE item_name=?;", ([(dlt_id)]))
                messagebox.showinfo('Success', 'Record Deleted Successfully Please Refresh To See Changes')
                conn.commit()
                conn.close()
            except IndexError as e:
                messagebox.showerror("Error", "Please Select A Record")
                return
        def pdf():
            conn = sqlite3.connect("Inventory.db")
            c = conn.cursor()
            c.execute('SELECT * FROM inventory')
            data_inventory = c.fetchall()
            counter = len(tree.get_children())
            if counter == 0:
                messagebox.showerror("Error", "No Data Availble in Table")
            else:
                if not os.path.exists('./Inventory Data PDF'):
                    os.makedirs('./Inventory Data PDF')
                today = str(date.today())
                pdf = SimpleDocTemplate("./Inventory Data PDF/Inventory List "+today+".pdf")
                flow_obj = []
                td = [['ID','Item Name', "Item Price", "Item Quantity"]]
                for i in data_inventory:
                    td.append(i)
                table = Table(td)
                flow_obj.append(table)
                pdf.build(flow_obj)
                messagebox.showinfo("Success", "PDF generated Successfully")

        def xlsx():
            conn = sqlite3.connect("Inventory.db")
            c = conn.cursor()
            c.execute('SELECT * FROM inventory')
            data_employee = c.fetchall()
            counter = len(tree.get_children())
            today = str(date.today())
            if counter == 0:
                messagebox.showerror("Error", "No Data Availble in Table")
            else:
                if not os.path.exists('./Inventory Data Excel'):
                    os.makedirs('./Inventory Data Excel')
                data = pd.DataFrame(data_employee, columns= ['ID','Item Name', 'Item Price', 'Item Quantity'])
                datatoexcel = pd.ExcelWriter("Inventory Data Excel/Inventory List "+today+".xlsx", engine='xlsxwriter')
                data.to_excel(datatoexcel, index=False, sheet_name = "Sheet")
                worksheet = datatoexcel.sheets['Sheet']
                worksheet.set_column('A:A', 25)
                worksheet.set_column('B:B', 20)
                worksheet.set_column('C:C', 25)
                worksheet.set_column('D:D', 20)
                datatoexcel.save()
                messagebox.showinfo("Success", "Excel File is Generated Successfully")

        def search_by_item_name():
            for i in tree.get_children():
                tree.delete(i)
            id_error = search_var.get()

            conn = sqlite3.connect("Inventory.db")
            c = conn.cursor()
            id_search = str(search_var.get())
            find_data= ("SELECT * FROM inventory WHERE item_name = ?")
            c.execute(find_data,[(id_search)])
            resultss=c.fetchall()
            counter_data = len(tree.get_children())

            if id_error == "":
                messagebox.showerror("Error", "Please Enter Item Name")
            
            elif len(resultss) ==0:
                messagebox.showerror("Error", "Invalid Input or Item Does Not Exists")

            elif counter_data == 0:
                for r in resultss:
                    tree.insert("", tk.END, values=r)

class View_Record(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        photo = PhotoImage(file = 'img.png')
        l = Label(self, image=photo)
        l.image=photo
        l.pack()

        btn_back = ttk.Button(self, text="Back", command= lambda: controller.show_frame(MainPage))
        btn_back.place(x=5, y=10)

        btn_emp = ttk.Button(self, text="Show Record", command= lambda: show_data())
        btn_emp.place(x=10, y=100,width=140, height=40)

        btn_emp = ttk.Button(self, text="Refresh", command= lambda: refresh())
        btn_emp.place(x=10, y=150,width=140, height=40)

        btn_emp = ttk.Button(self, text="Delete Record", command= lambda: dlt())
        btn_emp.place(x=10, y=200,width=140, height=40)

        btn_emp = ttk.Button(self, text="Save To Excel", command= lambda: xlsx())
        btn_emp.place(x=10, y=250,width=140, height=40)

        btn_emp = ttk.Button(self, text="Save To PDF", command= lambda: pdf())
        btn_emp.place(x=10, y=300,width=140, height=40)

        Label(self, text="Search By Person Name Here",font=("Times New Roman", 15, 'bold'), bg="black", fg="white").place(x=120, y=10)
        search_var = StringVar()
        search = ttk.Entry(self,width=20, textvariable=search_var)
        search.place(x=400, y=10)

        btn_back = ttk.Button(self, text="Search", command= lambda: search_by_item_name())
        btn_back.place(x=550, y=10)

        btn_back = ttk.Button(self, text="Back", command= lambda: controller.show_frame(MainPage))
        btn_back.place(x=5, y=10)
        Label(self, text="                                             Inventory Management System                               ", font=("Times New Roman", 15, 'bold'), bg="black", fg="white").place(x=0, y=515)

        tree = ttk.Treeview(self)
        tree["columns"]=("one","two","three", "four", "five", "six")
        tree.column("#0", width=0, minwidth=50, stretch=tk.NO)
        tree.column("one", width=50, minwidth=50, stretch=tk.NO)
        tree.column("two", width=70, minwidth=70)
        tree.column("three", width=70, minwidth=70, stretch=tk.NO)
        tree.column("four", width=100, minwidth=100, stretch=tk.NO)
        tree.column("five", width=70, minwidth=70, stretch=tk.NO)
        tree.column("six", width=70, minwidth=70, stretch=tk.NO)

        tree.heading("#0",text="index",anchor=tk.W)
        tree.heading("one", text="ID",anchor=tk.W)
        tree.heading("two", text="Person Name",anchor=tk.W)
        tree.heading("three", text="Item Name",anchor=tk.W)
        tree.heading("four", text="Item Quantity", anchor= tk.W)
        tree.heading("five", text="Time", anchor= tk.W)
        tree.heading("six", text="Date", anchor= tk.W)
        tree.place(x=170, y=40, width=500, height=450)

        def show_data():
            conn = sqlite3.connect("Inventory.db")
            c = conn.cursor()
            c.execute('SELECT * FROM assigned')
            data_inventory = c.fetchall()
            counter = len(tree.get_children())

            if counter == 0:
                for items in data_inventory:
                    tree.insert("", tk.END, values= items)
                conn.close()
            else:
                messagebox.showerror("Error", "Data Already Shown")

        def refresh():
            for i in tree.get_children():
                tree.delete(i)
            conn = sqlite3.connect("Inventory.db")
            c = conn.cursor()
            c.execute('SELECT * FROM assigned')
            data_inventory = c.fetchall()
            for items in data_inventory:
                tree.insert("", tk.END, values= items)
            conn.close()


        def dlt():
            conn = sqlite3.connect("Inventory.db")
            c = conn.cursor()
            try:
                id = tree.item(tree.selection())['values']
                dlt_id = id[1]
                c.execute("DELETE FROM assigned WHERE person_name=?;", ([(dlt_id)]))
                messagebox.showinfo('Success', 'Record Deleted Successfully Please Refresh To See Changes')
                conn.commit()
                conn.close()
            except IndexError as e:
                messagebox.showerror("Error", "Please Select A Record")
                return

        def pdf():
            conn = sqlite3.connect("Inventory.db")
            c = conn.cursor()
            c.execute('SELECT * FROM assigned')
            data_inventory = c.fetchall()
            counter = len(tree.get_children())
            if counter == 0:
                messagebox.showerror("Error", "No Data Availble in Table")
            else:
                if not os.path.exists('./Assigned Data PDF'):
                    os.makedirs('./Assigned Data PDF')
                today = str(date.today())
                pdf = SimpleDocTemplate("./Assigned Data PDF/Assigned List "+today+".pdf")
                flow_obj = []
                td = [['ID','Person Name', "Item Name", "Item Quantity", "Time", "Date"]]
                for i in data_inventory:
                    td.append(i)
                table = Table(td)
                flow_obj.append(table)
                pdf.build(flow_obj)
                messagebox.showinfo("Success", "PDF generated Successfully")

        def xlsx():
            conn = sqlite3.connect("Inventory.db")
            c = conn.cursor()
            c.execute('SELECT * FROM assigned')
            data_employee = c.fetchall()
            counter = len(tree.get_children())
            today = str(date.today())
            if counter == 0:
                messagebox.showerror("Error", "No Data Availble in Table")
            else:
                if not os.path.exists('./Assigned Data Excel'):
                    os.makedirs('./Assigned Data Excel')
                data = pd.DataFrame(data_employee, columns= ['ID','Person Name', 'Item Name', 'Item Quantity', 'Time', 'Date'])
                datatoexcel = pd.ExcelWriter("Assigned Data Excel/Assigned List "+today+".xlsx", engine='xlsxwriter')
                data.to_excel(datatoexcel, index=False, sheet_name = "Sheet")
                worksheet = datatoexcel.sheets['Sheet']
                worksheet.set_column('A:A', 25)
                worksheet.set_column('B:B', 20)
                worksheet.set_column('C:C', 25)
                worksheet.set_column('D:D', 20)
                worksheet.set_column('E:E', 20)
                worksheet.set_column('F:F', 20)
                datatoexcel.save()
                messagebox.showinfo("Success", "Excel File is Generated Successfully")

        def search_by_item_name():
            for i in tree.get_children():
                tree.delete(i)
            id_error = search_var.get()

            conn = sqlite3.connect("Inventory.db")
            c = conn.cursor()
            id_search = str(search_var.get())
            find_data= ("SELECT * FROM assigned WHERE person_name = ?")
            c.execute(find_data,[(id_search)])
            resultss=c.fetchall()
            counter_data = len(tree.get_children())

            if id_error == "":
                messagebox.showerror("Error", "Please Enter Person Name")
            
            elif len(resultss) ==0:
                messagebox.showerror("Error", "Invalid Input or Person Does Not Exists")

            elif counter_data == 0:
                for r in resultss:
                    tree.insert("", tk.END, values=r)

class Developer(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Label(self, text="Developer's Page", font=("Times New Roman", 20, 'bold'), bg="black", fg="white").pack(fill=X)

        photo = PhotoImage(file = 'img.png')
        l = Label(self, image=photo)
        l.image=photo
        l.pack()

        Label(self, text="Developer Name:", font=("Times New Roman", 20, 'bold'), bg="black", fg="white").place(x=50, y=50)

        Label(self, text="Haider khalil", font=("Times New Roman", 40, 'bold'), bg="black", fg="white").place(x=50, y=80)

        Label(self, text="Developer's Email:", font=("Times New Roman", 20, 'bold'), bg="black", fg="white").place(x=50, y=170)

        Label(self, text="(haiderkhalil0000@gmail.com)", font=("Times New Roman", 40, 'bold'), bg="black", fg="white").place(x=50, y=200)

        Label(self, text="                                             Inventory Management System                               ", font=("Times New Roman", 15, 'bold'), bg="black", fg="white").place(x=0, y=515)


app = MainClass()
app.mainloop()
