from checkout_shot_ui import Ui_CheckoutShotDialog
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqt_houdini
import os, glob, shutil
import utilities as amu
import hou_asset_mgr as ham
import hou

class CheckoutShotDialog(QDialog):
    def __init__(self,parent=None):
        super(CheckoutShotDialog, self).__init__(parent)
        self.ui = Ui_CheckoutShotDialog()
        self.ui.setupUi(self)

        # setup events
        self.ui.rdbFxFile.clicked.connect(self.fxButton_Click)
        self.ui.rdbLightingFile.clicked.connect(self.lightingButton_Click)
        self.ui.btnUnlock.clicked.connect(self.unlock_Click)
        self.ui.lwShots.currentItemChanged.connect(self.shotList_ItemSelectionChange)
        
        # intialize member variables
        self.currentShotType = 'lighting'
        self.currentShot = None

        # populate shots
        self.populateShots()
        item = self.ui.lwShots.currentItem()
        if item != None:
            name = str(item.text())
            self.setShot(name)
    
    def populateShots(self):
        shotPaths = glob.glob(os.path.join(os.environ['SHOTS_DIR'], '*'))
        for sp in shotPaths:
            bn = os.path.basename(sp)
            item = QListWidgetItem("lwi" + bn)
            item.setText(bn)
            self.ui.lwShots.addItem(item)
        self.ui.lwShots.sortItems(0)
        self.ui.lwShots.setSortingEnabled(True)
    
    def fxButton_Click(self):
        self.currentShotType = 'sfx'
        self.refreshShot()
    
    def lightingButton_Click(self):
        self.currentShotType = 'lighting'
        self.refreshShot()

    def accept(self):
        if self.currentShot != None:

            if not self.currentShot.isLocked():
                destpath = self.currentShot.checkout()
                print destpath                
                toOpen = self.getFileToOpen(destpath)
                print toOpen
                if os.path.exists(toOpen):
                    hou.hipFile.load(toOpen)
                else:
                    hou.hipFile.clear()
                    hou.hipFile.save(toOpen) 
                    self.done(0)
            elif self.currentShot.checkedOutByMe():
                destpath = self.currentShot.getCheckoutDest()
                toOpen = self.getFileToOpen(destpath)
                hou.hipFile.load(toOpen)
    
    def getFileToOpen(self, destpath):
        toCheckout = self.currentShot.workingDirectory
        toOpen = os.path.join(destpath, ham.get_filename(toCheckout)+'.hipnc')
        return toOpen

    def reject(self):
        self.done(0)    

    def unlock_Click(self):
        self.currentShot.unlock()
        self.refreshShot()
        

    def shotList_ItemSelectionChange(self, item=None):
        if item != None:
            name = str(item.text())
            self.setShot(name)

    def refreshShot(self):
        self.setShot(self.currentShot.name)

    def setShot(self, name):
        self.currentShot = Shot(name, self.currentShotType)
        self.ui.lblShot.setText( "Shot: " + self.currentShot.name)
        self.ui.txtDescription.setText(self.currentShot.description)
        isLocked = self.currentShot.isLocked()
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(not isLocked or self.currentShot.checkedOutByMe())
        self.ui.btnUnlock.setEnabled(isLocked)
        

class Shot:
    def __init__(self, name, shotType):
        self.name = name
        self.shotType = shotType
        self.workingDirectory = self._getWorkingDirectory()
        self.description = self._getDescription()
    
    def _getWorkingDirectory(self):
        parent = os.path.join(os.environ['SHOTS_DIR'], self.name)
        wd = os.path.join(parent, self.shotType)
        if not amu.isVersionedFolder(wd):
            amu.addVersionedFolder(parent, self.shotType, 5)
        return wd 
    
    def _getDescription(self):
        description = ''
        try:
            folderInfo = amu.getVersionedFolderInfo(self.workingDirectory)
            if self.isLocked():
                description += 'Last check out:\n\t' + folderInfo[0] + '\n'
            description += 'Last check in:\n\t' + folderInfo[1] + ' on ' + folderInfo[2] + '\n'
            if folderInfo[3] != '':
                description += "Last Comment:" 
                description += '\n\t"' + folderInfo[3] + '"' + '\n'
        except Exception as e:
            description = str(e)
        return description
    
    def isLocked(self):
        return amu.isLocked(self.workingDirectory)   
    
    def checkedOutByMe(self):
        return amu.checkedOutByMe(self.workingDirectory)    

    def unlock(self):
        amu.unlock(self.workingDirectory)
        
    def getCheckoutDest(self):
        return amu.getCheckoutDest(self.workingDirectory)

    def checkout(self):
        return amu.checkout(self.workingDirectory, True)

def showDialog():
    app = QApplication.instance()
    if app is None:
        app = QApplication(['houdini'])
    dialog = CheckoutShotDialog()
    dialog.show()
    pyqt_houdini.exec_(app, dialog)
    

