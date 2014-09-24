import hou_asset_mgr as mgr
import shutil
import string
import os
import hou
import uuid
import re

class UvLight:
    def __init__(self):
        self.uvLight = hou.node("/obj/uv_light")
        if (self.uvLight is None):
            self.uvLight = hou.node("/obj").createNode("envlight", 'uv_light')
            self.uvLight.parm("light_enable").set(0)
        self.sceneLights = []
        self.initSceneLights()

    def enable(self):
        for light, setting in self.sceneLights:
            light.parm("light_enable").set(0) 
        self.uvLight.parm("light_enable").set(1)


    def disable(self):
        for light, setting in self.sceneLights:
            light.parm("light_enable").set(setting)
        self.uvLight.parm("light_enable").set(0)

    def destroy(self):
        self.disable()
        self.uvLight.destroy()

    def initSceneLights(self, curr_node = hou.node("/obj")):
        match = re.search("^(hlight)|(envlight)|(indirectlight)|(ambient)$", curr_node.type().name())
        if match:
            self.sceneLights.append([curr_node, curr_node.parm("light_enable").eval()])
        children = curr_node.children()
        for child in children:
            self.initSceneLights(child)      

def getMantraNode():
    mn = hou.node("/out/mantra_uv")
    if (mn is None):
        #initialize with parms
        mn = hou.node("/out").createNode("ifd", "mantra_uv_" + str(uuid.uuid4()))
        mn.parm("vm_renderengine").set("pbrmicropoly")
        mn.parm("camera").set(getCameraNode().path())
    return mn

def getCameraNode():
    cam = hou.node("/obj/uv_cam")
    if (cam is None):
        cam = hou.node("/obj").createNode("cam", "uv_cam")
        cam.parm("resx").set("256")
        cam.parm("resy").set("256")
    return cam

def bake(node, writePath):
    if (node.type().name() == 'geo'):
        print 'baking...'
        mn = getMantraNode()
        mn.parm('vm_uvobject').set(node.path())
        filePath = os.path.join(writePath, getFileName(node))
        print filePath
        mn.parm('vm_picture').set(filePath)
        mn.parm('execute').pressButton()
        mn.destroy()
        print 'complete!'
        return filePath
    else:
        return None

def getFileName(node):
    children = node.children()
    try:
        for child in children:
            if child.type().name() == 'file':
                abcPath = child.parm('file').unexpandedString()
                name = os.path.splitext(os.path.basename(abcPath))[0]
                return name + '_bake.exr'
    except Exception, e:
        return node.name() + '_bake.exr'

def getWritePath(node):
    libraryPath = node.type().definition().libraryFilePath()
    filename = os.path.basename(libraryPath)
    assetname, ext = os.path.splitext(filename)
    bakeDir = os.path.join(os.environ['ASSETS_DIR'], assetname, 'images', 'bake')
    if not os.path.exists(bakeDir):
        os.makedirs(bakeDir)
    return bakeDir

def bakeScene():
    node = hou.node("/obj")
    children = node.children()
    for child in children:
        if mgr.isDigitalAsset(child):
            bakeAsset(child)

def bakeSelectedAsset():
    node = mgr.getSelectedNode()
    if mgr.isDigitalAsset(node):
        bakeAsset(node)

def bakeAsset(node):
    uvLight = UvLight()
    uvLight.enable()
    writePath = getWritePath(node)
    bakeNodeRecursive(node, writePath)
    getCameraNode().destroy()
    uvLight.disable()

def bakeNodeRecursive(node, writePath):
    bake(node, writePath)
    children = node.children()
    for child in children:
        if mgr.isDigitalAsset(child):
            bakeAsset(child)
        else:
            bakeNodeRecursive(child, writePath)
