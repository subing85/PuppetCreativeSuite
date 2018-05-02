'''
Foot for Puppet Creative Suite v1.0.0
Date : April 25, 2018
Last modified: May 02, 2018
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
        
        pymel.undoInfo(openChunk=1) 
        
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
        jointGroup.addAttr(self.input._ikfkBlend,  at='double', min=0, max=1, dv=0, k=True)            

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
            nullFk, shapeFk, offsetFk, groupFk = self.control.create(type='Circle', name='{}_{}_{}'.format(self.type, types[index], self.input._fk), side=self.side, radius=self.radius/1.5, orientation=[0,0,0], positionNode=fkJoints[index])    
             
            if index>0:                
                generic.snap(groupFk, fkControls[index-1][0])
                constraint = generic.getNameStyle([self.side, '{}_{}'.format(self.type, types[index]), '{}_{}_{}_{}'.format(self.input._fk, self.input._control, self.input._group, self.input._parentConstraint)])    
                 
                pymel.parentConstraint(fkControls[index-1][0], groupFk, w=1, n=constraint)
             
            pymel.parentConstraint(shapeFk, fkJoints[index], w=1)            
            fkControls.append([nullFk, shapeFk, offsetFk, groupFk])            
            groupFk.setParent(fkControlGroup)           
   
        #IK Controls
        ikBallHandle = generic.getNameStyle([self.side, '{}_{}'.format(self.type, types[1]), self.input._ikHandle])         
        if pymel.objExists(ikBallHandle):
            pymel.delete (ikBallHandle)      
                     
        ikBallHandle = pymel.ikHandle(n=ikBallHandle, sj=ankle_ik, ee=ball_ik, sol='ikRPsolver', s='sticky')
        ikAnkleEffector = generic.getNameStyle([self.side, '{}_{}'.format(self.type, types[1]), self.input._effector])          
        ikBallHandle[1].rename(ikAnkleEffector)
         
        ikBallHandleGroup = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, types[1]), '{}_{}'.format(self.input._ikHandle, self.input._group)])         
        if pymel.objExists(ikBallHandleGroup):
            pymel.delete (ikBallHandleGroup)          
          
        ikBallHandleGroup = generic.createGroup(ikBallHandle[0], ikBallHandleGroup)
        ikBallHandle[0].setParent(ikBallHandleGroup)
        ikBallHandleGroup.setParent(jointGroup)         
         
        ikToeHandle = generic.getNameStyle([self.side, '{}_{}'.format(self.type, types[2]), self.input._ikHandle])         
        if pymel.objExists(ikToeHandle):
            pymel.delete (ikToeHandle)      
                     
        ikToeHandle = pymel.ikHandle(n=ikToeHandle, sj=ball_ik, ee=toe_ik, sol='ikRPsolver', s='sticky')
        ikBallEffector = generic.getNameStyle([self.side, '{}_{}'.format(self.type, types[2]), self.input._effector])          
        ikToeHandle[1].rename(ikBallEffector) 

        ikToeHandleGroup = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, types[2]), '{}_{}'.format(self.input._ikHandle, self.input._group)])         
        if pymel.objExists(ikToeHandleGroup):
            pymel.delete (ikToeHandleGroup)          
          
        ikToeHandleGroup = generic.createGroup(ikToeHandle[0], ikToeHandleGroup)
        ikToeHandle[0].setParent(ikToeHandleGroup)
        ikToeHandleGroup.setParent(jointGroup)
     
        #IK ball Control        
        nullBallIK, shapeBallIK, offsetBallIK, groupBallIK = self.control.create(type='Circle', name='{}_{}_{}'.format(self.type, types[1], self.input._ik), side=self.side, radius=self.radius/1.5, orientation=[0,0,0], positionNode=ball_ik) 
        groupBallIK.setParent(ikControlGroup)        
        generic.lockHideAttributes(shapeBallIK, 'lockHide', ['tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v'])     
        shapeBallIK.setAttr('rotateOrder', k=True, cb=True)
        
        #Ik Foot Roll
        ikBallGroup = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._ball), '{}_{}'.format(self.input._ik, self.input._group)]) 
        ikBallGroup = generic.createGroup(None, ikBallGroup)        
        generic.snap(self.ball, ikBallGroup)
        
        ikBallRollGroup = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._ball), 'Roll_{}_{}'.format(self.input._ik, self.input._group)]) 
        ikBallRollGroup = generic.createGroup(None, ikBallRollGroup) 
        generic.snap(self.ball, ikBallRollGroup) 
        
        ikHeelGroup = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._heel), '{}_{}'.format(self.input._ik, self.input._group)]) 
        ikHeelGroup = generic.createGroup(None, ikHeelGroup) 
        generic.snap(self.heel, ikHeelGroup)   
        
        ikHeelRollGroup = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._heel), 'Roll_{}_{}'.format(self.input._ik, self.input._group)]) 
        ikHeelRollGroup = generic.createGroup(None, ikHeelRollGroup) 
        generic.snap(self.heel, ikHeelRollGroup)        
        
        ikToeGroup = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._toe), '{}_{}'.format(self.input._ik, self.input._group)]) 
        ikToeGroup = generic.createGroup(None, ikToeGroup) 
        generic.snap(self.toe, ikToeGroup)        
                               
        ikToeRollGroup = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._toe), 'Roll_{}_{}'.format(self.input._ik, self.input._group)]) 
        ikToeRollGroup = generic.createGroup(None, ikToeRollGroup) 
        generic.snap(self.toe, ikToeRollGroup)                       

        ikBigToeGroup = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._bigToe), '{}_{}'.format(self.input._ik, self.input._group)]) 
        ikBigToeGroup = generic.createGroup(None, ikBigToeGroup) 
        generic.snap(self.bigToe, ikBigToeGroup)       
            
        ikPinkyToeGroup = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._pinkyToe), '{}_{}'.format(self.input._ik, self.input._group)]) 
        ikPinkyToeGroup = generic.createGroup(None, ikPinkyToeGroup) 
        generic.snap(self.pinkyToe, ikPinkyToeGroup)  
        
        ikAnkleGroup = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._ankle), '{}_{}'.format(self.input._ik, self.input._group)]) 
        ikAnkleGroup = generic.createGroup(None, ikAnkleGroup) 
        #generic.snap(self.ankle, ikAnkleGroup)  
        generic.snapTranslate(self.ankle, ikAnkleGroup)  
        
        ikBallSdk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._ball), '{}_{}'.format(self.input._ik, self.input._sdk)]) 
        ikBallSdk = generic.createGroup(None, ikBallSdk) 
        generic.snap(self.ball, ikBallSdk)
                          
        ikBallRollSdk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._ball), 'Roll_{}_{}'.format(self.input._ik, self.input._sdk)]) 
        ikBallRollSdk = generic.createGroup(None, ikBallRollSdk) 
        generic.snap(self.ball, ikBallRollSdk)
        
        ikHeelSdk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._heel), '{}_{}'.format(self.input._ik, self.input._sdk)]) 
        ikHeelSdk = generic.createGroup(None, ikHeelSdk) 
        generic.snap(self.heel, ikHeelSdk)   
        
        ikHeelRollSdk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._heel), 'Roll_{}_{}'.format(self.input._ik, self.input._sdk)]) 
        ikHeelRollSdk = generic.createGroup(None, ikHeelRollSdk) 
        generic.snap(self.heel, ikHeelRollSdk)  
                   
        ikToeSdk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._toe), '{}_{}'.format(self.input._ik, self.input._sdk)]) 
        ikToeSdk = generic.createGroup(None, ikToeSdk) 
        generic.snap(self.toe, ikToeSdk)        
                               
        ikToeRollSdk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._toe), 'Roll_{}_{}'.format(self.input._ik, self.input._sdk)]) 
        ikToeRollSdk = generic.createGroup(None, ikToeRollSdk) 
        generic.snap(self.toe, ikToeRollSdk)                   
  
        ikBigToeSdk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._bigToe), '{}_{}'.format(self.input._ik, self.input._sdk)]) 
        ikBigToeSdk = generic.createGroup(None, ikBigToeSdk) 
        generic.snap(self.bigToe, ikBigToeSdk)       
            
        ikPinkyToeSdk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._pinkyToe), '{}_{}'.format(self.input._ik, self.input._sdk)]) 
        ikPinkyToeSdk = generic.createGroup(None, ikPinkyToeSdk) 
        generic.snap(self.pinkyToe, ikPinkyToeSdk)    
  
        ikAnkleSdk = generic.getNameStyle ([self.side, '{}_{}'.format(self.type, self.input._ankle), '{}_{}'.format(self.input._ik, self.input._sdk)]) 
        ikAnkleSdk = generic.createGroup(None, ikAnkleSdk) 
        #generic.snap(self.ankle, ikAnkleSdk)        
        generic.snapTranslate(self.ankle, ikAnkleSdk)  
        
        ikBallSdk.setParent(ikBallGroup)
        ikBallRollSdk.setParent(ikBallRollGroup)
        ikHeelSdk.setParent(ikHeelGroup) 
               
        ikToeRollSdk.setParent(ikToeRollGroup)        
        ikToeGroup.setParent(ikToeRollSdk)        
         
        ikBigToeSdk.setParent(ikBigToeGroup)
        ikPinkyToeSdk.setParent(ikPinkyToeGroup)
        ikAnkleSdk.setParent(ikAnkleGroup)
        
        pymel.parent(ikBallHandleGroup, ikToeHandleGroup, ikBallSdk)
        pymel.parent(ikBallGroup, ikBallRollGroup, ikHeelRollSdk)
        
        ikHeelRollGroup.setParent(ikHeelSdk)
        ikHeelGroup.setParent(ikToeSdk)
        ikToeRollGroup.setParent(ikBigToeSdk)
        ikBigToeGroup.setParent(ikPinkyToeSdk)
        ikPinkyToeGroup.setParent(ikAnkleSdk)

        shapeBallIK.connectAttr('rotate', '{}.rotate'.format(ikBallSdk), f=1) #Ik Control connections
        
        #Foot Roll Connections
        jointGroup.addAttr('reverseFoot',  at='double', dv=0, k=True)            
        jointGroup.setAttr('reverseFoot', cb=True)       
        
        jointGroup.addAttr('footRoll',  at='double', dv=0, k=True)            
        jointGroup.addAttr('footRollAngle',  at='double', dv=0, k=True)            
        jointGroup.addAttr('footTwist',  at='double', dv=0, k=True)            
        jointGroup.addAttr('toeRoll',  at='double', dv=0, k=True)            
        jointGroup.addAttr('toeTwist',  at='double', dv=0, k=True)            
        jointGroup.addAttr('ballLift',  at='double', dv=0, k=True)            
        jointGroup.addAttr('heelTwist',  at='double', dv=0, k=True) 
        
        pymel.setDrivenKeyframe('{}.rotateX'.format(ikBallRollSdk), cd='{}.footRoll'.format(jointGroup), itt='linear', ott='linear', dv=0, v=0)    
        pymel.setDrivenKeyframe('{}.rotateX'.format(ikHeelRollSdk), cd='{}.footRoll'.format(jointGroup), itt='linear', ott='linear', dv=0, v=0)           
        pymel.setDrivenKeyframe('{}.rotateX'.format(ikBallRollSdk), cd='{}.footRoll'.format(jointGroup), itt='linear', ott='linear', dv=180, v=-180)    
        pymel.setDrivenKeyframe('{}.rotateX'.format(ikHeelRollSdk), cd='{}.footRoll'.format(jointGroup), itt='linear', ott='linear', dv=180, v=0)        
        pymel.setDrivenKeyframe('{}.rotateX'.format(ikBallRollSdk), cd='{}.footRoll'.format(jointGroup), itt='linear', ott='linear', dv=-180, v=-0)    
        pymel.setDrivenKeyframe('{}.rotateX'.format(ikHeelRollSdk), cd='{}.footRoll'.format(jointGroup), itt='linear', ott='linear', dv=-180, v=-180)
        
        jointGroup.connectAttr('footRollAngle', '{}.rotateY'.format(ikToeSdk), f=1)
        jointGroup.connectAttr('footTwist', '{}.rotateZ'.format(ikBallRollSdk), f=1)
        
        pymel.setDrivenKeyframe('{}.rotateY'.format(ikToeRollSdk), cd='{}.toeRoll'.format(jointGroup), itt='linear', ott='linear', dv=0, v=0)    
        pymel.setDrivenKeyframe('{}.rotateX'.format(ikHeelSdk), cd='{}.toeRoll'.format(jointGroup), itt='linear', ott='linear', dv=0, v=0)        
        pymel.setDrivenKeyframe('{}.rotateY'.format(ikToeRollSdk), cd='{}.toeRoll'.format(jointGroup), itt='linear', ott='linear', dv=180, v=180)    
        pymel.setDrivenKeyframe('{}.rotateX'.format(ikHeelSdk), cd='{}.toeRoll'.format(jointGroup), itt='linear', ott='linear', dv=180, v=0)        
        pymel.setDrivenKeyframe('{}.rotateY'.format(ikToeRollSdk), cd='{}.toeRoll'.format(jointGroup), itt='linear', ott='linear', dv=180, v=0)    
        pymel.setDrivenKeyframe('{}.rotateX'.format(ikHeelSdk), cd='{}.toeRoll'.format(jointGroup), itt='linear', ott='linear', dv=-180, v=-180)       
        
        jointGroup.connectAttr('toeTwist', '{}.rotateZ'.format(ikToeRollSdk), f=1)
                          
        pymel.setDrivenKeyframe('{}.rotateZ'.format(ikPinkyToeSdk), cd='{}.ballLift'.format(jointGroup), itt='linear', ott='linear', dv=0, v=0)    
        pymel.setDrivenKeyframe('{}.rotateZ'.format(ikBigToeSdk), cd='{}.ballLift'.format(jointGroup), itt='linear', ott='linear', dv=0, v=0)    
        
        pymel.setDrivenKeyframe('{}.rotateZ'.format(ikPinkyToeSdk), cd='{}.ballLift'.format(jointGroup), itt='linear', ott='linear', dv=180, v=-180)    
        pymel.setDrivenKeyframe('{}.rotateZ'.format(ikBigToeSdk), cd='{}.ballLift'.format(jointGroup), itt='linear', ott='linear', dv=180, v=0)            
                      
        pymel.setDrivenKeyframe('{}.rotateZ'.format(ikPinkyToeSdk), cd='{}.ballLift'.format(jointGroup), itt='linear', ott='linear', dv=-180, v=-180)    
        pymel.setDrivenKeyframe('{}.rotateZ'.format(ikBigToeSdk), cd='{}.ballLift'.format(jointGroup), itt='linear', ott='linear', dv=-180, v=180)      
        
        jointGroup.connectAttr('heelTwist', '{}.rotateY'.format(ikHeelSdk), f=1)

        pymel.select(cl=True)                   
        pymel.undoInfo(closeChunk=1)         
#End############################################################################################################################################