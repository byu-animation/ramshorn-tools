me = hou.pwd()
mantra_parm = me.parm('mantra_node')
mantra_name = mantra_parm.eval()
mantra_node = hou.node(mantra_name)
exclude_parm = mantra_node.parm('excludelights')
excludelights = exclude_parm.evalAsString()
lightmask = '*'
for light in excludelights.split(' '):
    lightmask += ' ^' + light

print lightmask

asset_parm = me.parm('asset_nodes')
asset_nodes = asset_parm.eval().split(' ')
for asset in asset_nodes:
    asset_node = hou.node(asset)
    # render_parms = asset_node.parmsInFolder(('Render',))
    render_parms = asset_node.parms()
    for parm in render_parms:
        if 'lightmask' in parm.name():
            parm.set(lightmask)