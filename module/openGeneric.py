'''
Open Generic for Puppet CS v1.0.0
Date : March 29, 2018
Last modified: March 29, 2018
Author: Subin. Gopi (subing85@gmail.com)

# Copyright (c) 2018, Subin Gopi
# All rights reserved.

# WARNING! All changes made in this file will be lost!

Description
    This module includes generic function for maya
 
'''
import warnings

from pymel import core as pymel

from module import inputNames


class Generic (object):
    
    '''
    Description            
        Function includes generic create edit and quarry for maya scene
        
        :Type - standalone function        
        :param    None        
        :return   None
        
        :example to execute        

            import buildPuppet    
            buildPuppet.runMayaUiDemo ()        
    ''' 
    
    def __init__(self):
        pass
    
    
    def nodeNameStyle (self, components, values=(0, 1, 2)):
        
        '''
        Description
            Function for manipulate the maya node name how to order the first, middle and end name                     
            :Type - class function (method)            
            :param   components    <list>    [first, middle, end]
            :param   values    <tuple>    (0, 1, 2)
            :return result    <str>   ' first_middle_end'
        '''  
                
        result = None        
        if not components :  
            warnings.warn ('nodeNameStyle argument called \"components\" None or empty')  
            return None
                
        result = '{}_{}_{}'.format (components[values[0]], components[values[1]], components[values[2]])
        return result
    
    
    def createJoint(self, **kwargs):
        
        '''
        Description
            Function for create Joint based on kwargs inputs                        
            :Type - class function (method)            
            :param   radius    <float>    example 1.0
            :param   orientation    <tuple>    (0, 0, 0)
            :param   position   <tuple>    (0, 0, 0)
            :param   name    <str>    example 'Puppet_Joint'
            :param   dependency    <bool>    False
            :return currentJoint    <pymelObject>    'Puppet_Joint'
        '''  
        
        radius = 1.0
        if 'radius' in kwargs:
            radius = kwargs['radius']            
            
        orientation = (0, 0, 0)
        if 'orientation' in kwargs:
            orientation = kwargs['orientation']            
        
        position =  (0, 0, 0)
        if 'position' in kwargs:
            position = kwargs['position']        

        name = 'Puppet_Joint'
        if 'name' in kwargs:
            name = kwargs['name']
            
        dependency = False
        if 'dependency' in kwargs:
            dependency = kwargs['dependency'] 
            
        currentJoint = makeJoint (radius=radius, orientation=orientation, position=position, name=name, dependency=dependency) 
        
        return currentJoint
    
    
    
        
           
        
                 
                
    

def makeJoint(radius=None, orientation=None, position=None, name=None, dependency=None):
    
    '''
    Description
        Standalone Function for create Joint based on kwargs inputs                        
        :Type - class function (method)            
        :param   radius    <float>    example 1.0
        :param   orientation    <tuple>    (0, 0, 0)
        :param   position   <tuple>    (0, 0, 0)
        :param   name    <str>    example 'Puppet_Joint'
        :param   dependency    <bool>    False
        :return currentJoint    <pymelObject>    'Puppet_Joint'
    '''      
    
    if not dependency:
        pymel.select (cl=True)
        
    if pymel.objExists(name):
        pymel.delete (pymel.ls(name))
        
    currentJoint = pymel.joint(rad=radius, o=orientation, p=position, n=name)

    return currentJoint
        
        

'''

def setJointLabel (joint, label, side, switch):
    cmds.setAttr (joint + '.side', side)
    cmds.setAttr (joint + '.type', 18)
    cmds.setAttr (joint + '.otherType', label, type='string')
    cmds.setAttr (joint + '.drawLabel', switch)
    
    
def lockHideAttributes (node, type, attributes):
    for attribute in attributes :
        if type=='lock' :
            cmds.setAttr (node + '.' + attribute, lock=1)
        if type=='hide' :
            cmds.setAttr (node + '.' + attribute, keyable=0, channelBox=0)
        if type=='nonkeyable' :
            cmds.setAttr (node + '.' + attribute, keyable=0, channelBox=1)
        if type=='lockHide' :
            cmds.setAttr (node + '.' + attribute,lock=1, keyable=0, channelBox=0)
  
  
hierarchyAppend    = []      
def hierarchyList (root) :
    if root :
        child           = cmds.listRelatives (root, c=1)       
        if child :         
            for eachChild in child :
                hierarchyAppend.append (eachChild)
                hierarchyList (eachChild)
    return (hierarchyAppend)

def createJoint (joints, jointNames, side, type) :
    cmds.select (cl=1)    
    collectJoints               = []
    for jointLoop in range (0, len(joints), 1) :
        jointRotateOrder        = cmds.getAttr (joints[jointLoop] + '.rotateOrder')           
        preferredAngleX         = cmds.getAttr (joints[jointLoop] + '.preferredAngleX')
        preferredAngleY         = cmds.getAttr (joints[jointLoop] + '.preferredAngleY')
        preferredAngleZ         = cmds.getAttr (joints[jointLoop] + '.preferredAngleZ')
        newJoint                = cmds.joint (rad=gv.jntRadius, n=side + '_' + jointNames[jointLoop] + '_' + type + '_' + gv.joint)
        cmds.setAttr (newJoint + '.rotateOrder', jointRotateOrder)
        cmds.setAttr (newJoint + '.preferredAngleX', preferredAngleX)
        cmds.setAttr (newJoint + '.preferredAngleY', preferredAngleY)
        cmds.setAttr (newJoint + '.preferredAngleZ', preferredAngleZ)
        snapAction (joints[jointLoop], newJoint)       
        cmds.makeIdentity (newJoint, a=1, t=0, r=1, s=0, n=0)           
        collectJoints.append (newJoint)
    cmds.select (cl=1)       
    return collectJoints

def locatorSacle (locater, scale, lockHide):
    locatorShape        = cmds.listRelatives (locater[0], s=1)       
    cmds.setAttr (locatorShape[0] + '.localScaleX', scale)
    cmds.setAttr (locatorShape[0] + '.localScaleY', scale)
    cmds.setAttr (locatorShape[0] + '.localScaleZ', scale)
    cmds.setAttr (locatorShape[0] + '.visibility', k=1)
    if lockHide==1 :
        cmds.setAttr (locatorShape[0] + '.visibility', 0, l=1)
        
def createDistanceDimension (name, startPoint, endPoint):
    tempUpDistanceDimShape      = cmds.distanceDimension (sp=(0, 0, 0), ep=(0, 1, 0))
    tempUpStarLocator           = cmds.listConnections(tempUpDistanceDimShape + '.startPoint', d=0, s=1)
    tempUpEndLocator            = cmds.listConnections(tempUpDistanceDimShape + '.endPoint', d=0, s=1)
    tempUpDistanceDim           = cmds.listRelatives(tempUpDistanceDimShape, p=1)
    distanceDim                 = cmds.rename (tempUpDistanceDim[0], name + '_' + gv.distanceBetween)
    starLocator                 = cmds.rename (tempUpStarLocator[0], name + '_' + gv.distanceBetween + '_Start_' + gv.locator)
    endLocator                  = cmds.rename (tempUpEndLocator[0],  name + '_' + gv.distanceBetween + '_End_' + gv.locator)
    cmds.pointConstraint (startPoint, starLocator,  o=[0,0,0], w=1, n=starLocator + '_' + gv.pointConstraint)
    cmds.pointConstraint (endPoint, endLocator,  o=[0,0,0], w=1, n=endLocator + '_' + gv.pointConstraint)       
    distanceDimShape            = cmds.listRelatives (distanceDim, s=1)
    cmds.select (cl=1)    
    return [starLocator, endLocator, distanceDim, distanceDimShape[0]]

def listJointSide (joint) :      
    jointSide           = cmds.getAttr (joint + '.side')                            
    side                = ''
    sideName            = ''
    
    if jointSide==0 :
        side            = gv.centerSide
        sideName        = 'center'
    elif jointSide==1 :
        side            = gv.leftSide
        sideName        = 'left'
    elif jointSide==2 :
        side            = gv.rightSide
        sideName        = 'right'
    return [side, sideName]

def padding (shot=0, pShot=0):
    shotSize        = len(str(shot))
    zero            = pShot - shotSize
    zero            = (abs(zero)*"0")
    return zero

def setColorChange (nodes, rgbColor) :           
    if nodes :       
        for eachNode in nodes :
            cmds.setAttr (eachNode + '.overrideEnabled', 1);
            cmds.setAttr (eachNode + '.overrideColor', rgbColor)
            eachNodeShapes  = cmds.listRelatives (eachNode, s=1)
            for eachNodeShape in eachNodeShapes :                             
                cmds.setAttr (eachNodeShape + '.overrideEnabled', 1);
                cmds.setAttr (eachNodeShape + '.overrideColor', rgbColor)

def snapAction(source, target):      
    pointConst      = cmds.pointConstraint(source, target, o=[0, 0, 0], w=1)
    orientConst     = cmds.orientConstraint(source, target, o=[0, 0, 0], w=1)
    cmds.delete(pointConst, orientConst)

def snapInbetween (sourceA, sourceB, target):
    pointConst      = cmds.pointConstraint(sourceA, sourceB, target, o=[0, 0, 0], w=1)
    orientConst     = cmds.orientConstraint(sourceA, sourceB, target, o=[0, 0, 0], w=1)
    cmds.delete(pointConst, orientConst)

def snapInbetweenTranslate (sourceA, sourceB, target):
    pointConst      = cmds.pointConstraint(sourceA, sourceB, target, o=[0, 0, 0], w=1)
    cmds.delete(pointConst)

def snapRotate(source, target):   
    orientConst     = cmds.orientConstraint(source, target, o=[0, 0, 0], w=1)
    cmds.delete(orientConst)

def snapTranslate(source, target):   
    pointConst      = cmds.pointConstraint(source, target, o=[0, 0, 0], w=1)
    cmds.delete(pointConst)
'''