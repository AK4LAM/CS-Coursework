#Import Necessary Modules
from tkinter import *

import sqlite3

import datetime

from tkinter import messagebox

import time

import re

success = False

# Make database if it does not alrady exist
database = sqlite3.connect("Login_Details.db")
cursor = database.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS UserDetails(username TEXT NOT NULL PRIMARY KEY,password TEXT NOT NULL,
               UserID INT AUTO_INCREMENT);''')
cursor.execute('''CREATE TABLE IF NOT EXISTS UserProgress(username TEXT NOT NULL PRIMARY KEY,
                lastSignOn INT, totalQDone INT DEFAULT 1, totalQCorrect INT DEFAULT 1, pureQDone INT DEFAULT 1,
                pureQCorrect INT DEFAULT 1,  mechQDone INT DEFAULT 1, mechQCorrect INT DEFAULT 1,statsQDone INT DEFAULT 1,
                statsQCorrect INT DEFAULT 1, FOREIGN KEY(username) REFERENCES UserDetails(username));''')
database.commit()
database.close()

#Main Class
class main:
    def __init__(self,master):
    	#Initialise windows, variables and wigets
        self.master = master
        self.username = StringVar()
        self.password = StringVar()
        self.newUsername = StringVar()
        self.newPassword = StringVar()
        self.screenWidgets()


    #Regex to validate username and password
    def validRegex(self, usernameToCheck, passwordToCheck):
        #Regex for password
        regexPassword = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$"
        matchRe = re.compile(regexPassword)
        res = re.search(matchRe, passwordToCheck)
        #If password is valid, username is checked
        if res:
            print("Please enter username should be \n1)Should only be letters\n2) Length Should be 5-12: ")
            #Regex for username
            regexUsername = "^[a-zA-Z]{5,12}$"
            matchRe1 = re.compile(regexUsername)
            res1 = re.search(matchRe1, usernameToCheck)
            if res1:
                return False
        else:
            return True
    
    #Login Function
    def login(self):
    	#Connect to database
        with sqlite3.connect('Login_Details.db') as database:
            cursor = database.cursor()

        #Check if user exists
        find_user = ("SELECT * FROM UserDetails WHERE username = ? and password = ?")
        cursor.execute(find_user,[(self.username.get()),(self.password.get())])
        result = cursor.fetchall()
        if result:
            self.loginFrame.pack_forget()
            self.head["text"] = "Welcome \n" + self.username.get()
            self.head["pady"] = 50
            success = True
            timeInSeconds = int(time.time())
            usernameSelection = self.username.get()
            cursor.execute("UPDATE UserProgress SET lastSignOn = (?) WHERE username = (?)", (timeInSeconds, usernameSelection))
        else:
            messagebox.showerror("Username Not Found.")
            success = False

        if success == True:
            loginWindow.destroy()
            import MainScreenV5
            
    def new_user(self):
        #Connect to database
        with sqlite3.connect('Login_Details.db') as database:
            cursor = database.cursor()

        #Check whether username already used
        find_user = ("SELECT username FROM UserDetails WHERE username = ?")
        cursor.execute(find_user,[(self.newUsername.get())])
        invalid = self.validRegex(self.newUsername.get(), self.newPassword.get())
        if cursor.fetchall():
            messagebox.showerror("Error!","Username Taken Try a Different One.")
        elif invalid:
            messagebox.showerror("Error!", "Username must be 5-12 characters long and only letters \n \n Password must be 8-18 characters long, containing a capital letter, special character and a number")
            self.showCreate()
        else:
            messagebox.showinfo("Success!","Account Created!")
            self.showLogin()
            #Create new account
            insertDetails = "INSERT INTO UserDetails(username, password) VALUES(?, ?)"
            cursor.execute(insertDetails,[(self.newUsername.get()),(self.newPassword.get())])
            insertProgress = "INSERT INTO UserProgress(username, lastSignOn) VALUES(?, ?)"
            cursor.execute(insertProgress,[(self.newUsername.get()), round(time.time())])
            database.commit()

    #Frame Packing
    #Show login screen
    def showLogin(self):
        self.username.set('')
        self.password.set('')
        self.createFrame.pack_forget()
        self.head["text"] = "Login"
        self.loginFrame.pack()
    #Show create account screen
    def showCreate(self):
        self.newUsername.set('')
        self.newPassword.set('')
        self.loginFrame.pack_forget()
        self.head["text"] = "Create Account"
        self.createFrame.pack()
        
    #Draw Widgets
    def screenWidgets(self):
        # Widgets for login frame
        self.head = Label(self.master, text = "Login", font = ('',35), pady = 10, bg = "#FFF2CC")
        self.head.pack()
        self.loginFrame = Frame(self.master, padx =10, pady = 10, bg = "#FFF2CC")
        Label(self.loginFrame, text = "Username: ", font = ('',20), pady=10, padx=25, bg = "#FFF2CC").grid(sticky = W)
        Entry(self.loginFrame, textvariable = self.username, bd = 5, font = ('',15)).grid(row=0,column=1)
        Label(self.loginFrame, text = "Password: ", font = ('',20), pady=10, padx=25, bg = "#FFF2CC").grid(sticky = W)
        Entry(self.loginFrame, textvariable = self.password, bd = 5, font = ('',15), show = '*').grid(row=1,column=1)
        Button(self.loginFrame, text = "Login", bd = 3 , font = ('',15), padx=5, pady=10, bg = "#FFF2CC", command=self.login).grid()
        Button(self.loginFrame, text = "Go to Create Account ", bd = 3, font = ('',15), padx=5, pady=10, bg = "#FFF2CC",
               command=self.showCreate).grid(row=2,column=1)
        self.loginFrame.pack()

        #Widgets for create account frame
        self.createFrame = Frame(self.master, padx =10, pady = 10, bg = "#FFF2CC")
        Label(self.createFrame, text = "Username: ", font = ('',20), pady=10, padx=25, bg = "#FFF2CC").grid(sticky = W)
        Entry(self.createFrame, textvariable = self.newUsername, bd = 5, font = ('',15)).grid(row=0,column=1)
        Label(self.createFrame, text = "Password: ", font = ('',20), pady=10, padx=25, bg = "#FFF2CC").grid(sticky = W)
        Entry(self.createFrame, textvariable = self.newPassword, bd = 5, font = ('',15), show = '*').grid(row=1,column=1)
        Button(self.createFrame, text = "Create Account", bd = 3 , font = ('',15), padx=5, pady=10, bg = "#FFF2CC",
               command=self.new_user).grid()
        Button(self.createFrame, text = "Go to Login", bd = 3 , font = ('',15), padx=5, pady=10, bg = "#FFF2CC",
               command=self.showLogin).grid(row=2,column=1)

if __name__ == "__main__":
    #Window initialisiation
    loginWindow = Tk()
    loginWindow.title("Login Form")
    loginWindow.configure(bg = "#FFF2CC")
    main(loginWindow)
    loginWindow.mainloop()
