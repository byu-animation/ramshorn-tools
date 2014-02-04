# Coded by Andrew Rasmussen 2013. When it is terrible or breaks blame him. Or bake him pity cookies...

# ------------------------------------------------------------------------------
import os
import glob
def SendToFarm():
        # Intial Set up...
        obj = hou.node("/obj")
        ProjectName = "TestProject"
        Geo = obj.createNode("geo", "ReadInGeo")
        KeyFrame = hou.setKeyframe()
        RenderCam = obj.createNode("cam","RenderCam")
        RenderCam.parm("resx").set("1024")
        RenderCam.parm("resy").set("1024")
        RenderCam.parm("rx").set("-15")
        RenderCam.parm("ry").set("0")
        KeyFrame.setFrame("120")
        RenderCam.parm("ry").set("360")
        RenderCam.parm("ty").set("3")
        RenderCam.parm("tz").set("10")
        RenderCam.parm("py").set("-3")
        RenderCam.parm("pz").set("-10")
        ThreePTLight = obj.createNode("three_point_light")
        ThreePTLight.parm("scale").set("50")
        KeyFrame.setFrame("120")
        ThreePTLight.parm("ry").set("0")
        KeyFrame.setFrame("200")
        ThreePTLight.parm("ry").set("360")
        EnvLight = obj.createNode("envlight")
        out = hou.node("/out")
        HQRender = obj.createNode("hq_render", "TurnTableHQ")
        TurnTableMantra = obj.createNode("mantra", "TurnTableMantra")
        HQRender.parm("hq_driver").set(TurnTableMantra)
        HQRender.parm("hq_server").set("hqueue:5000")
        HQRender.parm("hq_job_name").set("${USER}_${HIPNAME}_" + ProjectName + "TurnTableRender")
        TurnTableMantra.parm("camera").set(RenderCam)
        TurnTableMantra.parm("trange").set("normal")
        TurnTableMantra.parm("f1").set("1")
        TurnTableMantra.parm("f2").set("200")
        TurnTableMantra.parm("vm_picture").set("$HIP/MariTestCase/renders/test$F.png")




        #HQRender.parm("execute").pressButton()



        print "done"
        

# ------------------------------------------------------------------------------
#SendToFarm()
