import os
import glob

'''
filepath is a valid path to a versioned render folder
finds the latest version folder
if it is empty, it returns it
otherwise creates the next version folder and returns it
'''
def set_version(filepath):
    filepath = os.path.join(filepath, '*')
    versions = glob.glob(filepath)
    versions.sort
    latest =  versions[-1]
    if not os.listdir(latest):
        return os.path.abspath(latest)
    latest_int = int(latest[-1:])+1
    latest = latest[:-1]+str(latest_int)
    os.mkdir(latest)
    return os.path.abspath(latest)
    
print set_version("version_render")