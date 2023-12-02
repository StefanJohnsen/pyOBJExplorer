# WavefrontMTL.py - Python script for parsing wavefront mtl files
#
# Copyright (c) 2023 by FalconCoding
# Author: Stefan Johnsen
# Email: stefan.johnsen@outlook.com
#
# This software is released under the MIT License.

import os
import numpy as np

vector = np.array

class Material:
    def __init__(self):
        self.name = None                    # Material name
        self.Kd = vector([0.5, 0.5, 0.5])   # Default diffuse color
        self.Ka = vector([0.0, 0.0, 0.0])   # Default ambient color
        self.Ks = vector([0.0, 0.0, 0.0])   # Default specular color
        self.Ke = vector([0.0, 0.5, 0.0])   # Default emission color
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
    def texture(self): return self.map_Kd

def mtlFile(file):
    if file is None: return None
    directory, basename = os.path.split(file)
    if not directory: directory = os.getcwd()
    name, ext = os.path.splitext(basename)
    if ext.lower() == '.obj': ext = '.mtl'
    file = os.path.join(directory, name + ext)
    return file

class WavefrontMTL:
    def __init__(self):
        self.materials = []
    
    def load(self, file):

        file = mtlFile(file)
        
        if not os.path.exists(file):
            print(f"mtl file not found: {file}")
            return

        directory = os.path.dirname(file)

        material = Material()

        with open(file) as buffer:
            for line in buffer:
                line = line.strip()
                
                if not line: continue

                words = line.split()
                command = words[0]
                data = words[1:]

                if command == 'newmtl':
                    if material.name != None:
                        self.materials.append(material)
                    material = Material()
                    material.name = data[0]
                elif command == 'Ka':
                    material.Ka = vector(list(map(float, data[:3])))
                elif command == 'Kd':
                    material.Kd = vector(list(map(float, data[:3])))
                elif command == 'Ks':
                    material.Ks = vector(list(map(float, data[:3])))
                elif command == 'Ke':
                    material.Ke = vector(list(map(float, data[:3])))
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
        
    def material(self, name):
        for material in self.materials:
            if material.name == name:
                return material
        return Material()
