'''
Twist for Puppet Creative Suite v1.0.0
Date : April 10, 2018
Last modified: April 10, 2018
Author: Subin. Gopi (subing85@gmail.com)

# Copyright (c) 2018, Subin Gopi
# All rights reserved.

# WARNING! All changes made in this file will be lost!

Description
    Module for Twist
 
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

def twist(side, type, upperTwistJoints, lowerTwistJoints, dkJoints, twistAxis, radius, orientation):
    
    pymel.undoInfo(openChunk=1)   
    
    channelAttributes = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY', 'scaleZ', 'v']
    channelAttributes.remove(twistAxis)
        
    generic = openGeneric.Generic()     
    input = inputNames.Names()           
    control = openControls.Controls()      
    
    globalScaleGroup = generic.getNameStyle ([side, type, '{}_{}'.format(input._globalScale, input._group)])    
    
    if not pymel.objExists(globalScaleGroup):
        globalScaleGroup = generic.createGroup(None, globalScaleGroup) 
    else:
        globalScaleGroup= pymel.PyNode(globalScaleGroup)        

    #create twist control
    nullUpperTwist, shapeUpperTwist, offsetUpperTwist, groupUpperTwist = control.create(type='ArrowSinglePin', name='{}_UpperTwist'.format(type), side=side, radius=radius, orientation=orientation, positionNode=dkJoints[0])    
    nullMiddleTwist, shapeMiddleTwist, offsetMiddleTwist, groupMiddleTwist = control.create(type='ArrowSinglePin', name='{}_MiddleTwist'.format(type), side=side, radius=radius, orientation=orientation, positionNode=dkJoints[1])    
    nullLowerTwist, shapeLowerTwist, offsetLowerTwist, groupLowerTwist = control.create(type='ArrowSinglePin', name='{}_LowerTwist'.format(type), side=side, radius=radius, orientation=orientation, positionNode=dkJoints[2])    

    #twist control group
    twistControlGroup = generic.getNameStyle ([side, type, 'Twist_{}_{}'.format(input._control, input._group)])    
    generic.removeExistsNode([twistControlGroup])
        
    twistControlGroup = generic.createGroup(None, twistControlGroup)     
    pymel.parent (groupUpperTwist, groupMiddleTwist, groupLowerTwist, twistControlGroup)     
    
    generic.lockHideAttributes (shapeUpperTwist, 'lockHide', channelAttributes)
    generic.lockHideAttributes (shapeMiddleTwist, 'lockHide', channelAttributes)
    generic.lockHideAttributes (shapeLowerTwist, 'lockHide', channelAttributes)
    
    #Twist control attributes
    twistControlGroup.addAttr('upperTwist', at='double', dv=0, k=1)
    twistControlGroup.addAttr('middleTwist', at='double', dv=0, k=1)
    twistControlGroup.addAttr('lowerTwist', at='double', dv=0, k=1)
        
    twistControlGroup.addAttr('middleTwistPosition', at='double', dv=0, k=1)
    twistControlGroup.addAttr('upperTwistFallOff', at='double', dv=0, k=1)
    twistControlGroup.addAttr('middleTwistFallOff', at='double', dv=0, k=1)
    twistControlGroup.addAttr('lowerTwistFallOff', at='double', dv=0, k=1)
    
    upperTwist_mdn = generic.getNameStyle ([side, type, 'UpperTwist{}'.format (input._multiplyDivide)])
    middleUpTwist_mdn = generic.getNameStyle ([side, type, 'MiddleTwist_UP{}'.format (input._multiplyDivide)])
    middleDnTwist_mdn = generic.getNameStyle ([side, type, 'MiddleTwist_LO{}'.format (input._multiplyDivide)])
    lowerTwist_mdn = generic.getNameStyle ([side, type, 'LowerTwist{}'.format (input._multiplyDivide)])

    generic.removeExistsNode([upperTwist_mdn, middleUpTwist_mdn, middleDnTwist_mdn, lowerTwist_mdn])

    upperTwist_mdn = pymel.shadingNode ('multiplyDivide', asUtility=1, n=upperTwist_mdn)    
    middleUpTwist_mdn = pymel.shadingNode ('multiplyDivide', asUtility=1, n=middleUpTwist_mdn)    
    middleDnTwist_mdn = pymel.shadingNode ('multiplyDivide', asUtility=1, n=middleDnTwist_mdn)    
    lowerTwist_mdn = pymel.shadingNode ('multiplyDivide', asUtility=1, n=lowerTwist_mdn)
    
    twistControlGroup.connectAttr('upperTwist', '{}.input1X'.format(upperTwist_mdn), f=True)
    twistControlGroup.connectAttr('middleTwist', '{}.input1X'.format(middleUpTwist_mdn), f=True)    
    twistControlGroup.connectAttr('middleTwist', '{}.input1X'.format(middleDnTwist_mdn), f=True)
    twistControlGroup.connectAttr('lowerTwist', '{}.input1X'.format(lowerTwist_mdn), f=True)
    
    twistControlGroup.connectAttr('upperTwistFallOff', '{}.input2X'.format(upperTwist_mdn), f=True)    
    twistControlGroup.connectAttr('middleTwistPosition', '{}.input2X'.format(middleUpTwist_mdn), f=True)    
    twistControlGroup.connectAttr('middleTwistFallOff', '{}.input2X'.format(middleDnTwist_mdn), f=True)    
    twistControlGroup.connectAttr('lowerTwistFallOff', '{}.input2X'.format(lowerTwist_mdn), f=True)
    
    nullMiddle, shapeMiddle, offsetMiddle, groupMiddle = control.create(type='SmoothSphere', name='{}_Middle'.format(type), side=side, radius=radius/1.75, orientation=orientation, positionNode=dkJoints[1])    
    generic.lockHideAttributes(shapeMiddle, 'lockHide', ['rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'])
    groupMiddle.setParent (twistControlGroup) 

    upperTwist_mdsn = [upperTwist_mdn, middleUpTwist_mdn]
    lowerTwist_mdsn = [middleDnTwist_mdn, lowerTwist_mdn]

    upJoints = [dkJoints[0], dkJoints[1]]
    dnJoints = [dkJoints[1], dkJoints[2]]    
    twistType = ['UpperTwist', 'LowerTwist']
    twistJoints = [upperTwistJoints, lowerTwistJoints]    
        
    twistDeformGroup = generic.getNameStyle ([side, type, 'Twist_{}'.format (input._group)])            
    twistDeformGroup = generic.createGroup(None, twistDeformGroup)     
        
    for index in range (2) :       
        up_xyz = pymel.xform (upJoints[index], q=1, ws=1, t=1)          
        dn_xyz = pymel.xform (dnJoints[index], q=1, ws=1, t=1)         
                 
        tempTwistCurve = pymel.curve (d=1,p=[(up_xyz), (dn_xyz)], k=[0, 1])
                
        twistCurve = generic.getNameStyle ([side, type, '{}_{}'.format (twistType[index], input._curve)])
        generic.removeExistsNode([twistCurve])         
        twistCurve = tempTwistCurve.rename(twistCurve)        
        twistCurveShape = twistCurve.getShape()        
        twistCurve.setAttr('visibility', 0, l=True)
        
        twistLength = len(twistJoints[index])
        twistIng = 1.00/float(twistLength)        
        twistPose = 0         

        #object Up object 
        objectUpLocator = generic.getNameStyle ([side, type, '{}_ObjectUp_{}'.format (twistType[index], input._locator)])    
        generic.removeExistsNode([objectUpLocator])               
        objectUpLocator = pymel.spaceLocator (p=[0, 0, 0], n=objectUpLocator)
        generic.snap(twistJoints[index][0], objectUpLocator)        
        objectUpLocator.setAttr ('visibility', 0, l=True) 
        
        eachTwistDeformGroup = generic.getNameStyle ([side, type, '{}_{}'.format (twistType[index], input._group)])            
        eachTwistDeformGroup = generic.createGroup(None, eachTwistDeformGroup)
        pymel.parent (twistCurve, objectUpLocator, eachTwistDeformGroup)        
        eachTwistDeformGroup.setParent(twistDeformGroup)
        
        objectUpParentConst = generic.getNameStyle ([side, type, 'ObjectUp_{}_{}'.format (input._locator, input._pointConstraint)]) 
        pymel.pointConstraint (dkJoints[index], objectUpLocator, o=[0, 0, 0], w=1, n=objectUpParentConst)
    
        twistLocatorGroup = generic.getNameStyle ([side, type, '{}_{}_{}'.format(twistType[index], input._locator, input._group)])    
        generic.removeExistsNode([twistLocatorGroup])       
        twistLocatorGroup = generic.createGroup(None, twistLocatorGroup)             
        twistLocatorGroup.setParent (eachTwistDeformGroup)     
        twistLocatorGroup.setAttr ('visibility', 0, l=True)
        
        twistLocators = []        

        for twistIntex in range (len(twistJoints[index])):
            paddingSize = '{}{}'.format (generic.padding (twistIntex+1, 2), twistIntex+1)            
            jointRotateOrder = twistJoints[index][twistIntex].getAttr('rotateOrder')
            
            twistJoint = generic.getNameStyle ([side, type, '{}_{}_{}'.format (twistType[index], paddingSize, input._joint)]) 
            generic.removeExistsNode([twistJoint]) 
            pymel.select (cl=1)        
            twistJoint = pymel.joint (rad=input._jointRadius, n=twistJoint)
            twistJoint.setAttr('rotateOrder', jointRotateOrder)
            
            twistLocator = generic.getNameStyle ([side, type, '{}_{}_{}'.format (twistType[index], paddingSize, input._locator)]) 
            generic.removeExistsNode([twistLocator])               
            twistLocator = pymel.spaceLocator (p=[0, 0, 0], n=twistLocator)
            twistJoint.setParent(twistLocator)              
            twistLocators.append(twistLocator)
            
            generic.snap(twistJoints[index][twistIntex], twistLocator)        
            pymel.makeIdentity (twistJoint, a=1, t=0, r=1, s=0, n=0)            
            
            
            pointOnCrInfo = generic.getNameStyle ([side, type, '{}_{}_{}'.format (twistType[index], paddingSize, input._pointOnCurveInfo)])
            generic.removeExistsNode([pointOnCrInfo])               
            pointOnCrInfo = pymel.createNode ('pointOnCurveInfo', n=pointOnCrInfo)            
            pointOnCrInfo.setAttr('turnOnPercentage', 1, k=True, l=True)
            pointOnCrInfo.setAttr('parameter', twistPose, k=True, l=True)            
            
            twistCurveShape.connectAttr('worldSpace[0]', '{}.inputCurve'.format(pointOnCrInfo))
            pointOnCrInfo.connectAttr('positionX', '{}.translateX'.format(twistLocator))
            pointOnCrInfo.connectAttr('positionY', '{}.translateY'.format(twistLocator))
            pointOnCrInfo.connectAttr('positionZ', '{}.translateZ'.format(twistLocator))              
               
            twistLocator.setParent(twistLocatorGroup)
            
            #Replace scale            
            globalScaleGroup.connectAttr('scaleX', '{}.scaleX'.format(twistLocator))
            globalScaleGroup.connectAttr('scaleY', '{}.scaleY'.format(twistLocator))
            globalScaleGroup.connectAttr('scaleZ', '{}.scaleZ'.format(twistLocator))
            
            

            if twistIntex>0: #Aim Constrain
                constraintPaddingSize = '{}{}'.format (generic.padding (twistIntex+1, 2), twistIntex)    
                aimConstraint = generic.getNameStyle([side, type, '{}_{}_{}_{}'.format (twistType[index], constraintPaddingSize, input._locator, input._aimConstraint)]) 
                pymel.aimConstraint(twistLocators [twistIntex], 
                                    twistLocators[twistIntex-1],  
                                    o=[0, 0, 0], w=1, 
                                    aim=[1, 0, 0], 
                                    u=[0, 1, 0], 
                                    wut='objectrotation',
                                    wu=[0,1,0], wuo=objectUpLocator, 
                                    n=aimConstraint
                                    )
            
            if twistIntex==len(twistJoints[index])-1 :
                aimConstraint = generic.getNameStyle ([side, type, '{}_{}_{}'.format (twistLocators[twistIntex], paddingSize, input._locator, input._aimConstraint)])
                pymel.aimConstraint(twistLocators[twistIntex-1], 
                                    twistLocators [twistIntex],  
                                    o=[0, 0, 0], 
                                    w=1, 
                                    aim=[-1, 0, 0], 
                                    u=[0, 1, 0], 
                                    wut='objectrotation', 
                                    wu=[0,1,0], 
                                    wuo=objectUpLocator, 
                                    n=aimConstraint)            
            
            eachTwistAttribute = '{}_{}_{}_Twist_{}'.format(side, type, twistType[index], paddingSize) 
            twistControlGroup.addAttr(eachTwistAttribute, at='double', dv=0, k=1)
            shapeMiddleTwist.addAttr(eachTwistAttribute, at='double', dv=0, k=1)
            
            twistBlendColor = '{}_{}_{}_Twist_'.format(side, type, twistType[index], paddingSize, input._blendColor)
            generic.removeExistsNode([twistBlendColor])                
            twistBlendColor = pymel.shadingNode ('blendColors',  asUtility=1, n=twistBlendColor)
    
            lowerTwist_mdsn[index].connectAttr('outputX', '{}.color1R'.format(twistBlendColor), f=True)        
            upperTwist_mdsn[index].connectAttr('outputX', '{}.color2R'.format(twistBlendColor), f=True)          
            twistBlendColor.connectAttr('outputR', '{}.rotateX'.format(twistJoint), f=True)          
            twistControlGroup.connectAttr(eachTwistAttribute, '{}.blender'.format(twistBlendColor), f=True)
            shapeMiddleTwist.connectAttr(eachTwistAttribute, '{}.{}'.format(twistControlGroup, eachTwistAttribute), f=True)


            twistPose+=twistIng
       
#===============================================================================
#     twistBindJoints = []
#     twistControls = [upperTwistControl[0], middleTwistControl[0], lowerTwistControl[0]]       
#     twistAttribute = [type + 'UpperTwist', type + 'MiddleTwist', type + 'LowerTwist']
#     limbJoints = [upperJoints[0], lowerJoints[0], lowerJoints[-1]]
# 
#     twistLockLocator = cmds.spaceLocator (p=[0, 0, 0], n=side + '_' + type + '_Twist_' + gv.locator)
#     twistLockLocGroup = cmds.group (em=1, n=side + '_' + type + '_Twist_' + gv.locator + '_' + gv.group)
#===============================================================================
           
       
       
    '''  


    cmds.parent (twistLockLocator[0], twistLockLocGroup)
    generic.locatorSacle (twistLockLocator, 0.1, 1)
    generic.snapAction (blendJoints[0], twistLockLocGroup)
    cmds.parent (twistLockLocGroup, twistLocatorGroup)       

    cmds.select (cl=1)
    
    for twistBindLoop in range (0, 3, 1) : 
        cmds.select (cl=1)
        twistBindJoint              = cmds.joint (rad=gv.jntRadius, n=side + '_' + type + '_' + twistCtrlType[twistBindLoop] + 'Twist_' + gv.joint)
        twistBindJointGroup         = cmds.group (em=1, n=side + '_' + type + '_' + twistCtrlType[twistBindLoop] + 'Twist_' + gv.joint + '_' + gv.group)

        cmds.parent (twistBindJoint, twistBindJointGroup)           
    
        generic.snapAction (limbJoints[twistBindLoop], twistBindJointGroup)   
        cmds.makeIdentity (twistBindJoint, a=1, t=0, r=1, s=0, n=0)
        twistBindJoints.append (twistBindJoint)           
        cmds.parent (twistBindJointGroup, twistLocatorGroup)            
        cmds.select (cl=1)

        twistParentConst            = cmds.parentConstraint (twistControls[twistBindLoop], twistBindJointGroup, w=1, n=twistBindJointGroup + '_' + gv.parentConstraint)
        twistScaleConst             = cmds.scaleConstraint (twistControls[twistBindLoop], twistBindJointGroup, o=[1,1,1], w=1, n=twistBindJointGroup + '_' + gv.scaleConstraint)

        twistLocator                = cmds.spaceLocator (p=[0, 0, 0], n=side + '_' + type + '_' + twistCtrlType[twistBindLoop] + 'Twist_' + gv.locator)
        twistLocGroup               = cmds.group (em=1, n=side + '_' + type + '_' + twistCtrlType[twistBindLoop] + 'Twist_' + gv.locator + '_' + gv.group)

        cmds.parent (twistLocator[0], twistLocGroup)
        generic.locatorSacle (twistLocator, 0.1, 0)
        generic.snapAction (limbJoints[twistBindLoop], twistLocGroup)
        cmds.parent (twistLocGroup, twistLocatorGroup)

        twistLocConst               = cmds.parentConstraint (twistControls[twistBindLoop], twistLocator[0], w=1, n=twistLocator[0] + '_' + gv.parentConstraint)

        #Connect to configure node
        cmds.connectAttr (twistLocator[0] + '.rotateX', configure + '.' + sideName + twistAttribute[twistBindLoop], f=1)
    
    cmds.skinCluster (twistBindJoints, twistCurves[0], tsb=True, mi=1, dr=4.0, rui=0, normalizeWeights=1, obeyMaxInfluences=True, n=twistCurves[0] + '_SkinClu')
    cmds.skinCluster (twistBindJoints, twistCurves[1], tsb=True, mi=1, dr=4.0, rui=0, normalizeWeights=1, obeyMaxInfluences=True, n=twistCurves[1] + '_SkinClu')

    kneeParentConst                 = cmds.parentConstraint (middleKneeControl[0], middleTwistControl[3], w=1, n=middleTwistControl[3] + '_' + gv.parentConstraint)
    kneeScaleConst                  = cmds.scaleConstraint (middleKneeControl[0], middleTwistControl[3], o=[1,1,1], w=1, n=middleTwistControl[3] + '_' + gv.scaleConstraint)                           

    #Leg Middle Twist Position
    middlePointConst                = cmds.pointConstraint (blendJoints[0], blendJoints[1], blendJoints[2], middleKneeControl[3], o=[0, 0, 0], w=1, n=middleKneeControl[3] + '_' + gv.pointConstraint)
    cmds.setDrivenKeyframe (middlePointConst[0] + '.' + blendJoints[0] + 'W0', cd=configure + '.' + sideName + type + 'MiddleTwistPosition', itt='linear', ott='linear', dv=0, v=0)       
    cmds.setDrivenKeyframe (middlePointConst[0] + '.' + blendJoints[1] + 'W1', cd=configure + '.' + sideName + type + 'MiddleTwistPosition', itt='linear', ott='linear', dv=0, v=1)        
    cmds.setDrivenKeyframe (middlePointConst[0] + '.' + blendJoints[2] + 'W2', cd=configure + '.' + sideName + type + 'MiddleTwistPosition', itt='linear', ott='linear', dv=0, v=0)       

    cmds.setDrivenKeyframe (middlePointConst[0] + '.' + blendJoints[0] + 'W0', cd=configure + '.' + sideName + type + 'MiddleTwistPosition', itt='linear', ott='linear', dv=1, v=1)       
    cmds.setDrivenKeyframe (middlePointConst[0] + '.' + blendJoints[1] + 'W1', cd=configure + '.' + sideName + type + 'MiddleTwistPosition', itt='linear', ott='linear', dv=1, v=0)       
    cmds.setDrivenKeyframe (middlePointConst[0] + '.' + blendJoints[2] + 'W2', cd=configure + '.' + sideName + type + 'MiddleTwistPosition', itt='linear', ott='linear', dv=1, v=0)   

    cmds.setDrivenKeyframe (middlePointConst[0] + '.' + blendJoints[0] + 'W0', cd=configure + '.' + sideName + type + 'MiddleTwistPosition', itt='linear', ott='linear', dv=-1, v=0)       
    cmds.setDrivenKeyframe (middlePointConst[0] + '.' + blendJoints[1] + 'W1', cd=configure + '.' + sideName + type + 'MiddleTwistPosition', itt='linear', ott='linear', dv=-1, v=0)       
    cmds.setDrivenKeyframe (middlePointConst[0] + '.' + blendJoints[2] + 'W2', cd=configure + '.' + sideName + type + 'MiddleTwistPosition', itt='linear', ott='linear', dv=-1, v=1)

    #Connect to configure node
    cmds.addAttr (upperTwistControl[1], ln='twistFallOff', at='double', min=-1, max=1, dv=1, k=1)
    cmds.addAttr (middleTwistControl[1], ln='twistFallOff', at='double', min=-1, max=1, dv=1, k=1)
    cmds.addAttr (lowerTwistControl[1], ln='twistFallOff', at='double', min=-1, max=1, dv=1, k=1)       
    cmds.addAttr (middleKneeControl[1], ln='position', at='double', min=-1, max=1, dv=0, k=1)       

    cmds.connectAttr (upperTwistControl[1] + '.twistFallOff', configure + '.' + sideName + type + 'UpperTwistFallOff',  f=1)
    cmds.connectAttr (middleTwistControl[1] + '.twistFallOff', configure + '.' + sideName + type + 'MiddleTwistFallOff',  f=1)
    cmds.connectAttr (lowerTwistControl[1] + '.twistFallOff', configure + '.' + sideName + type + 'LowerTwistFallOff',  f=1)       
    cmds.connectAttr (middleKneeControl[1] + '.position', configure + '.' + sideName + type + 'MiddleTwistPosition',  f=1)
    
    cmds.undoInfo(closeChunk=1)       
       
       
    '''
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
            
            

    pymel.undoInfo(closeChunk=1)
    return twistControlGroup
   
    
'''
def twistSetup (controlScale, configure, type, side, sideName, upperJoints, lowerJoints, blendJoints):
    
    
    cmds.undoInfo(openChunk=1)        



    cmds.parent (upperTwistControl[3], twistControlGroup)        
    cmds.parent (middleTwistControl[3], twistControlGroup)        
    cmds.parent (lowerTwistControl[3], twistControlGroup)                        
    cmds.parent (middleKneeControl[3], twistControlGroup)       

    twistJoints = []
    
        for tJntLoop in range (0, len(twistJoints[twistLoop]), 1) :
            paddingSize         = str (generic.padding (tJntLoop+1, 2)) + str(tJntLoop + 1)
            jointRotateOrder    = cmds.getAttr (twistJoints[twistLoop][tJntLoop] + '.rotateOrder')
            eachTwistJoint      = cmds.joint (rad=gv.jntRadius, n=side + '_' + type + '_' + twistType[twistLoop] + 'Twist_' + paddingSize + '_' + gv.joint)
            eachTwistLocator    = cmds.spaceLocator (p=[0, 0, 0], n=side + '_' + type + '_' + twistType[twistLoop] + 'Twist_' + paddingSize + '_' + gv.locator)
            cmds.setAttr (eachTwistJoint + '.rotateOrder', jointRotateOrder)

            generic.locatorSacle (eachTwistLocator, 0.1, 1)
            twistLocators.append (eachTwistLocator[0])
            cmds.parent (eachTwistJoint, eachTwistLocator[0])
            
            generic.snapAction (twistJoints[twistLoop][tJntLoop], eachTwistLocator[0])       
            cmds.makeIdentity (eachTwistJoint, a=1, t=0, r=1, s=0, n=0)
            cmds.select (cl=1)

            pointOnCrInfo       = cmds.createNode ('pointOnCurveInfo', n=side + '_' + type + '_' + twistType[twistLoop] + 'Twist_' + paddingSize + '_' + gv.pointOnCurveInfo)
            cmds.setAttr (pointOnCrInfo + '.turnOnPercentage', 1, k=1, l=1)
            cmds.setAttr (pointOnCrInfo + '.parameter', twistPose, k=1)  

            #twistCurveShape
            cmds.connectAttr (twistCurveShape[0] + '.worldSpace[0]', pointOnCrInfo + '.inputCurve')       
            cmds.connectAttr (pointOnCrInfo + '.positionX', eachTwistLocator[0] + '.translateX')       
            cmds.connectAttr (pointOnCrInfo + '.positionY', eachTwistLocator[0] + '.translateY')       
            cmds.connectAttr (pointOnCrInfo + '.positionZ', eachTwistLocator[0] + '.translateZ')               

            cmds.parent (eachTwistLocator[0], twistDeformGroup)

            cmds.connectAttr (gv.globalScale + '_' + gv.group + '.scaleX', eachTwistLocator[0] + '.scaleX', f=1)
            cmds.connectAttr (gv.globalScale + '_' + gv.group + '.scaleY', eachTwistLocator[0] + '.scaleY', f=1)
            cmds.connectAttr (gv.globalScale + '_' + gv.group + '.scaleZ', eachTwistLocator[0] + '.scaleZ', f=1)

            #Aim Constrain
            if tJntLoop>0 :
                twistAimConst       = cmds.aimConstraint(twistLocators [tJntLoop], twistLocators[tJntLoop-1],  o=[0, 0, 0], w=1, aim=[1, 0, 0], u=[0, 1, 0], wut='objectrotation', wu=[0,1,0], wuo=objectUpLocator[0], n=twistLocators[tJntLoop-1] + '_' + gv.aimConstraint)

            if tJntLoop==len(twistJoints[twistLoop])-1 :
                twistAimConst       = cmds.aimConstraint (twistLocators[tJntLoop-1], twistLocators [tJntLoop],  o=[0, 0, 0], w=1, aim=[-1, 0, 0], u=[0, 1, 0], wut='objectrotation', wu=[0,1,0], wuo=objectUpLocator[0], n=twistLocators [tJntLoop] + '_' + gv.aimConstraint)

            cmds.addAttr (configure, ln=sideName + '_' + type + '_' + twistType[twistLoop] + 'Twist_' + paddingSize,  at='double', dv=twistPose, k=1)
            cmds.addAttr (middleTwistControl[1], ln=twistType[twistLoop] + 'Twist_' + paddingSize,  at='double', dv=twistPose)

            legTwistBlendColor      = cmds.shadingNode ('blendColors',  asUtility=1, n=side + '_' + type + '_' + twistType[twistLoop] + 'Twist_' + paddingSize + '_' + gv.blendColor)
            cmds.connectAttr (legLowerTwist_mdsn[twistLoop] + '.outputX', legTwistBlendColor + '.color1R', f=1)
            cmds.connectAttr (legUpperTwist_mdsn[twistLoop] + '.outputX', legTwistBlendColor + '.color2R', f=1)               
            cmds.connectAttr (legTwistBlendColor + '.outputR', eachTwistJoint + '.rotateX', f=1)
            cmds.connectAttr (configure + '.'+ sideName + '_' + type + '_' + twistType[twistLoop] + 'Twist_' + paddingSize, legTwistBlendColor + '.blender', f=1)
            cmds.connectAttr (middleTwistControl[1] + '.' + twistType[twistLoop] + 'Twist_' + paddingSize, configure + '.'+ sideName + '_' + type + '_' + twistType[twistLoop] + 'Twist_' + paddingSize, f=1)

            twistPose               = twistPose + twistPoseIng

    #Twist curve bind joints       
    twistLocatorGroup               = cmds.group (em=1, n=side + '_' + type + '_' + 'Twist' + '_' + gv.group)
    cmds.setAttr (twistLocatorGroup + '.visibility', 0, l=1)
    cmds.parent (twistLocatorGroup, globalLimbJointGroup)  

    twistBindJoints                 = []
    twistControls                   = [upperTwistControl[0], middleTwistControl[0], lowerTwistControl[0]]       
    twistAttribute                  = [type + 'UpperTwist', type + 'MiddleTwist', type + 'LowerTwist']
    limbJoints                      = [upperJoints[0], lowerJoints[0], lowerJoints[-1]]

    twistLockLocator                = cmds.spaceLocator (p=[0, 0, 0], n=side + '_' + type + '_Twist_' + gv.locator)
    twistLockLocGroup               = cmds.group (em=1, n=side + '_' + type + '_Twist_' + gv.locator + '_' + gv.group)
    
    cmds.parent (twistLockLocator[0], twistLockLocGroup)
    generic.locatorSacle (twistLockLocator, 0.1, 1)
    generic.snapAction (blendJoints[0], twistLockLocGroup)
    cmds.parent (twistLockLocGroup, twistLocatorGroup)       

    cmds.select (cl=1)
    
    for twistBindLoop in range (0, 3, 1) : 
        cmds.select (cl=1)
        twistBindJoint              = cmds.joint (rad=gv.jntRadius, n=side + '_' + type + '_' + twistCtrlType[twistBindLoop] + 'Twist_' + gv.joint)
        twistBindJointGroup         = cmds.group (em=1, n=side + '_' + type + '_' + twistCtrlType[twistBindLoop] + 'Twist_' + gv.joint + '_' + gv.group)

        cmds.parent (twistBindJoint, twistBindJointGroup)           
    
        generic.snapAction (limbJoints[twistBindLoop], twistBindJointGroup)   
        cmds.makeIdentity (twistBindJoint, a=1, t=0, r=1, s=0, n=0)
        twistBindJoints.append (twistBindJoint)           
        cmds.parent (twistBindJointGroup, twistLocatorGroup)            
        cmds.select (cl=1)

        twistParentConst            = cmds.parentConstraint (twistControls[twistBindLoop], twistBindJointGroup, w=1, n=twistBindJointGroup + '_' + gv.parentConstraint)
        twistScaleConst             = cmds.scaleConstraint (twistControls[twistBindLoop], twistBindJointGroup, o=[1,1,1], w=1, n=twistBindJointGroup + '_' + gv.scaleConstraint)

        twistLocator                = cmds.spaceLocator (p=[0, 0, 0], n=side + '_' + type + '_' + twistCtrlType[twistBindLoop] + 'Twist_' + gv.locator)
        twistLocGroup               = cmds.group (em=1, n=side + '_' + type + '_' + twistCtrlType[twistBindLoop] + 'Twist_' + gv.locator + '_' + gv.group)

        cmds.parent (twistLocator[0], twistLocGroup)
        generic.locatorSacle (twistLocator, 0.1, 0)
        generic.snapAction (limbJoints[twistBindLoop], twistLocGroup)
        cmds.parent (twistLocGroup, twistLocatorGroup)

        twistLocConst               = cmds.parentConstraint (twistControls[twistBindLoop], twistLocator[0], w=1, n=twistLocator[0] + '_' + gv.parentConstraint)

        #Connect to configure node
        cmds.connectAttr (twistLocator[0] + '.rotateX', configure + '.' + sideName + twistAttribute[twistBindLoop], f=1)
    
    cmds.skinCluster (twistBindJoints, twistCurves[0], tsb=True, mi=1, dr=4.0, rui=0, normalizeWeights=1, obeyMaxInfluences=True, n=twistCurves[0] + '_SkinClu')
    cmds.skinCluster (twistBindJoints, twistCurves[1], tsb=True, mi=1, dr=4.0, rui=0, normalizeWeights=1, obeyMaxInfluences=True, n=twistCurves[1] + '_SkinClu')

    kneeParentConst                 = cmds.parentConstraint (middleKneeControl[0], middleTwistControl[3], w=1, n=middleTwistControl[3] + '_' + gv.parentConstraint)
    kneeScaleConst                  = cmds.scaleConstraint (middleKneeControl[0], middleTwistControl[3], o=[1,1,1], w=1, n=middleTwistControl[3] + '_' + gv.scaleConstraint)                           

    #Leg Middle Twist Position
    middlePointConst                = cmds.pointConstraint (blendJoints[0], blendJoints[1], blendJoints[2], middleKneeControl[3], o=[0, 0, 0], w=1, n=middleKneeControl[3] + '_' + gv.pointConstraint)
    cmds.setDrivenKeyframe (middlePointConst[0] + '.' + blendJoints[0] + 'W0', cd=configure + '.' + sideName + type + 'MiddleTwistPosition', itt='linear', ott='linear', dv=0, v=0)       
    cmds.setDrivenKeyframe (middlePointConst[0] + '.' + blendJoints[1] + 'W1', cd=configure + '.' + sideName + type + 'MiddleTwistPosition', itt='linear', ott='linear', dv=0, v=1)        
    cmds.setDrivenKeyframe (middlePointConst[0] + '.' + blendJoints[2] + 'W2', cd=configure + '.' + sideName + type + 'MiddleTwistPosition', itt='linear', ott='linear', dv=0, v=0)       

    cmds.setDrivenKeyframe (middlePointConst[0] + '.' + blendJoints[0] + 'W0', cd=configure + '.' + sideName + type + 'MiddleTwistPosition', itt='linear', ott='linear', dv=1, v=1)       
    cmds.setDrivenKeyframe (middlePointConst[0] + '.' + blendJoints[1] + 'W1', cd=configure + '.' + sideName + type + 'MiddleTwistPosition', itt='linear', ott='linear', dv=1, v=0)       
    cmds.setDrivenKeyframe (middlePointConst[0] + '.' + blendJoints[2] + 'W2', cd=configure + '.' + sideName + type + 'MiddleTwistPosition', itt='linear', ott='linear', dv=1, v=0)   

    cmds.setDrivenKeyframe (middlePointConst[0] + '.' + blendJoints[0] + 'W0', cd=configure + '.' + sideName + type + 'MiddleTwistPosition', itt='linear', ott='linear', dv=-1, v=0)       
    cmds.setDrivenKeyframe (middlePointConst[0] + '.' + blendJoints[1] + 'W1', cd=configure + '.' + sideName + type + 'MiddleTwistPosition', itt='linear', ott='linear', dv=-1, v=0)       
    cmds.setDrivenKeyframe (middlePointConst[0] + '.' + blendJoints[2] + 'W2', cd=configure + '.' + sideName + type + 'MiddleTwistPosition', itt='linear', ott='linear', dv=-1, v=1)

    #Connect to configure node
    cmds.addAttr (upperTwistControl[1], ln='twistFallOff', at='double', min=-1, max=1, dv=1, k=1)
    cmds.addAttr (middleTwistControl[1], ln='twistFallOff', at='double', min=-1, max=1, dv=1, k=1)
    cmds.addAttr (lowerTwistControl[1], ln='twistFallOff', at='double', min=-1, max=1, dv=1, k=1)       
    cmds.addAttr (middleKneeControl[1], ln='position', at='double', min=-1, max=1, dv=0, k=1)       

    cmds.connectAttr (upperTwistControl[1] + '.twistFallOff', configure + '.' + sideName + type + 'UpperTwistFallOff',  f=1)
    cmds.connectAttr (middleTwistControl[1] + '.twistFallOff', configure + '.' + sideName + type + 'MiddleTwistFallOff',  f=1)
    cmds.connectAttr (lowerTwistControl[1] + '.twistFallOff', configure + '.' + sideName + type + 'LowerTwistFallOff',  f=1)       
    cmds.connectAttr (middleKneeControl[1] + '.position', configure + '.' + sideName + type + 'MiddleTwistPosition',  f=1)
    
    cmds.undoInfo(closeChunk=1)
    
'''   
    
    
    
    
    
    
    
    
    
    
    
