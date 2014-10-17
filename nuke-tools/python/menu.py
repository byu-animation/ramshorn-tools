import common_Nuke as common
import checkin_Nuke as ci
import checkout_Nuke as co
import rollback_Nuke as rb
import discard_Nuke as ds
import autocomp_v16 as autocomp
import os


# methods called in menu items

def checkout():
	# nuke.message('check out')
    co.go()

def checkin():
	# nuke.message('check in')
	ci.go()

def discard():
	ds.go()

def rollback():
    rb.go()

def autocomp():
    autocomp.go()

# get menubar
menubar = nuke.menu('Nuke')

# add menu items
menubar.addCommand( 'Ramshorn/check out', 'checkout()')
menubar.addCommand( 'Ramshorn/check in', 'checkin()')
menubar.addCommand( 'Ramshorn/discard', 'discard()')
menubar.addCommand( 'Ramshorn/rollback', 'rollback()')
#nuke.menu( 'Nuke' ).addCommand( 'Ramshorn/autocomp', 'autocomp()')

# get toolbar
toolbar = nuke.toolbar("Nodes")

# add custom ramshorn toolbar
m = toolbar.addMenu("Nukeshorn", icon="ramshorn.png")
m.addCommand("Andre Masks", "nuke.createNode(\"andre_masks.gizmo\")", icon="andre.png")
m.addCommand("Papa Masks", "nuke.createNode('papa_masks.gizmo')", icon="papa.png")
m.addCommand("Rambo Masks", "nuke.createNode('rambo_masks.gizmo')", icon="rambo.png")

