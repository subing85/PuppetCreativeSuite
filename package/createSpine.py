'''
Foot for Puppet Creative Suite v1.0.0
Date : May 03, 2018
Last modified: May 03, 2018
Author: Subin. Gopi (subing85@gmail.com)

# Copyright (c) 2018, Subin Gopi
# All rights reserved.

# WARNING! All changes made in this file will be lost!

Description
    Module for create spine setup
 
example   
from package import createFinger
spine = createSpine.Spine( side=self.input._leftSide, type=self.input._armFinger, wrist=leftWrist[0], radius=radius) 
'''

from module import openGeneric
from module import inputNames
from module import openControls

reload(openGeneric)
reload(inputNames)
reload(openControls)

from pymel import core as pymel

class Spine(object):
    
    def __init__(self, **kwargs):
        
        '''
        Description
            Function for create the limb for Puppet Creative Suite                    
            :Type - class function (method)            
            :param     side    <str>    example 'L'
            :param     type    <str>    example 'Leg'            
            :param     cog   <str>    example 'cog'
            :param     cog   <str>    example 'cog'
            :param     spine1   <str>    example 'Spine1'
            :param     spine2   <str>    example 'Spine2'
            :param     chest   <str>    example 'Chest'
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
            
        if 'cog' in kwargs:
            self.cog = kwargs['cog'] 
             
        if 'spine' in kwargs:
            self.spine = kwargs['spine']
            
        if 'chest' in kwargs:
            self.chest = kwargs['chest']            
            
        if 'hip' in kwargs:
            self.hip = kwargs['hip']  
                                                           
        if 'radius' in kwargs:
            self.radius = kwargs['radius']  
                    
        self.attributes = ['Translate', 'Rotate', 'Scale'] 
        
        
    def create(self):
        
        pymel.undoInfo(openChunk=1) 
        
        generic = openGeneric.Generic()        
        
        jointGroup = generic.getNameStyle ([self.side, self.type, '{}_{}'.format (self.input._joint, self.input._group)])
        jointGroup = generic.createGroup(None, jointGroup)
        
        controlGroup = generic.getNameStyle ([self.side, self.type, '{}_{}'.format (self.input._control, self.input._group)])
        controlGroup = generic.createGroup(None, controlGroup)        

        #Create deformer joint  
        cog_dk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._cog), self.input._dk])       
        spine_dk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._spine), self.input._dk])         
        chest_dk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._chest), self.input._dk])         
        
        cog_dk = generic.createJoint (radius=0.1, name=cog_dk, position=self.cog)         
        spine_dk = generic.createJoint (radius=0.1, name=spine_dk, position=self.spine)            
        chest_dk = generic.createJoint (radius=0.1, name=chest_dk, position=self.chest)
        
        #Create FK joint 
        cog_fk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._cog), self.input._fk])       
        spine_fk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._spine), self.input._fk])         
        chest_fk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._chest), self.input._fk])            
          
        cog_fk = generic.createJoint (radius=0.1, name=cog_fk, position=self.cog)         
        spine_fk = generic.createJoint (radius=0.1, name=spine_fk, position=self.spine)            
        chest_fk = generic.createJoint (radius=0.1, name=chest_fk, position=self.chest)                  

        #Create IK joint         
        cog_ik = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._cog), self.input._ik])       
        spine_ik = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._spine), self.input._ik])         
        chest_ik = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._chest), self.input._ik])            
          
        cog_ik = generic.createJoint (radius=0.1, name=cog_ik, position=self.cog)         
        spine_ik = generic.createJoint (radius=0.1, name=spine_ik, position=self.spine)            
        chest_ik = generic.createJoint (radius=0.1, name=chest_ik, position=self.chest)                     
        
        generic.setParents ([cog_dk, spine_dk, chest_dk])
        generic.setParents ([cog_fk, spine_fk, chest_fk])
        generic.setParents ([cog_ik, spine_ik, chest_ik])
         
        spine_dkGroup = generic.getNameStyle ([self.side, self.type, '{}_{}_{}'.format (self.input._dk, self.input._joint, self.input._group)])
        spine_ikGgroup = generic.getNameStyle ([self.side, self.type, '{}_{}_{}'.format (self.input._ik, self.input._joint, self.input._group)])
        spine_fkGroup = generic.getNameStyle ([self.side, self.type, '{}_{}_{}'.format (self.input._fk, self.input._joint, self.input._group)])
         
        spine_dkGroup = generic.createGroup(cog_dk, spine_dkGroup)
        spine_ikGgroup = generic.createGroup(cog_ik, spine_ikGgroup)
        spine_fkGroup = generic.createGroup(cog_fk, spine_fkGroup)    
            
        spine_dkGroup.setParent (jointGroup)
        spine_ikGgroup.setParent (jointGroup)
        spine_fkGroup.setParent (jointGroup)
        
        ikJoints = [cog_ik, spine_ik, chest_ik]
        fkJoints = [cog_fk, spine_fk, chest_fk]
        dkJoints = [cog_dk, spine_dk, chest_dk]        
        
        types = [self.input._cog, self.input._spineMid, self.input._chest]                   
         
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
             
            nullFk, shapeFk, offsetFk, groupFk = self.control.create(type='Circle', 
                                                                     name='{}_{}_{}'.format(self.type, types[index], self.input._fk), 
                                                                     side=self.side, 
                                                                     radius=self.radius, 
                                                                     orientation=[0,0,90], 
                                                                     positionNode=fkJoints[index])    
             
            if index>0:                
                generic.snap(groupFk, fkControls[index-1][0])
                constraint = generic.getNameStyle([self.side, '{}_{}'.format(self.type, types[index]), '{}_{}_{}_{}'.format(self.input._fk, self.input._control, self.input._group, self.input._parentConstraint)])    
                  
                pymel.parentConstraint(fkControls[index-1][0], groupFk, w=1, n=constraint)
            
            constraint = generic.getNameStyle([self.side, '{}_{}'.format(self.type, types[index]), '{}_{}'.format(self.input._fk, self.input._parentConstraint)])  
            pymel.parentConstraint(shapeFk, fkJoints[index], w=1, n=constraint)            
            fkControls.append([nullFk, shapeFk, offsetFk, groupFk])            
            groupFk.setParent(fkControlGroup)  

        #IK setup        
        cog_xyz = pymel.xform(self.cog, q=1, a=1, ws=1, t=1)
        spine_xyz = pymel.xform(self.spine, q=1, a=1, ws=1, t=1)
        chest_xyz = pymel.xform(self.chest, q=1, a=1, ws=1, t=1)
        
        ikCurve = generic.getNameStyle([self.side, types[index], '{}_{}'.format(self.input._ikHandle, self.input._curve)])         
        if pymel.objExists(ikCurve):
            pymel.delete (ikCurve)           

        ikCurve = pymel.curve(  d=3, 
                                p=[(cog_xyz[0], cog_xyz[1], cog_xyz[2]), 
                                   (cog_xyz[0], cog_xyz[1], cog_xyz[2]),
                                   (spine_xyz[0], spine_xyz[1], spine_xyz[2]), 
                                   (chest_xyz[0], chest_xyz[1], chest_xyz[2]),
                                   (chest_xyz[0], chest_xyz[1], chest_xyz[2])], 
                                k=[0,0,0,1,2,2,2],
                                n=ikCurve)

        #pymel.rebuildCurve(ikCurve, ch=0,  rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=2, d=3, tol=0.01)

        ikHandle = generic.getNameStyle([self.side, types[index], self.input._ikHandle])         
        if pymel.objExists(ikHandle):
            pymel.delete (ikHandle)      
                    
        ikHandle = pymel.ikHandle(n=ikHandle, sj=cog_ik, ee=chest_ik, c=ikCurve,  sol='ikSplineSolver', ccv=0, pcv=0)
        ikEffector = generic.getNameStyle([self.side, types[index], self.input._effector])          
        ikHandle[1].rename(ikEffector)
        
        ikHandleGroup = generic.getNameStyle ([self.side, types[index], '{}_{}'.format(self.input._ikHandle, self.input._group)])         
        if pymel.objExists(ikHandleGroup):
            pymel.delete (ikHandleGroup)   
              
        ikHandleGroup = generic.createGroup(None, ikHandleGroup)
        ikHandleGroup.setParent(jointGroup)  
              
        ikHandle[0].setParent(ikHandleGroup)
        ikCurve.setParent(ikHandleGroup)        
                    
        #IK Follow locator
        cog_ikLocator = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._cog), '{}_{}'.format(self.input._ik, self.input._locator)])       
        spine_ikLocator = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._spine), '{}_{}'.format(self.input._ik, self.input._locator)])     
        chest_ikLocator = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._chest), '{}_{}'.format(self.input._ik, self.input._locator)])    
         
        for eachLocator in [cog_ikLocator, spine_ikLocator, chest_ikLocator]:
            if pymel.objExists(eachLocator):
                pymel.delete (eachLocator)  
                     
        cog_ikLocator = pymel.spaceLocator(p=(0, 0, 0), n=cog_ikLocator)
        spine_ikLocator = pymel.spaceLocator(p=(0, 0, 0), n=spine_ikLocator)
        chest_ikLocator = pymel.spaceLocator(p=(0, 0, 0), n=chest_ikLocator)

        generic.snapTranslate(self.cog, cog_ikLocator)
        generic.snapTranslate(self.spine, spine_ikLocator)
        generic.snapTranslate(self.chest, chest_ikLocator)
        
        ikLocatorGroup = generic.getNameStyle ([self.side, self.type, '{}_{}_{}'.format(self.input._ikHandle, self.input._locator, self.input._group)])         
        if pymel.objExists(ikLocatorGroup):
            pymel.delete (ikLocatorGroup)           
        
        ikLocatorGroup = generic.createGroup(None, ikLocatorGroup)
        ikLocatorGroup.setParent(jointGroup)     
        
        cog_ikLocator.setParent(ikLocatorGroup)        
        spine_ikLocator.setParent(ikLocatorGroup)        
        chest_ikLocator.setParent(ikLocatorGroup)        
        
        #ikLocatorGroup.setAttr ('visibility', 0, l=True)
        
        #IK Controls 
        nullCogIk, shapeCogIk, offsetCogIk, groupCogIk = self.control.create(   type='CubeIK', 
                                                                                name='{}_{}_{}'.format(self.type, types[0], self.input._ik), 
                                                                                side=self.side, 
                                                                                radius=self.radius, 
                                                                                orientation=[0,0,0], 
                                                                                positionNode=cog_ikLocator)   
        
        nullSpineIk, shapeSpineIk, offsetSpineIk, groupSpineIk = self.control.create(   type='CubeIK', 
                                                                                        name='{}_{}_{}'.format(self.type, types[1], self.input._ik), 
                                                                                        side=self.side, 
                                                                                        radius=self.radius, 
                                                                                        orientation=[0,0,0], 
                                                                                        positionNode=spine_ikLocator)   
                                                                                        

        nullChestIk, shapeChestIk, offsetChestIk, groupChestIk = self.control.create(   type='CubeIK', 
                                                                                        name='{}_{}_{}'.format(self.type, types[2], self.input._ik), 
                                                                                        side=self.side, 
                                                                                        radius=self.radius, 
                                                                                        orientation=[0,0,0], 
                                                                                        positionNode=chest_ikLocator) 
                                   
        constraint = generic.getNameStyle([self.side, '{}_{}'.format(self.type, self.input._cog), '{}_{}_{}'.format(self.input._ik, self.input._locator, self.input._parentConstraint)])
        pymel.parentConstraint(nullCogIk, cog_ikLocator, w=1, n=constraint) 
        
        constraint = generic.getNameStyle([self.side, '{}_{}'.format(self.type, self.input._spine), '{}_{}_{}'.format(self.input._ik, self.input._locator, self.input._parentConstraint)])
        pymel.parentConstraint(nullSpineIk, spine_ikLocator, w=1, n=constraint) 
        
        constraint = generic.getNameStyle([self.side, '{}_{}'.format(self.type, self.input._chest), '{}_{}_{}'.format(self.input._ik, self.input._locator, self.input._parentConstraint)])
        pymel.parentConstraint(nullChestIk, chest_ikLocator, w=1, n=constraint)                  
        
        ikCurveShape = ikCurve.getShape()        
        
        cog_ikLocator.connectAttr('translate', '{}.controlPoints[0]'.format(ikCurveShape))
        cog_ikLocator.connectAttr('translate', '{}.controlPoints[1]'.format(ikCurveShape))        
        spine_ikLocator.connectAttr('translate', '{}.controlPoints[2]'.format(ikCurveShape))        
        chest_ikLocator.connectAttr('translate', '{}.controlPoints[3]'.format(ikCurveShape))
        chest_ikLocator.connectAttr('translate', '{}.controlPoints[4]'.format(ikCurveShape))
        
        
        #IK Stretch
      
        #hipJoint = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._hip), self.input._joint])         
        #hipJoint = generic.createJoint (radius=0.1, name=hipJoint, position=self.hip)   
                
        
        pymel.select(cl=True)                   
        pymel.undoInfo(closeChunk=1)         
#End############################################################################################################################################