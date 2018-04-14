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
from PuppetCreativeSuite import buildPuppet
reload(buildPuppet)
buildPuppet.runMayaUiDemo()   
'''

import sys
import os
import datetime
import warnings
from functools import partial

from PySide import QtGui
from PySide import QtCore
from PySide import QtUiTools
import shiboken

from module import openStyleSheet
from module import collectBundels
from module import openGeneric
from module import inputNames
from package import createLimb

reload(openStyleSheet)
reload(collectBundels)
reload(openGeneric)
reload(createLimb)
reload(inputNames)

reload(collectBundels)
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
    
    '''
        Description            
            Function for Load Ui File and passing signals from Ui to Maya core.    
    '''
    
    def __init__(self):
        super(Puppet, self).__init__(MAINWINDOW)
        
        #Load Qt UI to maya
        loader = QtUiTools.QUiLoader()
        uifile = QtCore.QFile (UI_PATH)       
        uifile.open (QtCore.QFile.ReadOnly)
        self.ui = loader.load (uifile, MAINWINDOW)
        uifile.close()
        self.ui.setAttribute (QtCore.Qt.WA_DeleteOnClose, True)
        #self.ui.show ()        
        
        mainWindow = pymel.lsUI (wnd=1)[0]        
        #self.ui.setObjectName ('MainWindow') 
        
        if pymel.dockControl ('MainWindow', q=1, ex=1) :
            pymel.deleteUI('MainWindow', ctl=1)

        self.floatingLayout = pymel.paneLayout (cn='single', w=300, p=mainWindow)

        cmds.dockControl ('MainWindow', l='Smart Bake - v0.1', area='left', content=self.floatingLayout, allowedArea=['right', 'left'])        
        cmds.control ('MainWindow', e=1, p=self.floatingLayout)
         
        try :
            styleSheet = openStyleSheet.StyleSheet (self.ui)
            styleSheet.setStyleSheet ()            
        except :
            pass  
         
        self._fitSkeleyonPath =  os.path.join (CURRENT_PATH, 'resources') 
                
        self.loadFitSkeletons()       
        self.input = inputNames.Names()  
          
        self.ui.button_fitJoints.clicked.connect (self.createFitJoints)
        self.ui.button_lableOn.clicked.connect (partial (self.lableVisibility, True))
        self.ui.button_lableOff.clicked.connect (partial (self.lableVisibility, False))
        self.ui.button_updateTwistJoints.clicked.connect (self.updateTwistJoints)
        self.ui.spinBox_jointRadius.valueChanged.connect (self.setJointRadius)
        self.ui.button_jointRadiusReset.clicked.connect (self.jointRadiusReset)
     
        self.ui.button_build.clicked.connect (self.build)
        self.ui.button_reBuild.clicked.connect (self.reBuild)
        
        self.ui.slider_controlScale.valueChanged.connect (self.controlScale)
        self.ui.button_controlScale.clicked.connect (self.resetControlScale)

   
    def loadFitSkeletons (self):   
        
        '''
        Description
            Function for collect the Fit Skeleton modules from resources and load to QComboBox                        
            :Type - class function (method)            
            :param   None
            :attribute _fitSkeletons    <dict>    Example {'NAME': module}
            :return  None
        '''    
       
        validateBundle = collectBundels.Bundles (path=self._fitSkeleyonPath, moduleType='Fit Skeleton', bundelType='validate')           
        self._validBuldle = validateBundle.getValidBundles ()         
        result = collectBundels.reorder (self._validBuldle, 'ORDER')            
        #print 'self._validBuldle', self._validBuldle
        
        self.ui.comboBox_fitJoints.clear()         
        #self.ui.comboBox_fitJoints.addItem('None')      
        
        self._fitSkeletons = {}
                
        for ing, module in result.items () :
            currentModule = self._validBuldle[module]                    
            self.ui.comboBox_fitJoints.addItem(currentModule['NAME'])
            self._fitSkeletons.setdefault(currentModule['NAME'], currentModule)
            

    def createFitJoints (self):     
           
        currentSkeleton = str(self.ui.comboBox_fitJoints.currentText())
        
        if currentSkeleton=='None':            
            warnings.warn ('Current skeleton does not valid') 
            return None        
        
        bundle = self._fitSkeletons[currentSkeleton]  

        executeModule = 'from {} import {}\nreload({})\nresult = {}.{}()\nresult.createSkeleton()'.format ( 'resources', 
                                                                                                            bundle['__name__'], 
                                                                                                            bundle['__name__'], 
                                                                                                            bundle['__name__'],
                                                                                                            bundle['CLASS'])
                  
        #=======================================================================
        # currentModule = 'from {} import {}\nresult = {}.{}()\nresult.createSkeleton()'.format ( 'resources', 
        #                                                                                         bundle['__name__'], 
        #                                                                                         bundle['__name__'],
        #                                                                                         bundle['CLASS'])  
        #=======================================================================        
       
        try :        
            exec (executeModule)
        except Exception as exceptResult:   
            raise Exception ('fit skeleton create error', exceptResult)
        
    
    def lableVisibility (self, value):
        
        generic = openGeneric.Generic()        
        generic.jointLabelVisibility(value)
        
        
    def updateTwistJoints (self):
        currentJoints = pymel.ls(sl=True)
        value = int(self.ui.spinBox_twistJoints.value())       
        
        generic = openGeneric.Generic()        
        generic.splitJoints(currentJoints, value)        
        
        
    def jointRadiusReset (self):
        
        value = 0.1     
        self.ui.spinBox_jointRadius.setValue (value)
        generic = openGeneric.Generic()        
        generic.setJointRadius(value)  
        
        
    def setJointRadius (self):
        value = float (self.ui.spinBox_jointRadius.value())        
        generic = openGeneric.Generic()        
        generic.setJointRadius(value)
        
        
    def controlScale(self):          
        value = self.ui.slider_controlScale.value()        
        self.ui.button_controlScale.setText('{}%'.format(value))
        
    def resetControlScale(self):
        self.ui.slider_controlScale.setValue(100)    
                    
    def build (self):        

        self.buildBiped()
    
        
    def reBuild (self):
        pass
    
    
    def buildBiped(self):
        
        radius = float(self.ui.slider_controlScale.value())/100.00  

        generic = openGeneric.Generic()
              
        leftPelvis = generic.getJointFromLabel(1, 'Pelvis', False)
        leftKnee = generic.getJointFromLabel(1, 'Knee', False)
        leftAnkle = generic.getJointFromLabel(1, 'Ankle', False)   
        leftPoleVector = generic.getJointFromLabel(1, 'LegPoleVector', False)   
        
        
        if not leftPelvis or not leftKnee or not leftAnkle:
            warnings.warn ('leg fit skeleton is wrong.')            
            return None  
        
        #create left leg puppet        
        limb = createLimb.Limb( side=self.input._leftSide,
                                type=self.input._leg,
                                start={self.input._pelvis: leftPelvis[0]},
                                middle={self.input._knee: leftKnee[0]},
                                end={self.input._ankle: leftAnkle[0]},
                                poleVector={self.input._legPoleVector: leftPoleVector[0]},
                                radius=radius)        
        limb.create()

        
                
        #create left leg   
        
        
#End##################################################################################