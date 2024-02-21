from PyQt6 import QtWidgets, QtCore, QtGui, QtWebChannel


from src.login_widget import Login_Ui_Widget
from src.license import getMachine_addr, check_activation


class Login_Ui(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__()
        self.ui = Login_Ui_Widget()
        self.ui.setupUi(self)
        self.initUI(parent)
    def initUI(self, parent):
        self.ui.li_key.setText(parent.key)
        self.ui.li_password.setText(parent.password)
        self.ui.li_userid.setText(parent.userid)
        self.btn_event(parent)

    def btn_event(self,parent):
        self.ui.btn_log_yes.clicked.connect(lambda: self.activation(parent))
        self.ui.btn_log_no.clicked.connect(lambda: self.closebutton(parent))
    def activation(self, parent):

        key = self.ui.li_key.text()
        userid = self.ui.li_userid.text()
        password = self.ui.li_password.text()

        parent.format_value_userinfo(key, userid, password)
        self.close()
        # return key
    def closebutton(self, parent):
        parent.format_value_userinfo('', '', '')
        self.close()