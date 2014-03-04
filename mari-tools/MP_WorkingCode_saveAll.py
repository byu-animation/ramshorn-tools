# Coded by Andrew Rasmussen 2013. When it is terrible or breaks blame him. Or bake him pity cookies.
# ------------------------------------------------------------------------------

import os
import mari
import random
import PythonQt.QtGui as gui

# ------------------------------------------------------------------------------
#GLOBALS & ENVIROMENT VARIABLES
JOB = "/groups/owned/PRODUCTION/assets/"

projectName = "MariPipe"


# ------------------------------------------------------------------------------
def saveAll():
    objList = mari.geo.list()    # List all Objects of the scene
    for obj in objList:    # For each Object
        mari.geo.setCurrent(obj)    # Set Object to Current
        chanList = obj.channelList()    # List Object's Channels
        for chan in chanList:    # For each Channel
            print "Andrew Saving"
            # Export the Channel in the path you want (here /usr/tmp/)
            #chan.exportImagesFlattened('/usr/tmp/$ENTITY_$CHANNEL_$UDIM.tga')

# ------------------------------------------------------------------------------
#saveAll()
