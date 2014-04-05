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
    def __init__(self, parent, name, folder, asset_folder, can_edit):
        # name of this checkout context (i.e. Model, Rig, Animation)
        self.name = name
        # pathname to folder location (same as os.environ variable)
        self.folder = folder
        # folder location for the actual scene file to checkout
        self.asset_folder = asset_folder;
        # enable a New/Create button for this context
        self.can_edit = can_edit
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
        


class EditShotDialog(QDialog):
    def __init__(self, parent=maya_main_window()):
        #Setup the different checkout contexts
        self.contexts = [
            CheckoutContext(self, 'Animation', os.environ['SHOTS_DIR'], 'animation', False),
            CheckoutContext(self, 'Previs', os.environ['PREVIS_DIR'], 'animation', True)
        ]

        #Initialize the GUI
        QDialog.__init__(self, parent)
        self.setWindowTitle('Edit Shot')
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
        self.rename_button = QPushButton('Rename')
        self.delete_button = QPushButton('Delete')
        self.copy_button = QPushButton('Copy Previs')
        self.cancel_button = QPushButton('Cancel')
        
        #Create button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(2)

        button_layout.addWidget(self.rename_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        button_layout.addWidget(self.copy_button)
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
        self.rename_button.clicked.connect(self.rename)
        self.delete_button.clicked.connect(self.delete)
        self.copy_button.clicked.connect(self.copy)
        self.cancel_button.clicked.connect(self.close_dialog)
    
    def search(self, key):
        self.context.search(key)

    def refresh(self):
        # set the new context
        self.context = self.contexts[self.context_tabs.currentIndex()]
        # apply search filtering
        self.search(self.search_bar.text())
        # toggles the "New" button
        
        # refresh selection
        self.set_current_item(self.context.tree.currentItem())
        # toggles buttons when asset is checked out
        # self.rename_button.setEnabled(self.context.can_edit)
        # self.delete_button.setEnabled(self.context.can_edit)
        self.copy_button.setEnabled(self.context.can_edit)

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
    
    def showErrorDialog(self, message):
        return cmd.confirmDialog(title    = 'Error!'
                   , message       = message
                   , button        = ['Ok']
                   , defaultButton = 'Ok'
                   , cancelButton  = 'Ok'
                   , dismissString = 'Ok')
    
    def showSuccessDialog(self, message):
        return cmd.confirmDialog(title    = 'Success!'
                   , message       = message
                   , button        = ['Ok']
                   , defaultButton = 'Ok'
                   , cancelButton  = 'Ok'
                   , dismissString = 'Ok')
     
    ########################################################################
    # SLOTS
    ########################################################################
    def close_dialog(self):
        self.close()
    
    def set_current_item(self, item):
        self.current_item = item
        # self.copy_button.setEnabled(not not item)
        if not item:
            self.asset_info_label.hide()
            # self.copy_button.setEnabled(False)
        else:
            self.asset_info_label.show()
            self.show_node_info()
        
    def show_node_info(self):
        filePath = self.get_asset_path()
        node_info = amu.getVersionedFolderInfo(filePath)
        checkout_str = node_info[0]
        self.rename_button.setEnabled(checkout_str == '')
        self.delete_button.setEnabled(checkout_str == '')
        if (checkout_str == ''):
            checkout_str = '<font color="#6EFF81">Not checked out.</font>'
        else:
            checkout_str = '<font color="#FF6E6E">Checked out by '+node_info[0]+'.</font>'
        #checkin_str = '<br/>Last checked in by '+node_info[1]+' on '+node_info[2]
        checkin_str = '<br/>Last checkin: ' + node_info[3]
        self.asset_info_label.setText(checkout_str+checkin_str)
    
    def delete(self):
        print 'not implemented!'
    
    def rename(self):
        print 'not implemented!'
    
    def copy(self):
        name = str(self.current_item.text())
        if not name:
           # self.showErrorDialog('select a shot!')
            return
        if not amu.previsToAnim(name):
            self.showErrorDialog("This shot is currently checked out! It must be unlocked before it can be changed.")
            return
        self.close_dialog()
        self.showSuccessDialog("previs was successfuly copied to animation for shot "+name)
        
def go():
    dialog = EditShotDialog()
    dialog.show()
    
if __name__ == '__main__':
    go()
    
    
    
    
    
    
    
    
    
    
