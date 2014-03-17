# ------------------------------------------------------------------------------
# Threshold -  A Photoshop Style Threshold Filter with Soft Edge Settings
# Copyright (c) 2013 Jens Kafitz. All Rights Reserved.
# ------------------------------------------------------------------------------
# Author: Jens Kafitz | Mari Ideascale
# Web: www.campi3d.com      
# Web: www.mari.ideascale.com   
# Email: info@campi3d.com
# ------------------------------------------------------------------------------
# History:
# 05/06/13 Released 1.0
# 11/30/13 Mari 2.5 Version released
# 12/15/13 Re-released for Mari 2.5 with new Folder Structure
# 		   Fixed a bug that was causing Alphas to be threshold'ed as well, causing transparent
# 		   areas to appear on the layer
# 
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
		
def registerThreshold():
	"Register a new Threshold Adjustment Layer"
	# Register the code as a new custom shader module
	try:
		mari.gl_render.registerCustomAdjustmentLayerFromXMLFile("/Custom/Threshold",mari.resources.path(mari.resources.USER_SCRIPTS) + "/NodeLibrary/Adjustment/JK_Threshold.xml")
		print 'Registered Adjustment Layer : Threshold'
	except Exception as exc:
		print 'Error Registering Adjustment Layer : Threshold : ' + str(exc)

# ------------------------------------------------------------------------------

registerThreshold()