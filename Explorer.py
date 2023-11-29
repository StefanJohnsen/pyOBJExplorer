# Explorer.py
# Python script for loading wavfront obj(+mtl) files
# and visualize the 3D model in VPython (WebGL)
#
# Copyright (c) 2023 by FalconCoding
# Author: Stefan Johnsen
# Email: stefan.johnsen@outlook.com
#
# This software is released under the MIT License.

from vpython import *
from WavefrontOBJ import WavefrontOBJ
from WavefrontMTL import WavefrontMTL

import os
import sys
import argparse
import argparse
import Triangulate

#-------------------------------------------------------------------------------------

sceneWidth = 1470          # Adjust the width as needed
sceneHeight = 720          # Adjust the height as needed

loadThisObjFileInDebug = 'c:\\temp\\rubikcube.obj'

#-------------------------------------------------------------------------------------

def normal(v0, v1, v2):
    n = cross(v1 - v0, v2 - v1)
    if n.mag == 0.0: 
        return vector(0,0,0)
    return n / n.mag

def create_point(v, radius, color):
    shininess /= 1000
    return sphere(pos = v, radius=radius, color=color)

def create_line(v0, v1, radius, color):
    line = cylinder(pos=v0, axis=v1 - v0, radius=radius, color=color)
    node = sphere(pos = v1, radius=radius, color=color)
    return line, node

def create_triangle(v0, v1, v2, color):
    n = normal(v0, v1, v2)
    a = vertex(pos=v0, normal = n, color=color)
    b = vertex(pos=v1, normal = n, color=color)
    c = vertex(pos=v2, normal = n, color=color)
    return triangle(vs=[a,b,c])

def create_triangle_normal(v0, v1, v2, n0, n1, n2, color):
    a = vertex(pos=v0, normal = n0, color=color)
    b = vertex(pos=v1, normal = n1, color=color)
    c = vertex(pos=v2, normal = n2, color=color)
    return triangle(vs=[a,b,c])

def create_triangle_normal_texture(v0, v1, v2, n0, n1, n2, t0, t1, t2, texture):
    a = vertex(pos=v0, normal=n0, texpos=t0)
    b = vertex(pos=v1, normal=n1, texpos=t1)
    c = vertex(pos=v2, normal=n2, texpos=t2)
    return triangle(vs=[a,b,c], texture=texture)

def create_quad(v0, v1, v2, v3, color):
    n = normal(v0, v1, v2)
    a = vertex(pos=v0, normal = n, color=color)
    b = vertex(pos=v1, normal = n, color=color)
    c = vertex(pos=v2, normal = n, color=color)
    d = vertex(pos=v3, normal = n, color=color)
    return quad(vs=[a,b,c,d])

def create_quad_normal(v0, v1, v2, v3, n0, n1, n2, n3, color):
    a = vertex(pos=v0, normal = n0, color=color)
    b = vertex(pos=v1, normal = n1, color=color)
    c = vertex(pos=v2, normal = n2, color=color)
    d = vertex(pos=v3, normal = n3, color=color)
    return quad(vs=[a,b,c,d])

def create_quad_normal_texture(v0, v1, v2, v3, n0, n1, n2, n3, t0, t1, t2, t3, texture):
    a = vertex(pos=v0, normal=n0, texpos=t0)
    b = vertex(pos=v1, normal=n1, texpos=t1)
    c = vertex(pos=v2, normal=n2, texpos=t2)
    d = vertex(pos=v3, normal=n3, texpos=t3)
    return quad(vs=[a,b,c,d], texture=texture)

def create_wire_face(vertices, radius, color):
    if vertices is None: return
    if len(vertices) < 3: return
    face = curve(radius=radius, color=color)
    for vertex in vertices:
        face.append(vertex)
    return face

#-------------------------------------------------------------------------------------

def create_points(obj, geometry, material):
    if geometry.point is None: return
    for point in geometry.point:
        if point is None: continue
        for i in point:
            v = obj.vertex[i]
            create_point(v, 0.12, material.color())

def create_lines(obj, geometry, material):
    if geometry.line is None: return
    for line in geometry.line:
        if line is None: continue
        size = len(line)
        if size < 2: continue
        for i in range(size-1):
            v0 = obj.vertex[line[i]]
            v1 = obj.vertex[line[i + 1]]
            create_line(v0, v1, 0.01, material.color())

def create_wire_faces(obj, geometry, material):
    if geometry.face is None: return
    for face in geometry.face:
        if face is None: continue
        size = len(face)
        if size < 3: continue
        face_vertex = []
        for i in face:
            v = obj.vertex[i]
            face_vertex.append(v)
        create_wire_face(face_vertex, 0.01, material.color())

def create_faces(obj, geometry, material):
    if geometry.face is None: return

    color = material.color()
    texture = material.texture()

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
            v = obj.vertex[i]
            polygon.append(v)

        triangles, n = Triangulate.triangulate(polygon)

        for t in triangles:
            create_triangle_normal(t.p0, t.p1, t.p2, n, n, n, color)

def create_geometry(obj, mtl, geometry):
    if obj is None: return
    if mtl is None: return
    if geometry is None: return
    material = mtl.material(geometry.material)
    create_points(obj, geometry, material)
    create_lines(obj, geometry, material)
    #create_wire_faces(obj, geometry, material)
    create_faces(obj, geometry, material)

def create_box(center, size, color):
    if center is None: return
    size /= 2
    corners = []

    for dx in [-size.x, size.x]:
        for dy in [-size.y, size.y]:
            for dz in [-size.z, size.z]:
                corner = center + vector(dx, dy, dz)
                corners.append(corner)

    edges = [ (0, 1), (1, 3), (3, 2), (2, 0),  # Bottom face
              (4, 5), (5, 7), (7, 6), (6, 4),  # Top face
              (0, 4), (1, 5), (3, 7), (2, 6) ] # Vertical edges

    for edge in edges:
        create_line(corners[edge[0]], corners[edge[1]], 0.3, color)

#-------------------------------------------------------------------------------------

def position_camera(aabbCenter, aabbSize, elevation, zoom, box):
    area = [(aabbSize.y * aabbSize.z, vec(1, 0, 0)),
            (aabbSize.y * aabbSize.x, vec(0, 0, 1))]
    largest_area_direction = sorted(area, reverse=True)[0][1]
    distance = max(aabbSize.y, aabbSize.z)*zoom
    pos = aabbCenter + largest_area_direction * distance
    pos.y += distance * elevation
    scene.camera.pos = pos
    scene.camera.axis = aabbCenter - scene.camera.pos
    scene.camera.range = distance
    if box: create_box(aabbCenter, aabbSize, vector(1,0,0))

def set_light_behind_camera():
    direction = -scene.camera.axis.norm()
    distant_light(direction=direction, color=color.white)

#-------------------------------------------------------------------------------------

def load(file, box):

    obj = WavefrontOBJ()
    obj.load(file)

    mtl = WavefrontMTL()
    mtl.load(obj.mtllib)

    center, size = obj.aabb()
    obj.translate(-center)
    center = vector(0,0,0)

    position_camera(center, size, 0.4, 1.5, box)
    set_light_behind_camera()

    count = 0
    size = len(obj.geometry)

    for geometry in obj.geometry:
        count+=1
        print(f"geometry: {count} / {size} / faces : {len(geometry.face)}")
        create_geometry(obj, mtl, geometry)

#-------------------------------------------------------------------------------------

def load_Wavefront(file, boundingbox):
    scene.visible = False
    scene.width = sceneWidth
    scene.height = sceneHeight
    scene.background = color.white
    load(file, boundingbox)
    scene.waitfor("textures")
    scene.visible = True

    while True: pass

#-------------------------------------------------------------------------------------

description = 'Load and visualize 3D objects from Wavefront .obj files'

def main():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('filename', help='The name of the file to check')
    parser.add_argument('-b', '--boundingbox', action='store_true', help='Show bounding box')

    if 'pydevd' in sys.modules:
        args = parser.parse_args([loadThisObjFileInDebug])
    else:
        args = parser.parse_args()

    if not os.path.isfile(args.filename):
        print(f"Error: The file {args.filename} does not exist.")
        return

    _, ext = os.path.splitext(args.filename)
    if ext.lower() != '.obj':
        print("Error: The file is not a wavefront .obj file.")
        return

    load_Wavefront(args.filename, args.boundingbox)

if __name__ == "__main__":
    main()



