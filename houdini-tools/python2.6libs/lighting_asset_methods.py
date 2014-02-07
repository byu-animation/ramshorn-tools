# Author: Jonathan Tsai

import os, glob
import hou
import hou_asset_mgr

import utilities as amu #asset manager utilites
import hou_asset_mgr as ham

def checkoutLightingFile():
    print("checkoutLightingFile")
    shotPaths = glob.glob(os.path.join(os.environ['SHOTS_DIR'], '*'))
    selections = []
    for sp in shotPaths:
        selections.append(os.path.basename(sp))
    selections.sort()
    answer = hou.ui.selectFromList(selections, message='Select shot file to checkout:', exclusive=True)
    if answer:
        answer = answer[0]
        toCheckout = os.path.join(os.environ['SHOTS_DIR'], selections[answer], 'lighting')

        try:
            destpath = amu.checkout(toCheckout, True)
        except Exception as e:
            if not amu.checkedOutByMe(toCheckout):
                hou.ui.displayMessage('Can Not Checkout: '+str(e))
                return
            else:
                destpath = amu.getCheckoutDest(toCheckout)

        toOpen = os.path.join(destpath, ham.get_filename(toCheckout)+'.hipnc')

        if os.path.exists(toOpen):
            hou.hipFile.load(toOpen)
        else:
            hou.hipFile.clear()
            hou.hipFile.save(toOpen) 

def unlockLightingFile():
    print("unlockLightingFile")
    shotPaths = glob.glob(os.path.join(os.environ['SHOTS_DIR'], '*'))
    selections = []
    for sp in shotPaths:
        selections.append(os.path.basename(sp))
    selections.sort()
    answer = hou.ui.selectFromList(selections, message='Select shot file to unlock:', exclusive=True)
    if answer:
        answer = answer[0]
        toUnlock = os.path.join(os.environ['SHOTS_DIR'], selections[answer], 'lighting')
    if amu.isLocked(toUnlock):
        reply = hou.ui.displayMessage('Are you sure you want to unlock this file?', buttons=('Ok', 'Cancel'))
        if reply == 0:
            hou.hipFile.save()
            hou.hipFile.clear()		
            amu.unlock(toUnlock)
            hou.ui.displayMessage('Lighting file unlocked')

    else:
        hou.ui.displayMessage('Lighting file already unlocked')
        return

def checkinLightingFile():
    print('checkin lighting file')
    filepath = hou.hipFile.path()
    toCheckin = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(filepath)))
    backups = os.path.join(toCheckin, 'backup')
    print 'backup = ' + backups
    if os.path.isdir(backups):
        os.system('rm -rf '+backups)
    if amu.canCheckin(toCheckin):
        response = hou.ui.readInput("What did you change?", buttons=('OK', 'Cancel',), title='Comment')
        if(response[0] != 0):
            return
        comment = response[1]
        hou.hipFile.save()
        hou.hipFile.clear()
        amu.setComment(toCheckin, comment)
        dest = amu.checkin(toCheckin)
        srcFile = amu.getAvailableInstallFiles(dest)[0]
        amu.install(dest, srcFile)
    else:
        hou.ui.displayMessage('Checkin Failed')

def discardLightingFile():
    filepath = hou.hipFile.path()
    #TODO
    print(filepath)
    if hou.ui.displayMessage('YOU ARE ABOUT TO IRREVOKABLY DISCARD ALL CHANGES YOU HAVE MADE. '
                        'Please think this through very carefully.\n '
                        'Are you sure you want to discard '
                        'your changes?'
                        , buttons=('Yes','No',)
                        , default_choice=1
                        , title='Discard Confirmation') == 0:
        toDiscard = os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(filepath)))
        if amu.isCheckedOutCopyFolder(toDiscard):
            hou.hipFile.clear()
            amu.discard(toDiscard)
        else:
            hou.ui.displayMessage('This is not a checked out file.  There is nothing to discard', title='Invalid Command')
    else:
        hou.ui.displayMessage('Thank you for being responsible.', title='Discard Cancelled')
