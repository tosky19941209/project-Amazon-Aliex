# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(466, 207)
        self.li_machinenumber = QtWidgets.QLineEdit(Widget)
        self.li_machinenumber.setGeometry(QtCore.QRect(150, 50, 301, 31))
        self.li_machinenumber.setObjectName("li_machinenumber")
        self.li_serialnumber = QtWidgets.QLineEdit(Widget)
        self.li_serialnumber.setGeometry(QtCore.QRect(150, 100, 301, 31))
        self.li_serialnumber.setObjectName("li_serialnumber")
        self.label_machinenumber = QtWidgets.QLabel(Widget)
        self.label_machinenumber.setGeometry(QtCore.QRect(10, 50, 131, 21))
        self.label_machinenumber.setStyleSheet("font: 13pt \"MS Shell Dlg 2\";")
        self.label_machinenumber.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_machinenumber.setObjectName("label_machinenumber")
        self.label_serialnumber = QtWidgets.QLabel(Widget)
        self.label_serialnumber.setGeometry(QtCore.QRect(20, 100, 121, 21))
        self.label_serialnumber.setStyleSheet("font: 13pt \"MS Shell Dlg 2\";")
        self.label_serialnumber.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_serialnumber.setObjectName("label_serialnumber")
        self.btn_licience_yes = QtWidgets.QPushButton(Widget)
        self.btn_licience_yes.setGeometry(QtCore.QRect(0, 150, 231, 41))
        self.btn_licience_yes.setStyleSheet("color: rgb(255, 85, 0);\n"
"font: 14pt \"MS Shell Dlg 2\";")
        self.btn_licience_yes.setObjectName("btn_licience_yes")
        self.btn_licience_no = QtWidgets.QPushButton(Widget)
        self.btn_licience_no.setGeometry(QtCore.QRect(230, 150, 231, 41))
        self.btn_licience_no.setStyleSheet("color: rgb(0, 85, 255);\n"
"font: 14pt \"MS Shell Dlg 2\";")
        self.btn_licience_no.setObjectName("btn_licience_no")
        self.label_alert = QtWidgets.QLabel(Widget)
        self.label_alert.setGeometry(QtCore.QRect(110, 10, 241, 31))
        self.label_alert.setStyleSheet("font: 18pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 0, 0);")
        self.label_alert.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_alert.setObjectName("label_alert")

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.label_machinenumber.setText(_translate("Widget", "機械番号"))
        self.label_serialnumber.setText(_translate("Widget", "シリアルナンバー"))
        self.btn_licience_yes.setText(_translate("Widget", "生成"))
        self.btn_licience_no.setText(_translate("Widget", "近い"))
        self.label_alert.setText(_translate("Widget", "生成キー"))
