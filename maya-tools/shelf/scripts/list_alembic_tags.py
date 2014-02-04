from pymel.core import *

def listAlembicTags():
	transform_objects = ls(tr=True)
	tagged_objects = []
	for obj in transform_objects:
		if obj.hasAttr("BYU_Alembic_Export_Flag"):
			tagged_objects.append(obj)

	print tagged_objects

	showAlembicTagList(tagged_objects)


def showAlembicTagList(tagged_objects):
	taggedList = buildTagListStr(tagged_objects)

	return cmds.confirmDialog( title         = 'Tagged Objects'
		                         , message       = taggedList
		                         , button        = ['OK']
		                         , defaultButton = 'OK'
		                         , cancelButton  = 'OK'
		                         , dismissString = 'OK')

def buildTagListStr(tagged_objects):
	listStr = ""
	for obj in tagged_objects:
		listStr += obj.name() + "\n"
	return listStr

def go():
	listAlembicTags()