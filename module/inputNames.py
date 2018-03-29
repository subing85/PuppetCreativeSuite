'''
Name Inputs v0.1
Date : March 26, 2018
Last modified: March 26, 2018
Author: Subin. Gopi (subing85@gmail.com)

# Copyright (c) 2018, Subin Gopi
# All rights reserved.

# WARNING! All changes made in this file will be lost!

Description
    This module can provide the name attributes for Rig 
 
example   
    from module.blender import nameInputs            
    input = nameInputs.Inputs()
'''


class Inputs (object) :
    def __init__(self) :        

        #Global variables
        self._configure = 'Configure'
        self._globalScale = 'GlobalScale'
        self._globals = 'Global'
        
        self._jntRadius = 0.1
                
        self._cog = 'Cog'
        self._spine = 'Spine'
        self._chest = 'Chest'        
        self._neck = 'Neck'
        self._head = 'Head'        
        
        self._leg = 'Leg'
        self._legFinger = 'LegFinger'  
                      
        self._pelvis = 'Pelvis'
        self._hip = 'Hip'
        self._knee = 'Knee'
        self._ankle = 'Ankle'
        self._legPoleVector = 'LegPoleVector'
        
        self._foot = 'Foot'         
        self._ball = 'Ball'
        self._toe = 'Toe'
        self._heel = 'Heel'
        self._pinkyToe = 'PinkyToe'
        self._bigToe = 'BigToe'            

        self._arm = 'Arm'
        self._armFinger = 'ArmFinger'

        self._clavicle = 'Clavicle'
        self._shoulder = 'Shoulder'
        self._elbow = 'Elbow'
        self._wrist = 'Wrist'
        self._armPoleVector = 'ArmPoleVector' 
        self._thumb = 'Thumb'
        self._index = 'Index'
        self._middle = 'Middle'
        self._ring = 'Ring'        
        self._pinky = 'PinkyRoot' 

        self._upperJaw = 'UpperJaw'
        self._lowerJaw = 'LowerJaw'     

        self._eyeRoot = 'EyeRoot'
        self._eye = 'Eye'
        self._eyeAim = 'EyeAim'
        self._upperEyeBrow = 'UpperEyeBrow'
        self._lowerEyeBrow = 'LowerEyeBrow'       
        
        self._tongue = 'Tongue'
        self._ear = 'Ear' 
        self._uvula = 'Uvula'
        self._tail = 'Tail'   
        self._earD = 'EarD'  

        self._characterName = 'Generic'        
        self._joint = 'Jnt'
        self._fitJoint = 'FJnt'
        self._twist = 'Twist'
        self._leftSide = 'LT'
        self._rightSide = 'RT'
        self._centerSide = 'CT'
        self._frontSide = 'FR'
        self._backSide = 'BK' 

        self._ik = 'IK'
        self._fk = 'FK'
        self._bind = 'Bind'
        self._blend = 'Blend'       

        self._configureJoint = 'ConfigureJoint'       

        #General Utilities
        self._blendColor = 'BC'
        self._reverse = 'RV'
        self._multiplyDivide = 'MD'
        self._plusMinusAverage = 'PM'
        self._clamp = 'CP'
        self._distanceBetween = 'DB'
        self._pointOnCurveInfo = 'PC'       

        self._group = 'Group'
        self._offset = 'Offset'
        self._null = 'Null'
        self._control = 'Ctrl'
        self._sdk = 'SDK'
        self._locator = 'Loc'
        self._curve = 'Crv'   
        self._deform = 'Deform'  

        self._pointConstraint = 'PointConstraint' 
        self._orientConstraint = 'OrientConstraint'
        self._aimConstraint = 'AimConstraint' 
        self._parentConstraint = 'ParentConstraint'
        self._scaleConstraint = 'ScaleConstraint'
        self._poleVectorConstraint = 'PoleVectorConstraint'      

        self._ikHandle = 'IKHandle'
        self._effector = 'IKEffector'             

        self._hierarchyAppend = {'World': { '1_Control': ['Offset', 'Controls'], 
                                            '2_Geometry': ['Layout', 'Animation', 'Render'],
                                            '3_Skeleton': ['FitSkeleton'],
                                            '4_Deformer': [],
                                            '5_Global': [],                                            
                                            }
                                 }
