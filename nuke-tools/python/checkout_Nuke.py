from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import os, glob
import utilities as amu
import nuke

class CheckoutDialog(QDialog):

	def __init__(self, parent=QApplication.activeWindow()):
		QDialog.__init__(self, parent)
		self.checkout_controller = CheckoutController(self)
		self.create_layout()
		self.create_connections()
		self.populate_list()	

	def create_layout(self):
		self.selection_list = QListWidget()
		self.select_button = QPushButton('Select')
		self.info_button = QPushButton('Get Info')
		self.unlock_button = QPushButton('Unlock')
		self.cancel_button = QPushButton('Cancel')
		
		button_layout = QVBoxLayout()
		button_layout.setSpacing(2)
		button_layout.addStretch()
		button_layout.addWidget(self.select_button)
		button_layout.addWidget(self.info_button)
		button_layout.addWidget(self.unlock_button)
		button_layout.addWidget(self.cancel_button)
		
		main_layout = QVBoxLayout()
		main_layout.setSpacing(2)
		main_layout.setMargin(10)
		main_layout.addWidget(self.selection_list)
		main_layout.addLayout(button_layout)
		self.setLayout(main_layout)

	def create_connections(self):
		self.connect(self.selection_list, SIGNAL('currentItemChanged(QListWidgetItem*, QListWidgetItem*)'), self.set_current_item)
		self.connect(self.select_button, SIGNAL('clicked()'), self.select_clicked)
		self.connect(self.unlock_button, SIGNAL('clicked()'), self.unlock_button_clicked)
		#self.connect(self.info_button, SIGNAL('clicked()'), self.show_node_info)
		self.connect(self.cancel_button, SIGNAL('clicked()'), self.cancel_clicked)

	def set_list(self, asset_list):
		for s in asset_list:
			item = QListWidgetItem(s)
			item.setText(s)
			self.selection_list.addItem(item)

	def cancel_clicked(self):
		self.checkout_controller.cancel_clicked()

	def select_clicked(self):
		self.checkout_controller.select_clicked()

	def unlock_button_clicked(self):
		self.checkout_controller.unlock_button_clicked()

	def close_dialog(self):
		self.close()
	
	def populate_list(self):
		self.checkout_controller.populate_list()
		#selection = glob.glob(os.path.join(os.environ['SHOTS_DIR'], '*'))
		#for s in selection:
		#	item = QListWidgetItem(os.path.basename(s))
		#	item.setText(os.path.basename(s))
		#	self.selection_list.addItem(item)
		#self.selection_list.sortItems(0)

	def set_current_item(self, item):
		self.current_item = item

	def get_current_item(self):
		return str(self.current_item.text())

	def show_confirm_unlock_dialog(self):
		return nuke.ask('Are you sure you want to unlock this asset?')
	
	def show_message(self, text):
		nuke.message(text)

class CheckoutController:

	def __init__(self, checkout_dialog):
		self.checkout_dialog = checkout_dialog

	def select_clicked(self):
		self.checkout()
		self.checkout_dialog.close_dialog()

	def cancel_clicked(self):
		self.checkout_dialog.close_dialog()
	
	def item_selection_changed(self):
		pass #TODO: do something useful here

	def get_filename(self, parentdir):
		return os.path.basename(os.path.dirname(parentdir))+'_'+os.path.basename(parentdir)

	def populate_list(self):
		asset_list = []
		selection = glob.glob(os.path.join(os.environ['SHOTS_DIR'], '*'))
		
		for s in selection:
			asset_list.append(os.path.basename(s))
		asset_list.sort()
		self.checkout_dialog.set_list(asset_list)
	
	def get_asset_path(self):
		asset_name = self.checkout_dialog.get_current_item()
		return os.path.join(os.environ['SHOTS_DIR'], asset_name,'compositing')

	def checkout(self):
		asset_name = self.checkout_dialog.get_current_item()
		toCheckout = os.path.join(os.environ['SHOTS_DIR'], asset_name,'compositing')
		#nuke.message(toCheckout)
		try:
			destpath = amu.checkout(toCheckout, True)
			#nuke.message(destpath)		
		except Exception as e:
			if not amu.checkedOutByMe(toCheckout):
				nuke.message(str(e))
				return
			else:
				destpath = amu.getCheckoutDest(toCheckout)
				#nuke.message("destpath = " + destpath)
		toOpen = os.path.join(destpath,self.get_filename(toCheckout)+'.nk')
		#nuke.message(toOpen)
		#nuke.message("toOpen = " + toOpen)
		#nuke.scriptClose()
		if not os.path.exists(toOpen):
			nuke.scriptClear()
			nuke.scriptSaveAs(filename=toOpen, overwrite=1)
		else:
			nuke.scriptClear()
			nuke.scriptOpen(toOpen)
		nuke.message('Checkout Successful')

	def unlock_button_clicked(self):
		toUnlock = self.get_asset_path()
		
		if amu.isLocked(toUnlock):
			if self.checkout_dialog.show_confirm_unlock_dialog() == False:
				return
			amu.unlock(toUnlock)
			self.checkout_dialog.show_message("Asset unlocked")		
		else:
			self.checkout_dialog.show_message("Asset not locked")


def go():
	#nuke.message("go")
	dialog = CheckoutDialog()
	#dialog.show()
	dialog.exec_()
	#nuke.message("done")
