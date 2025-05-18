import pygame
import random
import math

#inisialisasi pygame
pygame.init()

#inisialisasi jendela game
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("AI Ball Bounce Game")

#warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#kecepatan bola dan gravitasi
ball_speed_x = random.choice([-5, 5])
ball_speed_y = -5
gravity = 0.5
bounce_factor = -0.8

#pengaturan bola
ball_radius = 15
ball_x = screen_width // 2
ball_y = 50

#paddle AI
paddle_width = 100
paddle_height = 20
paddle_x = screen_width //2 - paddle_width // 2
paddle_y = screen_height - 50
paddle_speed = 6

#game loop
clock = pygame.time.Clock()
run_game = True

while run_game:
    screen.fill(WHITE)

    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
    
    #gerakan bola
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    #efek gravitasi
    ball_speed_y += gravity

    #pantulan bola pada dinding kiri/kanan
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= screen_width:
        ball_speed_x *= -1
    #pantulan bola pada dinding bawah menggunakan faktor pantulan
    if ball_y + ball_radius >= screen_height:
        ball_speed_y *= bounce_factor
        ball_y = screen_height - ball_radius #bola tidak keluar dari lapangan
    #pantulan bola pada paddle AI
    if paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height and paddle_x <= ball_x <= paddle_x + paddle_width:
        ball_speed_y *= bounce_factor
        ball_y = paddle_y - ball_radius
    
    #gerakan paddle AI
    if ball_x < paddle_x + paddle_width // 2:
        paddle_x -= paddle_speed
    elif ball_x > paddle_x + paddle_width:
        paddle_x += paddle_speed
    
    #batas gerak paddle AI
    if paddle_x < 0:
        paddle_x = 0
    elif paddle_x + paddle_width > screen_width:
        paddle_x = screen_width - paddle_width

    #menggambar bola
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)

    #menggambar paddle AI
    pygame.draw.rect(screen, BLACK, (paddle_x, paddle_y, paddle_width, paddle_height))

    #menampilkan layar
    pygame.display.flip()

    #mengatur frame rate
    clock.tick(60)

#keluar dari game
pygame.quit()