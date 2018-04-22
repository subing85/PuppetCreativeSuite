


'''
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya


import utils.variables as variables
gv      = variables.VARIABLES ()
import generic as generic

import mod_createControls as createControl


def createFoot (controlScale, configure, type, side, sideName, foots, footNames) :

    cmds.undoInfo(openChunk=1) 
    
    ankle               = foots[0]
    ball                = foots[1]
    toe                 = foots[2]
    bigToe              = foots[3]    
    pinkyToe            = foots[4] 
    heel                = foots[5] 
       
    footN               = footNames[0]
    ballN               = footNames[1]
    toeN                = footNames[2]
       
    globalFootControlGroup  = gv.foot + '_' + gv.control + '_' + gv.group
    globalFootJointGroup    = gv.foot + '_' + gv.joint + '_' + gv.group
    globalFootDeformGroup   = gv.foot + '_' + gv.deform + '_' + gv.group

    if not cmds.objExists (globalFootControlGroup) :
        footJointGroup          = cmds.group (em=1, n=globalFootControlGroup)             
        cmds.parent (globalFootControlGroup, 'Controls_' + gv.group)
        
    if not cmds.objExists (globalFootJointGroup) :
        footJointGroup          = cmds.group (em=1, n=globalFootJointGroup)                 
        cmds.parent (globalFootJointGroup, 'Skeleton')
        
    if not cmds.objExists (globalFootDeformGroup) :
        footJointGroup          = cmds.group (em=1, n=globalFootDeformGroup)  
        cmds.parent (globalFootDeformGroup, 'Deform')               
        
    footJoints              = [ankle, ball, toe]
    footJointName           = [footN, ballN, toeN]

    ikJoints                = generic.createJoint (footJoints, footJointName, side, gv.ik)
    fkJoints                = generic.createJoint (footJoints, footJointName, side, gv.fk)
    blendJoints             = generic.createJoint (footJoints, footJointName, side, gv.blend) 

    footJointGroup          = cmds.group (em=1, n=side + '_' + type + '_' + gv.joint + '_' + gv.group)               
    ikJntGroup              = cmds.group (em=1, n=side + '_' + type + '_' + gv.ik + '_' + gv.joint + '_' + gv.group)
    fkJntGroup              = cmds.group (em=1, n=side + '_' + type + '_' + gv.fk + '_' + gv.joint + '_' + gv.group)
    blendJntGroup           = cmds.group (em=1, n=side + '_' + type + '_' + gv.blend + '_' + gv.joint + '_' + gv.group)

    footSideControlGroup    = cmds.group (em=1, n=side + '_' + type + '_' +  gv.control + '_' + gv.group)            
    footSideIkControlGroup  = cmds.group (em=1, n=side + '_' + type + '_' +  gv.ik + '_' + gv.control + '_' + gv.group)
    footSideFkControlGroup  = cmds.group (em=1, n=side + '_' + type + '_' +  gv.fk + '_' + gv.control + '_' + gv.group)
  
    generic.snapAction (ikJoints[0], ikJntGroup)
    generic.snapAction (fkJoints[0], fkJntGroup)
    generic.snapAction (blendJoints[0], blendJntGroup)       

    cmds.parent (ikJoints[0], ikJntGroup)
    cmds.parent (fkJoints[0], fkJntGroup)
    cmds.parent (blendJoints[0], blendJntGroup)       

    cmds.parent (ikJntGroup, fkJntGroup, blendJntGroup, footJointGroup)
    cmds.parent (footJointGroup, globalFootJointGroup) 

    cmds.parent (footSideIkControlGroup, footSideFkControlGroup, footSideControlGroup)
    cmds.parent (footSideControlGroup, globalFootControlGroup)

    cmds.setAttr (ikJntGroup + '.visibility', 0, l=1)     
    cmds.setAttr (fkJntGroup + '.visibility', 0, l=1)

    #IK FK Blending Create attributes on configure
    cmds.addAttr (configure, ln=sideName + type + 'IkFk_blend',  at='double', min=0, max=1, dv=0, k=1)       
    
    #Visibility Connection
    visbilityReverse            = cmds.shadingNode ('reverse',  asUtility=1, n=side + '_' + type + '_IKFK_' + gv.reverse)
    cmds.connectAttr (configure + '.' + sideName + type + 'IkFk_blend', visbilityReverse + '.inputX', f=1)
    cmds.connectAttr (configure + '.' + sideName + type + 'IkFk_blend', footSideFkControlGroup + '.visibility', f=1)
    cmds.connectAttr (visbilityReverse + '.outputX', footSideIkControlGroup + '.visibility', f=1)         
    
    for blendLoop in range (0, len(ikJoints), 1) :                       
        blendAttribute          = ['translate', 'rotate', 'scale']                       
        for attriLoop in range (0, 3, 1) :
            blendColor          = cmds.shadingNode ('blendColors',  asUtility=1, n=side + '_' + footJointName[blendLoop] + '_' + blendAttribute[attriLoop].capitalize()  + '_' + gv.blendColor)
            cmds.connectAttr (ikJoints[blendLoop] + '.' + blendAttribute[attriLoop] + 'X', blendColor + '.color2R', f=1)
            cmds.connectAttr (ikJoints[blendLoop] + '.' + blendAttribute[attriLoop] + 'Y', blendColor + '.color2G', f=1)
            cmds.connectAttr (ikJoints[blendLoop] + '.' + blendAttribute[attriLoop] + 'Z', blendColor + '.color2B', f=1)

            cmds.connectAttr (fkJoints[blendLoop] + '.' + blendAttribute[attriLoop] + 'X', blendColor + '.color1R', f=1)
            cmds.connectAttr (fkJoints[blendLoop] + '.' + blendAttribute[attriLoop] + 'Y', blendColor + '.color1G', f=1)
            cmds.connectAttr (fkJoints[blendLoop] + '.' + blendAttribute[attriLoop] + 'Z', blendColor + '.color1B', f=1)               

            cmds.connectAttr (blendColor + '.outputR', blendJoints[blendLoop] + '.' + blendAttribute[attriLoop] + 'X', f=1)
            cmds.connectAttr (blendColor + '.outputG', blendJoints[blendLoop] + '.' + blendAttribute[attriLoop] + 'Y', f=1)
            cmds.connectAttr (blendColor + '.outputB', blendJoints[blendLoop] + '.' + blendAttribute[attriLoop] + 'Z', f=1)   

            cmds.connectAttr (configure + '.' + sideName + type + 'IkFk_blend', blendColor + '.blender', f=1)

    #FK Control
    fkControl               = createControl.createControl ('Circle', side + '_' + ballN + '_' + gv.fk, (0 + controlScale), normal=[0,0,0])
    generic.snapAction (fkJoints[1], fkControl[3])

    fkParentConst           = cmds.parentConstraint (fkControl[0], fkJoints[1], w=1, n=fkJoints[1] + '_' + gv.parentConstraint)
    fkScaleConst            = cmds.scaleConstraint (fkControl[0], fkJoints[1], o=[1,1,1], w=1, n=fkJoints[1] + '_' + gv.scaleConstraint)
    cmds.parent (fkControl[3], footSideFkControlGroup) 

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

''''