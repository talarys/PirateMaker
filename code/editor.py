from settings import *
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
import pygame
import sys


class Editor:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.origin = vector(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.pan_active = False
        self.pan_offset = vector()
        self.support_line_surface = pygame.Surface(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.support_line_surface.set_colorkey('green')
        self.support_line_surface.set_alpha(30)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.pan_input(event)

    def pan_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[1]:
            self.pan_active = True
            self.pan_offset = vector(mouse_pos()) - self.origin

        if not mouse_buttons()[1]:
            self.pan_active = False

        if self.pan_active:
            self.origin = vector(mouse_pos()) - self.pan_offset

        if event.type == pygame.MOUSEWHEEL:
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.origin.y -= event.y*50
            else:
                self.origin.x -= event.y*50

    def draw_tile_lines(self):
        cols = WINDOW_WIDTH//TILE_SIZE
        rows = WINDOW_HEIGHT//TILE_SIZE

        self.support_line_surface.fill('green')

        for col in range(cols+1):
            x = (self.origin.x % TILE_SIZE) + col * TILE_SIZE
            pygame.draw.line(self.support_line_surface, LINE_COLOR,
                             (x, 0), (x, WINDOW_HEIGHT))

        for row in range(rows+1):
            y = (self.origin.y % TILE_SIZE) + row * TILE_SIZE
            pygame.draw.line(self.support_line_surface, LINE_COLOR,
                             (0, y), (WINDOW_WIDTH, y))

        self.display_surface.blit(self.support_line_surface, (0, 0))

    def run(self, dt):
        self.display_surface.fill('white')
        self.draw_tile_lines()
        self.event_loop()
        pygame.draw.circle(self.display_surface, 'red', self.origin, 10)
