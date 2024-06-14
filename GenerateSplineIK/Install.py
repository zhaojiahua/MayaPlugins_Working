import os
from maya import cmds
import Functions as Funs
cur_path=os.path.dirname(__file__)
uipath=os.path.join(cur_path,'ui.ui')

def onMayaDroppedPythonFile(obj):
    if cmds.window('SplineIKDialog',q=1,ex=1):
        cmds.deleteUI('SplineIKDialog')
    uiwind=cmds.loadUI(f=uipath)
    cmds.button('GenerateBtn',e=1,bgc=[0.9,0.9,0.9],c=Funs.GenerateBtn_Cmd)
    cmds.button('DeleteBtn',e=1,bgc=[0.9,0.9,0.9],c=Funs.DeleteBtn_Cmd)
    CtrColor_box1=cmds.colorSliderGrp('CtrColor_box1',rgb=(0.1, 0.1, 0.9),p='horizontalLayout006')
    CtrColor_box2=cmds.colorSliderGrp('CtrColor_box2',rgb=(0.1, 0.9 , 0.1),p='horizontalLayout007')
    CtrColor_box3=cmds.colorSliderGrp('CtrColor_box3',rgb=(0.9, 0.1, 0.1),p='horizontalLayout008',enable=False)
    cmds.intSliderGrp('skinJntCount_box',field=True,minValue=1,maxValue=200,fieldMinValue=1,fieldMaxValue=200,value=15,p='horizontalLayout001')
    cmds.intSliderGrp('ctrLayersCount_box',field=True,minValue=1,maxValue=3,fieldMinValue=1,fieldMaxValue=3,value=2,p='horizontalLayout002',cc=Funs.ctrLayersCount_box_ChangeCmd)
    cmds.intSliderGrp('firstLayerCtrCount_box',field=True,minValue=1,maxValue=200,fieldMinValue=1,fieldMaxValue=200,value=10,p='horizontalLayout003')
    cmds.intSliderGrp('secondLayerCtrCount_box',field=True,minValue=1,maxValue=100,fieldMinValue=1,fieldMaxValue=100,value=7,p='horizontalLayout004')
    cmds.intSliderGrp('thirdLayerCtrCount_box',field=True,minValue=1,maxValue=10,fieldMinValue=1,fieldMaxValue=10,value=3,p='horizontalLayout005',enable=False)
    cmds.showWindow(uiwind)
