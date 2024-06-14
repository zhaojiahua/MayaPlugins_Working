import copy
from maya import cmds
import math
from decimal import Decimal, getcontext
getcontext().prec = 40

class Z5Vector:
    def __init__(self):
        self.mateData=[0,0,0,0,0]
    def setElements(self,inlist):
        self.mateData=inlist
    def setElement(self,i,ivalue):
        self.mateData[i]=ivalue
    def getElement(self,i):
        return self.mateData[i]
    def __add__(self,invector):
        nvector=Z5Vector()
        for i in range(5):
            nvector.setElement(i,self.getElement(i)+invector.getElement(i))
        return nvector
    def __iadd__(self,invector):
        for i in range(5):
            self.mateData[i]+=invector.mateData[i]
    def __mul__(self,inv):
        nvector=Z5Vector()
        if isinstance(inv,Z5Vector):
            for i in range(5):
                nvector.setElement(i,self.getElement(i)*inv.getElement(i))
            return nvector
        elif isinstance(inv,float) or isinstance(inv,int) or isinstance(inv,Decimal):
            for i in range(5):
                nvector.setElement(i,inv*self.setElement(i))
            return nvector
        else:
            print('Z5Vector mul type error')
    def __repr__(self):
        return str(self.mateData)
    def __str__(self):
        return str(self.mateData)

class Z5Matrix:
    def __init__(self):
        self.mateData=[[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]]
    def setElementsAll(self,inv):
        self.mateData=inv
    def setElementsByZ5Vector(self,inc,inv):
        self.mateData[inc]=inv
    def getElementsByZ5Vector(self,inc):
        return self.mateData[inc]
    def setElement(self,inr,inc,inv):
        self.mateData[inr][inc]=inv
    def getElement(self,inr,inc):
        return self.mateData[inr][inc]
    def makeIdentity(self):
        self.mateData=[[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]]
    def Transpose(self):
        newMatrix=Z5Matrix()
        for i in range(5):
            for j in range(5):
                newMatrix.setElement(i,j,self.getElement(j,i))
        return newMatrix
    @classmethod
    def SubMatrix(cls,inm,inr,inc):
        tmatrix=copy.deepcopy(inm)
        del tmatrix[inr]
        for item in tmatrix:
            del item[inc]
        return tmatrix
    def __mul__(self,sv):
        tmatrix=Z5Matrix()
        if isinstance(sv,Z5Matrix):
            for i in range(5):
                for j in range(5):
                    tvalue=0
                    for ind in range(5):
                        tvalue+=(self.mateData[i][ind]*sv.mateData[ind][j])
                    tmatrix.setElement(i,j,tvalue)
            return tmatrix
        elif isinstance(sv,Z5Vector):
            tvector=Z5Vector()
            for i in range(5):
                tvalue=0
                for ind in range(5):
                    tvalue+=(self.mateData[i][ind]*sv.mateData[ind])
                tvector.setElement(i,tvalue)
            return tvector
        elif isinstance(sv,float) or isinstance(sv,int) or isinstance(sv,Decimal):
            for i in range(5):
                for j in range(5):
                    tmatrix.setElement(i,j,sv*self.getElement(i,j))
            return tmatrix
        else:
            print('Z5Matrix mul type error')
    def __rmul__(self,sv):
        return self*sv
    @classmethod
    def M2X2_Det(cls,inv):
        return Decimal(inv[0][0])*Decimal(inv[1][1])-Decimal(inv[0][1])*Decimal(inv[1][0])
    @classmethod
    def M3X3_Det(cls,inv):
        return inv[0][0]*Z5Matrix.M2X2_Det(Z5Matrix.SubMatrix(inv,0,0))-inv[0][1]*Z5Matrix.M2X2_Det(Z5Matrix.SubMatrix(inv,0,1))+inv[0][2]*Z5Matrix.M2X2_Det(Z5Matrix.SubMatrix(inv,0,2))
    @classmethod
    def M4X4_Det(cls,inv):
        return inv[0][0]*Z5Matrix.M3X3_Det(Z5Matrix.SubMatrix(inv,0,0))-inv[0][1]*Z5Matrix.M3X3_Det(Z5Matrix.SubMatrix(inv,0,1))+inv[0][2]*Z5Matrix.M3X3_Det(Z5Matrix.SubMatrix(inv,0,2))-inv[0][3]*Z5Matrix.M3X3_Det(Z5Matrix.SubMatrix(inv,0,3))
    def Determinant(self):
        return self.mateData[0][0]*Z5Matrix.M4X4_Det(Z5Matrix.SubMatrix(self.mateData,0,0))-self.mateData[0][1]*Z5Matrix.M4X4_Det(Z5Matrix.SubMatrix(self.mateData,0,1))+self.mateData[0][2]*Z5Matrix.M4X4_Det(Z5Matrix.SubMatrix(self.mateData,0,2))-self.mateData[0][3]*Z5Matrix.M4X4_Det(Z5Matrix.SubMatrix(self.mateData,0,3))+self.mateData[0][4]*Z5Matrix.M4X4_Det(Z5Matrix.SubMatrix(self.mateData,0,4))
    def AdjointMatrix(self):
        tmat=Z5Matrix()
        for i in range(5):
            for j in range(5):
                dsyzs=((-1)**(i+j))*Z5Matrix.M4X4_Det(Z5Matrix.SubMatrix(self.mateData,i,j))
                tmat.setElement(j,i,dsyzs)
        return tmat
    def InverseMatrix(self):
        return Decimal(1.0)/self.Determinant()*self.AdjointMatrix()
    def __repr__(self):
        return '\n[\n{}\n{}\n{}\n{}\n{}\n]'.format(self.mateData[0],self.mateData[1],self.mateData[2],self.mateData[3],self.mateData[4])
    def __str__(self):
        return '\n[\n{}\n{}\n{}\n{}\n{}\n]'.format(self.mateData[0],self.mateData[1],self.mateData[2],self.mateData[3],self.mateData[4])

def ShowVerties(inps,showradius=0.05):
    if not cmds.objExists('showSpheres_grp'):
        cmds.group(em=1,n='showSpheres_grp')
    for inp in inps:
        cmds.parent(cmds.sphere(r=showradius,ch=0,p=inp),'showSpheres_grp')
def Get2DPoints(ingeo):
    vertexCount=cmds.polyEvaluate(ingeo,vertex=1)
    xzDatas=[]
    xyDatas=[]
    yxDatas=[]
    yzDatas=[]
    zxDatas=[]
    zyDatas=[]
    xdatas=[]
    ydatas=[]
    zdatas=[]
    for i in range(vertexCount):
        xyzData=cmds.xform(ingeo+'.vtx[{}]'.format(i),q=1,t=1)
        xdatas.append(xyzData[0])
        ydatas.append(xyzData[1])
        zdatas.append(xyzData[2])
        xzDatas.append([Decimal(xyzData[0]),Decimal(xyzData[2])])
        xyDatas.append([Decimal(xyzData[0]),Decimal(xyzData[1])])
        yzDatas.append([Decimal(xyzData[1]),Decimal(xyzData[2])])
        yxDatas.append([Decimal(xyzData[1]),Decimal(xyzData[0])])
        zxDatas.append([Decimal(xyzData[2]),Decimal(xyzData[0])])
        zyDatas.append([Decimal(xyzData[2]),Decimal(xyzData[1])])
    foraxies=[[min(xdatas),max(xdatas)],[min(ydatas),max(ydatas)],[min(zdatas),max(zdatas)]]
    if JudgeAxies(foraxies)==0:
        return xyDatas,xzDatas,0,foraxies[0]
    elif JudgeAxies(foraxies)==1:
        return yxDatas,yzDatas,1,foraxies[1]
    else:
        return zxDatas,zyDatas,2,foraxies[2]

def JudgeAxies(in3Axies):
    xa=abs(in3Axies[0][0]-in3Axies[0][1])
    ya=abs(in3Axies[1][0]-in3Axies[1][1])
    za=abs(in3Axies[2][0]-in3Axies[2][1])
    if xa>ya:
        if xa>za:
            return 0
        else:
            return 2
    elif ya>za:
        return 1
    else:
        return 2

def GetAugmentedMatrix(inpts):
    S_xi0=0
    S_xi1=0
    S_xi2=0
    S_xi3=0
    S_xi4=0
    S_xi5=0
    S_xi6=0
    S_xi7=0
    S_xi8=0
    S_yi=0
    S_xiyi=0
    S_xi2yi=0
    S_xi3yi=0
    S_xi4yi=0
    for pt in inpts:
        S_xi0+=1
        S_xi1+=pt[0]
        S_xi2+=pt[0]**2
        S_xi3+=pt[0]**3
        S_xi4+=pt[0]**4
        S_xi5+=pt[0]**5
        S_xi6+=pt[0]**6
        S_xi7+=pt[0]**7
        S_xi8+=pt[0]**8
        S_yi+=pt[1]
        S_xiyi+=pt[0]*pt[1]
        S_xi2yi+=(pt[0]**2)*pt[1]
        S_xi3yi+=(pt[0]**3)*pt[1]
        S_xi4yi+=(pt[0]**4)*pt[1]
    XM=Z5Matrix()
    XM.setElement(0,0,S_xi0)
    XM.setElement(0,1,S_xi1)
    XM.setElement(0,2,S_xi2)
    XM.setElement(0,3,S_xi3)
    XM.setElement(0,4,S_xi4)
    XM.setElement(1,0,S_xi1)
    XM.setElement(1,1,S_xi2)
    XM.setElement(1,2,S_xi3)
    XM.setElement(1,3,S_xi4)
    XM.setElement(1,4,S_xi5)
    XM.setElement(2,0,S_xi2)
    XM.setElement(2,1,S_xi3)
    XM.setElement(2,2,S_xi4)
    XM.setElement(2,3,S_xi5)
    XM.setElement(2,4,S_xi6)
    XM.setElement(3,0,S_xi3)
    XM.setElement(3,1,S_xi4)
    XM.setElement(3,2,S_xi5)
    XM.setElement(3,3,S_xi6)
    XM.setElement(3,4,S_xi7)
    XM.setElement(4,0,S_xi4)
    XM.setElement(4,1,S_xi5)
    XM.setElement(4,2,S_xi6)
    XM.setElement(4,3,S_xi7)
    XM.setElement(4,4,S_xi8)
    YV=Z5Vector()
    YV.setElements([S_yi,S_xiyi,S_xi2yi,S_xi3yi,S_xi4yi])
    return XM,YV

ForOKBtn='''
import ZClasses as ZCL
from decimal import Decimal, getcontext
getcontext().prec = 40
crvpCount=cmds.intSliderGrp('crvCount_box',q=1,v=1)
for item in cmds.ls(sl=1):
    comd1,comd2,spreadAxies,minmaxv=ZCL.Get2DPoints(item)
    xm,yv=ZCL.GetAugmentedMatrix(comd1)
    A1=xm.InverseMatrix()*yv
    xm,yv=ZCL.GetAugmentedMatrix(comd2)
    A2=xm.InverseMatrix()*yv
    crvpts=[]
    if spreadAxies==0:
        alllength=(minmaxv[1]-minmaxv[0])/crvpCount
        for i in range(crvpCount+1):
            fi=Decimal(minmaxv[0]+alllength*i)
            comv1=A1.mateData[0]+A1.mateData[1]*fi+A1.mateData[2]*(fi**2)+A1.mateData[3]*(fi**3)+A1.mateData[4]*(fi**4)
            comv2=A2.mateData[0]+A2.mateData[1]*fi+A2.mateData[2]*(fi**2)+A2.mateData[3]*(fi**3)+A2.mateData[4]*(fi**4)
            crvpts.append([float(fi),float(comv1),float(comv2)])
    elif spreadAxies==1:
        alllength=(minmaxv[1]-minmaxv[0])/crvpCount
        for i in range(crvpCount+1):
            fi=Decimal(minmaxv[0]+alllength*i)
            comv1=A1.mateData[0]+A1.mateData[1]*fi+A1.mateData[2]*(fi**2)+A1.mateData[3]*(fi**3)+A1.mateData[4]*(fi**4)
            comv2=A2.mateData[0]+A2.mateData[1]*fi+A2.mateData[2]*(fi**2)+A2.mateData[3]*(fi**3)+A2.mateData[4]*(fi**4)
            crvpts.append([float(comv1),float(fi),float(comv2)])
    else:
        alllength=(minmaxv[1]-minmaxv[0])/crvpCount
        for i in range(crvpCount+1):
            fi=Decimal(minmaxv[0]+alllength*i)
            comv1=A1.mateData[0]+A1.mateData[1]*fi+A1.mateData[2]*(fi**2)+A1.mateData[3]*(fi**3)+A1.mateData[4]*(fi**4)
            comv2=A2.mateData[0]+A2.mateData[1]*fi+A2.mateData[2]*(fi**2)+A2.mateData[3]*(fi**3)+A2.mateData[4]*(fi**4)
            crvpts.append([float(comv1),float(comv2),float(fi)])
    cmds.curve(n=item+'_centerCrv',d=3,p=crvpts)
'''