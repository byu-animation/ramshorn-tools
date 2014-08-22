# Author: Jonathan Tsai

import os
import hou
import hou_asset_mgr

import utilities as amu #asset manager utilites

OTLDIR=os.environ['OTLS_DIR']

def checkin(node = None):
    """Checks in the selected node.  EXACTLY ONE node may be selected, and it MUST be a digital asset.
        The node must already exist in the database, and USERNAME must have the lock."""
    if not hou_asset_mgr.isDigitalAsset(node):
        hou.ui.displayMessage("Not a Digital Asset.")
    else:
        libraryPath = node.type().definition().libraryFilePath() #user checkout folder
        filename = os.path.basename(libraryPath) # otl filename
        toCheckin = os.path.dirname(libraryPath)

        if os.path.exists(os.path.join(toCheckin, ".checkoutInfo")) and amu.canCheckin(toCheckin):
            response = hou.ui.readInput("What did you change?", buttons=('OK', 'Cancel',), title='Comment')
            if(response[0] != 0):
                return
            comment = response[1]
            hou_asset_mgr.lockAsset(node, False)
            hou_asset_mgr.saveOTL(node)
            node.type().definition().save(libraryPath)
            hou.hda.uninstallFile(libraryPath, change_oplibraries_file=False)
            amu.setComment(toCheckin, comment)
            assetdir = amu.checkin(toCheckin)
            assetpath = amu.getAvailableInstallFiles(assetdir)[0]
            amu.install(assetdir, assetpath)
            hou.hda.installFile(os.path.join(OTLDIR, filename), change_oplibraries_file=True)
            hou.hda.uninstallFile("Embedded")
            if isCameraAsset(node) and hou.ui.displayMessage('Export Alembic?'
                                                        , buttons=('Yes','No',)
                                                        , default_choice=0
                                                        , title='Export Alembic') == 0:
                writeCamerasToAlembic(node)
            if isSetAsset(node) and hou.ui.displayMessage('Export Alembic?'
                                                        , buttons=('Yes','No',)
                                                        , default_choice=0
                                                        , title='Export Alembic') == 0:
                writeSetToAlembic(node)
            hou.ui.displayMessage("Checkin Successful!")

        else:
            hou.ui.displayMessage('Can Not Checkin.')

def getAssetName(node):
    if hou_asset_mgr.isDigitalAsset(node):
        lpath = node.type().definition().libraryFilePath()
        filename = os.path.basename(lpath)
        return str(filename.split('.')[0].replace("'", "_"))
    else:
        return None

def isCameraAsset(node):
    return 'cameras' in node.name()

def isSetAsset(node):
    sets = ('ramshorn_intro_set', 'ramshorn_cliff_set', 'ramshorn_mountain_set', 'ramshorn_gag_set' 'ramshorn_ground_set')
    return getAssetName(node) in sets

def writeToAlembic(outDir, filename, rootObject, objects='*', trange='off', startFrame=1, endFrame=240, stepSize=1, format='hdf5'):
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    abcFilePath = os.path.join(outDir, filename)

    # Create alembic ROP
    abcROP = hou.node('/out').createNode('alembic')

    # Set parameters
    parms = {}
    parms['trange'] = trange
    parms['f1'] = startFrame
    parms['f2'] = endFrame
    parms['f3'] = stepSize
    parms['filename'] = abcFilePath
    parms['root'] = rootObject.path()
    parms['objects'] = objects
    parms['format'] = format
    abcROP.setParms(parms)

    # Render ROP
    abcROP.render()
    abcROP.destroy()

    return abcFilePath
    
def writeCamerasToAlembic(node):
    sequence = node.name().split('_')[2][0]
    children = node.children()
    for c in children:
        name = c.name()
        if 'shot' in name:
            shot = name.split('_')[1]
            camDir = os.path.join(os.environ['SHOTS_DIR'], sequence+shot, 'camera')
            abcName = sequence+shot+'_camera'+'.abc'
            sFrame, eFrame = hou.playbar.playbackRange()
            sSize = hou.playbar.frameIncrement()
            abcFilePath = writeToAlembic(camDir, abcName, node
                                        , objects=os.path.join(c.path(), 'cam1')
                                        , trange='normal'
                                        # , startFrame=sFrame
                                        # , endFrame=eFrame
                                        , stepSize=sSize)
            mayaFilePath = os.path.join(camDir, sequence+shot+'_camera'+'.mb')
            if os.path.exists(mayaFilePath):
                os.remove(mayaFilePath)
            amu.mayaImportAlembicFile(mayaFilePath, abcFilePath)
            print hou.node(os.path.join(c.path(),'cam1')).evalParm('focal')
            amu.setFocalLengthMaya(mayaFilePath, hou.node(os.path.join(c.path(),'cam1')).evalParm('focal'))
            

def writeSetToAlembic(node):
    exclude_objects = ('owned_jeff_couch', 'owned_jeffs_controller', 'owned_abby_controller', 'owned_cyclopes_toy')
    assetName = getAssetName(node)
    print(assetName)
    abcName = assetName+'.abc'
    setDir = os.path.join(os.environ['PRODUCTION_DIR'], 'set_cache', assetName)
    include_objects = ''
    for c in node.children():
        name = getAssetName(c)
        if name != None and name not in exclude_objects and 'wall' not in name and 'layout' not in name:
            include_objects += ' '+c.path()
    abcFilePath = writeToAlembic(setDir, abcName, node, objects=include_objects)
    mayaFilePath = os.path.join(setDir, assetName+'.mb')
    if os.path.exists(mayaFilePath):
        os.remove(mayaFilePath)
    amu.mayaImportAlembicFile(mayaFilePath, abcFilePath)
