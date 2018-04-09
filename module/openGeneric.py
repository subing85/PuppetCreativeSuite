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

reload(inputNames)


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

        self.input = inputNames.Names() 
        
    
    def getNameStyle (self, components):
        
        '''
        Description
            Function for manipulate the maya node name how to order the first, middle and end name                     
            :Type - class function (method)            
            :param   components    <list>    [first, middle, end]
            :return result    <str>   ' first_middle_end'
        '''  
                
        result = None        
        if not components :  
            warnings.warn ('nodeNameStyle argument called \"components\" None or empty')  
            return None
        
        values = self.input._nameStyle                
        result = '{}_{}_{}'.format (components[values[0]], components[values[1]], components[values[2]])
        return result
    
    
    def jointHasValid (self, joint):
        
        joint = pymel.PyNode (joint)    

        if joint.type() != 'joint' :                
            return False
        
        side = joint.getAttr('side')
        type = joint.getAttr('type')
        otherType = joint.getAttr('otherType')               

        if side==3:
            return False
        
        if type!=18:
            return False
        
        if not otherType:
            return False

        return True
        
    
    def jointLabelVisibility (self, value):
        pymel.undoInfo(openChunk=1)       
        
        joints = pymel.ls(type='joint') 
        
        for eachJoint in joints:    
                    
            if not self.jointHasValid (eachJoint):
                continue            
            eachJoint.setAttr('drawLabel', value)
            
        pymel.select(cl=1)            
        print 'jointLabelVisibility\t', value        
        pymel.undoInfo(closeChunk=1)
        
    
    def splitJoints (self, currentJoints, jointCount):
        
        '''
        Description
            Function for create Joint based on kwargs inputs                        
            :Type - class function (method)            
            :param   currentJoints    <list>    ['L_Pelvis', 'L_Knee']
            :param   jointCount    <int>    4
            :param   position   <tuple>    (0, 0, 0)
            :param   name    <str>    example 'Puppet_Joint'
            :param   dependency    <bool>    False
            :return currentJoint    <pymelObject>    'Puppet_Joint'
        '''          
        

        pymel.undoInfo(openChunk=1)
        
        if not currentJoints :
            warnings.warn ('splitJoints\tcurrentJoints argument none or empty')
            return None
        
        jointCount = jointCount + 1
        
        for eachJoint in currentJoints :            

            if not self.jointHasValid (eachJoint):
                continue
            
            jointRadius = eachJoint.getAttr('radius')            
            childJoints = eachJoint.getChildren()
            #x, y, z = eachJoint.getAttr('jointOrient')
            
            if not childJoints:
                continue
            
            #start_xyz = eachJoint.getTranslation (p=True)
            #end_xyz = childJoints[0].getTranslation (p=True)            
            start_xyz = pymel.xform (eachJoint, q=1, a=1, ws=1, t=1)
            end_xyz = pymel.xform (childJoints[0], q=1, a=1, ws=1, t=1)  
            
            jointVectorX = (end_xyz[0]- start_xyz[0])/jointCount
            jointVectorY = (end_xyz[1]- start_xyz[1])/jointCount
            jointVectorZ = (end_xyz[2]- start_xyz[2])/jointCount           
            
            #pymel.select (eachJoint, r=1)
            splitJoints = [eachJoint]
            for jntLoop in range (1, jointCount, 1) :
                midPointX = start_xyz[0] + (jntLoop*jointVectorX)
                midPointY = start_xyz[1] + (jntLoop*jointVectorY)
                midPointZ = start_xyz[2] + (jntLoop*jointVectorZ)
                
                pymel.select (cl=True)
                twistJoint = pymel.joint (rad=jointRadius, o=(0,0,0), p=(midPointX, midPointY, midPointZ), n='{}_{}'.format (eachJoint, jntLoop))                         
                twistJoint.setParent (splitJoints[-1])                 
                twistJoint.setAttr('jointOrient', 0, 0, 0)      
                twistJoint.setAttr('rotate', 0, 0, 0)                                
                splitJoints.append (twistJoint)
               
            childJoints[0].setParent (splitJoints[-1])              
                   
        pymel.undoInfo(closeChunk=1)
        
        
    def setJointRadius (self, value):
        pymel.undoInfo(openChunk=1)
        
        joints = pymel.ls(type='joint')        
        if not joints :
            warnings.warn ('Joints are not exists in the scene.')
            
        pymel.select(cl=True) 
        pymel.jointDisplayScale (1.0, a=True) 
          
        for eachJoint in joints :
            eachJoint.setAttr('radius', value)
            
        pymel.undoInfo(closeChunk=1)
        
    
    def getJointFromLabel(self, side, lable):
        
        joints = pymel.ls(type='joint')        
        if not joints :
            warnings.warn ('Joints are not exists in the scene.')
            
        labelJoint = []
        
        for eachJoint in joints :
            if not self.jointHasValid (eachJoint):
                continue
            
            currentSide = eachJoint.getAttr('side')            
            currentLabel = eachJoint.getAttr('otherType')
            
            if currentSide!=side:
                continue
            
            if currentLabel!=lable:
                continue
                        
            labelJoint.append(eachJoint)
            
        if len(labelJoint)>1:
            warnings.warn ('more than one joint exists as a same label.')            
            return None
            
        return labelJoint


    def createJoint(self, radius=None, name=None, position=None): 
        
        #pymel.undoInfo(openChunk=1) 
               
        pymel.select (cl=True)
                    
        if pymel.objExists(name):
            pymel.delete (pymel.ls(name))  
                      
        currentJoint = pymel.joint(rad=radius, o=(0,0,0), p=(0,0,0), n=name)        
        self.snap(position, currentJoint)        
        pymel.makeIdentity(currentJoint, a=1, t=0, r=1, s=0, n=0)        
        #pymel.undoInfo(closeChunk=1)         
        return currentJoint 
        

    def snap(self, source, target):   
        
        try:           
            constraint = pymel.parentConstraint(source, target, w=1)
            pymel.delete(constraint)    
        except Exception as result:
            print result
            
            
    def setParents(self, nodes):        
        
        for index in range (len(nodes)):            
            
            if index>len(nodes)-2:
                continue
                
            child = pymel.PyNode(nodes[index+1])
            parent = pymel.PyNode(nodes[index])
            child.setParent(parent)
            
            
    def createGroup(self, node, group):
        
        if pymel.objExists(group):
            pymel.delete (pymel.ls(group))  
        
        group = pymel.group (em=1, n=group)
        
        if not node:
            return group
        
        self.snap (node, group)        
        node.setParent(group)
        
        return group
        
        
            
            
            



        

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