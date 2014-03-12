# ------------------------------------------------------------------------------
# Requirements: This Node Library requires MARI FunctionLibary 1.06
# Available at: http://mari.ideascale.com/
# ------------------------------------------------------------------------------
# Mari Ideascale - Custom Object Normal
# Copyright (c) 2013 Jens Kafitz. All Rights Reserved.
# ------------------------------------------------------------------------------
# Author: Jens Kafitz | Mari Ideascale
# Web: www.campi3d.com
# Web: www.mari.ideascale.com
# Email: info@campi3d.com
# ------------------------------------------------------------------------------
# History:
# - 04/15/13	1.0 Release
# - 11/15/13	1.1 Release for Mari 2.5, modified for consistency with DT3D Function Lib
# - 12/14/13	Release for Mari 2.5 with final python and folder structure
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

def registerCustomObjectNormal():
	"Register modified Object Normal Node with transformation controls"
	# Register the code as a new custom shader module
	try:
		mari.gl_render.registerCustomProceduralLayerFromXMLFile("Geometry/Custom/Custom Object Normal",mari.resources.path(mari.resources.USER_SCRIPTS) + "/NodeLibrary/Geometry/JK_CustomSurfaceNormal.xml")
		print 'Registered Geometry Node : Custom Object Normal'
	except Exception as exc:
		print 'Error Registering Geometry Node : Custom Object Normal : ' + str(exc)

# ------------------------------------------------------------------------------

registerCustomObjectNormal()
