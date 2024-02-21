from PyQt6 import QtWidgets, QtCore, QtGui, QtWebChannel


from src.license_widget import License_Ui_Widget
from src.license import getMachine_addr, check_activation

machine_number = ''
serial_number = ''
class License_Ui(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = License_Ui_Widget()
        self.ui.setupUi(self)
        self.initUI()
        self.btn_event()
    def initUI(self):
        global machine_number
        machine_number = getMachine_addr()
        machine_number = machine_number[12:len(machine_number)]
        self.ui.li_machinenumber.setText(machine_number)
        self.ui.li_machinenumber.setReadOnly(True)

    def btn_event(self):
        self.ui.btn_licience_yes.clicked.connect(self.activation)
        self.ui.btn_licience_no.clicked.connect(self.close)
    def activation(self):
        global serial_number
        serial_number = self.ui.li_serialnumber.text()
        status_activation = check_activation(serial_number)
        if status_activation == "yes":
            with open('author.dll', 'w') as file:
                # Write the text to the file
                file.write(serial_number)
            self.hide()
        else :
            print("retry")
