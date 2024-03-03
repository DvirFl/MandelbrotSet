import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import glGetString, GL_VERSION
from OpenGL.GLUT import glutInit
import Scene
import platform

def is_mac_os():
    return platform.system() == 'Darwin'

def loadTexture(imageName, dim=2):
    textureSurface = pygame.image.load(imageName)
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    texture = glGenTextures(1)
    if dim == 2:
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    else:
        glBindTexture(GL_TEXTURE_1D, texture)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage1D(GL_TEXTURE_1D, 0, GL_RGBA, width, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    return texture

# Vertex Shader
VERTEX_SHADER = """
#version 410 
attribute vec3 position;
attribute vec2 texcoords;
varying vec2 Texcoords;

void main() {
    gl_Position = vec4(position, 1.0);
    Texcoords = texcoords;
}
"""

# Fragment Shader
FRAGMENT_SHADER_1 = """
#version 410 
varying vec2 Texcoords;
uniform sampler2D tex;
uniform float radius;
uniform float scale;
uniform dvec2 point;

void main() {
    if (distance(Texcoords, point) > radius) {
        gl_FragColor = texture2D(tex, Texcoords);
    }
    else
        gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
}
"""

FRAGMENT_SHADER_2 = """
#version 410
uniform sampler1D tex;
uniform vec2 point;
uniform float scale;
uniform int iter;
uniform float p;

varying vec2 Texcoords;

void main() {
	vec2 z, c;
    int levels = 1;

	c.x = (Texcoords.x - 0.5) * scale - point.x;
	c.y = (Texcoords.y - 0.5) * scale - point.y;

	int i;
	z = c;
	for(i=0; i<iter; i++) {
        float r = sqrt(z.x * z.x + z.y * z.y), angle = atan(z.y,z.x);     
        float sn = sin(angle*p);
        float cn = cos(angle*p);
		float x = cn*pow(r,p) + c.x;
		float y = sn*pow(r,p) + c.y;
       // float x =  (z.x * z.x - z.y * z.y) + c.x;
		//float y = (z.y * z.x + z.x * z.y) + c.y;
		if((x * x + y * y) > 4.0) break;
		z.x = x;
		z.y = y;
	}

	gl_FragColor = texture1D(tex, (i == iter ? 0.0 : float(i)) / levels * 128.0f/iter);
}
"""

FRAGMENT_SHADER_3 = """
#version 120

varying vec2 Texcoords;
uniform float scale; // uniform variable for scale

void main()
{
    vec2 p = Texcoords * 2.0 - 1.0; // transform the coordinate to [-1, 1] range
    vec3 col = vec3(1.0); // initial color (white)

    // apply scale
    p *= scale;

    // scale and wrap the coordinates
    p *= 1.5 / max(abs(p.x), abs(p.y));
    
    // determine if the current pixel is in a 'removed' area
    for (int i = 0; i < 4; ++i) {
        if (all(lessThan(fract(p * pow(5.0, float(i))), vec2(0.5))))
            col *= 0.0; // make the pixel black
        p = abs(p * 2.0) - 1.0;
    }

    gl_FragColor = vec4(col, 1.0);
}
"""

def main():
    # glutInit()
    pygame.init()
    display = (800, 800)
    window = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    # pygame.display.set_mode(display, DOUBLEBUF | OPENGL | pygame.SCALED)

    version = gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION)
    print("Supported GLSL version:", version)
    print("OpenGL version:", glGetString(GL_VERSION).decode())

    # Compile shaders and program
    shaderProgram = compileProgram(
        compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        compileShader(FRAGMENT_SHADER_2, GL_FRAGMENT_SHADER)
    )

    # Define vertices and buffer
    #correct coordinates for windows
    if is_mac_os():
    #correct coordinates for mac
        vertices = [
        0, 0, 0.0,  -1.0, -1.0,  # Bottom left
        1, 0, 0.0,  1.0, -1.0,  # Bottom right
        0,  1, 0.0,  -1.0, 1.0,  # Top left
        1, 0, 0.0,  1.0, -1.0,  # Bottom right
        0,  1, 0.0,  -1.0, 1.0,  # Top left
        1,  1, 0.0,  1.0, 1.0  # Top right
        ]
    else:
        vertices = [
        -1, -1, 0.0,  0.0, 0.0,  # Bottom left
        1, -1, 0.0,  1.0, 0.0,  # Bottom right
        -1,  1, 0.0,  0.0, 1.0,  # Top left
        1, -1, 0.0,  1.0, 0.0,  # Bottom right
        -1,  1, 0.0,  0.0, 1.0,  # Top left
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
    scn = Scene.Scene((0, 0), (0, 0), 2, display, (0.0, 0.0))
    # texture = loadTexture("res/textures/box0.bmp")
    texture = loadTexture("res/textures/pal.bmp", 1)

    # glBindTexture(GL_TEXTURE_2D, texture)
    # glViewport(0, 0, 800, 800)
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
