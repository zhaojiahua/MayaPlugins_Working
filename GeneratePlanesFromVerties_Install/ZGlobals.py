import os
import sys
import re
from maya import cmds

cur_path=os.path.dirname(__file__)
uipath=os.path.join(cur_path,'GenUI.ui')
username=os.getlogin()
version=re.findall(r'\d+',sys.path[1])[0]
pluginpath="C:/Users/{}/Documents/maya/{}/plug-ins".format(username,version)
srcpath=os.path.join(cur_path,"plugins/{}/GeneratePlaneFromVertices.mll".format(version))
runtimes=0
def GenPlaneBtnF(obj):
    colsp=cmds.intSliderGrp('colCount_box',q=1,value=1)
    rowsp=cmds.intSliderGrp('rowCount_box',q=1,value=1)
    ebv=cmds.floatSliderGrp('extb_box',q=1,value=1)
    simmeshes=cmds.GeneratePlaneFromVertices(sp=colsp+1,rsp=rowsp,be=0.1*ebv)
    for item in simmeshes:
        cmds.sets(item,e=1,forceElement='initialShadingGroup')
def GenCurveBtnF(obj):
    colsp=cmds.intSliderGrp('colCount_box',q=1,value=1)
    maincurve=cmds.GeneratePlaneFromVertices(sp=colsp+1,gco=True)
def CancelBtnF(obj):
    cmds.window('GenPlanesDialog',e=1,visible=0)
def CreateGenWind(obj):
    if cmds.window('GenPlanesDialog',q=1,ex=1):
        cmds.window('GenPlanesDialog',e=1,visible=1)
    else:
        wind=cmds.loadUI(f=uipath)
        cmds.button('GenPlaneBtn',e=1,bgc=[0.85,0.8,0.9],c=GenPlaneBtnF)
        cmds.button('GenCurveBtn',e=1,bgc=[0.85,0.8,0.9],c=GenCurveBtnF)
        cmds.button('CancelBtn',e=1,bgc=[0.8,0.85,0.9],c=CancelBtnF)
        cmds.intSliderGrp('colCount_box',field=True,minValue=3,maxValue=50,fieldMinValue=1,fieldMaxValue=50,value=10,p='horizontalLayout01')
        cmds.intSliderGrp('rowCount_box',field=True,minValue=3,maxValue=50,fieldMinValue=1,fieldMaxValue=50,value=4,p='horizontalLayout02')
        cmds.floatSliderGrp('extb_box',field=True,minValue=0,maxValue=10,fieldMinValue=0,fieldMaxValue=10,value=0.2,p='horizontalLayout03')
        cmds.showWindow(wind)