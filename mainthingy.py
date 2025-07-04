import sys
from PyQt6 import QtCore, QtWidgets, uic
from datetime import datetime
from validate_email import validate_email
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIntValidator
import pyodbc
import math

server = 'LAPTOP-LLE4EO2V\SERVER2'
database = 'RMS'  # Name of project database
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# Establish a connection to the database
connection = pyodbc.connect(connection_string)

# Create a cursor to interact with the database
cursor = connection.cursor()

class UI(QtWidgets.QMainWindow):
    def __init__(self):
    # Call the inherited classes __init__ method
        super(UI, self).__init__()
        # Load the .ui file
        uic.loadUi('ui_files/User_Login.ui', self)

        self.show()
        
        self.registerButton.clicked.connect(self.register)
        self.loginButton.clicked.connect(self.login)
        self.guestLoginButton.clicked.connect(self.guestLogin)
        self.exitButton.clicked.connect(self.exitLogin)

        self.userPass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def register(self):
        self.register_user = registerUser()
        self.register_user.show()

    def login(self):
        checking_query_customer = "Select Email, password, id from Customer"
        checking_query_staff = "Select Email, Password, id from Staff"
        if(self.emailAddress.text() == "" or self.userPass.text() == ""):
            dlg = QtWidgets.QMessageBox.warning(self,"Missing Fields Failure","Fill all fields to login!",QtWidgets.QMessageBox.StandardButton.Ok)
        else:
            cursor.execute(checking_query_customer)
            for row in cursor.fetchall():
                if (self.emailAddress.text() == row[0] and self.userPass.text() == row[1]):
                    self.user_screen = userOptions(row[2])
                    self.user_screen.show()
                    return
            cursor.execute(checking_query_staff)
            for row in cursor.fetchall():
                if (self.emailAddress.text() == row[0] and self.userPass.text() == row[1]):
                    self.admin_screen = adminScreen(row[2])
                    self.admin_screen.show()
                    return
                
            dlg = QtWidgets.QMessageBox.warning(self,"Login Failure","No account with the following email address and password exist!",QtWidgets.QMessageBox.StandardButton.Ok)

    def guestLogin(self):
        try:
            # Connect to the database
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()
            # Step 1: Insert a new entry into the Customer table with 'Guest' as the name
            cursor.execute("""
                INSERT INTO Customer ([Restaurant_id],[First_Name])
                OUTPUT INSERTED.ID
                VALUES (1,'Guest')
            """)
            # Retrieve the generated CustomerID
            new_customer_id = cursor.fetchone()[0]
            conn.commit()
            QtWidgets.QMessageBox.information(
                self,
                "Guest Login",
                f"Guest login successful. Please note, You will not be able to login with the same guest id again. Customer ID: {new_customer_id}"
            )
            # Step 2: Show the GuestScreen
            self.guest_user_screen = GuestScreen(new_customer_id)  # Pass new ID to the guest screen
            self.guest_user_screen.show()
            
        except pyodbc.Error as e:
            # Handle any database errors
            QtWidgets.QMessageBox.critical(
                self,
                "Database Error",
                f"An error occurred while creating the guest entry: {e}"
            )
        finally:
            # Always close the database connection
            if conn:
                conn.close()

    def exitLogin(self):
        self.close()




class registerUser(QtWidgets.QMainWindow):
    def __init__(self):
        super(registerUser, self).__init__()

        uic.loadUi('ui_files/User_Registration.ui', self)
        self.salaryLine.setEnabled(False)
        self.roleBox.setEnabled(False)
        self.phoneLine_2.setEnabled(False)
        self.salaryLine_2.setEnabled(False)
        self.roleSelect.currentIndexChanged.connect(self.isStaff)
        self.returnLoginButton.clicked.connect(self.closeScreen)
        self.registerButton.clicked.connect(self.registering)
        #Cancel button has been disabled as it can be misleading/unnecessary
        # self.cancelButton.clicked.connect(self.closeApp)

    def isStaff(self, i):
        self.roleBox.clear()
        self.salaryLine.clear()
        if(i == 0):
            self.salaryLine.setEnabled(False)
            self.roleBox.setEnabled(False)
            self.phoneLine_2.setEnabled(False)
            self.salaryLine_2.setEnabled(False)
        else:
            self.salaryLine.setEnabled(True)
            self.roleBox.setEnabled(True)
            self.roleBox.addItems(["Manager","Chef","Waiter","Host","Sous Chef"])
            self.phoneLine_2.setEnabled(True)
            self.salaryLine_2.setEnabled(True)
    
    def registering(self):
        if (self.firstName.text() == "" or self.lastName.text() == "" or self.emailAddress.text() == "" or self.userName.text() == "" or self.userPass.text() == "" or self.passConfirm.text() == "" or self.addressBox.toPlainText() == "" or self.phoneLine.text() == "" or (self.salaryLine.text() == "" and self.phoneLine_2.text() == "" and self.salaryLine_2.text() == "" and self.roleSelect.currentText() == "Staff")):
            dlg = QtWidgets.QMessageBox.warning(self,"Missing Fields Failure","Fill all fields to register!",QtWidgets.QMessageBox.StandardButton.Ok)
        elif (not(validate_email(self.emailAddress.text()))):
            dlg = QtWidgets.QMessageBox.warning(self,"Invalid Email Address","Email address is invalid!",QtWidgets.QMessageBox.StandardButton.Ok)
        elif (self.userPass.text() != self.passConfirm.text()):
            dlg = QtWidgets.QMessageBox.warning(self,"Password Confirmation Failure","Confirm Password doesn't have the same password!",QtWidgets.QMessageBox.StandardButton.Ok)
        elif (self.roleSelect.currentText() == "Staff" and self.salaryLine_2.text() != "ABCDE"):
            dlg = QtWidgets.QMessageBox.warning(self,"Invalid Code","Code is invalid!",QtWidgets.QMessageBox.StandardButton.Ok)
        else:
            checking_query_customer = "Select Email, username from Customer"
            checking_query_staff = "Select Email, username from Staff"
            cursor.execute(checking_query_customer)
            checkFlag = True
            for row in cursor.fetchall():
                #Add QValidation
                if (row[0] == self.emailAddress.text()):
                    dlg = QtWidgets.QMessageBox.warning(self,"Email Address Already Exists","This email is already used to make an account!",QtWidgets.QMessageBox.StandardButton.Ok)
                    checkFlag = False
                    break
                elif (row[1] == self.userName.text()):
                    dlg = QtWidgets.QMessageBox.warning(self,"User Already Exists","The username is already used to make an account!",QtWidgets.QMessageBox.StandardButton.Ok)
                    checkFlag = False
                    break
            cursor.execute(checking_query_staff)
            for row in cursor.fetchall():
                #Add QValidation
                if (row[0] == self.emailAddress.text()):
                    dlg = QtWidgets.QMessageBox.warning(self,"Email Address Already Exists","This email is already used to make an account!",QtWidgets.QMessageBox.StandardButton.Ok)
                    checkFlag = False
                    break
                elif (row[1] == self.userName.text()):
                    dlg = QtWidgets.QMessageBox.warning(self,"User Already Exists","The username is already used to make an account!",QtWidgets.QMessageBox.StandardButton.Ok)
                    checkFlag = False
                    break
            if (checkFlag):
                if(self.roleSelect.currentText() == "Staff"):
                    insert_query = """
                        INSERT INTO Staff
                        ([RestaurantID],[Full_Name],[Last_Name],[Email],[username],[Password],[Address],[Phone_Number],[Position],[Salary],[Emergency_Contact],Status,[ownerID],[Joining_Date])
                        VALUES (1,?,?,?,?,?,?,?,?,?,?,?,?,GETDATE())
                    """
                    data = (
                        self.firstName.text(),self.lastName.text(),self.emailAddress.text(),self.userName.text(),self.userPass.text(),self.addressBox.toPlainText(),self.phoneLine.text(),self.roleBox.currentText(),self.salaryLine.text(),self.phoneLine_2.text(),"Working",6
                    )
                    cursor.execute(insert_query,data)
                else:
                    insert_query_customer = """
                        INSERT INTO Customer
                        ([Restaurant_id],[First_name],[Last_name],[Email],[username],[password],[Phone_number])
                        OUTPUT INSERTED.id
                        VALUES (1,?,?,?,?,?,?)
                        
                    """
                    data = (
                        self.firstName.text(),self.lastName.text(),self.emailAddress.text(),self.userName.text(),self.userPass.text(),self.phoneLine.text()
                    )
                    print(data)
                    cursor.execute(insert_query_customer,data)
                    insert_address_query = """
                        INSERT INTO Customer_Address
                        ([id],[Address])
                        VALUES (?,?)
                    """
                    data = (cursor.fetchone()[0],self.addressBox.toPlainText())
                    cursor.execute(insert_address_query,data)

                connection.commit()
                self.firstName.clear()
                self.lastName.clear()
                self.emailAddress.clear()
                self.userName.clear()
                self.userPass.clear()
                self.passConfirm.clear()
                self.addressBox.clear()
                self.phoneLine.clear()
                self.salaryLine.clear()
                # self.roleBox.setCurrentIndex(0)
                # self.roleSelect.setCurrentIndex(0)
                dlg = QtWidgets.QMessageBox.information(self,"Account created","Account was successfully created!",QtWidgets.QMessageBox.StandardButton.Ok)


    def closeScreen(self):
        self.close()

    # Cancel button has been disabled as it can be misleading/unnecessary
    # def closeApp(self):
    #     app.quit()


class userOptions(QtWidgets.QMainWindow):
    def __init__(self, userID):
        super(userOptions, self).__init__()

        uic.loadUi('ui_files/User_Screen.ui', self)

        self.userID = userID

        self.onlineOrderButton.clicked.connect(self.onlineOrderScreen)
        self.seatReservationButton.clicked.connect(self.seatReserveScreen)
        self.feedbackButton.clicked.connect(self.feedbackScreen)
        self.trackOrderButton.clicked.connect(self.trackOrder)
        self.editProfileButton.clicked.connect(self.editProfile)
        self.backButton.clicked.connect(self.back)
    
    def onlineOrderScreen(self):
        self.online_order_screen = onlineOrder(self.userID)
        self.online_order_screen.show()

    def seatReserveScreen(self):
        self.seat_reserve_screen = seatReserve(self.userID)
        self.seat_reserve_screen.show()

    def feedbackScreen(self):
        self.feedback_screen = feedbackScreen(self.userID)
        self.feedback_screen.show()

    def trackOrder(self):
        self.trackorder_screen = trackOrderScreen(self.userID)
        self.trackorder_screen.show()

    def editProfile(self):
        self.editProfile_screen = editProfileScreen(self.userID)
        self.editProfile_screen.show()

    def back(self):
        self.close()


class editProfileScreen(QtWidgets.QMainWindow):
    def __init__(self, userID):
        super(editProfileScreen, self).__init__()

        uic.loadUi('ui_files/EditProfile.ui', self)

        self.userID = userID
        self.userPass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.newPass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.confirmPass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.load_user_details()

        self.newAddressButton.clicked.connect(self.newAddress)
        self.applyButton.clicked.connect(self.applyChanges)
        self.deleteAddressButton.clicked.connect(self.deleteAddress)
        self.backButton.clicked.connect(self.back)
        self.changePassButton.clicked.connect(self.changePassword)


    def changePassword(self):
        verify_password_query = "Select Password from Customer where id = ?"
        cursor.execute(verify_password_query,(self.userID))
        if(cursor.fetchone()[0] != self.userPass.text()):
            dlg = QtWidgets.QMessageBox.warning(self,"Invalid Password","Password is incorrect!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        else:
            if(self.newPass.text() == "" or self.confirmPass.text() == ""):
                dlg = QtWidgets.QMessageBox.warning(self,"Missing Fields Failure","Fill all fields to change password!",QtWidgets.QMessageBox.StandardButton.Ok)
                return
            elif(self.newPass.text() != self.confirmPass.text()):
                dlg = QtWidgets.QMessageBox.warning(self,"Password Confirmation Failure","Confirm Password doesn't have the same password!",QtWidgets.QMessageBox.StandardButton.Ok)
                return
            update_query = """
                UPDATE Customer
                SET password = ?
                WHERE id = ?
            """
            data = (self.newPass.text(),self.userID)
            cursor.execute(update_query,data)
            connection.commit()
            dlg = QtWidgets.QMessageBox.information(self,"Password Changed","Password was successfully changed!",QtWidgets.QMessageBox.StandardButton.Ok)

    def load_user_details(self):
        autofill_query = "Select First_name, Last_name, Email, username, Phone_number from Customer where id = ?"
        cursor.execute(autofill_query,(self.userID))
        for row in cursor.fetchall():
            self.firstName.setText(row[0])
            self.lastName.setText(row[1])
            self.emailAddress.setText(row[2])
            self.userName.setText(row[3])
            # self.userPass.setText(row[4])
            # self.passConfirm.setText(row[4])
            self.phoneNum.setText(row[4])

        autofill_address_query = "Select Address from Customer_Address where id = ?"
        cursor.execute(autofill_address_query,(self.userID))
        self.addressList.clear()
        for row in cursor.fetchall():
            self.addressList.addItem(row[0])
        

    def newAddress(self):
        self.newAddress_screen = newAddressScreen(self.userID)
        self.newAddress_screen.signal_to_update.connect(self.load_user_details)
        self.newAddress_screen.show()

    def applyChanges(self):
        if (self.firstName.text() == "" or self.lastName.text() == "" or self.emailAddress.text() == "" or self.userName.text() == "" or self.phoneNum.text() == ""):
            dlg = QtWidgets.QMessageBox.warning(self,"Missing Fields Failure","Fill all fields to apply changes!",QtWidgets.QMessageBox.StandardButton.Ok)
        elif (not(validate_email(self.emailAddress.text()))):
            dlg = QtWidgets.QMessageBox.warning(self,"Invalid Email Address","Email address is invalid!",QtWidgets.QMessageBox.StandardButton.Ok)
        else:
            verify_query = "Select Email, username from Customer where id <> ?"
            cursor.execute(verify_query,(self.userID))
            for row in cursor.fetchall():
                if (self.emailAddress.text() == row[0]):
                    dlg = QtWidgets.QMessageBox.warning(self,"Email Address Already Exists","This email is already used to make an account!",QtWidgets.QMessageBox.StandardButton.Ok)
                    return
                elif (self.userName.text() == row[1]):
                    dlg = QtWidgets.QMessageBox.warning(self,"User Already Exists","The username is already used to make an account!",QtWidgets.QMessageBox.StandardButton.Ok)
                    return
            


            update_query = """
                UPDATE Customer
                SET First_name = ?, Last_name = ?, Email = ?, username = ?, Phone_number = ?
                WHERE id = ?
            """
            data = (self.firstName.text(),self.lastName.text(),self.emailAddress.text(),self.userName.text(),self.phoneNum.text(),self.userID)
            cursor.execute(update_query,data)
            connection.commit()
            dlg = QtWidgets.QMessageBox.information(self,"Changes Applied","Account was successfully updated!",QtWidgets.QMessageBox.StandardButton.Ok)
    
    def deleteAddress(self):
        if(self.addressList.currentItem() == None):
            dlg = QtWidgets.QMessageBox.warning(self,"No Address Selected","Select an address to delete!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        delete_query = "Delete Customer_Address where id = ? and Address = ?"
        cursor.execute(delete_query,(self.userID,self.addressList.currentItem().text()))
        self.addressList.takeItem(self.addressList.currentRow())
        dlg = QtWidgets.QMessageBox.information(self,"Address Deleted","Address was successfully deleted!",QtWidgets.QMessageBox.StandardButton.Ok)
        connection.commit()
    
    def back(self):
        self.close()

class GuestScreen(QtWidgets.QMainWindow):
    def __init__(self, userID):
        super(GuestScreen, self).__init__()

        self.userID = userID

        uic.loadUi('ui_files/GuestScreen.ui', self)

        self.onlineOrderButton.clicked.connect(self.onlineOrderScreen)
        self.trackOrderButton.clicked.connect(self.trackOrder)

    def onlineOrderScreen(self):
        self.online_order_screen = onlineOrder(self.userID)
        self.online_order_screen.show()

    def trackOrder(self):
        self.trackorder_screen = trackOrderScreen(self.userID)
        self.trackorder_screen.show()


class newAddressScreen(QtWidgets.QMainWindow):
    signal_to_update = QtCore.pyqtSignal()

    def __init__(self,user_id):
        super(newAddressScreen, self).__init__()

        uic.loadUi('ui_files/addAddressScreen.ui', self)

        self.userId = user_id

        self.submitButton.clicked.connect(self.addressSubmitted)
        self.backButton.clicked.connect(self.back)

    def addressSubmitted(self):
        if(self.addressBox.toPlainText() == ""):
            dlg = QtWidgets.QMessageBox.warning(self,"Missing Fields Failure","Fill all fields to submit address!",QtWidgets.QMessageBox.StandardButton.Ok)
        else:
            insert_query = """
                INSERT INTO Customer_Address
                ([id],[Address])
                VALUES (?,?)
            """
            data = (self.userId,self.addressBox.toPlainText())
            cursor.execute(insert_query,data)
            connection.commit()
            dlg = QtWidgets.QMessageBox.information(self,"Address Added","Address was successfully added!",QtWidgets.QMessageBox.StandardButton.Ok)
            self.signal_to_update.emit()

    def back(self):
        
        self.close()


class onlineOrder(QtWidgets.QMainWindow):
    def __init__(self, userID):
        super(onlineOrder, self).__init__()

        uic.loadUi('ui_files/Order_ItemSelect_Customer.ui', self)

        self.userID = userID

        self.populate_menu_table()
        self.populate_category_box()

        self.checkOutButton.clicked.connect(self.checkOutScreen)
        self.backButton.clicked.connect(self.back)
        self.searchButton.clicked.connect(self.filter_menu_table)
        self.showAllButton.clicked.connect(self.populate_menu_table)
        self.addCartButton.clicked.connect(self.add_to_cart_table)
        self.removeItem.clicked.connect(self.removeItemFromCart)

    def removeItemFromCart(self):
        selected_item = self.cartTable.currentRow()
        if (self.cartTable.selectedItems() == []):
            dlg = QtWidgets.QMessageBox.warning(self,"No Item Selected","Select an item to remove from cart!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        quantity = int(self.cartTable.item(selected_item, 2).text())
        if(quantity == 1):
            self.cartTable.removeRow(selected_item)
        else:
            self.cartTable.item(selected_item, 2).setText(str(quantity-1))
            self.cartTable.item(selected_item, 4).setText(str((quantity-1) * float(self.cartTable.item(selected_item, 3).text())))

    def populate_menu_table(self):
        column_names = ["Name","Category","Price"]
        self.menuTable.clear()
        self.menuTable.setHorizontalHeaderLabels(column_names)
        populate_menu_query = "Select Name, Category, Price from  MenuItem"
        cursor.execute(populate_menu_query)
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.menuTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.menuTable.setItem(row_index, col_index, item)
        

    def populate_category_box(self):
        populate_category_query = "Select distinct Category from MenuItem"
        cursor.execute(populate_category_query)
        for row in cursor.fetchall():
            print(row[0])
            self.categoryBox.addItem(row[0])
                
    def filter_menu_table(self):
        populate_menu_query = "Select Name, Category, Price from  MenuItem where Name like ? AND Category LIKE ?"
        cursor.execute(populate_menu_query,(f"%{self.itemNameLine.text()}%"),f"%{self.categoryBox.currentText()}%")
        stringArray = ["Name","Category","Price"]
        self.menuTable.clear()
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.menuTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.menuTable.setItem(row_index, col_index, item)
        self.menuTable.setHorizontalHeaderLabels(stringArray)

    def add_to_cart_table(self):
        selected_row = self.menuTable.currentRow()
        if self.menuTable.selectedItems() == []:
            dlg = QtWidgets.QMessageBox.warning(self,"No Item Selected","Select an item to add to cart!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        item_name = self.menuTable.item(selected_row, 0).text()
        item_category = self.menuTable.item(selected_row, 1).text()
        item_price = self.menuTable.item(selected_row, 2).text()
        for i in range(self.cartTable.rowCount()):
            if self.cartTable.item(i, 0).text() == item_name and self.cartTable.item(i, 1).text() == item_category and self.cartTable.item(i, 3).text() == item_price:
                self.cartTable.item(i, 2).setText(str(int(self.cartTable.item(i, 2).text()) + 1))
                self.cartTable.item(i, 4).setText(str(int(self.cartTable.item(i, 2).text()) * float(item_price)))
                return
        self.cartTable.insertRow(self.cartTable.rowCount())
        self.cartTable.setItem(self.cartTable.rowCount()-1, 0, QTableWidgetItem(str(item_name)))
        self.cartTable.setItem(self.cartTable.rowCount()-1, 1, QTableWidgetItem(str(item_category)))
        self.cartTable.setItem(self.cartTable.rowCount()-1, 2, QTableWidgetItem(str("1"))) 
        self.cartTable.setItem(self.cartTable.rowCount()-1, 3, QTableWidgetItem(str(item_price)))
        self.cartTable.setItem(self.cartTable.rowCount()-1, 4, QTableWidgetItem(str(item_price)))
        


    def back(self):
        self.close()

    def checkOutScreen(self):
        if(self.cartTable.rowCount() == 0):
            dlg = QtWidgets.QMessageBox.warning(self,"Empty Cart","Add items to cart to proceed to checkout!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        self.checkout_screen = checkOutScreen(self.cartTable,self.userID)
        self.checkout_screen.signal.connect(self.closeScreen)
        self.checkout_screen.show()

    def closeScreen(self):
        self.close()

class checkOutScreen(QtWidgets.QMainWindow):
    signal = QtCore.pyqtSignal()
    def __init__(self, cartTable, userID):
        super(checkOutScreen, self).__init__()

        uic.loadUi('ui_files/OnlineOrderCheckout.ui', self)
        
        self.cardNumber.setInputMask("0000-0000-0000-0000;_")
        self.cvcNumber.setInputMask("000;_") 
        self.expiryDate.setDisplayFormat("MM/yy")
        self.cashButton.setChecked(True)
        self.cardNumber.setEnabled(False)
        self.cvcNumber.setEnabled(False)
        self.expiryDate.setEnabled(False)
        self.cardHolderName.setEnabled(False)
        self.lineEdit.setEnabled(False)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_3.setEnabled(False)
        self.lineEdit_4.setEnabled(False)



        self.cartTable = cartTable
        self.userID = userID
        self.totalAmountInt = 0
        self.address = ""

        self.lineEdit_2.setText("500")

        self.autofill_information()
        self.backButton.clicked.connect(self.back)
        self.orderButton.clicked.connect(self.orderConfirmed)
        self.cashButton.toggled.connect(self.paymentMethod)
        self.addressList.itemSelectionChanged.connect(self.add_address)

    def add_address(self):
        self.address = self.addressList.currentItem().text()
        self.addressEdit.setText(self.address)        


    def paymentMethod(self, selected):
        if(selected):
            self.cardNumber.setEnabled(False)
            self.cvcNumber.setEnabled(False)
            self.expiryDate.setEnabled(False)
            self.cardHolderName.setEnabled(False)
            self.lineEdit_3.setText(str(self.totalAmountInt * 0.15))
        else:
            self.cardNumber.setEnabled(True)
            self.cvcNumber.setEnabled(True)
            self.expiryDate.setEnabled(True)
            self.cardHolderName.setEnabled(True)
            self.lineEdit_3.setText(str(self.totalAmountInt * 0.12))
        self.lineEdit_4.setText(str(self.totalAmountInt + 500 + float(self.lineEdit_3.text())))

    def back(self):
        self.close()

    def autofill_information(self):
        autofill_query = "Select concat(First_name, ' ', Last_name), Email, Phone_number from Customer where id = ?"
        cursor.execute(autofill_query,(self.userID))
        for row in cursor.fetchall():
            self.customerName.setText(row[0])
            self.emailAddress.setText(row[1])
            self.phoneNum.setText(row[2])

        self.customerName.setEnabled(False)
        self.emailAddress.setEnabled(False)
        self.phoneNum.setEnabled(False)

        address_autofill_query = "Select Address from Customer_Address where id = ?"
        cursor.execute(address_autofill_query,(self.userID))
        for row in cursor.fetchall():
            self.addressList.addItem(row[0])

        for row in range(self.cartTable.rowCount()):
            self.checkOutItemTable.insertRow(row)
            self.checkOutItemTable.setItem(row, 0, QTableWidgetItem(str(self.cartTable.item(row, 0).text())))
            self.checkOutItemTable.setItem(row, 1, QTableWidgetItem(str(self.cartTable.item(row, 3).text())))
            self.checkOutItemTable.setItem(row, 2, QTableWidgetItem(str(self.cartTable.item(row, 2).text())))
            self.checkOutItemTable.setItem(row, 3, QTableWidgetItem(str(float(self.cartTable.item(row, 4).text()) * int(self.cartTable.item(row, 2).text()))))
            self.totalAmountInt += float(self.cartTable.item(row, 4).text())
        self.lineEdit.setText(str(self.totalAmountInt))
        if(self.cashButton.isChecked()):
            self.lineEdit_3.setText(str((self.totalAmountInt+500) * 0.15))
        else:
            self.lineEdit_3.setText(str((self.totalAmountInt+500) * 0.12))
        self.lineEdit_4.setText(str(self.totalAmountInt + 500 + float(self.lineEdit_3.text())))
        
        

        # self.address = self.addressList.currentItem().text()  




    def orderConfirmed(self):
        if(self.addressEdit.text() == ""):
            dlg = QtWidgets.QMessageBox.warning(self,"No Address Given","Give an address to place order!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        else:
            self.address = self.addressEdit.text()
        
        if(self.cashButton.isChecked() == False and self.cardButton.isChecked() == False):
            dlg = QtWidgets.QMessageBox.warning(self,"No Payment Method Selected","Select a payment method to place order!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        
        if(self.cardButton.isChecked()):
            if(self.cardNumber.text() == "" or self.cvcNumber.text() == "" or self.expiryDate.text() == "" or self.cardHolderName.text() == ""):
                dlg = QtWidgets.QMessageBox.warning(self,"Missing Fields Failure","Fill all fields to place order!",QtWidgets.QMessageBox.StandardButton.Ok)
                return
        insert_transaction_query = """
            INSERT INTO [Transaction]([Date],[Time],[Type],[PaymentType],[Amount],[Tax])
            OUTPUT INSERTED.ID
            VALUES (?,?,?,?,?,?)
        """
        date = str(datetime.today().date())
        time = str(datetime.today().time())
        self.paymentType = ""
        if(self.cashButton.isChecked()):
            self.paymentType = "Cash"
        elif (self.cardButton.isChecked()):
            self.paymentType = "Card"
        print(self.paymentType)
        amountWithoutTax = float(self.lineEdit_2.text()) + float(self.lineEdit.text())
        tax = 0
        if(self.cashButton.isChecked()):
            tax = 15
        else:
            tax = 12
        data = (date,time,"Order",self.paymentType,amountWithoutTax,tax)
        cursor.execute(insert_transaction_query,data)

        insert_order_query = """
            INSERT INTO Orders([TransactionID],[CustomerID],[CustomerAddress],[Special_Request],[Date],[Time],[Status])
            OUTPUT INSERTED.ID
            VALUES (?,?,?,?,?,?,?)
        """
        date = str(datetime.today().date())
        time = str(datetime.today().time())
        print(self.address)
        print(self.specReq.text())
        data = (cursor.fetchone()[0],self.userID,self.address,self.specReq.text(),date,time,"Confirmed")
        cursor.execute(insert_order_query,data)

        insert_order_menu_query = """
            INSERT INTO Order_Menu([Order_ID],[Item_ID],[Quantity]) 
            VALUES (?,?,?)
        """
        orderID = cursor.fetchone()[0]
        for row in range(self.checkOutItemTable.rowCount()):
            itemID_query = "Select id from MenuItem where Name = ?"
            cursor.execute(itemID_query,(self.checkOutItemTable.item(row, 0).text()))
            itemID = cursor.fetchone()[0]
            data = (orderID,itemID,int(self.checkOutItemTable.item(row, 2).text()))
            cursor.execute(insert_order_menu_query,data)
        connection.commit()

        dlg = QtWidgets.QMessageBox.information(self,"Order Confirmed","Order was successfully placed!",QtWidgets.QMessageBox.StandardButton.Ok)
        
        self.signal.emit()
        self.close()


class seatReserve(QtWidgets.QMainWindow):
    def __init__(self,userID):
        super(seatReserve, self).__init__()

        uic.loadUi('ui_files/Reservation_Form.ui', self)

        self.userID = userID

        self.backButton.clicked.connect(self.back)
        self.cancelReservationButton.clicked.connect(self.cancelReservation)
        self.viewStatusButton.clicked.connect(self.viewStatus)
        self.reserveButton.clicked.connect(self.reserve)
        self.populateCustomerReservations()

    def populateCustomerReservations(self):
        self.reservationComboBox.clear()
        autofill_query = "Select concat(First_name, ' ', Last_name) from Customer where id = ?"
        cursor.execute(autofill_query,(self.userID))
        customerName = ""
        for row in cursor.fetchall():
            customerName = row[0]
        self.customerName.setText(customerName)
        self.customerName.setEnabled(False)
        populate_query = "Select id from Reservations where CustomerID = ?"
        cursor.execute(populate_query,(self.userID))
        for row in cursor.fetchall():
            self.reservationComboBox.addItem(str(row[0]))

    def back(self):
        self.close()

    def cancelReservation(self):
        if(self.reservationComboBox.currentText() == ""):
            dlg = QtWidgets.QMessageBox.warning(self,"No Reservation Selected","Select a reservation to cancel!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        update_query = "Update Reservations set Status = 'Cancelled' where id = ?"
        cursor.execute(update_query,(self.reservationComboBox.currentText()))
        connection.commit()
        self.reservationComboBox.removeItem(self.reservationComboBox.currentIndex())
        dlg = QtWidgets.QMessageBox.information(self,"Reservation Cancelled","Reservation was successfully cancelled!",QtWidgets.QMessageBox.StandardButton.Ok)

    def viewStatus(self):
        if(self.reservationComboBox.currentText() == ""):
            dlg = QtWidgets.QMessageBox.warning(self,"No Reservation Selected","Select a reservation to view status!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        self.view_status_screen = viewStatusScreen(self.userID,self.reservationComboBox.currentText())
        self.view_status_screen.show()

    def reserve(self):
        if(self.dateSelect.date() < QDate.currentDate() or (self.timeSelect.time() < QTime.currentTime() and self.dateSelect.date() == QDate.currentDate()) or self.customerName.text() == "" or self.partySize.value() == 0):
            dlg = QtWidgets.QMessageBox.warning(self,"Invalid Reservation","Invalid reservation details!",QtWidgets.QMessageBox.StandardButton.Ok)
        else:
            insert_reservation_query = """
                INSERT INTO Reservations([CustomerID],[Date],[Time],[Party_Size],[Status]) 
                OUTPUT INSERTED.ID
                VALUES (?,?,?,?,?)
            """
            date = self.dateSelect.date().toPyDate()
            time = self.timeSelect.time().toPyTime()
            data = (self.userID,date,time,self.partySize.value(),"Confirmed")
            cursor.execute(insert_reservation_query,data)
            self.generateId.setText("Reservation id: " + str(cursor.fetchone()[0]))
            connection.commit()
            dlg = QtWidgets.QMessageBox.information(self,"Reservation booked","Reservation was successfully booked!",QtWidgets.QMessageBox.StandardButton.Ok)
            self.populateCustomerReservations()


class viewStatusScreen(QtWidgets.QMainWindow):
    def __init__(self, userID, reservationId):
        super(viewStatusScreen, self).__init__()

        uic.loadUi('ui_files/Reservation_Status.ui', self)

        self.userID = userID
        self.reservationId = reservationId

        self.populateCustomerReservations()
        self.backButton.clicked.connect(self.back)

    def populateCustomerReservations(self):
        autofill_query = "Select concat(First_name, ' ', Last_name) from Customer where id = ?"
        cursor.execute(autofill_query,(self.userID))
        customerName = ""
        for row in cursor.fetchall():
            customerName = row[0]
        self.reservationIdLine.setText(self.reservationId)
        self.customerNameLine.setText(customerName)
        populate_query = "Select Date, Time, Party_Size, Status from Reservations where id = ?"
        cursor.execute(populate_query,((self.reservationId)))
        for row in cursor.fetchall():
            self.dateEdit.setDate(row[0])
            self.timeEdit.setTime(row[1])
            self.spinBox.setValue(row[2])
            self.statusLine.setText(row[3])
        self.dateEdit.setEnabled(False)
        self.timeEdit.setEnabled(False)
        self.spinBox.setEnabled(False)
        self.statusLine.setEnabled(False)
        self.reservationIdLine.setEnabled(False)
        self.customerNameLine.setEnabled(False)

    def back(self):
        self.close()


class feedbackScreen(QtWidgets.QMainWindow):
    def __init__(self, userID):
        super(feedbackScreen, self).__init__()

        uic.loadUi('ui_files/CustomerFeedBackForm.ui', self)

        self.userID = userID
        self.totalRating = 0

        self.populateOrderComboBox()
        self.backButton.clicked.connect(self.back)
        self.submitButton.clicked.connect(self.submit)

    def populateOrderComboBox(self):
        self.comboBox.clear()
        populate_query = "Select id from Orders where CustomerID = ? EXCEPT Select OrderID from Feedback"
        cursor.execute(populate_query,(self.userID))
        for row in cursor.fetchall():
            self.comboBox.addItem(str(row[0]))
        

    def back(self):
        self.close()

    def submit(self):
        check_query = "Select * from Feedback where OrderID = ?"
        cursor.execute(check_query,(self.comboBox.currentText()))
        if(cursor.fetchone() != None):
            dlg = QtWidgets.QMessageBox.warning(self,"Feedback Already Submitted","Feedback for this order has already been submitted!",QtWidgets.QMessageBox.StandardButton.Ok)
            return

        if(self.comboBox.currentText() == "" or (not(self.menuDiverseVPoor.isChecked() or self.menuDiversePoor.isChecked() or self.menuDiverseFair.isChecked() or self.menuDiverseGood.isChecked() or self.menuDiverseExcellent.isChecked())) or (not(self.freshnessVPoor.isChecked() or self.freshnessPoor.isChecked() or self.freshnessFair.isChecked() or self.freshnessGood.isChecked() or self.freshnessExcellent.isChecked())) or (not(self.responseVPoor.isChecked() or self.responsePoor.isChecked() or self.responseFair.isChecked() or self.responseGood.isChecked() or self.responseExcellent.isChecked())) or (not(self.politenessVPoor.isChecked() or self.politenessPoor.isChecked() or self.politenessFair.isChecked() or self.politenessGood.isChecked() or self.politenessExcellent.isChecked()))):
            dlg = QtWidgets.QMessageBox.warning(self,"Invalid Feedback","Fill all fields to submit feedback!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        if(self.menuDiverseVPoor.isChecked() or self.freshnessVPoor.isChecked() or self.responseVPoor.isChecked() or self.politenessVPoor.isChecked()):
            self.totalRating += 0
        if(self.menuDiversePoor.isChecked() or self.freshnessPoor.isChecked() or self.responsePoor.isChecked() or self.politenessPoor.isChecked()):
            self.totalRating += 1
        if(self.menuDiverseFair.isChecked() or self.freshnessFair.isChecked() or self.responseFair.isChecked() or self.politenessFair.isChecked()):
            self.totalRating += 2
        if(self.menuDiverseGood.isChecked() or self.freshnessGood.isChecked() or self.responseGood.isChecked() or self.politenessGood.isChecked()):
            self.totalRating += 3
        if(self.menuDiverseExcellent.isChecked() or self.freshnessExcellent.isChecked() or self.responseExcellent.isChecked() or self.politenessExcellent.isChecked()):
            self.totalRating += 4

        insert_feedback_query = """
            INSERT INTO Feedback([OrderID],[Rating]) VALUES (?,?)
        """
        data = (self.comboBox.currentText(),self.totalRating)
        cursor.execute(insert_feedback_query,data)
        connection.commit()

        dlg = QtWidgets.QMessageBox.information(self,"Feedback successfully submitted","Feedback was successfully submitted!",QtWidgets.QMessageBox.StandardButton.Ok)
        self.populateOrderComboBox()
        

class trackOrderScreen(QtWidgets.QMainWindow):
    def __init__(self, userID):
        super(trackOrderScreen, self).__init__()

        uic.loadUi('ui_files/OrderTrackMain.ui', self)

        self.userID = userID

        self.populateOrderTable()
        self.viewDetailsButton.clicked.connect(self.DetailScreen)
        self.backButton.clicked.connect(self.back)

    def populateOrderTable(self):
        self.orderTable.clear()
        populate_query = "Select id, Status from Orders where CustomerID = ?;"
        cursor.execute(populate_query,(self.userID))
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.orderTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.orderTable.setItem(row_index, col_index, item)
            total_amount_query = """
                SELECT (Amount+(Amount*(Tax/100))) from [Transaction] where id = (Select TransactionID from Orders where id = ?)
            """
            cursor.execute(total_amount_query,(row_data[0]))
            for row in cursor.fetchall():
                self.orderTable.setItem(row_index, 2, QTableWidgetItem(str(row[0])))
        self.orderTable.setHorizontalHeaderLabels(["Order ID","Status","Total Amount"])


    def DetailScreen(self):
        selected_row = self.orderTable.currentRow()
        if(self.orderTable.selectedItems() == []):
            dlg = QtWidgets.QMessageBox.warning(self,"No Order Selected","Select an order to view details!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        self.detail_screen = viewDetailScreen(self.userID,self.orderTable.item(selected_row,0).text())
        self.detail_screen.show()

    def back(self):
        self.close()


class viewDetailScreen(QtWidgets.QMainWindow):
    def __init__(self, userID, orderID):
        super(viewDetailScreen, self).__init__()

        uic.loadUi('ui_files/OrderTrackDetails.ui', self)   

        self.userID = userID
        self.orderID = orderID 

        self.populateOrderDetails()
        self.backButton.clicked.connect(self.back)

    def populateOrderDetails(self):
        get_person_info_query = """
            Select concat(First_name, ' ', Last_name), Email, Phone_number from Customer where id = ?
        """
        cursor.execute(get_person_info_query,(self.userID))
        for row in cursor.fetchall():
            self.customerName.setText(row[0])
            self.emailAddress.setText(row[1])
            self.phoneNum.setText(row[2])

        get_address_query = "Select CustomerAddress from Orders where id = ?"
        cursor.execute(get_address_query,(self.orderID))
        for row in cursor.fetchall():
            self.addressLine.setText(row[0])
        get_items_quantity_price_query = "Select Name, Price, Quantity from MenuItem Inner Join Order_Menu ON MenuItem.ID = Order_Menu.Item_ID where Order_ID = ?;"
        cursor.execute(get_items_quantity_price_query,(self.orderID))
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.itemTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.itemTable.setItem(row_index, col_index, item)
            self.itemTable.setItem(row_index, 3, QTableWidgetItem(str(float(row_data[1]) * int(row_data[2]))))
        
        transaction_query = "Select Amount, Tax from [Transaction] where id = (Select TransactionID from Orders where id = ?)"
        cursor.execute(transaction_query,(self.orderID))
        for row in cursor.fetchall():
            self.lineEdit.setText(str(row[0] - 500))
            self.lineEdit_2.setText("500")
            self.lineEdit_3.setText(str(row[1]*(row[0] / 100)))
            self.lineEdit_4.setText(str(row[0] + (row[0] * (row[1] / 100))))

        self.orderIdLine.setText(self.orderID)
        payment_type_query = "Select PaymentType from [Transaction] Inner Join Orders ON [Transaction].id = Orders.TransactionID where Orders.id = ?"
        cursor.execute(payment_type_query,(self.orderID))

        for row in cursor.fetchall():
            print(row[0])
            if(row[0] == "Cash"):
                self.cashButton.setChecked(True)
            elif(row[0] == "Card"):
                self.cardButton.setChecked(True)

        # if(cursor.fetchone()[0] == "Cash"):
        #     self.cashButton.setChecked(True)   
        # elif(cursor.fetchone()[0] == "Card"):
        #     self.cardButton.setChecked(True)

        get_special_request_query = "Select Special_Request, Status from Orders where id = ?"
        cursor.execute(get_special_request_query,(self.orderID))
        for row in cursor.fetchall():    
            self.specReqLine.setText(row[0])
            self.statusLine.setText(row[1])

        self.customerName.setEnabled(False)
        self.emailAddress.setEnabled(False)
        self.phoneNum.setEnabled(False)
        self.addressLine.setEnabled(False)
        self.orderIdLine.setEnabled(False)
        self.specReqLine.setEnabled(False)
        self.statusLine.setEnabled(False)
        self.lineEdit.setEnabled(False)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_3.setEnabled(False)
        self.lineEdit_4.setEnabled(False)
        self.itemTable.setEnabled(False)
        self.cashButton.setEnabled(False)
        self.cardButton.setEnabled(False)






    def back(self):
        self.close()

class adminScreen(QtWidgets.QMainWindow):
    def __init__(self,userID):
        super(adminScreen, self).__init__()

        uic.loadUi('ui_files/AdminScreen.ui', self)
        self.userID = userID
        self.billGenButton.clicked.connect(self.billGeneration)
        self.feedbackButton.clicked.connect(self.viewFeedback)
        self.inventoryButton.clicked.connect(self.showInventory)
        self.menuButton.clicked.connect(self.showMenu)
        self.orderButton.clicked.connect(self.showOrder)
        self.transactionButton.clicked.connect(self.showTransaction)
        self.reservationButton.clicked.connect(self.showReservations)
        self.staffButton.clicked.connect(self.showStaff)
        self.backButton.clicked.connect(self.back)

    def billGeneration(self):
        checking_query = "Select Position from Staff where id = ?"
        print(self.userID)
        cursor.execute(checking_query,(int(self.userID)))
        position = cursor.fetchone()[0]
        if (position == "Chef" or position == "Host" or position == "Sous Chef"):
            dlg = QtWidgets.QMessageBox.warning(self,"Access Denied","You do not have access to this feature!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        else:
            self.bill_screen = billScreen()
            self.bill_screen.show()

    def viewFeedback(self):
        self.feedback_screen = FeedbackScreen()
        self.feedback_screen.show()

    def showInventory(self):
        checking_query = "Select Position from Staff where id = ?"
        cursor.execute(checking_query,(self.userID))
        position = cursor.fetchone()[0]
        if(position == "Waiter" or position == "Host"):
            dlg = QtWidgets.QMessageBox.warning(self,"Access Denied","You do not have access to this feature!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        self.inventory_screen = InventoryScreen(self.userID)
        self.inventory_screen.show()

    def showMenu(self):
        checking_query = "Select Position from Staff where id = ?"
        cursor.execute(checking_query,(self.userID))
        position = cursor.fetchone()[0]
        if(position == "Waiter" or position == "Host"):
            dlg = QtWidgets.QMessageBox.warning(self,"Access Denied","You do not have access to this feature!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        self.menu_screen = MenuScreen()
        self.menu_screen.show()

    def showOrder(self):
        checking_query = "Select Position from Staff where id = ?"
        cursor.execute(checking_query,(self.userID))
        position = cursor.fetchone()[0]
        if (position == "Host"):
            dlg = QtWidgets.QMessageBox.warning(self,"Access Denied","You do not have access to this feature!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        self.order_screen = OrderScreen(self.userID)
        self.order_screen.show()

    def showTransaction(self):
        checking_query = "Select Position from Staff where id = ?"
        cursor.execute(checking_query,(self.userID))
        position = cursor.fetchone()[0]
        if (position == "CEO"):
            self.transaction_screen = TransactionScreen(self.userID)
            self.transaction_screen.show()
        else:
            dlg = QtWidgets.QMessageBox.warning(self,"Access Denied","You do not have access to this feature!",QtWidgets.QMessageBox.StandardButton.Ok)


    def showReservations(self):
        self.reservation_screen = ReservationScreen()
        self.reservation_screen.show()

    def showStaff(self):
        checking_query = "Select Position from Staff where id = ?"
        cursor.execute(checking_query,(self.userID))
        poistion = cursor.fetchone()[0]
        if(poistion == "CEO"):
            self.staff_screen = StaffScreen()
            self.staff_screen.show()
        else:
            dlg = QtWidgets.QMessageBox.warning(self,"Access Denied","You do not have access to this feature!",QtWidgets.QMessageBox.StandardButton.Ok)

    def back(self):
        self.close()


class billScreen(QtWidgets.QMainWindow): # DONE #
    def __init__(self):
        super(billScreen, self).__init__()

        uic.loadUi('ui_files/generateBillStart.ui', self)

        self.generateButton.clicked.connect(self.generateBill)
        self.backButton.clicked.connect(self.back)

        # Define the query
        query = """
        SELECT o.id AS OrderID, o.StaffID, o.Table_no, t.Type AS Type
        FROM Orders o
        JOIN [Transaction] t ON o.TransactionID = t.id
        """
        cursor.execute(query)
        data = cursor.fetchall()
        self.populate_table(data)

    def populate_table(self, data):
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)  # Select entire row on click

        # Populate the table widget
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)  # Items non-editable
                self.tableWidget.setItem(i, j, item)
        
    def getSelectedRowValues(self):
        selected_row = self.tableWidget.currentRow()
        row_values = []
        for col in range(self.tableWidget.columnCount()):
            item = self.tableWidget.item(selected_row, col)
            if item is not None:
                row_values.append(item.text())
        return row_values

    def generateBill(self):
        if self.tableWidget.selectedItems() != []:  # Check if no row is selected
            selected_rows = self.getSelectedRowValues()
            self.generateBill_screen = generateBillScreen(selected_rows)
            self.generateBill_screen.show()
        else:
            QMessageBox.warning(self, "Error", "Please select a row before generating the bill.")


    def back(self):
        self.close()

class generateBillScreen(QtWidgets.QMainWindow): # DONE #
    def __init__(self, data):
        super(generateBillScreen, self).__init__()

        uic.loadUi('ui_files/billPrintAndOrderCompleted.ui', self)

        self.order_id = data[0]
        self.staff_id = data[1]
        self.table_no = data[2]
        self.payment_type = data[3]

        query0 = """
        SELECT TransactionID
        FROM Orders 
        WHERE id = ?
        """
        cursor.execute(query0, (self.order_id))
        self.t_id = cursor.fetchone()[0]

        # Setting Order ID
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setText(self.order_id)

        # Setting payment type
        query = "SELECT PaymentType as [Payment Type] FROM [Transaction] WHERE id = ?"
        cursor.execute(query, (self.order_id))
        payment_type = cursor.fetchone()[0]
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setText(payment_type)

        # Setting type
        self.lineEdit_7.setReadOnly(True)
        self.lineEdit_7.setText(data[3])

        # Setting Served By:
        query1 = """
            SELECT concat(Full_Name,' ',Last_Name) as Name
            FROM Staff
            WHERE id = ?
        """
        cursor.execute(query1, (self.staff_id))
        staff_name = cursor.fetchone()[0]
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_3.setText(staff_name)

        # Setting subtotal
        query2 = """
            SELECT (om.Quantity * m.Price) as subtotal
            FROM Order_Menu om
            JOIN MenuItem m ON om.Item_ID = m.ID
            WHERE om.Order_ID = ?
        """
        cursor.execute(query2, (self.order_id))
        sub_total = cursor.fetchone()[0]
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_4.setText(str(sub_total))

        # Populate the list widget
        query3 = """
            SELECT m.Name AS MenuItemName, m.Category AS MenuCategory, m.Price AS MenuPrice, om.Quantity AS QuantityOrdered
            FROM Order_Menu om
            JOIN MenuItem m ON om.Item_ID = m.ID
            WHERE om.Order_ID = ?;
        """
        cursor.execute(query3, (self.order_id))
        items = cursor.fetchall()
        for item in items:
            name, category, price, quantity = item
            display_text = f"{name} ({category}) - ${price}, Qty: {quantity}"
            self.listWidget.addItem(display_text)

        # Setting the date and time
        query4 = """
            SELECT t.Date AS TransactionDate, t.Time AS TransactionTime
            FROM Orders o
            JOIN [Transaction] t ON o.TransactionID = t.id
            WHERE o.id = ?;
        """
        cursor.execute(query4, (self.order_id))
        t_data = cursor.fetchone()
        date, time = t_data
        self.dateTimeEdit.setReadOnly(True)
        t_date = QDate.fromString(date.strftime("%Y-%m-%d"), "yyyy-MM-dd")
        t_time = QTime.fromString(time.strftime("%H:%M:%S"), "HH:mm:ss")
        datetime = QDateTime(t_date, t_time)
        self.dateTimeEdit.setDateTime(datetime)

        # Setting tax%
        self.lineEdit_5.setReadOnly(True)
        query5 = """
            SELECT Tax
            FROM [Transaction]
            WHERE id = ?;
        """
        cursor.execute(query5, (self.t_id))
        tax = cursor.fetchone()[0]
        self.lineEdit_5.setText(str(tax))

        self.lineEdit_6.setReadOnly(True)
        self.calculate_total()

        self.printButton.clicked.connect(self.printBill)
        self.paymentButton.clicked.connect(self.paymentReceived)
        self.backButton.clicked.connect(self.back)

    def calculate_total(self):
        try:
            value_4 = float(self.lineEdit_4.text())
            value_5 = float(self.lineEdit_5.text())
            total = math.ceil(value_4 * (1 + (value_5/100)))
            self.lineEdit_6.setText(str(total))
        except ValueError:
            self.lineEdit_6.setText("")

    def printBill(self):
        dlg = QtWidgets.QMessageBox.information(self,"Bill Printed","Bill for order successfully printed!",QtWidgets.QMessageBox.StandardButton.Ok)
        
    def paymentReceived(self):
        dlg = QtWidgets.QMessageBox.information(self,"Payment Received","Payment for order successfully received!",QtWidgets.QMessageBox.StandardButton.Ok)

    def back(self):
        self.close()

class FeedbackScreen(QtWidgets.QMainWindow): # DONE #
    def __init__(self):
        super(FeedbackScreen, self).__init__()

        uic.loadUi('ui_files/CustomerFeedBackView.ui', self)

        populate_query = """
            SELECT o.id AS OrderID, o.StaffID, CONCAT(s.Full_Name, ' ', s.Last_Name) AS StaffName, f.Rating
            FROM Feedback f
            JOIN Orders o ON f.OrderID = o.id
            JOIN Staff s ON o.StaffID = s.id;
        """
        cursor.execute(populate_query)
        data = cursor.fetchall()
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.tableWidget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.populate_table(data)

        self.backButton.clicked.connect(self.back)
    
    def populate_table(self, data):
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Order ID", "Staff ID", "Staff Name", "Rating"])
        self.tableWidget.horizontalHeader().setVisible(True)
        # self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setRowCount(len(data))

        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                self.tableWidget.setItem(i, j, item)

    def back(self):
        self.close()

class InventoryScreen(QtWidgets.QMainWindow):
    def __init__(self, userID):
        super(InventoryScreen, self).__init__()

        uic.loadUi('ui_files/InventoryManagment.ui', self)

        self.userID = userID
    
        self.addButton.clicked.connect(self.newItem)
        self.updateButton.clicked.connect(self.updateItem)
        self.deleteButton.clicked.connect(self.deleteItem)
        self.backButton.clicked.connect(self.back)

        self.loadInventoryData()

    def get_selected_row(self):
        """ Utility function to get the currently selected row """
        selected_items = self.tableWidget.selectedItems()
        if not selected_items:  # If no row is selected
            QtWidgets.QMessageBox.warning(
                self, 
                "Selection Required", 
                "Please select one item to proceed."
            )
            return None
        return selected_items[0].row() 
    
    def loadInventoryData(self):
       
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        try:
            query = """
                SELECT Name, id, Stock, Last_Updated, CheckerStaffID, cost, company
                FROM Ingredients;
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Populate the table with the fetched data
            self.tableWidget.setRowCount(0)
            for row_index, row_data in enumerate(rows):
                self.tableWidget.insertRow(row_index)
                for col_index, value in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    self.tableWidget.setItem(row_index, col_index, item)

        except pyodbc.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def newItem(self):
      
        self.new_item_screen = AddItemScreen(self.userID)
        self.new_item_screen.itemAdded.connect(self.loadInventoryData)
        self.new_item_screen.show()

    def updateItem(self):
      
        selected_row = self.get_selected_row()
        if selected_row is None:  # If nothing is selected, return
            return
        

        # Gather data for the selected row
        item_data = {
            "id": int(self.tableWidget.item(selected_row, 1).text()),
            "name": self.tableWidget.item(selected_row, 0).text(),
            "stock": int(self.tableWidget.item(selected_row, 2).text()),
            "last_updated": self.tableWidget.item(selected_row, 3).text(),
            "staff_id": int(self.tableWidget.item(selected_row, 4).text()),
            "cost": int(self.tableWidget.item(selected_row, 5).text()),
            "company": self.tableWidget.item(selected_row, 6).text(),
        }

        self.update_item_screen = UpdateItemScreen(item_data,self.userID)
        self.update_item_screen.itemUpdated.connect(self.loadInventoryData)
        self.update_item_screen.show()

    def deleteItem(self):
       
        selected_row = self.get_selected_row()
        if selected_row is None:  # If nothing is selected, return
            return

        item_id = int(self.tableWidget.item(selected_row, 1).text())

        confirm = QtWidgets.QMessageBox.question(
            self, "Confirm Deletion",
            "Are you sure you want to delete this item?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )

        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()

            try:
                delete_query = "DELETE FROM Ingredients WHERE id = ?;"
                cursor.execute(delete_query, (item_id,))
                conn.commit()
                QtWidgets.QMessageBox.information(self, "Item Deleted", "Item successfully deleted!")
                self.loadInventoryData()

            except pyodbc.Error as e:
                QtWidgets.QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
            finally:
                conn.close()

    def back(self):
        """Close the inventory screen."""
        self.close()

class AddItemScreen(QtWidgets.QMainWindow):
    itemAdded = pyqtSignal()

    def __init__(self,userID):
        super(AddItemScreen, self).__init__()
        uic.loadUi('ui_files/ItemAdd.ui', self)

        self.userID = userID
        self.addButton.clicked.connect(self.addItem)
        self.backButton.clicked.connect(self.back)

    def addItem(self):
        """Add a new item to the database."""
        item_name = self.lineEdit_7.text()
        company = self.userName.text()
        stock = self.spinBox.value()
        price = self.emailAddress.text()
        staffID = self.userID

        if not item_name or not company or stock < 0 or not price.isdigit():
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please provide valid input.")
            return

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        try:
            query = """
                INSERT INTO Ingredients
                (Name, InventoryID, Company, Cost, Last_Updated, Stock, checkerStaffID)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?,?);
            """
            cursor.execute(query, (item_name, 1, company, int(price), stock,staffID))
            conn.commit()

            QtWidgets.QMessageBox.information(self, "Item Added", "Item successfully added!")
            self.itemAdded.emit()
            self.close()

        except pyodbc.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
            conn.rollback()

        finally:
            conn.close()

    def back(self):
        """Close the Add Item screen."""
        self.close()

class UpdateItemScreen(QtWidgets.QMainWindow):
    itemUpdated = pyqtSignal()

    def __init__(self, item_data,userID):
        super(UpdateItemScreen, self).__init__()
        uic.loadUi('ui_files/ItemUpdate.ui', self)

        self.userID = userID
        self.item_id = item_data["id"]
        self.lineEdit_7.setText(item_data["name"])
        self.userName.setText(item_data["company"])
        self.spinBox.setValue(item_data["stock"])
        self.emailAddress.setText(str(item_data["cost"]))

        self.updateButton.clicked.connect(self.updateItem)
        self.backButton.clicked.connect(self.back)

    def updateItem(self):
        """Update the item in the database."""
        item_name = self.lineEdit_7.text()
        company = self.userName.text()
        stock = self.spinBox.value()
        price = self.emailAddress.text()
        staff_id = self.userID

        if not item_name or not company or stock < 0 or not price.isdigit() or staff_id<0:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please provide valid input.")
            return

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        try:
            query = """
                UPDATE Ingredients
                SET Name = ?, Company = ?, Cost = ?, Stock = ?, Last_Updated = CURRENT_TIMESTAMP, CheckerStaffID = ?
                WHERE id = ?;
            """
            cursor.execute(query, (item_name, company, int(price), stock, int(staff_id), self.item_id))
            conn.commit()

            QtWidgets.QMessageBox.information(self, "Item Updated", "Item successfully updated!")
            self.itemUpdated.emit()
            self.close()

        except pyodbc.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
            conn.rollback()

        finally:
            conn.close()

    def back(self):
        """Close the Update Item screen."""
        self.close()
      
class MenuScreen(QtWidgets.QMainWindow): # DONE #
    def __init__(self):
        super(MenuScreen, self).__init__()

        uic.loadUi('ui_files/Menu_management.ui', self)

        category_query = "SELECT DISTINCT Category FROM MenuItem"
        cursor.execute(category_query)
        categories = cursor.fetchall()
        
        self.comboBox.clear()
        self.comboBox.addItem("<Not Selected>")
        for c in categories:
            self.comboBox.addItem(c[0])
        self.comboBox.setCurrentIndex(0)

        self.populate_table()

        self.lineEdit_2.setValidator(QIntValidator(0, 99999))

        self.addItemButton.clicked.connect(self.addItem)
        self.clearButton.clicked.connect(self.clear)
        self.backButton.clicked.connect(self.back)
        self.editItemButton.clicked.connect(self.editItem)
        self.removeItemButton.clicked.connect(self.removeItem)

    def populate_table(self):
        self.tableWidget.clear()
        populate_menu_query = "SELECT ID, Name, Category, Price, Discontinued FROM MenuItem"
        cursor.execute(populate_menu_query)
        data = cursor.fetchall()

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)  # Select entire row on click

        # Populate the table widget
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)  # Items non-editable
                self.tableWidget.setItem(i, j, item)

    def addItem(self):
        add_query = "INSERT INTO MenuItem(Name, Category, Price, Description, Discontinued) VALUES (?, ?, ?, ?, ?)"
        name = self.lineEdit.text()
        category = self.comboBox.currentText()
        price = self.lineEdit_2.text()
        description = self.textEdit.toPlainText()
        discontinued = 0
        if(self.comboBox_2.currentText() == "Availabe to order"):
            discontinued = 0
        else:
            discontinued = 1
        if name == "" or category == "<Not Selected>" or price == "" or description == "":
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please fill all fields.")
            return
        
        cursor.execute(add_query, (name, category, price, description, discontinued))
        connection.commit()

        self.populate_table()

        dlg = QtWidgets.QMessageBox.information(self,"Menu Item Added","Menu Item successfully added!",QtWidgets.QMessageBox.StandardButton.Ok)

    def clear(self):
        self.lineEdit.clear()
        self.comboBox.setCurrentIndex(0)
        self.lineEdit_2.clear()
        self.textEdit.clear()

    def back(self):
        self.close()

    def getSelectedRowValues(self):
        selected_row = self.tableWidget.currentRow()
        row_values = []
        for col in range(self.tableWidget.columnCount()):
            item = self.tableWidget.item(selected_row, col)
            if item is not None:
                row_values.append(item.text())
        return row_values

    def editItem(self):
        if self.tableWidget.selectedItems() != []:  # Check if no row is selected
            selected_rows = self.getSelectedRowValues()
            self.edit_item_screen = editItemScreen(selected_rows, self)
            self.edit_item_screen.show()
        else:
            QMessageBox.warning(self, "Error", "Please select an item to edit.")

    def removeItem(self):
        dlg = QtWidgets.QMessageBox.question(self,"Delete Menu Item","Are you sure you want to delete this item? Deleting this item would also delete its records from any orders",QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        if dlg == QtWidgets.QMessageBox.StandardButton.Yes:
            if self.tableWidget.selectedItems() != []:  # Check if no row is selected
                selected_rows = self.getSelectedRowValues()
            else:
                QMessageBox.warning(self, "Error", "Please select an item to remove.")
                return

            item_id = selected_rows[0]
            delete_order_item_query = "DELETE FROM Order_Menu WHERE Item_ID = ?"
            delete_query = "DELETE FROM MenuItem WHERE ID = ?"
            cursor.execute(delete_order_item_query, (item_id))
            cursor.execute(delete_query, (item_id))
            connection.commit()

            self.populate_table()

            dlg = QtWidgets.QMessageBox.information(self,"Menu Item Deleted","Menu Item successfully deleted!",QtWidgets.QMessageBox.StandardButton.Ok)

class OrderScreen(QtWidgets.QMainWindow):
    def __init__(self, userID):
        super(OrderScreen, self).__init__()

        # Load the first UI (Order_ItemSelect)
        uic.loadUi('ui_files/Order_ItemSelect.ui', self)
        self.userID = userID
        
        # Initialize UI Components
        self.loadMenuItems()
        self.populate_category_box()
        self.cartItems = []  # To store cart details
        
        # Connect Buttons
        self.addCartButton.clicked.connect(self.addToCart)
        self.showAllButton.clicked.connect(self.loadMenuItems)
        self.searchButton.clicked.connect(self.searchItems)
        self.checkOutButton.clicked.connect(self.goToCheckout)
        self.pushButton.clicked.connect(self.goToOrderStatus)
        self.removeItem.clicked.connect(self.removeFromCart)
        self.backButton.clicked.connect(self.goBack)
    

        # Table Widgets Setup
        self.menuTable.setColumnCount(3)  # Adjusted to 3 columns
        self.menuTable.setHorizontalHeaderLabels(["Item Name", "Category", "Price"])  
        
        self.cartTable.setColumnCount(5)
        self.cartTable.setHorizontalHeaderLabels(["Item Name", "Category", "Quantity", "Unit Price", "Total Price"])

    def goBack(self):
        self.close()

    def loadMenuItems(self):
        """ Load all menu items into the menu table """
        try:
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()
            
            # Fetch all menu items excluding PeoplePerServing
            query = "SELECT Name, Category, Price FROM MenuItem;"
            cursor.execute(query)
            menu_items = cursor.fetchall()

            # Clear the table
            self.menuTable.setRowCount(0)
            
            # Populate menu table
            for row_idx, (name, category, price) in enumerate(menu_items):
                self.menuTable.insertRow(row_idx)
                self.menuTable.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(name))
                self.menuTable.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(category))
                self.menuTable.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(str(price))) 

        
        except pyodbc.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def addToCart(self):
        selected_row = self.menuTable.currentRow()
        if self.menuTable.selectedItems() == []:
            dlg = QtWidgets.QMessageBox.warning(self,"No Item Selected","Select an item to add to cart!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        item_name = self.menuTable.item(selected_row, 0).text()
        item_category = self.menuTable.item(selected_row, 1).text()
        item_price = self.menuTable.item(selected_row, 2).text()
        print(item_name, item_category, item_price)
        for i in range(self.cartTable.rowCount()):
            print(self.cartTable.item(i, 0).text())
            print(self.cartTable.item(i, 1).text())
            print(self.cartTable.item(i, 3).text())
            if self.cartTable.item(i, 0).text() == item_name and self.cartTable.item(i, 1).text() == item_category and self.cartTable.item(i, 3).text() == item_price:
                self.cartTable.item(i, 2).setText(str(int(self.cartTable.item(i, 2).text()) + 1))
                self.cartTable.item(i, 4).setText(str(int(self.cartTable.item(i, 2).text()) * float(item_price)))
                for i in range(len(self.cartItems)):
                    if self.cartItems[i][0] == item_name and self.cartItems[i][1] == item_category and self.cartItems[i][3] == item_price:
                        self.cartItems[i] = (item_name, item_category, int(self.cartTable.item(i, 2).text()), item_price)
                return
        self.cartTable.insertRow(self.cartTable.rowCount())
        self.cartTable.setItem(self.cartTable.rowCount()-1, 0, QTableWidgetItem(str(item_name)))
        self.cartTable.setItem(self.cartTable.rowCount()-1, 1, QTableWidgetItem(str(item_category)))
        self.cartTable.setItem(self.cartTable.rowCount()-1, 2, QTableWidgetItem(str("1"))) 
        self.cartTable.setItem(self.cartTable.rowCount()-1, 3, QTableWidgetItem(str(item_price)))
        self.cartTable.setItem(self.cartTable.rowCount()-1, 4, QTableWidgetItem(str(item_price)))
        self.cartItems.append((item_name, item_category, 1, item_price))  # Store cart data internally

    def removeFromCart(self):
        """Remove the selected item from the cart."""
        selectedRow = self.cartTable.currentRow()
        if selectedRow >= 0:  # Ensure a row is selected
            # Remove the item from cartItems (internal data)
            del self.cartItems[selectedRow]
            
            # Remove the row visually from the table
            self.cartTable.removeRow(selectedRow)
        else:
            QtWidgets.QMessageBox.warning(self, "No Selection", "Please select an item to remove.")

    def populate_category_box(self):
        populate_category_query = "Select distinct Category from MenuItem"
        cursor.execute(populate_category_query)
        for row in cursor.fetchall():
            print(row[0])
            self.categoryBox.addItem(row[0])
                
    def searchItems(self):
        populate_menu_query = "Select Name, Category, Price from  MenuItem where Name like ? AND Category LIKE ?"
        cursor.execute(populate_menu_query,(f"%{self.itemNameLine.text()}%"),f"%{self.categoryBox.currentText()}%")
        stringArray = ["Name","Category","Price"]
        self.menuTable.clear()
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.menuTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.menuTable.setItem(row_index, col_index, item)
        self.menuTable.setHorizontalHeaderLabels(stringArray)

    def goToOrderStatus(self):
        """Navigate to the CheckoutScreenAdmin in read-only mode for order status."""
        self.checkoutScreen = CheckoutScreenAdmin(self.userID, self.cartItems, read_only=True)
        self.checkoutScreen.show()
        self.close()

    def goToCheckout(self):
        """ Navigate to the second screen and pass cart details """
        if not self.cartItems:  # Check if the cart is empty
            QtWidgets.QMessageBox.warning(self, "Empty Cart", "Your cart is empty. Add items before proceeding to checkout.")
            return
        self.checkoutScreen = CheckoutScreenAdmin(self.userID, self.cartItems)
        self.checkoutScreen.show()
        self.close()

class CheckoutScreenAdmin(QtWidgets.QMainWindow):
    def __init__(self, userID, cartItems, read_only=False):
        super(CheckoutScreenAdmin, self).__init__()

        # Load the second UI (Order_Management)
        uic.loadUi('ui_files/Order_Management.ui', self)
        self.userID = userID
        self.cartItems = cartItems
        self.read_only = read_only
        # Connect buttons to their respective methods
        self.placeOrderButton.clicked.connect(self.placeOrder)
        self.cancelOrderButton.clicked.connect(self.cancelOrder)
        self.viewStatusButton.clicked.connect(self.viewStatus)
        self.backButton.clicked.connect(self.goBack)
        self.pushButton.clicked.connect(self.serveOrder)

        # Display selected items in the list widget
        if self.read_only:
            self.makeReadOnly()
        self.populateCartItems()

    def populateCartItems(self):
        """ Populate the list widget with cart items """
        self.listWidget.clear()
        for item_name, category, quantity, price in self.cartItems:
            self.listWidget.addItem(f"{item_name} ({category}) x{quantity} - {price}")

    def makeReadOnly(self):
        """Disable non-order-status functionalities."""
        self.placeOrderButton.setEnabled(False)
        self.lineEdit.setEnabled(False)  # Table number
        self.lineEdit_2.setEnabled(False)  # Special request
        self.radioButton.setEnabled(False)  # Cash option
        self.radioButton_2.setEnabled(False)  # Card option
        self.listWidget.setEnabled(False)  # Cart items list

    def get_selected_items(self):
        """ Retrieve selected items (with their quantity) from the cartItems list """
        selected_items = []
        for item_name, category, quantity, price in self.cartItems:
            selected_items.append((item_name, quantity, price))  # Add quantity and price to list
        return selected_items

    def placeOrder(self):
        """ Place an order using cart details """
        table_number = self.lineEdit.text()
        special_request = self.lineEdit_2.text()
        payment_type = None

        # Step 1: Check payment type
        if self.radioButton.isChecked():
            payment_type = 'Cash'
        elif self.radioButton_2.isChecked():
            payment_type = 'Card'
        else:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please select a payment type.")
            return

        # Step 2: Validate table number input
        if not table_number.isdigit():
            QtWidgets.QMessageBox.warning(self, "Input Error", "Table number must be numeric.")
            return

        # Step 3: Retrieve selected items and calculate total amount
        selected_items = self.get_selected_items()  # Retrieve the selected items list
        total_amount = 0
        for item_name, quantity, price in selected_items:
            total_amount += (int(price)*int(quantity))  # Calculate total by summing item prices

        # Step 4: Apply tax based on payment type
        if payment_type == 'Card':
            tax_rate = 0.12  # 12% tax for card payments
        else:  # 'Cash'
            tax_rate = 0.15  # 15% tax for cash payments

        tax_amount = total_amount * tax_rate
        total_with_tax = total_amount + tax_amount

        # Step 5: Insert transaction with calculated amount and tax
        try:
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()

            # Insert transaction into [Transaction] table with tax included
            cursor.execute("""
                INSERT INTO [Transaction] (StaffID, PaymentType, Amount, Tax, Date, Time, Type, InventoryID)
                OUTPUT INSERTED.id
                VALUES (?, ?, ?, ?, CONVERT(date, GETDATE()), CONVERT(time, GETDATE()), 'Order', 1);
            """, (self.userID, payment_type, total_amount, tax_rate*100))  # Include tax_amount
            transaction_id = cursor.fetchone()[0]  # Get the transaction ID

            # Step 6: Insert order into Orders table
            cursor.execute("""
                INSERT INTO Orders (Table_no, StaffID, TransactionID, Special_Request, Status, Date, Time)
                VALUES (?, ?, ?, ?, 'Preparing', CONVERT(date, GETDATE()), CONVERT(time, GETDATE()));
            """, (int(table_number), self.userID, transaction_id, special_request))

            conn.commit()

            # Step 7: Show success message with total amount (including tax)
            QtWidgets.QMessageBox.information(self, 
                "Order Placed", 
                f"Your order has been placed!\nTotal Amount (including tax): ${total_with_tax:.2f}\nTax: ${tax_amount:.2f}"
            )
            self.close()

        except pyodbc.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            conn.close()


    def cancelOrder(self):
        """ Cancel an order based on Order ID input """
        order_id = self.lineEdit_3.text().strip()
        if not order_id.isdigit():
            QtWidgets.QMessageBox.warning(self, "Input Error", "Order ID must be numeric.")
            return

        try:
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()

            # Check if the order exists and can be canceled
            cursor.execute("SELECT TransactionID, Status FROM Orders WHERE id = ?", (int(order_id),))
            result = cursor.fetchone()

            if result:
                transaction_id, status = result
                if status == 'Preparing':
                    cursor.execute("UPDATE Orders SET TransactionID = NULL, Status = 'Cancelled' WHERE id = ?", (int(order_id),))
                    cursor.execute("DELETE FROM [Transaction] WHERE id = ?", (transaction_id,))
                    conn.commit()
                    QtWidgets.QMessageBox.information(self, "Order Cancelled", "The order has been successfully cancelled.")
                else:
                    QtWidgets.QMessageBox.warning(self, "Cannot Cancel", "Served/Cancelled orders cannot be cancelled.")
            else:
                QtWidgets.QMessageBox.warning(self, "Order Not Found", "No order found with the provided ID.")
        except pyodbc.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def viewStatus(self):
        """ View the status of an order based on Order ID """
        order_id = self.lineEdit_3.text().strip()
        if not order_id.isdigit():
            QtWidgets.QMessageBox.warning(self, "Input Error", "Order ID must be numeric.")
            return

        try:
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()

            # Retrieve the status of the specified order
            cursor.execute("SELECT Status FROM Orders WHERE id = ?", (int(order_id),))
            result = cursor.fetchone()

            if result:
                QtWidgets.QMessageBox.information(self, "Order Status", f"The status of your order is: {result[0]}")
            else:
                QtWidgets.QMessageBox.warning(self, "Order Not Found", "No order found with the provided ID.")
        except pyodbc.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def serveOrder(self):
        """ Mark an order as served by updating its status """
        order_id = self.lineEdit_3.text().strip()
        if not order_id.isdigit():
            QtWidgets.QMessageBox.warning(self, "Input Error", "Order ID must be numeric.")
            return

        try:
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()

            # Step 1: Check if the order exists and fetch its current status
            cursor.execute("SELECT Status FROM Orders WHERE id = ?", (int(order_id),))
            result = cursor.fetchone()

            if result:
                status = result[0]
                if status == 'Preparing':
                    # Step 2: Update the status to 'Served'
                    cursor.execute("UPDATE Orders SET Status = 'Served' WHERE id = ?", (int(order_id),))
                    conn.commit()
                    QtWidgets.QMessageBox.information(self, "Order Served", "The order status has been Served.")
                elif status == 'Served':
                    QtWidgets.QMessageBox.information(self, "Already Served", "The order is already marked as 'Served'.")
                elif status == 'Cancelled':
                    QtWidgets.QMessageBox.warning(self, "Cannot Serve", "Cancelled Order.")
                else:
                    QtWidgets.QMessageBox.warning(self, "Invalid Status", f"Order cannot be served. Current status: {status}")
            else:
                QtWidgets.QMessageBox.warning(self, "Order Not Found", "No order found with the provided ID.")
        except pyodbc.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            conn.close()


    def goBack(self):
        """ Return to the order selection screen """
        self.previousScreen = OrderScreen(self.userID)
        self.previousScreen.show()
        self.close()

class TransactionScreen(QtWidgets.QMainWindow):
    def __init__(self, staff_id):
        self.userID = staff_id
        super(TransactionScreen, self).__init__()

        uic.loadUi('ui_files/TransactionView.ui', self)

        self.populate_table()

        self.addButton.clicked.connect(self.add)
        self.updateButton.clicked.connect(self.update)
        self.deleteButton.clicked.connect(self.delete)
        self.calculateButton.clicked.connect(self.calculate)
        self.backButton.clicked.connect(self.back)

    def populate_table(self):
        populate_query = """
            SELECT t.id AS TransactionID, t.Date AS TransactionDate, t.Time AS TransactionTime, t.Type AS TransactionType, CONCAT(s.Full_Name, ' ', s.Last_Name) AS StaffName, t.Amount AS TransactionAmount, t.PaymentType AS PaymentType, t.tax AS Tax
            FROM [Transaction] t
            JOIN Staff s ON t.StaffID = s.id;
        """
        cursor.execute(populate_query)
        data = cursor.fetchall()
        # taxPercentage = 13
        self.updated_data = []
        for record in data:
            amount = record[5]
            taxPercentage = record[7]
            total = math.ceil(amount * (1 + taxPercentage / 100))
            print(total, taxPercentage, amount)
            self.updated_data.append(tuple(record) + (total,))

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        for i, row in enumerate(self.updated_data):
            for j, value in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                self.tableWidget.setItem(i, j, item)

    def getSelectedRowValues(self):
        selected_row = self.tableWidget.currentRow()
        row_values = []
        for col in range(self.tableWidget.columnCount()):
            item = self.tableWidget.item(selected_row, col)
            if item is not None:
                row_values.append(item.text())
        return row_values

    def add(self):
        self.add_screen = AddTransactionScreen(self,self.userID)
        self.add_screen.show()

    def update(self):
        if self.tableWidget.selectedItems() != []:  # Check if no row is selected
            selected_rows = self.getSelectedRowValues()
            self.update_screen = UpdateTransactionScreen(selected_rows, self)
            self.update_screen.show()
        else:
            QMessageBox.warning(self, "Error", "Please select a transaction to update.")

    def delete(self):
        dlg = QtWidgets.QMessageBox.information(self,"Delete Transaction","Transaction successfully deleted!",QtWidgets.QMessageBox.StandardButton.Ok)

    def calculate(self):
        self.calculate_screen = ProfitLossScreen(self.dateEdit.date(), self.dateEdit_2.date())
        self.calculate_screen.show()

    def back(self):
        self.close()

class ReservationScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(ReservationScreen, self).__init__()

        uic.loadUi('ui_files/Reservation_Form_View.ui', self)

        self.backButton.clicked.connect(self.back)
        self.upcomingButton.clicked.connect(self.showUpcomingReservations)
        self.allButton.clicked.connect(self.showAllReservations)

        # Load reservation data when the screen is initialized
        self.loadReservationData()

    def showUpcomingReservations(self):
        """Show only upcoming reservations."""
        """Fetch reservation details and populate the table."""
        conn = pyodbc.connect(connection_string)  # Replace with your connection string
        cursor = conn.cursor()

        try:
            query = """
                SELECT 
                    r.id,
                    r.CustomerID,
                    concat(first_name, last_name),
                    r.Date,
                    r.Time,
                    r.Party_Size,
                    r.status
                FROM 
                    reservations r
                JOIN 
                    Customer c
                ON 
                    r.CustomerID = c.id
                WHERE
                    r.Date >= GETDATE();
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            # Populate the table with fetched data
            self.reservationTable.setRowCount(0)  # Clear existing rows

            for row_index, row_data in enumerate(rows):
                self.reservationTable.insertRow(row_index)
                for col_index, value in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    self.reservationTable.setItem(row_index, col_index, item)

        except pyodbc.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")

        finally:
            conn.close()

    def showAllReservations(self):
        """Show all reservations."""
        self.loadReservationData()

    def loadReservationData(self):
        """Fetch reservation details and populate the table."""
        conn = pyodbc.connect(connection_string)  # Replace with your connection string
        cursor = conn.cursor()

        try:
            query = """
                SELECT 
                    r.id,
                    r.CustomerID,
                    concat(first_name, last_name),
                    r.Date,
                    r.Time,
                    r.Party_Size,
                    r.status
                FROM 
                    reservations r
                JOIN 
                    Customer c
                ON 
                    r.CustomerID = c.id;
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            # Populate the table with fetched data
            self.reservationTable.setRowCount(0)  # Clear existing rows

            for row_index, row_data in enumerate(rows):
                self.reservationTable.insertRow(row_index)
                for col_index, value in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    self.reservationTable.setItem(row_index, col_index, item)

        except pyodbc.Error as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")

        finally:
            conn.close()

    def back(self):
        """Close the reservation screen."""
        self.close()

class StaffScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(StaffScreen, self).__init__()

        uic.loadUi('ui_files/staffManagment.ui', self)

        self.populate_table()

        self.addButton.clicked.connect(self.add)
        self.updateButton.clicked.connect(self.update)
        self.deleteButton.clicked.connect(self.delete)
        self.backButton.clicked.connect(self.back)

    def populate_table(self):
        populate_query = """
            SELECT id, CONCAT(Full_Name, ' ', Last_Name) AS Name, Position, Phone_Number, Email, Address, Joining_Date, Salary, Emergency_Contact, Status
            FROM Staff;
        """
        cursor.execute(populate_query)
        data = cursor.fetchall()

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                self.tableWidget.setItem(i, j, item)

    def add(self):
        self.add_screen = StaffAddScreen(self)
        self.add_screen.show()

    def getSelectedRowValues(self):
        selected_row = self.tableWidget.currentRow()
        row_values = []
        for col in range(self.tableWidget.columnCount()):
            item = self.tableWidget.item(selected_row, col)
            if item is not None:
                row_values.append(item.text())
        return row_values
    
    def update(self):
        if self.tableWidget.selectedItems() != []:  # Check if a row is selected
            selected_rows = self.getSelectedRowValues()
            self.update_screen = StaffUpdateScreen(selected_rows, self)
            self.update_screen.show()
        else:
            QMessageBox.warning(self, "Error", "Please select a staff member to update.")

    def confirm_deletion(self):
        # Create a QMessageBox instance
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Staff Deletion")
        msg_box.setText("Are you sure you want to delete the staff records?")
        
        # Add custom buttons
        delete_button = msg_box.addButton("Delete Records", QMessageBox.ButtonRole.AcceptRole)
        keep_button = msg_box.addButton("Keep Records", QMessageBox.ButtonRole.RejectRole)

        # Execute and check which button was pressed
        msg_box.exec()

        if msg_box.clickedButton() == delete_button:
            return True
        
        elif msg_box.clickedButton() == keep_button:
            return False

    def delete(self):
        if self.tableWidget.selectedItems() != []:  # Check if a row is selected
            selected_rows = self.getSelectedRowValues()
            confirm = self.confirm_deletion()
            if confirm:
                update_query = """
                    UPDATE Orders
                    SET StaffID = NULL
                    WHERE StaffID = ?;
                """
                cursor.execute(update_query, (selected_rows[0]))
                # connection.commit()
                update_query = """
                    UPDATE [Transaction]
                    SET StaffID = NULL
                    WHERE StaffID = ?;
                """
                cursor.execute(update_query, (selected_rows[0]))
                # connection.commit()
                update_query = """
                    UPDATE MenuItem
                    SET StaffID = NULL
                    WHERE StaffID = ?;
                """
                cursor.execute(update_query, (selected_rows[0]))
                # connection.commit()
                update_query = """
                    UPDATE Ingredients
                    SET CheckerStaffID = NULL
                    WHERE CheckerStaffID = ?;
                """
                cursor.execute(update_query, (selected_rows[0]))
                # connection.commit()
                delete_query = "DELETE FROM Staff WHERE id = ?"
                cursor.execute(delete_query, (selected_rows[0]))
                connection.commit()
                self.populate_table()
                dlg = QtWidgets.QMessageBox.information(self,"Staff Deleted","Staff successfully deleted!",QtWidgets.QMessageBox.StandardButton.Ok)
            else:
                query = "UPDATE Staff SET Status = 'Terminated' WHERE id = ?"
                cursor.execute(query, (selected_rows[0]))
                connection.commit()
                self.populate_table()
                dlg = QtWidgets.QMessageBox.information(self,"Staff Terminated","Staff successfully terminated!",QtWidgets.QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.warning(self, "Error", "Please select a staff member to remove.")

    def back(self):
        self.close()

class StaffAddScreen(QtWidgets.QMainWindow):
    def __init__(self, staff):
        super(StaffAddScreen, self).__init__()

        uic.loadUi('ui_files/StaffAdd.ui', self)

        self.staffscreen = staff

        self.addStaffButton.clicked.connect(self.addStaff)
        self.backButton.clicked.connect(self.back)

    def addStaff(self):
        if self.lineEdit_3.text() == "" or self.lineEdit_4.text() == "" or self.lineEdit_5.text() == "" or self.lineEdit_6.text() == "" or self.lineEdit.text() == "" or self.lineEdit_2.text() == "" or self.lineEdit_7.text() == "" or self.lineEdit_8.text() == "" or self.lineEdit_9.text() == "" or self.lineEdit_10.text() == "" or self.dateEdit.text() == "":
            dlg = QtWidgets.QMessageBox.warning(self,"Missing Fields","Fill all fields to add an employee!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        elif self.dateEdit.date() > QDate.currentDate():
            dlg = QtWidgets.QMessageBox.warning(self,"Invalid Date","Invalid date!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        
        fname = self.lineEdit_7.text()
        lname = self.lineEdit_3.text()
        position = self.lineEdit_4.text()
        phone = self.lineEdit_5.text()
        try:
            phone = int(phone)
        except ValueError:
            dlg = QtWidgets.QMessageBox.warning(self,"Input Error","Phone number should be a number!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        
        email = self.lineEdit_6.text()
        address = self.lineEdit.text()
        emergency_contact = self.lineEdit_10.text()
        try:
            emergency_contact = int(emergency_contact)
        except ValueError:
            dlg = QtWidgets.QMessageBox.warning(self,"Input Error","Emergency contact should be a number!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        
        joining_date = self.dateEdit.date().toString("yyyy-MM-dd")
        salary = self.lineEdit_2.text()
        try:
            salary = int(salary)
        except ValueError:
            dlg = QtWidgets.QMessageBox.warning(self,"Input Error","Salary should be a number!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        
        username = self.lineEdit_8.text()
        password = self.lineEdit_9.text()
            
        insert_query = """
            INSERT INTO Staff (Full_Name, Last_Name, Position, Phone_Number, Email, username, Password, Address, Emergency_Contact, Joining_Date, Salary, Status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Working')
        """
        cursor.execute(insert_query, (fname, lname, position, phone, email, username, password, address, emergency_contact, joining_date, salary))
        connection.commit()

        dlg = QtWidgets.QMessageBox.information(self,"Staff added","Staff successfully added!",QtWidgets.QMessageBox.StandardButton.Ok)
        self.staffscreen.populate_table()
        self.back()

    def back(self):
        self.close()

class StaffUpdateScreen(QtWidgets.QMainWindow):
    def __init__(self, data, staff):
        super(StaffUpdateScreen, self).__init__()

        uic.loadUi('ui_files/StaffUpdate.ui', self)

        self.staffscreen = staff

        self.lineEdit_7.setText(data[0])
        self.lineEdit_7.setReadOnly(True)
        self.lineEdit_3.setText(data[1])
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_4.setText(data[2])
        self.lineEdit_5.setText(data[3])
        self.lineEdit_6.setText(data[4])
        self.lineEdit.setText(data[5])
        self.dateEdit.setDate(QDate.fromString(data[6], "yyyy-MM-dd"))
        self.lineEdit_2.setText(data[7])
        self.lineEdit_10.setText(data[8])
        self.lineEdit_11.setText(data[9])

        query = "SELECT username, Password FROM Staff WHERE id = ?"
        cursor.execute(query, (data[0]))
        username, password = cursor.fetchone()
        self.lineEdit_8.setText(username)
        self.lineEdit_9.setText(password)

        self.updateStaffButton.clicked.connect(self.updateStaff)
        self.backButton.clicked.connect(self.back)

    def updateStaff(self):

        if self.lineEdit_3.text() == "" or self.lineEdit_4.text() == "" or self.lineEdit_5.text() == "" or self.lineEdit_6.text() == "" or self.lineEdit.text() == "" or self.lineEdit_2.text() == "" or self.lineEdit_7.text() == "" or self.lineEdit_8.text() == "" or self.lineEdit_9.text() == "" or self.lineEdit_10.text() == "" or self.dateEdit.text() == "":
            dlg = QtWidgets.QMessageBox.warning(self,"Missing Fields","Fill all fields to add an employee!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        elif self.dateEdit.date() > QDate.currentDate():
            dlg = QtWidgets.QMessageBox.warning(self,"Invalid Date","Invalid date!",QtWidgets.QMessageBox.StandardButton.Ok)
            return

        # update the staff table based on the records from the fields
        id = self.lineEdit_7.text()
        position = self.lineEdit_4.text()
        phone = self.lineEdit_5.text()
        try:
            phone = int(phone)
        except ValueError:
            dlg = QtWidgets.QMessageBox.warning(self,"Input Error","Phone number should be a number!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        
        email = self.lineEdit_6.text()
        address = self.lineEdit.text()
        emergency_contact = self.lineEdit_10.text()
        try:
            emergency_contact = int(emergency_contact)
        except ValueError:
            dlg = QtWidgets.QMessageBox.warning(self,"Input Error","Emergency contact should be a number!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        
        joining_date = self.dateEdit.date().toString("yyyy-MM-dd")
        salary = self.lineEdit_2.text()
        try:
            salary = int(salary)
        except ValueError:
            dlg = QtWidgets.QMessageBox.warning(self,"Input Error","Salary should be a number!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        
        status = self.lineEdit_11.text()
        username = self.lineEdit_8.text()
        password = self.lineEdit_9.text()

        update_query = """
        UPDATE Staff
        SET Position = ?, Phone_Number = ?, Email = ?, username = ?, Password = ?, Address = ?, Joining_Date = ?, Salary = ?
        WHERE id = ?
        """
        cursor.execute(update_query, (position, phone, email, username, password, address, joining_date, salary, id))
        connection.commit()
        dlg = QtWidgets.QMessageBox.information(self,"Staff updated","Staff record updated successfully!",QtWidgets.QMessageBox.StandardButton.Ok)
        self.staffscreen.populate_table()
        self.back()

    def back(self):
        self.close()

class editItemScreen(QtWidgets.QMainWindow): # DONE #
    def __init__(self, data, menu):
        super(editItemScreen, self).__init__()

        uic.loadUi('ui_files/menuItemUpdate.ui', self)

        self.menuscreen = menu

        self.item_id = data[0]
        self.item_name = data[1]
        self.item_category = data[2]
        self.item_price = data[3]
        self.item_discontinuted = data[4]

        self.lineEdit.setText(self.item_name)
        self.lineEdit_2.setText(self.item_price)
        print(self.item_discontinuted)
        if(self.item_discontinuted == "False"):
            self.comboBox_2.setCurrentIndex(0)
        else:
            self.comboBox_2.setCurrentIndex(1)

        find_description = "SELECT Description FROM MenuItem WHERE ID = ?"
        cursor.execute(find_description, (self.item_id))
        self.description = cursor.fetchone()[0]
        self.textEdit.setText(self.description)

        category_query = "SELECT DISTINCT Category FROM MenuItem"
        cursor.execute(category_query)
        categories = cursor.fetchall()
        self.comboBox.clear()
        self.comboBox.addItem("<Not Selected>")
        for c in categories:
            self.comboBox.addItem(c[0])

        # category_query1 = "SELECT Category FROM MenuItem WHERE ID = ?"
        # cursor.execute(category_query1, (self.item_id))
        # category = cursor.fetchone()[0]
        # self.comboBox.setCurrentText(category)
        self.comboBox.setCurrentText(self.item_category)

        self.backButton.clicked.connect(self.back)
        self.updateItemButton.clicked.connect(self.updateItem)

    def back(self):
        self.close()

    def updateItem(self):
        if self.lineEdit.text() == "" or self.lineEdit_2.text() == "" or self.textEdit.toPlainText() == "":
            dlg = QtWidgets.QMessageBox.warning(self,"Missing Fields Failure","Fill all fields to update item!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
            
        elif self.lineEdit.text() == self.item_name and self.lineEdit_2.text() == self.item_price and self.textEdit.toPlainText() == self.description and self.comboBox_2.currentIndex() == self.item_discontinuted and self.comboBox.currentText() == self.item_category:
            dlg = QtWidgets.QMessageBox.warning(self,"No Changes Made","No changes made to item!",QtWidgets.QMessageBox.StandardButton.Ok)
            return

        name = self.lineEdit.text()
        category = self.comboBox.currentText()
        price = self.lineEdit_2.text()
        description = self.textEdit.toPlainText()
        discontinued = 1
        if(self.comboBox_2.currentText() == "Availabe to order"):
            discontinued = 0
        else:
            discontinued = 1
        update_query = "UPDATE MenuItem SET Name = ?, Category = ?, Price = ?, Description = ?, Discontinued = ? WHERE ID = ?" 
        cursor.execute(update_query, (name, category, price, description, discontinued, self.item_id))
        connection.commit()

        self.menuscreen.populate_table()

        dlg = QtWidgets.QMessageBox.information(self,"Menu Item Update","Menu Item successfully updated!",QtWidgets.QMessageBox.StandardButton.Ok)

class ViewStatusOrder(QtWidgets.QMainWindow): # ABDULLAH DOING #
    def __init__(self):
        super(ViewStatusOrder, self).__init__()

        uic.loadUi('ui_files/Order_Status.ui', self)

        self.backButton.clicked.connect(self.back)

    def back(self):
        self.close()

class AddTransactionScreen(QtWidgets.QMainWindow):
    def __init__(self, transaction, userID):
        super(AddTransactionScreen, self).__init__()

        uic.loadUi('ui_files/TransactionAdd.ui', self)

        self.transaction = transaction
        self.userID = userID

        self.lineEdit_11.setText("Auto Generated")
        self.lineEdit_11.setReadOnly(True)

        self.lineEdit_14.textChanged.connect(self.calculate_total)
        self.lineEdit_16.textChanged.connect(self.calculate_total)

        self.addTransactionButton.clicked.connect(self.addTransaction)
        self.backButton.clicked.connect(self.back)

    def addTransaction(self):
        if self.dateEdit.text() == "" or self.timeEdit.text() == "" or self.lineEdit_12.text() == "" or self.lineEdit_13.text() == "" or self.lineEdit_14.text() == "" or self.lineEdit_15.text() == "" or self.lineEdit_16.text() == "" or self.lineEdit_17.text() == "":
            dlg = QtWidgets.QMessageBox.warning(self,"Missing Fields Failure","Fill all fields to add transaction!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        elif self.dateEdit.date() > QDate.currentDate() or self.timeEdit.time() > QTime.currentTime():
            dlg = QtWidgets.QMessageBox.warning(self,"Invalid Date/Time","Invalid date/time for transaction!",QtWidgets.QMessageBox.StandardButton.Ok)
            return

        date = self.dateEdit.text()
        time = self.timeEdit.text()
        ttype = self.lineEdit_12.text()
        staff = self.lineEdit_13.text()
        amount = self.lineEdit_14.text()
        payment = self.lineEdit_15.text()
        tax = self.lineEdit_16.text()
        total = self.lineEdit_17.text()
        inventoryID = 0
        if(ttype == "Inventory"):
            inventoryID = 1
        if(inventoryID == 1):
            insert_query = "INSERT INTO [Transaction](Date, Time, Type, StaffID, Amount, PaymentType, InventoryID, Tax) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(insert_query, (date, time, ttype, self.userID, amount, payment,inventoryID, tax))
        else:
            insert_query = "INSERT INTO [Transaction](Date, Time, Type, StaffID, Amount, PaymentType, Tax) VALUES (?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(insert_query, (date, time, ttype, self.userID, amount, payment, tax))
        connection.commit()

        self.transaction.populate_table()

        dlg = QtWidgets.QMessageBox.information(self,"Transaction added","Transaction successfully added!",QtWidgets.QMessageBox.StandardButton.Ok)
    
    def calculate_total(self):
        try:
            amount = float(self.lineEdit_14.text())
            tax = float(self.lineEdit_16.text())
            total = math.ceil(amount * (1 + (tax/100)))
            self.lineEdit_17.setText(str(total))
        except ValueError:
            self.lineEdit_17.setText("")

    def back(self):
        self.close()

class UpdateTransactionScreen(QtWidgets.QMainWindow):
    def __init__(self, data, transaction):
        super(UpdateTransactionScreen, self).__init__()

        uic.loadUi('ui_files/TransactionUpdate.ui', self)

        self.transaction = transaction

        self.t_id = data[0]
        self.t_date = data[1]
        self.t_time = data[2]
        self.t_type = data[3]
        self.t_staff = data[4]
        self.t_amount = data[5]
        self.t_payment = data[6]
        self.t_tax = data[7]
        self.t_total = data[8]

        self.lineEdit_11.setText(self.t_id)
        self.lineEdit_11.setReadOnly(True)
        self.dateEdit.setDate(QDate.fromString(self.t_date, "yyyy-MM-dd"))
        self.timeEdit.setTime(QTime.fromString(self.t_time, "HH:mm:ss"))
        self.lineEdit_6.setText(self.t_type)
        self.lineEdit_7.setText(self.t_staff)
        self.lineEdit_7.setReadOnly(True)
        self.lineEdit_2.setText(str(self.t_amount))
        self.lineEdit_3.setText(self.t_payment)
        self.lineEdit_4.setText(str(self.t_tax))
        self.lineEdit_9.setText(str(self.t_total))

        self.lineEdit_4.textChanged.connect(self.calculate_total)
        self.lineEdit_2.textChanged.connect(self.calculate_total)

        self.updateTransactionButton.clicked.connect(self.updateTransaction)
        self.backButton.clicked.connect(self.back)

    def updateTransaction(self):
        if self.dateEdit.text() == "" or self.timeEdit.text() == "" or self.lineEdit_6.text() == "" or self.lineEdit_7.text() == "" or self.lineEdit_2.text() == "" or self.lineEdit_3.text() == "" or self.lineEdit_4.text() == "" or self.lineEdit_9.text() == "":
            dlg = QtWidgets.QMessageBox.warning(self,"Missing Fields Failure","Fill all fields to update transaction!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        elif self.dateEdit.text() == self.t_date and self.timeEdit.text() == self.t_time and self.lineEdit_6.text() == self.t_type and self.lineEdit_7.text() == self.t_staff and self.lineEdit_2.text() == self.t_amount and self.lineEdit_3.text() == self.t_payment and self.lineEdit_4.text() == self.t_tax and self.lineEdit_9.text() == self.t_total:
            dlg = QtWidgets.QMessageBox.warning(self,"No Changes Made","No changes made to transaction!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        elif self.dateEdit.date() > QDate.currentDate() or self.timeEdit.time() > QTime.currentTime():
            dlg = QtWidgets.QMessageBox.warning(self,"Invalid Date/Time","Invalid date/time for transaction!",QtWidgets.QMessageBox.StandardButton.Ok)

        tid = self.lineEdit_11.text()
        date = self.dateEdit.text()
        time = self.timeEdit.text()
        ttype = self.lineEdit_6.text()

        find_id = "SELECT id FROM Staff WHERE CONCAT(Full_Name, ' ', Last_Name) = ?"
        staff = self.lineEdit_7.text()
        cursor.execute(find_id, (staff))
        staff = cursor.fetchone()[0]

        amount = self.lineEdit_2.text()
        payment = self.lineEdit_3.text()
        tax = self.lineEdit_4.text()
        total = self.lineEdit_9.text()

        update_query = "UPDATE [Transaction] SET Date = ?, Time = ?, Type = ?, StaffID = ?, Tax = ?, Amount = ?, PaymentType = ? WHERE id = ?"
        cursor.execute(update_query, (date, time, ttype, staff, tax, amount, payment, tid))
        connection.commit()

        self.transaction.populate_table()

        dlg = QtWidgets.QMessageBox.information(self,"Transaction updated","Transaction successfully updated!",QtWidgets.QMessageBox.StandardButton.Ok)
    
    def calculate_total(self):
        try:
            amount = float(self.lineEdit_2.text())
            tax = float(self.lineEdit_4.text())
            total = math.ceil(amount * (1 + (tax/100)))
            self.lineEdit_9.setText(str(total))
        except ValueError:
            self.lineEdit_9.setText("")

    def back(self):
        self.close()

class ProfitLossScreen(QtWidgets.QMainWindow):
    def __init__(self, initialDate, endDate):
        super(ProfitLossScreen, self).__init__()

        self.startDate = initialDate
        self.endDate = endDate

        uic.loadUi('ui_files/ProfitLossScreen.ui', self)

        self.printButton.clicked.connect(self.printTransaction)
        self.backButton.clicked.connect(self.back)
        self.populate_table()
        self.calcButton.clicked.connect(self.calculate_table)

    def populate_table(self):
        
        totalRevenue_query = "SELECT SUM(Amount+(Amount * (Tax/100))) FROM [Transaction] WHERE Date BETWEEN ? AND ?"
        cursor.execute(totalRevenue_query, (self.startDate.toString("yyyy-MM-dd"), self.endDate.toString("yyyy-MM-dd")))
        totalRevenue = cursor.fetchone()[0]
        if(totalRevenue == None):
            totalRevenue = 0
        self.lineEdit.setText(str(totalRevenue))

        advertising_query = "SELECT SUM(Amount+(Amount * (Tax/100))) FROM [Transaction] where Type = 'Advertising' AND Date BETWEEN ? AND ?"
        cursor.execute(advertising_query, (self.startDate.toString("yyyy-MM-dd"), self.endDate.toString("yyyy-MM-dd")))
        advertising = cursor.fetchone()[0]
        if(advertising == None):
            advertising = 0
        self.lineEdit_6.setText(str(advertising))

        utility_query = "SELECT SUM(Amount+(Amount * (Tax/100))) FROM [Transaction] where Type = 'Utility' AND Date BETWEEN ? AND ?"
        cursor.execute(utility_query, (self.startDate.toString("yyyy-MM-dd"), self.endDate.toString("yyyy-MM-dd")))
        utility = cursor.fetchone()[0]
        if(utility == None):
            utility = 0
        self.lineEdit_7.setText(str(utility))

        repairs_maintenance_query = "SELECT SUM(Amount+(Amount * (Tax/100))) FROM [Transaction] where (Type = 'Repairs' OR Type = 'Maintenance') AND Date BETWEEN ? AND ?"
        cursor.execute(repairs_maintenance_query, (self.startDate.toString("yyyy-MM-dd"), self.endDate.toString("yyyy-MM-dd")))
        repairs_maintenance = cursor.fetchone()[0]
        if(repairs_maintenance == None):
            repairs_maintenance = 0
        self.lineEdit_2.setText(str(repairs_maintenance))
    
        wages_shipment_query = "SELECT SUM(Amount+(Amount * (Tax/100))) FROM [Transaction] where (Type = 'Wages' OR Type = 'Shipment') AND Date BETWEEN ? AND ?"
        cursor.execute(wages_shipment_query, (self.startDate.toString("yyyy-MM-dd"), self.endDate.toString("yyyy-MM-dd")))
        wages_shipment = cursor.fetchone()[0]
        if(wages_shipment == None):
            wages_shipment = 0
        self.lineEdit_3.setText(str(wages_shipment))

    def calculate_table(self):
        if(self.lineEdit_4.text() == "" or self.lineEdit_8.text() == "" or self.lineEdit_10.text() == ""):
            dlg = QtWidgets.QMessageBox.warning(self,"Missing Fields Failure","Fill all fields to calculate profit/loss!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
        profit = float(self.lineEdit_8.text())
        tax = float(self.lineEdit_10.text())
        totalRevenue = float(self.lineEdit.text())
        totalExpenses = totalRevenue - (totalRevenue * (profit/100)) + float(self.lineEdit_4.text())
        self.lineEdit_5.setText(str(totalExpenses))

        gross_profit = totalRevenue - totalExpenses
        self.lineEdit_11.setText(str(gross_profit))

        net_profit = gross_profit - (gross_profit * (tax/100))
        self.lineEdit_9.setText(str(net_profit))

    def printTransaction(self):
        dlg = QtWidgets.QMessageBox.information(self,"Transaction print","Transaction successfully printed!",QtWidgets.QMessageBox.StandardButton.Ok)

    def back(self):
        self.close()

# Create an instance of QtWidgets.QApplication
app = QtWidgets.QApplication(sys.argv)
window = UI() # Create an instance of our class
app.exec() # Start the application