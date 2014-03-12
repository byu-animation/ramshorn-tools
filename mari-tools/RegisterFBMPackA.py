# ------------------------------------------------------------------------------
# Requirements: This Node Library requires MARI FunctionLibary 1.06 or higher
# Available at: http://mari.ideascale.com/
# ------------------------------------------------------------------------------
# FBM Pack A
# Copyright (c) 2013 Jens Kafitz. All Rights Reserved.
# ------------------------------------------------------------------------------
# Author: Jens Kafitz | Mari Ideascale
# Web: www.campi3d.com      
# Web: www.mari.ideascale.com   
# Email: info@campi3d.com
# ------------------------------------------------------------------------------
# History:
# - 08/12/13	released for Mari 2.0
# 
# - 08/13/13	Threshold + SoftClip is now evaluated on a normalized version of the noise giving much more even results
# 
# - 12/12/13	Release for Mari 2.5
# 				Added compatibility with Mari Function Lib for Transforms and Noises - requires MARI Function Lib 1.06 or higher
# 				Added Vector FBM
# 				multiFBM Value Mapping is now using a smoother algorithm giving more organic results
# 				Baseline Features added to fbm and vfbm
# 				Amplitute Features added to all FBMs
# 				Invert Feature added to all FBMs
# 				Preview Handle Feature added to multiFBM
# 				Added Ability to invert just negative noise values ("valleys") by using Absolute Value
# 				Added Thresholding to all FBMs
# 				Added Ability to propagate negative noise values as either black or transparent into the end result
# 				Removed Propagation Features from multiFBM to reduce node handling complexity
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

def registerFBMPackA_fbm():
	"Register basic fbm, part of FBMPackA"
	# Register the code as a new custom shader module
	try:
		mari.gl_render.registerCustomProceduralLayerFromXMLFile("Procedural/Custom/FBM/fBm+",mari.resources.path(mari.resources.USER_SCRIPTS) + "/NodeLibrary/Procedurals/FBM/JK_FBM.xml")
		print 'Registered Procedural FBM Node : fBm+'
	except Exception as exc:
		print 'Error Registering Procedural FBM Node : fBm+ : ' + str(exc)


def registerFBMPackA_multifbm():
	"Register multifbm, part of FBMPackA"
	# Register the code as a new custom shader module
	try:
		mari.gl_render.registerCustomProceduralLayerFromXMLFile("Procedural/Custom/FBM/Multi fBm",mari.resources.path(mari.resources.USER_SCRIPTS) + "/NodeLibrary/Procedurals/FBM/JK_MultiFBM.xml")
		print 'Registered Procedural FBM Node : Multi fBm'
	except Exception as exc:
		print 'Error Registering Procedural FBM Node : Multi fBm : ' + str(exc)


def registerFBMPackA_Vfbm():
	"Register Vfbm, part of FBMPackA"
	# Register the code as a new custom shader module
	try:
		mari.gl_render.registerCustomProceduralLayerFromXMLFile("Procedural/Custom/FBM/Vec fBm",mari.resources.path(mari.resources.USER_SCRIPTS) + "/NodeLibrary/Procedurals/FBM/JK_VFBM.xml")
		print 'Registered Procedural FBM Node : Vec fBm'
	except Exception as exc:
		print 'Error Registering Procedural FBM Node : Vec fBm : ' + str(exc)
		
# ------------------------------------------------------------------------------

registerFBMPackA_fbm()
registerFBMPackA_multifbm()
registerFBMPackA_Vfbm()