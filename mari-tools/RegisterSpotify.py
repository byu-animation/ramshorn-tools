# ------------------------------------------------------------------------------
# Requirements: This Node Library requires DT3D_FunctionLibary 1.06 or higher
# Available at: http://mari.ideascale.com/
# ------------------------------------------------------------------------------
# Spotify | A multiFractal Node useful for weathering, terrain etc.
# Copyright (c) 2013 Jens Kafitz. All Rights Reserved.
# ------------------------------------------------------------------------------
# Author: Jens Kafitz | Mari Ideascale
# Web: www.campi3d.com      
# Web: www.mari.ideascale.com   
# Email: info@campi3d.com
# ------------------------------------------------------------------------------
# History:
# - 04/15/13	1.0 Release
# - 08/02/13 	Fixed Issue where the node breaks sometimes when multiple copies are in the same layerstack
# - 11/30/13	1.1 Release for Mari 2.5.
# 				New Default Values to better show what the node can do
# 				Replaced transform controls with the ones from the MARI Function Library
# 				Added Thresholding Controls
# - 12/15/13	Re-released for Mari 2.5 with new Folder Structure
# ------------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify		
# it under the terms of the GNU General Public License as published by		
# the Free Software Foundation, either version 3 of the License, or		
# (at your option) any later version.										
#																			
# This program is distributed in the hope that it will be useful,			
# but WITHOUT ANY WARRANTY; without even the implied warranty of			
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the			
# GNU General Public License for more details.								
#																			
# You should have received a copy of the GNU General Public License		
# along with this program.  If not, see <http://www.gnu.org/licenses/>.	
# ------------------------------------------------------------------------------

import mari	

def registerSpotify():
	"Register Spotify procedural"
	# Register the code as a new custom shader module
	try:
		mari.gl_render.registerCustomProceduralLayerFromXMLFile("Procedural/Custom/MultiFractal/Spotify",mari.resources.path(mari.resources.USER_SCRIPTS) + "/NodeLibrary/Procedurals/multiFractal/JK_Spotify.xml")
		print 'Registered Procedural multiFractal Node : Spotify'
	except Exception as exc:
		print 'Error Registering Procedural multiFractal Node : Spotify : ' + str(exc)
		
# ------------------------------------------------------------------------------

registerSpotify()
