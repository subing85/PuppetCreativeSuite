'''
QT StyleSheet v0.1 
Date : March 28, 2018
Last modified: March 28, 2018
Author: Subin. Gopi (subing85@gmail.com)

# Copyright (c) 2018, Subin Gopi
# All rights reserved.

# WARNING! All changes made in this file will be lost!

Description
    This module to set the style sheet to Qt ui
    
'''


class StyleSheet ():
    
    def __init__(self, window):            
        self.window = window  
    
    def setStyleSheet (self):
        setStyleSheets (self.window)        
    
    def getStyleSheet (self):        
        self._style = getStyleSheets ()        


def setStyleSheets (window) :
        
    style = getStyleSheets()    
    window.setStyleSheet(style)
    

def getStyleSheets () :
    
    groupBox = 'QGroupBox {font: 14pt \"MS Shell Dlg 2\"; border: 1px solid #FFAA00;}'        
    generic = 'QWidget {font: 10pt \"MS Shell Dlg 2\";}'   
    
    styleList = [groupBox, generic]    
    style = ''    
    
    for eachStyle in styleList :        
        style+='{} '.format (eachStyle)

    return style

#End########################################################################