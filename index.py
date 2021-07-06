from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import mysql.connector
from PyQt5.uic import loadUiType

ui, _ = loadUiType('library.ui')


class MainWindow(QMainWindow, ui):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.HandleUi_Changes()
        self.Handle_Buttons()

        # to store searched book id
        self.searched_book_id = None

        # To check if logedin for editing information
        self.login_status = False

        # To show data in table widgets in settings tab
        self.Show_Categories()
        self.Show_Authors()
        self.Show_Publishers()

        # To show data in comboboxes in Add new book tab
        self.Show_Category_Combobox()
        self.Show_Author_Combobox()
        self.Show_Publisher_Combobox()


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
        self.book_pushButto.clicked.connect(self.Open_Books_Tab)
        self.user_pushButton.clicked.connect(self.Open_Users_Tab)
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

        # Settings tab buttons to add categories, authors, publisehrs
        self.Add_New_Category_pushButton.clicked.connect(self.Add_Category)
        self.Add_New_Author_pushButton.clicked.connect(self.Add_Author)
        self.Add_New_Publisher_pushButton.clicked.connect(self.Add_Publisher)

        # Themes Buttons
        self.QDark_Theme_pushButton.clicked.connect(self.QDark_Theme)
        self.Dark_Orange_Theme_pushButton.clicked.connect(self.Dark_Orange_Theme)
        self.Dark_Blue_Theme_pushButton.clicked.connect(self.Dark_Blue_Theme)
        self.Dark_Grey_Theme_pushButton.clicked.connect(self.Dark_Grey_Theme)


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


    def Open_Settings_Tab(self):
        self.main_tabWidget.setCurrentIndex(3)
        self.Settings_tabWidget.setCurrentIndex(0)


    #####################################################
    ################## Books ############################


    def Add_New_Book(self):

        # Connecting to database
        self.db_con = mysql.connector.connect(user='root', password='2894', host='localhost', database='library')
        self.cur = self.db_con.cursor()

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
        ,(book_title, book_description, book_code, category+1, author+1, publisher+1,book_price))

        # Commiting the changes to the database
        self.db_con.commit()
        self.statusBar().showMessage("New Book Added")

        # Closing the Database Connection.
        self.db_con.close()
        self.cur.close()

        # Resetting the add new book filling boxes.
        self.book_title_lineEdit.setText('')
        self.Book_Description_textEdit.setPlainText('')
        self.book_code_lineEdit.setText('')
        self.category_comboBox.setCurrentIndex(0)
        self.Author_comboBox.setCurrentIndex(0)
        self.Publisher_comboBox.setCurrentIndex(0)
        self.book_price_lineEdit.setText('')


    def Search_Book(self):

        # Get user entered book title to search
        book_title = self.Search_Book_title_lineEdit.text()

        # Connecting to the database
        self.db_con = mysql.connector.connect(user = "root", password = "2894", host = "localhost", database = "library")
        self.cur = self.db_con.cursor()

        # Retrieving the book information from the database
        self.cur.execute(
            ''' select * from book WHERE book_name = %s''',(book_title,)
        )
        data = self.cur.fetchall()

        print(data)
        self.searched_book_id = data[0][0]

        # Displaying Retrieved Book data in the tab
        self.Edit_Book_Title_lineEdit.setText(str(data[0][1]))
        self.Edit_Book_Description_plainTextEdit.setPlainText(str(data[0][2]))
        self.Edit_Book_Code_lineEdit.setText(str(data[0][3]))
        self.Edit_book_category_comboBox.setCurrentIndex(data[0][4]-1)
        self.Edit_Book_Author_comboBox.setCurrentIndex(data[0][5]-1)
        self.Edit_Book_Publisher_comboBox.setCurrentIndex(data[0][6]-1)
        self.Edit_Book_Price_lineEdit.setText(str(data[0][7]))

        # Set the book title line edit to empty
        #self.Search_Book_title_lineEdit.setText('')

        # Closing the Database Connection.
        self.db_con.close()
        self.cur.close()

    def Edit_Book(self):

        # Connecting to the database
        self.db_con = mysql.connector.connect(user="root", password="2894", host="localhost", database="library")
        self.cur = self.db_con.cursor()

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
        , (book_title,description, book_code, category+1, author+1, publisher+1, price, id))

        # Commit changes to the database
        self.db_con.commit()
        self.statusBar().showMessage("Book Information Saved")

        # Closing the Database Connection.
        self.db_con.close()
        self.cur.close()

        # Clearing Book data in the tab
        self.Edit_Book_Title_lineEdit.setText('')
        self.Edit_Book_Description_plainTextEdit.setPlainText('')
        self.Edit_Book_Code_lineEdit.setText('')
        self.Edit_book_category_comboBox.setCurrentIndex(0)
        self.Edit_Book_Author_comboBox.setCurrentIndex(0)
        self.Edit_Book_Publisher_comboBox.setCurrentIndex(0)
        self.Edit_Book_Price_lineEdit.setText('')

    def Delete_Book(self):

        messageBox = QMessageBox.warning(
            self.tabWidget_2,
            "Waning!",
            "Do you want to delete this book?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            # Connecting to the database
            self.db_con = mysql.connector.connect(user="root", password="2894", host="localhost", database="library")
            self.cur = self.db_con.cursor()

            id = self.searched_book_id

            # Deleting the row matching the id of searched book
            self.cur.execute(
                '''DELETE FROM book WHERE id = %s''', (id,))

            # Commit changes to the database
            self.db_con.commit()
            self.statusBar().showMessage("Book Deleted Successfully")

            # Closing the Database Connection.
            self.db_con.close()
            self.cur.close()

        # Clearing Book data in the tab
        self.Edit_Book_Title_lineEdit.setText('')
        self.Edit_Book_Description_plainTextEdit.setPlainText('')
        self.Edit_Book_Code_lineEdit.setText('')
        self.Edit_book_category_comboBox.setCurrentIndex(0)
        self.Edit_Book_Author_comboBox.setCurrentIndex(0)
        self.Edit_Book_Publisher_comboBox.setCurrentIndex(0)
        self.Edit_Book_Price_lineEdit.setText('')


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

            # Connecting to the database
            self.db_con = mysql.connector.connect(user="root", password="2894", host="localhost", database="library")
            self.cur = self.db_con.cursor()

            # Adding the user to the User table in Database
            self.cur.execute('''
            INSERT INTO user 
            (user_name, user_email, user_password)
            VALUES (%s, %s, %s)''', (user_name,email, password))

            # Commit changes to the database
            self.db_con.commit()
            self.statusBar().showMessage("User Added Successfully")

            # Closing the Database Connection.
            self.db_con.close()
            self.cur.close()

            # Clearing the fields
            self.Add_Username_lineEdit.setText('')
            self.Add_Email_lineEdit.setText('')
            self.Add_Password_lineEdit.setText('')
            self.Add_Confirm_Password_lineEdit.setText('')

    def Edit_User_Login(self):

        # Connecting to the database
        self.db_con = mysql.connector.connect(user="root", password="2894", host="localhost", database="library")
        self.cur = self.db_con.cursor()

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
        print("running")

        # Closing the Database Connection.
        self.db_con.close()
        self.cur.close()

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
                # Connecting to the database
                self.db_con = mysql.connector.connect(user="root", password="2894", host="localhost", database="library")
                self.cur = self.db_con.cursor()

                self.cur.execute(
                    '''UPDATE user 
                    SET user_name = %s, user_email = %s, user_password = %s
                    WHERE user_name = %s''', (new_username,new_email,new_pass, login_username))

                # Commit Changes to table in the database
                self.db_con.commit()
                self.statusBar().showMessage("User Information Saved Successfully")

                # Closing the Database Connection.
                self.db_con.close()
                self.cur.close()

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
    ################## Settings #########################


    def Add_Category(self):

        # Connecting to the database
        self.db_con = mysql.connector.connect(user = "root", password="2894", host = "localhost", database="library")
        self.cur = self.db_con.cursor()

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

        # Closing the Database Connection.
        self.db_con.close()
        self.cur.close()

        # Clear the Entered text from line edit
        self.New_Category_lineEdit.setText("")

        # Display new Content in categories table
        self.Show_Categories()
        self.Show_Category_Combobox()


    def Show_Categories(self):

        # Connecting to Database
        self.db_con = mysql.connector.connect(user = "root", password = "2894", host = "localhost", database = "library")
        self.cur = self.db_con.cursor()

        # getting the all book categories from table category
        self.cur.execute("""SELECT * FROM category""")
        data = self.cur.fetchall()

        # Inserting data into the Categories Table
        if data:
            self.Categories_tableWidget.setRowCount(0)
            for row, form in enumerate(data):
                self.Categories_tableWidget.insertRow(row)
                for col, item in enumerate(form):
                    self.Categories_tableWidget.setItem(row,col,QTableWidgetItem(str(item)))


        self.db_con.close()
        self.cur.close()


    def Add_Author(self):

        # Connecting to the database
        self.db_con = mysql.connector.connect(user="root", password="2894", host="localhost", database="library")
        self.cur = self.db_con.cursor()

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

        # Closing the Database Connection.
        self.db_con.close()
        self.cur.close()

        # Clear the Entered text from line edit
        self.New_Author_lineEdit.setText("")

        # Display new Content in categories table
        self.Show_Authors()
        self.Show_Author_Combobox()


    def Show_Authors(self):

        # Connecting to Database
        self.db_con = mysql.connector.connect(user="root", password="2894", host="localhost", database="library")
        self.cur = self.db_con.cursor()

        # getting the all book categories from table category
        self.cur.execute("""SELECT * FROM author""")
        data = self.cur.fetchall()

        # Inserting data into the Categories Table
        if data:
            self.Authors_tableWidget.setRowCount(0)
            for row, form in enumerate(data):
                self.Authors_tableWidget.insertRow(row)
                for col, item in enumerate(form):
                    self.Authors_tableWidget.setItem(row, col, QTableWidgetItem(str(item)))

        self.db_con.close()
        self.cur.close()


    def Add_Publisher(self):

        # Connecting to the database
        self.db_con = mysql.connector.connect(user="root", password="2894", host="localhost", database="library")
        self.cur = self.db_con.cursor()

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

        # Closing the Database Connection.
        self.db_con.close()
        self.cur.close()

        # Clear the Entered text from line edit
        self.New_Publisher_lineEdit.setText("")

        # Display new Content in categories table
        self.Show_Publishers()
        self.Show_Publisher_Combobox()


    def Show_Publishers(self):

        # Connecting to Database
        self.db_con = mysql.connector.connect(user="root", password="2894", host="localhost", database="library")
        self.cur = self.db_con.cursor()

        # getting the all book categories from table category
        self.cur.execute("""SELECT * FROM publisher""")
        data = self.cur.fetchall()

        # Inserting data into the Categories Table
        if data:
            self.Publisher_tableWidget.setRowCount(0)
            for row, form in enumerate(data):
                self.Publisher_tableWidget.insertRow(row)
                for col, item in enumerate(form):
                    self.Publisher_tableWidget.setItem(row, col, QTableWidgetItem(str(item)))

        self.db_con.close()
        self.cur.close()


    #####################################################
    ############## Show settings data in UI #############

    def Show_Category_Combobox(self):

        # Conneting to the database library
        self.db_con = mysql.connector.connect(user = "root", password = "2894", host = "localhost", database = "library")
        self.cur = self.db_con.cursor()

        # Retreiving all the categories data from the database
        self.cur.execute('''SELECT category_name FROM category''')
        data = self.cur.fetchall()

        self.category_comboBox.clear()
        for category in data:
            self.category_comboBox.addItem(str(category[0]))
            self.Edit_book_category_comboBox.addItem(str(category[0]))

        # Closing the connection with database
        self.db_con.close()
        self.cur.close()


    def Show_Author_Combobox(self):

        # Conneting to the database library
        self.db_con = mysql.connector.connect(user="root", password="2894", host="localhost", database="library")
        self.cur = self.db_con.cursor()

        # Retreiving all the categories data from the database
        self.cur.execute('''SELECT author_name FROM author''')
        data = self.cur.fetchall()

        self.Author_comboBox.clear()
        for author in data:
            self.Author_comboBox.addItem(str(author[0]))
            self.Edit_Book_Author_comboBox.addItem(str(author[0]))

        # Closing the connection with database
        self.db_con.close()
        self.cur.close()


    def Show_Publisher_Combobox(self):

        # Conneting to the database library
        self.db_con = mysql.connector.connect(user="root", password="2894", host="localhost", database="library")
        self.cur = self.db_con.cursor()

        # Retreiving all the categories data from the database
        self.cur.execute('''SELECT publisher_name FROM publisher''')
        data = self.cur.fetchall()

        self.Publisher_comboBox.clear()
        for publisher in data:
            self.Publisher_comboBox.addItem(str(publisher[0]))
            self.Edit_Book_Publisher_comboBox.addItem(str(publisher[0]))

        # Closing the connection with database
        self.db_con.close()
        self.cur.close()

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
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()

