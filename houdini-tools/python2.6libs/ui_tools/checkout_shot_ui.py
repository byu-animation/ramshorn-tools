# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'checkout_shot.ui'
#
# Created: Wed Sep 17 15:24:52 2014
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_CheckoutShotDialog(object):
    def setupUi(self, CheckoutShotDialog):
        CheckoutShotDialog.setObjectName("CheckoutShotDialog")
        CheckoutShotDialog.resize(441, 298)
        self.buttonBox = QtGui.QDialogButtonBox(CheckoutShotDialog)
        self.buttonBox.setGeometry(QtCore.QRect(0, 260, 431, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.rdbLightingFile = QtGui.QRadioButton(CheckoutShotDialog)
        self.rdbLightingFile.setGeometry(QtCore.QRect(0, 230, 111, 23))
        self.rdbLightingFile.setAcceptDrops(False)
        self.rdbLightingFile.setAutoFillBackground(False)
        self.rdbLightingFile.setChecked(True)
        self.rdbLightingFile.setObjectName("rdbLightingFile")
        self.rdbFxFile = QtGui.QRadioButton(CheckoutShotDialog)
        self.rdbFxFile.setGeometry(QtCore.QRect(110, 230, 119, 23))
        self.rdbFxFile.setChecked(False)
        self.rdbFxFile.setObjectName("rdbFxFile")
        self.lwShots = QtGui.QListWidget(CheckoutShotDialog)
        self.lwShots.setGeometry(QtCore.QRect(0, 0, 131, 221))
        self.lwShots.setObjectName("lwShots")
        self.lblShot = QtGui.QLabel(CheckoutShotDialog)
        self.lblShot.setGeometry(QtCore.QRect(140, 10, 171, 18))
        self.lblShot.setObjectName("lblShot")
        self.txtDescription = QtGui.QTextBrowser(CheckoutShotDialog)
        self.txtDescription.setGeometry(QtCore.QRect(140, 30, 301, 181))
        self.txtDescription.setObjectName("txtDescription")
        self.btnUnlock = QtGui.QPushButton(CheckoutShotDialog)
        self.btnUnlock.setGeometry(QtCore.QRect(330, 220, 102, 31))
        self.btnUnlock.setObjectName("btnUnlock")

        self.retranslateUi(CheckoutShotDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), CheckoutShotDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), CheckoutShotDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CheckoutShotDialog)

    def retranslateUi(self, CheckoutShotDialog):
        CheckoutShotDialog.setWindowTitle(QtGui.QApplication.translate("CheckoutShotDialog", "Checkout Shot", None, QtGui.QApplication.UnicodeUTF8))
        self.rdbLightingFile.setText(QtGui.QApplication.translate("CheckoutShotDialog", "Lighting", None, QtGui.QApplication.UnicodeUTF8))
        self.rdbFxFile.setText(QtGui.QApplication.translate("CheckoutShotDialog", "FX", None, QtGui.QApplication.UnicodeUTF8))
        self.lblShot.setText(QtGui.QApplication.translate("CheckoutShotDialog", "Current Shot: <shot>", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUnlock.setText(QtGui.QApplication.translate("CheckoutShotDialog", "Unlock", None, QtGui.QApplication.UnicodeUTF8))

