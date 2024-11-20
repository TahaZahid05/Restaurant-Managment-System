import sys
from PyQt6 import QtCore, QtWidgets, uic
from datetime import datetime
from validate_email import validate_email
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIntValidator
import pyodbc
import math

server = 'TAHA\\SQLSERVER1'
database = 'Project'  # Name of your Northwind database
use_windows_authentication = True  # Set to True to use Windows Authentication
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

    def register(self):
        self.register_user = registerUser()
        self.register_user.show()

    def login(self):
        checking_query_customer = "Select Email, password, id from Customer"
        checking_query_staff = "Select Email, Password from Staff"
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
                    self.admin_screen = adminScreen()
                    self.admin_screen.show()
                    return
                
            dlg = QtWidgets.QMessageBox.warning(self,"Login Failure","No account with the following email address and password exist!",QtWidgets.QMessageBox.StandardButton.Ok)

    def guestLogin(self):
        self.guest_user_screen = GuestScreen()
        self.guest_user_screen.show()

    def exitLogin(self):
        self.close()




class registerUser(QtWidgets.QMainWindow):
    def __init__(self):
        super(registerUser, self).__init__()

        uic.loadUi('ui_files/User_Registration.ui', self)
        self.salaryLine.setEnabled(False)
        self.roleBox.setEnabled(False)
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
        else:
            self.salaryLine.setEnabled(True)
            self.roleBox.setEnabled(True)
            self.roleBox.addItems(["Manager","Chef","Waiter","Host","Sous Chef"])
    
    def registering(self):
        if (self.firstName.text() == "" or self.lastName.text() == "" or self.emailAddress.text() == "" or self.userName.text() == "" or self.userPass.text() == "" or self.passConfirm.text() == "" or self.addressBox.toPlainText() == "" or self.phoneLine.text() == "" or (self.salaryLine.text() == "" and self.roleSelect.currentText() == "Staff")):
            dlg = QtWidgets.QMessageBox.warning(self,"Missing Fields Failure","Fill all fields to register!",QtWidgets.QMessageBox.StandardButton.Ok)
        elif (not(validate_email(self.emailAddress.text()))):
            dlg = QtWidgets.QMessageBox.warning(self,"Invalid Email Address","Email address is invalid!",QtWidgets.QMessageBox.StandardButton.Ok)
        elif (self.userPass.text() != self.passConfirm.text()):
            dlg = QtWidgets.QMessageBox.warning(self,"Password Confirmation Failure","Confirm Password doesn't have the same password!",QtWidgets.QMessageBox.StandardButton.Ok)
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
                        ([First_Name],[Last_Name],[Email],[username],[Password],[Address],[Phone_Number],[Position],[Salary])
                        VALUES (?,?,?,?,?,?,?,?,?)
                    """
                    data = (
                        self.firstName.text(),self.lastName.text(),self.emailAddress.text(),self.userName.text(),self.userPass.text(),self.addressBox.toPlainText(),self.phoneLine.text(),self.roleBox.currentText(),self.salaryLine.text()
                    )
                    cursor.execute(insert_query,data)
                else:
                    insert_query = """
                        INSERT INTO Customer
                        ([First_Name],[Last_Name],[Email],[username],[Password],[Address],[Phone_number])
                        VALUES (?,?,?,?,?,?,?)
                    """
                    data = (
                        self.firstName.text(),self.lastName.text(),self.emailAddress.text(),self.userName.text(),self.userPass.text(),self.addressBox.toPlainText(),self.phoneLine.text()
                    )
                    cursor.execute(insert_query,data)
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

        self.load_user_details()

        self.newAddressButton.clicked.connect(self.newAddress)
        self.applyButton.clicked.connect(self.applyChanges)
        self.deleteAddressButton.clicked.connect(self.deleteAddress)
        self.backButton.clicked.connect(self.back)

    def load_user_details(self):
        autofill_query = "Select First_name, Last_name, Email, username, password, Phone_number from Customer where id = ?"
        cursor.execute(autofill_query,(self.userID))
        for row in cursor.fetchall():
            self.firstName.setText(row[0])
            self.lastName.setText(row[1])
            self.emailAddress.setText(row[2])
            self.userName.setText(row[3])
            self.userPass.setText(row[4])
            self.passConfirm.setText(row[4])
            self.phoneNum.setText(row[5])

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
        if (self.firstName.text() == "" or self.lastName.text() == "" or self.emailAddress.text() == "" or self.userName.text() == "" or self.userPass.text() == "" or self.passConfirm.text() == "" or self.phoneNum.text() == ""):
            dlg = QtWidgets.QMessageBox.warning(self,"Missing Fields Failure","Fill all fields to apply changes!",QtWidgets.QMessageBox.StandardButton.Ok)
        elif (not(validate_email(self.emailAddress.text()))):
            dlg = QtWidgets.QMessageBox.warning(self,"Invalid Email Address","Email address is invalid!",QtWidgets.QMessageBox.StandardButton.Ok)
        elif (self.userPass.text() != self.passConfirm.text()):
            dlg = QtWidgets.QMessageBox.warning(self,"Password Confirmation Failure","Confirm Password doesn't have the same password!",QtWidgets.QMessageBox.StandardButton.Ok)
        else:
            update_query = """
                UPDATE Customer
                SET First_name = ?, Last_name = ?, Email = ?, username = ?, Password = ?, Phone_number = ?
                WHERE id = ?
            """
            data = (self.firstName.text(),self.lastName.text(),self.emailAddress.text(),self.userName.text(),self.userPass.text(),self.phoneNum.text(),self.userID)
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
    def __init__(self):
        super(GuestScreen, self).__init__()

        uic.loadUi('ui_files/GuestScreen.ui', self)

        self.onlineOrderButton.clicked.connect(self.onlineOrderScreen)
        self.trackOrderButton.clicked.connect(self.trackOrder)

    def onlineOrderScreen(self):
        self.online_order_screen = onlineOrder()
        self.online_order_screen.show()

    def trackOrder(self):
        self.trackorder_screen = trackOrderScreen()
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

        uic.loadUi('ui_files/Order_ItemSelect.ui', self)

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
        self.cartTable.removeRow(selected_item)

    def populate_menu_table(self):
        self.menuTable.clear()
        populate_menu_query = "Select Name, Category, 1 AS [People Per Serving], Price from  MenuItem"
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
        populate_menu_query = "Select Name, Category, 1 AS [People Per Serving], Price from  MenuItem where Name like ? AND Category LIKE ?"
        cursor.execute(populate_menu_query,(f"%{self.itemNameLine.text()}%"),f"%{self.categoryBox.currentText()}%")
        stringArray = ["Name","Category","People Per Serving","Price"]
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
        item_price = self.menuTable.item(selected_row, 3).text()
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


        self.cartTable = cartTable
        self.userID = userID
        self.totalAmountInt = 0
        self.address = ""

        self.deliveryCharges.setText("500")

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
        else:
            self.cardNumber.setEnabled(True)
            self.cvcNumber.setEnabled(True)
            self.expiryDate.setEnabled(True)
            self.cardHolderName.setEnabled(True)

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

        self.totalAmount.setText(str(self.totalAmountInt + 500))

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
            INSERT INTO [Transaction]([Date],[Time],[Type],[PaymentType],[Amount])
            OUTPUT INSERTED.ID
            VALUES (?,?,?,?,?)
        """
        date = str(datetime.today().date())
        time = str(datetime.today().time())
        self.paymentType = ""
        if(self.cashButton.isChecked()):
            self.paymentType = "Cash"
        elif (self.cardButton.isChecked()):
            self.paymentType = "Card"
        print(self.paymentType)
        data = (date,time,"Order",self.paymentType,int(self.totalAmountInt + 500))
        cursor.execute(insert_transaction_query,data)
        print("yes")

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
        print("yes")
        connection.commit()
        print("yes")

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
        cancel_query = "Delete from Reservations where id = ?"
        cursor.execute(cancel_query,(self.reservationComboBox.currentText()))
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
                SELECT Amount from [Transaction] where id = (Select TransactionID from Orders where id = ?)
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
        totalAmount = 0
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
        print("yes")
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.itemTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.itemTable.setItem(row_index, col_index, item)
            self.itemTable.setItem(row_index, 3, QTableWidgetItem(str(float(row_data[1]) * int(row_data[2]))))
            totalAmount += float(row_data[1]) * int(row_data[2])
        
        self.deliveryCharges.setText("500")
        self.totalAmount.setText(str(totalAmount + 500))

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
        self.totalAmount.setEnabled(False)
        self.deliveryCharges.setEnabled(False)
        self.itemTable.setEnabled(False)
        self.cashButton.setEnabled(False)
        self.cardButton.setEnabled(False)






    def back(self):
        self.close()

class adminScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(adminScreen, self).__init__()

        uic.loadUi('ui_files/AdminScreen.ui', self)

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
        self.bill_screen = billScreen()
        self.bill_screen.show()

    def viewFeedback(self):
        self.feedback_screen = FeedbackScreen()
        self.feedback_screen.show()

    def showInventory(self):
        self.inventory_screen = InventoryScreen()
        self.inventory_screen.show()

    def showMenu(self):
        self.menu_screen = MenuScreen()
        self.menu_screen.show()

    def showOrder(self):
        self.order_screen = OrderScreen()
        self.order_screen.show()

    def showTransaction(self):
        self.transaction_screen = TransactionScreen()
        self.transaction_screen.show()

    def showReservations(self):
        self.reservation_screen = ReservationScreen()
        self.reservation_screen.show()

    def showStaff(self):
        self.staff_screen = StaffScreen()
        self.staff_screen.show()

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
        
        # Setting Order ID
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setText(data[0])

        # Settting payment type

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

        self.lineEdit_6.setReadOnly(True)
        self.lineEdit_5.textChanged.connect(self.calculate_total)

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
            SELECT o.id, o.StaffID, f.Rating
            FROM Feedback f
            JOIN Orders o ON f.OrderID = o.id;
        """
        cursor.execute(populate_query)
        data = cursor.fetchall()
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.tableWidget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.populate_table(data)

        self.backButton.clicked.connect(self.back)
    
    def populate_table(self, data):
        self.tableWidget.setRowCount(len(data))

        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                self.tableWidget.setItem(i, j, item)

    def back(self):
        self.close()

class InventoryScreen(QtWidgets.QMainWindow): # ABDULLAH DOING #
    def __init__(self):
        super(InventoryScreen, self).__init__()

        uic.loadUi('ui_files/InventoryManagment.ui', self)

        self.addButton.clicked.connect(self.newItem)
        self.updateButton.clicked.connect(self.updateItem)
        self.deleteButton.clicked.connect(self.deleteItem)
        self.backButton.clicked.connect(self.back)

    def newItem(self):
        self.new_item_screen = AddItemScreen()
        self.new_item_screen.show()

    def updateItem(self):
        self.update_item_screen = UpdateItemScreen()
        self.update_item_screen.show()

    def deleteItem(self):
        dlg = QtWidgets.QMessageBox.information(self,"Item Deleted","Item successfully deleted!",QtWidgets.QMessageBox.StandardButton.Ok)

    def back(self):
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
        populate_menu_query = "SELECT ID, Name, Category, Price FROM MenuItem"
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
        add_query = "INSERT INTO MenuItem(Name, Category, Price, Description) VALUES (?, ?, ?, ?)"
        name = self.lineEdit.text()
        category = self.comboBox.currentText()
        price = self.lineEdit_2.text()
        description = self.textEdit.toPlainText()
        cursor.execute(add_query, (name, category, price, description))
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
        if self.tableWidget.selectedItems() != []:  # Check if no row is selected
            selected_rows = self.getSelectedRowValues()
        else:
            QMessageBox.warning(self, "Error", "Please select an item to remove.")

        item_id = selected_rows[0]
        delete_query = "DELETE FROM MenuItem WHERE ID = ?"
        cursor.execute(delete_query, (item_id))
        connection.commit()

        self.populate_table()

        dlg = QtWidgets.QMessageBox.information(self,"Menu Item Deleted","Menu Item successfully deleted!",QtWidgets.QMessageBox.StandardButton.Ok)

class OrderScreen(QtWidgets.QMainWindow): # ABDULLAH DOING #
    def __init__(self):
        super(OrderScreen, self).__init__()

        uic.loadUi('ui_files/Order_Management.ui', self)

        self.placeOrderButton.clicked.connect(self.placeOrder)
        self.viewStatusButton.clicked.connect(self.viewStatus)
        self.cancelOrderButton.clicked.connect(self.cancelOrder)
        self.backButton.clicked.connect(self.back)

    def placeOrder(self):
        dlg = QtWidgets.QMessageBox.information(self,"Order Placed","Order successfully place!",QtWidgets.QMessageBox.StandardButton.Ok)

    def viewStatus(self):
        self.view_status_screen = ViewStatusOrder()
        self.view_status_screen.show()

    def cancelOrder(self):
        dlg = QtWidgets.QMessageBox.information(self,"Order Canceled","Order successfully cancelled!",QtWidgets.QMessageBox.StandardButton.Ok)

    def back(self):
        self.close()

class TransactionScreen(QtWidgets.QMainWindow):
    def __init__(self):
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
            SELECT t.id AS TransactionID, t.Date AS TransactionDate, t.Time AS TransactionTime, t.Type AS TransactionType, CONCAT(s.Full_Name, ' ', s.Last_Name) AS StaffName, t.Amount AS TransactionAmount, t.PaymentType AS PaymentType
            FROM [Transaction] t
            JOIN Staff s ON t.StaffID = s.id;
        """
        cursor.execute(populate_query)
        data = cursor.fetchall()
        taxPercentage = 13
        self.updated_data = []
        for record in data:
            amount = record[5]
            total = math.ceil(amount * (1 + taxPercentage / 100))
            self.updated_data.append(tuple(record) + (taxPercentage, total))

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
        self.add_screen = AddTransactionScreen(self)
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
        self.calculate_screen = ProfitLossScreen()
        self.calculate_screen.show()

    def back(self):
        self.close()

class ReservationScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(ReservationScreen, self).__init__()

        uic.loadUi('ui_files/Reservation_Form_View.ui', self)

        self.backButton.clicked.connect(self.back)

    def back(self):
        self.close()

class StaffScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(StaffScreen, self).__init__()

        uic.loadUi('ui_files/staffManagment.ui', self)

        self.addButton.clicked.connect(self.add)
        self.updateButton.clicked.connect(self.update)
        self.deleteButton.clicked.connect(self.delete)
        self.backButton.clicked.connect(self.back)

    def add(self):
        self.add_screen = StaffAddScreen()
        self.add_screen.show()

    def update(self):
        self.update_screen = StaffUpdateScreen()
        self.update_screen.show()

    def delete(self):
        dlg = QtWidgets.QMessageBox.information(self,"Staff deleted","Staff successfully deleted!",QtWidgets.QMessageBox.StandardButton.Ok)

    def back(self):
        self.close()

class StaffAddScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(StaffAddScreen, self).__init__()

        uic.loadUi('ui_files/StaffAdd.ui', self)

        self.addStaffButton.clicked.connect(self.addStaff)
        self.backButton.clicked.connect(self.back)

    def addStaff(self):
        dlg = QtWidgets.QMessageBox.information(self,"Staff added","Staff successfully added!",QtWidgets.QMessageBox.StandardButton.Ok)

    def back(self):
        self.close()

class StaffUpdateScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(StaffUpdateScreen, self).__init__()

        uic.loadUi('ui_files/StaffUpdate.ui', self)

        self.updateStaffButton.clicked.connect(self.updateStaff)
        self.backButton.clicked.connect(self.back)

    def updateStaff(self):
        dlg = QtWidgets.QMessageBox.information(self,"Staff updated","Staff successfully updated!",QtWidgets.QMessageBox.StandardButton.Ok)

    def back(self):
        self.close()

class AddItemScreen(QtWidgets.QMainWindow): # ABDULLAH DOING #
    def __init__(self):
        super(AddItemScreen, self).__init__()

        uic.loadUi('ui_files/ItemAdd.ui', self)

        self.addButton.clicked.connect(self.addItem)
        self.backButton.clicked.connect(self.back)

    def addItem(self):
        dlg = QtWidgets.QMessageBox.information(self,"Item Added","Item successfully added!",QtWidgets.QMessageBox.StandardButton.Ok)
        
    def back(self):
        self.close()

class UpdateItemScreen(QtWidgets.QMainWindow): # ABDULLAH DOING #
    def __init__(self):
        super(UpdateItemScreen, self).__init__()

        uic.loadUi('ui_files/ItemUpdate.ui', self)

        self.updateButton.clicked.connect(self.updateItem)
        self.backButton.clicked.connect(self.back)

    def updateItem(self):
        dlg = QtWidgets.QMessageBox.information(self,"Item Update","Item successfully updated!",QtWidgets.QMessageBox.StandardButton.Ok)
        
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

        self.lineEdit.setText(self.item_name)
        self.lineEdit_2.setText(self.item_price)

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

        category_query1 = "SELECT Category FROM MenuItem WHERE ID = ?"
        cursor.execute(category_query1, (self.item_id))
        category = cursor.fetchone()[0]
        self.comboBox.setCurrentText(category)

        self.backButton.clicked.connect(self.back)
        self.updateItemButton.clicked.connect(self.updateItem)

    def back(self):
        self.close()

    def updateItem(self):
        if self.lineEdit.text() == "" or self.lineEdit_2.text() == "" or self.textEdit.toPlainText() == "":
            dlg = QtWidgets.QMessageBox.warning(self,"Missing Fields Failure","Fill all fields to update item!",QtWidgets.QMessageBox.StandardButton.Ok)
            return
            
        elif self.lineEdit.text() == self.item_name and self.lineEdit_2.text() == self.item_price and self.textEdit.toPlainText() == self.description:
            dlg = QtWidgets.QMessageBox.warning(self,"No Changes Made","No changes made to item!",QtWidgets.QMessageBox.StandardButton.Ok)
            return

        name = self.lineEdit.text()
        category = self.comboBox.currentText()
        price = self.lineEdit_2.text()
        description = self.textEdit.toPlainText()
        update_query = "UPDATE MenuItem SET Name = ?, Category = ?, Price = ?, Description = ? WHERE ID = ?" 
        cursor.execute(update_query, (name, category, price, description, self.item_id))
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
    def __init__(self, transaction):
        super(AddTransactionScreen, self).__init__()

        uic.loadUi('ui_files/TransactionAdd.ui', self)

        self.transaction = transaction

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

        insert_query = "INSERT INTO [Transaction](Date, Time, Type, StaffID, Amount, PaymentType) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(insert_query, (date, time, ttype, staff, amount, payment))
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

        update_query = "UPDATE [Transaction] SET Date = ?, Time = ?, Type = ?, StaffID = ?, Amount = ?, PaymentType = ? WHERE id = ?"
        cursor.execute(update_query, (date, time, ttype, staff, amount, payment, tid))
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
    def __init__(self):
        super(ProfitLossScreen, self).__init__()

        uic.loadUi('ui_files/ProfitLossScreen.ui', self)

        self.printButton.clicked.connect(self.printTransaction)
        self.backButton.clicked.connect(self.back)

    def printTransaction(self):
        dlg = QtWidgets.QMessageBox.information(self,"Transaction print","Transaction successfully printed!",QtWidgets.QMessageBox.StandardButton.Ok)

    def back(self):
        self.close()
    

# Create an instance of QtWidgets . QApplication
app = QtWidgets.QApplication(sys.argv)
window = UI() # Create an instance of our class
# window.show()
app.exec() # Start the application