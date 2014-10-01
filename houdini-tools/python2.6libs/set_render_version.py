import os
import glob

import utilities as amu

# '''
# filepath is a valid path to a versioned render folder
# finds the latest version folder
# if it is empty, it returns it
# otherwise creates the next version folder and returns it
# '''
# def set_version(filepath, prefix=''):
#     searchpath = os.path.join(filepath, '*')
#     files = glob.glob(searchpath)
#     versions = [f for f in files if os.path.isdir(f)]
#     versions.sort()
#     length = len(versions)
#     # print versions
#     if length > 0:
#         latest = versions[-1]
#         index = 0
#         v = os.path.basename(latest)
#         # make sure it is a versioned folder
#         while  not re.match(prefix+'v[0-9]+', v) and index < length:
#             latest = versions[-1-index]
#             print latest
#             v = os.path.basename(latest)
#             index += 1
#         if index < length:
#             # if it's empty use it
#             if not os.listdir(latest):
#                 return latest
#         else:
#             v = prefix+'v000'
#     else:
#         v = prefix+'v000'
    
#     latest_int = int(v[1:])+1
#     latest = os.path.join(filepath,prefix+'v'+'%03d'%latest_int)

#     os.mkdir(latest)
#     return latest

'''
returns the correct Houdini render output path for the shot
'''
def get_output_path(shot, prefix):
    path = os.path.join(os.environ['SHOTS_DIR'], shot, 'renders/lighting')
    path = amu.set_version(path, prefix)
    path = path.replace(os.environ['JOB'], '$JOB')
    name = shot+'_$F3.exr'
    return  os.path.join(path, name)

#to be called from a mantra node in houdini
me = hou.pwd()
shot = me.parm('shot').evalAsString()
render_pass = me.parm('render_pass').evalAsString()+'_'
print 'shot_: '+str(shot)
path = get_output_path(shot, render_pass)
me.parm('vm_picture').set(path)