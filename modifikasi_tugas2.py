#import library
import pygame
import random

#inisialisasi pygame
pygame.init()

#inisialisasi jendela game
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tugas Mandiri 2")

#warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 102, 204)

#kecepatan bola
ball_speed_x = random.choice([-5, 5])
ball_speed_y = random.choice([-5, 5])

#pengaturan bola
ball_radius = 15
ball_x = screen_width // 2
ball_y = screen_height // 2

#kecepatan bola kedua
ball2_speed_x = - ball_speed_x
ball2_speed_y = random.choice([-5, 5])

#pengaturan bola kedua
ball2_radius = 15
ball2_x = screen_width // 2
ball2_y = screen_height // 2

#paddle
paddle1_width = 20
paddle1_height = 100
paddle1_x = 20
paddle1_y = screen_height // 2 - paddle1_height // 2 
paddle1_speed = 6

paddle2_width = 20
paddle2_height = 100   
paddle2_x = screen_width - (20 + paddle2_width)
paddle2_y = screen_height // 2 - paddle2_height // 2
paddle2_speed = 6

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
    ball2_x += ball2_speed_x
    ball2_y += ball2_speed_y

    #pamtulan bola
    if ball_x == ball2_x and ball_y == ball2_y:
        ball_speed_x *= -1
        # ball_speed_y *= -1
        ball2_speed_x *= -1
        # ball2_speed_y *= -1

    #pantulan bola pada dinding kiri/kanan
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= screen_width:
        ball_speed_x *= -1
        if ball_x - ball_radius <= 0:
            ball_x = ball_radius
        else:
            ball_x = screen_width - ball_radius
    
    #pantulan bola pada dinding atas/bawah
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= screen_height:
        ball_speed_y *= -1
        if ball_y - ball_radius <= 0:
            ball_y = ball_radius
        else:
            ball_y = screen_height - ball_radius
        
    #pantulan bola pada paddle
    if (paddle1_y <= ball_y + ball_radius or ball_y - ball_radius <= paddle1_y + paddle1_height ) and paddle1_x <= ball_x <= paddle1_x + paddle1_width:
        ball_speed_x *= -1
        ball_x = paddle1_x + paddle1_width + ball_radius
    if (paddle1_y <= ball_y + ball_radius or ball_y - ball_radius <= paddle1_y + paddle1_height ) and paddle2_x <= ball_x <= paddle2_x + paddle2_width:
        ball_speed_x *= -1
        ball_x = paddle2_x - ball_radius

    #gerakan paddle

    if ball_x < screen_width // 2 :
        if ball_y < paddle1_y:
            paddle1_y -= paddle1_speed
        elif ball_y > paddle1_y + paddle1_height:
            paddle1_y += paddle1_speed
    if ball_x > screen_width // 2 :
        if ball_y < paddle2_y:
            paddle2_y -= paddle2_speed
        elif ball_y > paddle2_y + paddle2_height:
            paddle2_y += paddle2_speed


    #pantulan bola pada dinding kiri/kanan
    if ball2_x - ball2_radius <= 0 or ball2_x + ball2_radius >= screen_width:
        ball2_speed_x *= -1
        if ball2_x - ball2_radius <= 0:
            ball2_x = ball2_radius
        else:
            ball2_x = screen_width - ball2_radius
    
    #pantulan bola pada dinding atas/bawah
    if ball2_y - ball2_radius <= 0 or ball2_y + ball2_radius >= screen_height:
        ball2_speed_y *= -1
        if ball2_y - ball2_radius <= 0:
            ball2_y = ball2_radius
        else:
            ball2_y = screen_height - ball2_radius
        
    #pantulan bola pada paddle
    if (paddle1_y <= ball2_y + ball2_radius or ball2_y - ball2_radius <= paddle1_y + paddle1_height ) and paddle1_x <= ball2_x <= paddle1_x + paddle1_width:
        ball2_speed_x *= -1
        ball2_x = paddle1_x + paddle1_width + ball2_radius
    if (paddle1_y <= ball2_y + ball2_radius or ball2_y - ball2_radius <= paddle1_y + paddle1_height ) and paddle2_x <= ball2_x <= paddle2_x + paddle2_width:
        ball2_speed_x *= -1
        ball2_x = paddle2_x - ball2_radius

    #gerakan paddle

    if ball2_x < screen_width // 2:
        if ball2_y < paddle1_y:
            paddle1_y -= paddle1_speed
        elif ball2_y > paddle1_y + paddle1_height:
            paddle1_y += paddle1_speed
    if ball2_x > screen_width // 2 :
        if ball2_y < paddle2_y:
            paddle2_y -= paddle2_speed
        elif ball2_y > paddle2_y + paddle2_height:
            paddle2_y += paddle2_speed
    
    #batas gerak paddle
    if paddle1_y < 0:
        paddle1_y = 0
    elif paddle1_y + paddle1_height > screen_height:
        paddle1_y = screen_height - paddle1_height
    if paddle2_y < 0:
        paddle2_y = 0
    elif paddle2_y + paddle2_height > screen_height:
        paddle2_y = screen_height - paddle2_height

    #menggambar
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
    pygame.draw.circle(screen, BLUE, (ball2_x, ball2_y), ball_radius)
    pygame.draw.rect(screen, BLACK, (paddle1_x, paddle1_y, paddle1_width, paddle1_height))
    pygame.draw.rect(screen, BLACK, (paddle2_x, paddle2_y, paddle2_width, paddle2_height))
    pygame.display.flip()

    clock.tick(60)
pygame.quit()   