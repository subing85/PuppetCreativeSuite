'''
Puppet Creative Suite v1.0.0
Date : March 28, 2018
Last modified: March 28, 2018
Author: Subin. Gopi (subing85@gmail.com)

# Copyright (c) 2018, Subin Gopi
# All rights reserved.

# WARNING! All changes made in this file will be lost!

Description
    This basi core module for Puppet Creative Suite
 
example   
from publish import studioPublish
reload(studioPublish)
window = studioPublish.Publish(types='compositing')
window.show ()      

'''

import sys
import os
import datetime
from functools import partial

from PySide import QtGui
from PySide import QtCore
from PySide import QtUiTools
import shiboken

from maya import cmds
from maya import mel
from pymel import core as pymel
from maya import OpenMayaUI as omu
from maya import OpenMaya as om

CURRENT_PATH = os.path.join (os.path.dirname (__file__))
UI_PATH = os.path.join (CURRENT_PATH, 'ui', 'buildPuppet_ui.ui')
MAINWINDOW = shiboken.wrapInstance (long(omu.MQtUtil.mainWindow()), QtGui.QWidget)

def runMayaUiDemo():
    
    '''
    Description            
        Function for load the class and delete the exists 'UI' in the scene.
        
        :Type - standalone function        
        :param    None        
        :return   None
        
        :example to execute        

            import buildPuppet    
            buildPuppet.runMayaUiDemo ()        
    '''    
    
    if (cmds.window("MainWindow", ex=True)):
        cmds.deleteUI ('MainWindow')
    else:
        #sys.stdout.write("tool is already open!\n")
        pass
        
    Puppet ()
    

class Puppet (QtGui.QMainWindow):
    
    def __init__(self):
        super(Puppet, self).__init__(MAINWINDOW)

        #Load Qt UI to maya
        loader      = QtUiTools.QUiLoader()
        uifile      = QtCore.QFile (UI_PATH)       
        uifile.open (QtCore.QFile.ReadOnly)
        self.ui     = loader.load (uifile, MAINWINDOW)
        uifile.close()
        self.ui.setAttribute (QtCore.Qt.WA_DeleteOnClose, True)
        self.ui.show ()
        
        
#End##################################################################################