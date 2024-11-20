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


class billScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(billScreen, self).__init__()

        uic.loadUi('ui_files/generateBillStart.ui', self)

        self.generateButton.clicked.connect(self.generateBill)
        self.backButton.clicked.connect(self.back)

    def generateBill(self):
        self.generateBill_screen = generateBillScreen()
        self.generateBill_screen.show()

    def back(self):
        self.close()

class generateBillScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(generateBillScreen, self).__init__()

        uic.loadUi('ui_files/billPrintAndOrderCompleted.ui', self)

        self.printButton.clicked.connect(self.printBill)
        self.paymentButton.clicked.connect(self.paymentReceived)
        self.backButton.clicked.connect(self.back)

    def printBill(self):
        dlg = QtWidgets.QMessageBox.information(self,"Bill Printed","Bill for order successfully printed!",QtWidgets.QMessageBox.StandardButton.Ok)
        
    def paymentReceived(self):
        dlg = QtWidgets.QMessageBox.information(self,"Payment Received","Payment for order successfully received!",QtWidgets.QMessageBox.StandardButton.Ok)

    def back(self):
        self.close()

class FeedbackScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(FeedbackScreen, self).__init__()

        uic.loadUi('ui_files/CustomerFeedBackView.ui', self)

        self.backButton.clicked.connect(self.back)

    def back(self):
        self.close()

class InventoryScreen(QtWidgets.QMainWindow):
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

class MenuScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(MenuScreen, self).__init__()

        uic.loadUi('ui_files/Menu_management.ui', self)

        self.addItemButton.clicked.connect(self.addItem)
        self.clearButton.clicked.connect(self.clear)
        self.backButton.clicked.connect(self.back)
        self.editItemButton.clicked.connect(self.editItem)
        self.removeItemButton.clicked.connect(self.removeItem)

    def addItem(self):
        dlg = QtWidgets.QMessageBox.information(self,"Menu Item Added","Menu Item successfully added!",QtWidgets.QMessageBox.StandardButton.Ok)

    def clear(self):
        pass
        #Will add functionality to clear all fields

    def back(self):
        self.close()

    def editItem(self):
        self.edit_item_screen = editItemScreen()
        self.edit_item_screen.show()

    def removeItem(self):
        dlg = QtWidgets.QMessageBox.information(self,"Menu Item Deleted","Menu Item successfully deleted!",QtWidgets.QMessageBox.StandardButton.Ok)

class OrderScreen(QtWidgets.QMainWindow):
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

        self.addButton.clicked.connect(self.add)
        self.updateButton.clicked.connect(self.update)
        self.deleteButton.clicked.connect(self.delete)
        self.calculateButton.clicked.connect(self.calculate)
        self.backButton.clicked.connect(self.back)

    def add(self):
        self.add_screen = AddTransactionScreen()
        self.add_screen.show()

    def update(self):
        self.update_screen = UpdateTransactionScreen()
        self.update_screen.show()

    def delete(self):
        dlg = QtWidgets.QMessageBox.information(self,"Transaction deleted","Transaction successfully deleted!",QtWidgets.QMessageBox.StandardButton.Ok)

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

class AddItemScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(AddItemScreen, self).__init__()

        uic.loadUi('ui_files/ItemAdd.ui', self)

        self.addButton.clicked.connect(self.addItem)
        self.backButton.clicked.connect(self.back)

    def addItem(self):
        dlg = QtWidgets.QMessageBox.information(self,"Item Added","Item successfully added!",QtWidgets.QMessageBox.StandardButton.Ok)
        
    def back(self):
        self.close()

class UpdateItemScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(UpdateItemScreen, self).__init__()

        uic.loadUi('ui_files/ItemUpdate.ui', self)

        self.updateButton.clicked.connect(self.updateItem)
        self.backButton.clicked.connect(self.back)

    def updateItem(self):
        dlg = QtWidgets.QMessageBox.information(self,"Item Update","Item successfully updated!",QtWidgets.QMessageBox.StandardButton.Ok)
        
    def back(self):
        self.close()

class editItemScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(editItemScreen, self).__init__()

        uic.loadUi('ui_files/menuItemUpdate.ui', self)

        self.backButton.clicked.connect(self.back)
        self.updateItemButton.clicked.connect(self.updateItem)

    def back(self):
        self.close()

    def updateItem(self):
        dlg = QtWidgets.QMessageBox.information(self,"Menu Item Update","Menu Item successfully updated!",QtWidgets.QMessageBox.StandardButton.Ok)

class ViewStatusOrder(QtWidgets.QMainWindow):
    def __init__(self):
        super(ViewStatusOrder, self).__init__()

        uic.loadUi('ui_files/Order_Status.ui', self)

        self.backButton.clicked.connect(self.back)

    def back(self):
        self.close()

class AddTransactionScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(AddTransactionScreen, self).__init__()

        uic.loadUi('ui_files/TransactionAdd.ui', self)

        self.addTransactionButton.clicked.connect(self.addTransaction)
        self.backButton.clicked.connect(self.back)

    def addTransaction(self):
        dlg = QtWidgets.QMessageBox.information(self,"Transaction added","Transaction successfully added!",QtWidgets.QMessageBox.StandardButton.Ok)
    
    def back(self):
        self.close()

class UpdateTransactionScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(UpdateTransactionScreen, self).__init__()

        uic.loadUi('ui_files/TransactionUpdate.ui', self)

        self.updateTransactionButton.clicked.connect(self.updateTransaction)
        self.backButton.clicked.connect(self.back)

    def updateTransaction(self):
        dlg = QtWidgets.QMessageBox.information(self,"Transaction updated","Transaction successfully updated!",QtWidgets.QMessageBox.StandardButton.Ok)
    
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