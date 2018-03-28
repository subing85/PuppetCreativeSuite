'''
Puppet Creative Suite v1.0.0
Date : March 28, 2018
Last modified: March 28, 2018
Author: Subin. Gopi (subing85@gmail.com)

# Copyright (c) 2018, Subin Gopi
# All rights reserved.

# WARNING! All changes made in this file will be lost!

Description
    constructor for Puppet Creative Suite
'''

from PuppetCreativeSuite import buildPuppet
reload(buildPuppet)

def main():
    buildPuppet.runMayaUiDemo()

main()
    
