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

import os

from pymel import core as pymel

from module import inputNames
from module import openGeneric
from resources import skeletonList

reload(inputNames)
reload(openGeneric)
reload(skeletonList)


class Biped (object):
    
    def __init__(self):
        
        self.input = inputNames.Names()
        self.generic = openGeneric.Generic()
        
        self.nameStyle = self.input._nameStyle
        self.jointRadius = self.input._jointRadius  
        
        skeleton = skeletonList.Skeleton()
        self.joints = skeleton.bipedJoints     

    
    def createSkeleton(self):
        
        '''
        Description
            Function for create the skleton for Bipe puppet, only in left side                     
            :Type - class function (method)            
            :param     None
            :return    None
        '''
        
        self.removeSkeleton ()        
        soucePath = os.path.abspath(os.path.join (os.environ['PUPPETCS_PATH'], 'fitSkeletons/bipedSkeleton.mel')).replace('\\', '/')
        pymel.mel.eval('source \"%s\";'%  soucePath)
        pymel.select (cl=True)  
        print 'create skeleton successfully done.'            


    def removeSkeleton(self):   
                 
        for eachJoint in self.joints:
            if not pymel.objExists (eachJoint):
                continue
            try :
                pymel.delete (eachJoint)
            except Exception as result:
                print result            
        
        print 'remove exists skeleton successfully done.'            

    
    def resetSkeleton(self):
        self.createSkeleton()
        print 'reset skeleton successfully done.'            
    
    
    def hasExists(self):
        
        result = {}
        
        for eachJoint in self.joints:
            if not pymel.objExists (eachJoint):
                result.setdefault(False, []).append(eachJoint)                
            else:
                result.setdefault(True, []).append(eachJoint)
                
        return result  
    
#End###################################################################################################    