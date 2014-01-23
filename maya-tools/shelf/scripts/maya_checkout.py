from PyQt4.QtCore import *
from PyQt4.QtGui import *

import maya.cmds as cmd
import maya.OpenMayaUI as omu
import sip
import os, glob
import utilities as amu

CHECKOUT_WINDOW_WIDTH = 330
CHECKOUT_WINDOW_HEIGHT = 620

def maya_main_window():
	ptr = omu.MQtUtil.mainWindow()
	return sip.wrapinstance(long(ptr), QObject)		

class CheckoutDialog(QDialog):
	def __init__(self, parent=maya_main_window()):
	#def setup(self, parent):
		QDialog.__init__(self, parent)
		self.setWindowTitle('Checkout')
		self.setFixedSize(CHECKOUT_WINDOW_WIDTH, CHECKOUT_WINDOW_HEIGHT)
		self.create_layout()
		self.create_connections()
		self.refresh()
	
	def create_layout(self):
		#Create the selected item list
		self.selection_list = QListWidget()
		self.selection_list.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)	

		#Create Models, Rig, Animation, Previs
		radio_button_group = QHBoxLayout()
		self.model_radio = QRadioButton('Model')
		self.rig_radio = QRadioButton('Rig')
		self.animation_radio = QRadioButton('Animation')
		self.previs_radio = QRadioButton('Previs')
		self.model_radio.setChecked(True)
		radio_button_group.setSpacing(2)
		radio_button_group.addWidget(self.model_radio)
		radio_button_group.addWidget(self.rig_radio)
		radio_button_group.addWidget(self.animation_radio)
		radio_button_group.addWidget(self.previs_radio)

		#Create Label to hold asset info
		self.asset_info_label = QLabel("test")
		self.asset_info_label.setWordWrap(True)

		#Create New Shot button; used by Animation & Previs modes
		self.new_shot_button = QPushButton('New Shot')
		
		#Create Unlock button
		self.unlock_button = QPushButton('Unlock')

		#Create Select and Cancel buttons
		self.select_button = QPushButton('Select')
		self.cancel_button = QPushButton('Cancel')
		
		#Create button layout
		button_layout = QHBoxLayout()
		button_layout.setSpacing(2)
		button_layout.addStretch()
	
		button_layout.addWidget(self.select_button)
		button_layout.addWidget(self.unlock_button)
		button_layout.addWidget(self.cancel_button)
		
		#Create main layout
		main_layout = QVBoxLayout()
		main_layout.setSpacing(2)
		main_layout.setMargin(2)
		main_layout.addWidget(self.selection_list)
		#add text box to main layout to display info when asset is selected
		main_layout.addWidget(self.asset_info_label)		
		main_layout.addLayout(radio_button_group)
		main_layout.addWidget(self.new_shot_button)
		main_layout.addLayout(button_layout)
		
		self.setLayout(main_layout)
	
	def create_connections(self):
		#Connect the selected item list widget
		self.connect(self.selection_list,
					SIGNAL('currentItemChanged(QListWidgetItem*, QListWidgetItem*)'),
					self.set_current_item)
			
		#Connect the buttons
		self.connect(self.model_radio, SIGNAL('clicked()'), self.refresh)
		self.connect(self.rig_radio, SIGNAL('clicked()'), self.refresh)
		self.connect(self.animation_radio, SIGNAL('clicked()'), self.refresh)
		self.connect(self.previs_radio, SIGNAL('clicked()'), self.refresh)
		self.connect(self.new_shot_button, SIGNAL('clicked()'), self.new_animation)
		self.connect(self.unlock_button, SIGNAL('clicked()'), self.unlock)
		self.connect(self.select_button, SIGNAL('clicked()'), self.checkout)
		self.connect(self.cancel_button, SIGNAL('clicked()'), self.close_dialog)
	
	def update_selection(self, selection):
		#Remove all items from the list before repopulating
		self.selection_list.clear()
		#Clear info displayed about asset
		self.asset_info_label.clear()
		
		#Add the list to select from
		for s in selection:
			item = QListWidgetItem(os.path.basename(s)) 
			item.setText(os.path.basename(s))
			self.selection_list.addItem(item)
		self.selection_list.sortItems(0)
	
	def refresh(self):
		# updates selection list and toggles the "New Shot" button
		self.new_shot_button.setEnabled(self.animation_radio.isChecked() or self.previs_radio.isChecked())
		selections = glob.glob(os.path.join(self.get_checkout_location(), '*'))
		self.update_selection(selections)
	
	def new_animation(self):
		text, ok = QInputDialog.getText(self, 'New Shot', 'Enter seq_shot (ie: a01)')
		if ok:
			text = str(text)
			if self.previs_radio.isChecked():
				amu.createNewPrevisFolders(os.environ['PREVIS_DIR'], text)
			elif self.animation_radio.isChecked():
				amu.createNewShotFolders(os.environ['SHOTS_DIR'], text)
		self.refresh()
		return
	
	def get_filename(self, parentdir):
		return os.path.basename(os.path.dirname(parentdir))+'_'+os.path.basename(parentdir)

	def get_asset_path(self):
		# returns the path for a single asset
		asset_name = str(self.current_item.text())
		if self.model_radio.isChecked():
			filePath = os.path.join(os.environ['ASSETS_DIR'], asset_name, 'model')
		elif self.rig_radio.isChecked():
			filePath = os.path.join(os.environ['ASSETS_DIR'], asset_name, 'rig')
		elif self.animation_radio.isChecked():
			filePath = os.path.join(os.environ['SHOTS_DIR'], asset_name, 'animation')
		elif self.previs_radio.isChecked():
			filePath = os.path.join(os.environ['PREVIS_DIR'], asset_name, 'animation')
		return filePath

	def get_checkout_location(self):
		# returns the environment path for this checkout mode
		if self.model_radio.isChecked() or self.rig_radio.isChecked():
			return os.environ['ASSETS_DIR']
		if self.animation_radio.isChecked():
			return os.environ['SHOTS_DIR']
		if self.previs_radio.isChecked():
			return os.environ['PREVIS_DIR']
		raise Exception("Unimplemented checkout mode...");

	def showIsLockedDialog(self):
		return cmd.confirmDialog(title = 'Already Unlocked'
                                , message       = 'Asset already unlocked'
                                , button        = ['Ok']
                                , defaultButton = 'Ok'
                                , cancelButton  = 'Ok'
                                , dismissString = 'Ok')

	def showConfirmUnlockDialog(self):
		return cmd.confirmDialog( title = 'Confirmation'
                                 , message       = 'Are you sure you want to unlock this asset?'
                                 , button        = ['Yes', 'No']
                                 , defaultButton = 'No'
                                 , cancelButton  = 'No'
                                 , dismissString = 'No')

	def showUnlockedDialog(self):
		return cmd.confirmDialog(title    = 'Asset unlocked'
		           , message       = 'Asset unlocked'
		           , button        = ['Ok']
		           , defaultButton = 'Ok'
		           , cancelButton  = 'Ok'
		           , dismissString = 'Ok')


	def unlock(self):
		toUnlock = self.get_asset_path()		
		if amu.isLocked(toUnlock):

			if self.showConfirmUnlockDialog() == 'No':
				return
			
			cmd.file(save=True, force=True)
			cmd.file(force=True, new=True) #open new file
			amu.unlock(toUnlock)
			self.showUnlockedDialog()
				
		else:
			self.showIsLockedDialog()

	
	########################################################################
	# SLOTS
	########################################################################
	def checkout(self):
		curfilepath = cmd.file(query=True, sceneName=True)
		if not curfilepath == '':
			cmd.file(save=True, force=True)

		toCheckout = self.get_asset_path()

		try:
			destpath = amu.checkout(toCheckout, True)
		except Exception as e:
			print str(e)
			if not amu.checkedOutByMe(toCheckout):
				cmd.confirmDialog(  title          = 'Can Not Checkout'
                                   , message       = str(e)
                                   , button        = ['Ok']
                                   , defaultButton = 'Ok'
                                   , cancelButton  = 'Ok'
                                   , dismissString = 'Ok')
				return
			else:
				destpath = amu.getCheckoutDest(toCheckout)

		toOpen = os.path.join(destpath, self.get_filename(toCheckout)+'.mb')
		
		# open the file
		if os.path.exists(toOpen):
			cmd.file(toOpen, force=True, open=True)#, loadReferenceDepth="none")
		else:
			# create new file
			cmd.file(force=True, new=True)
			cmd.file(rename=toOpen)
			cmd.file(save=True, force=True)
		self.close_dialog()
	
	def close_dialog(self):
		self.close()
	
	def set_current_item(self, item):
		self.current_item = item
		self.show_node_info()
		
	def show_node_info(self):
		asset_name = str(self.current_item.text())
		filePath = self.get_asset_path();
		node_info = amu.getVersionedFolderInfo(filePath)
		checkout_str = node_info[0]
		if(checkout_str ==''):
			checkout_str = 'Not checked out. '
		else:
			checkout_str = 'Checked out by '+node_info[0]+'. '
		checkin_str = 'Last checked in by '+node_info[1]+' on '+node_info[2]
		
		print 'should clear label'
		self.asset_info_label.setText(checkout_str+checkin_str)
		
def go():
	dialog = CheckoutDialog()
	dialog.show()
	
if __name__ == '__main__':
	go()
	
	
	
	
	
	
	
	
	
	
