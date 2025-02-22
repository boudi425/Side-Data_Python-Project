import re
import sqlite3
import pandas as pd
import sys
import os
import random
import datetime
import json
from Side_Funcitons import Strong_passkey

#This project will feature simple ideas like data management, analyzing and manipulation, Also feature some good functionally and security 
#It will be an app with login, Sign up and logout (Not GUI unfortunately But i will try to give it a try)
#As simple as this might look it will need work and time and management
#But as Abdo hassan it will be more than easy to me , Good Luck!
#Going to have two databases i think , One for users and one for articles which i think we will connect
# or join together by some functions in SQL

#This is a simple code that take the query out of the file and execute all of it
con = sqlite3.connect("Blog_Project_Database.db")
Cur = con.cursor()
with open("Data.sql", "r", encoding="utf-8") as Table_Query:
    Query = Table_Query.read()
Cur.executescript(Query)
#-------------------------------------------------------------------------------------------

#Class Sign up contains the following:- (Get_Name, Get_Password, Get_Passkey_Type(For data purposes) and Get_Passkey)
#The function name is enough to know what it does, But just a point , If you are wondering why there is no "Get_ID"
#It's because in the SQL query the ID is AutoIncrement
#And It has it's own "insert data" function
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
        result = Cur.execute("SELECT Name FROM Users_Data").fetchall()
        Names = {row[0] for row in result}
        return Names
    def get_Name(self):
        print("Enter your Name (Max:30 Characters): ")
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
        Passkeys = []
        for i in range(3):
            new_passkey = Strong_passkey(8)
            Passkeys.append(new_passkey)
        return Passkeys
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
            if Passkey_Type == "Password":
                self.passkey = self.Password
            elif Passkey_Type == "Passkey":
                self.passkey = self.Generate_Passkey()
                self.passkey = json.dumps(self.passkey)
                print(f"This is your passkey: {self.passkey}")
                with open("Passkeys.txt", "w") as Passkey_Writer:
                    Passkey_Writer.writelines(self.passkey)
            elif Passkey_Type == "Email":
                email = input("Enter your Email: ")
                self.passkey = email
            else:
                print("Invalid Input, Please try again")
            Dic = {"Passkey_Type": Passkey_Type, "Passkey": self.passkey}
            return Dic
    def insertData(self, Name, Password, Passkey_Type, Passkey):
        Cur.execute("INSERT INTO Users_Data(Name, Password, Passkey_Choice, Passkey) VALUES(?, ?, ?, ?)", (Name, Password, Passkey_Type, Passkey))
        con.commit()
    #The Sign up Class/Functions is Done!!!!
#------------------------------------------------------------------------------------------------------------------
#The login Class doesn't differ a lot from the Sign up Class
#The only Thing which is different which is quite obvious , That the Login class only contains two functions
#Which are (Get_Access, Login_User_Data_Manipulation)
#Why?, Because you need Access to Login first, Why?, Because if there is no data, How are going to login??
#So i made this function to deal with this, The Login_User_Data_Manipulation is a big Function that analyze The given data
#And Compare it to the current data , To Make Sure that the user get it's data and none other
#I am not going to dive in and say what the function do , Because it's pretty simple and clear
class Login:
    def __init__(self):
        self.Name = ''
        self.Password = ''
    def Get_Access(self):
        Names = Cur.execute("SELECT Name FROM Users_Data").fetchone()
        if Names is None:
            print("Can't Login Because there is no users in the database")
            return False
        return True
    def Login_User_Data_Manipulation(self):
        User_Data_Login = []
        print("Login Slide")
        print("Enter your Name: ")
        while True:
            Login_Name = input("> ")
            Login_Names = Cur.execute("SELECT Name FROM Users_Data").fetchall()
            Names = [row[0] for row in Login_Names]    
            if Login_Name.capitalize() not in Names:
                print(f"{Login_Name} isn't Available in the database")
            try:
                User_Data_Login += Cur.execute("SELECT * FROM Users_Data WHERE Name = ?", (Login_Name.capitalize(),)).fetchone()
            except TypeError:
                print("Try to Enter A Name Again")
                continue
            if Login_Name.capitalize() in Names:
                print(f"Welcome Back {Login_Name.capitalize()}")
                print("Enter your Password: ")
                while True:
                    Login_Password = input("> ")
                    if User_Data_Login[2] == Login_Password:
                        print("Correct!, Now let's check the F2A")
                        break
                    else:
                        print("Wrong Password, Please try again")
            else: 
                print("Wrong Input, Please try again")
            while True:
                print(f"Enter your Passkey (Your Passkey_Type: ({User_Data_Login[3]}): ")
                if User_Data_Login[3] == "Password":
                    print("Access granted")
                    break
                elif User_Data_Login[3] == "Passkey":
                    print("Enter your Passkey: ")
                    while True:
                        Login_Passkey = input("> ")
                        if Login_Passkey in json.loads(User_Data_Login[4]):
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
            break
        ID = Cur.execute("SELECT ID FROM Users_Data WHERE Name = ?", (Login_Name,)).fetchone()
        Dic = {"Access": True, "ID": ID, "Name": Login_Name}
        return Dic
            # I should Kys
            # I Hate Data Manipulation 
            #0 Id , 1 Name , 2 Password , 3 Passkey_Choice, 4 Passkey
    #Login Class/Functions are DONE!!!!
#--------------------------------------------------------------------------------------------------------------------------------
#Actually I forget that this class even exist, Because it took me no time to program it honestly
#Which Tell you , How easy this class is, It's like the Sign up Class but with (Get_Title, Get_Body, Get_Today_Date)
#Quite simple and nothing more , The function speaks for itself, BUt just for your point , The Get_Body Function is build to keep the user
#In the control of the article which he can stop at any time or delete or continue or anything , he wants to do with it
#This class has it's own insert_Data.... :-D
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
        Today_date = datetime.datetime.now().date()
        return Today_date
    def Insert_Data(self, Title, Body, Date, UserID):
        Cur.execute("""INSERT INTO Articles_Data(User_ID, Article_Name, Article_Body, Article_Date) VALUES(?, ?, ?, ?)""", (UserID, Title, Body, Date))
        con.commit()
    #Post Class/Functions are DONE!!!!!
Name = None
User_ID = None 
#------------------------------------------------------------------------
#The System class!, Might be the biggest one of them
#Three classes in one class, Combing to Produce the well build program and more
#The system is just like the motor, Which make the car active in everything
#The system has some of the function which i love to call : Acting_Functions,
#Which is basically A function that contains the other function of the class, It's just like a box
#Functions like (SignUp_Start, Login_Start and System_Start) is all Acting_Functions
#But See_Posts, See_Your_Posts and Search_Engine are not Acting_Functions
#They are Real Functions , That uses the power of SQL Join Method to merge two databases
#What about the Search_Engine Function?, It uses the power of SQL to search in data even if the input itself isn't complete
#Show_Selected_Post and Generate_Article_Design It's like a duo , The first one gets the data And the second one Organize it to make it readable
class System:
    #Don't Forget to define the Foreign Key Id in a variable itself!!!!
    #Don't Forget also this will carry all the Classes ,We are combining all the classes
    #In this class to get the well built and Strong System!!!   
    def __init__(self):
        self.Sign_Up_System = Sign_up()
        self.Login_System = Login()
        self.Posting = Post()
    def signUp_Start(self):
        Sign_Name = self.Sign_Up_System.get_Name()
        Name = Sign_Name
        Password = self.Sign_Up_System.Get_Password()
        Passkey = self.Sign_Up_System.Get_Passkey()
        self.Sign_Up_System.insertData(Sign_Name, Password, Passkey["Passkey_Type"], Passkey["Passkey"])
        print("Sign up successful, Now you can login")
        result = Cur.execute("SELECT * FROM Users_Data WHERE Name = ?", (Name,)).fetchone()
        Dic = {"ID": result[0], "Name": result[1], "Password": result[2], "Passkey_choice": result[3], "Passkey": result[4]}
        self.Login_Start()
        return Dic["ID"]
    def Login_Start(self):
        Access = self.Login_System.Get_Access()
        if Access:
            Access_To_System = self.Login_System.Login_User_Data_Manipulation()
            Dic = {"Access": Access_To_System[0], "ID": Access_To_System[1]}
            if Dic["Access"]:
                input("Press Enter to continue")
        else:
            print("try to sign up first")
            self.signUp_Start()
        return Dic["ID"]
    def Start_System(self):
        print("Choose from the following: ")
        print("1. Sign up")
        print("2. Login")
        print("3. Quit")
        while True:
            user_choice = input("> ")
            if user_choice.capitalize() == "Sign up" or user_choice == "1":
                User_ID = self.signUp_Start()
                break
            elif user_choice.capitalize() == "Login" or user_choice == "2":
                User_ID = self.Login_Start()
                break
            elif user_choice.capitalize() == "Quit" or user_choice == "3":
                print("Thanks for using our app <3")
                sys.exit()
            else:
                print("PLease enter a correct input")
                continue
        print("""Hello and Welcome, Thanks for login in
        Now you are in the posting side where you can post or see other people posts
        You can also see your own posts if you want to or Make one, And don't worry
        Articles and Data is all saved , if want to Log out Just Type (Quit)""")
        input("Press Enter to continue......")
        while True:
                print("1. Post")
                print("2. See Posts")
                print("3. See Your Posts")
                print("4. Search")        
                print("5. Logout or Quit")
                Choice = input("> ")
                Choice.capitalize()
                if Choice == "1" or Choice.capitalize() == "Post":
                    Article_Title = self.Posting.Get_Title()
                    Article_Content = self.Posting.Get_Body()
                    Article_Date = self.Posting.Get_Today_Date()
                    if isinstance(User_ID, tuple):
                        User_ID = User_ID[0]
                    self.Posting.Insert_Data(Article_Title ,Article_Content , Article_Date, User_ID)
                    print("Article Saved Successfully!")
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
        if isinstance(User_ID, tuple):
            User_ID = User_ID[0]
        UserName_Articles = Cur.execute("SELECT Article_Name ,Article_Body ,Article_Date FROM Articles_Data WHERE User_ID = ?",(User_ID,)).fetchall()
        Dic = {"Name": UserName_Articles[0], "Content": UserName_Articles[1], "Date": UserName_Articles[2]}
        return self.Generate_Article_Design(Dic["Name"], Dic["Content"], Dic["Date"])
    def Show_Selected_Post_Int(self, Choice):
        Articles = Cur.execute("""SELECT u.Name , a.Article_Name, a.Article_Body,
                                a.Article_Date FROM Users_Data AS u JOIN Articles_Data AS a
                                ON u.ID = a.User_ID;""").fetchall()
        Article_Chosen = Articles[1][Choice]
        Article_User_Name = Cur.execute("SELECT Article_Name, Article_Body, Article_Date FROM Articles_Data WHERE Article_Name = ?", (Article_Chosen,))
        Article_Dic = {"ID": Article_User_Name[0] ,"Name": Article_User_Name[1], "Body": Article_User_Name[2], "Date": Article_User_Name[3]}
        return self.Generate_Article_Design(Article_Dic["Name"], Article_Dic["Body"], Article_Dic["Date"], Article_Dic["ID"])
    def Show_Selected_Post(self, Choice):
        Articles = Cur.execute("""SELECT u.Name , a.Article_Name, a.Article_Body,
                                a.Article_Date FROM Users_Data AS u JOIN Articles_Data AS a
                                ON u.ID = a.User_ID;""").fetchall()
        Article_Chosen = Articles[1].index(Choice)
        Article_User_Name = Cur.execute("SELECT User_ID ,Article_Name, Article_Body, Article_Date FROM Articles_Data WHERE Article_Name = ?", (Article_Chosen,))
        Article_Dic = {"ID": Article_User_Name[0] ,"Name": Article_User_Name[1], "Body": Article_User_Name[2], "Date": Article_User_Name[3]}
        return self.Generate_Article_Design(Article_Dic["Name"], Article_Dic["Body"], Article_Dic["Date"], Article_Dic["ID"])
    def Search_Engine(self, algo):
        pass
    def Generate_Article_Design(self, Name, Content, Date, Author):
        print(f"\t {Name}")
        print(f"\t {Content}")
        print(f"\t {Date} --- By {Author}")
        
Test = System()
Test.Start_System()
