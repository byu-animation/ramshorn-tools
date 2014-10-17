import nuke

# Add subfolders to path to make this a little cleaner
nuke.pluginAddPath( './gizmos' )
nuke.pluginAddPath( './python' )
nuke.pluginAddPath( './plugins' )

sys.stderr.write( "\nHere\n" )

# set up ramshorn format
def setUpFormat():
    hasFormat = False
    scriptFormats = nuke.formats()
    for f in scriptFormats:
        if f.name() == 'ramshorn' and f.width() == 1280 and f.height() == 692:
            hasFormat = True
    if not hasFormat:
        ramshornFmt = '1280 692 ramshorn'
        nuke.addFormat(ramshornFmt)

setUpFormat()
