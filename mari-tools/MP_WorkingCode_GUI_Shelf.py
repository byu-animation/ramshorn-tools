# Coded by Andrew Rasmussen 2013. When it is terrible or breaks blame him. Or bake him pity cookies.
#Pop Up Gui and Shelf Gui
# ------------------------------------------------------------------------------
  
import mari
import PythonQt
from PythonQt import QtGui,QtCore
  
  
def ADRtools():
# ------------------------------------------------------------------------------
    #creates toolbar, names it, and place in widow.
    mari.app.createToolBar("ADR Tools", 4, 1)
    myTool = mari.app.toolBar("ADR Tools")
    #creates an action for the first 'button' 
    action = mari.actions.create("ADR Shelf Tools", 'butt01()');
    #sets an icon to the action
    action.setIconPath(mari.resources.path(mari.resources.ICONS)+"/Crash.png")
    #places button & action into toolbar
    myTool.addAction("/Mari/Scripts/tmp")
    
    #repeats all of the above for my second 'button'
    action = mari.actions.create("SpecialSauce", 'butt02()');
    action.setIconPath(mari.resources.path(mari.resources.ICONS)+"/Monkey.png")
    myTool.addAction("/Mari/Scripts/tmp")
    
# ------------------------------------------------------------------------------
  
# Register the "Convert Channel" action - but not during the documentation step
if mari.app.isRunning():
    mari.app.deleteToolBar("ADR Tools")
    ADRtools()