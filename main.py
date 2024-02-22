import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import glGetString, GL_VERSION
from OpenGL.GLUT import glutInit
import Scene

def loadTexture(imageName):
    textureSurface = pygame.image.load(imageName)
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    return texture

# Vertex Shader
VERTEX_SHADER = """
#version 120 
attribute vec3 position;
attribute vec2 texcoords;
varying vec2 Texcoords;

void main() {
    gl_Position = vec4(position, 1.0);
    Texcoords = texcoords;
}
"""

# Fragment Shader
FRAGMENT_SHADER = """
#version 120 
varying vec2 Texcoords;
uniform sampler2D tex;
uniform float radius;
uniform float scale;

void main() {
    if (distance(Texcoords, vec2(0.5, 0.5)) > radius) {
        gl_FragColor = texture2D(tex, Texcoords);
    }
    else
        gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
}
"""

def main():
    # glutInit()
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    # pygame.display.set_mode(display, DOUBLEBUF | OPENGL | pygame.SCALED)

    print("OpenGL version:", glGetString(GL_VERSION).decode())

    # Compile shaders and program
    shaderProgram = compileProgram(
        compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    )

    # Define vertices and buffer
    vertices = [
    0, 0, 0.0,  -1.0, -1.0,  # Bottom left
     1, 0, 0.0,  1.0, -1.0,  # Bottom right
     0,  1, 0.0,  -1.0, 1.0,  # Top left
     1, 0, 0.0,  1.0, -1.0,  # Bottom right
     0,  1, 0.0,  -1.0, 1.0,  # Top left
     1,  1, 0.0,  1.0, 1.0  # Top right
    ]
    
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, (GLfloat * len(vertices))(*vertices), GL_STATIC_DRAW)

    # Position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Texture coord attribute
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

        # Load texture
    scn = Scene.Scene((0, 0), (0, 0), 1.0, (800, 600), (0, 0))
    texture = loadTexture("res/textures/box0.bmp")
    glBindTexture(GL_TEXTURE_2D, texture)
    glViewport(0, 0, 800, 600)
    # Main loop
    while True:
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         quit()
        scn.handle_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(shaderProgram)
        # update uniforms of the shader program (Dvir, you can read about uniforms in the OpenGL documentation or ask chatGPT)
        scn.set_uniforms(shaderProgram)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__':
    main()
