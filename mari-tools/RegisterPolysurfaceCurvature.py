# ------------------------------------------------------------------------------
# Polysurface Curvature - Lowres Surface Curvature Node For Surface Detection
# Copyright (c) 2013 Jens Kafitz. All Rights Reserved.
# ------------------------------------------------------------------------------
# Author: Jens Kafitz | Mari Ideascale
# Web: www.campi3d.com
# Web: www.mari.ideascale.com
# Email: info@campi3d.com
# ------------------------------------------------------------------------------
# History:
# - 12/16/13 - First Release for Mari 2.5. 
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

def registerPolysurfaceCurvature():
	"Register Surface Curvature Node "
	# Register the code as a new custom shader module
	try:
		mari.gl_render.registerCustomProceduralLayerFromXMLFile("Geometry/Custom/PolySurface Curvature",mari.resources.path(mari.resources.USER_SCRIPTS) + "/NodeLibrary/Geometry/JK_SurfaceCurvature.xml")
		print 'Registered Geometery Node : polysurface Curvature'
	except Exception as exc:
		print 'Error Registering Geometery Node : polysurface Curvature : ' + str(exc)

# ------------------------------------------------------------------------------

registerPolysurfaceCurvature()