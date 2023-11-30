# OBJExplorer
Embrace the power of Python and VPython with OBJExplorer, a tool designed for parsing and visualizing Wavefront OBJ and MTL files. This solution gives the flexibility of Python and the graphical capabilities of VPython to offer a dynamic, interactive experience in exploring 3D models. Whether it's for educational purposes, design visualization, or simply for exploring the world of 3D graphics, OBJExplorer provides an intuitive and easy solution for users to delve into the details of textures, materials, and geometries in OBJ files. Ideal for students, designers, and enthusiasts in 3D modeling, OBJExplorer is your gateway to experiencing 3D models in a new dimension.

![OBJExplorer](https://github.com/StefanJohnsen/OBJExplorer/blob/main/objFiles/rubikcube.png)

### Following files is included
- `Explorer.py` The main file to run. It can also be executed from the command line with a specified OBJ file.
- `WavefrontOBJ.py` A standalone parser for OBJ files, which can be utilized in other contexts.
- `WavefrontMTL.py` A standalone parser for MTL files, also usable independently in various projects.
- `Triangulate.py` Used for converting polygon faces in OBJ files into triangles through fan and earcut triangulation techniques.

# Visualization
[VPython](https://pypi.org/project/vpython/) is required to use `Explorer.py`
```
pip install vpython
```
# OBJ Data Parsing Capabilities

The OBJExplorer's OBJ parser is processing a wide range of data encapsulated within Wavefront OBJ files. It reads vertices, texture coordinates, normals and geometrical elements like points, lines, faces. Notably, it is capable of interpreting all types of faces, including triangles, quads, and more complex polygons (with both positive and negative indices).

Here are some sample formats of faces that OBJ parser can interpret:

```
# Triangle
f 1 2 3 
f 1//1 2//2 3//3 # triangle with vertex and normal
f 1/1/1 2/2/2 3/3/3 # triangle with vertex, texture and normal

# Quad
f 1 2 3 4
f 1//1 2//2 3//3 4//4 # quad with vertex and normal
f 1/1/1 2/2/2 3/3/3 4/4/4 # quad with vertex, texture and normal

# Polygon
f 1 2 3 4 5 6 ....
f 1//1 2//2 3//3 4//4 5//5 6//6 ... # polygon with vertex and normal
f 1/1/1 2/2/2 3/3/3 4/4/4 5/5/5 6/6/6 ... # polygon with vertex, texture and normal

# Also negative indices is supported
```

# MTL Data Parsing Capabilities

The OBJExplorer's MTL parser is designed to handle the most common material data found in Wavefront MTL files, providing essential functionality for 3D model materials. For those who require additional data types, the parser's code is straightforward and user-friendly, making it easy to understand and extend as needed.

Following material data is supported:

```
newmtl Material
Kd 0.5 0.5 0.5
Ka 0.0 0.0 0.0
Ks 0.5 0.5 0.5
Ke 0.0 0.0 0.0
Ns 168.89702
Ni 1.0
d 1.0
illum 2
map_Kd pic1.jpg
map_Ka pic2.jpg
map_Ks pic3.jpg
map_Ns pic4.jpg
map_d pic5.jpg
```

# How to Get Started

To begin using the OBJExplorer, start by examining the Explore.py script. This script is the heart of the operation. To set everything up, you'll need just a few lines of code:

```
from vpython import *
from WavefrontOBJ import WavefrontOBJ
from WavefrontMTL import WavefrontMTL
import Triangulate

# Create an instance of the WavefrontOBJ parser
obj = WavefrontOBJ()
# Load your OBJ file
obj.load(file)

# Create an instance of the WavefrontMTL parser
mtl = WavefrontMTL()
# Load the associated MTL file
mtl.load(obj.mtllib)

# Now, explore the geometry of your OBJ file with the loaded materials
explore_geometry(obj, mtl)
```

# License
This software is released under the MIT License terms.

🌟 Supporting OBJExplorer 
If you find OBJExplorer useful or interesting, please consider giving it a star on GitHub 😊

