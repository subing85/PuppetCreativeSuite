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
    twistAttribute = ['upperTwist', 'middleTwist', 'lowerTwist']   
    twistControlGroup.addAttr(twistAttribute[0], at='double', dv=0, k=1)
    twistControlGroup.addAttr(twistAttribute[2], at='double', dv=0, k=1)
    twistControlGroup.addAttr(twistAttribute[1], at='double', dv=0, k=1)
        
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
    twistControlGroup.connectAttr('middleTwistFallOff', '{}.input2X'.format(middleUpTwist_mdn), f=True)    
    twistControlGroup.connectAttr('middleTwistFallOff', '{}.input2X'.format(middleDnTwist_mdn), f=True)    
    twistControlGroup.connectAttr('lowerTwistFallOff', '{}.input2X'.format(lowerTwist_mdn), f=True)
    
    nullMiddle, shapeMiddle, offsetMiddle, groupMiddle = control.create(type='SmoothSphere', 
                                                                        name='{}_Middle'.format(type), side=side, 
                                                                        radius=radius/1.75, 
                                                                        orientation=orientation, 
                                                                        positionNode=dkJoints[1])    
    generic.lockHideAttributes(shapeMiddle, 'lockHide', ['rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'])
    groupMiddle.setParent (twistControlGroup) 

    upperTwist_mdsn = [upperTwist_mdn, middleUpTwist_mdn]
    lowerTwist_mdsn = [middleDnTwist_mdn, lowerTwist_mdn]

    upJoints = [dkJoints[0], dkJoints[1]]
    dnJoints = [dkJoints[1], dkJoints[2]]    
    twistType = ['UpperTwist', 'LowerTwist']
    twistJoints = [upperTwistJoints, lowerTwistJoints]    
    twistCurves = []
        
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
        twistCurves.append(twistCurve)
        
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
                                    wu=[0,1,0], 
                                    wuo=objectUpLocator, 
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
                                    n=aimConstraint
                                    )            
            
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
       
    twistLockLocator = generic.getNameStyle ([side, type, 'Twist_{}'.format (input._locator)])    
    generic.removeExistsNode([twistLockLocator])               
    twistLockLocator = pymel.spaceLocator (p=[0, 0, 0], n=twistLockLocator)

    twistLockLocatorGroup = generic.getNameStyle ([side, type, 'Twist_{}_{}'.format(input._locator, input._group)])    
    generic.removeExistsNode([twistLockLocatorGroup])       
    twistLockLocatorGroup = generic.createGroup(None, twistLockLocatorGroup)    
    twistLockLocator.setParent(twistLockLocatorGroup)
    
    generic.snap(dkJoints[0], twistLockLocatorGroup) 
    twistLockLocatorGroup.setParent(twistDeformGroup)
    
    twistBindJoints = []
    twistControls = [shapeUpperTwist, shapeMiddleTwist, shapeLowerTwist]       
    limbJoints = [upperTwistJoints[0], lowerTwistJoints[0], lowerTwistJoints[-1]]     
    #twistAttribute = ['{}UpperTwist'.format(type), '{}MiddleTwist'.format(type),  '{}LowerTwist'.format(type)]        
    twistCtrlType = ['Upper', 'Middle', 'Lower']
    
    for bindIndex in range (3):
        pymel.select (cl=1)    
        
        twistBindJointGroup = generic.getNameStyle ([side, type, '{}_Twist_{}_{}'.format (twistCtrlType[bindIndex], input._joint, input._group)])         
        generic.removeExistsNode([twistBindJointGroup])       
        twistBindJointGroup = generic.createGroup(None, twistBindJointGroup)    
        twistBindJointGroup.setParent(twistDeformGroup)                       
            
        twistBindJoint = generic.getNameStyle ([side, type, '{}_Twist_{}'.format (twistCtrlType[bindIndex], input._joint)]) 
        generic.removeExistsNode([twistBindJoint]) 
        twistJoint = pymel.joint (rad=input._jointRadius, n=twistBindJoint)        
        twistJoint.setParent(twistBindJointGroup)
        twistBindJoints.append (twistBindJoint)             
        generic.snap(limbJoints[bindIndex], twistBindJointGroup) 
        
        pymel.makeIdentity (twistBindJoint, a=1, t=0, r=1, s=0, n=0)        
        
        parentConstraint = generic.getNameStyle ([side, type, '{}_Twist_{}_{}_{}'.format (twistCtrlType[bindIndex], input._joint, input._group, input._parentConstraint)])         
        scaleConstraint = generic.getNameStyle ([side, type, '{}_Twist_{}_{}_{}'.format (twistCtrlType[bindIndex], input._joint, input._group, input._scaleConstraint)])         
        generic.removeExistsNode([parentConstraint, scaleConstraint]) 
        pymel.parentConstraint (twistControls[bindIndex], twistBindJointGroup, w=1, n=parentConstraint)
        pymel.scaleConstraint (twistControls[bindIndex], twistBindJointGroup, o=[1,1,1], w=1, n=scaleConstraint)

        twistLocGroup = generic.getNameStyle ([side, type, '{}_Twist_{}_{}'.format(twistCtrlType[bindIndex], input._locator, input._group)])    
        generic.removeExistsNode([twistLocGroup])       
        twistLocGroup = generic.createGroup(None, twistLocGroup)    

        twistLocator = generic.getNameStyle ([side, type, '{}_Twist_{}'.format(twistCtrlType[bindIndex], input._locator)])    
        generic.removeExistsNode([twistLocator])               
        twistLocator = pymel.spaceLocator (p=[0, 0, 0], n=twistLocator)
        twistLocator.setParent(twistLocGroup)    
        ##generic.snap(limbJoints[bindIndex], twistLocGroup) 
        generic.snap(twistControls[bindIndex], twistLocGroup)        

        twistLocConst = generic.getNameStyle ([side, type, '{}_Twist_{}_{}'.format(twistCtrlType[bindIndex], input._locator, input._parentConstraint)])         
        pymel.parentConstraint (twistControls[bindIndex], twistLocator, w=1, n=twistLocConst)
        
        twistLocator.connectAttr('rotateX', '{}.{}'.format(twistControlGroup, twistAttribute[bindIndex]), f=True)
        
    upperCurveskincluster = generic.getNameStyle ([side, type, '{}_{}_{}'.format (twistType[0], input._curve, input._skinCluster)])
    generic.removeExistsNode([upperCurveskincluster])   
    pymel.skinCluster(twistBindJoints, twistCurves[0], tsb=True, mi=1, dr=4.0, rui=0, normalizeWeights=1, obeyMaxInfluences=True, n=upperCurveskincluster)
    
    lowerCurveskincluster = generic.getNameStyle ([side, type, '{}_{}_{}'.format (twistType[1], input._curve, input._skinCluster)])
    generic.removeExistsNode([lowerCurveskincluster])     
    pymel.skinCluster(twistBindJoints, twistCurves[1], tsb=True, mi=1, dr=4.0, rui=0, normalizeWeights=1, obeyMaxInfluences=True, n=lowerCurveskincluster)
    
    kneeParentConst = generic.getNameStyle ([side, type, 'MiddleTwist_{}_{}_{}'.format(input._control, input._group, input._parentConstraint)])    
    kneeScaleConst = generic.getNameStyle ([side, type, 'MiddleTwist_{}_{}_{}'.format(input._control, input._group, input._scaleConstraint)])    
    middlePointConst = generic.getNameStyle ([side, 'Middle', '{}_{}_{}_{}'.format(type, input._control, input._group, input._pointConstraint)])    
     
    pymel.parentConstraint(nullMiddle, groupMiddleTwist, w=True, n=kneeParentConst)
    pymel.scaleConstraint(nullMiddle, groupMiddleTwist, w=True, o=[1,1,1], n=kneeScaleConst)    
    middlePointConst = pymel.pointConstraint (dkJoints[0], dkJoints[1], dkJoints[2], groupMiddle, o=[0, 0, 0], w=1, n=middlePointConst)
    
    pymel.setDrivenKeyframe('{}.{}W0'.format(middlePointConst, dkJoints[0]), 
                            cd='{}.middleTwistPosition'.format(twistControlGroup),
                            itt='linear', ott='linear', dv=-1, v=1)
       
    pymel.setDrivenKeyframe('{}.{}W1'.format(middlePointConst, dkJoints[1]), 
                            cd='{}.middleTwistPosition'.format(twistControlGroup),
                            itt='linear', ott='linear', dv=-1, v=0)    
    
    pymel.setDrivenKeyframe('{}.{}W2'.format(middlePointConst, dkJoints[2]), 
                            cd='{}.middleTwistPosition'.format(twistControlGroup),
                            itt='linear', ott='linear', dv=-1, v=0)    
    
    pymel.setDrivenKeyframe('{}.{}W0'.format(middlePointConst, dkJoints[0]), 
                            cd='{}.middleTwistPosition'.format(twistControlGroup),
                            itt='linear', ott='linear', dv=0, v=0)
    
    pymel.setDrivenKeyframe('{}.{}W1'.format(middlePointConst, dkJoints[1]), 
                            cd='{}.middleTwistPosition'.format(twistControlGroup),
                            itt='linear', ott='linear', dv=0, v=1)    
    
    pymel.setDrivenKeyframe('{}.{}W2'.format(middlePointConst, dkJoints[2]), 
                            cd='{}.middleTwistPosition'.format(twistControlGroup),
                            itt='linear', ott='linear', dv=0, v=0)    
    
    pymel.setDrivenKeyframe('{}.{}W0'.format(middlePointConst, dkJoints[0]), 
                            cd='{}.middleTwistPosition'.format(twistControlGroup),
                            itt='linear', ott='linear', dv=1, v=0)
    
    pymel.setDrivenKeyframe('{}.{}W1'.format(middlePointConst, dkJoints[1]), 
                            cd='{}.middleTwistPosition'.format(twistControlGroup),
                            itt='linear', ott='linear', dv=1, v=0)    
    
    pymel.setDrivenKeyframe('{}.{}W2'.format(middlePointConst, dkJoints[2]), 
                            cd='{}.middleTwistPosition'.format(twistControlGroup),
                            itt='linear', ott='linear', dv=1, v=1)         
    
    shapeUpperTwist.addAttr('twistFallOff', at='double', min=-1, max=1, dv=1, k=True)
    shapeMiddleTwist.addAttr('twistFallOff', at='double', min=-1, max=1, dv=1, k=True)
    shapeLowerTwist.addAttr('twistFallOff', at='double', min=-1, max=1, dv=1, k=True)
    shapeMiddle.addAttr('position', at='double', min=-1, max=1, dv=0, k=True)   
   
    shapeUpperTwist.connectAttr('twistFallOff', '{}.upperTwistFallOff'.format(twistControlGroup), f=True)    
    shapeMiddleTwist.connectAttr('twistFallOff', '{}.middleTwistFallOff'.format(twistControlGroup), f=True)    
    shapeLowerTwist.connectAttr('twistFallOff', '{}.lowerTwistFallOff'.format(twistControlGroup), f=True)
    shapeMiddle.connectAttr('position', '{}.middleTwistPosition'.format(twistControlGroup), f=True)    

    pymel.undoInfo(closeChunk=1)
    return twistControlGroup   

#End ############################################################################################################
