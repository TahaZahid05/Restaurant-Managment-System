import sys
from PyQt6 import QtWidgets
from PyQt6 import uic
from validate_email import validate_email

#1st index contains sample data to help get an idea of what data would be in the list
userInfo = [["Taha","Zahid","tahazahid51@gmail.com","Taha Zahid","toto123",0]]

class UI(QtWidgets.QMainWindow):
    def __init__(self):
    # Call the inherited classes __init__ method
        super(UI, self).__init__()
        # Load the .ui file
        uic.loadUi('ui_files/User_Login.ui', self)

        self.show()
        
        self.registerButton.clicked.connect(self.register)
        self.loginButton.clicked.connect(self.login)

    def register(self):
        self.register_user = registerUser()
        self.register_user.show()

    def login(self):
        if(self.emailAddress.text() == "" or self.userPass.text() == ""):
            dlg = QtWidgets.QMessageBox.warning(self,"Missing Fields Failure","Fill all fields to login!",QtWidgets.QMessageBox.StandardButton.Ok)
        else:
            for i in range(len(userInfo)):
                for j in range(6):
                    if (self.emailAddress.text() == userInfo[i][2] and self.userPass.text() == userInfo[i][4]):
                        self.user_screen = userOptions()
                        self.user_screen.show()
                        return
            dlg = QtWidgets.QMessageBox.warning(self,"Login Failure","No account with the following email address and password exist!",QtWidgets.QMessageBox.StandardButton.Ok)


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


class onlineOrder(QtWidgets.QMainWindow):
    def __init__(self):
        super(onlineOrder, self).__init__()

        uic.loadUi('ui_files/Order_ItemSelect.ui', self)

        self.checkOutButton.clicked.connect(self.checkOutScreen)

    def checkOutScreen(self):
        self.checkout_screen = checkOutScreen()
        self.checkout_screen.show()

class checkOutScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(checkOutScreen, self).__init__()

        uic.loadUi('ui_files/OnlineOrderCheckout.ui', self)

        # self.checkOutButton.clicked.connect(self.checkOutScreen)

class seatReserve(QtWidgets.QMainWindow):
    def __init__(self):
        super(seatReserve, self).__init__()

        uic.loadUi('ui_files/Reservation_Form.ui', self)


class feedbackScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(feedbackScreen, self).__init__()

        uic.loadUi('ui_files/CustomerFeedBackForm.ui', self)

class trackOrderScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(trackOrderScreen, self).__init__()

        uic.loadUi('ui_files/OrderTrackMain.ui', self)

        self.viewDetailsButton.clicked.connect(self.DetailScreen)
        # self.checkOutButton.clicked.connect(self.checkOutScreen)

    def DetailScreen(self):
        self.detail_screen = viewDetailScreen()
        self.detail_screen.show()


class viewDetailScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(viewDetailScreen, self).__init__()

        uic.loadUi('ui_files/OrderTrackDetails.ui', self)    






    

# Create an instance of QtWidgets . QApplication
app = QtWidgets.QApplication(sys.argv)
window = UI() # Create an instance of our class
# window.show()
app.exec() # Start the application