# ------------------------------------------------------------------------------
# Normal Map Intensity - A adjustment layer to change the intensity of a normal map.
# Copyright (c) 2013 Orlando Esponda. All Rights Reserved.
# ------------------------------------------------------------------------------
# Author: Orlando Esponda      	
# Web: www.mari.ideascale.com 
# Email: 
# ------------------------------------------------------------------------------
# History:
#  11/30/13 Re-released for Mari 2.5
#  12/14/13 re-released for Mari 2.5 with proper Folder Structure
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
		
def registerNormalMapIntensity():
	"Register a new adjustment node adjust Normal Map Intensity"
	# Register the code as a new custom shader module
	try:
		mari.gl_render.registerCustomAdjustmentLayerFromXMLFile("/Custom/Normal Map Intensity",mari.resources.path(mari.resources.USER_SCRIPTS) + "/NodeLibrary/Adjustment/OE_NormalMapIntensity.xml")
		print 'Registered Adjustment Layer : Normal Map Intensity'
	except Exception as exc:
		print 'Error Registering Adjustment Layer : Normal Map Intensity : ' + str(exc)

# ------------------------------------------------------------------------------

registerNormalMapIntensity()
