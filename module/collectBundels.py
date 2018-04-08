'''
Bundles Modules v0.1
Date : March 28, 2018
Last modified: March 28, 2018
Author: Subin. Gopi (subing85@gmail.com)

# Copyright (c) 2018, Subin Gopi
# All rights reserved.

# WARNING! All changes made in this file will be lost!

Description
    This module manage to the all kind of Bundles for validate and extractor.    

'''

import os
import sys
import warnings
import pkgutil
import inspect
import py_compile
import pprint


class Bundles (object) :
    
    def __init__(self, path=None, moduleType=None, bundelType=None) :
        
        if not path:
            warnings.warn ('class \"Bundles\" argument \"path\" None or emty')        
                        
        if not moduleType:   
            warnings.warn ('class \"Bundles\" argument \"moduleType\" None or emty')                    
            
        if not bundelType:
            warnings.warn ('class \"Bundles\" argument \"bundelType\" None or emty')
            
        self._bundlePath = path                     
        self._moduleType = moduleType 
        self._bundleType = bundelType  
        
   
    def getValidBundles (self) :  
                
        bundles = collectBundles (self._bundlePath, self._moduleType, self._bundleType)        
        return bundles


def collectBundles (path, moduleType, bundleType):
    
    if not path :
        warnings.warn ('Function \"getBundles\" argument \"path\" None or emty')
        
    if not os.path.isdir(path) :
        warnings.warn ('{} - No such directory'.format(path))
  
    bundleData = {}        
 
    for module_loader, name, ispkg in pkgutil.iter_modules([path]) :                       
        loader = module_loader.find_module(name)    
        
          
        module = loader.load_module (name)
        
        if not hasattr(module, 'TYPE') :
            continue
        
        if not hasattr(module, 'MODULE_TYPE') :
            continue         
         
        if module.MODULE_TYPE!=moduleType:
            continue  
                     
        if module.TYPE!=bundleType:
            continue  
        
        if module.TYPE=='None':
            continue 
                    
        moduleMembers = {}                
        for moduleName, value in inspect.getmembers (module) :           
            moduleMembers.setdefault (moduleName, value)    
       
        bundleData.setdefault (module, moduleMembers)        
       
    return bundleData


def reorder (data, key) :
    
    result = {}
    ing = 0
    for eachKey, eachValue in data.items () :   
            
        if eachValue[key] :       
            ing = eachValue[key] 
                  
        if not eachValue[key] :           
            ing+=1
                   
        if eachValue[key] in result :
            ing = eachValue[key] + 1                 
               
        result.setdefault(ing, eachKey)
       
    return result  

#End############################################################################