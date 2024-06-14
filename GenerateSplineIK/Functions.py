import math
from maya import cmds
##Functions
def GetDistance(inp1,inp2):
    return math.sqrt((inp1[0]-inp2[0])**2+(inp1[1]-inp2[1])**2+(inp1[2]-inp2[2])**2)
def VectorAdd(inp1,inp2):
    return [inp1[0]+inp2[0],inp1[1]+inp2[1],inp1[2]+inp2[2]]
def VectorSub(inp1,inp2):
    return [inp1[0]-inp2[0],inp1[1]-inp2[1],inp1[2]-inp2[2]]
def VectorDotScalar(inp1,inp2):
    return [inp1*inp2[0],inp1*inp2[1],inp1*inp2[2]]
def VectorDot(inp1,inp2):
    return inp1[0]*inp2[0]+inp1[1]*inp2[1]+inp1[2]*inp2[2]
def CrvBones(incrv,inname):
    bones=[]
    cmds.select(cl=True)
    points=cmds.getAttr(incrv+'.spans')+1
    for point in range(points):
        pos=cmds.getAttr(incrv+'.ep['+str(point)+']')[0]
        bones.append(cmds.joint(n=inname+str(point)+'_bone',p=pos))
    return bones

def ExtendCurveBothEnds(incrv):
    crv=cmds.duplicate(incrv,n=incrv+'_extend')[0]
    cvCount=cmds.getAttr(crv+'.degree')+cmds.getAttr(crv+'.spans')
    cvpoint0=cmds.xform(crv+'.cv[0]',q=1,t=1,ws=1)
    cvpoint1=cmds.xform(crv+'.cv[1]',q=1,t=1,ws=1)
    cvpoint_n0=cmds.xform(crv+'.cv[{}]'.format(cvCount-1),q=1,t=1,ws=1)
    cvpoint_n1=cmds.xform(crv+'.cv[{}]'.format(cvCount-2),q=1,t=1,ws=1)
    sdir=VectorDotScalar(0.02,VectorSub(cvpoint0,cvpoint1))
    edir=VectorDotScalar(0.02,VectorSub(cvpoint_n0,cvpoint_n1))
    finalcvpoint0=VectorAdd(cvpoint0,sdir)
    finalcvpoint_n0=VectorAdd(cvpoint_n0,edir)
    cmds.xform(crv+'.cv[0]',t=finalcvpoint0,ws=1)
    cvpoint_n0=cmds.xform(crv+'.cv[{}]'.format(cvCount-1),t=finalcvpoint_n0,ws=1)
    return crv

def CreateFolliclesOnMesh(objs,meshtran,ctrsize,ctrcolor):
    closenode=cmds.createNode('closestPointOnMesh',n='closestPointOnMesh1')
    mesh=cmds.listRelatives(meshtran,c=1)[0]
    cmds.connectAttr(mesh+'.outMesh',closenode+'.inMesh',f=True)
    follicles=[]
    for obj in objs:
        cmds.connectAttr(obj+'.translate',closenode+'.inPosition')
        Uvelue=cmds.getAttr(closenode+'.result.parameterU')
        Vvelue=cmds.getAttr(closenode+'.result.parameterV')
        fol_name=cmds.createNode('follicle')
        cmds.connectAttr(mesh+'.outMesh',fol_name+'.inputMesh')
        cmds.connectAttr(mesh+'.worldMatrix',fol_name+'.inputWorldMatrix')
        cmds.select(fol_name)
        fol_up_name=cmds.pickWalk(d='up')[0]
        follicles.append(fol_up_name)
        cmds.connectAttr(fol_name+'.outTranslate',fol_up_name+'.translate')
        cmds.connectAttr(fol_name+'.outRotate',fol_up_name+'.rotate')
        cmds.setAttr(fol_name+'.parameterU',Uvelue)
        cmds.setAttr(fol_name+'.parameterV',Vvelue)
        boxCtr=cmds.curve(d=1,n=obj+'_boxCtr',p=[[-0.5*ctrsize,0.5*ctrsize,0.5*ctrsize],[0.5*ctrsize,0.5*ctrsize,0.5*ctrsize],[0.5*ctrsize,0.5*ctrsize,-0.5*ctrsize],[-0.5*ctrsize,0.5*ctrsize,-0.5*ctrsize],[-0.5*ctrsize,-0.5*ctrsize,-0.5*ctrsize],[-0.5*ctrsize,-0.5*ctrsize,0.5*ctrsize],[-0.5*ctrsize,0.5*ctrsize,0.5*ctrsize],[-0.5*ctrsize,0.5*ctrsize,-0.5*ctrsize],[0.5*ctrsize,0.5*ctrsize,-0.5*ctrsize],[0.5*ctrsize,-0.5*ctrsize,-0.5*ctrsize],[-0.5*ctrsize,-0.5*ctrsize,-0.5*ctrsize],[-0.5*ctrsize,-0.5*ctrsize,0.5*ctrsize],[0.5*ctrsize,-0.5*ctrsize,0.5*ctrsize],[0.5*ctrsize,-0.5*ctrsize,-0.5*ctrsize],[0.5*ctrsize,-0.5*ctrsize,0.5*ctrsize],[0.5*ctrsize,0.5*ctrsize,0.5*ctrsize]])
        boxctr_grp=cmds.group(boxCtr,n=boxCtr+'_grp')
        cmds.parent(boxctr_grp,obj)
        cmds.xform(boxctr_grp,t=[0,0,0],ro=[0,0,0])
        cmds.parent(boxctr_grp,fol_up_name)
        SetBoxCrvColor(boxCtr,ctrcolor)
        cmds.parentConstraint(boxCtr,obj,mo=True)
        cmds.disconnectAttr(obj+'.translate',closenode+'.inPosition')
    cmds.delete(closenode)
    return follicles

def SetBoxCrvColor(incrv,incolor):
    cmds.setAttr(incrv+'.overrideEnabled',1)
    cmds.setAttr(incrv+'.drawOverride.overrideRGBColors',1)
    cmds.setAttr(incrv+'.drawOverride.overrideColorRGB.overrideColorR',incolor[0])
    cmds.setAttr(incrv+'.drawOverride.overrideColorRGB.overrideColorG',incolor[1])
    cmds.setAttr(incrv+'.drawOverride.overrideColorRGB.overrideColorB',incolor[2])

GenerateBtn_Cmd='''
try:
    cmds.select(crv)
    cmds.delete(rigGrp)
    cmds.delete('skinBones_grp')
except:
    pass
import Functions as Funs
cmds.button('GenerateBtn',e=1,bgc=[0.9,0.9,0.1])
crvs=[]
sllist=cmds.ls(sl=1)
if len(sllist)==0:
    cmds.warning('select one curve')
else:
    for item in sllist:
        childnode=cmds.listRelatives(item,c=1)
        if cmds.nodeType(childnode)=='nurbsCurve':
            crvs.append(item)
    if len(crvs)<1:
        cmds.warning('select one curve')
ctrBoxColor1=cmds.colorSliderGrp('CtrColor_box1',q=1,rgb=1)
ctrBoxColor2=cmds.colorSliderGrp('CtrColor_box2',q=1,rgb=1)
ctrBoxColor3=cmds.colorSliderGrp('CtrColor_box3',q=1,rgb=1)
skinJntCount=cmds.intSliderGrp('skinJntCount_box',q=1,v=1)
ctrLayersCount=cmds.intSliderGrp('ctrLayersCount_box',q=1,v=1)
firstLayerCtrCount=cmds.intSliderGrp('firstLayerCtrCount_box',q=1,v=1)
secondLayerCtrCount=cmds.intSliderGrp('secondLayerCtrCount_box',q=1,v=1)
thirdLayerCtrCount=cmds.intSliderGrp('thirdLayerCtrCount_box',q=1,v=1)
for crv in crvs:
    rigGrp=cmds.group(em=1,n=crv+'_RigGrp')
    cmds.setAttr(crv+'.visibility',0)
    cmds.select(cl=1)
    rootBone=cmds.joint(n=crv+'_rootBone')
    cmds.group(rootBone,n='skinBones_grp')
    Assist_grps=cmds.group(em=1,n='Assist_grps')
    cmds.parent(Assist_grps,rigGrp)
    ExtraSurfaces_grp=cmds.group(em=1,n=crv+'_ExtraSurfaces_grp')
    cmds.parent(ExtraSurfaces_grp,Assist_grps)
    cmds.rebuildCurve(crv,ch=0,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=1,kt=0,s=skinJntCount-1,d=3,tol=0.01)
    skinBones=Funs.CrvBones(crv,crv+'_skin')
    boneRadius=0.05*Funs.GetDistance(cmds.xform(skinBones[0],q=1,t=1),cmds.xform(skinBones[1],q=1,t=1))
    cmds.joint(skinBones[0],e=1,oj='xzy',secondaryAxisOrient='zup',ch=1,zso=1)
    cmds.setAttr(skinBones[-1]+'.jointOrientX',0)
    cmds.setAttr(skinBones[-1]+'.jointOrientY',0)
    cmds.setAttr(skinBones[-1]+'.jointOrientZ',0)
    for bone in skinBones:
        cmds.setAttr(bone+'.radius',boneRadius)
        cmds.parent(bone,rootBone)
    #AllCtrs/***
    AllCtr=cmds.curve(d=1,n='AllCtr',p=[[-0.5*boneRadius*5,0.5*boneRadius*5,0.5*boneRadius*5],[0.5*boneRadius*5,0.5*boneRadius*5,0.5*boneRadius*5],[0.5*boneRadius*5,0.5*boneRadius*5,-0.5*boneRadius*5],[-0.5*boneRadius*5,0.5*boneRadius*5,-0.5*boneRadius*5],[-0.5*boneRadius*5,-0.5*boneRadius*5,-0.5*boneRadius*5],[-0.5*boneRadius*5,-0.5*boneRadius*5,0.5*boneRadius*5],[-0.5*boneRadius*5,0.5*boneRadius*5,0.5*boneRadius*5],[-0.5*boneRadius*5,0.5*boneRadius*5,-0.5*boneRadius*5],[0.5*boneRadius*5,0.5*boneRadius*5,-0.5*boneRadius*5],[0.5*boneRadius*5,-0.5*boneRadius*5,-0.5*boneRadius*5],[-0.5*boneRadius*5,-0.5*boneRadius*5,-0.5*boneRadius*5],[-0.5*boneRadius*5,-0.5*boneRadius*5,0.5*boneRadius*5],[0.5*boneRadius*5,-0.5*boneRadius*5,0.5*boneRadius*5],[0.5*boneRadius*5,-0.5*boneRadius*5,-0.5*boneRadius*5],[0.5*boneRadius*5,-0.5*boneRadius*5,0.5*boneRadius*5],[0.5*boneRadius*5,0.5*boneRadius*5,0.5*boneRadius*5]])
    Funs.SetBoxCrvColor(AllCtr,[1,0.05,0.05])
    AllCtr_grp001=cmds.group(AllCtr,n='AllCtr_grp001')
    AllCtr_grp002=cmds.group(AllCtr,n='AllCtr_grp002')
    cmds.parent(AllCtr_grp001,skinBones[0])
    cmds.xform(AllCtr_grp001,t=[0,0,0],ro=[0,0,0])
    cmds.parent(AllCtr_grp001,w=1)
    cmds.parent(AllCtr_grp001,rigGrp)
    #AllCtrs***/
    baseCrv=cmds.curve(n='baseCrv',d=3,p=[[-boneRadius,0,0],[-0.33333*boneRadius,0,0],[0.33333*boneRadius,0,0],[boneRadius,0,0]])
    extendCrv=Funs.ExtendCurveBothEnds(crv)
    first_xsf=cmds.extrude(baseCrv,extendCrv,ch=0,rn=0,po=1,et=2,ucp=1,fpt=1,upn=1,rotation=0,scale=1,rsp=1,n='layer1ExtraSurface')
    cmds.parent(first_xsf,ExtraSurfaces_grp)
    cmds.delete(extendCrv)
    cmds.delete(baseCrv)
    cmds.polySmooth(first_xsf,mth=0,sdt=2,ovb=1,ofb=3,ofc=0,ost=0,dv=2,ch=0)
    cmds.polyRetopo(first_xsf,targetFaceCount=100,ch=0)
    cmds.polyAutoProjection(first_xsf,ch=0)
    firstLayerFollicles=Funs.CreateFolliclesOnMesh(skinBones,first_xsf,boneRadius*0.5,[0.9,0.05,0.05])
    cmds.group(firstLayerFollicles,n='firstLayerFollicles_grp')
    cmds.parent('firstLayerFollicles_grp',Assist_grps)
    #Generate First Ctrs Layer
    cmds.rebuildCurve(crv,ch=0,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=1,kt=0,s=firstLayerCtrCount-1,d=3,tol=0.01)
    firstLayerCtrBones=Funs.CrvBones(crv,'firstCtr')
    cmds.joint(firstLayerCtrBones[0],e=1,oj='xzy',secondaryAxisOrient='zup',ch=1,zso=1)
    cmds.setAttr(firstLayerCtrBones[-1]+'.jointOrientX',0)
    cmds.setAttr(firstLayerCtrBones[-1]+'.jointOrientY',0)
    cmds.setAttr(firstLayerCtrBones[-1]+'.jointOrientZ',0)
    cmds.group(firstLayerCtrBones,n='firstLayerCtrBones_grp')
    cmds.parent('firstLayerCtrBones_grp',AllCtr)
    layer1CtrOutGrps=[]
    for bone in firstLayerCtrBones:
        cmds.setAttr(bone+'.radius',boneRadius*3)
        toutgrp=cmds.group(em=1,n=bone+'_grp001')
        layer1CtrOutGrps.append(toutgrp)
        cmds.parent(toutgrp,'firstLayerCtrBones_grp')
        cmds.xform(toutgrp,t=cmds.xform(bone,q=1,t=1),ro=Funs.VectorAdd(cmds.xform(bone,q=1,ro=1),cmds.joint(bone,q=1,o=1)))
        layer1_boxCtr=cmds.curve(d=1,n=bone+'_layer1boxCtr',p=[[-0.5*boneRadius*2,0.5*boneRadius*2,0.5*boneRadius*2],[0.5*boneRadius*2,0.5*boneRadius*2,0.5*boneRadius*2],[0.5*boneRadius*2,0.5*boneRadius*2,-0.5*boneRadius*2],[-0.5*boneRadius*2,0.5*boneRadius*2,-0.5*boneRadius*2],[-0.5*boneRadius*2,-0.5*boneRadius*2,-0.5*boneRadius*2],[-0.5*boneRadius*2,-0.5*boneRadius*2,0.5*boneRadius*2],[-0.5*boneRadius*2,0.5*boneRadius*2,0.5*boneRadius*2],[-0.5*boneRadius*2,0.5*boneRadius*2,-0.5*boneRadius*2],[0.5*boneRadius*2,0.5*boneRadius*2,-0.5*boneRadius*2],[0.5*boneRadius*2,-0.5*boneRadius*2,-0.5*boneRadius*2],[-0.5*boneRadius*2,-0.5*boneRadius*2,-0.5*boneRadius*2],[-0.5*boneRadius*2,-0.5*boneRadius*2,0.5*boneRadius*2],[0.5*boneRadius*2,-0.5*boneRadius*2,0.5*boneRadius*2],[0.5*boneRadius*2,-0.5*boneRadius*2,-0.5*boneRadius*2],[0.5*boneRadius*2,-0.5*boneRadius*2,0.5*boneRadius*2],[0.5*boneRadius*2,0.5*boneRadius*2,0.5*boneRadius*2]])
        Funs.SetBoxCrvColor(layer1_boxCtr,ctrBoxColor1)
        cmds.xform(bone,t=[0,0,0],ro=[0,0,0])
        cmds.joint(bone,e=1,o=[0,0,0])
        cmds.parent(bone,layer1_boxCtr)
        tingrp=cmds.group(layer1_boxCtr,n=bone+'_grp002')
        cmds.parent(tingrp,toutgrp)
        cmds.xform(tingrp,t=[0,0,0],ro=[0,0,0])
    cmds.skinCluster(firstLayerCtrBones,first_xsf)
    if ctrLayersCount >1:
        #Generate Second Ctrs Layer
        second_xsf=cmds.duplicate(first_xsf,n='layer2ExtraSurface')[0]
        secondLayerFollicles=Funs.CreateFolliclesOnMesh(layer1CtrOutGrps,second_xsf,boneRadius*0.7,ctrBoxColor2)
        cmds.group(secondLayerFollicles,n='secondLayerFollicles_grp')
        cmds.rebuildCurve(crv,ch=0,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=1,kt=0,s=secondLayerCtrCount-1,d=3,tol=0.01)
        secondLayerCtrBones=Funs.CrvBones(crv,'secondCtr')
        cmds.joint(secondLayerCtrBones[0],e=1,oj='xzy',secondaryAxisOrient='zup',ch=1,zso=1)
        cmds.setAttr(secondLayerCtrBones[-1]+'.jointOrientX',0)
        cmds.setAttr(secondLayerCtrBones[-1]+'.jointOrientY',0)
        cmds.setAttr(secondLayerCtrBones[-1]+'.jointOrientZ',0)
        cmds.group(secondLayerCtrBones,n='secondLayerCtrBones_grp')
        cmds.parent('secondLayerCtrBones_grp',AllCtr)
        cmds.setAttr('secondLayerFollicles_grp.visibility',0)
        cmds.parent('secondLayerFollicles_grp',Assist_grps)
        layer2CtrOutGrps=[]
        for bone in secondLayerCtrBones:
            cmds.setAttr(bone+'.radius',boneRadius*4)
            toutgrp=cmds.group(em=1,n=bone+'_grp001')
            layer2CtrOutGrps.append(toutgrp)
            cmds.parent(toutgrp,'secondLayerCtrBones_grp')
            cmds.xform(toutgrp,t=cmds.xform(bone,q=1,t=1),ro=Funs.VectorAdd(cmds.xform(bone,q=1,ro=1),cmds.joint(bone,q=1,o=1)))
            layer2_boxCtr=cmds.curve(d=1,n=bone+'_layer2boxCtr',p=[[-0.5*boneRadius*3,0.5*boneRadius*3,0.5*boneRadius*3],[0.5*boneRadius*3,0.5*boneRadius*3,0.5*boneRadius*3],[0.5*boneRadius*3,0.5*boneRadius*3,-0.5*boneRadius*3],[-0.5*boneRadius*3,0.5*boneRadius*3,-0.5*boneRadius*3],[-0.5*boneRadius*3,-0.5*boneRadius*3,-0.5*boneRadius*3],[-0.5*boneRadius*3,-0.5*boneRadius*3,0.5*boneRadius*3],[-0.5*boneRadius*3,0.5*boneRadius*3,0.5*boneRadius*3],[-0.5*boneRadius*3,0.5*boneRadius*3,-0.5*boneRadius*3],[0.5*boneRadius*3,0.5*boneRadius*3,-0.5*boneRadius*3],[0.5*boneRadius*3,-0.5*boneRadius*3,-0.5*boneRadius*3],[-0.5*boneRadius*3,-0.5*boneRadius*3,-0.5*boneRadius*3],[-0.5*boneRadius*3,-0.5*boneRadius*3,0.5*boneRadius*3],[0.5*boneRadius*3,-0.5*boneRadius*3,0.5*boneRadius*3],[0.5*boneRadius*3,-0.5*boneRadius*3,-0.5*boneRadius*3],[0.5*boneRadius*3,-0.5*boneRadius*3,0.5*boneRadius*3],[0.5*boneRadius*3,0.5*boneRadius*3,0.5*boneRadius*3]])
            Funs.SetBoxCrvColor(layer2_boxCtr,ctrBoxColor2)
            cmds.xform(bone,t=[0,0,0],ro=[0,0,0])
            cmds.joint(bone,e=1,o=[0,0,0])
            cmds.parent(bone,layer2_boxCtr)
            tingrp=cmds.group(layer2_boxCtr,n=bone+'_grp002')
            cmds.parent(tingrp,toutgrp)
            cmds.xform(tingrp,t=[0,0,0],ro=[0,0,0])
        cmds.skinCluster(secondLayerCtrBones,second_xsf)
    if ctrLayersCount == 3:
        #Generate Third Ctrs Layer
        third_xsf=cmds.duplicate(first_xsf,n='layer3ExtraSurface')[0]
        thirdLayerFollicles=Funs.CreateFolliclesOnMesh(layer2CtrOutGrps,third_xsf,boneRadius*0.9,ctrBoxColor3)
        cmds.group(thirdLayerFollicles,n='thirdLayerFollicles_grp')
        cmds.rebuildCurve(crv,ch=0,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=1,kt=0,s=thirdLayerCtrCount-1,d=3,tol=0.01)
        thirdLayerCtrBones=Funs.CrvBones(crv,'thirdCtr')
        cmds.joint(thirdLayerCtrBones[0],e=1,oj='xzy',secondaryAxisOrient='zup',ch=1,zso=1)
        cmds.setAttr(thirdLayerCtrBones[-1]+'.jointOrientX',0)
        cmds.setAttr(thirdLayerCtrBones[-1]+'.jointOrientY',0)
        cmds.setAttr(thirdLayerCtrBones[-1]+'.jointOrientZ',0)
        cmds.group(thirdLayerCtrBones,n='thirdLayerCtrBones_grp')
        cmds.parent('thirdLayerCtrBones_grp',AllCtr)
        cmds.setAttr('thirdLayerFollicles_grp.visibility',0)
        cmds.parent('thirdLayerFollicles_grp',Assist_grps)
        for bone in thirdLayerCtrBones:
            cmds.setAttr(bone+'.radius',boneRadius*5)
            toutgrp=cmds.group(em=1,n=bone+'_grp001')
            cmds.parent(toutgrp,'thirdLayerCtrBones_grp')
            cmds.xform(toutgrp,t=cmds.xform(bone,q=1,t=1),ro=Funs.VectorAdd(cmds.xform(bone,q=1,ro=1),cmds.joint(bone,q=1,o=1)))
            layer3_boxCtr=cmds.curve(d=1,n=bone+'_layer3boxCtr',p=[[-0.5*boneRadius*4,0.5*boneRadius*4,0.5*boneRadius*4],[0.5*boneRadius*4,0.5*boneRadius*4,0.5*boneRadius*4],[0.5*boneRadius*4,0.5*boneRadius*4,-0.5*boneRadius*4],[-0.5*boneRadius*4,0.5*boneRadius*4,-0.5*boneRadius*4],[-0.5*boneRadius*4,-0.5*boneRadius*4,-0.5*boneRadius*4],[-0.5*boneRadius*4,-0.5*boneRadius*4,0.5*boneRadius*4],[-0.5*boneRadius*4,0.5*boneRadius*4,0.5*boneRadius*4],[-0.5*boneRadius*4,0.5*boneRadius*4,-0.5*boneRadius*4],[0.5*boneRadius*4,0.5*boneRadius*4,-0.5*boneRadius*4],[0.5*boneRadius*4,-0.5*boneRadius*4,-0.5*boneRadius*4],[-0.5*boneRadius*4,-0.5*boneRadius*4,-0.5*boneRadius*4],[-0.5*boneRadius*4,-0.5*boneRadius*4,0.5*boneRadius*4],[0.5*boneRadius*4,-0.5*boneRadius*4,0.5*boneRadius*4],[0.5*boneRadius*4,-0.5*boneRadius*4,-0.5*boneRadius*4],[0.5*boneRadius*4,-0.5*boneRadius*4,0.5*boneRadius*4],[0.5*boneRadius*4,0.5*boneRadius*4,0.5*boneRadius*4]])
            Funs.SetBoxCrvColor(layer3_boxCtr,ctrBoxColor3)
            cmds.xform(bone,t=[0,0,0],ro=[0,0,0])
            cmds.joint(bone,e=1,o=[0,0,0])
            cmds.parent(bone,layer3_boxCtr)
            tingrp=cmds.group(layer3_boxCtr,n=bone+'_grp002')
            cmds.parent(tingrp,toutgrp)
            cmds.xform(tingrp,t=[0,0,0],ro=[0,0,0])
        cmds.skinCluster(thirdLayerCtrBones,third_xsf)
'''

DeleteBtn_Cmd='''
cmds.setAttr(crv+'.visibility',1)
try:
    cmds.delete(rigGrp)
    cmds.delete('skinBones_grp')
except:
    pass
'''

ctrLayersCount_box_ChangeCmd='''
tv=cmds.intSliderGrp('ctrLayersCount_box',q=1,v=1)
if tv==1:
    cmds.intSliderGrp('secondLayerCtrCount_box',e=1,enable=False)
    cmds.intSliderGrp('thirdLayerCtrCount_box',e=1,enable=False)
    cmds.colorSliderGrp('CtrColor_box2',e=1,enable=False)
    cmds.colorSliderGrp('CtrColor_box3',e=1,enable=False)
if tv==2:
    cmds.intSliderGrp('secondLayerCtrCount_box',e=1,enable=True)
    cmds.intSliderGrp('thirdLayerCtrCount_box',e=1,enable=False)
    cmds.colorSliderGrp('CtrColor_box2',e=1,enable=True)
    cmds.colorSliderGrp('CtrColor_box3',e=1,enable=False)
if tv==3:
    cmds.intSliderGrp('secondLayerCtrCount_box',e=1,enable=True)
    cmds.intSliderGrp('thirdLayerCtrCount_box',e=1,enable=True)
    cmds.colorSliderGrp('CtrColor_box2',e=1,enable=True)
    cmds.colorSliderGrp('CtrColor_box3',e=1,enable=True)
'''