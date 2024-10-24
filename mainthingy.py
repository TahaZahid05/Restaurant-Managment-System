import sys
from PyQt6 import QtWidgets
from PyQt6 import uic
from validate_email import validate_email

#1st index contains sample data to help get an idea of what data would be in the list
#0 = First Name
#1 = Last Name
#2 = Email
#3 = Username
#4 = Password
#5 = Address
#6 = Phone Number
userInfo = [["Taha","Zahid","tahazahid51@gmail.com","Taha Zahid","toto123",["H4 Yasir Complex"],"0308 2895690"],
            ["Abdullah","Shaikh","abdullahboi1@gmail.com","Abdullah Shaikh","sheikhchilli123",["Cricket"],"0000 0000000"]]
adminInfo = [["Ayaan","Merchant","ayaannoob1@gmail.com","Ayaan Merchant","ayoyo123",["Table Tennis"],"0000 0000000"]]

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
        if(self.emailAddress.text() == "" or self.userPass.text() == ""):
            dlg = QtWidgets.QMessageBox.warning(self,"Missing Fields Failure","Fill all fields to login!",QtWidgets.QMessageBox.StandardButton.Ok)
        else:
            for i in range(len(userInfo)):
                if (self.emailAddress.text() == userInfo[i][2] and self.userPass.text() == userInfo[i][4]):
                    self.user_screen = userOptions()
                    self.user_screen.show()
                    return
                    
            for l in range(len(adminInfo)):
                if (self.emailAddress.text() == adminInfo[l][2] and self.userPass.text() == adminInfo[l][4]):
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

        self.returnLoginButton.clicked.connect(self.closeScreen)
        self.registerButton.clicked.connect(self.registering)
        #Cancel button has been disabled as it can be misleading/unnecessary
        # self.cancelButton.clicked.connect(self.closeApp)
    
    def registering(self):
        for i in range(len(userInfo)):
            for j in range(6):
                #Add QValidation
                if (self.firstName.text() == "" or self.lastName.text() == "" or self.emailAddress.text() == "" or self.userName.text() == "" or self.userPass.text() == "" or self.passConfirm.text() == ""):
                    dlg = QtWidgets.QMessageBox.warning(self,"Missing Fields Failure","Fill all fields to register!",QtWidgets.QMessageBox.StandardButton.Ok)
                    break
                elif (userInfo[i][2] == self.emailAddress.text()):
                    dlg = QtWidgets.QMessageBox.warning(self,"Email Address Already Exists","This email is already used to make an account!",QtWidgets.QMessageBox.StandardButton.Ok)
                    break
                elif (userInfo[i][3] == self.userName.text()):
                    dlg = QtWidgets.QMessageBox.warning(self,"User Already Exists","The username is already used to make an account!",QtWidgets.QMessageBox.StandardButton.Ok)
                    break
                elif (not(validate_email(self.emailAddress.text()))):
                    dlg = QtWidgets.QMessageBox.warning(self,"Invalid Email Address","Email address is invalid!",QtWidgets.QMessageBox.StandardButton.Ok)
                    break
                elif (self.userPass.text() != self.passConfirm.text()):
                    dlg = QtWidgets.QMessageBox.warning(self,"Password Confirmation Failure","Confirm Password doesn't have the same password!",QtWidgets.QMessageBox.StandardButton.Ok)
                    break
                else:
                    userInfo.append([self.firstName.text(),self.lastName.text(),self.emailAddress.text(),self.userName.text(),self.userPass.text(),self.roleSelect.currentIndex()])
                    dlg = QtWidgets.QMessageBox.information(self,"Account created","Account was successfully created!",QtWidgets.QMessageBox.StandardButton.Ok)
                    self.firstName.clear()
                    self.lastName.clear()
                    self.emailAddress.clear()
                    self.userName.clear()
                    self.userPass.clear()
                    self.passConfirm.clear()
                    break


    def closeScreen(self):
        self.close()

    # Cancel button has been disabled as it can be misleading/unnecessary
    # def closeApp(self):
    #     app.quit()


class userOptions(QtWidgets.QMainWindow):
    def __init__(self):
        super(userOptions, self).__init__()

        uic.loadUi('ui_files/User_Screen.ui', self)

        self.onlineOrderButton.clicked.connect(self.onlineOrderScreen)
        self.seatReservationButton.clicked.connect(self.seatReserveScreen)
        self.feedbackButton.clicked.connect(self.feedbackScreen)
        self.trackOrderButton.clicked.connect(self.trackOrder)
        self.editProfileButton.clicked.connect(self.editProfile)
        self.backButton.clicked.connect(self.back)
    
    def onlineOrderScreen(self):
        self.online_order_screen = onlineOrder()
        self.online_order_screen.show()

    def seatReserveScreen(self):
        self.seat_reserve_screen = seatReserve()
        self.seat_reserve_screen.show()

    def feedbackScreen(self):
        self.feedback_screen = feedbackScreen()
        self.feedback_screen.show()

    def trackOrder(self):
        self.trackorder_screen = trackOrderScreen()
        self.trackorder_screen.show()

    def editProfile(self):
        self.editProfile_screen = editProfileScreen()
        self.editProfile_screen.show()

    def back(self):
        self.close()


class editProfileScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(editProfileScreen, self).__init__()

        uic.loadUi('ui_files/EditProfile.ui', self)

        self.newAddressButton.clicked.connect(self.newAddress)
        self.applyButton.clicked.connect(self.applyChanges)
        self.backButton.clicked.connect(self.back)

    def newAddress(self):
        self.newAddress_screen = newAddressScreen()
        self.newAddress_screen.show()

    def applyChanges(self):
        dlg = QtWidgets.QMessageBox.information(self,"Changes Applied","Account was successfully updated!",QtWidgets.QMessageBox.StandardButton.Ok)

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
    def __init__(self):
        super(newAddressScreen, self).__init__()

        uic.loadUi('ui_files/addAddressScreen.ui', self)

        self.submitButton.clicked.connect(self.addressSubmitted)
        self.backButton.clicked.connect(self.back)

    def addressSubmitted(self):
        dlg = QtWidgets.QMessageBox.information(self,"Changes Applied","Account was successfully updated!",QtWidgets.QMessageBox.StandardButton.Ok)

    def back(self):
        self.close()


class onlineOrder(QtWidgets.QMainWindow):
    def __init__(self):
        super(onlineOrder, self).__init__()

        uic.loadUi('ui_files/Order_ItemSelect.ui', self)

        self.checkOutButton.clicked.connect(self.checkOutScreen)
        self.backButton.clicked.connect(self.back)

    def back(self):
        self.close()

    def checkOutScreen(self):
        self.checkout_screen = checkOutScreen()
        self.checkout_screen.show()

class checkOutScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(checkOutScreen, self).__init__()

        uic.loadUi('ui_files/OnlineOrderCheckout.ui', self)

        self.backButton.clicked.connect(self.back)

    def back(self):
        self.close()

class seatReserve(QtWidgets.QMainWindow):
    def __init__(self):
        super(seatReserve, self).__init__()

        uic.loadUi('ui_files/Reservation_Form.ui', self)

        self.backButton.clicked.connect(self.back)
        self.cancelReservationButton.clicked.connect(self.cancelReservation)
        self.viewStatusButton.clicked.connect(self.viewStatus)
        self.reserveButton.clicked.connect(self.reserve)

    def back(self):
        self.close()

    def cancelReservation(self):
        dlg = QtWidgets.QMessageBox.information(self,"Reservation Cancelled","Reservation was successfully cancelled!",QtWidgets.QMessageBox.StandardButton.Ok)

    def viewStatus(self):
        self.view_status_screen = viewStatusScreen()
        self.view_status_screen.show()

    def reserve(self):
        dlg = QtWidgets.QMessageBox.information(self,"Reservation booked","Reservation was successfully booked!",QtWidgets.QMessageBox.StandardButton.Ok)


class viewStatusScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(viewStatusScreen, self).__init__()

        uic.loadUi('ui_files/Reservation_Status.ui', self)

        self.backButton.clicked.connect(self.back)

    def back(self):
        self.close()


class feedbackScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(feedbackScreen, self).__init__()

        uic.loadUi('ui_files/CustomerFeedBackForm.ui', self)

        self.backButton.clicked.connect(self.back)
        self.submitButton.clicked.connect(self.submit)

    def back(self):
        self.close()

    def submit(self):
        dlg = QtWidgets.QMessageBox.information(self,"Feedback successfully submitted","Feedback was successfully submitted!",QtWidgets.QMessageBox.StandardButton.Ok)


class trackOrderScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(trackOrderScreen, self).__init__()

        uic.loadUi('ui_files/OrderTrackMain.ui', self)

        self.viewDetailsButton.clicked.connect(self.DetailScreen)
        self.backButton.clicked.connect(self.back)

    def DetailScreen(self):
        self.detail_screen = viewDetailScreen()
        self.detail_screen.show()

    def back(self):
        self.close()


class viewDetailScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(viewDetailScreen, self).__init__()

        uic.loadUi('ui_files/OrderTrackDetails.ui', self)    

        self.backButton.clicked.connect(self.back)

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