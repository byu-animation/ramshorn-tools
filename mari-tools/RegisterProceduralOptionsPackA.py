# ------------------------------------------------------------------------------
# Requirements: This Node Library requires DT3D_FunctionLibary 1.06 or higher
# Available at: http://mari.ideascale.com/
# ------------------------------------------------------------------------------
# Mari Ideascale - Procedural Options Pack A
# Copyright (c) 2013 Jens Kafitz. All Rights Reserved.
# ------------------------------------------------------------------------------                         	
# Author: Jens Kafitz | Mari Ideascale
# Web: www.campi3d.com      
# Web: www.mari.ideascale.com   
# Email: info@campi3d.com
# ------------------------------------------------------------------------------			                                   	
# History:
# - 04/15/13	1.0 Release
# - 11/29/13	1.1 Release for Mari 2.5, modified for consistency with DT3D Function Lib
# - 12/14/13	Re-Release for Mari 2.5, with new folder structure
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

def registerProceduralOptionsPackA_Cellular():
	"Register modified Mari Legacy Procedurals with added Options: Cellular"
	# Register the code as a new custom shader module
	try:
		mari.gl_render.registerCustomProceduralLayerFromXMLFile("Procedural/Custom/Voronoi/Legacy Cellular",mari.resources.path(mari.resources.USER_SCRIPTS) + "/NodeLibrary/Procedurals/Legacy/JK_Cellular.xml")
		print 'Registered Procedural Node : Legacy Cellular'
	except Exception as exc:
		print 'Error Registering Procedural Node : Legacy Cellular : ' + str(exc)

def registerProceduralOptionsPackA_Cloud():
	"Register modified Mari Legacy Procedurals with added Options: Cloud"
	# Register the code as a new custom shader module
	try:
		mari.gl_render.registerCustomProceduralLayerFromXMLFile("Procedural/Custom/Noise/Legacy Cloud",mari.resources.path(mari.resources.USER_SCRIPTS) + "/NodeLibrary/Procedurals/Legacy/JK_Cloud.xml")
		print 'Registered Procedural Node : Legacy Cloud'
	except Exception as exc:
		print 'Error Registering Procedural Node : Legacy Cloud : ' + str(exc)

def registerProceduralOptionsPackA_Perlin():
	"Register modified Mari Legacy Procedurals with added Options: Perlin"
	# Register the code as a new custom shader module
	try:
		mari.gl_render.registerCustomProceduralLayerFromXMLFile("Procedural/Custom//Perlin/Legacy Perlin",mari.resources.path(mari.resources.USER_SCRIPTS) + "/NodeLibrary/Procedurals/Legacy/JK_Perlin.xml")
		print 'Registered Procedural Node : Legacy Perlin'
	except Exception as exc:
		print 'Error Registering Procedural Node : Legacy Perlin : ' + str(exc)

def registerProceduralOptionsPackA_Squiggle():
	"Register modified Mari Legacy Procedurals with added Options: Squiggle"
	# Register the code as a new custom shader module
	try:
		mari.gl_render.registerCustomProceduralLayerFromXMLFile("Procedural/Custom/Noise/Legacy Squiggle",mari.resources.path(mari.resources.USER_SCRIPTS) + "/NodeLibrary/Procedurals/Legacy/JK_Squiggle.xml")
		print 'Registered Procedural Node : Legacy Squiggle'
	except Exception as exc:
		print 'Error Registering Procedural Node : Legacy Squiggle : ' + str(exc)

def registerProceduralOptionsPackA_Turbulence():
	"Register modified Mari Legacy Procedurals with added Options: Turbulence"
	# Register the code as a new custom shader module
	try:
		mari.gl_render.registerCustomProceduralLayerFromXMLFile("Procedural/Custom/Noise/Legacy Turbulence",mari.resources.path(mari.resources.USER_SCRIPTS) + "/NodeLibrary/Procedurals/Legacy/JK_Turbulence.xml")
		print 'Registered Procedural Node : Legacy Turbulence'
	except Exception as exc:
		print 'Error Registering Procedural Node : Legacy Turbulence : ' + str(exc)
		
# ------------------------------------------------------------------------------

registerProceduralOptionsPackA_Cellular()
registerProceduralOptionsPackA_Cloud()
registerProceduralOptionsPackA_Perlin()
registerProceduralOptionsPackA_Squiggle()
registerProceduralOptionsPackA_Turbulence()