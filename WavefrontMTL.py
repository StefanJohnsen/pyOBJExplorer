# WavefrontMTL.py - Python script for parsing wavefront mtl files
#
# Copyright (c) 2023 by FalconCoding
# Author: Stefan Johnsen
# Email: stefan.johnsen@outlook.com
#
# This software is released under the MIT License.

import os
import shutil
from enum import Enum
from vpython import vector

class Material:
    def __init__(self):
        self.name = None                    # Material name
        self.Kd = vector(0.5, 0.5, 0.5)     # Default diffuse color
        self.Ka = vector(0.0, 0.0, 0.0)     # Default ambient color
        self.Ks = vector(0.0, 0.0, 0.0)     # Default specular color
        self.Ke = vector(0.0, 0.5, 0.0)     # Default emission color
        self.Ns = 0.0                       # Default specular exponent
        self.Ni = 1.0                       # Default optical density
        self.d = 1.0                        # Default dissolve
        self.illum = 0                      # Default illumination model
        self.map_Kd = None                  # Texture map   
        self.map_Ka = None                  # Texture map   
        self.map_Ks = None                  # Texture map   
        self.map_Ns = None                  # Texture map   
        self.map_d = None                   # Texture map   

    def color(self): return self.Kd
    def opacity(self): return self.d
    def shininess(self): return self.Ns
    def texture(self, basename = True):
        if self.map_Kd is None: return None
        if basename: return os.path.basename(self.map_Kd)
        return self.map_Kd

def copyFile(file):
    if file is None: return None
    if not os.path.exists(file): return
    directory = os.getcwd()
    basename = os.path.basename(file)
    copyfile = os.path.join(directory, basename)
    if os.path.exists(copyfile): return
    if file.lower() == copyfile.lower(): return
    shutil.copy(file, copyfile)

def deleteFile(file):
    if file is None: return None
    if not os.path.exists(file): return
    directory = os.getcwd()
    basename = os.path.basename(file)
    copyfile = os.path.join(directory, basename)
    if not os.path.exists(copyfile): return
    if file.lower() == copyfile.lower(): return
    print(f"{file.lower()} == {copyfile.lower()}")
    os.remove(copyfile)

class WavefrontMTL:
    def __init__(self):
        self.materials = [] #List of materials

    def copyTextures(self):
        for material in self.materials:
            copyFile(material.map_Kd)
            copyFile(material.map_Ka)
            copyFile(material.map_Ks)
            copyFile(material.map_Ns)
            copyFile(material.map_d)

    def deleteTextures(self):
        for material in self.materials:
            deleteFile(material.map_Kd)
            deleteFile(material.map_Ka)
            deleteFile(material.map_Ks)
            deleteFile(material.map_Ns)
            deleteFile(material.map_d)

    def __del__(self):
        self.deleteTextures()

    def load(self, fname):

        if fname is None: return

        directory, filename = os.path.split(fname)
        if not directory: directory = os.getcwd()
        base, ext = os.path.splitext(filename)
        if ext.lower() == '.obj': ext = '.mtl'
        fname = os.path.join(directory, base + ext)
        
        if not os.path.exists(fname):
            print(f"mtl file not found: {fname}")
            return

        material = Material()

        with open(fname) as file:
            for line in file:
                line = line.strip()
                
                if not line: continue

                words = line.split()
                command = words[0]
                data = words[1:]

                if command == 'newmtl':  # New material
                    if material.name != None:
                        self.materials.append(material)
                    material = Material()
                    material.name = data[0]
                elif command == 'Ka':
                    material.Ka = vector(*tuple(map(float, data[:3])))
                elif command == 'Kd':
                    material.Kd = vector(*tuple(map(float, data[:3])))
                elif command == 'Ks':
                    material.Ks = vector(*tuple(map(float, data[:3])))
                elif command == 'Ke':
                    material.Ke = vector(*tuple(map(float, data[:3])))
                elif command == 'Ns':
                    material.Ns = float(data[0])
                elif command == 'Ni':
                    material.Ni = float(data[0])
                elif command == 'd':
                    material.d = float(data[0])
                elif command == 'illum':
                    material.illum = int(data[0])
                elif command == 'map_Kd':
                    material.map_Kd = os.path.join(directory, data[0])
                elif command == 'map_Ka':
                    material.map_Ka = os.path.join(directory, data[0])
                elif command == 'map_Ks':
                    material.map_Ks = os.path.join(directory, data[0])
                elif command == 'map_Ns':
                    material.map_Ns = os.path.join(directory, data[0])
                elif command == 'map_d':
                    material.map_d = os.path.join(directory, data[0])

        if material is not None:
            self.materials.append(material)

        self.copyTextures()

    def material(self, name):
        for material in self.materials:
            if material.name == name:
                return material
        return Material()
