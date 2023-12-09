# Explorer.py
# Python script for loading wavfront obj(+mtl) files
# and visualize the 3D model in VPython (WebGL)
#
# Copyright (c) 2023 by FalconCoding
# Author: Stefan Johnsen
# Email: stefan.johnsen@outlook.com
#
# This software is released under the MIT License.
#-------------------------------------------------------------------------------------

import vpythonex as vp                   # import a wrapper to avoid ZeroDivisionError 

import MapTextures as map
#-------------------------------------------------------------------------------------    

from WavefrontOBJ import *
from WavefrontMTL import *

import os
import sys
import argparse
import Triangulate
import numpy as np
    
#-------------------------------------------------------------------------------------

sceneWidth = 1470          # Adjust the width as needed
sceneHeight = 720          # Adjust the height as needed

loadThisObjFileInDebug = 'c:\\temp\\rubikcube.obj'

#-------------------------------------------------------------------------------------

radiusLine = 0.01
radiusPoint = 0.01

def setRadiusLinePoint(aabbSize):
    global radiusLine, radiusPoint
    radiusLine = np.linalg.norm(aabbSize) / 1000
    radiusPoint = radiusLine

#-------------------------------------------------------------------------------------

def vector(array):
    return vp.vector(array[0], array[1], array[2])

def normal(v0, v1, v2):
    n = np.cross(v1 - v0, v2 - v1)
    if np.linalg.norm(n) == 0.0:
        return np.array([0.0, 0.0, 0.0])
    return n / np.linalg.norm(n)

#-------------------------------------------------------------------------------------

def create_point(v, radius, color):
    return vp.sphere(pos=vector(v), radius=radius, color=vector(color))
   
def create_line(v0, v1, radius, color):
    rgb = vector(color)
    line = vp.cylinder(pos=vector(v0), axis=vector(v1-v0), radius=radius, color=rgb)
    node = vp.sphere(pos=vector(v1), radius=radius, color=rgb)
    return line, node
    
def create_triangle(v0, v1, v2, color):
    rgb = vector(color)
    n = vector(normal(v0, v1, v2))
    a = vp.vertex(pos=vector(v0), normal=n, color=rgb)
    b = vp.vertex(pos=vector(v1), normal=n, color=rgb)
    c = vp.vertex(pos=vector(v2), normal=n, color=rgb)
    return vp.triangle(vs=[a,b,c])

def create_triangle_normal(v0, v1, v2, n0, n1, n2, color):
    rgb = vector(color)    
    a = vp.vertex(pos=vector(v0), normal=vector(n0), color=rgb)
    b = vp.vertex(pos=vector(v1), normal=vector(n1), color=rgb)
    c = vp.vertex(pos=vector(v2), normal=vector(n2), color=rgb)
    return vp.triangle(vs=[a,b,c])

def create_triangle_texture(v0, v1, v2, t0, t1, t2, texture):
    n = vector(normal(v0, v1, v2))
    a = vp.vertex(pos=vector(v0), normal=n, texpos=vector(t0))
    b = vp.vertex(pos=vector(v1), normal=n, texpos=vector(t1))
    c = vp.vertex(pos=vector(v2), normal=n, texpos=vector(t2))
    return vp.triangle(vs=[a,b,c], texture=texture)

def create_triangle_normal_texture(v0, v1, v2, n0, n1, n2, t0, t1, t2, texture):
    a = vp.vertex(pos=vector(v0), normal=vector(n0), texpos=vector(t0))
    b = vp.vertex(pos=vector(v1), normal=vector(n1), texpos=vector(t1))
    c = vp.vertex(pos=vector(v2), normal=vector(n2), texpos=vector(t2))
    return vp.triangle(vs=[a,b,c], texture=texture)

def create_quad(v0, v1, v2, v3, color):
    rgb = vector(color)
    n = vector(normal(v0, v1, v2))
    a = vp.vertex(pos=vector(v0), normal=n, color=rgb)
    b = vp.vertex(pos=vector(v1), normal=n, color=rgb)
    c = vp.vertex(pos=vector(v2), normal=n, color=rgb)
    d = vp.vertex(pos=vector(v3), normal=n, color=rgb)
    return vp.quad(vs=[a,b,c,d])

def create_quad_normal(v0, v1, v2, v3, n0, n1, n2, n3, color):
    rgb = vector(color)    
    a = vp.vertex(pos=vector(v0), normal=vector(n0), color=rgb)
    b = vp.vertex(pos=vector(v1), normal=vector(n1), color=rgb)
    c = vp.vertex(pos=vector(v2), normal=vector(n2), color=rgb)
    d = vp.vertex(pos=vector(v3), normal=vector(n3), color=rgb)
    return vp.quad(vs=[a,b,c,d])

def create_quad_texture(v0, v1, v2, v3, t0, t1, t2, t3, texture):
    n = vector(normal(v0, v1, v2))
    a = vp.vertex(pos=vector(v0), normal=n, texpos=vector(t0))
    b = vp.vertex(pos=vector(v1), normal=n, texpos=vector(t1))
    c = vp.vertex(pos=vector(v2), normal=n, texpos=vector(t2))
    d = vp.vertex(pos=vector(v3), normal=n, texpos=vector(t3))
    return vp.quad(vs=[a,b,c,d], texture=texture)

def create_quad_normal_texture(v0, v1, v2, v3, n0, n1, n2, n3, t0, t1, t2, t3, texture):
    a = vp.vertex(pos=vector(v0), normal=vector(n0), texpos=vector(t0))
    b = vp.vertex(pos=vector(v1), normal=vector(n1), texpos=vector(t1))
    c = vp.vertex(pos=vector(v2), normal=vector(n2), texpos=vector(t2))
    d = vp.vertex(pos=vector(v3), normal=vector(n3), texpos=vector(t3))
    return vp.quad(vs=[a,b,c,d], texture=texture)
    
def create_wire_face(vertices, radius, color):
    if vertices is None: return
    if len(vertices) < 3: return
    face = vp.curve(radius=radius, color=vector(color))
    for vertex in vertices:
        face.append(vector(vertex))
    return face

#-------------------------------------------------------------------------------------
def getcwd_texture(texture):
    if texture is None: return None
    if os.path.exists(texture):
       return os.path.basename(texture)
    return None

def create_points(obj, geometry, material):
    if geometry.point is None: return
    for point in geometry.point:
        if point is None: continue
        for i in point:
            v = obj.vertex[i]
            create_point(v, radiusPoint, material.color())

def create_lines(obj, geometry, material):
    if geometry.line is None: return
    for line in geometry.line:
        if line is None: continue
        size = len(line)
        if size < 2: continue
        for i in range(size-1):
            v0 = obj.vertex[line[i]]
            v1 = obj.vertex[line[i + 1]]
            create_line(v0, v1, radiusLine, material.color())

def create_wire_faces(obj, geometry, material):
    if geometry.face is None: return
    for face in geometry.face:
        if face is None: continue
        size = len(face.vertex)
        if size < 3: continue
        face_vertex = []
        for i in face.vertex:
            v = obj.vertex[i]
            face_vertex.append(v)
        create_wire_face(face_vertex, radiusLine, np.array([0.5, 0.5, 0.5]))

def create_faces(obj, geometry, material):
    if geometry.face is None: return

    color = material.color()
    texture = material.texture()
    texture = getcwd_texture(texture)

    for face in geometry.face:
        if face is None: continue
        size = len(face.vertex)
        if size < 2: continue

        if size == 3:
            v0 = obj.vertex[face.vertex[0]]
            v1 = obj.vertex[face.vertex[1]]
            v2 = obj.vertex[face.vertex[2]]

            if len(face.normal) == 3:
                n0 = obj.normal[face.normal[0]]
                n1 = obj.normal[face.normal[1]]
                n2 = obj.normal[face.normal[2]]
                if len(face.texture) == 3 and texture is not None:
                    t0 = obj.texture[face.texture[0]]
                    t1 = obj.texture[face.texture[1]]
                    t2 = obj.texture[face.texture[2]]
                    create_triangle_normal_texture(v0, v1, v2, n0, n1, n2, t0, t1, t2, texture)
                else:
                    create_triangle_normal(v0, v1, v2, n0, n1, n2, color)
            else:
                if len(face.texture) == 3 and texture is not None:
                    t0 = obj.texture[face.texture[0]]
                    t1 = obj.texture[face.texture[1]]
                    t2 = obj.texture[face.texture[2]]
                    create_triangle_texture(v0, v1, v2, t0, t1, t2, texture)
                else:
                    create_triangle(v0, v1, v2, color)

            continue

        if size == 4:
            v0 = obj.vertex[face.vertex[0]]
            v1 = obj.vertex[face.vertex[1]]
            v2 = obj.vertex[face.vertex[2]]
            v3 = obj.vertex[face.vertex[3]]

            if len(face.normal) == 4:
                n0 = obj.normal[face.normal[0]]
                n1 = obj.normal[face.normal[1]]
                n2 = obj.normal[face.normal[2]]
                n3 = obj.normal[face.normal[3]]
                if len(face.texture) == 4 and texture is not None:
                    t0 = obj.texture[face.texture[0]]
                    t1 = obj.texture[face.texture[1]]
                    t2 = obj.texture[face.texture[2]]
                    t3 = obj.texture[face.texture[3]]
                    create_quad_normal_texture(v0, v1, v2, v3, n0, n1, n2, n3, t0, t1, t2, t3, texture)
                else:
                    create_quad_normal(v0, v1, v2, v3, n0, n1, n2, n3, color)
            else:
                if len(face.texture) == 4 and texture is not None:
                    t0 = obj.texture[face.texture[0]]
                    t1 = obj.texture[face.texture[1]]
                    t2 = obj.texture[face.texture[2]]
                    t3 = obj.texture[face.texture[3]]
                    create_quad_texture(v0, v1, v2, v3, t0, t1, t2, t3, texture)
                else:
                    create_quad(v0, v1, v2, v3, color)

            continue

        polygon = []
        for i in face.vertex:
            p = obj.vertex[i]
            v = Triangulate.Point(p[0], p[1], p[2], i)
            polygon.append(v)

        triangles, normal = Triangulate.triangulate(polygon)

        n = np.array([normal.x, normal.y, normal.z])

        for t in triangles:
            v0 = np.array([t.p0.x, t.p0.y, t.p0.z])
            v1 = np.array([t.p1.x, t.p1.y, t.p1.z])
            v2 = np.array([t.p2.x, t.p2.y, t.p2.z])
            create_triangle_normal(v0, v1, v2, n, n, n, color)

def create_geometry(obj, mtl, geometry, wireframe):
    if geometry is None: return
    material = mtl.material(geometry.material)
    create_points(obj, geometry, material)
    create_lines(obj, geometry, material)
    
    if wireframe:
        create_wire_faces(obj, geometry, material)
    else:
        create_faces(obj, geometry, material)

def explore_geometry(obj, mtl, wireframe):
    if obj is None: return
    if mtl is None: return
    count = 0
    size = len(obj.geometry)
    for geometry in obj.geometry:
        count+=1
        print(f"geometry: {count} / {size} / faces : {len(geometry.face)}")
        create_geometry(obj, mtl, geometry, wireframe)
        
def create_box(center, size, color):
    if center is None: return
    size /= 2
    corners = []
    for dx in [-size[0], size[0]]:
        for dy in [-size[1], size[1]]:
            for dz in [-size[2], size[2]]:
                corner = center + np.array([dx, dy, dz])
                corners.append(corner)

    edges = [ (0, 1), (1, 3), (3, 2), (2, 0),  # Bottom face
              (4, 5), (5, 7), (7, 6), (6, 4),  # Top face
              (0, 4), (1, 5), (3, 7), (2, 6) ] # Vertical edges

    for edge in edges:
        create_line(corners[edge[0]], corners[edge[1]], radiusLine, color)

#-------------------------------------------------------------------------------------

def position_camera(center, size, elevation, zoom, box):
    
    area = [(size[1] * size[2], np.array([1, 0, 0])),
            (size[1] * size[0], np.array([0, 0, 1]))]
    
    largest_area_direction = max(area, key=lambda x: x[0])[1]
    distance = max(size[1], size[2])*zoom
    pos = center + largest_area_direction * distance
    pos[1] += distance * elevation
    
    vp.scene.camera.pos = vector(pos)
    vp.scene.camera.axis = vector(center) - vp.scene.camera.pos
    vp.scene.camera.range = distance
    
    if box: create_box(center, size, np.array([1,0,0]))

def set_light_behind_camera():
    direction = -vp.scene.camera.axis.norm()
    vp.distant_light(direction=direction, color=vp.color.white)

#-------------------------------------------------------------------------------------

def load(file, box, wireframe):

    obj = WavefrontOBJ()
    obj.load(file)

    mtl = WavefrontMTL()
    mtl.load(obj.mtllib)

    center, size = obj.aabb()
    obj.translate(-center)
    center = np.array([0,0,0])
    
    setRadiusLinePoint(size)
    
    position_camera(center, size, 0.4, 1.5, box)
    
    set_light_behind_camera()
    
    map.setupVPythonTextureFiles(mtl)
    
    explore_geometry(obj, mtl, wireframe)

#-------------------------------------------------------------------------------------

def load_Wavefront(file, boundingbox, wireframe):
    
    vp.scene.visible = False
    vp.scene.width = sceneWidth
    vp.scene.height = sceneHeight
    vp.scene.background = vp.vector(1,1,1)
    load(file, boundingbox, wireframe)
    vp.scene.waitfor("textures")
    vp.scene.visible = True

    while True: vp.rate(30)
        
#-------------------------------------------------------------------------------------

description = 'Load and visualize 3D objects from Wavefront .obj file'

def main():
    
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('filename', help='The name of the file to check')
    parser.add_argument('-b', '--boundingbox', action='store_true', help='Show bounding box')
    parser.add_argument('-w', '--wireframe', action='store_true', help='Show wireframe')
    
    if 'pydevd' in sys.modules:
        args = parser.parse_args([loadThisObjFileInDebug, '-b'])
    else:
        args = parser.parse_args()

    if not os.path.isfile(args.filename):
        print(f"Error: The file {args.filename} does not exist.")
        return

    _, ext = os.path.splitext(args.filename)
    if ext.lower() != '.obj':
        print("Error: The file is not a wavefront .obj file.")
        return

    load_Wavefront(args.filename, args.boundingbox, args.wireframe)

if __name__ == "__main__":
     main()
    
    
    
