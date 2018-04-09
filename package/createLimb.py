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
                        
        self.attributes = ['Translate', 'Rotate', 'Scale']   


    def create(self):
        
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
        
        pevlis_dkGroup = generic.getNameStyle ([self.side, self.startType, '{}_{}'.format (self.input._dk, self.input._group)])
        pevlis_ikGgroup = generic.getNameStyle ([self.side, self.startType, '{}_{}'.format (self.input._ik, self.input._group)])
        pevlis_fkGroup = generic.getNameStyle ([self.side, self.startType, '{}_{}'.format (self.input._fk, self.input._group)])
        
        pevlis_dkGroup = generic.createGroup(pevlis_dk, pevlis_dkGroup)
        pevlis_ikGgroup = generic.createGroup(pevlis_fk, pevlis_ikGgroup)
        pevlis_fkGroup = generic.createGroup(pevlis_ik, pevlis_fkGroup)        
        
        controlGroup = generic.getNameStyle ([self.side, self.type, '{}_{}'.format (self.input._control, self.input._group)])
        jointGroup = generic.getNameStyle ([self.side, self.type, '{}_{}'.format (self.input._joint, self.input._group)])     

        controlGroup = generic.createGroup(None, controlGroup)
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
        
        #=======================================================================
        # #Visibility Connection
        # reverse = generic.getNameStyle ([self.side, self.type, '{}_{}'.format(self.input._blend, self.input._reverse)])        
        # reverse = pymel.shadingNode ('reverse',  asUtility=1, n=reverse)        
        # jointGroup.connectAttr(self.input._ikfkBlend, '{}.inputX'.format(reverse))
        # jointGroup.connectAttr(self.input._ikfkBlend, '{}.visibility'.format(pevlis_fkGroup))
        # reverse.connectAttr('outputX', '{}.visibility'.format(pevlis_ikGgroup))
        #======================================================================= 
        
        for index in range (len(ikJoints)):     
                    
            for attrIndex in range (len(self.attributes)):                 
                blendColor = generic.getNameStyle ([self.side, types[index], '{}_{}'.format (self.attributes[attrIndex], self.input._blendColor)])
                
                if pymel.objExists (blendColor):
                    pymel.delete(blendColor)  
                                 
                blendColor = pymel.shadingNode ('blendColors',  asUtility=1, n=blendColor)
                
                currentAttribute = self.attributes[attrIndex].lower()
                ikJoints[index].connectAttr(currentAttribute, '{}.color2'.format(blendColor))
                fkJoints[index].connectAttr(currentAttribute, '{}.color1'.format(blendColor))
                blendColor.connectAttr('output', '{}.{}'.format(dkJoints[index], currentAttribute))
                jointGroup.connectAttr(self.input._ikfkBlend, '{}.blender'.format(blendColor))
                
        
        #FK Controls        
        fkControls = []
        for index in range (len(fkJoints)):
            
            fkControlName = generic.getNameStyle ([self.side, types[index], self.input._control])
            null, shape, offset, group = self.control.create(type='Circle', name=fkControlName, side=self.side, radius=1, orientation=[0,0,0], positionNode=fkJoints[index])    
            
            if index>0:                
                generic.snap(group, fkControls[index-1][0])              
                pymel.parentConstraint(fkControls[index-1][0], group, w=1)
            
            pymel.parentConstraint(shape, fkJoints[index], w=1)            
            fkControls.append([null, shape, offset, group])
            
            
        #IK Controls
        
        
            
            
                    
    
            #[nullGroup, currentControl, offsetGroup, group]
    def remove(self):
        pass
    
    
    def hasValid(self):
        pass
    
    
    def rebuild(self):
        pass
    