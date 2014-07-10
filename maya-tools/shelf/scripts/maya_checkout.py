from PyQt4.QtCore import *
from PyQt4.QtGui import *

import maya.cmds as cmd
import maya.OpenMayaUI as omu
import sip
import os, glob
import shutil
import utilities as amu

CHECKOUT_WINDOW_WIDTH = 340
CHECKOUT_WINDOW_HEIGHT = 575

def maya_main_window():
	ptr = omu.MQtUtil.mainWindow()
	return sip.wrapinstance(long(ptr), QObject)

class CheckoutContext:
	def __init__(self, parent, name, folder, asset_folder, can_create):
		# name of this checkout context (i.e. Model, Rig, Animation)
		self.name = name
		# pathname to folder location (same as os.environ variable)
		self.folder = folder
		# folder location for the actual scene file to checkout
		self.asset_folder = asset_folder;
		# enable a New/Create button for this context
		self.can_create = can_create
		# intialize self.tree (the widget)
		self.get_items(parent)
		# no filtering, to start out with
		self.cur_filter = ''

	def get_items(self, parent):
		# creates a QTreeWidget with the items to checkout
		self.tree = QListWidget()
		#self.tree.setColumnCount(1)
		self.tree.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
		folders = glob.glob(os.path.join(self.folder, '*'))
		for f in folders:
			bname = os.path.basename(f)
			item = QListWidgetItem(bname)
			item.setText(bname)
			self.tree.addItem(item)
		self.tree.sortItems(0)
		self.tree.setSortingEnabled(True)
		# bind selection handler
		self.tree.currentItemChanged.connect(parent.set_current_item)

	def add_item(self, name):
		# adds an item to the tree, with the given folder basename
		item = QListWidgetItem(name)
		item.setText(name)
		self.tree.addItem(item)

	def search(self, key):
		# cache the old search key, so we don't perform unnecessary re-filtering
		if self.cur_filter != key:
			self.cur_filter = key
			# search the list, show only the ones that match
			# returns the index of the first valid result; -1 if no matches
			first_result = key == ''
			count = self.tree.count()
			idx = 0
			while idx < count:
				item = self.tree.item(idx)
				show = key == '' or key in item.text()
				# auto-select the first search result
				if show and not first_result:
					first_result = True
					self.tree.setCurrentItem(item)
				self.tree.setRowHidden(idx, not show)
				idx += 1
			# no results, hide selection
			if not first_result:
				self.tree.setCurrentItem(None)
		


class CheckoutDialog(QDialog):
	def __init__(self, parent=maya_main_window()):
		#Setup the different checkout contexts
		self.contexts = [
			CheckoutContext(self, 'Model', os.environ['ASSETS_DIR'], 'model', False),
			CheckoutContext(self, 'Rig', os.environ['ASSETS_DIR'], 'rig', False),
			CheckoutContext(self, 'Animation', os.environ['SHOTS_DIR'], 'animation', True),
			CheckoutContext(self, 'Previs', os.environ['PREVIS_DIR'], 'animation', True)
		]

		#Initialize the GUI
		QDialog.__init__(self, parent)
		self.setWindowTitle('Checkout')
		self.setFixedSize(CHECKOUT_WINDOW_WIDTH, CHECKOUT_WINDOW_HEIGHT)
		self.create_layout()
		self.create_connections()
		self.refresh()
	
	def create_layout(self):
		#Create tabbed view
		self.context_tabs = QTabWidget()
		for context in self.contexts:
			self.context_tabs.addTab(context.tree, context.name)

		#Search input box
		self.search_bar = QLineEdit()
		search_layout = QHBoxLayout()
		search_layout.addWidget(QLabel("Filter: "))
		search_layout.addWidget(self.search_bar)

		#Create Label to hold asset info
		self.asset_info_label = QLabel()
		self.asset_info_label.setWordWrap(True)

		#Create action buttons
		self.new_button = QPushButton('New')
		self.unlock_button = QPushButton('Unlock')
		self.checkout_button = QPushButton('Checkout')
		self.cancel_button = QPushButton('Cancel')
		
		#Create button layout
		button_layout = QHBoxLayout()
		button_layout.setSpacing(2)

		button_layout.addWidget(self.new_button)
		button_layout.addWidget(self.unlock_button)
		button_layout.addStretch()
		button_layout.addWidget(self.checkout_button)
		button_layout.addWidget(self.cancel_button)
		
		#Create main layout
		main_layout = QVBoxLayout()
		main_layout.setSpacing(5)
		main_layout.setMargin(6)
		main_layout.addLayout(search_layout)
		main_layout.addWidget(self.context_tabs)
		main_layout.addWidget(self.asset_info_label)
		main_layout.addLayout(button_layout)
		
		self.setLayout(main_layout)

	def create_connections(self):
		#Change checkout context
		self.context_tabs.currentChanged.connect(self.refresh)

		#Search bar
		self.search_bar.textChanged.connect(self.search)

		#Connect the buttons
		self.new_button.clicked.connect(self.new_animation)
		self.unlock_button.clicked.connect(self.unlock)
		self.checkout_button.clicked.connect(self.checkout)
		self.cancel_button.clicked.connect(self.close_dialog)
	
	def search(self, key):
		self.context.search(key)

	def refresh(self):
		# set the new context
		self.context = self.contexts[self.context_tabs.currentIndex()]
		# apply search filtering
		self.search(self.search_bar.text())
		# toggles the "New" button
		self.new_button.setEnabled(self.context.can_create)
		# refresh selection
		self.set_current_item(self.context.tree.currentItem())

	def new_animation(self):
		text, ok = QInputDialog.getText(self, 'New Shot', 'Enter seq_shot (ie: a01)')
		if ok:
			text = str(text)
			if self.context.name == 'Previs':
				amu.createNewPrevisFolders(self.context.folder, text)
			else:
				amu.createNewShotFolders(self.context.folder, text)
			self.copy_template_animation(text)
			self.context.add_item(text)
			self.refresh()
		return

	def copy_template_animation(self, shot_name):
		template = os.path.join(os.environ['SHOTS_DIR'], 'static/animation/stable/static_animation_stable.mb')
		if(os.path.exists(template)):
			dest = os.path.join(self.context.folder, shot_name, 'animation/src/v000/'+shot_name+'_animation.mb')
			shutil.copyfile(template, dest)
			print 'copied '+template+' to '+dest
		return
	
	def get_filename(self, parentdir):
		return os.path.basename(os.path.dirname(parentdir))+'_'+os.path.basename(parentdir)

	def get_asset_path(self):
		# returns the path for a single asset
		asset_name = str(self.current_item.text())
		return os.path.join(self.context.folder, asset_name, self.context.asset_folder)

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
		print("unlocking!!!!")
		
		toUnlock = self.get_asset_path()
		if amu.isLocked(toUnlock):
			if self.showConfirmUnlockDialog() == 'No':
				return
			if cmd.file(q=True, sceneName=True) != "":
				cmd.file(save=True, force=True)	
			cmd.file(force=True, new=True) #open new file
			amu.unlock(toUnlock)
			self.showUnlockedDialog()	
		else:
			self.showIsLockedDialog()
		#Update node info
		self.show_node_info()
		

	
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
			cmd.viewClipPlane('perspShape', ncp=0.01)
			cmd.file(save=True, force=True)
		
		self.close_dialog()
	
	def close_dialog(self):
		self.close()
	
	def set_current_item(self, item):
		self.current_item = item
		self.checkout_button.setEnabled(not not item)
		if not item:
			self.asset_info_label.hide()
			self.unlock_button.setEnabled(False)
		else:
			self.asset_info_label.show()
			self.show_node_info()
		
	def show_node_info(self):
		filePath = self.get_asset_path()
		node_info = amu.getVersionedFolderInfo(filePath)
		checkout_str = node_info[0]
		self.unlock_button.setEnabled(checkout_str != '')
		if (checkout_str == ''):
			checkout_str = '<font color="#6EFF81">Not checked out.</font>'
		else:
			checkout_str = '<font color="#FF6E6E">Checked out by '+node_info[0]+'.</font>'
		#checkin_str = '<br/>Last checked in by '+node_info[1]+' on '+node_info[2]
		checkin_str = '<br/>Last checkin: ' + node_info[3]
		self.asset_info_label.setText(checkout_str+checkin_str)
		
def go():
	dialog = CheckoutDialog()
	dialog.show()
	
if __name__ == '__main__':
	go()
	
	
	
	
	
	
	
	
	
	
