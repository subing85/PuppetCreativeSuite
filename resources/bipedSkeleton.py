'''
Biped Skeleton for Puppet CS v1.0.0
Date : March 29, 2018
Last modified: March 29, 2018
Author: Subin. Gopi (subing85@gmail.com)

# Copyright (c) 2018, Subin Gopi
# All rights reserved.

# WARNING! All changes made in this file will be lost!

Description
    This module for generate Biped Skeleton for Puppet Creative Suite
 
'''

NAME = 'Biped'
ORDER = 1
MODULE_TYPE = 'Fit Skeleton'
TYPE = 'validate'
DATE = 'March 29, 2018'
AUTHOR = 'Subin Gopi'
COMMENTS = 'To Generate Biped Skeleton'
VERSION = 1.0
CLASS = 'Biped'


from pymel import core as pymel

from module import inputNames
from module import openGeneric

reload(inputNames)
reload(openGeneric)


class Biped (object):
    
    def __init__(self):
        
        self.input = inputNames.Names()
        self.generic = openGeneric.Generic()
        
        self.nameStyle = self.input._nameStyle
        self.jointRadius = self.input._jointRadius
        
    
    
    def createSkeleton(self):
        
        '''
        Description
            Function for create the skleton for Bipe puppet, only in left side                     
            :Type - class function (method)            
            :param     None
            :return    None
        '''  
        
        pelvisName = self.generic.nodeNameStyle([self.input._leftSide, self.input._pelvis,  self.input._fitJoint], self.input._nameStyle)         
        leftPelvisJoint = self.generic.createJoint(radius=self.jointRadius, orientation=(180, 0, -90), position=(1, 6.5, 0.0), name=pelvisName, dependency=False)        
        
        kneeName = self.generic.nodeNameStyle([self.input._leftSide, self.input._knee,  self.input._fitJoint], self.input._nameStyle)         
        leftKneeJoint = self.generic.createJoint(radius=self.jointRadius, orientation=(0, 0, 0), position=(1, 3.75, 0.0), name=kneeName, dependency=True)
         
        ankleName = self.generic.nodeNameStyle([self.input._leftSide, self.input._ankle,  self.input._fitJoint], self.input._nameStyle)         
        leftAnkleJoint = self.generic.createJoint(radius=self.jointRadius, orientation=(0, 0, 0), position=(1, 1.0, 0.0), name=ankleName, dependency=True)    
        
        ballName = self.generic.nodeNameStyle([self.input._leftSide, self.input._ball,  self.input._fitJoint], self.input._nameStyle)         
        leftBallJoint = self.generic.createJoint(radius=self.jointRadius, orientation=(0, 63.435, 0), position=(1, 0.5, 1.0), name=ballName, dependency=True)           
     
        toeName = self.generic.nodeNameStyle([self.input._leftSide, self.input._toe,  self.input._fitJoint], self.input._nameStyle)         
        leftToeNameJoint = self.generic.createJoint(radius=self.jointRadius, orientation=(0, 0, 0), position=(1,  0.0, 2.0), name=toeName, dependency=True)           
        
       
        bigToeName = self.generic.nodeNameStyle([self.input._leftSide, self.input._bigToe,  self.input._fitJoint], self.input._nameStyle)         
        leftBigToeJoint = self.generic.createJoint(radius=self.jointRadius, orientation=(0, 0, 0), position=(0.3, 0.0, 1.0), name=bigToeName, dependency=False)    
        
        pinkyToeName = self.generic.nodeNameStyle([self.input._leftSide, self.input._pinkyToe,  self.input._fitJoint], self.input._nameStyle)         
        leftPinkyToeJoint = self.generic.createJoint(radius=self.jointRadius, orientation=(0, 0, 0), position=(1.7, 0.0, 1.0), name=pinkyToeName, dependency=False)                    
        
        heelName = self.generic.nodeNameStyle([self.input._leftSide, self.input._heel,  self.input._fitJoint], self.input._nameStyle)         
        leftHeelJoint = self.generic.createJoint(radius=self.jointRadius, orientation=(0, 0, 0), position=(1, 0.0, -1.0), name=heelName, dependency=False)                 
         
        legPoleName = self.generic.nodeNameStyle([self.input._leftSide, self.input._legPoleVector,  self.input._fitJoint], self.input._nameStyle)         
        leftLegPoleJoint = self.generic.createJoint(radius=self.jointRadius, orientation= (0, 0, 0), position=(1, 3.75, 2.5), name=legPoleName, dependency=False)  
        
        leftBigToeJoint.setParent(leftBallJoint)
        leftPinkyToeJoint.setParent(leftBallJoint)
        leftHeelJoint.setParent(leftAnkleJoint)              
        leftLegPoleJoint.setParent(leftKneeJoint)
        leftKneeJoint.setAttr('preferredAngleY', -1)
        
        


    
    
    def removeSkeleton(self):
        pass
    
    
    def resetSkeleton(self):
        pass
    
    
    def hasExists (self):
        pass


    
'''       
import maya.cmds as cmds
import maya.api.OpenMaya as om

import utils.variables as variables
gv      = variables.VARIABLES ()
import generic as generic

def importBipedSkeleton () :
    cmds.undoInfo(openChunk=1)
    cmds.select (cl=1)

    if cmds.objExists (gv.centerSide + '_' + gv.pelvis + '_' + gv.fitJoint) :
        om.MGlobal.displayWarning ('Biped skeleton already exists.')
        return False
    #Leg
    ctPelvisJnt             = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(0, 6.7, 0), n=gv.centerSide + '_' + gv.pelvis + '_' + gv.fitJoint)
    ltPelvisJnt             = cmds.joint(rad=gv.jntRadius, o= (180, 0, -90), p=(1, 6.5, 0.0), n=gv.leftSide + '_' + gv.pelvis  + '_' + gv.fitJoint)
    ltHipJnt                = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(1, 6.0, 0.0), n=gv.leftSide + '_' + gv.hip  + '_' + gv.fitJoint)
    ltKneeJnt               = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(1, 3.5, 0), n=gv.leftSide + '_' + gv.knee  + '_' + gv.fitJoint)
    ltAnkleJnt              = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(1, 1.0, 0.0), n=gv.leftSide + '_' + gv.ankle  + '_' + gv.fitJoint)
    cmds.setAttr (ltKneeJnt + '.preferredAngleY', -1)
    cmds.select(cl=1)
    ltLegPoleJnt            = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(1, 3.492, 2.5), n=gv.leftSide + '_' + gv.legPoleVector + '_' + gv.fitJoint)
    cmds.parent(ltLegPoleJnt, ltKneeJnt)
    cmds.select(cl=1)

    #Label
    generic.setJointLabel (ctPelvisJnt, gv.pelvis, 0, 1)
    generic.setJointLabel (ltPelvisJnt, gv.pelvis, 1, 1)
    generic.setJointLabel (ltHipJnt, gv.hip, 1, 1)
    generic.setJointLabel (ltKneeJnt, gv.knee, 1, 1)
    generic.setJointLabel (ltAnkleJnt, gv.ankle, 1, 1)
    generic.setJointLabel (ltLegPoleJnt, gv.legPoleVector, 1, 1)

    #Foot
    ltBall                  = cmds.joint(rad=gv.jntRadius, o= (180, -63.435, -90), p=(1, 0.5, 1.0), n=gv.leftSide + '_' + gv.ball  + '_' + gv.fitJoint)
    ltToe                   = cmds.joint(rad=gv.jntRadius, o= (0, 26.565, 0) , p=(1,  0.0, 2.0), n=gv.leftSide + '_' + gv.toe  + '_' + gv.fitJoint)

    cmds.select(cl=1)
    ltBigToe                = cmds.joint(rad=gv.jntRadius, p=(0.3, 0.0, 1.0), n=gv.leftSide + '_' + gv.bigToe + '_' + gv.fitJoint)
    ltPinkyToe              = cmds.joint(rad=gv.jntRadius, p=(1.7, 0.0, 1.0), n=gv.leftSide + '_' + gv.pinkyToe  + '_' + gv.fitJoint)
    ltHeel                  = cmds.joint(rad=gv.jntRadius, p=(1, 0.0, -1.0), n=gv.leftSide + '_' + gv.heel  + '_' + gv.fitJoint)

    cmds.parent (ltBall, ltAnkleJnt)
    cmds.parent (ltBigToe, ltBall)
    cmds.parent (ltPinkyToe, ltBall)
    cmds.parent (ltHeel, ltAnkleJnt)
    cmds.select (cl=1)

    generic.setJointLabel (ltBall, gv.ball, 1, 1)
    generic.setJointLabel (ltToe, gv.toe, 1, 1)
    generic.setJointLabel (ltBigToe, gv.bigToe, 1, 1)
    generic.setJointLabel (ltPinkyToe, gv.pinkyToe, 1, 1)
    generic.setJointLabel (ltHeel, gv.heel, 1, 1)

    cogSkel                 = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(0, 7.0, 0), n=gv.centerSide + '_' + gv.cog + '_' + gv.fitJoint)
    spineASkel              = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(0, 7.8, 0), n=gv.centerSide + '_' + gv.spineA + '_' + gv.fitJoint)
    spineBSkel              = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(0, 8.6, 0), n=gv.centerSide + '_' + gv.spineB + '_' + gv.fitJoint)
    chestSkel               = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(0, 9.4, 0), n=gv.centerSide + '_' + gv.chest + '_' + gv.fitJoint)

    cmds.parent (ctPelvisJnt, cogSkel)
    cmds.select (cl=1)

    generic.setJointLabel (cogSkel, gv.cog, 0, 1)
    generic.setJointLabel (spineASkel, gv.spineA, 0, 1)
    generic.setJointLabel (spineBSkel, gv.spineB, 0, 1)
    generic.setJointLabel (chestSkel, gv.chest, 0, 1)

    ltClavicleJnt           = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(0.15, 10.0, 0), n=gv.leftSide + '_' + gv.clavicle  + '_' + gv.fitJoint)
    ltShoulderJnt           = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(0.83, 10.0, 0), n=gv.leftSide + '_' + gv.shoulder  + '_' + gv.fitJoint)
    ltElbowJnt              = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(2.415, 10.0, 0), n=gv.leftSide + '_' + gv.elbow  + '_' + gv.fitJoint)
    ltwristJnt              = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(4, 10.0, 0), n=gv.leftSide + '_' + gv.wrist  + '_' + gv.fitJoint)
    cmds.setAttr (ltElbowJnt + '.preferredAngleY', -1)

    cmds.select (cl=1)
    ltArmPoleJnt            = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(2.415, 10.0, -1.5), n=gv.leftSide + '_' + gv.armPoleVector  + '_' + gv.fitJoint)

    cmds.parent(ltArmPoleJnt, ltElbowJnt)
    cmds.parent (ltClavicleJnt, chestSkel)
    cmds.select (cl=1)

    generic.setJointLabel (ltClavicleJnt, gv.clavicle, 1, 1)
    generic.setJointLabel (ltShoulderJnt, gv.shoulder, 1, 1)
    generic.setJointLabel (ltElbowJnt, gv.elbow, 1, 1)
    generic.setJointLabel (ltwristJnt, gv.wrist, 1, 1)
    generic.setJointLabel (ltArmPoleJnt, gv.armPoleVector, 1, 1)

    #Arm Finger
    ltThumbRootJnt          = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(4.5, 10.0, 0.3), n=gv.leftSide + '_' + gv.thumbRoot + '_' + gv.fitJoint)
    ltThumbAJnt             = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(4.65, 10.0, 0.3), n=gv.leftSide + '_' + gv.thumbA + '_' + gv.fitJoint)
    ltThumbBJnt             = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(4.85, 10.0, 0.3), n=gv.leftSide + '_' + gv.thumbB + '_' + gv.fitJoint)
    ltThumbCJnt             = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(5.05, 10.0, 0.3), n=gv.leftSide + '_' + gv.thumbC + '_' + gv.fitJoint)
    ltThumbDJnt             = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(5.25, 10.0, 0.3), n=gv.leftSide + '_' + gv.thumbD + '_' + gv.fitJoint)
    cmds.select (cl=1)

    ltIndexRootJnt          = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(4.5, 10.0, 0.15), n=gv.leftSide + '_' + gv.indexRoot + '_' + gv.fitJoint)
    ltIndexAJnt             = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(4.65, 10.0, 0.15), n=gv.leftSide + '_' + gv.indexA + '_' + gv.fitJoint)
    ltIndexBJnt             = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(4.85, 10.0, 0.15), n=gv.leftSide + '_' + gv.indexB + '_' + gv.fitJoint)
    ltIndexCJnt             = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(5.05, 10.0, 0.15), n=gv.leftSide + '_' + gv.indexC + '_' + gv.fitJoint)
    ltIndexDJnt             = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(5.25, 10.0, 0.15), n=gv.leftSide + '_' + gv.indexD + '_' + gv.fitJoint)
    cmds.select (cl=1)

    ltMiddleRootJnt         = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(4.5, 10.0,  -0.0), n=gv.leftSide + '_' + gv.middleRoot + '_' + gv.fitJoint)
    ltMiddleAJnt            = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(4.65, 10.0, -0.0), n=gv.leftSide + '_' + gv.middleA + '_' + gv.fitJoint)
    ltMiddleBJnt            = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(4.85, 10.0, -0.0), n=gv.leftSide + '_' + gv.middleB + '_' + gv.fitJoint)
    ltMiddleCJnt            = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(5.05, 10.0, -0.0), n=gv.leftSide + '_' + gv.middleC + '_' + gv.fitJoint)
    ltMiddleDJnt            = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(5.25, 10.0, -0.0), n=gv.leftSide + '_' + gv.middleD + '_' + gv.fitJoint)
    cmds.select (cl=1)

    ltRingRootJnt           = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(4.5, 10.0,  -0.15), n=gv.leftSide + '_' + gv.ringRoot + '_' + gv.fitJoint)
    ltRingAJnt              = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(4.65, 10.0, -0.15), n=gv.leftSide + '_' + gv.ringA + '_' + gv.fitJoint)
    ltRingBJnt              = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(4.85, 10.0, -0.15), n=gv.leftSide + '_' + gv.ringB + '_' + gv.fitJoint)
    ltRingCJnt              = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(5.05, 10.0, -0.15), n=gv.leftSide + '_' + gv.ringC + '_' + gv.fitJoint)
    ltRingDJnt              = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(5.25, 10.0, -0.15), n=gv.leftSide + '_' + gv.ringD + '_' + gv.fitJoint)
    cmds.select (cl=1)

    ltPinkyRootJnt          = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(4.5, 10.0,  -0.3), n=gv.leftSide + '_' + gv.pinkyRoot + '_' + gv.fitJoint)
    ltPinkyAJnt             = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(4.65, 10.0, -0.3), n=gv.leftSide + '_' + gv.pinkyA + '_' + gv.fitJoint)
    ltPinkyBJnt             = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(4.85, 10.0, -0.3), n=gv.leftSide + '_' + gv.pinkyB + '_' + gv.fitJoint)
    ltPinkyCJnt             = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(5.05, 10.0, -0.3), n=gv.leftSide + '_' + gv.pinkyC + '_' + gv.fitJoint)
    ltPinkyDJnt             = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(5.25, 10.0, -0.3), n=gv.leftSide + '_' + gv.pinkyD + '_' + gv.fitJoint)

    cmds.parent (ltThumbRootJnt, ltIndexRootJnt, ltMiddleRootJnt, ltRingRootJnt, ltPinkyRootJnt, ltwristJnt)
    cmds.select (cl=1)

    generic.setJointLabel (ltThumbRootJnt, gv.thumbRoot, 1, 1)
    generic.setJointLabel (ltIndexRootJnt, gv.indexRoot, 1, 1)
    generic.setJointLabel (ltMiddleRootJnt, gv.middleRoot, 1, 1)
    generic.setJointLabel (ltRingRootJnt, gv.ringRoot, 1, 1)
    generic.setJointLabel (ltPinkyRootJnt, gv.pinkyRoot, 1, 1)

    #Neck
    neckRootSkel            = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(0.0, 10.0, 0.0), n=gv.centerSide + '_' + gv.neckRoot + '_' + gv.fitJoint)
    neckSkel                = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(0.0, 10.5, 0.0), n=gv.centerSide + '_' + gv.neck + '_' + gv.fitJoint)
    neckTipSkel            = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(0.0, 11.0, 0.0), n=gv.centerSide + '_' + gv.neckTip + '_' + gv.fitJoint)
    headRootSkel            = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(0.0, 11.25, 0.0), n=gv.centerSide + '_' + gv.head + '_' + gv.fitJoint)

    cmds.parent (neckRootSkel, chestSkel)
    cmds.select (cl=1)

    generic.setJointLabel (neckRootSkel, gv.neckRoot, 0, 1)
    generic.setJointLabel (neckSkel, gv.neck, 0, 1)
    generic.setJointLabel (neckTipSkel, gv.neckTip, 0, 1)
    generic.setJointLabel (headRootSkel, gv.head, 0, 1)

    #Head
    upperJawSkel            = cmds.joint(rad=gv.jntRadius, o= (0, 180, 0), p=(0, 11.25, 0.4), n=gv.centerSide + '_' + gv.upperJaw  + '_' + gv.fitJoint)
    cmds.select(cl=1)
    lowerJawSkel            = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(0, 11, 0.4), n=gv.centerSide + '_' + gv.lowerJaw  + '_' + gv.fitJoint)
    upperJawEndSkel         = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(0, 11.25, 2.0), n=gv.centerSide + '_' + gv.upperJaw + '_' + 'end'  + '_' + gv.fitJoint)
    lowerJawEndSkel         = cmds.joint(rad=gv.jntRadius, o= (0, 0, 0), p=(0, 11, 2.0), n=gv.centerSide + '_' + gv.lowerJaw + '_' + 'end'  + '_' + gv.fitJoint)

    cmds.parent(upperJawEndSkel, upperJawSkel)
    cmds.parent(lowerJawEndSkel, lowerJawSkel)
    cmds.parent(upperJawSkel, headRootSkel)
    cmds.parent(lowerJawSkel, headRootSkel)
    cmds.select(cl=1)

    generic.setJointLabel (upperJawSkel, gv.upperJaw, 0, 1)
    generic.setJointLabel (lowerJawSkel, gv.lowerJaw, 0, 1)

    #Eye......................
    ltEyeRootSkel           = cmds.joint(rad=gv.jntRadius,  o= (0, 0, 0), p=(0.5, 12.5, 1.50), n=gv.leftSide + '_' + gv.eyeRoot  + '_' + gv.fitJoint)
    ltEyeEndSkel            = cmds.joint(rad=gv.jntRadius,  o= (0, 0, 0), p=(0.5, 12.5, 2.25), n=gv.leftSide + '_' + gv.eye + '_' + gv.fitJoint)
    ltEyeAimSkel            = cmds.joint(rad=gv.jntRadius,  o= (0, 0, 0), p=(0.5, 12.5, 6.00), n=gv.leftSide + '_' + gv.eyeAim + '_' + gv.fitJoint)

    cmds.parent(ltEyeRootSkel, headRootSkel)
    cmds.select(cl=1)
    generic.setJointLabel (ltEyeRootSkel, gv.eyeRoot, 1, 1)
    generic.setJointLabel (ltEyeAimSkel, gv.eyeAim, 1, 1)

    #Eye brow.....................
    cmds.select(cl=1)
    ltUpEyeBrowSkel         = cmds.joint(rad=gv.jntRadius,  o= (-45, 0, 0), p=(0.5, 12.5, 1.50), n=gv.leftSide + '_' + gv.upperEyeBrow + '_' + gv.fitJoint)
    ltUpEyeBrowEndSkel      = cmds.joint(rad=gv.jntRadius,  o= (0, 0, 0), p=(0.5, 13.0, 2.0), n=gv.leftSide + '_' + gv.upperEyeBrow + '_' + 'end' + '_' + gv.fitJoint)
    cmds.select(cl=1)

    ltDnEyeBrowSkel         = cmds.joint(rad=gv.jntRadius,  o= (135, 0,180), p=(0.5, 12.5, 1.50), n=gv.leftSide + '_' + gv.lowerEyeBrow + '_' + gv.fitJoint)
    ltDnEyeBrowEndSkel      = cmds.joint(rad=gv.jntRadius,  o= (0, 0, 0), p=(0.5, 12.0, 2.0), n=gv.leftSide + '_' + gv.lowerEyeBrow + '_' + 'end' + '_' + gv.fitJoint)

    cmds.parent(ltUpEyeBrowSkel, headRootSkel)
    cmds.parent(ltDnEyeBrowSkel, headRootSkel)
    cmds.select(cl=1)

    generic.setJointLabel (ltUpEyeBrowSkel, gv.upperEyeBrow, 1, 1)
    generic.setJointLabel (ltDnEyeBrowSkel, gv.lowerEyeBrow, 1, 1)

    #Tongue.......................................
    tongueRootSkel          = cmds.joint (rad=gv.jntRadius, o= (0, -90, 0), p=(0.0, 11.125, 0.4), n=gv.centerSide + '_' + gv.tongueRoot + '_' + gv.fitJoint)
    tongueASkel             = cmds.joint (rad=gv.jntRadius, o= (0, 0, 0), p=(0.0, 11.125, 0.8), n=gv.centerSide + '_' + gv.tongueA + '_' + gv.fitJoint)
    tongueBSkel             = cmds.joint (rad=gv.jntRadius, o= (0, 0, 0), p=(0.0, 11.125, 1.2), n=gv.centerSide + '_' + gv.tongueB + '_' + gv.fitJoint)
    tongueCSkel             = cmds.joint (rad=gv.jntRadius, o= (0, 0, 0), p=(0.0, 11.125, 1.6), n=gv.centerSide + '_' + gv.tongueC + '_' + gv.fitJoint)
    tongueDSkel             = cmds.joint (rad=gv.jntRadius, o= (0, 0, 0), p=(0.0, 11.125, 2.0), n=gv.centerSide + '_' + gv.tongueD + '_' + gv.fitJoint)

    cmds.parent (tongueRootSkel, headRootSkel)
    cmds.select(cl=1)
    generic.setJointLabel (tongueRootSkel, gv.tongueRoot, 0, 1)

    #Uvula.......................................
    uvulaRootSkel           = cmds.joint (rad=gv.jntRadius, o= (0, -90, 0), p=(0.0, 12.2, 0.4 ), n=gv.centerSide + '_' + gv.uvulaRoot + '_' + gv.fitJoint)
    uvulaASkel              = cmds.joint (rad=gv.jntRadius, o= (0, 0, 0), p=(0.0, 12.0, 0.4 ), n=gv.centerSide + '_' + gv.uvulaA + '_' + gv.fitJoint)
    uvulaBSkel              = cmds.joint (rad=gv.jntRadius, o= (0, 0, 0), p=(0.0, 11.8, 0.4 ), n=gv.centerSide + '_' + gv.uvulaB + '_' + gv.fitJoint)
    uvulaCSkel              = cmds.joint (rad=gv.jntRadius, o= (0, 0, 0), p=(0.0, 11.6, 0.4 ), n=gv.centerSide + '_' + gv.uvulaC + '_' + gv.fitJoint)
    uvulaDSkel              = cmds.joint (rad=gv.jntRadius, o= (0, 0, 0), p=(0.0, 11.4, 0.4 ), n=gv.centerSide + '_' + gv.uvulaD + '_' + gv.fitJoint)

    cmds.parent (uvulaRootSkel, headRootSkel)
    cmds.select(cl=1)
    generic.setJointLabel (uvulaRootSkel, gv.uvulaRoot, 0, 1)

    #Ear.......................................
    earRootSkel             = cmds.joint (rad=gv.jntRadius, o= (0, 0, 0), p=(1.0, 13.0, 0.0), n=gv.leftSide + '_' + gv.earRoot + '_' + gv.fitJoint)
    earASkel                = cmds.joint (rad=gv.jntRadius, o= (0, 0, 0), p=(1.5, 13.0, 0.0), n=gv.leftSide + '_' + gv.earA + '_' + gv.fitJoint)
    earBSkel                = cmds.joint (rad=gv.jntRadius, o= (0, 0, 0), p=(2.0, 13.0, 0.0), n=gv.leftSide + '_' + gv.earB + '_' + gv.fitJoint)
    earCSkel                = cmds.joint (rad=gv.jntRadius, o= (0, 0, 0), p=(2.5, 13.0, 0.0), n=gv.leftSide + '_' + gv.earC + '_' + gv.fitJoint)
    earDSkel                = cmds.joint (rad=gv.jntRadius, o= (0, 0, 0), p=(3.0, 13.0, 0.0), n=gv.leftSide + '_' + gv.earD + '_' + gv.fitJoint)

    cmds.parent (earRootSkel, headRootSkel)
    cmds.select(cl=1)
    generic.setJointLabel (earRootSkel, gv.earRoot, 1, 1)

    cmds.undoInfo(closeChunk=1)
    return True
#End###############################################################################################
'''    

