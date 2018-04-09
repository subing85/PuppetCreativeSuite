'''
Open Control v1.0.0
Date : April 09, 2018
Last modified: April 09, 2018
Author: Subin. Gopi (subing85@gmail.com)

# Copyright (c) 2018, Subin Gopi
# All rights reserved.

# WARNING! All changes made in this file will be lost!

Description
    This module includes control shape for maya
 
'''

import warnings

from pymel import core as pymel

from module import openGeneric
from module import inputNames

reload(openGeneric)
reload(inputNames)


class Controls(object):
    
    def __init__(self):
        
        self.input = inputNames.Names()
            
    
    def create(self, type=None, name=None, side=None, radius=None, orientation=[0,0,0], positionNode=None):

        currentControl = None
    
        if type=='Circle' :
            currentControl = pymel.circle(c=(0, 0, 0), nr=(1, 0, 0), sw=360,  r=1, d=3, ut=0, tol=0.01, s=8, ch=0)[0]
    
        if type=='FootSqure' :
            currentControl = pymel.mel.eval ('curve -d 1 -p -0.666157 0 -1.306548 -p -0.986307 0 1.306548 -p 0.986307 0 1.306548 -p 0.442043 0 -1.306548 -p -0.666157 0 -1.306548 -k 0 -k 1 -k 2 -k 3 -k 4 ;')
      
        if type=='Pyramid' :
            currentControl = pymel.mel.eval ('curve -d 1 -p -4.38902e-008 -5.81842e-008 1.004092 -p 1.004092 1.42041e-009 0 -p 0 1.369416 0 -p -4.38902e-008 -5.81842e-008 1.004092 -p -1.004092 1.42041e-009 -8.77805e-008 -p 0 1.369416 0 -p 1.004092 1.42041e-009 0 -p 1.31671e-007 1.42041e-009 -1.004092 -p -1.004092 1.42041e-009 -8.77805e-008 -p 0 1.369416 0 -p 1.31671e-007 1.42041e-009 -1.004092 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 ;')
               
        if type=='ArrowSinglePin' :
            currentControl = pymel.mel.eval ('curve -d 1 -p 0 0 0 -p 0 0 0.626368 -p 0 0 1 -p 0 0.150969 0.626368 -p 0 0 0.626368 -p 0 -0.150969 0.626368 -p 0 0 1 -p 0.150969 0 0.626368 -p 0 0 0.626368 -p -0.150969 0 0.626368 -p 0 0 1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 ;')
       
        if type=='SmoothSphere' :
            currentControl =  pymel.mel.eval ('curve -d 1 -p 0 1.001829 0 -p 0 0.996341 0.10472 -p 0 0.979937 0.208292 -p 0 0.952796 0.309582 -p 0 0.915217 0.407481 -p 0 0.86761 0.500915 -p 0 0.810497 0.588861 -p 0 0.744504 0.670355 -p 0 0.670355 0.744504 -p 0 0.588861 0.810497 -p 0 0.500915 0.86761 -p 0 0.407481 0.915217 -p 0 0.309582 0.952796 -p 0 0.208292 0.979937 -p 0 0.10472 0.996341 -p 0 0 1.001829 -p 0 -0.10472 0.996341 -p 0 -0.208292 0.979937 -p 0 -0.309582 0.952796 -p 0 -0.407481 0.915217 -p 0 -0.500915 0.86761 -p 0 -0.588861 0.810497 -p 0 -0.670355 0.744504 -p 0 -0.744504 0.670355 -p 0 -0.810497 0.588861 -p 0 -0.86761 0.500915 -p 0 -0.915217 0.407481 -p 0 -0.952796 0.309582 -p 0 -0.979937 0.208292 -p 0 -0.996341 0.10472 -p 0 -1.001829 0 -p 0 -0.996341 -0.10472 -p 0 -0.979937 -0.208292 -p 0 -0.952796 -0.309582 -p 0 -0.915217 -0.407481 -p 0 -0.86761 -0.500915 -p 0 -0.810497 -0.588861 -p 0 -0.744504 -0.670355 -p 0 -0.670355 -0.744504 -p 0 -0.588861 -0.810497 -p 0 -0.500915 -0.86761 -p 0 -0.407481 -0.915217 -p 0 -0.309582 -0.952796 -p 0 -0.208292 -0.979937 -p 0 -0.10472 -0.996341 -p 0 0 -1.001829 -p 0 0.10472 -0.996341 -p 0 0.208292 -0.979937 -p 0 0.309582 -0.952796 -p 0 0.407481 -0.915217 -p 0 0.500915 -0.86761 -p 0 0.588861 -0.810497 -p 0 0.670355 -0.744504 -p 0 0.744504 -0.670355 -p 0 0.810497 -0.588861 -p 0 0.86761 -0.500915 -p 0 0.915217 -0.407481 -p 0 0.952796 -0.309582 -p 0 0.979937 -0.208292 -p 0 0.996341 -0.10472 -p 0 1.001829 0 -p 0.10472 0.996341 0 -p 0.208292 0.979937 0 -p 0.309582 0.952796 0 -p 0.407481 0.915217 0 -p 0.500915 0.86761 0 -p 0.588861 0.810497 0 -p 0.670355 0.744504 0 -p 0.744504 0.670355 0 -p 0.810497 0.588861 0 -p 0.86761 0.500915 0 -p 0.915217 0.407481 0 -p 0.952796 0.309582 0 -p 0.979937 0.208292 0 -p 0.996341 0.10472 0 -p 1.001829 0 0 -p 0.996341 -0.10472 0 -p 0.979937 -0.208292 0 -p 0.952796 -0.309582 0 -p 0.915217 -0.407481 0 -p 0.86761 -0.500915 0 -p 0.810497 -0.588861 0 -p 0.744504 -0.670355 0 -p 0.670355 -0.744504 0 -p 0.588861 -0.810497 0 -p 0.500915 -0.86761 0 -p 0.407481 -0.915217 0 -p 0.309582 -0.952796 0 -p 0.208292 -0.979937 0 -p 0.10472 -0.996341 0 -p 0 -1.001829 0 -p -0.10472 -0.996341 0 -p -0.208292 -0.979937 0 -p -0.309582 -0.952796 0 -p -0.407481 -0.915217 0 -p -0.500915 -0.86761 0 -p -0.588861 -0.810497 0 -p -0.670355 -0.744504 0 -p -0.744504 -0.670355 0 -p -0.810497 -0.588861 0 -p -0.86761 -0.500915 0 -p -0.915217 -0.407481 0 -p -0.952796 -0.309582 0 -p -0.979937 -0.208292 0 -p -0.996341 -0.10472 0 -p -1.001829 0 0 -p -0.996341 0.10472 0 -p -0.979937 0.208292 0 -p -0.952796 0.309582 0 -p -0.915217 0.407481 0 -p -0.86761 0.500915 0 -p -0.810497 0.588861 0 -p -0.744504 0.670355 0 -p -0.670355 0.744504 0 -p -0.588861 0.810497 0 -p -0.500915 0.86761 0 -p -0.407481 0.915217 0 -p -0.309582 0.952796 0 -p -0.208292 0.979937 0 -p -0.10472 0.996341 0 -p 0 1.001829 0 -p 0 0.996341 -0.10472 -p 0 0.979937 -0.208292 -p 0 0.952796 -0.309582 -p 0 0.915217 -0.407481 -p 0 0.86761 -0.500915 -p 0 0.810497 -0.588861 -p 0 0.744504 -0.670355 -p 0 0.670355 -0.744504 -p 0 0.588861 -0.810497 -p 0 0.500915 -0.86761 -p 0 0.407481 -0.915217 -p 0 0.309582 -0.952796 -p 0 0.208292 -0.979937 -p 0 0.10472 -0.996341 -p 0 0 -1.001829 -p 0.10472 0 -0.996341 -p 0.208292 0 -0.979937 -p 0.309582 0 -0.952796 -p 0.407481 0 -0.915217 -p 0.500915 0 -0.86761 -p 0.588861 0 -0.810497 -p 0.670355 0 -0.744504 -p 0.744504 0 -0.670355 -p 0.810497 0 -0.588861 -p 0.86761 0 -0.500915 -p 0.915217 0 -0.407481 -p 0.952796 0 -0.309582 -p 0.979937 0 -0.208292 -p 0.996341 0 -0.10472 -p 1.001829 0 0 -p 0.996341 0 0.10472 -p 0.979937 0 0.208292 -p 0.952796 0 0.309582 -p 0.915217 0 0.407481 -p 0.86761 0 0.500915 -p 0.810497 0 0.588861 -p 0.744504 0 0.670355 -p 0.670355 0 0.744504 -p 0.588861 0 0.810497 -p 0.500915 0 0.86761 -p 0.407481 0 0.915217 -p 0.309582 0 0.952796 -p 0.208292 0 0.979937 -p 0.10472 0 0.996341 -p 0 0 1.001829 -p -0.10472 0 0.996341 -p -0.208292 0 0.979937 -p -0.309582 0 0.952796 -p -0.407481 0 0.915217 -p -0.500915 0 0.86761 -p -0.588861 0 0.810497 -p -0.670355 0 0.744504 -p -0.744504 0 0.670355 -p -0.810497 0 0.588861 -p -0.86761 0 0.500915 -p -0.915217 0 0.407481 -p -0.952796 0 0.309582 -p -0.979937 0 0.208292 -p -0.996341 0 0.10472 -p -1.001829 0 0 -p -0.996341 0 -0.10472 -p -0.979937 0 -0.208292 -p -0.952796 0 -0.309582 -p -0.915217 0 -0.407481 -p -0.86761 0 -0.500915 -p -0.810497 0 -0.588861 -p -0.744504 0 -0.670355 -p -0.670355 0 -0.744504 -p -0.588861 0 -0.810497 -p -0.500915 0 -0.86761 -p -0.407481 0 -0.915217 -p -0.309582 0 -0.952796 -p -0.208292 0 -0.979937 -p -0.10472 0 -0.996341 -p 0 0 -1.001829 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -k 38 -k 39 -k 40 -k 41 -k 42 -k 43 -k 44 -k 45 -k 46 -k 47 -k 48 -k 49 -k 50 -k 51 -k 52 -k 53 -k 54 -k 55 -k 56 -k 57 -k 58 -k 59 -k 60 -k 61 -k 62 -k 63 -k 64 -k 65 -k 66 -k 67 -k 68 -k 69 -k 70 -k 71 -k 72 -k 73 -k 74 -k 75 -k 76 -k 77 -k 78 -k 79 -k 80 -k 81 -k 82 -k 83 -k 84 -k 85 -k 86 -k 87 -k 88 -k 89 -k 90 -k 91 -k 92 -k 93 -k 94 -k 95 -k 96 -k 97 -k 98 -k 99 -k 100 -k 101 -k 102 -k 103 -k 104 -k 105 -k 106 -k 107 -k 108 -k 109 -k 110 -k 111 -k 112 -k 113 -k 114 -k 115 -k 116 -k 117 -k 118 -k 119 -k 120 -k 121 -k 122 -k 123 -k 124 -k 125 -k 126 -k 127 -k 128 -k 129 -k 130 -k 131 -k 132 -k 133 -k 134 -k 135 -k 136 -k 137 -k 138 -k 139 -k 140 -k 141 -k 142 -k 143 -k 144 -k 145 -k 146 -k 147 -k 148 -k 149 -k 150 -k 151 -k 152 -k 153 -k 154 -k 155 -k 156 -k 157 -k 158 -k 159 -k 160 -k 161 -k 162 -k 163 -k 164 -k 165 -k 166 -k 167 -k 168 -k 169 -k 170 -k 171 -k 172 -k 173 -k 174 -k 175 -k 176 -k 177 -k 178 -k 179 -k 180 -k 181 -k 182 -k 183 -k 184 -k 185 -k 186 -k 187 -k 188 -k 189 -k 190 -k 191 -k 192 -k 193 -k 194 -k 195 ;')
    
        if type=='Cube' :
            currentControl = pymel.mel.eval ('curve -d 1 -p 1 1 1 -p 1 1 -1 -p -1 1 -1 -p -1 -1 -1 -p 1 -1 -1 -p 1 -1 1 -p -1 -1 1 -p -1 1 1 -p 1 1 1 -p 1 -1 1 -p 1 -1 -1 -p 1 1 -1 -p -1 1 -1 -p -1 1 1 -p -1 -1 1 -p -1 -1 -1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 ;')
    
        if type=='Pentagon' :
            currentControl = pymel.mel.eval ('curve -d 1 -p -0.671444 0 -1 -p -1 0 0.303691 -p 0 0 1 -p 1 0 0.303691 -p 0.671444 0 -1 -p -0.671444 0 -1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 ;')
       
        if type=='SingleArrow' :
            currentControl = pymel.mel.eval ('curve -d 1 -p 0 0 1 -p 1 0 0 -p 0.357143 0 0 -p 0.357143 0 -1 -p -0.357143 0 -1 -p -0.357143 0 0 -p -1 0 0 -p 0 0 1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 ;')
               
        if type=='AimCircle' :
            currentControl = pymel.mel.eval ('curve -d 1 -p 0 0.330576 0 -p 0.0376921 0.382454 0 -p 0.0892717 0.437381 0 -p 0.147329 0.48541 0 -p 0.210948 0.525784 0 -p 0.279125 0.557866 0 -p 0.350786 0.58115 0 -p 0.4248 0.595269 0 -p 0.5 0.6 0 -p 0.5752 0.595269 0 -p 0.649214 0.58115 0 -p 0.720875 0.557866 0 -p 0.789052 0.525784 0 -p 0.852671 0.48541 0 -p 0.910728 0.437381 0 -p 0.962308 0.382454 0 -p 1.006597 0.321496 0 -p 1.042896 0.255468 0 -p 1.070634 0.18541 0 -p 1.089372 0.112429 0 -p 1.098816 0.0376743 0 -p 1.098816 -0.0376743 0 -p 1.089372 -0.112429 0 -p 1.070634 -0.18541 0 -p 1.042896 -0.255468 0 -p 1.006597 -0.321496 0 -p 0.962308 -0.382454 0 -p 0.910728 -0.437381 0 -p 0.852671 -0.48541 0 -p 0.789052 -0.525784 0 -p 0.720875 -0.557866 0 -p 0.649214 -0.58115 0 -p 0.5752 -0.595269 0 -p 0.5 -0.6 0 -p 0.4248 -0.595269 0 -p 0.350786 -0.58115 0 -p 0.279125 -0.557866 0 -p 0.210948 -0.525784 0 -p 0.147329 -0.48541 0 -p 0.0892717 -0.437381 0 -p 0.0376921 -0.382454 0 -p 1.7524e-010 -0.330576 0 -p -0.0376921 -0.382454 0 -p -0.0892717 -0.437381 0 -p -0.147329 -0.48541 0 -p -0.210948 -0.525784 0 -p -0.279125 -0.557866 0 -p -0.350786 -0.58115 0 -p -0.4248 -0.595269 0 -p -0.5 -0.6 0 -p -0.5752 -0.595269 0 -p -0.649214 -0.58115 0 -p -0.720875 -0.557866 0 -p -0.789052 -0.525784 0 -p -0.852671 -0.48541 0 -p -0.910728 -0.437381 0 -p -0.962308 -0.382454 0 -p -1.006597 -0.321496 0 -p -1.042896 -0.255468 0 -p -1.070634 -0.18541 0 -p -1.089372 -0.112429 0 -p -1.098816 -0.0376743 0 -p -1.098816 0.0376743 0 -p -1.089372 0.112429 0 -p -1.070634 0.18541 0 -p -1.042896 0.255468 0 -p -1.006597 0.321496 0 -p -0.962308 0.382454 0 -p -0.910728 0.437381 0 -p -0.852671 0.48541 0 -p -0.789052 0.525784 0 -p -0.720875 0.557866 0 -p -0.649214 0.58115 0 -p -0.5752 0.595269 0 -p -0.5 0.6 0 -p -0.4248 0.595269 0 -p -0.350786 0.58115 0 -p -0.279125 0.557866 0 -p -0.210948 0.525784 0 -p -0.147329 0.48541 0 -p -0.0892717 0.437381 0 -p -0.0376921 0.382454 0 -p 0 0.330576 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -k 38 -k 39 -k 40 -k 41 -k 42 -k 43 -k 44 -k 45 -k 46 -k 47 -k 48 -k 49 -k 50 -k 51 -k 52 -k 53 -k 54 -k 55 -k 56 -k 57 -k 58 -k 59 -k 60 -k 61 -k 62 -k 63 -k 64 -k 65 -k 66 -k 67 -k 68 -k 69 -k 70 -k 71 -k 72 -k 73 -k 74 -k 75 -k 76 -k 77 -k 78 -k 79 -k 80 -k 81 -k 82 ;')
    
        if type=='IKFK' :
            ikIControl = pymel.mel.eval ('curve -d 1 -p -3.064299 0 2.088051 -p -2.822937 0 2.088051 -p -2.822937 0 3.911949 -p -3.064299 0 3.911949 -p -3.064299 0 2.088051 -k 0 -k 1 -k 2 -k 3 -k 4 ;')
            ikKControl = pymel.mel.eval ('curve -d 1 -p -2.407397 0 2.088051 -p -2.407397 0 3.911949 -p -2.166035 0 3.911949 -p -2.166035 0 3.27993 -p -1.867443 0 2.988803 -p -1.218006 0 3.911949 -p -0.899508 0 3.911949 -p -1.698241 0 2.827066 -p -0.9331 0 2.088051 -p -1.260306 0 2.088051 -p -2.166035 0 2.992535 -p -2.166035 0 2.088051 -p -2.407397 0 2.088051 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 ;')
            fkFControl = pymel.mel.eval ('curve -d 1 -p 0.0223944 0 2.088051 -p 0.0223944 0 3.911949 -p 0.263756 0 3.911949 -p 0.263756 0 3.083357 -p 1.119719 0 3.083357 -p 1.119719 0 2.868122 -p 0.263756 0 2.868122 -p 0.263756 0 2.303286 -p 1.252842 0 2.303286 -p 1.252842 0 2.088051 -p 0.0223944 0 2.088051 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 ;')
            fkKControl = pymel.mel.eval ('curve -d 1 -p 1.55641 0 2.088051 -p 1.55641 0 3.911949 -p 1.797772 0 3.911949 -p 1.797772 0 3.27993 -p 2.096364 0 2.988803 -p 2.745801 0 3.911949 -p 3.064299 0 3.911949 -p 2.265566 0 2.827066 -p 3.030707 0 2.088051 -p 2.7035 0 2.088051 -p 1.797772 0 2.992535 -p 1.797772 0 2.088051 -p 1.55641 0 2.088051 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 ;')
    
            ikKShape = pymel.listRelatives (ikKControl, s=1)
            fkFShape = pymel.listRelatives (fkFControl, s=1)
            fkKShape = pymel.listRelatives (fkKControl, s=1)
            pymel.parent (ikKShape[0], ikIControl, r=1, s=1)
            pymel.parent (fkFShape[0], ikIControl, r=1, s=1)
            pymel.parent (fkKShape[0], ikIControl, r=1, s=1)
            pymel.delete (ikKControl, fkFControl, fkKControl)

        generic = openGeneric.Generic()
        
        #controlName = generic.getNameStyle ([side, name, self.input._control]) 
        controlName = name        
        nullGroup = generic.getNameStyle ([side, name, self.input._null])
        offsetGroup = generic.getNameStyle ([side, name, self.input._offset])
        group = generic.getNameStyle ([side, name, self.input._group])

        for eachNode in [nullGroup, controlName, offsetGroup, group]:
            if not pymel.objExists(str(eachNode)):
                continue   
            try :         
                pymel.delete (eachNode)
            except Exception as result:
                warnings.warn(result)              

        nullGroup = pymel.group (em=1, n=nullGroup)            
        offsetGroup = pymel.group (em=1, n=offsetGroup)
        group = pymel.group (em=1, n=group)        
        currentControl = currentControl.rename(controlName)               
        
        currentControl.setParent(offsetGroup)
        offsetGroup.setParent(group)
        nullGroup.setParent(currentControl)
        
        if not positionNode :
            return [nullGroup, currentControl, offsetGroup, group]

        generic.snap(positionNode, group)
        return [nullGroup, currentControl, offsetGroup, group]
        
#End###################################################################################################