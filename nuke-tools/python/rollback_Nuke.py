import common_Nuke as common
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import nuke
import os, glob, shutil
import utilities as amu

CHECKOUT_WINDOW_WIDTH = 300
CHECKOUT_WINDOW_HEIGHT = 400

class RollbackDialog(QDialog):
	def get_file_path(self):
		return nuke.callbacks.filenameFilter( nuke.root().name() )

	def __init__(self, parent=QApplication.activeWindow()):
		#def setup(self, parent):
		self.ORIGINAL_FILE_NAME = common.get_file_path()
		self.rollback_controller = RollbackController(self)
		QDialog.__init__(self, parent)
		self.setWindowTitle('Rollback')
		self.setFixedSize(CHECKOUT_WINDOW_WIDTH, CHECKOUT_WINDOW_HEIGHT)		
		self.create_layout()
		self.create_connections()
		self.rollback_controller.populate_list()
  
	def create_layout(self):
		#Create the selected item list
		self.selection_list = QListWidget()
		self.selection_list.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding) 

		#Create Select and Cancel buttons
		self.help_button = QPushButton('Help')
		self.checkout_button = QPushButton('Checkout')
		self.cancel_button = QPushButton('Cancel')

		#Create button layout
		button_layout = QHBoxLayout()
		button_layout.setSpacing(2)
		button_layout.addStretch()
		button_layout.addWidget(self.checkout_button)
		button_layout.addWidget(self.cancel_button)

		#Create main layout
		main_layout = QVBoxLayout()
		main_layout.setSpacing(2)
		main_layout.setMargin(2)
		main_layout.addWidget(self.selection_list)
		main_layout.addWidget(self.help_button)
		main_layout.addLayout(button_layout)
		
		self.setLayout(main_layout)

	def create_connections(self):
		#Connect the selected item list widget
		self.connect(self.selection_list,
					SIGNAL('currentItemChanged(QListWidgetItem*, QListWidgetItem*)'),
					self.set_current_item)
			
		#Connect the buttons
		self.connect(self.help_button, SIGNAL('clicked()'), self.help_button_clicked)
		self.connect(self.checkout_button, SIGNAL('clicked()'), self.checkout_button_clicked)
		self.connect(self.cancel_button, SIGNAL('clicked()'), self.close_button_clicked)

	def help_button_clicked(self):
		self.rollback_controller.help_button_clicked()

	def checkout_button_clicked(self):
		self.rollback_controller.checkout_button_clicked()

	def close_button_clicked(self):
		self.rollback_controller.close_button_clicked()


	def populate_list(self):
		self.rollback_controller.populate_list()

	def set_current_item(self, item):
		self.current_item = item

	def get_current_item(self):
		return str(self.current_item.text())

	def set_list(self, asset_list):
		self.selection_list.clear()
		for s in asset_list:
			item = QListWidgetItem(s)
			item.setText(s)
			self.selection_list.addItem(item)

class RollbackController:
	def __init__(self, rollback_dialog):
		self.rollback_dialog = rollback_dialog
		toCheckin = common.get_checkin_path()

	def help_button_clicked(self):
		nuke.message("See Nathan: nbstandiford@gmail.com")

	def checkout_button_clicked(self):
		version = self.rollback_dialog.get_current_item()[1:]
		filePath = common.get_checkin_path()
		toCheckout = amu.getCheckinDest(filePath)
		
		latestVersion = amu.tempSetVersion(toCheckout, version)
		amu.discard(filePath)
		try:
			destpath = amu.checkout(toCheckout, True)
		except Exception as e:
			if not amu.checkedOutByMe(toCheckout):
				muke.message(str(e))
				return
			else:
				destpath = amu.getCheckoutDest(toCheckout)

		amu.tempSetVersion(toCheckout, latestVersion)
		# move to correct checkout directory
		correctCheckoutDir = amu.getCheckoutDest(toCheckout)
		if not destpath == correctCheckoutDir:
			if os.path.exists(correctCheckoutDir):
				shutil.rmtree(correctCheckoutDir)
			os.rename(destpath, correctCheckoutDir)
		toOpen = os.path.join(correctCheckoutDir, self.get_filename(toCheckout)+'.nk')
		if not os.path.exists(toOpen):
			# create new file
			nuke.scriptNew()
			nuke.scriptSaveAs(filename=toOpen, overwrite=0)
		else:
			nuke.scriptOpen(toOpen)
		self.rollback_dialog.close()

	def close_button_clicked(self):
		self.rollback_dialog.close()

	def populate_list(self):
		filePath = common.get_checkin_path()
		checkInDest = amu.getCheckinDest(filePath)
		versionFolders = os.path.join(checkInDest, "src")
		selections = glob.glob(os.path.join(versionFolders, '*'))
		selections = [os.path.basename(selection) for selection in selections]
		self.rollback_dialog.set_list(selections)

	def get_filename(self, parentdir):
		return os.path.basename(os.path.dirname(parentdir))+'_'+os.path.basename(parentdir)

def rollback():
	if common.can_checkin():
		rollback_dialog = RollbackDialog()
		rollback_dialog.exec_()
	else:
		nuke.message("cannot rollback file: not versioned")

def go():
	rollback()
