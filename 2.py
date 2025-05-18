# Pada modifikasi ini, ditambahkan brick yang dapat dihancurkan oleh bola sebagai ritangan.
# brick dipanggil secara acak dengan jumlah yang ditentukan dan memiliki jumlah hit yang bisa diatur.
# Jika bola mengenai brick, maka brick akan berkurang satu hit.
# Jika brick sudah tidak memiliki hit, maka brick tersebut akan hilang dari layar.

# Semua bagian memiliki koefisien pantulan yang sama yaitu 0.8
# Jika bola mengenai dinding, maka bola akan memantul dengan koefisien pantulan 0.8



# Import library
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

# Define font
font = pygame.font.Font(None, 36)  # Default font with size 36

#kecepatan bola dan gravitasi
ball_speed_x = random.choice([-10,10])
ball_speed_y = 0
gravity = 0.7
bounce_factor = -0.8

#pengaturan bola
ball_radius = 15
ball_x = screen_width // 2
ball_y = 50

#paddle AI
paddle_width = 100
paddle_height = 20
paddle_x = screen_width //2 - paddle_width // 2
paddle_y = screen_height - 100
paddle_speed = 6

# Brick
brick_width = 80
brick_height = 30
brick_cols = screen_width // brick_width
brick_rows = (screen_height // 2 - 50) // brick_height
brick_offset = 50

#pengaturan brick
class Brick:
    def __init__(self, x, y, hits):
        self.rect = pygame.Rect(x, y, brick_width, brick_height)
        self.hits = hits

    def draw(self, surface):
        if self.hits > 0:
            color = (0, 102, 204)
            pygame.draw.rect(surface, color, self.rect)
            text = font.render(str(self.hits), True, WHITE)
            surface.blit(text, (
                self.rect.x + brick_width // 2 - text.get_width() // 2,
                self.rect.y + brick_height // 2 - text.get_height() // 2
            ))

# Generate bricks
bricks = []
for row in range(brick_rows):
    for col in range(brick_cols):
        hits = random.randint(0, 1)
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

    #efek gravitasi
    ball_speed_y += gravity

    #pantulan bola pada dinding kiri/kanan
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= screen_width:
        ball_speed_x *= bounce_factor
    #pantulan bola pada dinding bawah 
    if ball_y + ball_radius >= screen_height:
        ball_speed_y *= bounce_factor
        ball_y = screen_height - ball_radius #bola tidak keluar dari lapangan
    #pantulan bola pada dinding atas
    if ball_y - ball_radius <= 0:
        ball_speed_y *= bounce_factor
        ball_y = 0 + ball_radius #bola tidak keluar dari lapangan
    #pantulan bola pada paddle AI
    if paddle_y <= ball_y + ball_radius <= paddle_y + paddle_width and paddle_x <= ball_x+ball_radius and ball_x-ball_radius <= paddle_x + paddle_width:
        ball_speed_y *= bounce_factor
        ball_y = paddle_y - ball_radius

    #pantulan bola pada brick dan mengurangi hit
    for brick in bricks:
        if brick.hits > 0 and brick.rect.colliderect(
            pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)
        ):
            brick.hits -= 1
            ball_speed_y *= bounce_factor
            ball_speed_x *= bounce_factor
            break

    # Render text untuk informasi kecepatan bola
    speed_text = font.render(f"Ball Speed: {ball_speed_x} i + {ball_speed_y} j", True, (0, 0,0))  # black text
    screen.blit(speed_text, (20, 20))  # Draw text at position (20, 20)
    
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

    for brick in bricks:
        brick.draw(screen)

    #menampilkan layar
    pygame.display.flip()

    #mengatur frame rate
    clock.tick(60)

#keluar dari game
pygame.quit()