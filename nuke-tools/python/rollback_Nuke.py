import common_Nuke as common
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import nuke

CHECKOUT_WINDOW_WIDTH = 300
CHECKOUT_WINDOW_HEIGHT = 400

class RollbackDialog(QDialog):
	def get_file_path(self):
		return nuke.callbacks.filenameFilter( nuke.root().name() )

	def __init__(self, parent=QApplication.activeWindow()):
		#def setup(self, parent):
		self.original_file_name = common.get_file_path()
		self.rollback_controller = RollbackController()
		QDialog.__init__(self, parent)
		self.setWindowTitle('Rollback')
		self.setFixedSize(CHECKOUT_WINDOW_WIDTH, CHECKOUT_WINDOW_HEIGHT)		
		self.create_layout()
		self.create_connections()
  
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
					self.current_item_changed)
			
		#Connect the buttons
		self.connect(self.help_button, SIGNAL('clicked()'), self.help_button_clicked)
		self.connect(self.checkout_button, SIGNAL('clicked()'), self.checkout_button_clicked)
		self.connect(self.cancel_button, SIGNAL('clicked()'), self.close_button_clicked)

	def help_button_clicked(self):
		rollback_controller.help_button_clicked()

	def checkout_button_clicked(self):
		rollback_controller.checkout_button_clicked()

	def close_button_clicked(self):
		rollback_controller.close_button_clicked()

	def current_item_changed(self):
		rollback_controller.current_item_changed()

	def populate_list(self):
		rollback_controller.populate_list()

	def set_current_item(self, item):
		self.current_item = item

	def get_current_item(self):
		return str(self.current_item.text())

	def set_list(asset_list):
		for s in asset_list:
			item = QListWidgetItem(s)
			item.setText(s)
			self.selection_list.addItem(item)

class RollbackController:
	
	def __init__(self, rollback_dialog):
		self.rollback_dialog = rollback_dialog
		pass

	def help_button_clicked(self):
		pass

	def checkout_button_clicked(self):
		pass

	def close_button_clicked(self):
		pass

	def populate_list(self):
		pass

def rollback():
	rollback_dialog = RollbackDialog()
	rollback_dialog.exec_()

def go():
	rollback()
