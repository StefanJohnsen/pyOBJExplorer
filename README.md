# pyOBJExplorer

Explore 3D visualization of Wavefront OBJ models with [pyOBJParser](https://github.com/StefanJohnsen/pyOBJParser), a showcase of how to integrate VPython and pyOBJParser. pyOBJExplorer offers an intuitive and straightforward solution, allowing users to delve into the intricate details of textures, materials, and geometries within OBJ files. Ideal for students, designers, and 3D modeling enthusiasts, pyOBJExplorer is an excellent tool for experiencing and interacting with 3D models in a user-friendly environment.

# VPython (Visual Python)
[VPython](https://en.wikipedia.org/wiki/VPython) is a lightweight and simple Python library for creating interactive 3D visualizations and simulations, often used in education to teach concepts like physics and computer science through hands-on 3D experiences. Testing Wavefront OBJ files larger than 10 MB for simulation is not recommended.


![OBJExplorer](https://github.com/StefanJohnsen/pyOBJExplorer/blob/main/objFiles/explorer.png)

### Following files is included
- `Explorer.py` The main file to run. It can also be executed from the command line with a specified OBJ file.
- `WavefrontOBJ.py` A standalone parser for OBJ files (a copy from : [pyOBJParser](https://github.com/StefanJohnsen/pyOBJParser))
- `WavefrontMTL.py` A standalone parser for MTL files (a copy from : [pyOBJParser](https://github.com/StefanJohnsen/pyOBJParser))
- `Triangulate.py` Used for converting polygon faces in OBJ files into triangles through fan and earcut triangulation techniques.

### Dependencies
- os
- sys
- numpy
- [vpython](https://pypi.org/project/vpython/)
- atexit
  
# Install vpython
```
pip install vpython
```

# Usage

From the command line, simply enter 'explorer.py' followed by the file name.<br>
Please ensure to close the browser upon completion to restore command line control.

```
python Explorer.py .\objFiles\rubikcube.obj
```
![rubikcube](https://github.com/StefanJohnsen/pyOBJExplorer/blob/main/objFiles/rubikcube.png)
<br>*Rubik's cube with standard color*
```
python Explorer.py -w .\objFiles\rubikcube.obj
```
![rubikcube](https://github.com/StefanJohnsen/pyOBJExplorer/blob/main/objFiles/rubikcube-wire.png)
<br>*Rubik's cube with wireframe*
```
python Explorer.py -b .\objFiles\drill.obj
```
![rubikcube](https://github.com/StefanJohnsen/pyOBJExplorer/blob/main/objFiles/drill-box.png)
<br>*Drill with texture and axis align bounding box*

# VPython Controls Guide

Mouse controls only
- Rotate: Click and drag with the right mouse button to rotate the scene.
- Zoom: Scroll the middle mouse wheel to zoom in and out.
  
Mouse Controls and Keyboard
- Rotate: `Ctrl` + click and drag with the left mouse button to rotate the scene.
- Pan: `Shift` + click and drag with the left mouse button to pan the scene.

# License
This software is released under the MIT License terms.
