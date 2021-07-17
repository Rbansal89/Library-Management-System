from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import mysql.connector
import datetime
from xlsxwriter import Workbook

from PyQt5.uic import loadUiType
#from library import Ui_MainWindow
#from login import Ui_Form

ui, _ = loadUiType('library.ui')
login,_ = loadUiType('login.ui')


class Login(QWidget, login):

    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.Message_label.setHidden(True)
        self.login_status = False
        self.Login_pushButton.clicked.connect(self.Handle_Login)


    def Handle_Login(self):
        # Connecting to the database
        self.db_con = mysql.connector.connect(user="root", password="2894", host="localhost", database="library")
        self.cur = self.db_con.cursor()

        username = self.username_lineEdit.text()
        password = self.password_lineEdit.text()

        print(username,password)

        # getting user login info
        self.cur.execute(
            '''SELECT * from user where user_name = %s''', (username,))
        data = self.cur.fetchone()
        print(data)

        if data is not None:
            if data[3] != password:
                print("not login")
            else:
                print("Login")
                self.login_status = True
        else:
            print("wrong")

        print("Done")
        # Closing the Database Connection.
        self.db_con.close()
        self.cur.close()

        if self.login_status:
            self.window2 = MainWindow()
            self.close()
            self.window2.show()
        else:
            self.Message_label.setHidden(False)


class MainWindow(QMainWindow, ui):

    def __init__(self):
        QMainWindow.__init__(self)
        self.db_con = None
        self.cur = None
        # Connect to Database
        self.db_con ,self.cur = self.Connect_To_Database()
        self.setupUi(self)
        self.HandleUi_Changes()
        self.Handle_Buttons()

        # Default theme
        self.Dark_Blue_Theme()

        # to store searched book id
        self.searched_book_id = None

        # To check if logedin for editing information
        self.login_status = False

        # To Show data in day to day operations table
        self.Show_All_Operations()

        # To show data in table widgets in settings tab
        self.Show_Categories()
        self.Show_Authors()
        self.Show_Publishers()

        # To show data in comboboxes in Add new book tab
        self.Show_Category_Combobox()
        self.Show_Author_Combobox()
        self.Show_Publisher_Combobox()

        # To show data in Book table
        self.Show_All_Books()
        # To show data in client table
        self.Show_All_Client()

        print(self.db_con)
        print(self.cur)

    def __del__(self):
        print("calling delete and clsoing database connection!")
        self.db_con.close()
        self.cur.close()

    def HandleUi_Changes(self):
        self.Hiding_Themes()
        self.Open_Day_To_Day_Tab()
        self.main_tabWidget.tabBar().setVisible(False)

    def Handle_Buttons(self):
        # Button to show themes groupbox
        self.theme_pushButton.clicked.connect(self.Show_Themes)
        # Button to hide themes groupbox
        self.themeHide_pushButton.clicked.connect(self.Hiding_Themes)

        # Buttons changing Main Tabs
        self.dayToDay_pushButton.clicked.connect(self.Open_Day_To_Day_Tab)
        self.book_pushButton.clicked.connect(self.Open_Books_Tab)
        self.user_pushButton.clicked.connect(self.Open_Users_Tab)
        self.client_pushButton.clicked.connect(self.Open_Clients_Tab)
        self.setting_pushButton.clicked.connect(self.Open_Settings_Tab)

        # Button to add new book
        self.Add_Book_pushButton.clicked.connect(self.Add_New_Book)

        # Button to search, edit, delete a book
        self.Search_Book_pushButton.clicked.connect(self.Search_Book)
        self.Delete_Book_pushButton.clicked.connect(self.Delete_Book)
        self.Save_Edited_Book_pushButton.clicked.connect(self.Edit_Book)

        # Button to add new user, edit user info
        self.Add_User_pushButton.clicked.connect(self.Add_New_User)
        self.Edit_user_login_pushButton.clicked.connect(self.Edit_User_Login)
        self.Save_User_Info_pushButton.clicked.connect(self.Edit_User_Info)
        self.Delete_Client_pushButton.clicked.connect(self.Delete_Client)

        # Button to add new client, edit and delete client info
        self.Add_Client_pushButton.clicked.connect(self.Add_New_Client)
        self.Search_Client_pushButton.clicked.connect(self.Search_Client)
        self.Save_Edited_Client_pushButton.clicked.connect(self.Save_Edit_Client_Info)

        # Settings tab buttons to add categories, authors, publisehrs
        self.Add_New_Category_pushButton.clicked.connect(self.Add_Category)
        self.Add_New_Author_pushButton.clicked.connect(self.Add_Author)
        self.Add_New_Publisher_pushButton.clicked.connect(self.Add_Publisher)

        # Button to Export Data
        self.Export_day_operations_pushButton.clicked.connect(self.Export_Day_Operations)
        self.Export_Books_pushButton.clicked.connect(self.Export_Books)
        self.Export_Clients_pushButton.clicked.connect(self.Export_Clients)

        # Themes Buttons
        self.QDark_Theme_pushButton.clicked.connect(self.QDark_Theme)
        self.Dark_Orange_Theme_pushButton.clicked.connect(self.Dark_Orange_Theme)
        self.Dark_Blue_Theme_pushButton.clicked.connect(self.Dark_Blue_Theme)
        self.Dark_Grey_Theme_pushButton.clicked.connect(self.Dark_Grey_Theme)

        # Add New Book
        self.Add_New_Operations_pushButton.clicked.connect(self.Handle_Day_Operations)

    # Function to Connect with Database
    def Connect_To_Database(self):
        try:
            self.db_con = mysql.connector.connect(user='root', password='2894', host='localhost', database='library')
            self.cur = self.db_con.cursor()
            print("Connection Successful!")
            return (self.db_con, self.cur)
        except:
            self.db_con = None
            self.cur = None
            print("Except running")
            return (None, None)


    def Show_Themes(self):
        self.theme_groupBox.show()


    def Hiding_Themes(self):
        self.theme_groupBox.hide()

    #####################################################
    ########### Openign Tabs ############################

    def Open_Day_To_Day_Tab(self):
        self.main_tabWidget.setCurrentIndex(0)


    def Open_Books_Tab(self):
        self.main_tabWidget.setCurrentIndex(1)
        self.Books_tabWidget.setCurrentIndex(0)


    def Open_Users_Tab(self):
        self.main_tabWidget.setCurrentIndex(2)


    def Open_Clients_Tab(self):
        self.main_tabWidget.setCurrentIndex(3)
        self.Clients_tabWidget.setCurrentIndex(0)


    def Open_Settings_Tab(self):
        self.main_tabWidget.setCurrentIndex(4)
        self.Settings_tabWidget.setCurrentIndex(0)


    #####################################################
    ############# Day to Day Operations #################

    def Show_All_Operations(self):

        if not self.db_con:
            # Connecting to database
            self.db_con, self.cur = self.Connect_To_Database()

        # Getting data from the database
        self.cur.execute(
            '''SELECT * FROM dayoperations'''
        )

        data = self.cur.fetchall()

        if data is not None:
            self.Day_Operations_tableWidget.setRowCount(0)
            for row, form in enumerate(data):
                self.Day_Operations_tableWidget.insertRow(row)
                for col, item in enumerate(form[1:4]+form[5:]):
                    self.Day_Operations_tableWidget.setItem(row, col, QTableWidgetItem(str(item)))


    def Handle_Day_Operations(self):

        book_title = self.Enter_Book_title_lineEdit.text()
        client_name = self.Enter_Client_Name_lineEdit.text()
        type = self.Type_comboBox.currentText()
        days_number = self.Days_comboBox.currentIndex() + 1
        today_date = datetime.date.today()
        to_date = today_date+ datetime.timedelta(days = days_number)

        if not self.db_con:
            # Connecting to database
            self.db_con. self.cur = self.Connect_To_Database()

        print(book_title, client_name, type, days_number, today_date, to_date)

        # Getting Books data from book table
        self.cur.execute(
            '''INSERT INTO dayoperations
            (book_name, client_name, type, days, from_date, to_date)
            VALUES (%s, %s, %s, %s, %s, %s)''', (book_title, client_name, type, days_number + 1, str(today_date), str(to_date)))

        # Committing changes to the database
        self.db_con.commit()
        self.statusBar().showMessage("New Operation Added")

        # Clearing all fields
        self.Enter_Book_title_lineEdit.setText('')
        self.Enter_Client_Name_lineEdit.setText('')
        self.Type_comboBox.setCurrentIndex(0)
        self.Days_comboBox.setCurrentIndex(0)

        # Updating day to day operations table
        self.Show_All_Operations()

    #####################################################
    ################## Books ############################

    def Show_All_Books(self):

        if not self.db_con:
            # Connecting to database
            self.db_con.self.cur = self.Connect_To_Database()

        # Getting Books data from book table
        self.cur.execute('''SELECT * FROM book''')

        data = self.cur.fetchall()

        if data is not None:
            self.Books_show_tableWidget.setRowCount(0)
            for row, form in enumerate(data):
                self.Books_show_tableWidget.insertRow(row)
                col = 0
                for item in form[1:4]:
                    self.Books_show_tableWidget.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                value1 = self.category_comboBox.itemText(form[4])
                value2 = self.Author_comboBox.itemText(form[5])
                value3 = self.Publisher_comboBox.itemText(form[6])
                self.Books_show_tableWidget.setItem(row,3,QTableWidgetItem(value1) )
                self.Books_show_tableWidget.setItem(row,4,QTableWidgetItem(value2) )
                self.Books_show_tableWidget.setItem(row,5,QTableWidgetItem(value3) )
                self.Books_show_tableWidget.setItem(row,6,QTableWidgetItem(str(form[7])) )


    def Add_New_Book(self):

        if not self.db_con:
            # Connecting to database
            self.db_con.self.cur = self.Connect_To_Database()

        # Getting all the values filled by user
        book_title = self.book_title_lineEdit.text()
        book_description = self.Book_Description_textEdit.toPlainText()
        book_code = self.book_code_lineEdit.text()
        category = self.category_comboBox.currentIndex()
        author = self.Author_comboBox.currentIndex()
        publisher = self.Publisher_comboBox.currentIndex()
        book_price = self.book_price_lineEdit.text()

        # Inserting the data into the table book
        self.cur.execute('''
        INSERT INTO book
        (book_name, book_description, book_code, book_category, book_author,
        book_publisher, book_price)
        VALUES (%s,%s,%s,%s,%s,%s,%s)'''
        ,(book_title, book_description, book_code, category, author, publisher,book_price))

        # Commiting the changes to the database
        self.db_con.commit()
        self.statusBar().showMessage("New Book Added")

        # Resetting the add new book filling boxes.
        self.book_title_lineEdit.setText('')
        self.Book_Description_textEdit.setPlainText('')
        self.book_code_lineEdit.setText('')
        self.category_comboBox.setCurrentIndex(0)
        self.Author_comboBox.setCurrentIndex(0)
        self.Publisher_comboBox.setCurrentIndex(0)
        self.book_price_lineEdit.setText('')

        # Updating book table
        self.Show_All_Books()


    def Search_Book(self):

        # Get user entered book title to search
        book_title = self.Search_Book_title_lineEdit.text()

        if not self.db_con:
            # Connecting to database
            self.db_con. self.cur = self.Connect_To_Database()

        # Retrieving the book information from the database
        self.cur.execute(
            ''' select * from book WHERE book_name = %s''',(book_title,)
        )
        data = self.cur.fetchall()

        # to edit book with this id in database
        self.searched_book_id = data[0][0]

        if data is not None:
            # Displaying Retrieved Book data in the tab
            self.Edit_Book_Title_lineEdit.setText(str(data[0][1]))
            self.Edit_Book_Description_plainTextEdit.setPlainText(str(data[0][2]))
            self.Edit_Book_Code_lineEdit.setText(str(data[0][3]))
            self.Edit_book_category_comboBox.setCurrentIndex(data[0][4])
            self.Edit_Book_Author_comboBox.setCurrentIndex(data[0][5])
            self.Edit_Book_Publisher_comboBox.setCurrentIndex(data[0][6])
            self.Edit_Book_Price_lineEdit.setText(str(data[0][7]))

            # Set the book title line edit to empty
            #self.Search_Book_title_lineEdit.setText('')
        else:
            self.statusBar().showMessage("No Book Found with this Name")


    def Edit_Book(self):

        if not self.db_con:
            # Connecting to database
            self.db_con. self.cur = self.Connect_To_Database()

        # Getting Edited data of the book
        id = self.searched_book_id
        book_title = self.Edit_Book_Title_lineEdit.text()
        description = self.Edit_Book_Description_plainTextEdit.toPlainText()
        book_code = self.Edit_Book_Code_lineEdit.text()
        category = self.Edit_book_category_comboBox.currentIndex()
        author = self.Edit_Book_Author_comboBox.currentIndex()
        publisher = self.Edit_Book_Publisher_comboBox.currentIndex()
        price = self.Edit_Book_Price_lineEdit.text()

        # Updating the book information
        self.cur.execute(
            '''UPDATE book SET book_name = %s, book_description = %s,book_code = %s, book_category = %s,
            book_author = %s, book_publisher = %s, book_price = %s WHERE (id = %s)'''
        , (book_title,description, book_code, category, author, publisher, price, id))

        # Commit changes to the database
        self.db_con.commit()
        self.statusBar().showMessage("Book Information Saved")

        # Clearing Book data in the tab
        self.Search_Book_title_lineEdit.setText('')
        self.Edit_Book_Title_lineEdit.setText('')
        self.Edit_Book_Description_plainTextEdit.setPlainText('')
        self.Edit_Book_Code_lineEdit.setText('')
        self.Edit_book_category_comboBox.setCurrentIndex(0)
        self.Edit_Book_Author_comboBox.setCurrentIndex(0)
        self.Edit_Book_Publisher_comboBox.setCurrentIndex(0)
        self.Edit_Book_Price_lineEdit.setText('')

        # Updating book table
        self.Show_All_Books()


    def Delete_Book(self):

        print("delete running")

        messageBox = QMessageBox.warning(
            self,
            "Waning!",
            "Do you want to delete this book?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            if not self.db_con:
                # Connecting to database
                self.db_con.self.cur = self.Connect_To_Database()

            id = self.searched_book_id

            # Deleting the row matching the id of searched book
            self.cur.execute(
                '''DELETE FROM book WHERE id = %s''', (id,))

            # Commit changes to the database
            self.db_con.commit()
            self.statusBar().showMessage("Book Deleted Successfully")

            # Clearing Book data in the tab
            self.Edit_Book_Title_lineEdit.setText('')
            self.Edit_Book_Description_plainTextEdit.setPlainText('')
            self.Edit_Book_Code_lineEdit.setText('')
            self.Edit_book_category_comboBox.setCurrentIndex(0)
            self.Edit_Book_Author_comboBox.setCurrentIndex(0)
            self.Edit_Book_Publisher_comboBox.setCurrentIndex(0)
            self.Edit_Book_Price_lineEdit.setText('')

        # Updating book table
        self.Show_All_Books()


    #####################################################
    ################## Users ############################

    def Add_New_User(self):

        user_name = self.Add_Username_lineEdit.text()
        email = self.Add_Email_lineEdit.text()
        password = self.Add_Password_lineEdit.text()
        confirm_password = self.Add_Confirm_Password_lineEdit.text()


        if password != confirm_password:
            self.statusBar().showMessage("Password Does Not Match!")
        else:

            if not self.db_con:
                # Connecting to database
                self.db_con.self.cur = self.Connect_To_Database()

            # Adding the user to the User table in Database
            self.cur.execute('''
            INSERT INTO user 
            (user_name, user_email, user_password)
            VALUES (%s, %s, %s)''', (user_name,email, password))

            # Commit changes to the database
            self.db_con.commit()
            self.statusBar().showMessage("User Added Successfully")

            # Clearing the fields
            self.Add_Username_lineEdit.setText('')
            self.Add_Email_lineEdit.setText('')
            self.Add_Password_lineEdit.setText('')
            self.Add_Confirm_Password_lineEdit.setText('')


    def Edit_User_Login(self):

        if not self.db_con:
            # Connecting to database
            self.db_con. self.cur = self.Connect_To_Database()

        User_name = self.login_edit_username_lineEdit.text()
        password = self.login_edit_password_lineEdit.text()

        # getting user login info
        self.cur.execute(
            '''SELECT * from user where user_name = %s''', (User_name,))
        data = self.cur.fetchone()
        print(data)

        if data is not None:
            if data[3] != password:
                self.statusBar().showMessage("Incorrect Password!")
            else:
                self.login_status = True
                self.statusBar().showMessage("Login Successful")
        else:
            self.statusBar().showMessage("Either Username or Password is Incorrect")


    def Edit_User_Info(self):

        if self.login_status:
            login_username = self.login_edit_username_lineEdit.text()
            new_username = self.Edit_Username_lineEdit.text()
            new_email = self.Edit_email_lineEdit.text()
            new_pass = self.Edit_Password_lineEdit.text()
            new_confirm_pass = self.Edit_Confirm_Password_lineEdit.text()

            if new_pass != new_confirm_pass:
                self.statusBar().showMessage("Password Does not Match!")

            else:
                if not self.db_con:
                    # Connecting to database
                    self.db_con.self.cur = self.Connect_To_Database()

                self.cur.execute(
                    '''UPDATE user 
                    SET user_name = %s, user_email = %s, user_password = %s
                    WHERE user_name = %s''', (new_username,new_email,new_pass, login_username))

                # Commit Changes to table in the database
                self.db_con.commit()
                self.statusBar().showMessage("User Information Saved Successfully")

                #Clearing all fields
                self.login_edit_username_lineEdit.setText('')
                self.login_edit_password_lineEdit.setText('')

                self.Edit_Username_lineEdit.setText('')
                self.Edit_email_lineEdit.setText('')
                self.Edit_Password_lineEdit.setText('')
                self.Edit_Confirm_Password_lineEdit.setText('')

        else:
            self.statusBar().showMessage("Please Login To Edit User Information")


    #####################################################
    ################## Clients ############################

    def Show_All_Client(self):

        if not self.db_con:
            # Connecting to database
            self.db_con. self.cur = self.Connect_To_Database()

        # Getting Client data fron client table in database
        self.cur.execute('''SELECT * FROM client''')

        data = self.cur.fetchall()

        if data is not None:
            self.Client_tableWidget.setRowCount(0)
            for row, form in enumerate(data):
                self.Client_tableWidget.insertRow(row)
                for col, item in enumerate(form[1:]):
                    self.Client_tableWidget.setItem(row,col, QTableWidgetItem(str(item)))


    def Add_New_Client(self):

        client_name = self.Add_Client_Name_lineEdit.text()
        client_email = self.Add_Client_email_lineEdit.text()
        client_id = self.Add_Client_id_lineEdit.text()

        if not self.db_con:
            # Connecting to database
            self.db_con. self.cur = self.Connect_To_Database()

        print(client_id,client_email,client_name)

        # Inserting new client row in client table in database
        self.cur.execute(
            '''INSERT INTO client
            (client_name, client_email, client_id)
            VALUES (%s, %s, %s)''',
            (client_name,client_email,client_id))

        # Commiting to the database
        self.db_con.commit()
        self.statusBar().showMessage("Client Added Successfully")
        print("Done")

        self.Add_Client_Name_lineEdit.setText("")
        self.Add_Client_email_lineEdit.setText("")
        self.Add_Client_id_lineEdit.setText("")

        # Updating Client Table Values
        self.Show_All_Client()


    def Search_Client(self):

        client_search_id = self.Search_Client_id_lineEdit.text()

        if not self.db_con:
            # Connecting to database
            self.db_con. self.cur = self.Connect_To_Database()

        # Searching for client in client table in database
        self.cur.execute(
            '''SELECT * from client WHERE client_id = %s''',(client_search_id,))

        data = self.cur.fetchone()

        if data:
            self.Edit_Client_Name_lineEdit.setText(str(data[1]))
            self.Edit_Client_Email_lineEdit.setText(str(data[2]))
            self.Edit_Client_id_lineEdit.setText(str(data[3]))
            self.statusBar().showMessage("Client Found!")
        else:
            self.statusBar().showMessage("Client Not Found!")


    def Save_Edit_Client_Info(self):

        client_name = self.Edit_Client_Name_lineEdit.text()
        client_email = self.Edit_Client_Email_lineEdit.text()
        client_id = self.Edit_Client_id_lineEdit.text()

        client_search_id = self.Search_Client_id_lineEdit.text()

        if not self.db_con:
            # Connecting to database
            self.db_con. self.cur = self.Connect_To_Database()

        # Updating Client Info
        self.cur.execute(
            '''UPDATE client
            SET client_name = %s, client_email = %s, client_id = %s
            WHERE client_id = %s''', (client_name,client_email,client_id,client_search_id))

        # Commit changes to database
        self.db_con.commit()
        self.statusBar().showMessage("Client Data Updated")

        self.Edit_Client_Name_lineEdit.setText('')
        self.Edit_Client_Email_lineEdit.setText('')
        self.Edit_Client_id_lineEdit.setText('')

        #Updating Client table
        self.Show_All_Client()


    def Delete_Client(self):

        client_search_id = self.Search_Client_id_lineEdit.text()

        if client_search_id != "":

            delete_message = QMessageBox.warning(
                self,
                "Warning!",
                "Do you want to Delete this Client?",
                QMessageBox.Yes | QMessageBox.No
            )

            if delete_message == QMessageBox.Yes:
                if not self.db_con:
                    # Connecting to database
                    self.db_con.self.cur = self.Connect_To_Database()

                # Delete Client from client table in database
                self.cur.execute(
                    '''Delete FROM client WHERE client_id = %s''', (client_search_id,))

                # Commiting changes to database
                self.db_con.commit()
                self.statusBar().showMessage("Client Data Deleted")

                # Updating Client Table
                self.Show_All_Client()
            else:
                return
        else:
            self.statusBar().showMessage("Please Enter Correct Client Id!")


    #####################################################
    ################## Settings #########################

    def Add_Category(self):

        if not self.db_con:
            # Connecting to database
            self.db_con. self.cur = self.Connect_To_Database()

        # get the category value filled by user
        category_name = self.New_Category_lineEdit.text()
        # insert category in the table in database
        self.cur.execute(
        '''
        INSERT INTO category (category_name) VALUES (%s)
        ''',(category_name,))

        # Commit to the database
        self.db_con.commit()
        self.statusBar().showMessage("New Category Added")

        # Clear the Entered text from line edit
        self.New_Category_lineEdit.setText("")

        # Display new Content in categories table
        self.Show_Categories()
        self.Show_Category_Combobox()


    def Show_Categories(self):

        if not self.db_con:
            # Connecting to database
            self.db_con. self.cur = self.Connect_To_Database()

        # getting the all book categories from table category
        self.cur.execute("""SELECT * FROM category""")
        data = self.cur.fetchall()

        # Inserting data into the Categories Table
        if data:
            self.Categories_tableWidget.setRowCount(0)
            for row, form in enumerate(data):
                self.Categories_tableWidget.insertRow(row)
                for col, item in enumerate(form[1:]):
                    self.Categories_tableWidget.setItem(row,col,QTableWidgetItem(str(item)))


    def Add_Author(self):

        if not self.db_con:
            # Connecting to database
            self.db_con. self.cur = self.Connect_To_Database()

        # get the category value filled by user
        author_name = self.New_Author_lineEdit.text()
        # insert category in the table in database
        self.cur.execute(
            '''
            INSERT INTO author (author_name) VALUES (%s)
            ''', (author_name,))

        # Commit to the database
        self.db_con.commit()
        self.statusBar().showMessage("New Author Added")

        # Clear the Entered text from line edit
        self.New_Author_lineEdit.setText("")

        # Display new Content in categories table
        self.Show_Authors()
        self.Show_Author_Combobox()


    def Show_Authors(self):

        if not self.db_con:
            # Connecting to database
            self.db_con. self.cur = self.Connect_To_Database()

        # getting the all book categories from table category
        self.cur.execute("""SELECT * FROM author""")
        data = self.cur.fetchall()

        # Inserting data into the Categories Table
        if data:
            self.Authors_tableWidget.setRowCount(0)
            for row, form in enumerate(data):
                self.Authors_tableWidget.insertRow(row)
                for col, item in enumerate(form[1:]):
                    self.Authors_tableWidget.setItem(row, col, QTableWidgetItem(str(item)))


    def Add_Publisher(self):

        if not self.db_con:
            # Connecting to database
            self.db_con. self.cur = self.Connect_To_Database()

        # get the category value filled by user
        publisher_name = self.New_Publisher_lineEdit.text()
        # insert category in the table in database
        self.cur.execute(
            '''
            INSERT INTO publisher (publisher_name) VALUES (%s)
            ''', (publisher_name,))

        # Commit to the database
        self.db_con.commit()
        self.statusBar().showMessage("New Publisher Added")

        # Clear the Entered text from line edit
        self.New_Publisher_lineEdit.setText("")

        # Display new Content in categories table
        self.Show_Publishers()
        self.Show_Publisher_Combobox()


    def Show_Publishers(self):

        if not self.db_con:
            # Connecting to database
            self.db_con. self.cur = self.Connect_To_Database()

        # getting the all book categories from table category
        self.cur.execute("""SELECT * FROM publisher""")
        data = self.cur.fetchall()

        # Inserting data into the Categories Table
        if data:
            self.Publisher_tableWidget.setRowCount(0)
            for row, form in enumerate(data):
                self.Publisher_tableWidget.insertRow(row)
                for col, item in enumerate(form[1:]):
                    self.Publisher_tableWidget.setItem(row, col, QTableWidgetItem(str(item)))


    #####################################################
    ############## Show settings data in UI #############

    def Show_Category_Combobox(self):

        if not self.db_con:
            # Connecting to database
            self.db_con. self.cur = self.Connect_To_Database()

        # Retreiving all the categories data from the database
        self.cur.execute('''SELECT category_name FROM category''')
        data = self.cur.fetchall()

        self.category_comboBox.clear()
        for category in data:
            self.category_comboBox.addItem(str(category[0]))
            self.Edit_book_category_comboBox.addItem(str(category[0]))


    def Show_Author_Combobox(self):

        if not self.db_con:
            # Connecting to database
            self.db_con. self.cur = self.Connect_To_Database()

        # Retreiving all the categories data from the database
        self.cur.execute('''SELECT author_name FROM author''')
        data = self.cur.fetchall()

        self.Author_comboBox.clear()
        for author in data:
            self.Author_comboBox.addItem(str(author[0]))
            self.Edit_Book_Author_comboBox.addItem(str(author[0]))


    def Show_Publisher_Combobox(self):

        if not self.db_con:
            # Connecting to database
            self.db_con. self.cur = self.Connect_To_Database()

        # Retreiving all the categories data from the database
        self.cur.execute('''SELECT publisher_name FROM publisher''')
        data = self.cur.fetchall()

        self.Publisher_comboBox.clear()
        for publisher in data:
            self.Publisher_comboBox.addItem(str(publisher[0]))
            self.Edit_Book_Publisher_comboBox.addItem(str(publisher[0]))


    #####################################################
    ################# Export Data #######################

    def Export_Day_Operations(self):

        if not self.db_con:
            # Connecting to database
            self.db_con. self.cur = self.Connect_To_Database()

        # Retreiving all the categories data from the database
        self.cur.execute('''SELECT * FROM dayoperations''')
        data = self.cur.fetchall()

        with Workbook('Day_operations.xlsx') as wb:

            sheet1 = wb.add_worksheet('Sheet 1')

            # Sheet formatting
            sheet1.set_column(0,5,30)

            # Formatting for Headers
            header_format = wb.add_format({'bold': True, 'align': 'center', 'font_size' : 16})
            data_format = wb.add_format({'font_size' : 14})

            # Adding Headers to sheet
            sheet1.write(0,0, "Book Title", header_format)
            sheet1.write(0,1, "Client Name", header_format)
            sheet1.write(0,2, "Type", header_format)
            sheet1.write(0,3, "Days", header_format)
            sheet1.write(0,4, "From - Date", header_format)
            sheet1.write(0,5, "To - Date", header_format)

            if data is not None:
                for row, form in enumerate(data):
                    for col, item in enumerate(form[1:]):
                        sheet1.write(row+1,col, str(item), data_format)

            self.statusBar().showMessage("File Exported Successfully")


    def Export_Books(self):

        if not self.db_con:
            # Connecting to database
            self.db_con. self.cur = self.Connect_To_Database()

        # Retreiving all the categories data from the database
        self.cur.execute('''SELECT * FROM book''')
        data = self.cur.fetchall()

        with Workbook('Books_data.xlsx') as wb:

            sheet1 = wb.add_worksheet('Sheet 1')

            # Sheet formatting
            sheet1.set_column(0,6,22)

            # Formatting for Headers
            header_format = wb.add_format({'bold': True, 'align': 'center', 'font_size' : 15})
            data_format = wb.add_format({'font_size' : 13})

            # Adding Headers to sheet
            sheet1.write(0,0, "Book Title", header_format)
            sheet1.write(0,1, "Book Description", header_format)
            sheet1.write(0,2, "Book Code", header_format)
            sheet1.write(0,3, "Category", header_format)
            sheet1.write(0,4, "Author", header_format)
            sheet1.write(0,5, "Publisher", header_format)
            sheet1.write(0,6, "Price", header_format)

            if data is not None:
                for row, form in enumerate(data):
                    for col, item in enumerate(form[1:]):
                        sheet1.write(row+1,col, str(item), data_format)

            self.statusBar().showMessage("File Exported Successfully")


    def Export_Clients(self):

        if not self.db_con:
            # Connecting to database
            self.db_con. self.cur = self.Connect_To_Database()

        # Retreiving all the categories data from the database
        self.cur.execute('''SELECT * FROM client''')
        data = self.cur.fetchall()

        with Workbook('Clients_data.xlsx') as wb:

            sheet1 = wb.add_worksheet('Sheet 1')

            # Sheet formatting
            sheet1.set_column(0, 2, 30)

            # Formatting for Headers
            header_format = wb.add_format({'bold': True, 'align': 'center', 'font_size': 16})
            data_format = wb.add_format({'font_size': 14})

            # Adding Headers to sheet
            sheet1.write(0, 0, "Client Name", header_format)
            sheet1.write(0, 1, "Client Email", header_format)
            sheet1.write(0, 2, "Client Id", header_format)

            if data is not None:
                for row, form in enumerate(data):
                    for col, item in enumerate(form[1:]):
                        sheet1.write(row + 1, col, str(item), data_format)

            self.statusBar().showMessage("File Exported Successfully")


    #####################################################
    ################## UI Themes ########################

    def Dark_Blue_Theme(self):
        style = open('themes/darkblue.css','r')
        style = style.read()
        self.setStyleSheet(style)


    def Dark_Grey_Theme(self):
        style = open('themes/darkgrey.css', 'r')
        style = style.read()
        self.setStyleSheet(style)


    def Dark_Orange_Theme(self):
        style = open('themes/darkorange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)


    def QDark_Theme(self):
        style = open('themes/qdark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)


def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()

