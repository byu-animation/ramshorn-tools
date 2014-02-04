# Author: Jonathan Tsai

import shutil
import os, glob
import hou
import subprocess
import hou_asset_mgr

import utilities as amu #asset manager utilites

def convert_texture(userTextureMap, assetImageDir, folder_name=''):
    print userTextureMap

    if os.path.isdir(userTextureMap):
        return

    extensions = ['.jpg','.jpeg','.tiff','.tif','.png','.exr']
    userFileName, userExt = os.path.splitext(os.path.basename(userTextureMap))
    if userExt not in extensions:
        return

    # Set Variables for texture paths
    convertedTexture = os.path.join('/tmp','intermediate'+userFileName+'.exr')
    print "convertedTexture:: "+convertedTexture
    finalTexture = os.path.join('/tmp','finished'+userFileName+'.rat')
    print "finalTexture:: "+finalTexture

    # Gamma correct for linear workflow
    if 'DIFF' in userTextureMap or 'diffuse' in userTextureMap:
        args = ['icomposite',convertedTexture,'=','gamma',str(1/2.2),userTextureMap]
        
        try:
            subprocess.check_call(args)
        except subprocess.CalledProcessError as e:
            hou.ui.displayMessage('Failed to convert texture. The following error occured:\n' + str(e))        
            return
        didgamma = '\nIt has been gamma corrected.'
    else:
        convertedTexture = userTextureMap
        didgamma = ''
    '''    
    # Convert to .exr with optimized settings. Also, setting compatible with RenderMan (in case we need to render there)
    args = ['txmake','-mode','periodic','-compression','zip']
    args += ['-format','openexr','-half',convertedTexture,finalTexture]
    '''
    # Uncomment the following and comment out the previous call if PRMan is not present

    args = ['iconvert', convertedTexture, finalTexture] 
    
    #subprocess.check_call( args.split() )


    try:
        subprocess.check_call(args)
    except subprocess.CalledProcessError as e:
        hou.ui.displayMessage('Failed to convert texture. The following error occured:\n' + str(e))
    else:
        # Rename texture and move into production pipeline 
        newTextureName = userFileName + '.rat'

        newfilepath = os.path.join(assetImageDir, folder_name, newTextureName)
        print "new file path:: "+newfilepath

        try:
            shutil.move(finalTexture, newfilepath)  
        except Exception as e:
            os.remove(finalTexture)
            hou.ui.displayMessage('Failed to move texture. The following error occured:\n' + str(e), severity=hou.severityType.Error)
        finally:
            if convertedTexture != userTextureMap:
                os.remove(convertedTexture)

def newTexture():
    # Get a list of assets 
    assetList = glob.glob(os.path.join(os.environ['ASSETS_DIR'], '*'))
    selections = []
    for aL in assetList:
        # basename takes last folder in path.
        selections.append(os.path.basename(aL)) 
        # sort alphabetically
    selections.sort()
    answer = hou.ui.selectFromList(selections, message='Choose an asset to add/update textures for', exclusive=True)
    if answer:
        answer = answer[0]
        assetName = selections[answer]
        assetImageDir = os.path.join(os.environ['ASSETS_DIR'], assetName, 'images')

        # Allow user to choose texture map in user local directory   
        userDirectory = os.environ['USER_DIR']
        userSelection = hou.ui.selectFile(start_directory=userDirectory, title='Select texture map, or folder of texture maps', image_chooser=True, pattern='*.jpg,*.jpeg,*.tiff,*.tif,*.png,*.exr') 
        
        #Allow user to search for texture in any directory
        userSelection = os.path.expandvars(userSelection)

        if os.path.isdir(userSelection):
            folder_name = os.path.basename(os.path.dirname(userSelection))
            texture_paths = glob.glob(os.path.join(userSelection, '*'))

            newFileDir = os.path.join(assetImageDir, folder_name)
            os.system('rm -rf '+newFileDir)
            print 'newFileDir:: '+newFileDir
            os.makedirs(newFileDir)
            
            for t in texture_paths:
                convert_texture(t, assetImageDir, folder_name=folder_name)
        else:
            convert_texture(userSelection, assetImageDir)

        hou.ui.displayMessage('Done.')
