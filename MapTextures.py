# MapTextures.py
# 
# This Python script is designed to copy texture files 
# to the current working directory. VPython fails to 
# locate texture files that are not in the working 
# directory, even when their full path is provided.

# Copyright (c) 2023 by FalconCoding
# Author: Stefan Johnsen
# Email: stefan.johnsen@outlook.com
#
# This software is released under the MIT License.

import os
import shutil

temporarilyCopyTextureFilesToWorkingDir = []

def copyFileToWorkingDir(sourceFile):
    global temporarilyCopyTextureFilesToWorkingDir
    if sourceFile is None: return
    if not os.path.exists(sourceFile): return
    sourceDirectory = os.path.dirname(sourceFile)
    if sourceDirectory == '': return
    targetDirectory = os.getcwd()
    if sourceDirectory.lower() == targetDirectory.lower():
        return
    basename = os.path.basename(sourceFile)
    targetFile = os.path.join(targetDirectory, basename)
    if os.path.exists(targetFile): return
    shutil.copy(sourceFile, targetFile)
    temporarilyCopyTextureFilesToWorkingDir.append(targetFile)

def setupVPythonTextureFiles(mtl):
    for material in mtl.materials:
        copyFileToWorkingDir(material.map_Kd)
        copyFileToWorkingDir(material.map_Ka)
        copyFileToWorkingDir(material.map_Ks)
        copyFileToWorkingDir(material.map_Ns)
        copyFileToWorkingDir(material.map_d)

def removeTempTextureFilesInWorkingDir():
    print("Delete all registered copy texture files")
    global temporarilyCopyTextureFilesToWorkingDir
    for texture in temporarilyCopyTextureFilesToWorkingDir:
        if os.path.exists(texture):
            os.remove(texture)
   
# This will be executed when the process ends
import atexit
atexit.register(removeTempTextureFilesInWorkingDir)

 