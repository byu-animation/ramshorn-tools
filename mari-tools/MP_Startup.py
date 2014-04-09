# Coded by Andrew Rasmussen 2013. When it is terrible or breaks blame him. Or bake him pity cookies.
#Startup Script: Sets any custom presets we need in Mari
# ------------------------------------------------------------------------------


import mari
import signal

def resetColorDefaults():
	#Set the Input Color Space to Linear
	print "Setting Color Space..."
	mari.system._ocio_toolbar.toolbar.setColorSpace("linear")

	#Set the Gamma to 0.45
	print "Setting Gamma..."
	mari.system._ocio_toolbar.toolbar.setGamma(0.45)

resetColorDefaults()

mari.utils.signal_helpers.connect(mari.projects.opened, resetColorDefaults)
