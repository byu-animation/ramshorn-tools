import sys, os, glob
import utilities as amu
import nuke
import common_Nuke as common

def checkin():
	save = nuke.scriptSave()
	if save==True:
		toCheckin = common.get_checkin_path()
		if common.can_checkin():
			amu.setComment(toCheckin, 'comment')
			dest = amu.checkin(toCheckin)
			nuke.message('Checkin Successful!')
			nuke.scriptClose()
		else:
			nuke.message('Can not check in')

def go():
	checkin()
