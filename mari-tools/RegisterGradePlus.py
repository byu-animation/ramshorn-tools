# ------------------------------------------------------------------------------
# GradePlus - A Grade Node with added functionality
# Copyright (c) 2013 Jens Kafitz. All Rights Reserved.
# ------------------------------------------------------------------------------
# Author: Jens Kafitz | Mari Ideascale
# Web: www.campi3d.com      
# Web: www.mari.ideascale.com   
# Email: info@campi3d.com
# ------------------------------------------------------------------------------
# History:

# - 08/17/13 released
# - 11/18/13 Mari 2.5 compatible version released and colorSelectors added
#  -12/14/13 Re-release with new Folder Structure
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
		
def registerGradePlus():
	"Register a new custom grade node with Nuke Style functions"
	# Register the code as a new custom shader module
	try:
		mari.gl_render.registerCustomAdjustmentLayerFromXMLFile("/Custom/Grade+",mari.resources.path(mari.resources.USER_SCRIPTS) + "/NodeLibrary/Adjustment/JK_GradePlus.xml")
		print 'Registered Adjustment Layer : Grade+'
	except Exception as exc:
		print 'Error Registering Adjustment Layer : Grade+ : ' + str(exc)

# ------------------------------------------------------------------------------

registerGradePlus()