# OBJExplorer
Embrace the power of Python and VPython in 3D modeling with OBJExplorer, a tool designed for parsing and visualizing Wavefront OBJ and MTL files. This application harnesses the flexibility of Python and the graphical capabilities of VPython to offer a dynamic, interactive experience in exploring 3D models. Whether it's for educational purposes, design visualization, or simply for exploring the world of 3D graphics, OBJExplorer provides an intuitive and comprehensive platform for users to delve into the details of textures, materials, and geometries in OBJ files. Ideal for students, designers, and enthusiasts in 3D modeling, OBJExplorer is your gateway to experiencing 3D models in a new dimension.

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

The OBJExplorer's OBJ parser is processing a wide range of data encapsulated within Wavefront OBJ files. Its capabilities include:

- Vertex Data Processing: Accurately reads and interprets vertex coordinates, forming the fundamental geometric structure of the 3D models.
- Normal Vectors Interpretation: Efficiently handles normal vectors, essential for realistic lighting and shading effects in 3D visualization.
- Texture Coordination: Capable of parsing texture coordinates, facilitating detailed and accurate texturing of 3D model surfaces.
- Robust Index Handling: Versatile in managing various types of indices (also negative), including faces, lines, and points, ensuring a thorough representation of the 3D object structure.
  
Designed to be thorough and precise, this parser allows for a detailed and faithful reconstruction of 3D models, encompassing all critical aspects of the OBJ format.

# MTL Data Parsing Capabilities

The OBJExplorer's MTL parser excels in interpreting and processing material attributes associated with Wavefront MTL files, enabling detailed and realistic material representations for 3D models. Its key capabilities include:

- Material Name Recognition: Identifies and assigns names to different materials, facilitating organized and intuitive material management.
- Diffuse Color (Kd) Processing: Interprets the diffuse color attributes, critical for defining the primary color of materials under white light.
- Ambient Color (Ka) Interpretation: Handles ambient color values, which contribute to the color seen in shadows and under indirect lighting.
- Specular Color (Ks) Analysis: Reads specular color properties, essential for determining the color and intensity of highlights and reflections.
- Emission Color (Ke) Parsing: Capable of interpreting emission color, defining the self-illumination properties of materials.
- Specular Exponent (Ns) Handling: Manages the specular exponent attribute, influencing the sharpness and focus of specular highlights.
- Optical Density (Ni) Reading: Processes optical density values, related to the refractive properties of materials.
- Dissolve Factor (d) Interpretation: Deals with dissolve attributes, essential for understanding the transparency or opacity of materials.
- Illumination Model (illum) Determination: Identifies the illumination model, crucial for defining how the material interacts with light.
- Texture Maps (map_Kd, map_Ka, map_Ks, map_Ns, map_d): Parses various texture maps, enriching the visual complexity and realism of materials.

This parser's detailed approach ensures a nuanced and accurate portrayal of material properties, enhancing the visual fidelity of 3D models rendered from OBJ files.
