import pygame
import math


def rot_center(image, angle, x, y):
    rotate_image = pygame.transform.rotate(image, angle)
    new_rect = rotate_image.get_rect(center=image.get_rect(center=(x, y)).center)
    return rotate_image, new_rect


def custom_center_rotate(image, pos, angle, originPos):
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_tp = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_tp.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
    return rotated_image, rotated_image_rect


class Tank():
    def __init__(self, map):
        self.map = map
        self.x = 640
        self.y = 360
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

        self.inert_stop_fb = 3
        self.inert_stop_lr = 5
        self.min_fb = 1
        self.min_lr = 0.5
        self.body_orig = pygame.image.load("body T-34 85.png")
        self.body_orig_metric_width = 5.964
        orig_size = self.body_orig.get_size()
        vo_scale_coof = self.body_orig_metric_width / self.map.viewport_metric_width
        map_target_width = self.map.viewport_size[0] * vo_scale_coof
        transform_coof = map_target_width / orig_size[0]
        self.body_orig = pygame.transform.scale(self.body_orig,
                                                (transform_coof * orig_size[0], transform_coof * orig_size[1]))

        self.turret_orig = pygame.image.load("turret T-34 85.png")
        self.turret_rotate_center_orig = [496, 100]
        self.turret_orig_metric_width = 6
        self.turret_angle = 0
        self.target_turret_angle = 0
        orig_size = self.turret_orig.get_size()
        vo_scale_coof = self.turret_orig_metric_width / self.map.viewport_metric_width
        map_target_width = self.map.viewport_size[0] * vo_scale_coof
        transform_coof = map_target_width / orig_size[0]
        self.turret_orig = pygame.transform.scale(self.turret_orig,
                                                  (transform_coof * orig_size[0], transform_coof * orig_size[1]))
        self.turret_rotate_center = [self.turret_rotate_center_orig[0] * transform_coof,
                                     self.turret_rotate_center_orig[1] * transform_coof]
        print(self.turret_rotate_center)
        self.body = self.body_orig
        self.turret = self.turret_orig

    def render(self):
        self.map.screen.blit(self.body[0], (
        self.x + self.body[1][0] + self.map.offset[0], self.y + self.body[1][1] + self.map.offset[1]))
        self.map.screen.blit(self.turret[0], (self.turret[1][0], self.turret[1][1]))

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
        self.body = rot_center(self.body_orig, math.degrees(self.turn_angle), 0, 0)
        # self.turret = rot_center(self.turret_orig, self.turret_angle, 10, 10)

        self.target_turret_angle = self.target_turret_angle + 90
        self.turret_angle = self.turret_angle + 90
        raznost = self.target_turret_angle - self.turret_angle

        if (raznost < 0 and raznost > -180) or raznost > 180:
            self.turret_angle -= 1
        elif (raznost > 0 and raznost<= 180) or raznost < -180:
            self.turret_angle += 1

        self.turret_angle = abs(self.turret_angle % 360)
        self.target_turret_angle = abs(self.target_turret_angle % 360)
        self.target_turret_angle = self.target_turret_angle - 90
        self.turret_angle = self.turret_angle - 90
        self.turret = custom_center_rotate(self.turret_orig, (self.x + self.map.offset[0], self.y + self.map.offset[1]), self.turret_angle, self.turret_rotate_center)

    def aim(self, coors):
        dxy = [coors[0] - self.x - self.map.offset[0], coors[1] - self.y - self.map.offset[1]]
        if dxy[0] == 0:
            dxy[0] = 0.001
        if dxy[0] < 0:
            self.target_turret_angle = int(-math.degrees(math.atan(dxy[1] / dxy[0])))
        else:
            self.target_turret_angle = int(-math.degrees(math.atan(dxy[1] / dxy[0])) + 180)
