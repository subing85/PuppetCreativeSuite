'''
IK Strech for Puppet Creative Suite v1.0.0
Date : April 10, 2018
Last modified: April 10, 2018
Author: Subin. Gopi (subing85@gmail.com)

# Copyright (c) 2018, Subin Gopi
# All rights reserved.

# WARNING! All changes made in this file will be lost!

Description
    Module for ik strech
 
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

def iKStretch (side, type, ikJoints, ikHandle, poleVector, strechAxis, value):
    
    #pymel.undoInfo(openChunk=1)      
    generic = openGeneric.Generic()     
    input = inputNames.Names()  
       
    upperStartLoc, upperEndLoc, upperDistance, upperDistanceDim = generic.createDistanceDimension(side, '{}_UpperStrech'.format (type), ikJoints[0], poleVector)
    lowerStartLoc, lowerEndLoc, lowerDistance, lowerDistanceDim = generic.createDistanceDimension(side, '{}_LowerStrech'.format (type), poleVector, ikHandle)    
    middleStartLoc, middleEndLoc, middleDistance, middleDistanceDim = generic.createDistanceDimension(side, '{}Strech'.format (type), ikJoints[0], ikHandle)

    strechGroup = generic.getNameStyle ([side, type, 'Strech_{}'.format(input._group)])     
    upperStrechGroup = generic.getNameStyle ([side, type, 'UpperStrech_{}'.format(input._group)]) 
    lowerStrechGroup = generic.getNameStyle ([side, type, 'LowerStrech_{}'.format(input._group)]) 
    middleStrechGroup = generic.getNameStyle ([side, type, 'MiddleStrech_{}'.format(input._group)]) 

    generic.removeExistsNode([strechGroup, upperStrechGroup, lowerStrechGroup, middleStrechGroup])
              
    strechGroup = generic.createGroup(None, strechGroup)
    upperStrechGroup = generic.createGroup(None, upperStrechGroup)
    lowerStrechGroup = generic.createGroup(None, lowerStrechGroup)    
    middleStrechGroup = generic.createGroup(None, middleStrechGroup)    
    
    pymel.parent (upperStartLoc, upperEndLoc, upperDistance, upperStrechGroup)
    pymel.parent (lowerStartLoc, lowerEndLoc, lowerDistance, lowerStrechGroup)
    pymel.parent (middleStartLoc, middleEndLoc, middleDistance, middleStrechGroup)
    
    pymel.parent (lowerStrechGroup, upperStrechGroup, middleStrechGroup, strechGroup)
    
    upperLength = ikJoints[1].getAttr(strechAxis)
    lowerLength = ikJoints[2].getAttr(strechAxis)    
    
    #Strech Connections
    upperStrech_blendColor = generic.getNameStyle ([side, type, 'UpperStrech_{}'.format (input._blendColor)])             
    lowerStrech_blendColor = generic.getNameStyle ([side, type, 'LowerStrech_{}'.format (input._blendColor)])             
    strech_mdn = generic.getNameStyle ([side, type, 'Strech_{}'.format (input._multiplyDivide)])
    strech_cp = generic.getNameStyle ([side, type, 'Strech_{}'.format (input._clamp)])
    scaleStrech_mdn = generic.getNameStyle ([side, type, 'ScaleStrech_{}'.format (input._multiplyDivide)]) 
    strech_pma = generic.getNameStyle ([side, type, 'Strech_{}'.format (input._plusMinusAverage)])
    lowerStrech_pma = generic.getNameStyle ([side, type, 'LowerStrech_{}'.format (input._plusMinusAverage)])
    upperStrech_pma = generic.getNameStyle ([side, type, 'UpperStrech_{}'.format (input._plusMinusAverage)])
    offestStrech_mdn = generic.getNameStyle ([side, type, 'OffestStrech_{}'.format (input._multiplyDivide)])
    switchStrech_pma = generic.getNameStyle ([side, type, 'SwitchStrech_{}'.format (input._plusMinusAverage)])
    switchStrech_mdn = generic.getNameStyle ([side, type, 'SwitchStrech_{}'.format (input._multiplyDivide)])
    autoSwitchStrech_mdn = generic.getNameStyle ([side, type, 'AutoSwitchStrech_{}'.format (input._multiplyDivide)])
    sacleDistSwitchStrech_mdn = generic.getNameStyle ([side, type, 'SacleDistStrech_{}'.format (input._multiplyDivide)])
    kneeStrech_mdn = generic.getNameStyle ([side, type, 'KneeStrech_{}'.format (input._multiplyDivide)])
    strechOffset_mdn = generic.getNameStyle ([side, type, 'Strech_Offset_{}'.format (input._multiplyDivide)])
    kneeStrechOffset_mdn = generic.getNameStyle ([side, type, 'KneeStrech_Offset_{}'.format (input._multiplyDivide)])
    
    generic.removeExistsNode([  upperStrech_blendColor,
                                lowerStrech_blendColor,
                                strech_mdn,
                                strech_cp,
                                scaleStrech_mdn,
                                strech_pma,
                                lowerStrech_pma,
                                upperStrech_pma,
                                offestStrech_mdn,
                                switchStrech_pma,
                                switchStrech_mdn,
                                autoSwitchStrech_mdn,
                                sacleDistSwitchStrech_mdn,
                                kneeStrech_mdn,
                                strechOffset_mdn,
                                kneeStrechOffset_mdn])
                                   
    upperStrech_blendColor = pymel.shadingNode ('blendColors', asUtility=1, n=upperStrech_blendColor)    
    lowerStrech_blendColor = pymel.shadingNode ('blendColors', asUtility=1, n=lowerStrech_blendColor)    
    strech_mdn = pymel.shadingNode ('multiplyDivide', asUtility=1, n=strech_mdn)
    strech_cp = pymel.shadingNode ('clamp', asUtility=1, n=strech_cp)
    scaleStrech_mdn = pymel.shadingNode ('multiplyDivide', asUtility=1, n=scaleStrech_mdn)
    strech_pma = pymel.shadingNode ('plusMinusAverage', asUtility=1, n=strech_pma)
    lowerStrech_pma = pymel.shadingNode ('plusMinusAverage', asUtility=1, n=lowerStrech_pma)
    upperStrech_pma = pymel.shadingNode ('plusMinusAverage', asUtility=1, n=upperStrech_pma)
    offestStrech_mdn = pymel.shadingNode ('multiplyDivide', asUtility=1, n=offestStrech_mdn)    
    switchStrech_pma = pymel.shadingNode ('plusMinusAverage', asUtility=1, n=switchStrech_pma)
    switchStrech_mdn = pymel.shadingNode ('multiplyDivide', asUtility=1, n=switchStrech_mdn)
    autoSwitchStrech_mdn = pymel.shadingNode ('multiplyDivide', asUtility=1, n=autoSwitchStrech_mdn)
    sacleDistSwitchStrech_mdn = pymel.shadingNode ('multiplyDivide', asUtility=1, n=sacleDistSwitchStrech_mdn)
    kneeStrech_mdn = pymel.shadingNode ('multiplyDivide', asUtility=1, n=kneeStrech_mdn)
    strechOffset_mdn = pymel.shadingNode ('multiplyDivide', asUtility=1, n=strechOffset_mdn)
    kneeStrechOffset_mdn = pymel.shadingNode ('multiplyDivide', asUtility=1, n=kneeStrechOffset_mdn)    
    
    strech_mdn.setAttr('operation', 1, k=True)
    strech_cp.setAttr('minR', 1)
    scaleStrech_mdn.setAttr('operation', 2, k=True)
    strech_pma.setAttr('operation', 1, k=True)
    lowerStrech_pma.setAttr('operation', 1, k=True)
    lowerStrech_pma.setAttr('input1D[1]', lowerLength)
    upperStrech_pma.setAttr('operation', 1, k=True)    
    upperStrech_pma.setAttr('input1D[1]', upperLength)            
    offestStrech_mdn.setAttr('operation', 1, k=True)    
    offestStrech_mdn.setAttr('input2X', upperLength)    
    offestStrech_mdn.setAttr('input2Y', lowerLength)    
    switchStrech_pma.setAttr('operation', 1, k=True)  
       
    switchStrech_mdn.setAttr('operation', 2, k=True)
    switchStrech_mdn.setAttr('input2X', 10)
    switchStrech_mdn.setAttr('input2Y', 10)
    switchStrech_mdn.setAttr('input2Z', 10)
    
    autoSwitchStrech_mdn.setAttr('operation', 1, k=True)
    sacleDistSwitchStrech_mdn.setAttr('operation', 2, k=True)
    kneeStrech_mdn.setAttr('operation', 2, k=True)   
    strechOffset_mdn.setAttr('operation', 1, k=True)
    strechOffset_mdn.setAttr('input2X', value)
    strechOffset_mdn.setAttr('input2Y', value)
    strechOffset_mdn.setAttr('input2Z', value)
    
    kneeStrechOffset_mdn.setAttr('operation', 1, k=True)
    kneeStrechOffset_mdn.setAttr('input2X', value)
    kneeStrechOffset_mdn.setAttr('input2Y', value)
    kneeStrechOffset_mdn.setAttr('input2Z', value)     
    
    strechGroup.addAttr('switchStretch',  at='double', dv=0, k=True) 
    strechGroup.addAttr('lengthStrech',  at='double', dv=0, k=True) 
    strechGroup.addAttr('upperStretch',  at='double', dv=0, k=True) 
    strechGroup.addAttr('lowerStretch',  at='double', dv=0, k=True) 
    strechGroup.addAttr('stretch',  at='double', dv=0, k=True) 
    strechGroup.addAttr('kneeLock',  at='double', dv=0, k=True)     

    upperStrech_blendColor.connectAttr('outputR', '{}.{}'.format(ikJoints[1], strechAxis), f=True)
    lowerStrech_blendColor.connectAttr('outputR', '{}.{}'.format(ikJoints[2], strechAxis), f=True)         
    strech_mdn.connectAttr('outputY', '{}.color2R'.format(lowerStrech_blendColor), f=True)        
    kneeStrech_mdn.connectAttr('outputY', '{}.color1R'.format(lowerStrech_blendColor), f=True)    
    strechGroup.connectAttr('kneeLock', '{}.blender'.format(lowerStrech_blendColor), f=True)    
    strech_mdn.connectAttr('outputX', '{}.color2R'.format(upperStrech_blendColor), f=True)     
       
    kneeStrech_mdn.connectAttr('outputX', '{}.color1R'.format(upperStrech_blendColor), f=True)     
    strechGroup.connectAttr('kneeLock', '{}.blender'.format(upperStrech_blendColor), f=True) 
    strech_cp.connectAttr('outputR', '{}.input2X'.format(strech_mdn), f=True)    
    strech_cp.connectAttr('outputR', '{}.input2Y'.format(strech_mdn), f=True)  
      
    upperStrech_pma.connectAttr('output1D', '{}.input1X'.format(strech_mdn), f=True)    
    lowerStrech_pma.connectAttr('output1D', '{}.input1Y'.format(strech_mdn), f=True)
    scaleStrech_mdn.connectAttr('outputX', '{}.input1X'.format(strechOffset_mdn), f=True)    
    strechOffset_mdn.connectAttr('outputX', '{}.inputR'.format(strech_cp), f=True)
    
    strechGroup.connectAttr('lengthStrech', '{}.maxR'.format(strech_cp), f=True) 
    autoSwitchStrech_mdn.connectAttr('outputX', '{}.input1X'.format(scaleStrech_mdn), f=True)    
    strech_pma.connectAttr('output1D', '{}.input2X'.format(scaleStrech_mdn), f=True)   
            
    upperStrech_pma.connectAttr('output1D', '{}.input1D[1]'.format(strech_pma), f=True)    
    lowerStrech_pma.connectAttr('output1D', '{}.input1D[0]'.format(strech_pma), f=True)
    
    offestStrech_mdn.connectAttr('outputX', '{}.input1D[0]'.format(upperStrech_pma), f=True)    
    offestStrech_mdn.connectAttr('outputY', '{}.input1D[0]'.format(lowerStrech_pma), f=True)      
    switchStrech_pma.connectAttr('output2Dx', '{}.input1X'.format(offestStrech_mdn), f=True)    
    switchStrech_pma.connectAttr('output2Dy', '{}.input1Y'.format(offestStrech_mdn), f=True)
    
    switchStrech_mdn.connectAttr('outputY', '{}.input2D[1].input2Dx'.format(switchStrech_pma), f=True)    
    switchStrech_mdn.connectAttr('outputZ', '{}.input2D[1].input2Dy'.format(switchStrech_pma), f=True)
    switchStrech_mdn.connectAttr('outputX', '{}.input2D[0].input2Dx'.format(switchStrech_pma), f=True)        
    switchStrech_mdn.connectAttr('outputX', '{}.input2D[0].input2Dy'.format(switchStrech_pma), f=True)   
         
    strechGroup.connectAttr('stretch', '{}.input1X'.format(switchStrech_mdn), f=True)    
    strechGroup.connectAttr('upperStretch', '{}.input1Y'.format(switchStrech_mdn), f=True)    
    strechGroup.connectAttr('lowerStretch', '{}.input1Z'.format(switchStrech_mdn), f=True)    
    
    strechGroup.connectAttr('switchStretch', '{}.input2X'.format(autoSwitchStrech_mdn), f=True)    
    sacleDistSwitchStrech_mdn.connectAttr('outputX', '{}.input1X'.format(autoSwitchStrech_mdn), f=True)  
        
    strechGroup.connectAttr('scaleX', '{}.input1X'.format(kneeStrechOffset_mdn), f=True)
    strechGroup.connectAttr('scaleX', '{}.input1Y'.format(kneeStrechOffset_mdn), f=True)
    strechGroup.connectAttr('scaleX', '{}.input2X'.format(sacleDistSwitchStrech_mdn), f=True)
    
    kneeStrechOffset_mdn.connectAttr('outputX', '{}.input2X'.format(kneeStrech_mdn), f=True)
    kneeStrechOffset_mdn.connectAttr('outputY', '{}.input2Y'.format(kneeStrech_mdn), f=True)   
      
    upperDistanceDim.connectAttr('distance', '{}.input1X'.format(kneeStrech_mdn), f=True)
    lowerDistanceDim.connectAttr('distance', '{}.input1Y'.format(kneeStrech_mdn), f=True)
    middleDistanceDim.connectAttr('distance', '{}.input1X'.format(sacleDistSwitchStrech_mdn), f=True)
    
    strechGroup.setAttr ('v', 0, l=True)
    
    return strechGroup 
                 


    
    
    