'''
Foot for Puppet Creative Suite v1.0.0
Date : April 25, 2018
Last modified: May 03, 2018
Author: Subin. Gopi (subing85@gmail.com)

# Copyright (c) 2018, Subin Gopi
# All rights reserved.

# WARNING! All changes made in this file will be lost!

Description
    Module for create foot setup
 
example   
from package import createFinger
finger = createFinger.Finger( side=self.input._leftSide, type=self.input._armFinger, wrist=leftWrist[0], radius=radius) 
'''

from module import openGeneric
from module import inputNames
from module import openControls

reload(openGeneric)
reload(inputNames)
reload(openControls)

from pymel import core as pymel

class Finger(object):
    
    def __init__(self, **kwargs):
        
        '''
        Description
            Function for create the limb for Puppet Creative Suite                    
            :Type - class function (method)            
            :param     side    <str>    example 'L'
            :param     type    <str>    example 'Leg'            
            :param     wrist   <str>    example 'L_Pelvis'
            :param     radius   <float>  example 1.00
            :return    None
        '''        
        
        self.side = None
        self.type = None
        self.wrist = None
        self.radius = 1.00
                
        self.input = inputNames.Names()         
        self.control = openControls.Controls()        
        
        if 'side' in kwargs:
            self.side = kwargs['side']
            
        if 'type' in kwargs:
            self.type = kwargs['type']   
            
        if 'wrist' in kwargs:
            self.wrist = kwargs['wrist']  
                                    
        if 'radius' in kwargs:
            self.radius = kwargs['radius']  
                    
        
    def create(self):
        
        pymel.undoInfo(openChunk=1) 
        
        generic = openGeneric.Generic()
        
        basejoints = self.wrist.getChildren()
        
        if not basejoints:
            return False
        
        jointGroup = generic.getNameStyle ([self.side, self.type, '{}_{}'.format (self.input._joint, self.input._group)])
        jointGroup = generic.createGroup(None, jointGroup)
        
        controlGroup = generic.getNameStyle ([self.side, self.type, '{}_{}'.format (self.input._control, self.input._group)])
        controlGroup = generic.createGroup(None, controlGroup)        
        
        wristJoint = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._wrist), self.input._joint])         
        wristJoint = generic.createJoint (radius=0.1, name=wristJoint, position=self.wrist)   
        
        wristJointGroup = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._wrist), '{}_{}' .format(self.input._joint, self.input._group)])       
        wristJointGroup = generic.createGroup(None, wristJointGroup)        
        generic.snap(self.wrist, wristJointGroup)
        wristJoint.setParent(wristJointGroup)  
        wristJointGroup.setParent(jointGroup) 

        #wrist controls
        nullWristFk, shapeWristFk, offsetWristFk, groupWristFk = self.control.create(   type='SmoothSphere', 
                                                                                        name='{}_{}'.format(self.type, self.input._wrist), 
                                                                                        side=self.side, 
                                                                                        radius=self.radius/2.0, 
                                                                                        orientation=[0,0,0], 
                                                                                        positionNode=wristJoint)           
       
        constraint = generic.getNameStyle([self.side, '{}_{}'.format(self.type, self.input._wrist), '{}_{}_{}'.format(self.input._joint, self.input._group, self.input._parentConstraint)])
        pymel.parentConstraint(nullWristFk, wristJointGroup, w=1, n=constraint)        
        groupWristFk.setParent(controlGroup)  
        
        fingerCtrlGroup = generic.getNameStyle ([self.side, self.type, '{}_{}_{}'.format (self.input._arm, self.input._control, self.input._group)])       
        fingerCtrlGroup = generic.createGroup(None, fingerCtrlGroup)        
        generic.snap(self.wrist, fingerCtrlGroup)
        fingerCtrlGroup.setParent(controlGroup) 
        
        constraint = generic.getNameStyle([self.side, self.type, '{}_{}_{}_{}'.format (self.input._arm, self.input._control, self.input._group, self.input._parentConstraint)])
        
        pymel.parentConstraint(nullWristFk, fingerCtrlGroup, w=1, n=constraint)
        pymel.scaleConstraint(nullWristFk, fingerCtrlGroup, w=1, o=(1,1,1), n=constraint)

        for eachBaseJoint in basejoints:   
                       
            childObjects = generic.getHierarchys(eachBaseJoint)
            
            if not childObjects:
                continue
            
            if not generic.jointHasValid (childObjects[0]):
                continue                
            
            currentFinger = childObjects[0].getAttr('otherType')
            
            fingerJoints = []
            
            fingerControlGroup = generic.getNameStyle ([self.side, self.type, '{}_{}_{}'.format (currentFinger, self.input._control, self.input._group)])
            fingerControlGroup = generic.createGroup(None, fingerControlGroup)              
            fingerControlGroup.setParent(fingerCtrlGroup)            
            
            jointGroup.addAttr('{}{}'.format(currentFinger, self.input._armCurl),  at='double', dv=0, k=True)            
            jointGroup.addAttr('{}{}'.format(currentFinger, self.input._armTwist),  at='double', dv=0, k=True)            
            jointGroup.addAttr('{}{}'.format(currentFinger, self.input._armRotate),  at='double', dv=0, k=True) 
            
            #Finger fk joints
            for index in range (len(childObjects)):                
                paddingSize = '{}{}'.format (generic.padding (index+1, 2), index+1)                        
                currentJoint = generic.getNameStyle ([self.side, '{}_{}_{}'.format(self.type, currentFinger, paddingSize), self.input._fk])         
                currentJoint = generic.createJoint (radius=0.1, name=currentJoint, position=childObjects[index])
                
                if len(fingerJoints)>0:                    
                    currentJoint.setParent(fingerJoints[-1])
                    
                fingerJoints.append(currentJoint)
  
            fingerJoints[0].setParent(wristJoint)                    
  
            #Finger fk controls            
            fingerControls =[]                
            for index in range (len(fingerJoints)):    
                
                paddingSize = '{}{}'.format (generic.padding (index+1, 2), index+1) 
                   
                if index!=len(fingerJoints)-1:                            
                    nullFk, shapeFk, offsetFk, groupFk = self.control.create(   type='Circle', 
                                                                                name='{}_{}_{}_{}'.format(self.type, currentFinger, paddingSize, self.input._fk), 
                                                                                side=self.side, 
                                                                                radius=self.radius/5.0, 
                                                                                orientation=[0,0,0], 
                                                                                positionNode=fingerJoints[index])
                    
                    generic.lockHideAttributes(shapeFk, 'lockHide', ['tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v'])                    
                    groupFk.setParent(fingerControlGroup) 

                    constraint = generic.getNameStyle([ self.side, 
                                                        '{}_{}_{}'.format(self.type, currentFinger, paddingSize), 
                                                        '{}_{}'.format(self.input._fk, self.input._parentConstraint)])    
                    pymel.parentConstraint(nullFk, fingerJoints[index], w=1, n=constraint)
                    
                    if index>0:
                        pymel.parentConstraint(fingerControls[-1][0], groupFk, mo=True, w=True, n=constraint)
            
                    jointGroup.connectAttr('{}{}'.format(currentFinger, self.input._armCurl), '{}.rotateZ'.format(offsetFk), f=1)
                    jointGroup.connectAttr('{}{}'.format(currentFinger, self.input._armTwist), '{}.rotateX'.format(offsetFk), f=1)
                    jointGroup.connectAttr('{}{}'.format(currentFinger, self.input._armRotate), '{}.rotateY'.format(offsetFk), f=1)
            
                    fingerControls.append([nullFk, shapeFk, offsetFk, groupFk])       

        pymel.select(cl=True)                   
        pymel.undoInfo(closeChunk=1)         
#End############################################################################################################################################