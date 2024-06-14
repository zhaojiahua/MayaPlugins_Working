import os
from maya import cmds
import ZClasses as ZCL
cur_path=os.path.dirname(__file__)
uipath=os.path.join(cur_path,'GenUI.ui')
def onMayaDroppedPythonFile(obj):
    if cmds.window('GenCrvDialog',q=1,ex=1):
        cmds.deleteUI('GenCrvDialog')
    uiwind=cmds.loadUI(f=uipath)
    cmds.button('OKBtn',e=1,bgc=[0.85,0.8,0.9],c=ZCL.ForOKBtn)
    cmds.button('CancelBtn',e=1,bgc=[0.8,0.85,0.9],c="cmds.deleteUI('GenCrvDialog')")
    cmds.intSliderGrp('crvCount_box',field=True,minValue=3,maxValue=100,fieldMinValue=1,fieldMaxValue=200,value=10,p='horizontalLayout')
    cmds.showWindow(uiwind)
