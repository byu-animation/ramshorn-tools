from PyQt4.QtCore import *
from PyQt4.QtGui import *

import maya.cmds as cmd
import maya.OpenMayaUI as omu
import sip
import os, glob, shutil
import utilities as amu

from ui_issue_form import Ui_IssueForm

def maya_main_window():
	ptr = omu.MQtUtil.mainWindow()
	return sip.wrapinstance(long(ptr), QObject)

class IssueForm(QDialog):
	def __init__(self, parent=maya_main_window()):
		QDialog.__init__(self,parent)		
		self.ui = Ui_IssueForm()
		self.ui.setupUi(self)
		self.ui.cboAsset.autoCompletion = True
		self.ui.btnSubmit.clicked.connect(self.submit)
		self.ui.btnCancel.clicked.connect(self.cancel)
		self.populate()

	def populate(self):
		priorities = ['(none)','Low','High']
		self.ui.cboPriority.addItems(priorities)
		folders = glob.glob(os.path.join(os.environ['ASSETS_DIR'],'*'))
		names = []
		for f in folders:
			name = os.path.basename(f)
			self.ui.cboAsset.addItem(name)

	def getSubject(self):
		return '[ramshorn-issue] ' + self.ui.txtSummary.text()

	def getMessage(self):
		message = """
Submitter Name: %s
Email: %s
Asset: %s
Priority: %s

%s
		""" % (str(self.ui.txtName.text())
			   , str(self.ui.txtEmail.text())
			   , str(self.ui.cboAsset.currentText())
			   , str(self.ui.cboPriority.currentText())
			   , str(self.ui.txtDetail.toPlainText())
			   )
		return message

	def submit(self):
		subject = self.getSubject()
		message_text = self.getMessage()
		success = False
		retries = 0
		while (success is False or retries < 3):
			success = amu.sendmail(subject, message_text)
			retries += 1
		if (success is True):
			self.close()
		else:
			cmds.confirmDialog(  title         = 'Cannot Send'
							   , message       = 'Cannot send after 3 attempts. Please try again later.'
							   , button        = ['Ok']
							   , defaultButton = 'Ok'
							   , cancelButton  = 'Ok'
							   , dismissString = 'Ok')

	def cancel(self):
		self.close()

def go():
	dialog = IssueForm()
	dialog.show()

if __name__ == '__main__':
	go()
