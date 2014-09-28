import os

import utilities as amu

def get_output_path(shot, prefix):
    path = os.path.join(os.environ['SHOTS_DIR'], shot, 'animation_cache/geo_sequences')
    path = amu.set_version(path, prefix)
    path = path.replace(os.environ['JOB'], '$JOB')
    name = shot+'_$F3.bgeo'
    return  os.path.join(path, name)

me = hou.pwd()
shot = me.parm('anim').evalAsString()
prefix = me.name()
path = get_output_path(shot, prefix)
me.parm('sopoutput').set(path)