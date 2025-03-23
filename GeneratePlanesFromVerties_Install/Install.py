import shutil
import os
import sys
import re
from maya import cmds
from maya import mel
import ZGlobals
cur_path=ZGlobals.cur_path
uipath=ZGlobals.uipath
username=ZGlobals.username
version=ZGlobals.version
pluginpath=ZGlobals.pluginpath
srcpath=ZGlobals.srcpath
def onMayaDroppedPythonFile(obj):
    #create window
    ZGlobals.CreateGenWind(obj)
    #copy plugins
    try:
        os.mkdir(pluginpath)
    except:
        pass
    if pluginpath not in sys.path:
        sys.path.append(pluginpath)
    try:
        pluginfullpath=shutil.copy(srcpath,pluginpath)
        successfulLoadPlugins=cmds.loadPlugin(pluginfullpath,qt=1)
        if successfulLoadPlugins is not None:
            print("GeneratePlaneFromVertices.mll load successful")
    except:
        pass
    #add scripts to shelf
    if ZGlobals.runtimes<1 :
        mel.eval('scriptToShelf ("Gen", "import ZGlobals\\nZGlobals.CreateGenWind(None)",false);')
    ZGlobals.runtimes+=1

