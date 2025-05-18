import pygame
import random

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
BLUE = (0, 102, 204)


#Font
font = pygame.font.SysFont(None, 24)

#kecepatan bola dan gravitasi
ball_speed_x = random.choice([-5, 5]) #perbesar variasi kecepatan bola
ball_speed_y = 0
gravity = 0.98
bounce_factor = -0.8
bounce_factor_paddle = -1.25 #perbesar faktor pantulan pada paddle AI

#pengaturan bola
ball_radius = 10
ball_x = screen_width // 2
ball_y = 400

#paddle AI
paddle_width = 100
paddle_height = 20
paddle_x = screen_width //2 - paddle_width // 2
paddle_y = screen_height - 100
paddle_speed = 6 #mempercepat gerakan paddle AI

#Brick
bricks = []
brick_width = 80
brick_height = 30
brick_cols = screen_width // brick_width
brick_rows = (screen_width // 2 - 50) // brick_height
brick_offset = 50

# Class Brick
class Brick:
    def __init__(self, x, y, hits):
        self.rect = pygame.Rect(x, y, brick_width, brick_height)
        self.hits = hits

    def draw(self, surface):
        if self.hits > 0:
            color = BLUE
            pygame.draw.rect(surface, color, self.rect)
            text = font.render(str(self.hits), True, WHITE)
            surface.blit(text, (
                self.rect.x + brick_width // 2 - text.get_width() // 2,
                self.rect.y + brick_height // 2 - text.get_height() // 2
            ))

for row in range(brick_rows):
    for col in range(brick_cols):
        hits = random.choices(range(0, 11), weights=[0.7] + [0.03] * 10, k=1)[0]
        x = col * brick_width
        y = row * brick_height + brick_offset
        bricks.append(Brick(x, y, hits))

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

    #gravity
    ball_speed_y += gravity


    #pantulan bola pada dinding kiri/kanan
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= screen_width:
        ball_speed_x *= -1 #dinding kiri/kanan memiliki bounce factor
    #dinding atas
    if ball_y - ball_radius <= 0:
        ball_speed_y *= bounce_factor
        ball_y = ball_radius
    #pantulan bola pada dinding bawah
    if ball_y + ball_radius >= screen_height:
        ball_y = 400
        ball_speed_y = 0
        ball_speed_x = random.choice([-5, 5]) #perbesar variasi kecepatan bola 
        ball_x = screen_width // 2
        paddle_x = screen_width // 2 - paddle_width // 2
    #pantulan bola pada paddle AI
    if  ball_y + ball_radius <= paddle_y and paddle_x <= ball_x <= paddle_x + paddle_width:
        ball_speed_y *= bounce_factor_paddle #perbesar faktor pantulan pada paddle AI
        ball_y = paddle_y - ball_radius
        # ball_speed_x *= bounce_factor_paddle #dinding kiri/kanan memiliki bounce factor
    
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

    # Brick collision
    for brick in bricks:
        if brick.hits > 0 and brick.rect.colliderect(
            pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)
        ):
            brick.hits -= 1
            ball_speed_y *= bounce_factor
            ball_speed_x *= -1
            break
    #menggambar bola
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)

    #menggambar paddle AI
    pygame.draw.rect(screen, BLACK, (paddle_x, paddle_y, paddle_width, paddle_height))
    # Gambar brick
    for brick in bricks:
        brick.draw(screen)
    #menampilkan layar
    pygame.display.flip()

    #mengatur frame rate
    clock.tick(60)

#keluar dari game
pygame.quit()