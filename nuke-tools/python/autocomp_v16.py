import nuke
class Group():
    def __init__(self, name):
        self.groupName = name
        self.layerList = []
      
    def add(self, layer):
        #print 'fullname: ' + fullName
        self.layerList.append(layer)
        return
      
    def getLayerList(self):
        return self.layerList

def parseForGroupName(layer):
    splitLayer = layer.split('_') 
    #print splitLayer
    if len(splitLayer) <= 2:
        return layer
    else:
        return splitLayer[3]

def parseForLayerName(layer):
    splitLayer = layer.split('_')
    #print splitLayer
    if len(splitLayer) > 5:
        return splitLayer[4] + '_' + splitLayer[5]
    elif len(splitLayer) > 4:
        return splitLayer[4]
    else:
        return layer

def getGroup(newGrpName, grpList):
    for eachGrp in grpList:
        if newGrpName == eachGrp.groupName:
            return eachGrp

    return None

selectedNodes = nuke.selectedNodes()
#print 'Beginning'
for readNode in selectedNodes:
    if readNode.Class() != 'Read':
        nuke.message('This is not ReadNode. Plase select Read Node.')
        break;
           #print readNode.channels()
    else:
        rawChannelList = readNode.channels()
        channelLayerList = []
        lightNameList = []
        for channel in rawChannelList:
            channelLayer = channel.split('.')
            channelLayerList.append(channelLayer[0])
        newLayerList = list(set(channelLayerList))
        #print newLayerList
        oldGrpName = ""
        global grpList
        grpList = []
        for layer in newLayerList:
            names = layer.split('_')
            #print names[0]
            if names[0] == 'objmshrn' or names[0] == 'sss' or names[0] == 'obj':
                newGrpName = parseForGroupName(layer)
                curGrp = getGroup(newGrpName, grpList)
                if curGrp == None: #if no same name in group
                    newGrp = Group(newGrpName)#create new group and add it to the list
                    newGrp.add(layer)
                    grpList.append(newGrp)
                else: #if found the same name in group
                    curGrp.add(layer)
        
        #print "printing group"
        #print grpList
        
        CustomNode = nuke.nodes.Group(name="LightControl", inputs=[readNode])
        CustomNode.knob('postage_stamp').setValue(True)
        global inputForCN
        global outputForCN
        global countForCN
        global bInputForCN
        global CCList
        global mergeNodeCN
        CCList = []
        CustomNode.begin()
        countForCN = 1
        mergeNodeCN = nuke.nodes.Merge()
        inputForCN = nuke.nodes.Input()
        outputForCN = nuke.nodes.Output()
        for group in grpList:
            GN = group.groupName
            #print "Groupname: " + group.groupName
            if GN != 'rgba' and GN != 'P' and GN != 'other' and GN != 'N' and GN != 'depth':
                g = nuke.nodes.Group(name=GN, inputs = [inputForCN])
                g.knob('postage_stamp').setValue(True)
                layers = group.getLayerList()
                g.begin()
                global varIn
                global varOut
                global count
                global bInput
                global mergeNode
                global x
                varIn = nuke.nodes.Input()
                varOut = nuke.nodes.Output()
                count = 1
                #print "here"
                #mergeNode = nuke.nodes.Merge(operation='plus')
                #nuke.autoplaceSnap(mergeNode)
                #print "Size: {}".format(len(layers))
                #x = 0
                for layer in layers:
                    #print parseForLayerName(layer)
                    shuffleNode = nuke.nodes.Shuffle(name=parseForLayerName(layer), inputs=[varIn]) 
                    shuffleNode.knob('in').setValue(layer)
                    shuffleNode.knob('postage_stamp').setValue(True)
                    if len(layers) < 2:
                        varOut.setInput(0, shuffleNode)
                    else:
                        if count == 1:
                            bInput = shuffleNode
                        else:
                            mergeNode = nuke.nodes.Merge(inputs=[bInput, shuffleNode], operation='plus')
                            bInput = mergeNode
                            if len(layers) == count:
                                varOut.setInput(0, mergeNode)
                    count = count + 1
               
                g.end()
            if GN != 'rgba' and GN != 'P' and GN != 'other' and GN != 'N' and GN != 'depth':
                UnPremultNode = nuke.nodes.Unpremult(inputs=[g])
                CCNode = nuke.nodes.ColorCorrect(name="CC: {}".format(group.groupName), inputs=[UnPremultNode])
                CCList.append(CCNode)
                PremultNode = nuke.nodes.Premult(inputs=[CCNode]) 
                if countForCN == 1:
                    bInputForCN = PremultNode
                else:
                    mergeNodeCN = nuke.nodes.Merge(inputs=[bInputForCN, PremultNode], operation="plus", A='rgb')
                    bInputForCN = mergeNodeCN
                    #print "SizeCN: {}".format(len(grpList))   
                countForCN = countForCN + 1
            
        outputForCN.setInput(0, mergeNodeCN)    
        CustomNode.end()
        

        for group in grpList:
            tab = nuke.Tab_Knob(group.groupName, group.groupName)
            CustomNode.addKnob(tab)
            #CustomNode.pickKnob(CCList[0])
            #CustomNode.addKnob(CCList[0])
   
