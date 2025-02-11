import re
import sqlite3
import pandas as pd
import sys
import os
import random
import datetime
import pandas as pd

#This project will feature simple ideas like data management, analyzing and manipulation, Also feature some good functionally and security 
#It will be an app with login, Sign up and logout (Not GUI unfortunately But i will try to give it a try)
#As simple as this might look it will need work and time and management
#But as Abdo hassan it will be more than easy to me , Good Luck!
#Going to have two databases i think , One for users and one for articles which i think we will connect
# or join together by some functions in SQL
con = sqlite3.connect("Data.db")
Cur = con.cursor()
with open("Data.sql", "r") as Table_Query:
    Query = Table_Query.readlines()
Cur.execute(Query)
class Sign_up:
    print("""Hello and Welcome to my side project app,
    Probely wondering what is this app about, it is about testing my knowledge
    and also to post articles and share them with the world, I hope you enjoy it
    Don't hesitate to give us feedback and suggestions""")
    input("Press Enter to continue......")
    def __init__(self):
        self.Name = ''
        self.Password = ''
        self.passkey = ''
    def Get_All_Names(self):
        result = Cur.execute("SELECT Name FROM Users_Data")
        Names = result.fetchall()
        return Names
    def get_Name(self):
        print("Enter your Name (Max:30 Characters): ")
        self.Name = input("> ")
        Names = self.Get_All_Names()
        while True:
            self.Name = input("> ")
            if self.Name.capitalize() in Names:
                print(f"The name {self.Name} is already taken, Try something else..!")
            elif len(self.Name) > 30:
                print("Name is too long, Please try again")
            else:
                break
        return self.Name.capitalize()
    def Get_Password(self):
        print("Enter your Password (Least:8): ")
        self.Password = input("> ")
        while True:
            if len(self.Password) < 8:
                print("Password is too short, Please try again")
            else:
                break
        return self.Password
    def Generate_Passkey(self):
        pass
    def Get_Passkey_Type(self):
        print("Choose your Passkey way(For additional security): ")
        print("Password will not need anything expect your name and password")
        print("Passkey will be additional on the name and password, you will get the passkey if you choose it")
        print("Email, In the email we will send you a verification code that you will need to enter")
        print("1. Password")
        print("2. Passkey")
        print("3. Email")
        while True:
            choice = input("> ")
            if choice == "1" or choice.capitalize() == "Password":
                choice = "Password"
                return choice
            elif choice == "2" or choice.capitalize() == "Passkey":
                choice = "Passkey"
                return choice
            elif choice == "3" or choice.capitalize() == "Email":
                choice = "Email"
                return choice
            else:
                print("Wrong Input, Please try again")
    def Get_Passkey(self):
        Passkey_Type = self.Get_Passkey_Type()
        while True:
            self.passkey = input("> ")
            if Passkey_Type == "1" or Passkey_Type == "Password":
                self.passkey = self.Password
            elif Passkey_Type == "2" or Passkey_Type == "Passkey":
                self.passkey = self.Generate_Passkey()
                print(f"This is your passkey: {self.passkey}")
            elif Passkey_Type == "3" or Passkey_Type == "Email":
                email = input("Enter your Email: ")
                self.passkey = email
            else:
                print("Invalid Input, Please try again")
            return self.passkey
    def insertData(self, Name, Password, Passkey_Type, Passkey):
        Cur.execute("INSERT INTO Users_Data VALUES(?, ?, ?, ?)", (Name, Password, Passkey_Type, Passkey))
        con.commit()
    #The Sign up Class/Functions is Done!!!!
class Login:
    def __init__(self):
        self.Name = ''
        self.Password = ''
    def Get_Access(self):
        Names = Cur.execute("SELECT Name FROM Users_Data")
        if Names is None:
            print("Can't Login Because there is no users in the database")
            return False
        return True
    def Login_User_Data_Manipulation(self):
        User_Data_Login = []
        print("Login Slide")
        print("Enter your Name: ")
        Login_Name = input("> ")
        Names = Cur.execute("SELECT Name FROM Users_Data")
        if Login_Name.capitalize() not in Names:
            print(f"{Login_Name} isn't Available in the database")
        elif Login_Name.capitalize() in Names:
            User_Data_Login += Cur.execute("SELECT * FROM Users_Data WHERE Name = ?", (Login_Name.capitalize(),)).fetchall()
            print(f"Welcome Back {Login_Name.capitalize()}")
            print("Enter your Password: ")
            while True:
                Login_Password = input("> ")
                if User_Data_Login[2] == Login_Password:
                    print("Correct!, Now let's check the F2A")
                else:
                    print("Wrong Password, Please try again")
        else: 
            print("Wrong Input, Please try again")
        while True:
            print(f"Enter your Passkey (Your Passkey_Type{User_Data_Login[3]}): ")
            if User_Data_Login[3] == "Password":
                print("Access granted")
                break
            elif User_Data_Login[3] == "Passkey":
                print("Enter your Passkey: ")
                while True:
                    Login_Passkey = input("> ")
                    if Login_Passkey in User_Data_Login[4]:
                        print("Access Granted")
                        break
                    else:
                        print("Wrong Passkey, Please check your passkey file")
            elif User_Data_Login[3] == "Email":
                print("Enter your Email: ")
                while True:
                    Login_Email = input("> ")
                    if Login_Email in User_Data_Login[4]:
                        print("Access Granted")
                        break
                    else:
                        print("Wrong Email, Please check your Email")
            else:
                print("What in the world is this?")
        return True
            # I should Kys
            # I Hate Data Manipulation 
            #0 Id , 1 Name , 2 Password , 3 Passkey_Choice, 4 Passkey
    #Login Class/Functions are DONE!!!!
class Post:
    def __init__(self):
        self.Title = ''
        self.Body = ''
        self.Date = ''

    def Get_Title(self):
        print("Enter Your Title: ")
        while True:
            self.Title = input("> ")
            if len(self.Title) > 30:
                print("Title is too long, Please try again")
            else:
                return self.Title
    def Get_Body(self):
        print("Here You can start Writing Your Post: ")
        input("Press Enter to start Writing...")
        print("Enter Your Post: ")
        Post = input("> ")
        print("Are you sure you want to post this?")
        Choice = input("Yes or No: ")
        if Choice.capitalize() == "Yes":
            return Post
        elif Choice.capitalize() == "No":
            print("Continue Writing? (Yes, No): ")
            while True:
                response = input("> ")
                if response.capitalize() == "Yes":
                    input("Press Enter To continue Writing.....")
                    print("Press Enter when Finished")
                    input(Post )
                    return Post
                elif response.capitalize() == "No":
                    break
                else:
                    print("Please Enter Yes or No")
        elif Choice.capitalize() == "Quit":
            print("Thanks for using my app")
            sys.exit()
        else:
            print("Please Enter Yes or No (For Quit Type 'Quit'")
    def Get_Today_Date(self):
        Today_date = datetime.datetime.now().date
        return Today_date
    def Insert_Data(self, Title, Body, Date, UserID):
        Cur.execute("""INSERT INTO Articles_Data(User_ID, Name_Of_Article, Body_Of_Article, Date_Of_Article) VALUES(?, ?, ?, ?)""", (UserID, Title, Body, Date))
        con.commit()
    #Post Class/Functions are DONE!!!!!
Name = None
class System:
    #Don't Forget to define the Foreign Key Id in a variable itself!!!!
    #Don't Forget also this will carry all the Classes ,We are combining all the classes
    #In this class to get the well built and Strong System!!!   
    def __init__(self):
        self.Sign_Up = Sign_up()
        self.Login = Login()
        self.Posting = Post()
    def signUp_Start(self):
        Sign_Name = self.Sign_up.get_Name
        Name = Sign_Name
        ID = Cur.execute("SELECT ID FROM Users_Data WHERE Name = ?", (Name,))
        Password = self.Sign_up.Get_Password()
        Passkey_Type = self.Sign_up.Get_Passkey_Type()
        Passkey = self.Sign_up.Get_Passkey()
        self.Sign_up.insertData(Sign_Name, Password, Passkey_Type, Passkey)
        print("Sign up successful, Now you can login")
        self.Login_Start()
        return ID
    def Login_Start(self):
        Access = self.Login.Get_Access()
        if Access:
            Access_To_System = self.Login.Login_User_Data_Manipulation()
            if Access_To_System:
                input("Press Enter to continue")
        else:
            print("try to sign up first")
            self.signUp_Start()
    def Start_System(self):
        Id_Start = self.signUp_Start()
        print("""Hello and Welcome, Thanks for login in
        Now you are in the posting side where you can post or see other people posts
        You can also see your own posts if you want to or Make one, And don't worry
        Your Articles and Data is all saved , if want to Log out Just Type (Quit)""")
        input("Press Enter to continue......")
        print("1. Post")
        print("2. See Posts")
        print("3. Search")
        print("4. See Your Posts")        
        print("5. Logout or Quit")
        while True:
            Choice = input("> ")
            Choice.capitalize()
            if Choice == "1" or Choice.capitalize() == "Post":
                Article_Title = self.Posting.Get_Title()
                Article_Content = self.Posting.Get_Body()
                Article_Date = self.Posting.Get_Today_Date()
                self.Posting.Insert_Data(Id_Start ,Article_Title, Article_Content, Article_Date)
            elif Choice == "2" or Choice.capitalize() == "See posts":
                self.See_Posts()
            elif Choice == "3" or Choice.capitalize() == "See your posts":
                self.See_Your_Posts()
            elif Choice == "4" or Choice.capitalize == "Search":
                print("Enter the Post you want to find: ")
                response = input("> ")
                self.Search_Engine(response)
            elif Choice == "5" or Choice.capitalize() == "Logout" or Choice.capitalize() == "Quit":
                print("Thanks for using my app")
                sys.exit()
            else:
                print("Please Enter a Valid Input")
    def See_Posts(self):
        result = Cur.execute("""SELECT u.Name , a.Article_Name, a.Article_Body,
                                a.Article_Date FROM Users_Data AS u JOIN Articles_Data AS a
                                ON u.ID = a.User_ID;""").fetchall()
        Total = 1
        for Num, (Name, Title) in enumerate(result[0:1], start=1):
            print(f"#{Num}. {Title} by {Name}")
            Total += 1
        print(f"{Total}. Quit")
        print("Enter The Name or The Number of the Article to Open it: ")
        response = input("> ")
        if response.isdecimal():
            if int(response) == Total:
                print("Thanks for using my program")
                sys.exit()
            elif int(response) > len(result[1]):
                print("Not a valid option, try again")
            else:
                return self.Show_Selected_Post_Int(int(response))
        elif response.isalpha():
            if response == "Quit":
                print("Thanks for using my program")
                sys.exit()
            elif response not in result[1]:
                print("Enter a valid option, try again")
            else:
                return self.Show_Selected_Post(response)
    def See_Your_Posts(self):
        pass
    def Show_Selected_Post_Int(self, Choice):
        Articles = Cur.execute("""SELECT u.Name , a.Article_Name, a.Article_Body,
                                a.Article_Date FROM Users_Data AS u JOIN Articles_Data AS a
                                ON u.ID = a.User_ID;""").fetchall()
        Article_Chosen = Articles[1][Choice]
        Article_User_Name = Cur.execute("SELECT Article_Name, Article_Body, Article_Date FROM Articles_Data WHERE Article_Name = ?", (Article_Chosen,))
        return Article_User_Name
    def Show_Selected_Post(self, Choice):
        Articles = Cur.execute("""SELECT u.Name , a.Article_Name, a.Article_Body,
                                a.Article_Date FROM Users_Data AS u JOIN Articles_Data AS a
                                ON u.ID = a.User_ID;""").fetchall()
        Article_Chosen = Articles[1].index(Choice)
        Article_User_Name = Cur.execute("SELECT Article_Name, Article_Body, Article_Date FROM Articles_Data WHERE Article_Name = ?", (Article_Chosen,))
        return Article_User_Name
    def Search_Engine(self, algo):
        pass