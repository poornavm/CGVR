import glfw
from OpenGL.GL import *
import numpy as np
import ctypes


# -------------------------------
# Vertex Shader
# -------------------------------
vertex_shader_source = """
#version 330 core

layout (location = 0) in vec3 aPos;

void main()
{
    gl_Position = vec4(aPos, 1.0);
}
"""


# -------------------------------
# Fragment Shader
# -------------------------------
fragment_shader_source = """
#version 330 core

out vec4 FragColor;

void main()
{
    FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
"""


# -------------------------------
# Initialize GLFW
# -------------------------------
if not glfw.init():
    raise Exception("GLFW initialization failed")


# IMPORTANT: Set OpenGL version BEFORE creating window
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(
    glfw.OPENGL_PROFILE,
    glfw.OPENGL_CORE_PROFILE
)

# Required for macOS
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)


# -------------------------------
# Create Window
# -------------------------------
window = glfw.create_window(
    800,
    600,
    "OpenGL Shader Program",
    None,
    None
)

if not window:
    glfw.terminate()
    raise Exception("Window creation failed")


# Make context current
glfw.make_context_current(window)


# -------------------------------
# Triangle vertices
# -------------------------------
vertices = np.array([
    -0.5, -0.5, 0.0,
     0.5, -0.5, 0.0,
     0.0,  0.5, 0.0
], dtype=np.float32)


# -------------------------------
# Compile Vertex Shader
# -------------------------------
vertex_shader = glCreateShader(GL_VERTEX_SHADER)

glShaderSource(
    vertex_shader,
    vertex_shader_source
)

glCompileShader(vertex_shader)


# -------------------------------
# Compile Fragment Shader
# -------------------------------
fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)

glShaderSource(
    fragment_shader,
    fragment_shader_source
)

glCompileShader(fragment_shader)


# -------------------------------
# Create Shader Program
# -------------------------------
shader_program = glCreateProgram()

glAttachShader(
    shader_program,
    vertex_shader
)

glAttachShader(
    shader_program,
    fragment_shader
)

glLinkProgram(shader_program)


# Delete shaders
glDeleteShader(vertex_shader)
glDeleteShader(fragment_shader)


# -------------------------------
# Create VAO
# -------------------------------
VAO = glGenVertexArrays(1)

glBindVertexArray(VAO)


# -------------------------------
# Create VBO
# -------------------------------
VBO = glGenBuffers(1)

glBindBuffer(
    GL_ARRAY_BUFFER,
    VBO
)

glBufferData(
    GL_ARRAY_BUFFER,
    vertices.nbytes,
    vertices,
    GL_STATIC_DRAW
)


# -------------------------------
# Vertex Attribute
# -------------------------------
glVertexAttribPointer(
    0,
    3,
    GL_FLOAT,
    GL_FALSE,
    3 * vertices.itemsize,
    ctypes.c_void_p(0)
)

glEnableVertexAttribArray(0)


# -------------------------------
# Main Loop
# -------------------------------
while not glfw.window_should_close(window):

    # Background color
    glClearColor(
        0.1,
        0.1,
        0.1,
        1.0
    )

    # Clear screen
    glClear(GL_COLOR_BUFFER_BIT)

    # Use shader program
    glUseProgram(shader_program)

    # Bind VAO
    glBindVertexArray(VAO)

    # Draw triangle
    glDrawArrays(
        GL_TRIANGLES,
        0,
        3
    )

    # Swap buffers
    glfw.swap_buffers(window)

    # Process events
    glfw.poll_events()


# -------------------------------
# Cleanup
# -------------------------------
glDeleteVertexArrays(
    1,
    [VAO]
)

glDeleteBuffers(
    1,
    [VBO]
)

glDeleteProgram(
    shader_program
)

glfw.terminate()