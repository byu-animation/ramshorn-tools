#!/bin/bash
# Coded by Andrew Rasmussen 2013. When it is terrible or breaks blame him. Or bake him pity cookies.
# Start Up Script for Mari in the pipeline, setting all the variables.
# ------------------------------------------------------------------------------


#export USER_SCRIPTS=${HOME}/ADRMariScripts/
export PROJECT_NAME=ramshorn
export JOB=/groups/${PROJECT_NAME}
export MARI_SCRIPT_PATH=${JOB}/ramshorn-tools/mari-tools/
export MARI_DEFAULT_GEOMETRY_PATH=${JOB}/PRODUCTION/assets/
export ICONS=/usr/local/Mari2.5v2/Media/Icons/
export PATH=/opt/hfs13.0.343/bin:$PATH
#export MARI_DEFAULT_CACHE=/warthome/${USERNAME}



#MARI_DEFAULT_GEOMETRY_PATH
#MARI_DEFAULT_IMAGE_PATH
#MARI_DEFAULT_ARCHIVE_PATH
#MARI_DEFAULT_EXPORT_PATH
#MARI_DEFAULT_SHELF_PATH
#MARI_DEFAULT_RENDER_PATH
#MARI_DEFAULT_CAMERA_PATH



wacomTabSetUp()
{
    ## This Preset is set up specifically for Mari 2.0
    ## Stylus
    xsetwacom set "Wacom Cintiq 22HD stylus" MapToOutput HEAD-1 
    ## Eraser
    xsetwacom set "Wacom Cintiq 22HD eraser" MapToOutput HEAD-1
    ## Pad
    xsetwacom set "Wacom Cintiq 22HD pad" MapToOutput HEAD-1
    ## Central button (Full Screen) 
    ##xsetwacom set "Wacom Cintiq 22HD pad" Button 1 "key f11"
    ## Button Mapping Left
    xsetwacom set "Wacom Cintiq 22HD pad" StripLeftDown "key minus"      # Brush radius
    xsetwacom set "Wacom Cintiq 22HD pad" StripLeftUp "key plus"      # Brush radius
    xsetwacom set "Wacom Cintiq 22HD pad" Button 1 "key +shift"      # Shift
    xsetwacom set "Wacom Cintiq 22HD pad" Button 2 "key +c"     # EyeDropper
    xsetwacom set "Wacom Cintiq 22HD pad" Button 3 "key +k"      # Brushes
    xsetwacom set "Wacom Cintiq 22HD pad" Button 8 "key +alt"      # Alt
    xsetwacom set "Wacom Cintiq 22HD pad" Button 9 "key ctrl z"      # Undo
    xsetwacom set "Wacom Cintiq 22HD pad" Button 10 "key b"      # Bake Paint Layer
    xsetwacom set "Wacom Cintiq 22HD pad" Button 11 "key super F9"      # Pie Selector
    xsetwacom set "Wacom Cintiq 22HD pad" Button 12 "key +x"      # Guestures
    ##xsetwacom set "Wacom Cintiq 22HD pad" Button 13 "key home"      # Hide All Pallates
    ## Button Mapping Right
    xsetwacom set "$WACOM_PAD" StripRightUp "key super pgup"      # brush radius (must be mapped in GIMP) 
    xsetwacom set "$WACOM_PAD" StripRightDown "key super pgdn"   # +ctrl = faster 
    xsetwacom set "Wacom Cintiq 22HD pad" Button 15 "key t"      # Hide Selection
    xsetwacom set "Wacom Cintiq 22HD pad" Button 16 "key t"      # Show Entire Object
    xsetwacom set "Wacom Cintiq 22HD pad" Button 17 "key super F2"      # F2
    xsetwacom set "Wacom Cintiq 22HD pad" Button 18 "key super F3"      # F3
    xsetwacom set "Wacom Cintiq 22HD pad" Button 19 "key n"      # Hard Brush
    xsetwacom set "Wacom Cintiq 22HD pad" Button 20 "key n"      # Open BYU Houdini
    xsetwacom set "Wacom Cintiq 22HD pad" Button 21 "key n"      # Open BYU Maya
    xsetwacom set "Wacom Cintiq 22HD pad" Button 22 "key n"      # Open Terminal

    # Here is the layout for custom mapping: 
    # 
    #   Left              Right 
    # +-----------+     +-----------+ 
    # | Button 2  |     | Button 15 | 
    # +-----------+     +-----------+ 
    # | Button 3  |     | Button 16 | 
    # +-----------+     +-----------+ 
    # | Button 8  |     | Button 17 | 
    # +-----------+     +-----------+ 
    # | Button 9  |     | Button 18 | 
    # +-----------+     +-----------+ 
    # +-----------+     +-----------+ 
    # | Button 1  |     | Button 14 | 
    # +-----------+     +-----------+ 
    # +-----------+     +-----------+ 
    # | Button 10 |     | Button 19 | 
    # +-----------+     +-----------+ 
    # | Button 11 |     | Button 20 | 
    # +-----------+     +-----------+ 
    # | Button 12 |     | Button 21 | 
    # +-----------+     +-----------+ 
    # | Button 13 |     | Button 22 | 
    # +-----------+     +-----------+ 
    # 

	echo "Pen Tablet Settings Calibrated";
}
wacomTabSetUp


# Starting Mari
echo "Starting Mari...";
/usr/local/Mari2.5v2/mari

#createJToolsMenu()

















# CERTIFICATES = 'CERTIFICATES' #: Security certificates. 
# COLOR = 'COLOR' #: L{Color} data. 
# C_API_DOCS = 'C_API_DOCS' #: C API documentation. 
# DEFAULT_ARCHIVE = 'MARI_DEFAULT_ARCHIVE_PATH' #: The default path to load and save project archives. 
# DEFAULT_CAMERA = 'MARI_DEFAULT_CAMERA_PATH' #: The default path to load and save cameras and projectors. 
# DEFAULT_EXPORT = 'MARI_DEFAULT_EXPORT_PATH' #: The default path to export textures to. 
# DEFAULT_GEO = 'MARI_DEFAULT_GEOMETRY_PATH' #: The default path to load geometry from. 
# DEFAULT_IMAGE = 'MARI_DEFAULT_IMAGE_PATH' #: The default path to load and save reference images. 
# DEFAULT_IMPORT = 'MARI_DEFAULT_IMPORT_PATH' #: The default path to import textures from. 
# DEFAULT_RENDER = 'MARI_DEFAULT_RENDER_PATH' #: The default path to save renders such as turntables. 
# DEFAULT_SHELF = 'MARI_DEFAULT_SHELF_PATH' #: The default path to load and save shelf files. 
# EXAMPLES = 'EXAMPLES' #: Example data assets. 
# GRADIENTS = 'GRADIENTS' #: Brush gradients. 
# HELP = 'HELP' #: Help documentation resources. 
# ICONS = 'ICONS' #: Tool bar and menu item icons. 
# IMAGES = 'IMAGES' #: General system images. 
# LOGOS = 'LOGOS' #: Logo images for the application. 
# LUTS = 'LUTS' #: LUT data. 
# MEDIA = 'MEDIA' #: Top level media directory. 
# MISC = 'MISC' #: Other miscellaneous data. 
# QT_PLUGINS = 'QT_PLUGINS' #: Qt plug-ins. 
# SCRIPT_DOCS = 'SCRIPT_DOCS' #: Python documentation. 
# SETTINGS = 'SETTINGS' #: Default settings. 
# SHADERS = 'SHADERS' #: Built-in shader code. 
# SYSTEM_SCRIPTS = 'SCRIPTS' #: Built-in Python scripts - AppDir/Media/Scripts. 
# USER = 'MARI_USER_PATH' #: Root of the default user path - default: ~/Mari. 
# USER_PLUGINS = 'MARI_PLUGINS_PATH' #: A list of paths to load custom user plug-ins from - default: ~/Mari/Plugins. 
# USER_SCRIPTS = 'MARI_SCRIPT_PATH' #: A list of paths to run scripts from - default: ~/Mari/Scripts. 
