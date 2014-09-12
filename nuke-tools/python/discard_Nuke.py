import sys, os, glob
import utilities as amu
import nuke

def get_file_path():
	return nuke.callbacks.filenameFilter( nuke.root().name() )

def get_checkout_path():
	return os.path.basename(os.path.dirname(get_file_path()))

def get_checkin_path():
	filePath = get_file_path()
	return os.path.join(amu.getUserCheckoutDir(), os.path.basename(os.path.dirname(filePath)))

def show_confirm_dialog():
	return nuke.ask('YOU ARE ABOUT TO IRREVOKABLY DISCARD ALL CHANGES YOU HAVE MADE. '
			'Please think this through very carefully.\r\n\r\nNow that we have '
			'gotten that straightened out, are you sure you want to discard '
			'your changes?')

def show_dialog(text):
	nuke.message(text)

def discard():
	file_path = get_file_path()
	if file_path:
		toDiscard = get_checkin_path()
		if amu.isCheckedOutCopyFolder(toDiscard):
			if show_confirm_dialog():
				nuke.scriptClear()
				amu.discard(toDiscard)
		else:
			show_dialog('ERROR: Not checked out.')
	else:
		show_dialog('ERROR: Not a file.')

def go():
	discard()
