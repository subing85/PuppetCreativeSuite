'''
Foot for Puppet Creative Suite v1.0.0
Date : April 25, 2018
Last modified: April 25, 2018
Author: Subin. Gopi (subing85@gmail.com)

# Copyright (c) 2018, Subin Gopi
# All rights reserved.

# WARNING! All changes made in this file will be lost!

Description
    Module for create foot setup
 
example   
from package import createIKStretch
#reload(createIKStretch)
strechGroup = createIKStretch.iKStretch(self.side, self.type, ikJoints, ikHandle[0], nullKneeIk, 'translateX', 1) 
'''

from module import openGeneric
from module import inputNames
from module import openControls

reload(openGeneric)
reload(inputNames)
reload(openControls)

from pymel import core as pymel

class Foot(object):
    
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
        self.ankle = None
        self.ball = None        
        self.toe = None
        self.heel = None        
        self.pinkyToe = None
        self.bigToe = None
        self.radius = 1.00
                
        self.input = inputNames.Names()         
        self.control = openControls.Controls()
        
        if 'side' in kwargs:
            self.side = kwargs['side']
            
        if 'type' in kwargs:
            self.type = kwargs['type']   
            
        if 'ankle' in kwargs:
            self.ankle = kwargs['ankle']  
                        
        if 'ball' in kwargs:            
            self.ball = kwargs['ball']  
                        
        if 'toe' in kwargs:            
            self.toe = kwargs['toe']  
                        
        if 'heel' in kwargs:
            self.heel = kwargs['heel']              
                                               
        if 'pinkyToe' in kwargs:
            self.pinkyToe = kwargs['pinkyToe']  
                        
        if 'bigToe' in kwargs:            
            self.bigToe = kwargs['bigToe']  
           
        if 'radius' in kwargs:
            self.radius = kwargs['radius']  
                        
        self.attributes = ['Translate', 'Rotate', 'Scale']
        
        
    def create(self):
        
        generic = openGeneric.Generic()
        
        #Create deformer joint         
        ankle_dk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._ankle), self.input._dk])
        ball_dk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._ball), self.input._dk])
        toe_dk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._toe), self.input._dk])
         
        ankle_dk = generic.createJoint (radius=0.1, name=ankle_dk, position=self.ankle)
        ball_dk = generic.createJoint (radius=0.1, name=ball_dk, position=self.ball)
        toe_dk = generic.createJoint (radius=0.1, name=toe_dk, position=self.toe)

        ankle_fk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._ankle), self.input._fk])
        ball_fk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._ball), self.input._fk])
        toe_fk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._toe), self.input._fk])
         
        ankle_fk = generic.createJoint (radius=0.1, name=ankle_fk, position=self.ankle)
        ball_fk = generic.createJoint (radius=0.1, name=ball_fk, position=self.ball)
        toe_fk = generic.createJoint (radius=0.1, name=toe_fk, position=self.toe)
        
        ankle_ik = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._ankle), self.input._ik])
        ball_ik = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._ball), self.input._ik])
        toe_ik = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._toe), self.input._ik])
         
        ankle_ik = generic.createJoint (radius=0.1, name=ankle_ik, position=self.ankle)
        ball_ik = generic.createJoint (radius=0.1, name=ball_ik, position=self.ball)
        toe_ik = generic.createJoint (radius=0.1, name=toe_ik, position=self.toe)          
              
        #set the hierarchy        
        generic.setParents ([ankle_dk, ball_dk, toe_dk])        
        generic.setParents ([ankle_fk, ball_fk, toe_fk])        
        generic.setParents ([ankle_ik, ball_ik, toe_ik])        
        
        foot_dkGroup = generic.getNameStyle ([self.side, self.type, '{}_{}_{}'.format (self.input._dk, self.input._joint, self.input._group)])        
        foot_ikGgroup = generic.getNameStyle ([self.side, self.type, '{}_{}_{}'.format (self.input._ik, self.input._joint, self.input._group)])
        foot_fkGroup = generic.getNameStyle ([self.side, self.type, '{}_{}_{}'.format (self.input._fk, self.input._joint, self.input._group)])
         
        foot_dkGroup = generic.createGroup(ankle_dk, foot_dkGroup)
        foot_ikGgroup = generic.createGroup(ankle_ik, foot_ikGgroup)
        foot_fkGroup = generic.createGroup(ankle_fk, foot_fkGroup)
        
        jointGroup = generic.getNameStyle ([self.side, self.type, '{}_{}'.format (self.input._joint, self.input._group)])
        jointGroup = generic.createGroup(None, jointGroup)
        
        foot_dkGroup.setParent (jointGroup)
        foot_ikGgroup.setParent (jointGroup)
        foot_fkGroup.setParent (jointGroup)  
        
        #=======================================================================
        # foot_ikGgroup.setAttr ('visibility', 0, l=True)    
        # foot_fkGroup.setAttr ('visibility', 0, l=True)    
        #=======================================================================
         
        ikJoints = [ankle_ik, ball_ik, toe_ik]
        fkJoints = [ankle_fk, ball_fk, toe_fk]
        dkJoints = [ankle_dk, ball_dk, toe_dk]        
        types = [self.input._ankle, self.input._ball, self.input._toe]                   
         
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
        for index in range (len(fkJoints)-1):
             
            #fkControlName = generic.getNameStyle([self.side, types[index], self.input._control])
            nullFk, shapeFk, offsetFk, groupFk = self.control.create(type='Circle', name='{}_{}_{}'.format(self.type, types[index], self.input._fk), side=self.side, radius=self.radius, orientation=[0,0,0], positionNode=fkJoints[index])    
             
            if index>0:                
                generic.snap(groupFk, fkControls[index-1][0])
                constraint = generic.getNameStyle([self.side, '{}_{}'.format(self.type, types[index]), '{}_{}_{}_{}'.format(self.input._fk, self.input._control, self.input._group, self.input._parentConstraint)])    
                 
                pymel.parentConstraint(fkControls[index-1][0], groupFk, w=1, n=constraint)
             
            pymel.parentConstraint(shapeFk, fkJoints[index], w=1)            
            fkControls.append([nullFk, shapeFk, offsetFk, groupFk])            
            groupFk.setParent(fkControlGroup)           
   
        #IK Controls
        ikAnkleHandle = generic.getNameStyle([self.side, '{}_{}'.format(self.type, types[0]), self.input._ikHandle])         
        if pymel.objExists(ikAnkleHandle):
            pymel.delete (ikAnkleHandle)      
                     
        ikAnkleHandle = pymel.ikHandle(n=ikAnkleHandle, sj=ankle_ik, ee=ball_ik, sol='ikRPsolver', s='sticky')
        ikAnkleEffector = generic.getNameStyle([self.side, '{}_{}'.format(self.type, types[0]), self.input._effector])          
        ikAnkleHandle[1].rename(ikAnkleEffector)
         
        ikAnkleHandleGroup = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, types[0]), '{}_{}'.format(self.input._ikHandle, self.input._group)])         
        if pymel.objExists(ikAnkleHandleGroup):
            pymel.delete (ikAnkleHandleGroup)          
          
        ikAnkleHandleGroup = generic.createGroup(ikAnkleHandle[0], ikAnkleHandleGroup)
        ikAnkleHandle[0].setParent(ikAnkleHandleGroup)
        ikAnkleHandleGroup.setParent(jointGroup)
         
        ikBallHandle = generic.getNameStyle([self.side, '{}_{}'.format(self.type, types[1]), self.input._ikHandle])         
        if pymel.objExists(ikBallHandle):
            pymel.delete (ikBallHandle)      
                     
        ikBallHandle = pymel.ikHandle(n=ikBallHandle, sj=ball_ik, ee=toe_ik, sol='ikRPsolver', s='sticky')
        ikBallEffector = generic.getNameStyle([self.side, '{}_{}'.format(self.type, types[1]), self.input._effector])          
        ikBallHandle[1].rename(ikBallEffector) 

        ikBallHandleGroup = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, types[1]), '{}_{}'.format(self.input._ikHandle, self.input._group)])         
        if pymel.objExists(ikBallHandleGroup):
            pymel.delete (ikBallHandleGroup)          
          
        ikBallHandleGroup = generic.createGroup(ikBallHandle[0], ikBallHandleGroup)
        ikBallHandle[0].setParent(ikBallHandleGroup)
        ikBallHandleGroup.setParent(jointGroup)              
        
     


'''

    #Ik Control    
    ikControl               = createControl.createControl ('Circle', side + '_' + ballN + '_' + gv.ik, (0 + controlScale), normal=[0,0,0])
    generic.snapAction (ikJoints[1], ikControl[3])
    
    cmds.parent (ikControl[3], footSideIkControlGroup)

    generic.lockHideAttributes (fkControl[1], 'lockHide', ['tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v'])       
    generic.lockHideAttributes (ikControl[1], 'lockHide', ['tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v'])   
    cmds.setAttr (fkControl[1] + '.rotateOrder',  k=1, channelBox=1)           

    #Ik Controls setup
    ballIkHandle                = cmds.ikHandle (n=side + '_' + ballN + '_' + gv.ikHandle, sj=ikJoints[0], ee=ikJoints[1], sol='ikSCsolver', s='sticky')
    ballIkEffector              = cmds.rename (ballIkHandle[1], side + '_' + ballN + '_' + gv.effector)               
    
    toeIkHandle                 = cmds.ikHandle (n=side + '_' + toeN + '_' + gv.ikHandle, sj=ikJoints[1], ee=ikJoints[2], sol='ikSCsolver', s='sticky')
    toeIkEffector               = cmds.rename (toeIkHandle[1], side + '_' + toeN + '_' + gv.effector)       

    #Foot Roll         
    ikBallGroup                 = cmds.group (em=1, n=side + '_' + gv.ball + '_' + gv.ik + '_' + gv.group)
    ikBallRollGroup             = cmds.group (em=1, n=side + '_' + gv.ball + '_Roll_' + gv.ik + '_' + gv.group)
    ikHeelRollGroup             = cmds.group (em=1, n=side + '_' + gv.heel + '_Roll_' + gv.ik + '_' + gv.group)
    ikHeelGroup                 = cmds.group (em=1, n=side + '_' + gv.heel + '_' + gv.ik + '_' + gv.group)
    ikToeGroup                  = cmds.group (em=1, n=side + '_' + gv.toe + '_' + gv.ik + '_' + gv.group)
    ikToeRollGroup              = cmds.group (em=1, n=side + '_' + gv.toe + '_Roll_' + gv.ik + '_' + gv.group)
    ikBigToeGroup               = cmds.group (em=1, n=side + '_' + gv.bigToe + '_' + gv.ik + '_' + gv.group)
    ikPinkyToeGroup             = cmds.group (em=1, n=side + '_' + gv.pinkyToe + '_' + gv.ik + '_' + gv.group)
    ikAnkleGroup                = cmds.group (em=1, n=side + '_' + gv.foot + '_' + gv.ik + '_' + gv.group)       

    ikBallSdk                   = cmds.group (em=1, n=side + '_' + gv.ball + '_' + gv.ik + '_' + gv.sdk)
    ikBallRollSdk               = cmds.group (em=1, n=side + '_' + gv.ball + '_Roll_' + gv.ik + '_' + gv.sdk)
    ikHeelRollSdk               = cmds.group (em=1, n=side + '_' + gv.heel + '_Roll_' + gv.ik + '_' + gv.sdk)
    ikHeelSdk                   = cmds.group (em=1, n=side + '_' + gv.heel + '_' + gv.ik + '_' + gv.sdk)
    ikToeSdk                    = cmds.group (em=1, n=side + '_' + gv.toe + '_' + gv.ik + '_' + gv.sdk)
    ikToeRollSdk                = cmds.group (em=1, n=side + '_' + gv.toe + '_Roll_' + gv.ik + '_' + gv.sdk)
    ikBigToeSdk                 = cmds.group (em=1, n=side + '_' + gv.bigToe + '_' + gv.ik + '_' + gv.sdk)
    ikPinkyToeSdk               = cmds.group (em=1, n=side + '_' + gv.pinkyToe + '_' + gv.ik + '_' + gv.sdk)
    ikAnkleSdk                  = cmds.group (em=1, n=side + '_' + gv.foot + '_' + gv.ik + '_' + gv.sdk)

    cmds.parent (ikBallSdk, ikBallGroup)
    cmds.parent (ikBallRollSdk, ikBallRollGroup)
    cmds.parent (ikHeelRollSdk, ikHeelRollGroup)
    cmds.parent (ikHeelSdk, ikHeelGroup)
    cmds.parent (ikToeRollSdk, ikToeRollGroup)

    cmds.parent (ikToeSdk, ikToeGroup) 
    cmds.parent (ikToeGroup, ikToeRollSdk)       

    cmds.parent (ikBigToeSdk, ikBigToeGroup)
    cmds.parent (ikPinkyToeSdk, ikPinkyToeGroup)
    cmds.parent (ikAnkleSdk, ikAnkleGroup)

    generic.snapAction (ball, ikBallGroup)
    generic.snapAction (ball, ikBallRollGroup)
    generic.snapAction (heel, ikHeelRollGroup)
    generic.snapAction (heel, ikHeelGroup)
    generic.snapAction (toe, ikToeRollGroup)
    generic.snapAction (bigToe, ikBigToeGroup)
    generic.snapAction (pinkyToe, ikPinkyToeGroup)
    generic.snapTranslate (ankle, ikAnkleGroup)

    cmds.parent (ballIkHandle[0], toeIkHandle[0], ikBallSdk)
    #cmds.parent (ankleIkHandle[0], ikBallRollSdk)
    cmds.parent (ikBallGroup, ikBallRollGroup, ikHeelRollSdk)
    cmds.parent (ikHeelRollGroup, ikHeelSdk)
    cmds.parent (ikHeelGroup, ikToeSdk)
    cmds.parent (ikToeRollGroup, ikBigToeSdk)
    cmds.parent (ikBigToeGroup, ikPinkyToeSdk)
    cmds.parent (ikPinkyToeGroup, ikAnkleSdk)
    cmds.parent (ikAnkleGroup, globalFootJointGroup)       
    cmds.setAttr (ikAnkleGroup + '.visibility', 0, l=1)        

    #Ik Control connections
    cmds.connectAttr (ikControl[1] + '.rotateX', ikBallSdk + '.rotateX', f=1)
    cmds.connectAttr (ikControl[1] + '.rotateY', ikBallSdk + '.rotateY', f=1)
    cmds.connectAttr (ikControl[1] + '.rotateZ', ikBallSdk + '.rotateZ', f=1) 

    #Foot Roll Connections
    cmds.addAttr (configure, ln=sideName + type + 'ReverseFoot',  at='double', dv=0, k=1)
    cmds.setAttr (configure + '.' + sideName + type + 'ReverseFoot', channelBox=1)

    cmds.addAttr (configure, ln=sideName + type + 'FootRoll',  at='double', dv=0, k=1)
    cmds.addAttr (configure, ln=sideName + type + 'FootRollAngle',  at='double', dv=0, k=1)
    cmds.addAttr (configure, ln=sideName + type + 'FootTwist',  at='double', dv=0, k=1)
    cmds.addAttr (configure, ln=sideName + type + 'ToeRoll',  at='double', dv=0, k=1)
    cmds.addAttr (configure, ln=sideName + type + 'ToeTwist',  at='double', dv=0, k=1)
    cmds.addAttr (configure, ln=sideName + type + 'BallLift',  at='double',dv=0, k=1)
    cmds.addAttr (configure, ln=sideName + type + 'HeelTwist',  at='double', dv=0, k=1)

    cmds.setDrivenKeyframe (ikBallRollSdk + '.rotateY', cd=configure + '.' + sideName + type + 'FootRoll', itt='linear', ott='linear', dv=0, v=0)       
    cmds.setDrivenKeyframe (ikHeelRollSdk + '.rotateX', cd=configure + '.' + sideName + type + 'FootRoll', itt='linear', ott='linear', dv=0, v=0) 
    cmds.setDrivenKeyframe (ikBallRollSdk + '.rotateY', cd=configure + '.' + sideName + type + 'FootRoll', itt='linear', ott='linear', dv=180, v=-180)       
    cmds.setDrivenKeyframe (ikHeelRollSdk + '.rotateX', cd=configure + '.' + sideName + type + 'FootRoll', itt='linear', ott='linear', dv=180, v=0)       
    cmds.setDrivenKeyframe (ikBallRollSdk + '.rotateY', cd=configure + '.' + sideName + type + 'FootRoll', itt='linear', ott='linear', dv=-180, v=0)       
    cmds.setDrivenKeyframe (ikHeelRollSdk + '.rotateX', cd=configure + '.' + sideName + type + 'FootRoll', itt='linear', ott='linear', dv=-180, v=-180) 

    cmds.connectAttr (configure + '.' + sideName + type + 'FootRollAngle', ikToeSdk + '.rotateY', f=1)
    cmds.connectAttr (configure + '.' + sideName + type + 'FootTwist', ikBallRollSdk + '.rotateZ', f=1)

    cmds.setDrivenKeyframe (ikToeRollSdk + '.rotateY', cd=configure + '.' + sideName + type + 'ToeRoll', itt='linear', ott='linear', dv=0, v=0)       
    cmds.setDrivenKeyframe (ikHeelSdk + '.rotateX', cd=configure + '.' + sideName + type + 'ToeRoll', itt='linear', ott='linear', dv=0, v=0)  

    cmds.setDrivenKeyframe (ikToeRollSdk + '.rotateY', cd=configure + '.' + sideName + type + 'ToeRoll', itt='linear', ott='linear', dv=180, v=-180)       
    cmds.setDrivenKeyframe (ikHeelSdk + '.rotateX', cd=configure + '.' + sideName + type + 'ToeRoll', itt='linear', ott='linear', dv=180, v=0)

    cmds.setDrivenKeyframe (ikToeRollSdk + '.rotateY', cd=configure + '.' + sideName + type + 'ToeRoll', itt='linear', ott='linear', dv=-180, v=0)       
    cmds.setDrivenKeyframe (ikHeelSdk + '.rotateX', cd=configure + '.' + sideName + type + 'ToeRoll', itt='linear', ott='linear', dv=-180, v=-180)

    cmds.connectAttr (configure + '.' + sideName + type + 'ToeTwist', ikToeRollSdk + '.rotateZ', f=1)

    cmds.setDrivenKeyframe (ikPinkyToeSdk + '.rotateZ', cd=configure + '.' + sideName + type + 'BallLift', itt='linear', ott='linear', dv=0, v=0)       
    cmds.setDrivenKeyframe (ikBigToeSdk + '.rotateZ', cd=configure + '.' + sideName + type + 'BallLift', itt='linear', ott='linear', dv=0, v=0)

    cmds.setDrivenKeyframe (ikPinkyToeSdk + '.rotateZ', cd=configure + '.' + sideName + type + 'BallLift', itt='linear', ott='linear', dv=180, v=-180)       
    cmds.setDrivenKeyframe (ikBigToeSdk + '.rotateZ', cd=configure + '.' + sideName + type + 'BallLift', itt='linear', ott='linear', dv=180, v=0)                

    cmds.setDrivenKeyframe (ikPinkyToeSdk + '.rotateZ', cd=configure + '.' + sideName + type + 'BallLift', itt='linear', ott='linear', dv=-180, v=0)       
    cmds.setDrivenKeyframe (ikBigToeSdk + '.rotateZ', cd=configure + '.' + sideName + type + 'BallLift', itt='linear', ott='linear', dv=-180, v=180)   

    cmds.connectAttr (configure + '.' + sideName + type + 'HeelTwist', ikHeelSdk + '.rotateY', f=1)
    cmds.undoInfo(closeChunk=1)

'''