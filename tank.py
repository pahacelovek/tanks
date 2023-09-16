import pygame
import math


def rot_center(image, angle, x, y):
    rotate_image = pygame.transform.rotate(image, angle)
    new_rect = rotate_image.get_rect(center=image.get_rect(center=(x, y)).center)
    return rotate_image, new_rect


class Tank():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 0
        self.turn_speed = 0
        self.turn_angle = 0

        self.max_front_speed = -4
        self.max_rear_speed = 3
        self.max_right_turn = -2
        self.max_left_turn = 2
        self.front_acceleration = -2
        self.rear_acceleration = 1
        self.right_acceleration = -1
        self.left_acceleration = 1

        self.inert_stop_fb = 0.5
        self.inert_stop_lr = 5
        self.min_fb = 1
        self.min_lr = 0.5

        self.body_orig = pygame.transform.scale(pygame.image.load("fv4202.png"), (800, 400))
        self.turret_orig = None

        self.body = self.body_orig
        self.turret = self.turret_orig

    def forward(self, frame_percent):
        self.speed = self.speed + (self.front_acceleration * frame_percent)
        self.speed = max(self.speed, self.max_front_speed)

    def back(self, frame_percent):
        self.speed = self.speed + (self.rear_acceleration * frame_percent)
        self.speed = min(self.speed, self.max_rear_speed)

    def left(self, frame_percent):
        self.turn_speed = self.turn_speed + (self.left_acceleration * frame_percent)
        self.turn_speed = min(self.turn_speed, self.max_left_turn)

    def right(self, frame_percent):
        self.turn_speed = self.turn_speed + (self.right_acceleration * frame_percent)
        self.turn_speed = max(self.turn_speed, self.max_right_turn)

    def lr_stop(self, frame_percent):
        self.turn_speed = self.turn_speed - (self.turn_speed * self.inert_stop_lr) * frame_percent
        if math.fabs(self.turn_speed) <= self.min_lr:
            self.turn_speed = 0

    def fb_stop(self, frame_percent):
        self.speed = self.speed - (self.speed * self.inert_stop_fb) * frame_percent
        if math.fabs(self.speed) <= self.min_fb:
            self.speed = 0


    def move(self, frame_percent):
        self.turn_angle = self.turn_angle + (self.turn_speed * frame_percent)
        self.x = self.x + self.speed * math.cos(self.turn_angle)
        self.y = self.y - self.speed * math.sin(self.turn_angle)
        self.body = rot_center(self.body_orig, math.degrees(self.turn_angle), 10, 10)
