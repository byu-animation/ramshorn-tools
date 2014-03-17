# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'issue_form.ui'
#
# Created: Wed Mar 12 17:43:20 2014
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_IssueForm(object):
    def setupUi(self, IssueForm):
        IssueForm.setObjectName("IssueForm")
        IssueForm.resize(501, 405)
        self.lblSummary = QtGui.QLabel(IssueForm)
        self.lblSummary.setGeometry(QtCore.QRect(10, 51, 71, 20))
        self.lblSummary.setObjectName("lblSummary")
        self.txtSummary = QtGui.QLineEdit(IssueForm)
        self.txtSummary.setGeometry(QtCore.QRect(90, 50, 411, 23))
        self.txtSummary.setObjectName("txtSummary")
        self.cboAsset = QtGui.QComboBox(IssueForm)
        self.cboAsset.setGeometry(QtCore.QRect(90, 70, 411, 24))
        self.cboAsset.setEditable(True)
        self.cboAsset.setInsertPolicy(QtGui.QComboBox.InsertAlphabetically)
        self.cboAsset.setObjectName("cboAsset")
        self.lblAsset = QtGui.QLabel(IssueForm)
        self.lblAsset.setGeometry(QtCore.QRect(10, 70, 71, 21))
        self.lblAsset.setFrameShape(QtGui.QFrame.NoFrame)
        self.lblAsset.setObjectName("lblAsset")
        self.lblPriority = QtGui.QLabel(IssueForm)
        self.lblPriority.setGeometry(QtCore.QRect(10, 90, 71, 31))
        self.lblPriority.setObjectName("lblPriority")
        self.cboPriority = QtGui.QComboBox(IssueForm)
        self.cboPriority.setGeometry(QtCore.QRect(90, 95, 121, 24))
        self.cboPriority.setObjectName("cboPriority")
        self.lblDetail = QtGui.QLabel(IssueForm)
        self.lblDetail.setGeometry(QtCore.QRect(10, 120, 491, 16))
        self.lblDetail.setObjectName("lblDetail")
        self.txtDetail = QtGui.QPlainTextEdit(IssueForm)
        self.txtDetail.setGeometry(QtCore.QRect(0, 140, 501, 241))
        self.txtDetail.setCenterOnScroll(False)
        self.txtDetail.setObjectName("txtDetail")
        self.btnSubmit = QtGui.QPushButton(IssueForm)
        self.btnSubmit.setGeometry(QtCore.QRect(400, 380, 100, 24))
        self.btnSubmit.setObjectName("btnSubmit")
        self.btnCancel = QtGui.QPushButton(IssueForm)
        self.btnCancel.setGeometry(QtCore.QRect(300, 380, 100, 24))
        self.btnCancel.setObjectName("btnCancel")
        self.txtName = QtGui.QLineEdit(IssueForm)
        self.txtName.setGeometry(QtCore.QRect(90, 10, 411, 23))
        self.txtName.setObjectName("txtName")
        self.lblName = QtGui.QLabel(IssueForm)
        self.lblName.setGeometry(QtCore.QRect(10, 10, 81, 21))
        self.lblName.setObjectName("lblName")
        self.txtEmail = QtGui.QLineEdit(IssueForm)
        self.txtEmail.setGeometry(QtCore.QRect(90, 30, 411, 23))
        self.txtEmail.setObjectName("txtEmail")
        self.lblEmail = QtGui.QLabel(IssueForm)
        self.lblEmail.setGeometry(QtCore.QRect(10, 30, 71, 20))
        self.lblEmail.setObjectName("lblEmail")

        self.retranslateUi(IssueForm)
        QtCore.QMetaObject.connectSlotsByName(IssueForm)

    def retranslateUi(self, IssueForm):
        IssueForm.setWindowTitle(QtGui.QApplication.translate("IssueForm", "Submit An Issue", None, QtGui.QApplication.UnicodeUTF8))
        self.lblSummary.setText(QtGui.QApplication.translate("IssueForm", "Summary:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblAsset.setText(QtGui.QApplication.translate("IssueForm", "Asset:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblPriority.setText(QtGui.QApplication.translate("IssueForm", "Priority:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblDetail.setText(QtGui.QApplication.translate("IssueForm", "Describe the issue you are encountering in detail:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSubmit.setText(QtGui.QApplication.translate("IssueForm", "Submit", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("IssueForm", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.lblName.setText(QtGui.QApplication.translate("IssueForm", "Your Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblEmail.setText(QtGui.QApplication.translate("IssueForm", "Email:", None, QtGui.QApplication.UnicodeUTF8))

