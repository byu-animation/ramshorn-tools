import maya.cmds as cmds
import os
import utilities as amu
import maya_checkout
import maya_checkin

def go():
    filePath = cmds.file(q=True, sceneName=True)
    toCheckin = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(filePath)))
    toCheckout = amu.getCheckinDest(toCheckin) 
    maya_checkin.checkin()
    try:
        destpath = amu.checkout(toCheckout, True)
    except Exception as e:
        print str(e)
        if not amu.checkedOutByMe(toCheckout):
            cmd.confirmDialog(  title          = 'Can Not Checkout'
                               , message       = str(e)
                               , button        = ['Ok']
                               , defaultButton = 'Ok'
                               , cancelButton  = 'Ok'
                               , dismissString = 'Ok')
            return
        else:
            destpath = amu.getCheckoutDest(toCheckout)
    filename = os.path.basename(os.path.dirname(toCheckout))+'_'+os.path.basename(toCheckout)+'.mb'
    toOpen = os.path.join(destpath, filename)
    # open the file
    if os.path.exists(toOpen):
        cmds.file(toOpen, force=True, open=True)#, loadReferenceDepth="none")
    else:
        # create new file
        cmds.file(force=True, new=True)
        cmds.file(rename=toOpen)
        cmds.viewClipPlane('perspShape', ncp=0.01)
        cmds.file(save=True, force=True)