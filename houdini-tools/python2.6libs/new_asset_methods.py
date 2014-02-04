# Author: Jonathan Tsai

import os
import hou
import hou_asset_mgr
from miscutil import fileutil

import utilities as amu #asset manager utilites

OTLDIR=os.environ['OTLS_DIR']
ASSETSDIR=os.environ['ASSETS_DIR']

def new():
    otb = ('Container', 'Geometry', 'Cancel')
    # optype = ui.infoWindow("Choose operator type.", wbuttons=otb, wtitle='Asset Type')
    optype = hou.ui.displayMessage("Choose operator type.", buttons=otb, title='Asset Type')
    hpath = determineHPATH()
    if optype == 0:
        newContainer(hpath)
    elif optype == 1:
        newGeo(hpath)

def listContainers():
    dirlist = list()
    for root,dirs,files in os.walk(ASSETSDIR):
        if root != ASSETSDIR:
            break
        else:
            for dir in dirs:
                dirlist.append(str(dir))
    dirlist.sort()
    return dirlist

def newContainer(hpath):
    templateNode = hou.node(hpath).createNode("containerTemplate")
    templateNode.hide(True)
    # resp = ui.inputWindow("Enter the New Operator Label", wtitle="OTL Label")
    response = hou.ui.readInput("Enter the New Operator Label", buttons=('Ok', 'Cancel'), title="OTL Label")
    if response[0]==0:
        name = response[1]
    else:
        name = None
    if name != None and name.strip() != '':
        name = hou_asset_mgr.formatName(name)
        filename = name.replace(' ', '_')
        newfilepath = os.path.join(OTLDIR, filename+'.otl')
        
        if not os.path.exists(newfilepath):
            # create file heirarchy if container asset            
            amu.createNewAssetFolders(ASSETSDIR, filename)

            newversiondir = os.path.join(ASSETSDIR, filename+'/otl')
            print "dir " + newversiondir
            newversionpath = os.path.join(newversiondir, 'src/v000/'+filename+'.otl')
            print "path " + newversionpath
            templateNode.type().definition().copyToHDAFile(newversionpath, new_name=filename, new_menu_name=name)
            stablepath = amu.install(newversiondir, newversionpath)
            os.symlink(stablepath, newfilepath)
            hou.hda.installFile(newfilepath, change_oplibraries_file=True)
            fileutil.clobberPermissions(newfilepath)
            newnode = hou.node(hpath).createNode(filename)
            
            # templateNode.type().definition().copyToHDAFile(newfilepath, new_name=filename, new_menu_name=name)
            # hou.hda.installFile(newfilepath, change_oplibraries_file=True)
            # fileutil.clobberPermissions(newfilepath)
            # newnode = hou.node(hpath).createNode(filename)
        else:
            hou.ui.displayMessage("Asset by that name already exists. Cannot create asset.", title='Asset Name', severity=hou.severityType.Error)
        
    # clean up
    templateNode.destroy()

def newGeo(hpath):
    templateNode = hou.node(hpath).createNode("geometryTemplate")
    alist = listContainers()
    response = hou.ui.readInput("Enter the New Operator Label", title="OTL Label", buttons=('OK', 'Cancel'))
    filename = str()
    if response[0]==0:
        name = response[1]
    else:
        name = None
    if name != None and name.strip() != '':
        name = hou_asset_mgr.formatName(name)
        filename = name.replace(' ', '_')
        templateNode.setName(filename, unique_name=True)
    answer = hou.ui.selectFromList(alist, message='Select Container Asset this belongs to:', exclusive=True)
    if not answer:
        hou.ui.displayMessage("Geometry must be associated with a container asset! Geometry asset not created.", severity=hou.severityType.Error)
        templateNode.destroy()
        return
    answer = answer[0]
    sdir = '$JOB/production/assets/'
    gfile = hou.ui.selectFile(start_directory=os.path.join(sdir, alist[answer]+'/geo'), title='Choose Geometry', chooser_mode=hou.fileChooserMode.Read, pattern='*.bjson, *.obj')
    if len(gfile) > 4 and gfile[:4] != '$JOB':
        hou.ui.displayMessage("Path must start with '$JOB'. Default geometry used instead.", title='Path Name', severity=hou.severityType.Error)
        templateNode.destroy()
    elif gfile != '':
        hou.parm(templateNode.path() + '/read_file/file').set(gfile)

def determineHPATH():
    hpane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    hpath = hpane.pwd().path()
    if not isinstance(hpane.pwd(), hou.ObjNode):
        hpath = "/obj"
    return hpath
