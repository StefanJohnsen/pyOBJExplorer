
# Triangulate.py - Python script for triangulating polygons
#
# This script specializes in triangulating polygons using two techniques:
# - Fan method for convex polygons
# - Earcut technique for concave polygons
#
# Copyright (c) 2023 by FalconCoding
# Author: Stefan Johnsen
# Email: stefan.johnsen@outlook.com
#
# This software is released under the MIT License.

from vpython import vector, cross, dot, mag
from enum import Enum

epsilon = 1e-6

class TurnDirection(Enum):
    Right = 1
    Left = -1
    NoTurn = 0

class Triangle:
    def __init__(self, p0, p1, p2):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2

def turn(p, u, n, q):
    d = dot(cross(q - p, u), n)

    if d > 0.0:
        return TurnDirection.Right
    elif d < 0.0:
        return TurnDirection.Left
    else:
        return TurnDirection.NoTurn

def triangleAreaSquared(a, b, c):
    c = cross(b - a, c - a)
    return mag(c)**2 / 4.0

def normalize(v):
    m = mag(v)
    return v / m if m != 0 else vector(0, 0, 0)

def normal(polygon):
    n = len(polygon)
    v = vector(0, 0, 0)

    if n < 3:
        return v

    for index in range(n):
        item = polygon[index % n]
        next = polygon[(index + 1) % n]

        v.x += (next.y - item.y) * (next.z + item.z)
        v.y += (next.z - item.z) * (next.x + item.x)
        v.z += (next.x - item.x) * (next.y + item.y)

    return normalize(v)

def getBarycentricTriangleCoordinates(a, b, c, p):
    alpha = beta = gamma = -2 * epsilon

    v0 = c - a
    v1 = b - a
    v2 = p - a

    dot00 = dot(v0, v0)
    dot01 = dot(v0, v1)
    dot02 = dot(v0, v2)
    dot11 = dot(v1, v1)
    dot12 = dot(v1, v2)

    denom = dot00 * dot11 - dot01 * dot01

    if abs(denom) < epsilon:
        return alpha, beta, gamma

    alpha = (dot11 * dot02 - dot01 * dot12) / denom
    beta = (dot00 * dot12 - dot01 * dot02) / denom
    gamma = 1.0 - alpha - beta

    return alpha, beta, gamma

def pointInsideOrEdgeTriangle(a, b, c, p):
    alpha, beta, gamma = getBarycentricTriangleCoordinates(a, b, c, p)
    return alpha >= -epsilon and beta >= -epsilon and gamma >= -epsilon

def isEar(index, polygon, normal):
    n = len(polygon)

    if n < 3:
        return False

    if n == 3:
        return True

    prevIndex = (index - 1 + n) % n
    itemIndex = index % n
    nextIndex = (index + 1) % n

    prev = polygon[prevIndex]
    item = polygon[itemIndex]
    next = polygon[nextIndex]

    u = normalize(item - prev)

    if turn(prev, u, normal, next) != TurnDirection.Right:
        return False

    for i in range(n):
        if i in (prevIndex, itemIndex, nextIndex):
            continue

        if pointInsideOrEdgeTriangle(prev, item, next, polygon[i]):
            return False

    return True

def getBiggestEar(polygon, normal):
    n = len(polygon)

    if n == 3:
        return 0

    if n == 0:
        return -1

    maxIndex = -1
    maxArea = float("-inf")

    for index in range(n):
        if isEar(index, polygon, normal):
            prev = polygon[(index - 1 + n) % n]
            item = polygon[index % n]
            next = polygon[(index + 1) % n]

            area = triangleAreaSquared(prev, item, next)

            if area > maxArea:
                maxIndex = index
                maxArea = area

    return maxIndex

def convex(polygon, normal):
    n = len(polygon)

    if n < 3:
        return False

    if n == 3:
        return True

    polygonTurn = TurnDirection.NoTurn

    for index in range(n):
        prev = polygon[(index - 1 + n) % n]
        item = polygon[index % n]
        next_item = polygon[(index + 1) % n]

        u = normalize(item - prev)
        item_turn = turn(prev, u, normal, next_item)

        if item_turn == TurnDirection.NoTurn:
            continue

        if polygonTurn == TurnDirection.NoTurn:
            polygonTurn = item_turn

        if polygonTurn != item_turn:
            return False

    return True

def clockwiseOriented(polygon, normal):
    n = len(polygon)

    if n < 3:
        return False

    orientationSum = 0.0

    for index in range(n):
        prev = polygon[(index - 1 + n) % n]
        item = polygon[index % n]
        next = polygon[(index + 1) % n]

        edge = item - prev

        toNextPoint = next - item

        v = cross(edge, toNextPoint)

        orientationSum += dot(v, normal)

    return orientationSum < 0.0

def makeClockwiseOrientation(polygon, normal):
    if len(polygon) < 3:
        return

    if not clockwiseOriented(polygon, normal):
        polygon.reverse()


def fanTriangulation(polygon):
    triangles = []
    for index in range(1, len(polygon) - 1):
        triangles.append(Triangle(polygon[0], polygon[index], polygon[index + 1]))
    return triangles

def cutTriangulation(polygon, normal):
    triangles = []
    makeClockwiseOrientation(polygon, normal)

    while polygon:
        index = getBiggestEar(polygon, normal)

        if index == -1:
            return []

        n = len(polygon)

        prev = polygon[(index - 1 + n) % n]
        item = polygon[index % n]
        next = polygon[(index + 1) % n]

        triangles.append(Triangle(prev, item, next))

        del polygon[index]

        if len(polygon) < 3:
            break

    return triangles if len(polygon) == 2 else []

def triangulate(polygon):
    if len(polygon) < 3:
        return []

    if len(polygon) == 3:
        return [Triangle(polygon[0], polygon[1], polygon[2])]

    n = normal(polygon)

    if convex(polygon, n):
        return fanTriangulation(polygon), n

    return cutTriangulation(polygon, n), n