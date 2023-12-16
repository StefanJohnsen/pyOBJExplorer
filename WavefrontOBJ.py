# WavefrontMTL.py - Python script for parsing wavefront mtl files
#
# Copyright (c) 2023 by FalconCoding
# Author: Stefan Johnsen
# Email: stefan.johnsen@outlook.com
#
# This software is released under the MIT License.

import os
import sys
import numpy as np

vector = np.array

class Face:
    def __init__(self):
        self.vertex  = []
        self.texture = []
        self.normal  = []

class Geometry:
    def __init__(self):
        self.material = None
        self.face  = []
        self.point = []
        self.line  = []

def index(objIndex, indexToList):
    i = int(objIndex)
    if i > 0: return i - 1
    return i + len(indexToList)

class WavefrontOBJ:

    def __init__(self):
        self.mtllib = None
        self.vertex   = []
        self.texture  = []
        self.normal   = []
        self.geometry = []

    def load(self, fname):
        
        if fname is None: return

        geometry = Geometry()

        if not os.path.exists(fname):
            print(f"obj file not found: {fname}")
            return

        self.mtllib = fname

        with open(fname) as file_in:
            for line in file_in:
                line = line.strip()
                
                if not line: continue

                words = line.split()
                command = words[0]
                data = words[1:]

                if command == 'mtllib':  # Material library
                    path = os.path.split(fname)[0]
                    self.mtllib = os.path.join(path, data[0])
                    
                elif command == 'usemtl':  # Use material
                    if geometry.material != None:
                        self.geometry.append(geometry)
                    geometry = Geometry()
                    geometry.material = data[0]

                elif command == 'v':  # Vertex
                    x, y, z = map(float, data[:3])
                    self.vertex.append(vector([x, y, z]))

                elif command == 'vt':  # Texture
                    x, y = map(float, data[:2])
                    self.texture.append(vector([x, y, 0]))

                elif command == 'vn':  # Normal
                    x, y, z = map(float, data[:3])
                    self.normal.append(vector([x, y, z]))

                elif command == 'p':  # Point
                    indices = [index(item, self.vertex) for item in data]
                    geometry.point.append(indices)

                elif command == 'l':  # Line
                    indices = [index(item, self.vertex) for item in data]
                    if len(indices) == 2:
                        geometry.line.append(indices)

                elif command == 'f':  # Face
                    face = Face()
                    for group in data:
                        indices = group.split('/')
                        if len(indices) == 0:
                            continue
                        if len(indices) > 0 and indices[0]:
                            face.vertex.append(index(indices[0], self.vertex))
                        if len(indices) > 1 and indices[1]:
                            face.texture.append(index(indices[1], self.texture))
                        if len(indices) > 2 and indices[2]:
                            face.normal.append(index(indices[2], self.normal))
                    geometry.face.append(face)

        self.geometry.append(geometry)

    def aabb(self):  # axis-aligned bounding box
        
        zero = np.array([0.0, 0.0, 0.0])
        
        if not self.vertex:
            return zero, zero

        max = sys.float_info.max
        
        start = np.array([max, max, max])
        
        min_coord = +start
        max_coord = -start

        for geometry in self.geometry:
            for face in geometry.face:
                for i in face.vertex:
                    vertex = self.vertex[i]
                    min_coord = np.minimum(min_coord, vertex)
                    max_coord = np.maximum(max_coord, vertex)
            for line in geometry.line:
                for i in line:
                    vertex = self.vertex[i]
                    min_coord = np.minimum(min_coord, vertex)
                    max_coord = np.maximum(max_coord, vertex)
            for point in geometry.point:
                for i in point:
                    vertex = self.vertex[i]
                    min_coord = np.minimum(min_coord, vertex)
                    max_coord = np.maximum(max_coord, vertex)

        if np.all(min_coord == start) or np.all(max_coord == start):
            return zero, zero
            
        # Calculate center and size
        center = (max_coord + min_coord) / 2
        size = max_coord - min_coord

        return center, size
    
    def translate(self, translation):    
        if translation is None: return
        if not self.vertex: return
        self.vertex += translation

    def geometries(self):
        geometries = {}
        for geometry in self.geometry:
            if geometry.material not in geometries:
                geometries[geometry.material] = Geometry()
                geometries[geometry.material].material = geometry.material
            geometries[geometry.material].face.extend(geometry.face)
            geometries[geometry.material].point.extend(geometry.point)
            geometries[geometry.material].line.extend(geometry.line)

        return geometries