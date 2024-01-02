import pygame
import time


class Map():
    def __init__(self, screen):
        self.screen = screen
        self.viewport_size = pygame.display.get_surface().get_size()
        self.original_image = pygame.image.load("town1.png")
        self.offset = [0, 0]
        self.orig_metric_width = 150
        self.viewport_metric_width = 30
        self.bullets = []
        self.orig_size = self.original_image.get_size()
        self.calc_sizes()
        self.last_recalc_timestamp = time.time()
        self.recalc_cd = 0.01
        self.recalc_step = 5
        self.transform_coof = 1

    def calc_sizes(self):
        vo_scale_coof = self.orig_metric_width / self.viewport_metric_width
        map_target_width = self.viewport_size[0] * vo_scale_coof
        self.transform_coof = map_target_width / self.orig_size[0]
        self.transformed_img = pygame.transform.scale(self.original_image,
                                                      (self.transform_coof * self.orig_size[0],
                                                       self.transform_coof * self.orig_size[1]))

    def center_on(self, object):
        self.offset = [
            -object.x + self.viewport_size[0] / 2,
            -object.y + self.viewport_size[1] / 2
        ]
