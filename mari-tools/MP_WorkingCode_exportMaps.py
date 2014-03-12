# Coded by Andrew Rasmussen 2013. When it is terrible or breaks blame him. Or bake him pity cookies.
# ------------------------------------------------------------------------------

import os
import re
import mari
import random
import subprocess
import PythonQt.QtGui as gui

# ------------------------------------------------------------------------------
#GLOBALS & ENVIROMENT VARIABLES
#JOB = "/groups/owned/PRODUCTION/assets/"

projectName = "MariPipe"

# ------------------------------------------------------------------------------
def convertToRat(filePathNoExt):
	args = ['iconvert', '-g', 'off', filePathNoExt + '.png', filePathNoExt + '.rat', 'makemips', 'compression="none"']
	try:
		subprocess.check_call(args)
	except subprocess.CalledProcessError as e:
		mari.utils.message("Error: " + str(e))

def exportChannel(geo, imgSet, chanName):
	# Build up a map of (UDIM -> image) pairs
	images = {}
	for patch in geo.patchList():
		uv_index = patch.uvIndex()
		image = imgSet.image(uv_index)
		if image is not None:
			udim = 1001 + patch.u() + (10 * patch.v())
			images[udim] = image

	# Export Patches as separate images
	exportPath = ''
	for udim, image in images.iteritems():
		if(len(exportPath) == 0):
			lastExportPath = image.lastExportPath()
			dirSlashes = [m.start() for m in re.finditer('/', lastExportPath)]
			if(len(dirSlashes) > 0):
				fileNameBegin = dirSlashes[len(dirSlashes) - 1]
				exportPath = lastExportPath[:fileNameBegin]
				print "Exporting " + chanName + " channel to " + exportPath

		fileName = '%s_%s_%d' % (geo.name(), chanName, udim)
		fileExt = '.png'

		if(len(exportPath) == 0):
			exportPath = mari.utils.getExistingDirectory(None, 'Select Map Export Path for \"' + fileName + '.rat\"')
			if(len(exportPath) == 0):
				break

		fullFilePath = exportPath + '/' + fileName + fileExt
		image.saveAs(fullFilePath)
		convertToRat(exportPath + '/' + fileName)


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

	channel = geo.currentChannel()
	imgSet = geo.currentImageSet()
	if imgSet is None:
		mari.utils.message('Please select a channel to export.')

	exportChannel(geo, imgSet, channel.name())

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
	imageSets = geo.imageSetList()
	currentChanInd = 0

	for imgSet in imageSets:
		exportChannel(geo, imgSet, channels[currentChanInd].name())
		currentChanInd = (currentChanInd + 1)

	mari.utils.message('All maps successfully exported.')
	
# ------------------------------------------------------------------------------

