import pygame
import math

pygame.init()
display_width = 1280
display_height = 720

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Танчики")

icon = pygame.image.load("icon.jpg")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

fv4202 = pygame.transform.scale(pygame.image.load("fv4202.png"), (400, 200))


x = 200
y = 200
deg_angle = 0
rad_angle = 0
max_front_speed = 5
max_rear_speed = 2
speed = 0

def rot_center(image, angle, x, y):
    rotate_image = pygame.transform.rotate(image, angle)
    new_rect = rotate_image.get_rect(center=image.get_rect(center=(x,y)).center)
    return rotate_image, new_rect

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_a] and not pressed[pygame.K_s]:
        deg_angle+=0.5
    elif pressed[pygame.K_a] and pressed[pygame.K_s]:
        deg_angle-=0.5
    if pressed[pygame.K_d] and not pressed[pygame.K_s]:
        deg_angle -= 0.5
    elif pressed[pygame.K_d] and pressed[pygame.K_s]:
        deg_angle += 0.5
    if pressed[pygame.K_s]: speed = max_rear_speed
    elif pressed[pygame.K_w]: speed = - max_front_speed
    else: speed = 0

    if (pressed[pygame.K_s] or pressed[pygame.K_w]) and (pressed[pygame.K_a] or pressed[pygame.K_d]):
        speed = speed/2


    rad_angle = math.radians(deg_angle)
    screen.fill((0,0,0))
    x = x + speed*math.cos(rad_angle)
    y = y - speed * math.sin(rad_angle)
    rotated_tank = rot_center(fv4202, deg_angle, 10,10)
    screen.blit(rotated_tank[0], (x+rotated_tank[1][0], y+rotated_tank[1][1]))
    pygame.display.flip()
    clock.tick(120)