from PyQt6 import QtCore, QtGui, QtWidgets
from out2 import Ui_Widget
import os, sys
import hashlib
import datetime
import time
import jwt

contract_date = ''
class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self):
        # super().__init__()
        super().__init__()
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.ui.calendar.clicked.connect(self.on_date_selected)
        self.ui.btn_licience_yes.clicked.connect(self.generator_key)
        self.ui.btn_licience_no.clicked.connect(self.close)

    def on_date_selected(self):
        global contract_date
        date = self.ui.calendar.selectedDate()
        date = date.toString('yyyy-MM-dd')
        contract_date = date
    def hash_message_with_key(self, message, key):
        # Combine the message and key
        message_with_key = message + key

        # Create a new hash object using SHA-256 algorithm
        hash_object = hashlib.sha256(message_with_key.encode())

        # Get the hexadecimal representation of the hash
        hashed_message = hash_object.hexdigest()

        return hashed_message
    

        
    def state_date(self):
        global contract_date
        year = int(contract_date[0:4])	
        month = int(contract_date[5:7])
        day = int(contract_date[8:10])

        now = time.time()
        dt = datetime.datetime.fromtimestamp(now)
        date_now = str(dt)
        
        year_now = int(date_now[0:4])	
        month_now = int(date_now[5:7])
        day_now = int(date_now[8:10])


    def generator_key(self):
        global contract_date
        machinenumber = self.ui.li_machinenumber.text()
        if contract_date == '' or machinenumber =='':
            print("no")
        else :
            
        # print(machinenumber)
            year = int(contract_date[0:4])	
            month = int(contract_date[5:7])
            day = int(contract_date[8:10])

            year = str(year)
    
            if month < 10:
                month = '0'+str(month)
            else:
                month = str(month)

            if day < 10:
                day = '0'+str(day)
            else:
                day = str(day)

            key = 'tlkwjdqhd'
            json = {"time":year + '-' + month + '-' + day, "machinenumber":machinenumber}
            print(json)
            token = jwt.encode(json,key)
            self.ui.li_serialnumber.setText(token)
            # self.ui.label_alert.hide()
     
            # print(token)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    window = Ui_MainWindow()
    # license_window = License_Ui()
    window.show()
    app.exec()
    # window.setWindowIcon(QtGui.QIcon('img/icon.ico'))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
