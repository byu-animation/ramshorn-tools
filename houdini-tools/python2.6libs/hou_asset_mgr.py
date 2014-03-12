# Digital Asset management
# Provides New, Add, Checkin, Checkout, Revert, and other functionality for .otl files
# Author: Brian Kingery
import shutil
import sqlite3 as lite
import os, glob, sys
import hou
import subprocess
from ui_tools import ui, messageSeverity, fileMode
from miscutil import fileutil
import new_asset_methods
import checkin_asset_methods

import utilities as amu #asset manager utilites
import houdini_rollback as rb #rollback tool

JOB=os.environ['JOB']
USERNAME=os.environ['USER']
OTLDIR=os.environ['OTLS_DIR']
ASSETSDIR=os.environ['ASSETS_DIR']
USERDIR=os.path.join(os.environ['USER_DIR'], 'otls')

database=os.path.join(OTLDIR, '.otl.db')
otlTableDef="otl_table(id INTEGER PRIMARY KEY, filename TEXT, locked INT, lockedby TEXT, UNIQUE(filename))"
insert_ignore_sql="INSERT OR IGNORE INTO otl_table (filename, locked, lockedby) VALUES (?, ?, ?)"

def createUsrDir():
    if not os.path.exists(USERDIR):
        os.makedirs(USERDIR)

def updateDB():
    """Update the database with what is in OTLDIR"""
    con = lite.connect(database)
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS "+otlTableDef+";")
        files = glob.glob(os.path.join(OTLDIR, '*.otl'))
        # Add any new files to the Database
        for file in files:
            cur.execute(insert_ignore_sql, (os.path.basename(file), 0, ""))
        con.commit()
        # Delete any files that are no longer with us
        cur.execute("SELECT filename FROM otl_table")
        rows = cur.fetchall()
        toDelete = []
        for row in rows:
            toDelete.append(row[0].encode('utf-8'))
        for file in files:
            f = os.path.basename(file)
            if f in toDelete:
                toDelete.remove(f)
        for d in toDelete:
            cur.execute("DELETE FROM otl_table WHERE filename='"+d+"'")
        con.commit()
    con.close()

def getSelectedNode():
    """Returns the current node if EXACTLY ONE is selected
        Otherwise returns None"""
    node = None
    nodes = hou.selectedNodes()
    if len(nodes) == 1:
        node = nodes[0]
    return node

def isDigitalAsset(node):
    """Returns True if node is a digital asset, False if not"""
    if node.type().definition() is None:
        return False
    else:
        return True

def saveOTL():
    """Calls saveOTL with the selected node"""
    node = getSelectedNode()
    if node != None:
        saveOTL(node)

def saveOTL(node):
    """If node is a digital asset,
        Saves node's operator type and marks node as the current defintion"""
    if isDigitalAsset(node):
        # try/except statement is needed for assets that generate code, like shaders.
        try:
            node.type().definition().updateFromNode(node)
        except:
            pass
        node.matchCurrentDefinition()

def switchOPLibraries(oldfilepath, newfilepath):
    hou.hda.uninstallFile(oldfilepath, change_oplibraries_file=False)
    hou.hda.installFile(newfilepath, change_oplibraries_file=True)
    hou.hda.uninstallFile("Embedded")

def copyToOtlDir(node, filename, newName, newDef):
    """Moves the .otl file out of the USERDIR into the OTLDIR and removes it from USERDIR.
        Changes the oplibrary to the one in OTLDIR."""
    newfilepath = os.path.join(OTLDIR, filename)
    oldfilepath = os.path.join(USERDIR, filename)
    node.type().definition().copyToHDAFile(newfilepath, new_name=newName, new_menu_name=newDef)
    #fileutil.clobberPermissions(newfilepath)
    switchOPLibraries(oldfilepath, newfilepath)

def moveToOtlDir(node, filename):
    """Calls copyToOtlDir and then removes the otl from USERDIR."""
    oldfilepath = os.path.join(USERDIR, filename)
    copyToOtlDir(node, filename, None, None)
    os.remove(oldfilepath)

def copyToUsrDir(node, filename, destpath):
    """Copies the .otl file from OTLDIR to USERDIR
        Changes the oplibrary to the one in USERDIR"""
    if not os.path.exists(destpath):
        os.mkdir(destpath)
    newfilepath = os.path.join(destpath, filename)
    oldfilepath = os.path.join(OTLDIR, filename)
    node.type().definition().copyToHDAFile(newfilepath)
    #fileutil.clobberPermissions(newfilepath)
    switchOPLibraries(oldfilepath, newfilepath)

def lockOTL(filename):
    """Updates the database entry specified by filename to locked=1 and lockedby=USERNAME"""
    con = lite.connect(database)
    with con:
        cur = con.cursor()
        cur.execute("UPDATE otl_table SET locked=1, lockedby='"+USERNAME+"' WHERE filename='"+filename+"'")
        con.commit()
    con.close()

def unlockOTLbyNode(node = None):
    """Calls unlockOTL with the selected node"""
    if node != None:
        if not isDigitalAsset(node):
            hou.ui.displayMessage("Not a Digital Asset.")
        else:
            warningMsg = 'WARNING! You are unlocking this node! \n If you didn\'t mean to do this, please click \n CANCEL!'
            reply = hou.ui.displayMessage(warningMsg, title='Warning!', buttons=('Ok', 'Cancel'), default_choice=1)
            if reply == 0:
                libraryPath = node.type().definition().libraryFilePath()
                filename = os.path.basename(libraryPath)
                #TODO save this somewhere
                unlockOTL(filename)
            else:
                hou.ui.displayMessage('Thank you for being safe. \n If you have a question please talk to someone in charge.')                

def unlockOTL(filename):
	asset_name, ext = os.path.splitext(filename)
	toUnlock = os.path.join(os.environ['ASSETS_DIR'], asset_name, 'otl')
	print toUnlock
	if amu.isLocked(toUnlock):
		reply = hou.ui.displayMessage('Are you REALLY sure you want to unlock this node?', buttons=('Ok', 'Cancel'))
		if reply == 0:	
			amu.unlock(toUnlock)
			hou.ui.displayMessage('Node unlocked')
	else:
		hou.ui.displayMessage('Node already unlocked')
		return
	

def addOTL(filename):
    """Updates the database with a new table entry for filename"""
    con = lite.connect(database)
    with con:
        cur = con.cursor()
        cur.execute(insert_ignore_sql, (filename, 0, ""))
        con.commit()
    con.close()

def getFileInfo(filename):
    """Returns all of the table information for filename"""
    info = None
    con = lite.connect(database)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM otl_table WHERE filename='"+filename+"'")
        info = cur.fetchone()
    con.close()
    return info

def isContainer(node):
    if not isDigitalAsset(node):
        return False

    ndef = node.type().definition()
    nsec = ndef.sections()['Tools.shelf']
    contents = str(nsec.contents())
    if contents.find('Container Assets') != -1:
        return True
    else:
        return False

def isEditableAsset(node):
    if not isDigitalAsset(node):
        return False

    ndef = node.type().definition()
    nsec = ndef.sections()['Tools.shelf']
    contents = str(nsec.contents())
    if contents.find('Editable Assets') != -1:
        return True
    else:
        return False

def _lockAssetOriginal(node, lockit):
     if isContainer(node):
         ndef = node.type().definition()
         opts = ndef.options()
         opts.setLockContents(lockit)
         ndef.setOptions(opts)
 
def _lockAssetNew(node, lockit):
    if isDigitalAsset(node):
        ndef = node.type().definition()
        opts = ndef.options()
        val = '' if lockit else '*'
        if isContainer(node): 
            ndef.addSection('EditableNodes', '')
            opts.setLockContents(True)
            ndef.setOptions(opts)
        elif isEditableAsset(node):
            ndef.addSection('EditableNodes', val)
            opts.setLockContents(True)
            ndef.setOptions(opts)
        else: # On everything else, for now do nothing. 
            pass

lockAsset = _lockAssetNew

def get_filename(parentdir):
    return os.path.basename(os.path.dirname(parentdir))+'_'+os.path.basename(parentdir)

# checkoutLightingFile(), unlockLightingFile(), checkinLightingFile() and discardLightingFile() moved to the lighting_asset_methods.py

def checkout(node):
    """Checks out the selected node.  EXACTLY ONE node may be selected, and it MUST be a digital asset.
        The node must already exist in the database."""
    if not isDigitalAsset(node):
        hou.ui.displayMessage("Not a Digital Asset.")
    else:
        if node.type().name() == "geometryTemplate":
            hou.ui.displayMessage("Cannot checkout geometry template node.")
            return False
        libraryPath = node.type().definition().libraryFilePath()
        filename = os.path.basename(libraryPath)

        asset_name, ext = os.path.splitext(filename)
        toCheckout = os.path.join(os.environ['ASSETS_DIR'], asset_name, 'otl')
        myCheckout = False
        try:
            destpath = amu.checkout(toCheckout, True)
        except Exception as e:
            print str(e)
            myCheckout = amu.checkedOutByMe(toCheckout)
            if not myCheckout:
                # hou.ui.displayMessage('Can Not Checkout. Locked by')
                getInfo(node, 'Asset Locked')
                return
            else:
                destpath = amu.getCheckoutDest(toCheckout)

        if myCheckout:
            switchOPLibraries(os.path.join(OTLDIR, filename), os.path.join(destpath, filename))
        else:
            copyToUsrDir(node, filename, destpath)
        lockAsset(node, True)
        saveOTL(node)
        node.allowEditingOfContents()
        hou.ui.displayMessage("Checkout Successful!", title='Success!')

# checkin(node = None), isCameraAsset(node), isSetAsset(node), writeToAlembic(outDir, filename, rootObject, objects='*', trange='off', startFrame=1, endFrame=240, stepSize=1), writeCamerasToAlembic(node), and writeSetToAlembic(node) moved to checkin_asset_methods.py

def discard(node = None):
    if not isDigitalAsset(node):
        hou.ui.displayMessage("Not a Digital Asset.")
    else:
        libraryPath = node.type().definition().libraryFilePath()
        filename = os.path.basename(libraryPath)
        toDiscard = os.path.dirname(libraryPath)
        if amu.isCheckedOutCopyFolder(toDiscard):
            switchOPLibraries(libraryPath, os.path.join(OTLDIR, filename))
            node.matchCurrentDefinition()
            amu.discard(toDiscard)
            hou.ui.displayMessage("Revert Successful!")

# formatName(name) is also used in the new_asset_methods.py
def formatName(name):
    name = name.strip()
    name = name.replace('_', ' ')
    if name.split()[0].lower() != os.environ['PROJECT_NAME']:
        name = str(os.environ['PROJECT_NAME']) + ' ' + name
    return name.lower()

# listContainers() and newContainer(hpath) moved to new_asset_methods.py

def printList(pList, ws=4):
    indent = ' '*ws
    result = ''
    for l in pList:
        result += indent + str(l) + '\n'
    return result

def getAssetDependents(assetName):
    dependents = []
    otls = glob.glob(os.path.join(OTLDIR, 'owned*.otl'))
    for o in otls:
        ndef = hou.hda.definitionsInFile(o)[0]
        contents = ndef.sections()['CreateScript'].contents().splitlines()
        for c in contents:
            if 'opadd -e -n' in c:
                c = c.split(' ')
                d = os.path.basename(o).split('.')[0]
                if c[3] == assetName and d not in dependents:
                    dependents.append(d)
    return dependents

def rename(node = None):
    """Renames the selected node. EXACTLY ONE node may be selected, and it MUST be a digital asset.
        The node must already exist in the database.
    """
    if node != None:
        if not isDigitalAsset(node):
            hou.ui.displayMessage("Not a Digital Asset.")
        else:
            if isContainer(node):
                oldlibraryPath = node.type().definition().libraryFilePath()
                oldfilename = os.path.basename(oldlibraryPath)
                oldAssetName = oldfilename.split('.')[0]
                assetDirPath = os.path.join(ASSETSDIR, oldAssetName)

                dependents = getAssetDependents(oldAssetName)

                if dependents:
                    hou.ui.displayMessage('The following assets are depenent on this asset: \n\n'+printList(dependents)+'\nModify these assets first before attempting to rename again!!', title='Can NOT rename!', severity=hou.severityType.Error)
                    return

                nodeDir = os.path.join(os.environ['ASSETS_DIR'], oldAssetName, 'otl')
                info = amu.getVersionedFolderInfo(nodeDir);
                if info[0] == "":
                    if passwordWindow('r3n@m3p@ssw0rd', 'Enter the rename password...'):
                        resp = hou.ui.readInput("Enter the New Operator Label", title="Rename OTL")
                        if resp != None and resp[1].strip() != '':
                            name = formatName(resp[1])
                            newfilename = name.replace(' ', '_')
                            newfilepath = os.path.join(OTLDIR, newfilename+'.otl')
                            if os.path.exists(newfilepath):
                                hou.ui.displayMessage("Asset by that name already exists. Cannot rename asset.", title='Asset Name', severity=hou.severityType.Error)
                            elif not amu.canRename(assetDirPath, newfilename):
                                hou.ui.displayMessage("Asset checked out in Maya. Cannot rename asset.", title='Asset Name', severity=hou.severityType.Error)
                            else:
                                node.type().definition().copyToHDAFile(newfilepath, new_name=newfilename, new_menu_name=name)
                                hou.hda.installFile(newfilepath, change_oplibraries_file=True)
                                newnode = hou.node(new_asset_methods.determineHPATH()).createNode(newfilename)
                                node.destroy()
                                hou.hda.uninstallFile(oldlibraryPath, change_oplibraries_file=False)
                                subprocess.check_call( ['rm','-f',oldlibraryPath] )
                                amu.renameAsset(assetDirPath, newfilename)
                else:
                    logname, realname = amu.lockedBy(info[0].encode('utf-8'))
                    whoLocked = 'User Name: ' + logname + '\nReal Name: ' + realname + '\n'
                    errstr = 'Cannot checkout asset. Locked by: \n\n' + whoLocked
                    hou.ui.displayMessage(errstr, title='Asset Locked', severity=hou.severityType.Error)
    else:
        hou.ui.displayMessage("Select EXACTLY one node.")

def deleteAsset(node = None):
    """Deletes the selected node. EXACTLY ONE node may be selected, and it MUST be a digital asset.
        The node must already exist in the database. It may not be already checked out in Houdini
        or in Maya.
    """
    if node != None:
        if not isDigitalAsset(node):
            hou.ui.displayMessage("Not a Digital Asset.", title='Non-Asset Node', severity=hou.severityType.Error)
            return
        else:
            if isContainer(node):
                oldlibraryPath = node.type().definition().libraryFilePath()
                oldfilename = os.path.basename(oldlibraryPath)
                oldAssetName = oldfilename.split('.')[0]
                assetDirPath = os.path.join(ASSETSDIR, oldAssetName)
                dependents = getAssetDependents(oldAssetName)

                if dependents:
                    hou.ui.displayMessage('The following assets are depenent on this asset: \n\n'+printList(dependents)+'\nModify these assets first before attempting to delete again!!', title='Can NOT delete!', severity=hou.severityType.Error)
                    return

                nodeDir = os.path.join(os.environ['ASSETS_DIR'], oldAssetName, 'otl')
                info = amu.getVersionedFolderInfo(nodeDir);
                print info[0]
                if not info[0] == "":
                    logname, realname = amu.lockedBy(info[0].encode('utf-8'))
                    whoLocked = 'User Name: ' + logname + '\nReal Name: ' + realname + '\n'
                    errstr = 'Cannot delete asset. Locked by: \n\n' + whoLocked
                    hou.ui.displayMessage(errstr, title='Asset Locked', severity=hou.severityType.Error)
                    return

                if not amu.canRemove(assetDirPath):
                    hou.ui.displayMessage("Asset currently checked out in Maya. Cannot delete asset.", title='Maya Lock', severity=hou.severityType.Error)
                    return

                message = "The following paths and files will be deleted:\n" + assetDirPath + "\n" + oldlibraryPath
                hou.ui.displayMessage(message, title='Asset Deleted', severity=hou.severityType.Error)

                if passwordWindow('d3l3t3p@ssw0rd', wmessage='Enter the deletion password ...'):
                    node.destroy()
                    hou.hda.uninstallFile(oldlibraryPath, change_oplibraries_file=False)
                    try:
                        amu.removeFolder(assetDirPath)
                        os.remove(oldlibraryPath)
                    except Exception as ex:
                        hou.ui.displayMessage("The following exception occured:\n" + str(ex), title='Exception Occured', severity=hou.severityType.Error)
                        return
    else:
        hou.ui.displayMessage("Select EXACTLY one node.")
        return

# new(), newGeo(hpath) and determineHPATH() moved to new_asset_methods.py

# getAssetName(node) moved to checkin_asset_methods.py

def refresh(node = None):
    """Only updates transforms of internal nodes of "Editable Assets"

    Everything else is probably either light linking data, or something else 
    that should always have a local override."""
    hou.hscript("otrefresh -r") # Refresh all definitions first
    
    if node == None or hasattr(node, "__len__"):
        hou.ui.displayMessage("Select EXACTLY one node.")
    elif not isEditableAsset(node):
        hou.ui.displayMessage('Not an "Editable Asset".')
    else:
        npath = os.path.dirname(node.path())
        dopple = hou.node(npath).createNode(node.type().name())
        for c in node.children():
            for dc in dopple.children():
                if c.name() == dc.name() and isinstance(c, hou.ObjNode):
                    c.setParmTransform(dc.parmTransform())
        dopple.destroy()
        hou.ui.displayMessage('Refresh successful.')

# TODO: This function probably needs to be removed.
def add(node = None):
    """Adds the selected node. EXACTLY ONE node may be selected, and it MUST be a digital asset.
        The node CAN NOT already exist in the database."""
    if node != None:
        if node.type().definition() is None:
            hou.ui.displayMessage("Not a Digital Asset.")
        else:
            libraryPath = node.type().definition().libraryFilePath()
            filename = os.path.basename(libraryPath)
            info = getFileInfo(filename)
            if info == None:
                saveOTL(node)
                moveToOtlDir(node, filename)
                addOTL(filename)
                hou.ui.displayMessage("Add Successful!")
            else:
                hou.ui.displayMessage("Already Added")
    else:
        hou.ui.displayMessage("Select EXACTLY one node.")

# convert_texture(userTextureMap, assetImageDir, folder_name='') and newTexture() moved to texture_update_methods.py

def getInfo(node, window_title='Node Info'):
    if node == None:
        # code for getting info from the checked out scene file goes here
        sys.stderr.write('Code for shot info does not yet exist for Houdini!')
        pass
    elif isDigitalAsset(node):
        # code for getting info selected node
        libraryPath = node.type().definition().libraryFilePath()
        filename = os.path.basename(libraryPath)
        assetname, ext = os.path.splitext(filename)
        nodeDir = os.path.join(os.environ['ASSETS_DIR'], assetname, 'otl')
        nodeInfo = amu.getVersionedFolderInfo(nodeDir)
        message = ''
        if nodeInfo[0]:
            logname, realname = amu.lockedBy(nodeInfo[0].encode('utf-8'))
            message = 'Checked out by '+realname+' ('+logname+').\n'
        else:
            message = 'Not Checked out.\n'
        message = message+'Last checked in by '+nodeInfo[3]
        hou.ui.displayMessage(message, title=window_title)

def passwordWindow(password, wtitle='Enter Password', wmessage='Enter Password', wlabel='Password'):
    '''Pop up a window with a text window to enter a password into

Returns true when the password entered matches the password given as a 
parameter and false otherwise.'''
    resp = ''
    ok = 0
    first = True
    label = (wlabel + ':',)
    while ok == 0 and resp != password:
        if not first:
            hou.ui.displayMessage('Incorrect!\nTry Again.', buttons=('Ok',), title='Error', severity=hou.severityType.Message)
        ok, resp = hou.ui.readMultiInput(message=wmessage, input_labels=label, password_input_indices=(0,), buttons=('OK', 'Cancel'), title=wtitle)
        resp = resp[0]
        first = False
    return ok == 0

# make getNodeInfo an alias of getInfo
getNodeInfo = getInfo

def rollbackOTL(node): # Calling rollback method in separate module
	rb.rollbackOTL(node)

def rollbackShot(): # Rollback for the separate shots.
	rb.rollbackShotFiles()





