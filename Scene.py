import pygame
from OpenGL.GL import *
# from OpenGL.GL import glGetUniformLocation, glUniform1f

class Scene:
    def __init__(self, mouse_pos, prev_mouse_pos, scale, resolution, center):
        self.mouse_pos = mouse_pos
        self.prev_mouse_pos = prev_mouse_pos
        self.scale = scale
        self.resolution = resolution
        self.center = center
        self.radius = 0.2
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = pygame.mouse.get_pos()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.radius += 0.05
                    print("radius plus:", self.radius)
                elif event.key == pygame.K_DOWN:
                    self.radius -= 0.05
                    print("radius minus:", self.radius)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.radius = 0.2
                print("radius:", self.radius)

    
    def set_uniforms(self, shaderProgram):
        location = glGetUniformLocation(shaderProgram, 'radius')
        glUniform1f(location, self.radius)
        location = glGetUniformLocation(shaderProgram, 'scale')
        glUniform1f(location, self.scale)
        
    def get_mouse_pos(self):
        return self.mouse_pos
