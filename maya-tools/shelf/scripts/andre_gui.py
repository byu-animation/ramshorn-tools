from functools import partial
import maya.cmds as cmds

# Andre Picker - basics of this is based off a tutorial by Jeremy Ernst.

print "testing andreGUI"


def buildUI():

	widgets = {}
	if cmds.window("andrePicker_UI", exists = True):
		cmds.deleteUI("andrePicker_UI")

	widgets["window"] = cmds.window("andrePicker_UI", title = "Andre Picker", w = 709, h = 651, mnb = True, mxb = False)

	# two different layouts
	widgets["mainLayout"] = cmds.columnLayout(w = 709, h = 651)
	widgets["formLayout"] = cmds.formLayout(w = 709, h = 651)

	# Add background image of Andre
	imagePath = cmds.internalVar(upd = True) + "icons/AndrePickerImage.jpg"
	cmds.image(image = imagePath)

	andre_ns = "ramshorn_andre_rig_stable:"

	# Create the buttons - this might be simpler than what I want. We'll see, though.

	widgets["globalControlButton"] = cmds.button(label = "GLOBAL\nCONTROL", w = 70, h = 40, bgc = [0, 1, 0], c = partial(selectControls, [andre_ns + "Character_ctrl_01"]))
	widgets["globalMoveButton"] = cmds.button(label = "GLOBAL\nMOVE", w = 55, h = 30, bgc = [0, 1, 0], c = partial(selectControls, [andre_ns + "cc_globalMove_01"]))

	widgets["headButton"] = cmds.button(label = "", w = 51, h = 30, bgc = [1, 1, 0], c = partial(selectControls, [andre_ns + "cc_head_01"]))
	widgets["chestButton"] = cmds.button(label = "", w = 150, h = 60, bgc = [0, 1, 0], c = partial(selectControls, [andre_ns + "cc_chest_01"]))
	widgets["allButtons"] = cmds.button(label = "ALL\nCONTROLS", w = 70, h = 60, bgc = [1, 0.5, 0], c = partial(selectControls, [andre_ns + "cc_head_01", andre_ns + "cc_chest_01", andre_ns + "cc_l_bendyShoulder_01", andre_ns + "cc_l_shld_01",
		andre_ns + "cc_l_armFK_01", andre_ns + "cc_l_forearmFK_01", andre_ns + "cc_l_handFK_01", andre_ns + "cc_l_armIK_01", andre_ns + "cc_l_elbowIK_01", andre_ns + "cc_r_bendyShoulder_01",
		andre_ns + "cc_r_shld_01", andre_ns + "cc_r_armFK_01", andre_ns + "cc_r_forearmFK_01", andre_ns + "cc_r_handFK_01", andre_ns + "cc_r_armIK_01", andre_ns + "cc_r_elbowIK_01",
		andre_ns + "cc_hip_01", andre_ns + "cc_COG_01", andre_ns + "cc_l_ikfk_01", andre_ns + "cc_r_ikfk_01", andre_ns + "cc_spine_a_FK_01", andre_ns + "cc_spine_b_FK_01", andre_ns + "cc_spine_c_FK_01", 
		andre_ns + "cc_spine_d_FK_01", andre_ns + "cc_spine_e_FK_01", andre_ns + "cc_l_knee_01", andre_ns + "cc_l_foot_01", andre_ns + "cc_l_footRoll_01", andre_ns + "cc_r_knee_01",
		andre_ns + "cc_r_foot_01", andre_ns + "cc_r_footRoll_01", andre_ns + "cc_l_Hand_01", andre_ns + "cc_l_Thumb_01", andre_ns + "cc_l_Index_01", andre_ns + "cc_l_Middle_01", andre_ns + "cc_l_Ring_01",
		andre_ns + "cc_l_Pinky_01", andre_ns + "cc_r_Hand_01", andre_ns + "cc_r_Thumb_01", andre_ns + "cc_r_Index_01", andre_ns + "cc_r_Middle_01", andre_ns + "cc_r_Ring_01",
		andre_ns + "cc_r_Pinky_01", andre_ns + "cc_l_legFK_01", andre_ns + "cc_l_shinFK_01", andre_ns + "cc_l_ankleFK_01", andre_ns + "cc_l_toeFK_01", 
		andre_ns + "cc_r_legFK_01", andre_ns + "cc_r_shinFK_01", andre_ns + "cc_r_ankleFK_01", andre_ns + "cc_r_toeFK_01", andre_ns + "Character_ctrl_01", andre_ns + "cc_globalMove_01", andre_ns + "cc_l_bendyShld_01",
		andre_ns + "cc_l_mid_bendyArm_01", andre_ns + "cc_l_bendyElbow_01", andre_ns + "cc_l_mid_bendyForearm_01", andre_ns + "cc_r_bendyShld_01", andre_ns + "cc_r_mid_bendyArm_01", andre_ns + "cc_r_bendyElbow_01", andre_ns + "cc_r_mid_bendyForearm_01",
		andre_ns + "cc_l_bendyHip_01", andre_ns + "cc_l_mid_bendyThigh_01", andre_ns + "cc_l_bendyKnee_01", andre_ns + "cc_l_mid_bendyShin_01", andre_ns + "cc_l_bendyAnkle_01",
		andre_ns + "cc_r_bendyHip_01", andre_ns + "cc_r_mid_bendyThigh_01", andre_ns + "cc_r_bendyKnee_01", andre_ns + "cc_r_mid_bendyShin_01", andre_ns + "cc_r_bendyAnkle_01",
		andre_ns + "flexi_spine:cc_flexiSpine_mid_01"]))


	# Left Arm
	widgets["leftShoulderBendyButton"] = cmds.button(label = "", w = 14, h = 15, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_l_bendyShoulder_01"]))
	widgets["leftShoulderButton"] = cmds.button(label = "", w = 20, h = 25, bgc = [0, 0, 1], c = partial(selectControls, [andre_ns + "cc_l_shld_01"]))
	widgets["leftArmFKButton"] = cmds.button(label = "FK", w = 65, h = 60, bgc = [0, 0, 1], c = partial(selectControls, [andre_ns + "cc_l_armFK_01"]))
	widgets["leftForearmFKButton"] = cmds.button(label = "FK", w = 75, h = 40, bgc = [0, 0, 1], c = partial(selectControls, [andre_ns + "cc_l_forearmFK_01"]))
	widgets["leftHandFKButton"] = cmds.button(label = "FK", w = 45, h = 20, bgc = [0, 0, 1], c = partial(selectControls, [andre_ns + "cc_l_handFK_01"]))

	widgets["leftArmIKButton"] = cmds.button(label = "IK", w = 15, h = 40, bgc = [0, 0, 1], c = partial(selectControls, [andre_ns + "cc_l_armIK_01"]))
	widgets["leftElbowIKButton"] = cmds.button(label = "IK", w = 20, h = 20, bgc = [0, 0, 1], c = partial(selectControls, [andre_ns + "cc_l_elbowIK_01"]))
	
	widgets["l_bendyShldButton"] = cmds.button(label = "", w = 20, h = 20, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_l_bendyShld_01"]))
	widgets["l_bendyMidArmButton"] = cmds.button(label = "", w = 20, h = 20, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_l_mid_bendyArm_01"]))
	widgets["l_bendyElbowButton"] = cmds.button(label = "", w = 20, h = 20, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_l_bendyElbow_01"]))
	widgets["l_bendyForearmButton"] = cmds.button(label = "", w = 20, h = 20, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_l_mid_bendyForearm_01"]))


	#widgets["leftArmIKFKButton"] = cmds.button(label = "IK/FK TOGGLE", w = 85, h = 20, bgc = [0.7, 0.7, 1], c = l_arm_ikfk_toggle)

	# Right Arm
	widgets["rightShoulderBendyButton"] = cmds.button(label = "", w = 14, h = 15, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_r_bendyShoulder_01"]))
	widgets["rightShoulderButton"] = cmds.button(label = "", w = 20, h = 25, bgc = [1, 0, 0], c = partial(selectControls, [andre_ns + "cc_r_shld_01"]))
	widgets["rightArmFKButton"] = cmds.button(label = "FK", w = 65, h = 60, bgc = [1, 0, 0], c = partial(selectControls, [andre_ns + "cc_r_armFK_01"]))
	widgets["rightForearmFKButton"] = cmds.button(label = "FK", w = 75, h = 40, bgc = [1, 0, 0], c = partial(selectControls, [andre_ns + "cc_r_forearmFK_01"]))
	widgets["rightHandFKButton"] = cmds.button(label = "FK", w = 45, h = 20, bgc = [1, 0, 0], c = partial(selectControls, [andre_ns + "cc_r_handFK_01"]))		

	widgets["rightArmIKButton"] = cmds.button(label = "IK", w = 15, h = 40, bgc = [1, 0, 0], c = partial(selectControls, [andre_ns + "cc_r_armIK_01"]))
	widgets["rightElbowIKButton"] = cmds.button(label = "IK", w = 20, h = 20, bgc = [1, 0, 0], c = partial(selectControls, [andre_ns + "cc_r_elbowIK_01"]))
	
	widgets["r_bendyShldButton"] = cmds.button(label = "", w = 20, h = 20, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_r_bendyShld_01"]))
	widgets["r_bendyMidArmButton"] = cmds.button(label = "", w = 20, h = 20, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_r_mid_bendyArm_01"]))
	widgets["r_bendyElbowButton"] = cmds.button(label = "", w = 20, h = 20, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_r_bendyElbow_01"]))
	widgets["r_bendyForearmButton"] = cmds.button(label = "", w = 20, h = 20, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_r_mid_bendyForearm_01"]))


	#widgets["rightArmIKFKButton"] = cmds.button(label = "IK/FK TOGGLE", w = 85, h = 20, bgc = [1, 0.7, 0.7], c = r_arm_ikfk_toggle)

	# Torso
	widgets["hipButton"] = cmds.button(label = "HIP", w = 75, h = 40, bgc = [0, 1, 0], c = partial(selectControls, [andre_ns + "cc_hip_01"]))
	widgets["centerOfGravityButton"] = cmds.button(label = "CENTER", w = 100, h = 15, bgc = [1, 1, 0], c = partial(selectControls, [andre_ns + "cc_COG_01"]))
	widgets["leftIKFKButton"] = cmds.button(label = "IK/FK", w = 50, h = 20, bgc = [0, 0, 1], c = partial(selectControls, [andre_ns + "cc_l_ikfk_01"]))
	widgets["rightIKFKButton"] = cmds.button(label = "IK/FK", w = 50, h = 20, bgc = [1, 0, 0], c = partial(selectControls, [andre_ns + "cc_r_ikfk_01"]))
	widgets["flexSpineMidButton"] = cmds.button(label = "MID", w = 120, h = 15, bgc = [1, 1, 0], c = partial(selectControls, [andre_ns + "flexi_spine:cc_flexiSpine_mid_01"]))
	widgets["spineAButton"] = cmds.button(label = "A", w = 17, h = 17, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_spine_a_FK_01"]))
	widgets["spineBButton"] = cmds.button(label = "B", w = 17, h = 17, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_spine_b_FK_01"]))
	widgets["spineCButton"] = cmds.button(label = "C", w = 17, h = 17, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_spine_c_FK_01"]))
	widgets["spineDButton"] = cmds.button(label = "D", w = 17, h = 17, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_spine_d_FK_01"]))
	widgets["spineEButton"] = cmds.button(label = "E", w = 17, h = 17, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_spine_e_FK_01"]))
	widgets["spineAllButton"] = cmds.button(label = "ALL", w = 50, h = 20, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_spine_e_FK_01", andre_ns + "cc_spine_d_FK_01", andre_ns + "cc_spine_c_FK_01", andre_ns + "cc_spine_b_FK_01", andre_ns + "cc_spine_a_FK_01"]))


	# Left Leg
	widgets["l_IKKneeButton"] = cmds.button(label = "IK", w = 25, h = 25, bgc = [0, 0, 1], c = partial(selectControls, [andre_ns + "cc_l_knee_01"]))		
	widgets["l_IKFootButton"] = cmds.button(label = "IK", w = 30, h = 20, bgc = [0, 0, 1], c = partial(selectControls, [andre_ns + "cc_l_foot_01"]))		
	widgets["l_IKFootRollButton"] = cmds.button(label = "IK", w = 25, h = 15, bgc = [0, 0, 1], c = partial(selectControls, [andre_ns + "cc_l_footRoll_01"]))		
	widgets["l_FKLegButton"] = cmds.button(label = "FK", w = 23, h = 90, bgc = [0, 0, 1], c = partial(selectControls, [andre_ns + "cc_l_legFK_01"]))		
	widgets["l_FKShinButton"] = cmds.button(label = "FK", w = 22, h = 70, bgc = [0, 0, 1], c = partial(selectControls, [andre_ns + "cc_l_shinFK_01"]))		
	widgets["l_FKAnkleButton"] = cmds.button(label = "FK", w = 30, h = 15, bgc = [0, 0, 1], c = partial(selectControls, [andre_ns + "cc_l_ankleFK_01"]))		
	widgets["l_FKToeButton"] = cmds.button(label = "FK", w = 30, h = 15, bgc = [0, 0, 1], c = partial(selectControls, [andre_ns + "cc_l_toeFK_01"]))		

	widgets["l_bendyHipButton"] = cmds.button(label = "", w = 20, h = 20, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_l_bendyHip_01"]))
	widgets["l_bendyThighButton"] = cmds.button(label = "", w = 20, h = 20, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_l_mid_bendyThigh_01"]))
	widgets["l_bendyKneeButton"] = cmds.button(label = "", w = 20, h = 20, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_l_bendyKnee_01"]))
	widgets["l_bendyShinButton"] = cmds.button(label = "", w = 20, h = 20, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_l_mid_bendyShin_01"]))
	widgets["l_bendyAnkleButton"] = cmds.button(label = "", w = 20, h = 20, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_l_bendyAnkle_01"]))

	#widgets["leftLegIKFKButton"] = cmds.button(label = "IK/FK TOGGLE", w = 85, h = 20, bgc = [0.7, 0.7, 1], c = l_leg_ikfk_toggle)


	# Right Leg
	widgets["r_IKKneeButton"] = cmds.button(label = "IK", w = 25, h = 25, bgc = [1, 0, 0], c = partial(selectControls, [andre_ns + "cc_r_knee_01"]))		
	widgets["r_IKFootButton"] = cmds.button(label = "IK", w = 30, h = 20, bgc = [1, 0, 0], c = partial(selectControls, [andre_ns + "cc_r_foot_01"]))
	widgets["r_IKFootRollButton"] = cmds.button(label = "IK", w = 25, h = 15, bgc = [1, 0, 0], c = partial(selectControls, [andre_ns + "cc_r_footRoll_01"]))		
	widgets["r_FKLegButton"] = cmds.button(label = "FK", w = 23, h = 90, bgc = [1, 0, 0], c = partial(selectControls, [andre_ns + "cc_r_legFK_01"]))		
	widgets["r_FKShinButton"] = cmds.button(label = "FK", w = 22, h = 70, bgc = [1, 0, 0], c = partial(selectControls, [andre_ns + "cc_r_shinFK_01"]))		
	widgets["r_FKAnkleButton"] = cmds.button(label = "FK", w = 30, h = 15, bgc = [1, 0, 0], c = partial(selectControls, [andre_ns + "cc_r_ankleFK_01"]))		
	widgets["r_FKToeButton"] = cmds.button(label = "FK", w = 30, h = 15, bgc = [1, 0, 0], c = partial(selectControls, [andre_ns + "cc_r_toeFK_01"]))		

	widgets["r_bendyHipButton"] = cmds.button(label = "", w = 20, h = 20, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_r_bendyHip_01"]))
	widgets["r_bendyThighButton"] = cmds.button(label = "", w = 20, h = 20, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_r_mid_bendyThigh_01"]))
	widgets["r_bendyKneeButton"] = cmds.button(label = "", w = 20, h = 20, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_r_bendyKnee_01"]))
	widgets["r_bendyShinButton"] = cmds.button(label = "", w = 20, h = 20, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_r_mid_bendyShin_01"]))
	widgets["r_bendyAnkleButton"] = cmds.button(label = "", w = 20, h = 20, bgc = [0, 1, 1], c = partial(selectControls, [andre_ns + "cc_r_bendyAnkle_01"]))

	#widgets["rightLegIKFKButton"] = cmds.button(label = "IK/FK TOGGLE", w = 85, h = 20, bgc = [1, 0.7, 0.7], c = r_leg_ikfk_toggle)

	# Left Hand
	widgets["leftPalmButton"] = cmds.button(label = "", w = 40, h = 40, bgc = [0, 0, 1], c = partial(selectControls, [andre_ns + "cc_l_Hand_01"]))				
	widgets["leftThumbButton"] = cmds.button(label = "", w = 12, h = 30, bgc = [0, 1, 0], c = partial(selectControls, [andre_ns + "cc_l_Thumb_01"]))				
	widgets["leftIndexButton"] = cmds.button(label = "", w = 30, h = 12, bgc = [0, 1, 0], c = partial(selectControls, [andre_ns + "cc_l_Index_01"]))				
	widgets["leftMiddleButton"] = cmds.button(label = "", w = 30, h = 12, bgc = [0, 1, 0], c = partial(selectControls, [andre_ns + "cc_l_Middle_01"]))				
	widgets["leftRingButton"] = cmds.button(label = "", w = 30, h = 12, bgc = [0, 1, 0], c = partial(selectControls, [andre_ns + "cc_l_Ring_01"]))				
	widgets["leftPinkyButton"] = cmds.button(label = "", w = 30, h = 12, bgc = [0, 1, 0], c = partial(selectControls, [andre_ns + "cc_l_Pinky_01"]))				


	# Right Hand
	widgets["rightPalmButton"] = cmds.button(label = "", w = 40, h = 40, bgc = [1, 0, 0], c = partial(selectControls, [andre_ns + "cc_r_Hand_01"]))				
	widgets["rightThumbButton"] = cmds.button(label = "", w = 12, h = 30, bgc = [0, 1, 0], c = partial(selectControls, [andre_ns + "cc_r_Thumb_01"]))				
	widgets["rightIndexButton"] = cmds.button(label = "", w = 30, h = 12, bgc = [0, 1, 0], c = partial(selectControls, [andre_ns + "cc_r_Index_01"]))				
	widgets["rightMiddleButton"] = cmds.button(label = "", w = 30, h = 12, bgc = [0, 1, 0], c = partial(selectControls, [andre_ns + "cc_r_Middle_01"]))				
	widgets["rightRingButton"] = cmds.button(label = "", w = 30, h = 12, bgc = [0, 1, 0], c = partial(selectControls, [andre_ns + "cc_r_Ring_01"]))				
	widgets["rightPinkyButton"] = cmds.button(label = "", w = 30, h = 12, bgc = [0, 1, 0], c = partial(selectControls, [andre_ns + "cc_r_Pinky_01"]))				







	# Place the buttons
	# Button is placed in the form layout. af is adjust format. It's a list that comprises two items, which are themselves lists. 
	# One of the sides is left or right, and the other is top or bottom. Could do more, but unnecessary. left and top is simplest.
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["globalControlButton"], 'left', 625), (widgets["globalControlButton"], 'top', 515) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["globalMoveButton"], 'left', 632), (widgets["globalMoveButton"], 'top', 480) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["headButton"], 'left', 331), (widgets["headButton"], 'top', 20) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["chestButton"], 'left', 285), (widgets["chestButton"], 'top', 200) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["allButtons"], 'left', 625), (widgets["allButtons"], 'top', 570) ] )

	# Left Arm
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["leftShoulderBendyButton"], 'left', 423), (widgets["leftShoulderBendyButton"], 'top', 154) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["leftShoulderButton"], 'left', 420), (widgets["leftShoulderButton"], 'top', 170) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["leftArmFKButton"], 'left', 450), (widgets["leftArmFKButton"], 'top', 200) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["leftForearmFKButton"], 'left', 520), (widgets["leftForearmFKButton"], 'top', 207) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["leftHandFKButton"], 'left', 635), (widgets["leftHandFKButton"], 'top', 212) ] )

	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["leftArmIKButton"], 'left', 609), (widgets["leftArmIKButton"], 'top', 255) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["leftElbowIKButton"], 'left', 510), (widgets["leftElbowIKButton"], 'top', 265) ] )

	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["l_bendyShldButton"], 'left', 445), (widgets["l_bendyShldButton"], 'top', 178) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["l_bendyMidArmButton"], 'left', 495), (widgets["l_bendyMidArmButton"], 'top', 178) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["l_bendyElbowButton"], 'left', 545), (widgets["l_bendyElbowButton"], 'top', 178) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["l_bendyForearmButton"], 'left', 595), (widgets["l_bendyForearmButton"], 'top', 178) ] )


	#cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["leftArmIKFKButton"], 'left', 615), (widgets["leftArmIKFKButton"], 'top', 255) ] )		

	# Right Arm
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["rightShoulderBendyButton"], 'left', 283), (widgets["rightShoulderBendyButton"], 'top', 154) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["rightShoulderButton"], 'left', 280), (widgets["rightShoulderButton"], 'top', 170) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["rightArmFKButton"], 'left', 195), (widgets["rightArmFKButton"], 'top', 200) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["rightForearmFKButton"], 'left', 115), (widgets["rightForearmFKButton"], 'top', 207) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["rightHandFKButton"], 'left', 35), (widgets["rightHandFKButton"], 'top', 212) ] )

	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["rightArmIKButton"], 'left', 89), (widgets["rightArmIKButton"], 'top', 255) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["rightElbowIKButton"], 'left', 180), (widgets["rightElbowIKButton"], 'top', 265) ] )

	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["r_bendyShldButton"], 'left', 255), (widgets["r_bendyShldButton"], 'top', 178) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["r_bendyMidArmButton"], 'left', 205), (widgets["r_bendyMidArmButton"], 'top', 178) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["r_bendyElbowButton"], 'left', 155), (widgets["r_bendyElbowButton"], 'top', 178) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["r_bendyForearmButton"], 'left', 105), (widgets["r_bendyForearmButton"], 'top', 178) ] )

	#cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["rightArmIKFKButton"], 'left', 15), (widgets["rightArmIKFKButton"], 'top', 255) ] )		

	# Torso
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["hipButton"], 'left', 320), (widgets["hipButton"], 'top', 375) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["centerOfGravityButton"], 'left', 308), (widgets["centerOfGravityButton"], 'top', 410) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["leftIKFKButton"], 'left', 400), (widgets["leftIKFKButton"], 'top', 385) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["rightIKFKButton"], 'left', 265), (widgets["rightIKFKButton"], 'top', 385) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["spineAButton"], 'left', 172), (widgets["spineAButton"], 'top', 398) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["spineBButton"], 'left', 176), (widgets["spineBButton"], 'top', 440) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["spineCButton"], 'left', 168), (widgets["spineCButton"], 'top', 489) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["spineDButton"], 'left', 124), (widgets["spineDButton"], 'top', 526) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["spineEButton"], 'left', 101), (widgets["spineEButton"], 'top', 566) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["spineAllButton"], 'left', 102), (widgets["spineAllButton"], 'top', 601) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["flexSpineMidButton"], 'left', 296), (widgets["flexSpineMidButton"], 'top', 300) ] )

	# Left Leg
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["l_IKKneeButton"], 'left', 420), (widgets["l_IKKneeButton"], 'top', 500) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["l_IKFootButton"], 'left', 420), (widgets["l_IKFootButton"], 'top', 605) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["l_IKFootRollButton"], 'left', 455), (widgets["l_IKFootRollButton"], 'top', 608) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["l_FKLegButton"], 'left', 362), (widgets["l_FKLegButton"], 'top', 431) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["l_FKShinButton"], 'left', 365), (widgets["l_FKShinButton"], 'top', 530) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["l_FKAnkleButton"], 'left', 362), (widgets["l_FKAnkleButton"], 'top', 605) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["l_FKToeButton"], 'left', 362), (widgets["l_FKToeButton"], 'top', 627) ] )

	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["l_bendyHipButton"], 'left', 390), (widgets["l_bendyHipButton"], 'top', 430) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["l_bendyThighButton"], 'left', 393), (widgets["l_bendyThighButton"], 'top', 470) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["l_bendyKneeButton"], 'left', 393), (widgets["l_bendyKneeButton"], 'top', 510) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["l_bendyShinButton"], 'left', 393), (widgets["l_bendyShinButton"], 'top', 550) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["l_bendyAnkleButton"], 'left', 393), (widgets["l_bendyAnkleButton"], 'top', 590) ] )


	#cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["leftLegIKFKButton"], 'left', 440), (widgets["leftLegIKFKButton"], 'top', 605) ] )		

	# Right Leg
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["r_IKKneeButton"], 'left', 265), (widgets["r_IKKneeButton"], 'top', 500) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["r_IKFootButton"], 'left', 260), (widgets["r_IKFootButton"], 'top', 605) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["r_IKFootRollButton"], 'left', 230), (widgets["r_IKFootRollButton"], 'top', 608) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["r_FKLegButton"], 'left', 325), (widgets["r_FKLegButton"], 'top', 431) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["r_FKShinButton"], 'left', 323), (widgets["r_FKShinButton"], 'top', 530) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["r_FKAnkleButton"], 'left', 320), (widgets["r_FKAnkleButton"], 'top', 605) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["r_FKToeButton"], 'left', 320), (widgets["r_FKToeButton"], 'top', 627) ] )

	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["r_bendyHipButton"], 'left', 300), (widgets["r_bendyHipButton"], 'top', 430) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["r_bendyThighButton"], 'left', 298), (widgets["r_bendyThighButton"], 'top', 470) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["r_bendyKneeButton"], 'left', 298), (widgets["r_bendyKneeButton"], 'top', 510) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["r_bendyShinButton"], 'left', 298), (widgets["r_bendyShinButton"], 'top', 550) ] )
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["r_bendyAnkleButton"], 'left', 298), (widgets["r_bendyAnkleButton"], 'top', 590) ] )


	#cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["rightLegIKFKButton"], 'left', 190), (widgets["rightLegIKFKButton"], 'top', 605) ] )		

	# Left Hand
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["leftPalmButton"], 'left', 560), (widgets["leftPalmButton"], 'top', 85) ] )		
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["leftThumbButton"], 'left', 575), (widgets["leftThumbButton"], 'top', 53) ] )		
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["leftIndexButton"], 'left', 600), (widgets["leftIndexButton"], 'top', 70) ] )		
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["leftMiddleButton"], 'left', 607), (widgets["leftMiddleButton"], 'top', 91) ] )		
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["leftRingButton"], 'left', 604), (widgets["leftRingButton"], 'top', 111) ] )		
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["leftPinkyButton"], 'left', 595), (widgets["leftPinkyButton"], 'top', 130) ] )		


	# Right Hand
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["rightPalmButton"], 'left', 117), (widgets["rightPalmButton"], 'top', 85) ] )		
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["rightThumbButton"], 'left', 131), (widgets["rightThumbButton"], 'top', 53) ] )		
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["rightIndexButton"], 'left', 87), (widgets["rightIndexButton"], 'top', 68) ] )		
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["rightMiddleButton"], 'left', 82), (widgets["rightMiddleButton"], 'top', 89) ] )		
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["rightRingButton"], 'left', 85), (widgets["rightRingButton"], 'top', 109) ] )		
	cmds.formLayout(widgets["formLayout"], edit = True, af = [ (widgets["rightPinkyButton"], 'left', 92), (widgets["rightPinkyButton"], 'top', 128) ] )		


	cmds.showWindow(widgets["window"])




def selectControls(controls, buttons, *args):
	
	# If you have shift held down (shift is a modifier):
	mods = cmds.getModifiers()
	if (mods & 1) > 0: 
		for control in controls:
			cmds.select(control, tgl = True)

		
	# If you have no modifiers:
	else:
		cmds.select(clear = True) # Clear the selection.

		for i in range(len(controls)):

			cmds.select(controls[i], add = True)


def go():
    buildUI()


if __name__ == '__main__':
    go()
