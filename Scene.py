import pygame
import numpy as np
from OpenGL.GL import *
# from OpenGL.GL import glGetUniformLocation, glUniform1f

class Scene:
    def __init__(self, mouse_pos, prev_mouse_pos, scale, resolution, center):
        self.mouse_pos = np.array(mouse_pos)
        self.prev_mouse_pos = np.array(prev_mouse_pos)
        self.scale = scale
        self.resolution = resolution
        self.point = center
        self.radius = 0.1
        self.power = 7
        self.iters_num = 120
        
        
    def handle_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    quit()
                case pygame.MOUSEMOTION:
                    self.mouse_pos = np.array(pygame.mouse.get_pos())
                    self.mouse_pos[1] =  self.resolution[1] - self.mouse_pos[1]
                    self.point += (self.mouse_pos - self.prev_mouse_pos) * self.scale / np.array(self.resolution)
                    self.prev_mouse_pos = np.array(self.mouse_pos) 
                case pygame.FINGERDOWN:
                    self.mouse_pos = np.array(pygame.mouse.get_pos())
                    self.mouse_pos[1] =  self.resolution[1] - self.mouse_pos[1]
                    self.point -= (self.mouse_pos - self.prev_mouse_pos) * self.scale / np.array(self.resolution)
                    self.prev_mouse_pos = np.array(self.mouse_pos) 
                case pygame.KEYDOWN:
                
                    match event.key:
                        case pygame.K_UP:
                            self.scale *= 1.15
                            print("radius plus:", self.scale)
                        case pygame.K_DOWN:
                            self.scale *= 0.85
                            print("radius minus:", self.scale)
                        case pygame.K_ESCAPE:
                            pygame.quit()
                            quit()
                case pygame.MOUSEBUTTONDOWN:
                    self.radius = 0.1
                    print("radius:", self.radius)

    
    def set_uniforms(self, shaderProgram):
        location = glGetUniformLocation(shaderProgram, 'p')
        glUniform1d(location, self.power)
        location = glGetUniformLocation(shaderProgram, 'iter')
        glUniform1i(location, self.iters_num)
        location = glGetUniformLocation(shaderProgram, 'radius')
        glUniform1d(location, self.radius)
        location = glGetUniformLocation(shaderProgram, 'scale')
        glUniform1d(location, self.scale)
        location = glGetUniformLocation(shaderProgram, 'point')
        glUniform2dv(location,1, self.point)
        
    def get_mouse_pos(self):
        return self.mouse_pos
