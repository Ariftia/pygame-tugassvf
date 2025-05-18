import pygame
import random

#initialize pygame
pygame.init()

#initialize game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("AI Ball Bounce Game")

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 102, 204)

#font
font = pygame.font.SysFont(None, 24)

#ball speed and gravity
ball_speed_x = random.choice([-5, 5])
ball_speed_y = 0
gravity = 0.1
bounce_factor = 0.8
bounce_factor_paddle = 1.2 #increase bounce factor on AI paddle

#ball settings
ball_radius = 10
ball_x = screen_width // 2
inisial_y = 500
ball_y = inisial_y

#AI paddle
paddle_width = 100
paddle_height = 20  
paddle_x = screen_width //2 - paddle_width // 2
paddle_y = screen_height - 100
paddle_acceleration = 0.5
paddle_speed = 0

#brick settings
bricks = []
brick_width = 80
brick_height = 30
brick_cols = screen_width // brick_width
brick_rows = (screen_width // 2 - 50) // brick_height
brick_offset = 50

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

    #ball movement
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    #gravity effect
    ball_speed_y += gravity

    #bounce ball on left/right walls
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= screen_width:
        ball_speed_x *= -1*bounce_factor
    #bounce ball on bottom wall 
    if ball_y + ball_radius >= screen_height:
        ball_speed_y = 0
        ball_y = inisial_y
    #bounce ball on AI paddle
    if paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height and paddle_x <= ball_x <= paddle_x + paddle_width:
        ball_speed_y *= -1*bounce_factor_paddle
        ball_y = paddle_y - ball_radius

    #AI paddle movement
    if ball_x < paddle_x + paddle_width // 2:
        paddle_x -= paddle_speed
    elif ball_x > paddle_x + paddle_width:
        paddle_x += paddle_speed

    #limit AI paddle movement
    if paddle_x < 0:
        paddle_x = 0
        paddle_speed = 0
    elif paddle_x + paddle_width > screen_width:
        paddle_x = screen_width - paddle_width
        paddle_speed = 0

    for brick in bricks:
        if brick.hits > 0 and brick.rect.colliderect(
            pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)
        ):
            brick.hits -= 1
            ball_speed_y *= bounce_factor
            ball_speed_x *= bounce_factor
            break
    #draw AI paddle and bricks
    pygame.draw.rect(screen, BLACK, (paddle_x, paddle_y, paddle_width, paddle_height))
    
    for brick in bricks:
        brick.draw(screen)

    #draw the ball
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)

    pygame.display.flip()