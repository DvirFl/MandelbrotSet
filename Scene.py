import pygame
import numpy as np
from OpenGL.GL import *
# from OpenGL.GL import glGetUniformLocation, glUniform1f

class Scene:
    def __init__(self, mouse_pos, prev_mouse_pos, scale, resolution, center):
        self.mouse_pos = np.array(mouse_pos)
        self.prev_mouse_pos = prev_mouse_pos
        self.scale = scale
        self.resolution = resolution
        self.point = ( mouse_pos) / np.array(resolution) 
        self.radius = 0.1
        self.power = 2
        self.iters_num = 100
        
        
    def handle_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    quit()
                case pygame.MOUSEMOTION:
                    self.mouse_pos = np.array(pygame.mouse.get_pos())
                    self.mouse_pos[1] =  self.resolution[1] - self.mouse_pos[1]
                    self.point = (self.mouse_pos) / np.array(self.resolution) 
                case pygame.FINGERDOWN:
                    self.mouse_pos = np.array(pygame.mouse.get_pos())
                    self.mouse_pos[1] =  self.resolution[1] - self.mouse_pos[1]
                    self.point = (self.mouse_pos) / np.array(self.resolution) 
                case pygame.KEYDOWN:
                
                    match event.key:
                        case pygame.K_UP:
                            self.radius += 0.05
                            print("radius plus:", self.radius)
                        case pygame.K_DOWN:
                            self.radius -= 0.05
                            print("radius minus:", self.radius)
                        case pygame.K_ESCAPE:
                            pygame.quit()
                            quit()
                case pygame.MOUSEBUTTONDOWN:
                    self.radius = 0.1
                    print("radius:", self.radius)

    
    def set_uniforms(self, shaderProgram):
        location = glGetUniformLocation(shaderProgram, 'radius')
        glUniform1f(location, self.radius)
        location = glGetUniformLocation(shaderProgram, 'scale')
        glUniform1f(location, self.scale)
        location = glGetUniformLocation(shaderProgram, 'point')
        glUniform2fv(location,1, self.point)
        
    def get_mouse_pos(self):
        return self.mouse_pos
