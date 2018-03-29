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

NAME = 'Template'
ORDER = 1
MODULE_TYPE = 'Fit Skeleton'
TYPE = 'validate'
DATE = 'March 29, 2018'
AUTHOR = 'Subin Gopi'
COMMENTS = 'To Generate Template Skeleton'
VERSION = 1.0
CLASS = 'Template'


from pymel import core as pymel

class Template (object):
    
    def __init__(self):     
        pass
    
    
    def createSkeleton(self):        
        print 'Template skeleton module'
    
    
    def removeSkeleton(self):
        pass
    
    
    def resetSkeleton(self):
        pass
    
    
    def hasExists (self):
        pass


    
        


