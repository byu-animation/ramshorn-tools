import maya.cmds as cmds
import utilities as amu #asset manager utilities
import maya_geo_export as geo
import os

def saveFile():
        if not cmds.file(q=True, sceneName=True) == '':
                cmds.file(save=True, force=True) #save file

def isModelAsset():
        # unpack decoded entries and check if assetType is a 'model'
        assetName, assetType, version = geo.decodeFileName()
        return assetType == 'model'

def isRigAsset():
        # unpack decoded entries and check if assetType is a 'rig'
        assetName, assetType, version = geo.decodeFileName()
        return assetType == 'rig'

def isAnimationAsset():
        # unpack decoded entries and check if assetType is a 'rig'
        assetName, assetType, version = geo.decodeFileName()
        return assetType == 'animation'

def saveGeo():
        print 'saving geo...'
        # this is not a model asset. don't save objs
        if not isModelAsset():
                return True
        
        print 'we have a model'
        # if we can export the objs, export the objs to the asset folder
        if geo.generateGeometry():
                print 'generateGeometry done'
                geo.installGeometry()
                
                return True # copy was successful
        else:
                return False

def showFailDialog(): 
        return cmds.confirmDialog( title         = 'Checkin Failed'
                                 , message       = 'Checkin was unsuccessful'
                                 , button        = ['Ok']
                                 , defaultButton = 'Ok'
                                 , cancelButton  = 'Ok'
                                 , dismissString = 'Ok')

def showConfirmAlembicDialog():
        return cmds.confirmDialog( title         = 'Export Alembic'
                                 , message       = 'Export Alembic?'
                                 , button        = ['Yes', 'No']
                                 , defaultButton = 'Yes'
                                 , cancelButton  = 'No'
                                 , dismissString = 'No')

def getAssetName(filepath):
        return os.path.basename(filepath).split('.')[0]

def checkin():
        print 'checkin'
        saveFile() # save the file before doing anything
        print 'save'
        filePath = cmds.file(q=True, sceneName=True)
        print 'filePath: '+filePath
        toCheckin = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(filePath)))
        print 'toCheckin: '+toCheckin
        toInstall = isRigAsset()
	specialInstallFiles = [os.path.join(os.environ['SHOTS_DIR'], 'static/animation')]
        anim = isAnimationAsset()
        references = cmds.ls(references=True)
        loaded = []
        if amu.canCheckin(toCheckin) and saveGeo(): # objs must be saved before checkin
		comment = 'Comment'
		commentPrompt = cmds.promptDialog(
				    title='Comment',
				    message='What changes did you make?',
				    button=['OK','Cancel'],
				    defaultButton='OK',
				    dismissString='Cancel',
				sf = True)
		if commentPrompt == 'OK':
			comment = cmds.promptDialog(query=True, text=True);
		else:
			return
		amu.setComment(toCheckin, comment)
                dest = amu.getCheckinDest(toCheckin)
                # if anim and showConfirmAlembicDialog() == 'Yes':
                #   for ref in references:
                #     if cmds.referenceQuery(ref, isLoaded=True):
                #       loaded.append(ref)
                #       cmds.file(unloadReference=ref)
                #   print loaded
                #   for ref in loaded:
                #     cmds.file(loadReference=ref)
                #     refPath = cmds.referenceQuery(ref, filename=True)
                #     assetName = getAssetName(refPath)
                #     print "\n\n\n\n**************************************************************\n"
                #     print dest
                #     print filePath
                #     print refPath
                #     print assetName
                #     saveFile()
                #     amu.runAlembicConverter(dest, filePath, filename=assetName)
                #     cmds.file(unloadReference=ref)

                #   for ref in loaded:
                #     cmds.file(loadReference=ref)

                saveFile()
                cmds.file(force=True, new=True) #open new file
                dest = amu.checkin(toCheckin) #checkin
		toInstall |= (dest in specialInstallFiles)
                srcFile = amu.getAvailableInstallFiles(dest)[0]
                if toInstall:
                    amu.install(dest, srcFile)
        else:
                showFailDialog()

def go():
        try:
                checkin()
        except Exception as ex:
                msg = "RuntimeException:" + str(ex)
                print msg
                cmds.confirmDialog( title         = 'Uh Oh!'
                                  , message       = 'An exception just occured!\r\nHere is the message: ' + msg
                                  , button        = ['Dismiss']
                                  , defaultButton = 'Dismiss'
                                  , cancelButton  = 'Dismiss'
                                  , dismissString = 'Dismiss')
                

