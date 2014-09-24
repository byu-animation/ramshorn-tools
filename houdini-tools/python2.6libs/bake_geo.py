import os

me = hou.pwd()
shot = me.parm('shot').evalAsString()
folder = os.path.join(os.environ['SHOTS_DIR'], shot, 'animation_cache/geo_sequences')
node_path = me.path()
name = node_path.replace('/', '_') + '.bgeo'
path = os.path.join(folder, name)
geo = me.geometry()
geo.saveToFile(path)