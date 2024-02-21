from PyQt6 import QtWidgets, QtCore, QtGui, QtWebChannel
import draw_tool
from src.out1 import Ui_Widget
from src.license_class import License_Ui
import requests
from io import BytesIO
import time
import os
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from src.license import getMachine_addr, check_activation

class WorkerThread(QThread):
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)

    def run(self):
        # Your thread logic goes here
        import amazon_request.Get_Amazon
        time.sleep(3)
        self.finished.emit()

class BGMainUi(QtWidgets.QWidget):
    def __init__(self):
        # super().__init__()
        super().__init__()
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.thread = WorkerThread()
        self.thread.finished.connect(self.on_thread_finished)

        self.initUI()
    def initUI(self):
        # self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint)
        self.setstyle_setting()
        self.btn_event()
    def closeEvent(self, event):
        import amazon_request.deleteFile
        # result_delete_files = delete_csv_file()
        print("deleted!!!")
        import amazon_request.renameFile
        # result_rename_files = renameF()
        print("renamed!!!")

    def setstyle_setting(self):
        self.ui.btn_close.hide()
        self.ui.btn_hide.hide()
        self.ui.label_qoo.hide()
        self.ui.label_ratu.hide()
        self.setstyle_amazon()
        self.setstyle_btn()

        self.ui.btn_qoo.clicked.connect(self.setstyle_qoo)
        self.ui.btn_ratu.clicked.connect(self.setstyle_ratu)
        self.ui.btn_amazon.clicked.connect(self.setstyle_amazon)

    def setstyle_btn(self):
        QtGui.QFontDatabase.addApplicationFont("img/1.ttf")
        QtGui.QFontDatabase.addApplicationFont("img/2.ttf")
        # self.ui.btn_new.setStyleSheet("QPushButton{font-size:50px;font-family:'Algerian'}")
    def btn_event(self):
        self.ui.btn_display.clicked.connect(self.ConnectServer_amazon)
        self.ui.btn_close.clicked.connect(self.close_event)
        self.ui.btn_hide.clicked.connect(self.showMinimized)
        self.ui.btn_get.clicked.connect(self.get_dataset)
        self.ui.btn_new.clicked.connect(self.ConnectServer_qoo)
    def get_dataset(self):
        self.thread.start()
        self.ui.btn_get.setText("作業中")
    def on_thread_finished(self):
        self.ui.btn_get.setText('抽出')
    def close_event(self):
        import amazon_request.deleteFile
        # result_delete_files = delete_csv_file()
        print("deleted!!!")
        import amazon_request.renameFile
        # result_rename_files = renameF()
        print("renamed!!!")
        self.close()
    def setstyle_qoo(self):
        self.ui.label_qoo.show()
        self.ui.label_amazon.hide()
        self.ui.label_ratu.hide()
        self.ui.wid_amazon.hide()
        self.ui.wid_raku.hide()
        self.ui.wid_qoo.show()
        self.ui.stackedWidget.setCurrentIndex(1)

    def setstyle_ratu(self):
        self.ui.label_ratu.show()
        self.ui.label_amazon.hide()
        self.ui.label_qoo.hide()
        self.ui.wid_amazon.hide()
        self.ui.wid_qoo.hide()
        self.ui.wid_raku.show()
        self.ui.stackedWidget.setCurrentIndex(3)

    def setstyle_amazon(self):
        self.ui.label_amazon.show()
        self.ui.label_ratu.hide()
        self.ui.label_qoo.hide()
        self.ui.wid_qoo.hide()
        self.ui.wid_raku.hide()
        self.ui.wid_amazon.show()
        self.ui.stackedWidget.setCurrentIndex(0)


    def setTable_amazon(self, count):
        self.ui.tableWidget_amazon.setRowCount(count)
        self.ui.tableWidget_amazon.setColumnCount(5)
        self.ui.tableWidget_amazon.setColumnWidth(0, 150)
        self.ui.tableWidget_amazon.setColumnWidth(1, 400)
        self.ui.tableWidget_amazon.setColumnWidth(2, 200)
        self.ui.tableWidget_amazon.setColumnWidth(3, 200)
        self.ui.tableWidget_amazon.setColumnWidth(4, 200)

        for i in range(0, count):
            self.ui.tableWidget_amazon.setRowHeight(i, 100)
    def setTable_qoo(self, count):
        self.ui.tableWidget_qoo.setRowCount(count)
        self.ui.tableWidget_qoo.setColumnCount(5)
        self.ui.tableWidget_qoo.setColumnWidth(0, 150)
        self.ui.tableWidget_qoo.setColumnWidth(1, 400)
        self.ui.tableWidget_qoo.setColumnWidth(2, 200)
        self.ui.tableWidget_qoo.setColumnWidth(3, 200)
        self.ui.tableWidget_qoo.setColumnWidth(4, 200)

        for i in range(0, count):
            self.ui.tableWidget_qoo.setRowHeight(i, 100)
    def setTable_raku(self, count):
        self.ui.tableWidget_raku.setRowCount(count)
        self.ui.tableWidget_raku.setColumnCount(5)
        self.ui.tableWidget_raku.setColumnWidth(0, 150)
        self.ui.tableWidget_raku.setColumnWidth(1, 400)
        self.ui.tableWidget_raku.setColumnWidth(2, 200)
        self.ui.tableWidget_raku.setColumnWidth(3, 200)
        self.ui.tableWidget_raku.setColumnWidth(4, 200)

        for i in range(0, count):
            self.ui.tableWidget_raku.setRowHeight(i, 100)
    def img_product(self, img_url):
        image = QtGui.QPixmap()
        image.loadFromData(BytesIO(img_url.content).read())
        image = image.scaled(80, 80)
        img_product = QtWidgets.QLabel()
        img_product.setPixmap(image)
        return img_product
    def ConnectServer_amazon(self):
        result = amazon_request.draw_tool.Get_Amazon('Amazon(1).csv')
        count = result[5]
        # count = 2
        self.setTable_amazon(count)
        for i in range(1, count):
            response = requests.get(str(result[0][i]))
            self.ui.tableWidget_amazon.setCellWidget(i-1, 0, self.img_product(response))

            item_title = QtWidgets.QTableWidgetItem(str(result[1][i]))
            font = QtGui.QFont("Arial", 20)  # Example font and size
            item_title.setFont(font)
            self.ui.tableWidget_amazon.setItem(i-1, 1, item_title)

            item_price = QtWidgets.QTableWidgetItem(str(result[2][i]))
            item_price.setFont(font)
            self.ui.tableWidget_amazon.setItem(i-1, 2, item_price)


            item_qty = QtWidgets.QTableWidgetItem(str(result[3][i]))
            item_qty.setFont(font)
            self.ui.tableWidget_amazon.setItem(i-1, 3, item_qty)

            item_asin = QtWidgets.QTableWidgetItem(str(result[4][i]))
            item_asin.setFont(font)
            self.ui.tableWidget_amazon.setItem(i-1, 4, item_asin)
    def ConnectServer_qoo(self):
        result = amazon_request.draw_tool.Get_Amazon('newlist.csv')
        count = result[5]
        # count = 2
        self.setTable_qoo(count)
        for i in range(1, count):
            response = requests.get(str(result[0][i]))
            self.ui.tableWidget_qoo.setCellWidget(i-1, 0, self.img_product(response))

            item_title = QtWidgets.QTableWidgetItem(str(result[1][i]))
            font = QtGui.QFont("Arial", 20)  # Example font and size
            item_title.setFont(font)
            self.ui.tableWidget_qoo.setItem(i-1, 1, item_title)

            item_price = QtWidgets.QTableWidgetItem(str(result[2][i]))
            item_price.setFont(font)
            self.ui.tableWidget_qoo.setItem(i-1, 2, item_price)


            item_qty = QtWidgets.QTableWidgetItem(str(result[3][i]))
            item_qty.setFont(font)
            self.ui.tableWidget_qoo.setItem(i-1, 3, item_qty)

            item_asin = QtWidgets.QTableWidgetItem(str(result[4][i]))
            item_asin.setFont(font)
            self.ui.tableWidget_qoo.setItem(i-1, 4, item_asin)
    def ConnectServer_raku(self):
        result = amazon_request.draw_tool.Get_Amazon()
        count = result[5]
        # count = 2
        self.setTable_raku(count)
        for i in range(1, count):
            response = requests.get(str(result[0][i]))
            self.ui.tableWidget_amazon.setCellWidget(i-1, 0, self.img_product(response))

            item_title = QtWidgets.QTableWidgetItem(str(result[1][i]))
            font = QtGui.QFont("Arial", 20)  # Example font and size
            item_title.setFont(font)
            self.ui.tableWidget_amazon.setItem(i-1, 1, item_title)

            item_price = QtWidgets.QTableWidgetItem(str(result[2][i]))
            item_price.setFont(font)
            self.ui.tableWidget_amazon.setItem(i-1, 2, item_price)


            item_qty = QtWidgets.QTableWidgetItem(str(result[3][i]))
            item_qty.setFont(font)
            self.ui.tableWidget_amazon.setItem(i-1, 3, item_qty)

            item_asin = QtWidgets.QTableWidgetItem(str(result[4][i]))
            item_asin.setFont(font)
            self.ui.tableWidget_amazon.setItem(i-1, 4, item_asin)