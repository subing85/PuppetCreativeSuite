'''
Create Limb
Date : April 08, 2018
Last modified: March 28, 2018
Author: Subin. Gopi (subing85@gmail.com)

# Copyright (c) 2018, Subin Gopi
# All rights reserved.

# WARNING! All changes made in this file will be lost!

Description
    This module will create limb rig setup to Puppet Creative Suite
 
example   
from PuppetCreativeSuite import buildPuppet
reload(buildPuppet)
buildPuppet.runMayaUiDemo()   
'''

import warnings


from module import openGeneric
from module import inputNames
from module import openControls

reload(openGeneric)
reload(inputNames)
reload(openControls)

from pymel import core as pymel

class Limb(object):
    
    def __init__(self, **kwargs):
        
        '''
        Description
            Function for create the limb for Puppet Creative Suite                    
            :Type - class function (method)            
            :param     side    <str>    example 'L'
            :param     side    <str>    example 'Leg'            
            :param     start   <str>    example 'L_Pelvis'
            :param     middle  <str>    example 'L_Knee'
            :param     end     <str>    example 'L_Ankle'
            :param     scale   <float>  example 1.00
            :return    None
        '''        
        
        self.side = None
        self.type = None
        self.start = None
        self.startType = None        
        self.middle = None
        self.middleType = None        
        self.end = None
        self.endType = None
        self.poleVector = None
        self.radius = 1.00
                
        self.input = inputNames.Names()         
        self.control = openControls.Controls()
        
        if 'side' in kwargs:
            self.side = kwargs['side']
            
        if 'type' in kwargs:
            self.type = kwargs['type']            
            
        if 'start' in kwargs:
            self.start = kwargs['start'].values()[0]
            self.startType = kwargs['start'].keys()[0]
            
        if 'middle' in kwargs:
            self.middle = kwargs['middle'].values()[0]              
            self.middleType = kwargs['middle'].keys()[0]              

        if 'end' in kwargs:
            self.end = kwargs['end'].values()[0]  
            self.endType = kwargs['end'].keys()[0]
            
        if 'radius' in kwargs:
            self.radius = kwargs['radius']
            
        if 'poleVector' in kwargs:
            self.poleVector = kwargs['poleVector'].values()[0]            
            self.poleVectorType = kwargs['poleVector'].keys()[0]            
                        
        self.attributes = ['Translate', 'Rotate', 'Scale']   


    def create(self):
        pymel.undoInfo(openChunk=1) 
        generic = openGeneric.Generic()
        
        #Create deformer joint        
        pevlis_dk = generic.getNameStyle ([self.side, self.startType, self.input._dk])
        knee_dk = generic.getNameStyle ([self.side, self.middleType, self.input._dk])
        ankle_dk = generic.getNameStyle ([self.side, self.endType, self.input._dk])
         
        pevlis_dk = generic.createJoint (radius=0.1, name=pevlis_dk, position=self.start)
        knee_dk = generic.createJoint (radius=0.1, name=knee_dk, position=self.middle)
        ankle_dk = generic.createJoint (radius=0.1, name=ankle_dk, position=self.end)
         
        #Create FK joint 
        pevlis_fk = generic.getNameStyle ([self.side, self.startType, self.input._fk])
        knee_fk = generic.getNameStyle ([self.side, self.middleType, self.input._fk])
        ankle_fk = generic.getNameStyle ([self.side, self.input._ankle, self.input._fk])
         
        pevlis_fk = generic.createJoint (radius=0.1, name=pevlis_fk, position=self.start)
        knee_fk = generic.createJoint (radius=0.1, name=knee_fk, position=self.middle)
        ankle_fk = generic.createJoint (radius=0.1, name=ankle_fk, position=self.end)        
         
        #Create IK joint 
        pevlis_ik = generic.getNameStyle ([self.side, self.startType, self.input._ik])
        knee_ik = generic.getNameStyle ([self.side, self.middleType, self.input._ik])
        ankle_ik = generic.getNameStyle ([self.side, self.input._ankle, self.input._ik])
         
        pevlis_ik = generic.createJoint (radius=0.1, name=pevlis_ik, position=self.start)
        knee_ik = generic.createJoint (radius=0.1, name=knee_ik, position=self.middle)
        ankle_ik = generic.createJoint (radius=0.1, name=ankle_ik, position=self.end) 
         
        #set the hierarchy        
        generic.setParents ([pevlis_dk, knee_dk, ankle_dk])
        generic.setParents ([pevlis_fk, knee_fk, ankle_fk])
        generic.setParents ([pevlis_ik, knee_ik, ankle_ik])
         
        pevlis_dkGroup = generic.getNameStyle ([self.side, self.type, '{}_{}_{}'.format (self.input._dk, self.input._joint, self.input._group)])
        pevlis_ikGgroup = generic.getNameStyle ([self.side, self.type, '{}_{}_{}'.format (self.input._ik, self.input._joint, self.input._group)])
        pevlis_fkGroup = generic.getNameStyle ([self.side, self.type, '{}_{}_{}'.format (self.input._fk, self.input._joint, self.input._group)])
         
        pevlis_dkGroup = generic.createGroup(pevlis_dk, pevlis_dkGroup)
        pevlis_ikGgroup = generic.createGroup(pevlis_ik, pevlis_ikGgroup)
        pevlis_fkGroup = generic.createGroup(pevlis_fk, pevlis_fkGroup)        
         
        jointGroup = generic.getNameStyle ([self.side, self.type, '{}_{}'.format (self.input._joint, self.input._group)])
        jointGroup = generic.createGroup(None, jointGroup)
 
        pevlis_ikGgroup.setParent (jointGroup)
        pevlis_fkGroup.setParent (jointGroup)
        pevlis_dkGroup.setParent (jointGroup)
         
        ikJoints = [pevlis_ik, knee_ik, ankle_ik]
        fkJoints = [pevlis_fk, knee_fk, ankle_fk]
        dkJoints = [pevlis_dk, knee_dk, ankle_dk]        
        types = [self.startType, self.middleType, self.endType]                   
         
        #IK FK Blending
        jointGroup.addAttr(self.input._ikfkBlend,  at='double', min=0, max=1, dv=0, k=1) 
         
        for index in range (len(ikJoints)):     
                     
            for attrIndex in range(len(self.attributes)):                 
                blendColor = generic.getNameStyle ([self.side, types[index], '{}_{}'.format (self.attributes[attrIndex], self.input._blendColor)])
                 
                if pymel.objExists (blendColor):
                    pymel.delete(blendColor)  
                                  
                blendColor = pymel.shadingNode('blendColors',  asUtility=1, n=blendColor)
                 
                currentAttribute = self.attributes[attrIndex].lower()
                ikJoints[index].connectAttr(currentAttribute, '{}.color2'.format(blendColor))
                fkJoints[index].connectAttr(currentAttribute, '{}.color1'.format(blendColor))
                blendColor.connectAttr('output', '{}.{}'.format(dkJoints[index], currentAttribute))
                jointGroup.connectAttr(self.input._ikfkBlend, '{}.blender'.format(blendColor))
                
        #Create control group         
        controlGroup = generic.getNameStyle ([self.side, self.type, '{}_{}'.format (self.input._control, self.input._group)])             
        ikControlGroup = generic.getNameStyle ([self.side, self.type, '{}_{}_{}'.format (self.input._ik, self.input._control, self.input._group)])
        fkControlGroup = generic.getNameStyle ([self.side, self.type, '{}_{}_{}'.format (self.input._fk, self.input._control, self.input._group)])  
                
        controlGroup = generic.createGroup(None, controlGroup)             
        ikControlGroup = generic.createGroup(None, ikControlGroup)
        fkControlGroup = generic.createGroup(None, fkControlGroup)    
            
        ikControlGroup.setParent(controlGroup)
        fkControlGroup.setParent(controlGroup)

        #FK Controls        
        fkControls = []
        for index in range (len(fkJoints)):
             
            #fkControlName = generic.getNameStyle([self.side, types[index], self.input._control])
            nullFk, shapeFk, offsetFk, groupFk = self.control.create(type='Circle', name='{}_{}'.format(types[index], self.input._fk), side=self.side, radius=self.radius, orientation=[0,0,0], positionNode=fkJoints[index])    
             
            if index>0:                
                generic.snap(groupFk, fkControls[index-1][0])
                constraint = generic.getNameStyle([self.side, types[index], '{}_{}_{}_{}'.format(self.input._fk, self.input._control, self.input._group, self.input._parentConstraint)])    
                 
                pymel.parentConstraint(fkControls[index-1][0], groupFk, w=1, n=constraint)
             
            pymel.parentConstraint(shapeFk, fkJoints[index], w=1)            
            fkControls.append([nullFk, shapeFk, offsetFk, groupFk])            
            groupFk.setParent(fkControlGroup)                     
             
        #IK Controls
        ikHandle = generic.getNameStyle([self.side, types[index], self.input._ikHandle])
         
        if pymel.objExists(ikHandle):
            pymel.delete (ikHandle)      
                    
        ikHandle = pymel.ikHandle(n=ikHandle, sj=pevlis_ik, ee=ankle_ik, sol='ikRPsolver', s='sticky')
        ikEffector = generic.getNameStyle([self.side, types[index], self.input._effector])          
        ikHandle[1].rename(ikEffector)
         
        ikHandleGroup = generic.getNameStyle ([self.side, types[index], '{}_{}'.format(self.input._ikHandle, self.input._group)])
         
        if pymel.objExists(ikHandleGroup):
            pymel.delete (ikHandleGroup)          
         
        ikHandleGroup = generic.createGroup(ikHandle[0], ikHandleGroup)
        ikHandle[0].setParent(ikHandleGroup)
        ikHandleGroup.setParent(jointGroup)
         
        #IK Ankle Control        
        nullAnkleIK, shapeAnkleIK, offsetAnkleIK, groupAnkleIK = self.control.create(type='Cube', name='{}_{}'.format(self.endType, self.input._ik), side=self.side, radius=self.radius/1.5, orientation=[0,0,0], positionNode=ikHandleGroup)    
        constraint = generic.getNameStyle ([self.side, types[index], '{}_{}_{}'.format(self.input._ikHandle, self.input._group, self.input._parentConstraint)])
        pymel.parentConstraint(nullAnkleIK, ikHandleGroup, w=1, n=constraint)                
         
        #IK Knee Control       
        nullKneeIk, shapeKneeIk, offsetKneeIk, groupKneeIk = self.control.create(type='Arrow', name='{}_{}'.format(self.poleVectorType, self.input._ik), side=self.side, radius=self.radius/1.5, orientation=[0,0,0], positionNode=self.poleVector)    
        constraint = generic.getNameStyle ([self.side, self.poleVectorType, '{}_{}_{}'.format(self.input._ikHandle, self.input._group, self.input._poleVectorConstraint)])
        pymel.poleVectorConstraint (nullKneeIk, ikHandle[0], w=1, n=constraint)
        
        #IK Pelvis Control        
        nullPelvisIK, shapePelvisIK, offsetPelvisIK, groupPelvisIK = self.control.create(type='LongCube', name='{}_{}'.format(self.startType, self.input._ik), side=self.side, radius=self.radius/1.5, orientation=[0,0,-90], positionNode=pevlis_ik)    
        constraint = generic.getNameStyle ([self.side, self.startType, '{}_{}_{}'.format(self.input._ikHandle, self.input._group, self.input._poleVectorConstraint)])
        pymel.parentConstraint (nullPelvisIK, pevlis_ik, w=1, n=constraint) 

        groupAnkleIK.setParent (ikControlGroup)
        groupKneeIk.setParent (ikControlGroup)
        groupPelvisIK.setParent (ikControlGroup)
         
        #Visibility Connection
        reverse = generic.getNameStyle ([self.side, self.type, '{}_{}'.format(self.input._blend, self.input._reverse)])        
        reverse = pymel.shadingNode ('reverse',  asUtility=1, n=reverse)        
        jointGroup.connectAttr(self.input._ikfkBlend, '{}.inputX'.format(reverse))
        jointGroup.connectAttr(self.input._ikfkBlend, '{}.visibility'.format(fkControlGroup))
        reverse.connectAttr('outputX', '{}.visibility'.format(ikControlGroup))        
        
        #Ik Strech        
        from package import createIKStrech
        #reload(createIKStrech)
        strechGroup = createIKStrech.ikStrech(self.side, self.type, ikJoints, ikHandle[0], nullKneeIk, 'translateX', 1)
        
        #Connection to control
        shapeAnkleIK.addAttr('switchStretch', at='double', min=0, max=1, dv=0, k=1)
        shapeAnkleIK.addAttr('lengthStrech', at='double', min=1, max=100, dv=10, k=1)
        shapeAnkleIK.addAttr('upperStretch', at='double', min=-50, max=50, dv=0, k=1)
        shapeAnkleIK.addAttr('lowerStretch', at='double', min=0, max=1, dv=0, k=1)
        shapeAnkleIK.addAttr('stretch', at='double', min=-180, max=180, dv=0, k=1)
        shapeKneeIk.addAttr('kneeLock', at='double', min=0, max=1, dv=0, k=1)
        
        shapeAnkleIK.connectAttr('switchStretch', '{}.switchStretch'.format(strechGroup), f=True)
        shapeAnkleIK.connectAttr('lengthStrech', '{}.lengthStrech'.format(strechGroup), f=True)
        shapeAnkleIK.connectAttr('upperStretch', '{}.upperStretch'.format(strechGroup), f=True)
        shapeAnkleIK.connectAttr('lowerStretch', '{}.lowerStretch'.format(strechGroup), f=True)
        shapeAnkleIK.connectAttr('stretch', '{}.stretch'.format(strechGroup), f=True)
        shapeKneeIk.connectAttr('kneeLock', '{}.kneeLock'.format(strechGroup), f=True)
      
        #Twist setup         
          
        pymel.undoInfo(closeChunk=1)         
        

    def remove(self):
        pass
    
    
    def hasValid(self):
        pass
    
    
    def rebuild(self):
        pass
    