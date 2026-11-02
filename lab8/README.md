# Experiment 8 — Vertex and Fragment Shaders

Two implementations are supplied. The OpenGL program directly satisfies the experiment title. The Unity version mirrors the folder arrangement and automatic setup of the attached Lab 9; Unity uses ShaderLab/HLSL and is not a standalone OpenGL program.

## 1. Standalone OpenGL (recommended for this experiment)
Requires Python 3.10+ and a graphics driver supporting OpenGL 3.3 core.
Open a terminal in `opengl_shader_lab8`, then run:

    python -m pip install -r requirements.txt
    python main_lab8.py

A red/green/blue triangle appears with smoothly interpolated colours. Shader compile/link errors are printed in the terminal. A remote desktop or VM may need GPU support.

## 2. Unity project (similar to Lab 9)
In Unity Hub, choose Add > Add project from disk and select `unity_shader_lab8` (the folder containing Assets, Packages and ProjectSettings). Use Unity 6000.3.0f1, matching the attachment, or allow a compatible Unity 6 editor to upgrade the project. This project uses the Built-in Render Pipeline.

Wait for import and script compilation. The editor automatically generates and saves the triangle scene, mesh and material. If needed, use the menu **Lab 8 > Create or Open Shader Scene**. Press Play and click the Game view to give it keyboard focus. Legacy Input Manager is selected in the included settings; if importing these assets into another project, set Active Input Handling to Input Manager (Old) or Both.

The manifest and editor version files intentionally use Unity's required names `manifest.json` and `ProjectVersion.txt`.

## Controls (both versions)
- Arrow keys: translation
- Q / E: anticlockwise / clockwise rotation
- Z / X: decrease / increase uniform scale
- A / D: decrease / increase X shear
- F: toggle reflection across the Y-axis
- R: reset transformations
- Escape: close standalone OpenGL window

## Principle and algorithm
1. Define three vertices with position and RGB colour attributes.
2. Compile a vertex shader and fragment shader; link the OpenGL shader program.
3. Upload vertex data to a VBO and describe attributes in a VAO.
4. Construct homogeneous matrices for scaling/reflection S, shear H, rotation R and translation T.
5. Compose M = T * R * H * S. Column vectors are transformed right to left.
6. The vertex shader applies projection * M to each position and passes its colour onward.
7. Rasterization interpolates vertex colours. The fragment shader writes each fragment's interpolated RGB colour with alpha 1.
8. Draw and update transformations from keyboard input.

OpenGL uses 3 x 3 matrices for (x, y, 1). Unity embeds the same operations in 4 x 4 matrices and applies the camera view/projection afterward. No light or texture is required.

## Lab mapping
Aim: implement two-dimensional geometric transformations using homogeneous coordinates and transformation matrices.
Course outcome CO2: apply 2D graphics transformations for graphical object manipulation.
Bloom level: L3 — Apply.
Learning objectives: coordinate transformations; matrix operations; translation, rotation, scaling, reflection and shearing; homogeneous coordinates; OpenGL programming.

Expected result: a coloured triangle rendered by vertex and fragment shaders responds to all five transformation types. This is the expected result, not a claim of execution on your machine.

## Validation
Python syntax and matrix composition are checked during packaging. Unity Editor and graphical execution must be checked on a machine with Unity/OpenGL installed; these runtime checks were not performed in the packaging environment.
