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

        self.Show_Categories()
        self.Show_Authors()
        self.Show_Publishers()

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

        self.Add_New_Category_pushButton.clicked.connect(self.Add_Category)
        self.Add_New_Author_pushButton.clicked.connect(self.Add_Author)
        self.Add_New_Publisher_pushButton.clicked.connect(self.Add_Publisher)


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


    def Open_Users_Tab(self):
        self.main_tabWidget.setCurrentIndex(2)


    def Open_Settings_Tab(self):
        self.main_tabWidget.setCurrentIndex(3)


    #####################################################
    ################## Books ############################


    def Add_New_Book(self):

        # Connecting to database
        self.db_con = mysql.connector.connect(user='root', password='2894', host='localhost', database='library')
        self.cur = self.db_con.cursor()

        # Getting all the values filled by user
        book_title = self.book_title_lineEdit.text()
        book_code = self.book_code_lineEdit.text()
        category = self.category_comboBox.CurentText()
        author = self.Author_comboBox.CurentText()
        publisher = self.Publisher_comboBox.CurentText()
        book_price = self.book_price_lineEdit.text()


        # Closing the Database Connection.
        self.db_con.close()
        self.cur.close()


    def searchBook(self):
        pass


    def editBook(self):
        pass


    def deleteBook(self):
        pass


    #####################################################
    ################## Users ############################


    def addNewUser(self):
        pass


    def login(self):
        pass


    def editUser(self):
        pass


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


    def Show_Categories(self):

        # Connecting to Database
        self.db_con = mysql.connector.connect(user = "root", password = "2894", host = "localhost", database = "library")
        self.cur = self.db_con.cursor()

        # getting the all book categories from table category
        self.cur.execute("""SELECT category_name FROM category""")
        data = self.cur.fetchall()

        # Inserting data into the Categories Table
        if data:
            self.Categories_tableWidget.setRowCount(0)
            for row, form in enumerate(data):
                self.Categories_tableWidget.insertRow(row)
                form = [row+1] + [form[0]]
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


    def Show_Authors(self):

        # Connecting to Database
        self.db_con = mysql.connector.connect(user="root", password="2894", host="localhost", database="library")
        self.cur = self.db_con.cursor()

        # getting the all book categories from table category
        self.cur.execute("""SELECT author_name FROM author""")
        data = self.cur.fetchall()

        # Inserting data into the Categories Table
        if data:
            self.Authors_tableWidget.setRowCount(0)
            for row, form in enumerate(data):
                self.Authors_tableWidget.insertRow(row)
                form = [row + 1] + [form[0]]
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


    def Show_Publishers(self):

        # Connecting to Database
        self.db_con = mysql.connector.connect(user="root", password="2894", host="localhost", database="library")
        self.cur = self.db_con.cursor()

        # getting the all book categories from table category
        self.cur.execute("""SELECT publisher_name FROM publisher""")
        data = self.cur.fetchall()

        # Inserting data into the Categories Table
        if data:
            self.Publisher_tableWidget.setRowCount(0)
            for row, form in enumerate(data):
                self.Publisher_tableWidget.insertRow(row)
                form = [row + 1] + [form[0]]
                for col, item in enumerate(form):
                    self.Publisher_tableWidget.setItem(row, col, QTableWidgetItem(str(item)))

        self.db_con.close()
        self.cur.close()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()

