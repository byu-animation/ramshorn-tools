# Coded by Andrew Rasmussen 2013. When it is terrible or breaks blame him. Or bake him pity cookies.
# ------------------------------------------------------------------------------

import os
import re
import mari
import random
import subprocess
import PythonQt.QtGui as gui
from ConfigParser import ConfigParser

# ------------------------------------------------------------------------------
#GLOBALS & ENVIROMENT VARIABLES
#JOB = "/groups/owned/PRODUCTION/assets/"

projectName = "MariPipe"

# ------------------------------------------------------------------------------
def convertToRat(geo, filePathNoUDIM):
	for patch in geo.patchList():
		# Get Patch UDIM numbers
		udim = 1001 + patch.u() + (10 * patch.v())

		# Convert with Houdini iconvert
		args = ['iconvert', '-g', 'off', filePathNoUDIM + '_' + str(udim) + '.png', filePathNoUDIM + '_' + str(udim) + '.rat', 'makemips', 'compression="none"']
		try:
			subprocess.check_call(args)
		except subprocess.CalledProcessError as e:
			mari.utils.message("Error: " + str(e))

		# Delete the PNG file
		os.remove(filePathNoUDIM + '_' + str(udim) + '.png')

def exportChannel(geo, channel):
	# Set the template for the file name
	fileName = '$ENTITY_$CHANNEL_$UDIM'
	fileExt = '.png'

	# Check for the project info file 
	cp = ConfigParser()
	projPath = mari.current.project().info().projectPath()[:-11]
	cp.read(os.path.join(projPath, ".projectInfo")) 
	exportPath = ""

	try:
		# Try and pull the last export path
		exportPath = cp.get("FilePaths", "Export")
	except:
		# If there was none, Prompt user for destination directory
		exportPath = mari.utils.getExistingDirectory(None, 'Select Map Export Path for \"' + channel.name() + '\"')
		if(len(exportPath) == 0):
			return
		else:
			# Save it to a project info file
			projInfo = ConfigParser()
			projInfo.add_section("FilePaths")
			projInfo.set("FilePaths", "Export", exportPath)
			projInfoFile = open(os.path.join(projPath, ".projectInfo"), "wb")
			projInfo.write(projInfoFile)

	# Save all images as PNG
	fullFilePath = exportPath + '/' + fileName + fileExt
	print fullFilePath
	channel.exportImagesFlattened(fullFilePath, mari.Image.DISABLE_SMALL_UNIFORMS)

	# Convert to RAT
	convertToRat(geo, exportPath + '/' + geo.name() + '_' + channel.name())


def exportSelectedMaps():
	print "Export Selected"

	# Make sure that there is an open project
	if mari.projects.current() is None:
		mari.utils.message('Please open a project first')
		return

	# Find the currently selected object
	geo = mari.geo.current()
	if geo is None:
		mari.utils.message('Please select an object to export a channels from.')

	# Find the currently selected channel
	channel = geo.currentChannel()
	if channel is None:
		mari.utils.message('Please select a channel to export.')

	# Export all images in channel
	exportChannel(geo, channel)

	mari.utils.message('Maps for \"' + channel.name() + '\" successfully exported.')

def exportAllMaps():
	print "Exporting All Maps"

	# Make sure that there is an open project
	if mari.projects.current() is None:
		mari.utils.message('Please open a project first')
		return

	# Find the currently selected object
	geo = mari.geo.current()
	if geo is None:
		mari.utils.message('Please select an object to export a channels from.')

	# Get a list of all the channels attached to the current object
	channels = geo.channelList()
	print geo.name()
	print geo

	# Export all images in each channel
	for chan in channels:
		print chan.name()
		print chan
		exportChannel(geo, chan)

	mari.utils.message('All maps successfully exported.')
	
# ------------------------------------------------------------------------------

