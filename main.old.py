import pygame
import math
import time
import tank

pygame.init()
display_width = 1280
display_height = 720

# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((display_width, display_height), vsync=1)
pygame.display.set_caption("Танчики")

icon = pygame.image.load("icon.jpg")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

fv4202 = pygame.transform.scale(pygame.image.load("fv4202.png"), (800, 400))

x = 200
y = 200
deg_angle = 0
rad_angle = 0
deg_diff = 0

right_turn = -30  # d/s
left_turn = 30  # d/s

max_front_speed = 100  # px/s
max_rear_speed = 40  # px/s
speed = 0  # px/s


def rot_center(image, angle, x, y):
    rotate_image = pygame.transform.rotate(image, angle)
    new_rect = rotate_image.get_rect(center=image.get_rect(center=(x, y)).center)
    return rotate_image, new_rect


last_frame_timestamp = pygame.time.get_ticks()
last_fps_update_timestamp = -999999
done = False
fps_img = None
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    now_last_diff = pygame.time.get_ticks() - last_frame_timestamp
    if now_last_diff > 10:
        last_frame_timestamp = pygame.time.get_ticks()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a] and not pressed[pygame.K_s]:
            deg_diff = left_turn
        elif pressed[pygame.K_a] and pressed[pygame.K_s]:
            deg_diff = right_turn
        if pressed[pygame.K_d] and not pressed[pygame.K_s]:
            deg_diff = right_turn
        elif pressed[pygame.K_d] and pressed[pygame.K_s]:
            deg_diff = left_turn
        if pressed[pygame.K_s]:
            speed = max_rear_speed
        elif pressed[pygame.K_w]:
            speed = - max_front_speed
        else:
            speed = 0
        if (pressed[pygame.K_s] or pressed[pygame.K_w]) and (pressed[pygame.K_a] or pressed[pygame.K_d]):
            speed = speed / 2
        frame_percent = now_last_diff * 0.001
        speed = speed * frame_percent
        deg_diff = deg_diff * frame_percent
        deg_angle = (deg_angle + deg_diff) % 360
        rad_angle = math.radians(deg_angle)
        screen.fill((0, 0, 0))
        x = x + speed * math.cos(rad_angle)
        y = y - speed * math.sin(rad_angle)
        rotated_tank = rot_center(fv4202, deg_angle, 10, 10)
        screen.blit(rotated_tank[0], (x + rotated_tank[1][0], y + rotated_tank[1][1]))
        if pygame.time.get_ticks() - last_fps_update_timestamp > 1000:
            last_fps_update_timestamp = pygame.time.get_ticks()
            fps = clock.get_fps()
            fps_img = font.render(f"{math.floor(fps)} fps x:{math.floor(x)} y:{math.floor(y)} angle:{math.floor(deg_angle)}", True, (0, 0, 255))
        screen.blit(fps_img, (20, 20))
        pygame.display.flip()

    clock.tick(1000)

