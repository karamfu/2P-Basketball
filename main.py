import pygame
import random
import math

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 600

# Colors needed for this game 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up scree nsize and background
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Two Player Basketball Game')

background_img = pygame.image.load('background2.jpg')
basketball_img = pygame.image.load('basketball.png')
hoop_img = pygame.image.load('hoop.png')
power_up_img = pygame.image.load('power_up.png')

basketball_img = pygame.transform.scale(basketball_img, (50, 50))
hoop_img = pygame.transform.scale(hoop_img, (150, 150))
power_up_img = pygame.transform.scale(power_up_img, (50, 50))

font = pygame.font.Font(None, 74)

# all the necessary variables for basketball speed, angles, gravity, etc.
basketball_pos1 = [SCREEN_WIDTH // 4, SCREEN_HEIGHT - 50]
hoop_pos1 = [random.randint(100, SCREEN_WIDTH // 2 - 200), 50]
shooting1 = False
angle1 = 0
power1 = 25
gravity = 0.5
ball_speed1 = [0, 0]
score1 = 0
arrow_angle1 = 0
arrow_direction1 = 1
arrow_sway_speed1 = 0.1  
fast_ball1 = False
fast_ball_timer1 = 0
big_net1 = False
big_net_timer1 = 0

basketball_pos2 = [3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT - 50]
hoop_pos2 = [random.randint(SCREEN_WIDTH // 2 + 100, SCREEN_WIDTH - 200), 50]
shooting2 = False
angle2 = 0
power2 = 25
ball_speed2 = [0, 0]
score2 = 0
arrow_angle2 = 0
arrow_direction2 = 1
arrow_sway_speed2 = 0.1  
fast_ball2 = False
fast_ball_timer2 = 0
big_net2 = False
big_net_timer2 = 0

power_ups = []
power_up_timer = 0
power_up_interval = random.randint(6, 10) * 1000

arrow_length = 100

# 1 minute 30 seconds
game_time = 90  
start_ticks = pygame.time.get_ticks()  

# Drawing the arrow indicators for the basketballs on both sides
def draw_arrow(screen, start_pos, angle, length):
    end_pos = (start_pos[0] + length * math.cos(angle), start_pos[1] - length * math.sin(angle))
    pygame.draw.line(screen, RED, start_pos, end_pos, 5)
    pygame.draw.polygon(screen, RED, [
        (end_pos[0] + 10 * math.cos(angle - math.pi / 6), end_pos[1] - 10 * math.sin(angle - math.pi / 6)),
        (end_pos[0] + 10 * math.cos(angle + math.pi / 6), end_pos[1] - 10 * math.sin(angle + math.pi / 6)),
        end_pos
    ])

# Powerups display
def display_message(screen, message, color):
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(1500)

running = True
while running:
    screen.fill(WHITE)
    screen.blit(background_img, (0, 0))
    screen.blit(hoop_img, hoop_pos1)
    screen.blit(basketball_img, (basketball_pos1[0] - basketball_img.get_width() // 2, basketball_pos1[1] - basketball_img.get_height() // 2))
    screen.blit(hoop_img, hoop_pos2)
    screen.blit(basketball_img, (basketball_pos2[0] - basketball_img.get_width() // 2, basketball_pos2[1] - basketball_img.get_height() // 2))

    if big_net1:
        big_hoop_img1 = pygame.transform.scale(hoop_img, (200, 200))
        screen.blit(big_hoop_img1, hoop_pos1)
    else:
        screen.blit(hoop_img, hoop_pos1)

    if big_net2:
        big_hoop_img2 = pygame.transform.scale(hoop_img, (200, 200))
        screen.blit(big_hoop_img2, hoop_pos2)
    else:
        screen.blit(hoop_img, hoop_pos2)

    pygame.draw.line(screen, BLACK, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 5)

    score_text1 = font.render(f'Player 1 Score: {score1}', True, RED)
    score_text2 = font.render(f'Player 2 Score: {score2}', True, BLUE)
    screen.blit(score_text1, (10, 10))
    screen.blit(score_text2, (SCREEN_WIDTH // 2 + 10, 10))


    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    timer_text = font.render(f'Time: {game_time - seconds}', True, BLACK)
    timer_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(timer_text, timer_rect)

    if game_time - seconds <= 0:
        running = False
        if score1 > score2:
            display_message(screen, "Player 1 Wins!", RED)
        elif score2 > score1:
            display_message(screen, "Player 2 Wins!", BLUE)
        else:
            display_message(screen, "It's a Draw!", BLACK)

    current_time = pygame.time.get_ticks()
    if current_time - power_up_timer >= power_up_interval:
        power_up_timer = current_time
        power_up_interval = random.randint(6, 10) * 1000
        power_ups.append({
            'pos': [random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 200)],
            'type': random.choice(['fast_indicator', 'slow_indicator', 'fast_ball', 'big_net'])
        })

    for power_up in power_ups:
        screen.blit(power_up_img, (power_up['pos'][0] - 25, power_up['pos'][1] - 25))

    for power_up in power_ups:
        if math.sqrt((power_up['pos'][0] - basketball_pos1[0]) ** 2 + (power_up['pos'][1] - basketball_pos1[1]) ** 2) <= 25:
            if power_up['type'] == 'fast_indicator':
                arrow_sway_speed2 = 0.3  
                pygame.time.set_timer(pygame.USEREVENT + 1, 5000)
                display_message(screen, "SPEED UP", RED)
            elif power_up['type'] == 'slow_indicator':
                arrow_sway_speed2 = 0.02
                pygame.time.set_timer(pygame.USEREVENT + 2, 5000)
                display_message(screen, "SLOW-MO", RED)
            elif power_up['type'] == 'fast_ball':
                fast_ball1 = True
                fast_ball_timer1 = pygame.time.get_ticks()
                display_message(screen, "FAST BALL", RED)
            elif power_up['type'] == 'big_net':
                big_net1 = True
                big_net_timer1 = pygame.time.get_ticks()
                display_message(screen, "BIG NET", RED)
            power_ups.remove(power_up)
            break

# The various powerup effects (moving faster, bigger net, etc.)
    for power_up in power_ups:
        if math.sqrt((power_up['pos'][0] - basketball_pos2[0]) ** 2 + (power_up['pos'][1] - basketball_pos2[1]) ** 2) <= 25:
            if power_up['type'] == 'fast_indicator':
                arrow_sway_speed1 = 0.3 
                pygame.time.set_timer(pygame.USEREVENT + 3, 5000)
                display_message(screen, "SPEED UP", BLUE)
            elif power_up['type'] == 'slow_indicator':
                arrow_sway_speed1 = 0.02
                pygame.time.set_timer(pygame.USEREVENT + 4, 5000)
                display_message(screen, "SLOW-MO", BLUE)
            elif power_up['type'] == 'fast_ball':
                fast_ball2 = True
                fast_ball_timer2 = pygame.time.get_ticks()
                display_message(screen, "FAST BALL", BLUE)
            elif power_up['type'] == 'big_net':
                big_net2 = True
                big_net_timer2 = pygame.time.get_ticks()
                display_message(screen, "BIG NET", BLUE)
            power_ups.remove(power_up)
            break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT + 1:
            arrow_sway_speed2 = 0.1
        if event.type == pygame.USEREVENT + 2:
            arrow_sway_speed2 = 0.1
        if event.type == pygame.USEREVENT + 3:
            arrow_sway_speed1 = 0.1
        if event.type == pygame.USEREVENT + 4:
            arrow_sway_speed1 = 0.1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q and (not shooting1 or fast_ball1):
                shooting1 = True
                ball_speed1[0] = power1 * math.cos(arrow_angle1)
                ball_speed1[1] = power1 * -math.sin(arrow_angle1)
                if fast_ball1:
                    ball_speed1[0] *= 2
                    ball_speed1[1] *= 2
            if event.key == pygame.K_p and (not shooting2 or fast_ball2):
                shooting2 = True
                ball_speed2[0] = power2 * math.cos(arrow_angle2)
                ball_speed2[1] = power2 * -math.sin(arrow_angle2)
                if fast_ball2:
                    ball_speed2[0] *= 2
                    ball_speed2[1] *= 2

    # specifically handling the fast ball and big net powerups
    if fast_ball1 and pygame.time.get_ticks() - fast_ball_timer1 > 7000:
        fast_ball1 = False

    if fast_ball2 and pygame.time.get_ticks() - fast_ball_timer2 > 7000:
        fast_ball2 = False

    if big_net1 and pygame.time.get_ticks() - big_net_timer1 > 10000:
        big_net1 = False

    if big_net2 and pygame.time.get_ticks() - big_net_timer2 > 10000:
        big_net2 = False

    if not shooting1:
        arrow_angle1 += arrow_sway_speed1 * arrow_direction1
        if arrow_angle1 > math.pi or arrow_angle1 < 0:
            arrow_direction1 *= -1
        draw_arrow(screen, (basketball_pos1[0], basketball_pos1[1] - basketball_img.get_height() // 2), arrow_angle1, arrow_length)

    if not shooting2:
        arrow_angle2 += arrow_sway_speed2 * arrow_direction2
        if arrow_angle2 > math.pi or arrow_angle2 < 0:
            arrow_direction2 *= -1
        draw_arrow(screen, (basketball_pos2[0], basketball_pos2[1] - basketball_img.get_height() // 2), arrow_angle2, arrow_length)

    #Handling shooting mechanics of the ball
    if shooting1:
        basketball_pos1[0] += ball_speed1[0]
        basketball_pos1[1] += ball_speed1[1]
        ball_speed1[1] += gravity
        if hoop_pos1[0] < basketball_pos1[0] < hoop_pos1[0] + hoop_img.get_width() and hoop_pos1[1] < basketball_pos1[1] < hoop_pos1[1] + hoop_img.get_height():
            score1 += 1
            arrow_sway_speed1 += 0.004
            shooting1 = False
            basketball_pos1 = [SCREEN_WIDTH // 4, SCREEN_HEIGHT - 50]
            hoop_pos1 = [random.randint(100, SCREEN_WIDTH // 2 - 200), 50]
        if basketball_pos1[0] < 0 or basketball_pos1[0] > SCREEN_WIDTH // 2 or basketball_pos1[1] > SCREEN_HEIGHT:
            shooting1 = False
            basketball_pos1 = [SCREEN_WIDTH // 4, SCREEN_HEIGHT - 50]

    if shooting2:
        basketball_pos2[0] += ball_speed2[0]
        basketball_pos2[1] += ball_speed2[1]
        ball_speed2[1] += gravity
        if hoop_pos2[0] < basketball_pos2[0] < hoop_pos2[0] + hoop_img.get_width() and hoop_pos2[1] < basketball_pos2[1] < hoop_pos2[1] + hoop_img.get_height():
            score2 += 1
            arrow_sway_speed2 += 0.004
            shooting2 = False
            basketball_pos2 = [3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT - 50]
            hoop_pos2 = [random.randint(SCREEN_WIDTH // 2 + 100, SCREEN_WIDTH - 200), 50]
        if basketball_pos2[0] < SCREEN_WIDTH // 2 or basketball_pos2[0] > SCREEN_WIDTH or basketball_pos2[1] > SCREEN_HEIGHT:
            shooting2 = False
            basketball_pos2 = [3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT - 50]

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
