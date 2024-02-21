from PyQt6 import QtWidgets, QtCore, QtGui, QtWebChannel

import requests
from io import BytesIO
import time
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
import os
from src.out5 import Ui_Widget
from src.license_class import License_Ui
from src.license import  check_activation
from Aliex.Aliexpress_Products import Aliex_main_id
from Qoo10.Qoo10_products import main_id
from src.login_class import Login_Ui

rate_qoo = 1
rate_raku = 1
status_market_qoo = '0'
status_market_amazon = '0'

status_button = 'amazon'
class WorkerThread(QThread):
    finished = pyqtSignal()

    def __init__(self, flag):
        super().__init__()
        self.flag = flag
    def run(self):
        Aliex_main_id(self.flag)
        time.sleep(3)
        self.finished.emit()

class WorkThread_Draw(QThread):
    progress_load_image = pyqtSignal(QtGui.QPixmap, str, str, str, str, int)

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
    
    def run(self):
        from Qoo10.Draw import Draw_csv
        global rate_qoo, status_market_qoo
        result = Draw_csv(self.filename)

        count = result[5]
        for i in range(1, count):
            if self.filename !='消去.csv':
                response = requests.get(str(result[1][i]))
                image = QtGui.QPixmap()
                image.loadFromData(BytesIO(response.content).read())
                img_product = QtGui.QPixmap(image)   

            if self.filename =='消去.csv':
                response = str(result[1][i])
                image = QtGui.QPixmap()
                # image.loadFromData(BytesIO(response.content).read())
                img_product = QtGui.QPixmap(image)        
            
            title = str(result[2][i])

            price = str(result[0][i])
            
            item_qty = str(result[3][i])
            
            item_asin = str(result[4][i])

            self.progress_load_image.emit(img_product, title, price, item_qty, item_asin, i)
                                                                                           
class BGMainUi(QtWidgets.QWidget):
    def __init__(self):
        # super().__init__()
        super().__init__()
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.initUI()
        self.key = ''
        self.userid = ''
        self.password = ''


    def initUI(self):

        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint)
        self.setstyle_setting()
        self.btn_event()

    def closeEvent(self, event):
        print("Closed!")
        if os.path.exists('author.dll') and os.path.isfile('author.dll'):
            os.remove('author.dll')
    def format_value_userinfo(self, key, id, pwd):
        self.key = key
        self.userid = id
        self.password = pwd
    
        if key == '' or id == '' or pwd == '':
            # global in_key, in_userid, in_password
            self.setstyle_amazon()
            # print(f'in-key : {self.key}')
            # print(f'in-id : {self.userid}')
            # print(f'in-pwd : {self.password}')
    
    def setstyle_setting(self):

        self.ui.btn_close.hide()
        self.ui.btn_hide.hide()
        self.ui.label_qoo.hide()
        self.ui.label_raku.hide()
        self.ui.btn_raku.hide()
        self.setstyle_amazon()
        self.setstyle_btn()
        self.ui.btn_qoo.clicked.connect(self.setstyle_qoo)
        self.ui.btn_raku.clicked.connect(self.setstyle_raku)
        self.ui.btn_amazon.clicked.connect(self.setstyle_amazon)

        self.movie = QtGui.QMovie('img/loading.gif')
        self.ui.label_loading.setMovie(self.movie)
        self.movie.start()
        self.ui.label_loading.hide()

    def setstyle_btn(self):
        QtGui.QFontDatabase.addApplicationFont("img/1.ttf")
        QtGui.QFontDatabase.addApplicationFont("img/2.ttf")

    def btn_event(self):
        self.ui.btn_compare.clicked.connect(lambda : self.get_dataset(2))
        self.ui.btn_close.clicked.connect(self.close_event)
        self.ui.btn_hide.clicked.connect(self.showMinimized)
        self.ui.btn_get.clicked.connect(lambda: self.get_dataset(0))
        self.ui.btn_new.clicked.connect(lambda: self.ConnectServer_preprocess('new'))
        self.ui.btn_update.clicked.connect(lambda :self.ConnectServer_preprocess('update'))
        self.ui.btn_remove.clicked.connect(lambda :self.ConnectServer_preprocess('remove'))
        self.ui.btn_rate.clicked.connect(self.set_rate)
        self.ui.btn_start.clicked.connect(self.send_updatedData)
        self.ui.btn_get2.clicked.connect(lambda: self.get_dataset(1))

    def get_dataset(self, flag):
        self.thread = WorkerThread(flag)
        self.thread.finished.connect(self.on_thread_get_finished)
        self.thread.start()
        self.ui.btn_get.setText("作業中")
        self.ui.label_loading.show()

    def on_thread_get_finished(self):
        self.ui.btn_get.setText('抽出')
        self.ConnectServer_amazon('登録.csv')
        self.ui.label_loading.hide()

    def close_event(self):
        self.close()

    def setstyle_qoo(self):
        self.setstyle_qoo_init()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("特典設定をしましたか?")
        # msg.setInformativeText("This is additional information")
        msg.setWindowTitle("特典設定")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)     

   # Run the dialog, and check results   
        bttn = msg.exec()
        if bttn == QMessageBox.StandardButton.Yes:
            if self.key == '' or self.password == '' or self.userid == '':
                window_login = Login_Ui(self)
                window_login.exec()
        else:
            self.setstyle_amazon()

    def setstyle_qoo_init(self):
        global status_button
        status_button = 'qoo'
        print(f'status_button : {status_button}')
        self.ui.label_qoo.show()
        self.ui.label_amazon.hide()
        self.ui.label_raku.hide()
        self.ui.wid_amazon.hide()
        self.ui.wid_raku.hide()
        self.ui.wid_qoo.show()
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.lineEdit_rate.setText(str(rate_qoo))
    # def setstyle_qoo(self):
    #     global status_button
    #     status_button = 'qoo'
    #     self.ui.label_qoo.show()
    #     self.ui.label_amazon.hide()
    #     self.ui.label_raku.hide()
    #     self.ui.wid_amazon.hide()
    #     self.ui.wid_raku.hide()
    #     self.ui.wid_qoo.show()
    #     self.ui.stackedWidget.setCurrentIndex(1)
    #     self.ui.lineEdit_rate.setText(str(rate_qoo))

    def setstyle_raku(self):
        global status_button
        status_button = 'raku'
        self.ui.label_raku.show()
        self.ui.label_amazon.hide()
        self.ui.label_qoo.hide()
        self.ui.wid_amazon.hide()
        self.ui.wid_qoo.hide()
        self.ui.wid_raku.show()
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.lineEdit_rate.setText(str(rate_raku))

    def setstyle_amazon(self):
        global status_button
        status_button = 'amazon'
        self.ui.label_amazon.show()
        self.ui.label_raku.hide()
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
        image = img_url.scaled(80, 80)
        img_product = QtWidgets.QLabel()
        img_product.setPixmap(image)
        return img_product

    def set_rate(self):
        global rate_qoo, rate_raku
        text = self.ui.lineEdit_rate.text()
        if status_button == 'qoo':
            if text:
                rate_qoo = float(text)
                print("rate_qoo:", rate_qoo)
            else:
                print("The line edit is empty")
        if status_button == 'raku':
            if text:
                rate_raku = float(text)
                print("rate_raku:", rate_raku)
            else:
                print("The line edit is empty")


    def send_updatedData(self):

        global status_market_qoo, status_market_raku
        # status_market = 'qoo'
        # main_id(status_market, self.key, self.userid, self.password)

        if(status_button == 'qoo'):
            rate = rate_qoo
            status_market = status_market_qoo

        if status_market == '0':
            print("not active")
        else:
            # update_csv(rate, status_market)
            main_id(status_market, self.userid, self.key, self.password)

    def ConnectServer_amazon(self, filename):
        from Qoo10.Draw import Draw_csv
        global rate_qoo, status_market_amazon, status_button
        result = Draw_csv(filename)
        count = result[5]
        # print(result)
        status_button = 'amazon'
        status_market_amazon = filename
        
        self.ui.label_loading.show()
        self.thread_amazon = WorkThread_Draw(filename)
        self.thread_amazon.progress_load_image.connect(self.Draw_img)
        self.thread_amazon.start()
        self.thread_amazon.finished.connect(self.ConnectServer_amazon_finished)
        self.setTable_amazon(count)
    def ConnectServer_amazon_finished(self):
        self.ui.label_amazon.hide()
    def ConnectServer_preprocess(self,btn_name):

        if btn_name == 'new':
            if os.path.exists('登録.csv') and os.path.isfile('登録.csv'):
                self.setTable_qoo(0)
                self.ConnectServer_qoo('登録.csv', 'new')
            else:
                self.ui.tableWidget_qoo.setRowCount(0)
                self.ui.tableWidget_qoo.setColumnCount(0)
                print('not file')
        if btn_name == 'update':
            if os.path.exists('更新.csv') and os.path.isfile('更新.csv'):
                self.setTable_qoo(0)
                self.ConnectServer_qoo('更新.csv', 'update')
            else:
                self.ui.tableWidget_qoo.setRowCount(0)
                self.ui.tableWidget_qoo.setColumnCount(0)
                print('not file')
        if btn_name == 'remove':
            if os.path.exists('消去.csv') and os.path.isfile('消去.csv'):
                self.setTable_qoo(0)
                self.ConnectServer_qoo('消去.csv', 'remove')
            else:
                self.ui.tableWidget_qoo.setRowCount(0)
                self.ui.tableWidget_qoo.setColumnCount(0)
                print('not file')


    def ConnectServer_qoo(self,filename, btn_name):
        from Qoo10.Draw import Draw_csv
        global rate_qoo, status_market_qoo, status_button
        result = Draw_csv(filename)
        count = result[5]
        # print(result)
        status_market_qoo = filename
        status_button = 'qoo'

        self.ui.label_loading.show()
        if btn_name == 'new':
            self.ui.btn_new.setText("作業中")
        if btn_name == 'update':
            self.ui.btn_update.setText('作業中')
        if btn_name == 'remove':
            self.ui.btn_remove.setText('作業中')

        self.thread_qoo = WorkThread_Draw(filename)
        self.thread_qoo.progress_load_image.connect(self.Draw_img)
        self.thread_qoo.start()
        self.thread_qoo.finished.connect(lambda:self.ConnectServer_qoo_finished(btn_name))
        self.setTable_qoo(count)

    def ConnectServer_qoo_finished(self, btn_name):
        self.ui.label_loading.hide()
        if btn_name == 'new':
            self.ui.btn_new.setText("新規")
        if btn_name == 'update':
            self.ui.btn_update.setText('更新')
        if btn_name == 'remove':
            self.ui.btn_remove.setText('消去')
    def Draw_img(self, img, title, price, qty, asin ,i):
        if(status_button == 'qoo'):
            self.ui.tableWidget_qoo.setCellWidget(i-1, 0, self.img_product(img))

            item_title = QtWidgets.QTableWidgetItem(title)
            font = QtGui.QFont("Arial", 20)  # Example font and size
            item_title.setFont(font)
            self.ui.tableWidget_qoo.setItem(i-1, 1, item_title)

        
            item_price = QtWidgets.QTableWidgetItem(price)
            item_price.setFont(font)
            self.ui.tableWidget_qoo.setItem(i-1, 2, item_price)

            item_qty = QtWidgets.QTableWidgetItem(qty)
            item_qty.setFont(font)
            self.ui.tableWidget_qoo.setItem(i-1, 3, item_qty)

            item_asin = QtWidgets.QTableWidgetItem(asin)
            item_asin.setFont(font)
            self.ui.tableWidget_qoo.setItem(i-1, 4, item_asin)
        if(status_button == 'amazon'):
            self.ui.tableWidget_amazon.setCellWidget(i-1, 0, self.img_product(img))

            item_title = QtWidgets.QTableWidgetItem(title)
            font = QtGui.QFont("Arial", 20)  # Example font and size
            item_title.setFont(font)
            self.ui.tableWidget_amazon.setItem(i-1, 1, item_title)

        
            item_price = QtWidgets.QTableWidgetItem(price)
            item_price.setFont(font)
            self.ui.tableWidget_amazon.setItem(i-1, 2, item_price)

            item_qty = QtWidgets.QTableWidgetItem(qty)
            item_qty.setFont(font)
            self.ui.tableWidget_amazon.setItem(i-1, 3, item_qty)

            item_asin = QtWidgets.QTableWidgetItem(asin)
            item_asin.setFont(font)
            self.ui.tableWidget_amazon.setItem(i-1, 4, item_asin)

def activation():
    with open('author.dll', 'r') as file:
        serialnumber = file.read()
    if(check_activation(serialnumber) == 'yes'):
        print("authorization activated")
        timer.stop()
        window.show()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    app = QtWidgets.QApplication([])

    window = BGMainUi()
    license_window = License_Ui()

    window.setWindowIcon(QtGui.QIcon('img/icon.ico'))
    # window.show()
    if os.path.exists('author.dll') != True:
        with open('author.dll', 'w') as file:
            file.write('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0aW1lIjoiMjAwMC0wMS0wMSIsIm1hY2hpbmVudW1iZXIiOiJZTFgzQVRORCJ9.Zf4mBuTA0JUFZ9tyATSD2HdAHvKfaXxGg8KgiFfGBRw')
    
    with open('author.dll', 'r') as file:
        serialnumber = file.read()
    status_authorization = check_activation(serialnumber)
    # status_authorization = check_activation('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0aW1lIjoiMjAyMy0wMS0xMyIsIm1hY2hpbmVudW1iZXIiOiJZTFgzQVRORCJ9.ewJ8a7lUE7-GbLoglAs_MA1cVfquaU52zBwlWL8G98Q')
    if (status_authorization != 'yes'):
        timer = QTimer()
        timer.timeout.connect(activation)  # Connect the timer timeout signal to the update_label_text function
        timer.start(500)
        license_window.show()
    else :
        window.show()
    app.exec()