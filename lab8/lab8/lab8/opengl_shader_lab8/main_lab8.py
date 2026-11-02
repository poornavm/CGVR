"""OpenGL 3.3: VAO/VBO, separate GLSL shaders and homogeneous 2D transforms."""
from pathlib import Path
import ctypes
import math
import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


def model_matrix(x, y, angle, scale, shear, reflected):
    c, s = math.cos(angle), math.sin(angle)
    t = np.array([[1, 0, x], [0, 1, y], [0, 0, 1]], dtype=np.float32)
    r = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=np.float32)
    h = np.array([[1, shear, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32)
    scaling = np.diag([-scale if reflected else scale, scale, 1]).astype(np.float32)
    return t @ r @ h @ scaling


def main():
    pygame.init()
    program = vao = vbo = None
    try:
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.set_mode((1000, 720), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption('Lab 8 | Arrows move | Q/E rotate | Z/X scale | A/D shear | F reflect | R reset | Esc quit')
        root = Path(__file__).resolve().parent
        program = compileProgram(
            compileShader((root / 'vertex_lab8.glsl').read_text(), GL_VERTEX_SHADER),
            compileShader((root / 'fragment_lab8.glsl').read_text(), GL_FRAGMENT_SHADER))
        vertices = np.array([[-1,-.8,1,0,0], [1,-.8,0,1,0], [0,1,0,0,1]], dtype=np.float32)
        vao, vbo = glGenVertexArrays(1), glGenBuffers(1)
        glBindVertexArray(vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(8))
        glEnableVertexAttribArray(1)
        glUseProgram(program)
        model_location = glGetUniformLocation(program, 'model')
        projection_location = glGetUniformLocation(program, 'projection')
        # Fixed initial window; aspect correction preserves the triangle proportions.
        glViewport(0, 0, 1000, 720)
        projection = np.diag([1 / (3 * 1000 / 720), 1 / 3, 1]).astype(np.float32)
        glUniformMatrix3fv(projection_location, 1, GL_FALSE, np.ascontiguousarray(projection.T))
        x = y = angle = shear = 0.0
        scale, reflected, running = 1.0, False, True
        clock = pygame.time.Clock()
        while running:
            dt = min(clock.tick(60) / 1000, .05)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: running = False
                    if event.key == pygame.K_f: reflected = not reflected
                    if event.key == pygame.K_r:
                        x = y = angle = shear = 0.0
                        scale, reflected = 1.0, False
            k = pygame.key.get_pressed()
            x += (k[pygame.K_RIGHT] - k[pygame.K_LEFT]) * dt
            y += (k[pygame.K_UP] - k[pygame.K_DOWN]) * dt
            angle += (k[pygame.K_q] - k[pygame.K_e]) * dt
            scale = max(.1, min(3, scale + (k[pygame.K_x] - k[pygame.K_z]) * dt))
            shear = max(-2, min(2, shear + (k[pygame.K_d] - k[pygame.K_a]) * dt))
            matrix = model_matrix(x, y, angle, scale, shear, reflected)
            glUniformMatrix3fv(model_location, 1, GL_FALSE, np.ascontiguousarray(matrix.T))
            glClearColor(.035, .05, .09, 1)
            glClear(GL_COLOR_BUFFER_BIT)
            glDrawArrays(GL_TRIANGLES, 0, 3)
            pygame.display.flip()
    finally:
        if vbo is not None: glDeleteBuffers(1, [vbo])
        if vao is not None: glDeleteVertexArrays(1, [vao])
        if program is not None: glDeleteProgram(program)
        pygame.quit()


if __name__ == '__main__':
    main()
