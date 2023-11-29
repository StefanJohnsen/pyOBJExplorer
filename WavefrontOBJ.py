import os
from vpython import vector

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

        # Check if the file exists
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
                    self.vertex.append(vector(x, y, z))

                elif command == 'vt':  # Texture
                    x, y = map(float, data[:2])
                    self.texture.append(vector(x, y, 0))

                elif command == 'vn':  # Normal
                    x, y, z = map(float, data[:3])
                    self.normal.append(vector(x, y, z))

                elif command == 'p':  # Point
                    indices = [int(index) - 1 for index in data]
                    geometry.p.append(indices)

                elif command == 'l':  # Line
                    indices = [int(index) - 1 for index in data]
                    geometry.l.append(indices)

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

    def aabb(self): #axis align bounding box
        if not self.vertex:
            return None
        
        min_coord = vector(self.vertex[0])
        max_coord = vector(self.vertex[0])

        for v in self.vertex:
            min_coord.x = min(min_coord.x, v.x)
            min_coord.y = min(min_coord.y, v.y)
            min_coord.z = min(min_coord.z, v.z)
            max_coord.x = max(max_coord.x, v.x)
            max_coord.y = max(max_coord.y, v.y)
            max_coord.z = max(max_coord.z, v.z)

        center = (max_coord + min_coord) / 2
        size = max_coord - min_coord

        return center, size

    def translate(self, translation):    
        if not self.vertex: return
        self.vertex = [vertex + translation for vertex in self.vertex]


