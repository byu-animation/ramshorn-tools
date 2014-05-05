# Houdini Rollback tool
# Provides Rollback tool for Houdini, similar to Maya tool
# Author: Chris Wasden, Joe Gremlich
from PyQt4.QtGui import *
from PyQt4 import QtGui
from ui_tools import pyqt_houdini
import os, glob, sys
import hou
from ui_tools import ui, messageSeverity, fileMode
import utilities as amu #asset manager utilities
import hou_asset_mgr as ham # houdini asset manager

ASSETSDIR = os.environ['ASSETS_DIR']
SHOTSDIR = os.environ['SHOTS_DIR']

class VersionDialog(QDialog):
	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		vbox = QVBoxLayout()
		self.lbox = QListWidget()
		self.lbox.currentRowChanged.connect(self.changeLabel)
		self.versionInfo = QLabel("Info")
		self.versionInfo.setWordWrap(True)
		opts_layout = QHBoxLayout()
		vbox.addWidget(QLabel("Versions:"))
		opts_layout.addWidget(self.lbox)
		vbox.addLayout(opts_layout)
		vbox.addWidget(QLabel("Version info:"))
		vbox.addWidget(self.versionInfo)
		self.accept_btn = QPushButton('Accept')
		self.accept_btn.clicked.connect(self.accept)
		self.cancel_btn = QPushButton('Cancel')
		self.cancel_btn.clicked.connect(self.close)
		btn_layout = QHBoxLayout()
		btn_layout.addWidget(self.cancel_btn)
		btn_layout.addWidget(self.accept_btn)
		vbox.addLayout(btn_layout)
		self.setLayout(vbox)
		self.setModal(True)
		self.setFixedSize(360, 420)
		self.setWindowTitle("Select Version For Rollback")
	def addItems(self,selections, info):
		self.lbox.addItems(selections)
		self.sInfo = info
		self.lbox.setCurrentRow(0)
		self.versionInfo.setText(self.sInfo[0])	
	def changeLabel(self):
		self.versionInfo.setText(self.sInfo[self.lbox.currentRow()])
	def accept(self):
		curItem = self.lbox.item(self.lbox.currentRow())
		self.close()
		if(self.otl):			
			rollbackOTLgo(str(curItem.text()),self.versionedFolders,self.assetName,self.toCheckout)
		else:
			rollbackShotFilesGo(str(curItem.text()),self.versionedFolders,self.assetName,self.toCheckout)
	def setParams(self, versionedFolders,assetName,toCheckout,otl):
		self.versionedFolders = versionedFolders
		self.assetName = assetName
		self.toCheckout = toCheckout
		self.otl = otl

def rollbackOTL(node = None):
	"""Pulls a rollback window for the user to select a version to rollback to. EXACTLY ONE node may be selected, and it MUST be a digital asset.
	    The node must already exist in the database.
	"""
	print 'RollbackOTL'

	#Need to check if a particular node is a digital asset first. Rollback is will only work as a DA, with model, rigs and animation.
	if node != None:

		if not ham.isDigitalAsset(node):
			ui.infoWindow('Wait! You can only rollback Digital Assets!')
			print "NOT A DIGITAL ASSET."
		else:
			# First, we need to see if this is checked out or not. If it is checked out, then we can proceed. If not, state so.
			# For the productions path			
			libraryPath = node.type().definition().libraryFilePath()
			filename = os.path.basename(libraryPath)

			asset_name, ext = os.path.splitext(filename)
			#print "asset_name " + asset_name
			toCheckout = os.path.join(ASSETSDIR, asset_name, 'otl')
			#print "toCheckout " + toCheckout
			myCheckout = False

			myCheckout = amu.isCheckedOut(toCheckout)
			if myCheckout: #If it has been checked out
				myCheckout = amu.checkedOutByMe(toCheckout)
				if myCheckout: #If user was the last to checkout
					#Here we rollback.
					versionedFolders = os.path.join(toCheckout, "src")
					#print "versionedFolders ", versionedFolders
					versions = glob.glob(os.path.join(versionedFolders, '*'))
					#print "selections ", versions
					#Wooohoooo!!!
					selections = []
					selectionInfo = []
					nodeInfoDest = toCheckout

					for vr in versions:
						selections.append(os.path.basename(vr))
						comment = amu.getVersionComment(nodeInfoDest,os.path.basename(vr))
						selectionInfo.append(comment)
					selections.sort()
					dialog = VersionDialog()
					dialog.addItems(selections,selectionInfo)
					dialog.show()
					dialog.setParams(versionedFolders,asset_name,toCheckout,True)
					pyqt_houdini.exec_(dialog)
					
				else:
					hou.ui.displayMessage('Already checked out.')
					return
			else:
				hou.ui.displayMessage('Please checkout asset first.')
	else:
		print "Node does not exist"

def rollbackOTLgo(answer,versionedFolders,asset_name,toCheckout):
	#answer = dialog.answer#hou.ui.selectFromList(selections, message='Select version to rollback:', exclusive=True)
	if answer:
		version = int(answer[1:])
		versionStr = "%03d" % version
		newVersion = os.path.join(versionedFolders,"v" + versionStr)
		checkoutFilePath = os.path.join(amu.getUserCheckoutDir(), asset_name)

		rollingBack = hou.ui.displayMessage('WARNING: You are about to remove your most recent changes. Proceed at your own risk.', buttons=('Actually, I don\'t want to', 'Yes. Roll me back'), severity=hou.severityType.Warning, title=("Woah there, pardner!"))
	

		if (rollingBack):
			print "rollingBack"
			# Temporarily set the version to the rollback version, and check out.
			oldVersion = int(amu.tempSetVersion(toCheckout, versionStr))
			oldVersionStr = "%03d" % oldVersion
			print toCheckout
			tempFilePath = os.path.join(checkoutFilePath + "_otl_" + versionStr)
			filePath = os.path.join(checkoutFilePath + "_otl_" + oldVersionStr)
			# Now that we've set the version, we will 
			amu.discard(filePath) # Hey! This is working!!!
			amu.checkout(toCheckout, True)

			# Reset the version number, and rename the checkout path to the most recent version.
			amu.tempSetVersion(toCheckout, oldVersion)
			correctCheckoutDest = amu.getCheckoutDest(toCheckout)
			os.rename(tempFilePath, correctCheckoutDest)

def rollbackShotFiles():
	# NOTE: Currently, we do not "check out" a shot file when it is pulled in. That is interesting. I wonder why not? Anyway, I don't know if that is an issue yet. Ah well. I guess we'll play with it.
	print "RollbackShotFiles"
	filepath = hou.hipFile.path() # The filepath goes to the path for the checked out file in the user directory.
	filename = os.path.basename(filepath)

	if not (filename == "untitled.hip"):\
		# If it isn't untitled, then we have a checked out lighting file, and we will proceed.
		shotNumber = filename.split("_");
		shotPaths = os.path.join(SHOTSDIR, str(shotNumber[0]))
		lightingPath = os.path.join(shotPaths, "lighting")
		lightingSrc = os.path.join(lightingPath, "src")	
	
		versions = glob.glob(os.path.join(lightingSrc, "*"))
		versionList = []
		versionInfo = []
		nodeInfoDest = lightingPath

		for v in versions:
			versionList.append(os.path.basename(v))
			comment = amu.getVersionComment(nodeInfoDest,os.path.basename(v))
			versionInfo.append(comment)

		versionList.sort() # Should only be one. Whatever.
		dialog = VersionDialog()
		dialog.addItems(versionList,versionInfo)
		dialog.show()
		dialog.setParams(lightingSrc,shotNumber,lightingPath,False)
		pyqt_houdini.exec_(dialog)

def rollbackShotFilesGo(answer,versionedFolders,asset_name,toCheckout):
	if answer:
		version = int(answer[1:])	
		versionStr = "%03d" % version

		rollingBack = hou.ui.displayMessage('WARNING: You are about to remove your most recent changes. Proceed at your own risk.', buttons=('Actually, I don\'t want to', 'Yes. Roll me back'), severity=hou.severityType.Warning, title=("Woah there, pardner!"))

		if (rollingBack):
			newLighting = os.path.join(versionedFolders, "v" + versionStr)

			# Again: set the latest version in the .nodeInfo file to the selected version, and checkout the next version.
			#asset_name, ext = os.path.splitext(filename)

			checkoutFilePath = os.path.join(amu.getUserCheckoutDir(), (asset_name[0]+"_lighting"))

			oldVersion = int(amu.tempSetVersion(toCheckout, version))

			oldVersionStr = "%03d" % oldVersion				
			
			tempFilePath = os.path.join(checkoutFilePath + "_" + versionStr)
			filePath = os.path.join(checkoutFilePath + "_" + oldVersionStr)

			# Discard the old file, and check out the rollbacked one.
			amu.discard(filePath) # Hey! This is working!!!
			amu.checkout(toCheckout, True)
			
			# Then resetting the version number back to the most recent, so when we check in again, we will be in the most recent version.
			amu.tempSetVersion(toCheckout, oldVersion)
			correctCheckoutDest = amu.getCheckoutDest(toCheckout)
			#print "correctCheckoutDest ", correctCheckoutDest

			os.rename(tempFilePath, correctCheckoutDest)
	# This is just the shot[lighting] files. Not animation, models, or rigs. Remember that.
		
