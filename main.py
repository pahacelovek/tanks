import pygame
import math
import time
import tank


def rot_center(image, angle, x, y):
    rotate_image = pygame.transform.rotate(image, angle)
    new_rect = rotate_image.get_rect(center=image.get_rect(center=(x, y)).center)
    return rotate_image, new_rect


pygame.init()
display_width = 1280
display_height = 720

screen = pygame.display.set_mode((display_width, display_height), vsync=1)
pygame.display.set_caption("Танчики")

icon = pygame.image.load("icon.jpg")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
last_frame_timestamp = pygame.time.get_ticks()
last_fps_update_timestamp = -999999
fv4202 = tank.Tank()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    now_last_diff = pygame.time.get_ticks() - last_frame_timestamp
    if now_last_diff > 10:
        frame_percent = now_last_diff * 0.001
        last_frame_timestamp = pygame.time.get_ticks()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a] and not pressed[pygame.K_s]:
            fv4202.left(frame_percent)
        elif pressed[pygame.K_a] and pressed[pygame.K_s]:
            fv4202.right(frame_percent)
        if pressed[pygame.K_d] and not pressed[pygame.K_s]:
            fv4202.right(frame_percent)
        elif pressed[pygame.K_d] and pressed[pygame.K_s]:
            fv4202.left(frame_percent)
        if pressed[pygame.K_s]:
            fv4202.back(frame_percent)
        elif pressed[pygame.K_w]:
            fv4202.forward(frame_percent)

        if not pressed[pygame.K_w] and not pressed[pygame.K_s]:
            fv4202.fb_stop(frame_percent)
        if not pressed[pygame.K_a] and not pressed[pygame.K_d]:
            fv4202.lr_stop(frame_percent)

        fv4202.move(frame_percent)
        screen.fill((0, 0, 0))
        screen.blit(fv4202.body[0], (fv4202.x + fv4202.body[1][0], fv4202.y + fv4202.body[1][1]))
        if pygame.time.get_ticks() - last_fps_update_timestamp > 1000:
            last_fps_update_timestamp = pygame.time.get_ticks()
            fps = clock.get_fps()
            fps_img = font.render(f"{math.floor(fps)} fps x:{math.floor(fv4202.x)} y:{math.floor(fv4202.y)} angle:{math.floor(math.degrees(fv4202.turn_angle))}", True, (0, 0, 255))
        screen.blit(fps_img, (20, 20))
        pygame.display.flip()

    clock.tick(1000)
