# ------------------------------------------------------------------------------
# Requirements: This Node Library requires MARI FunctionLibary 1.06
# ------------------------------------------------------------------------------
# Mari Ideascale - Camo Procedural
# Copyright (c) 2013 Antoni Kujawa. All Rights Reserved.
# ------------------------------------------------------------------------------
# Author: Antoni Kujawa
# Web: www.mari.ideascale.com
# Email: info@campi3d.com
# ------------------------------------------------------------------------------
# Contributor: Jens Kafitz
# Web: www.mari.ideascale.com
# Email: info@campi3d.com
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

def registerCamoProcedural():
	"Register a military Camo Procedural Layer"
	# Register the code as a new custom shader module
	try:
		mari.gl_render.registerCustomProceduralLayerFromXMLFile("Procedural/Custom/Pattern/Camo Pattern",mari.resources.path(mari.resources.USER_SCRIPTS) + "/NodeLibrary/Procedurals/Pattern/AK_Camo.xml")
		print 'Registered Procedural Pattern Node : Camo Pattern'
	except Exception as exc:
		print 'Error Registering Procedural Pattern Node : Camo Pattern : ' + str(exc)

# ------------------------------------------------------------------------------

registerCamoProcedural()