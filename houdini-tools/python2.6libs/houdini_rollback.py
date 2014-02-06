# Houdini Rollback tool
# Provides Rollback tool for Houdini, similar to Maya tool
# Author: Chris Wasden, Joe Gremlich
import os, glob, sys
import hou
from ui_tools import ui, messageSeverity, fileMode
import utilities as amu #asset manager utilities
import hou_asset_mgr as ham # houdini asset manager

ASSETSDIR = os.environ['ASSETS_DIR']
SHOTSDIR = os.environ['SHOTS_DIR']

def rollbackOTL(node = None):
	"""Pulls a rollback window for the user to select a version to rollback to. EXACTLY ONE node may be selected, and it MUST be a digital asset.
	    The node must already exist in the database.
	"""
	print 'RollbackOTL'

	ham.updateDB()

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
					for vr in versions:
						selections.append(os.path.basename(vr))
					selections.sort()
					answer = hou.ui.selectFromList(selections, message='Select version to rollback:', exclusive=True)
					if answer:
						version = answer[0]
						versionStr = "%03d" % version

						newVersion = os.path.join(versionedFolders, "v" + versionStr)
						checkoutFilePath = os.path.join(amu.getUserCheckoutDir(), asset_name)


						rollingBack = hou.ui.displayMessage('WARNING: You are about to remove your most recent changes. Proceed at your own risk.', buttons=('Actually, I don\'t want to', 'Yes. Roll me back'), severity=hou.severityType.Warning, title=("Woah there, pardner!"))
						

						if (rollingBack):
							print "rollingBack"
							# Temporarily set the version to the rollback version, and check out.
							oldVersion = int(amu.tempSetVersion(toCheckout, version))
							oldVersionStr = "%03d" % oldVersion

							tempFilePath = os.path.join(checkoutFilePath + "_otl_" + versionStr)
							filePath = os.path.join(checkoutFilePath + "_otl_" + oldVersionStr)
							# Now that we've set the version, we will 
							amu.discard(filePath) # Hey! This is working!!!
							amu.checkout(toCheckout, True)

							# Reset the version number, and rename the checkout path to the most recent version.
							amu.tempSetVersion(toCheckout, oldVersion)
							correctCheckoutDest = amu.getCheckoutDest(toCheckout)
							os.rename(tempFilePath, correctCheckoutDest)
				else:
					hou.ui.displayMessage('Already checked out.')
					return
			else:
				hou.ui.displayMessage('Please checkout asset first.')				


			
	else:
		print "Node does not exist"



	

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
		for v in versions:
			versionList.append(os.path.basename(v))
		versionList.sort() # Should only be one. Whatever.

		answer = hou.ui.selectFromList(versionList, message='Select lighting version to rollback:', exclusive=True)
		if answer:		
			version = answer[0]
			versionStr = "%03d" % version

			rollingBack = hou.ui.displayMessage('WARNING: You are about to remove your most recent changes. Proceed at your own risk.', buttons=('Actually, I don\'t want to', 'Yes. Roll me back'), severity=hou.severityType.Warning, title=("Woah there, pardner!"))

			if (rollingBack):
				newLighting = os.path.join(lightingSrc, "v" + versionStr)

				# Again: set the latest version in the .nodeInfo file to the selected version, and checkout the next version.
				asset_name, ext = os.path.splitext(filename)
				checkoutFilePath = os.path.join(amu.getUserCheckoutDir(), asset_name)

				oldVersion = int(amu.tempSetVersion(lightingPath, version))
				oldVersionStr = "%03d" % oldVersion				
				
				tempFilePath = os.path.join(checkoutFilePath + "_" + versionStr)
				filePath = os.path.join(checkoutFilePath + "_" + oldVersionStr)

				# Discard the old file, and check out the rollbacked one.
				amu.discard(filePath) # Hey! This is working!!!
				amu.checkout(lightingPath, True)
				
				# Then resetting the version number back to the most recent, so when we check in again, we will be in the most recent version.
				amu.tempSetVersion(lightingPath, oldVersion)
				correctCheckoutDest = amu.getCheckoutDest(lightingPath)
				print "correctCheckoutDest ", correctCheckoutDest

				os.rename(tempFilePath, correctCheckoutDest)
		# This is just the shot[lighting] files. Not animation, models, or rigs. Remember that.
		
