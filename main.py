import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import glGetString, GL_VERSION
from OpenGL.GLUT import glutInit


# Vertex Shader
VERTEX_SHADER = """
#version 120 
attribute vec3 position;
void main() {
    gl_Position = vec4(position, 1.0);
}
"""

# Fragment Shader
FRAGMENT_SHADER = """
#version 120 
//out vec4 fragColor;
void main() {
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);  // Red color
}
"""

def main():
    glutInit()
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    print("OpenGL version:", glGetString(GL_VERSION).decode())

    # Compile shaders and program
    shaderProgram = compileProgram(
        compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    )

    # Define vertices and buffer
    vertices = [
        -1, -1, 0.0,
         1, -1, 0.0,
         -1, 1, 0.0,
         1, -1, 0.0,
         -1, 1, 0.0,
         1,  1, 0.0,
         
    ]
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, (GLfloat * len(vertices))(*vertices), GL_STATIC_DRAW)

    # Set the position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(shaderProgram)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__':
    main()
