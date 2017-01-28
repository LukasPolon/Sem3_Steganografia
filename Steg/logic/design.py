# -*- coding: utf-8 -*-
import os
import PyQt4
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QPixmap
from PyQt4.QtCore import Qt
import steganography
from crypto import Crypto
from PIL import Image

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1257, 600)

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(
                                                        20, 10, 1001, 541))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8(
                                                    "horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        
        self.picture_before = QtGui.QLabel(self.horizontalLayoutWidget)
        self.picture_before.setObjectName(_fromUtf8("picture_before"))
        self.horizontalLayout.addWidget(self.picture_before)
        
        self.picture_after = QtGui.QLabel(self.horizontalLayoutWidget)
        self.picture_after.setObjectName(_fromUtf8("picture_after"))
        self.horizontalLayout.addWidget(self.picture_after)

        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(1040, 10, 211, 541))
        self.verticalLayoutWidget.setObjectName(_fromUtf8(
                                                "verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        
        self.load_file_button = QtGui.QPushButton(self.verticalLayoutWidget)
        self.load_file_button.setObjectName(_fromUtf8("load_file_button"))
        self.verticalLayout.addWidget(self.load_file_button)
        self.verticalLayout.addWidget(self.load_file_button)
        
        self.save_changed_file_button = QtGui.QPushButton(
                                                    self.verticalLayoutWidget)
        self.save_changed_file_button.setObjectName(
                                        _fromUtf8("save_changed_file_button"))
        self.verticalLayout.addWidget(self.save_changed_file_button)

        self.insert_text_button = QtGui.QPushButton(self.verticalLayoutWidget)
        self.insert_text_button.setObjectName(_fromUtf8("insert_text_button"))
        self.verticalLayout.addWidget(self.insert_text_button)

        self.inserted_text = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.read_text = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.inserted_text.setObjectName(_fromUtf8("inserted_text"))
        self.verticalLayout.addWidget(self.inserted_text)
        
        self.read_text_button = QtGui.QPushButton(self.verticalLayoutWidget)
        self.read_text_button.setObjectName(_fromUtf8("read_text_button"))
        self.verticalLayout.addWidget(self.read_text_button)
        self.read_text.setObjectName(_fromUtf8("read_text"))
        self.verticalLayout.addWidget(self.read_text)
        
        self.horizontalLayoutWidget.raise_()
        self.picture_after.raise_()
        self.verticalLayoutWidget.raise_()
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1257, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))

        self.picture_before.setText(_translate("MainWindow", "picture_before", None))


        self.picture_after.setText(_translate("MainWindow", "picture_after", None))

        self.load_file_button.setText(_translate("MainWindow", "Load file", None))
        self.load_file_button.clicked.connect(self.select_file_before)

        self.save_changed_file_button.setText(_translate("MainWindow", "Save changed file", None))
        self.insert_text_button.setText(_translate("MainWindow", "Insert text", None))

        self.insert_text_button.clicked.connect(self.InsertText)
        self.read_text_button.clicked.connect(self.readtext)

        self.read_text_button.setText(_translate("MainWindow", "Read text", None))

    def select_file_before(self):
        self.img_obj = QtGui.QFileDialog.getOpenFileName(self, 'OpenFile')
        self.display_picture(self.img_obj, 'before')

    def select_file_after(self, filename):
        img_after = QtGui.QPixmap(filename)
        self.display_picture(img_after, 'after')

    def display_picture(self, img_obj, aft_bef):
        image_profile = QtGui.QImage(img_obj)
        image_profile = image_profile.scaled(600, 500,
                                             QtCore.Qt.KeepAspectRatio,
                                             QtCore.Qt.SmoothTransformation)
        if aft_bef == 'before':
            self.picture_before.setPixmap(QPixmap.fromImage(image_profile))
        elif aft_bef == 'after':
            self.picture_after.setPixmap(
                QPixmap.fromImage(image_profile))

    def InsertText(self):
        img = Image.open(str(self.img_obj))
        passwd = self.read_text.text()
        text = self.inserted_text.text()
        enc = Crypto(passwd, msg=text)
        enc_text = enc.encrypt()
        steg = steganography.Steganography(img, message=enc_text)

        path = str(self.img_obj)
        filename = path.split('/')
        fn = filename.pop()
        fn = 'enc_' + fn
        filename.append(fn)
        new_path = os.path.join(*filename)
        new_path = '/' + new_path
        img_enc = steg.encode_image()
        img_enc.save(new_path)

        self.select_file_after(new_path)

    def readtext(self):
        img = Image.open(str(self.img_obj))
        passwd = self.read_text.text()
        steg = steganography.Steganography(img)
        msg = steg.decode_image()

        decr = Crypto(passwd, enc_msg=msg)
        end_msg = decr.decrypt()

        self.inserted_text.setText(end_msg)

