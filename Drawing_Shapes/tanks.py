import pygame
import random

pygame.init()

#fire_sound = pygame.mixer.Sound('explosion.wav')
explosion_sound = pygame.mixer.Sound('explosion.wav')

pygame.mixer.music.load('explosion.wav')
#pygame.mixer.music.play(-1)

FPS = 20    # frames per second

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 155, 0)
yellow = (200, 200, 0)
light_green = (0, 255, 0)
light_yellow = (255, 255, 0)
light_red = (255, 0, 0)

# screen size
display_width = 800
display_height = 600

left_click = (1, 0, 0)

# tank dimensions
tank_width = 40
tank_height = 20
turret_width = 5
wheel_width = 5

# ground dimensions
ground_height = 35

# Set size and title
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Tanks')
# icon = pygame.image.load('snake_icon.png')
# pygame.display.set_icon(icon)

block_size = 20

# img = pygame.image.load('snake_head.png')
# apple_img = pygame.image.load('red_apple.png')
#
# img = pygame.transform.scale(img, (block_size, block_size))
# apple_img = pygame.transform.scale(apple_img, (block_size, block_size))

clock = pygame.time.Clock()     # used to set frames per second

# fonts used
small_font = pygame.font.SysFont('comicsansms', 25)
med_font = pygame.font.SysFont('comicsansms', 50)
large_font = pygame.font.SysFont('comicsansms', 75)



def score(score):
    text = small_font.render('Score: {}'.format(score), True, black)
    gameDisplay.blit(text, [0, 0])


def text_objects(text, color, size):
    if size == 'small':
        text_surface = small_font.render(text, True, color)
    elif size == 'medium':
        text_surface = med_font.render(text, True, color)
    elif size == 'large':
        text_surface = large_font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def text_to_button(msg, color, btn_x, btn_y, btn_width, btn_height, size='small'):
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = (btn_x + btn_width / 2, btn_y + btn_height / 2)
    gameDisplay.blit(text_surf, text_rect)

def message_to_screen(msg, color, y_displace=0, size = 'small'):
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = (display_width / 2, display_height / 2 + y_displace)
    gameDisplay.blit(text_surf, text_rect)

def button(text, x, y, width, height, inactive_color, active_color, action=None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < cur[0] < x + width and y < cur[1] < y + height:
        pygame.draw.rect(gameDisplay, active_color, (x, y, width, height))
        if click == left_click and action is not None:
            if action == 'quit':
                pygame.quit()
                quit()
            if action == 'controls':
                game_controls()
            if action == 'play':
                game_loop()
            if action == 'main':
                game_intro()
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height))
    text_to_button(text, black, x, y, width, height)

def tank(x, y, tur_pos):
    x = int(x)
    y = int(y)

    possible_turrets = [(x - 27, y - 2),
                        (x - 26, y - 5),
                        (x - 25, y - 8),
                        (x - 23, y - 12),
                        (x - 20, y - 14),
                        (x - 18, y - 15),
                        (x - 15, y - 17),
                        (x - 13, y - 19),
                        (x - 11, y - 21)]




    pygame.draw.circle(gameDisplay, black, (x, y), int(tank_height / 2))
    pygame.draw.rect(gameDisplay, black, (x - tank_height, y, tank_width,tank_height))
    pygame.draw.line(gameDisplay, black, (x, y), possible_turrets[tur_pos], turret_width)


    start_x = 15
    for i in range(7):
        pygame.draw.circle(gameDisplay, black, (x - start_x, y + 20), wheel_width)
        start_x -= 5

    return possible_turrets[tur_pos]

def enemy_tank(x, y, tur_pos):
    x = int(x)
    y = int(y)

    possible_turrets = [(x + 27, y - 2),
                        (x + 26, y - 5),
                        (x + 25, y - 8),
                        (x + 23, y - 12),
                        (x + 20, y - 14),
                        (x + 18, y - 15),
                        (x + 15, y - 17),
                        (x + 13, y - 19),
                        (x + 11, y - 21)]




    pygame.draw.circle(gameDisplay, black, (x, y), int(tank_height / 2))
    pygame.draw.rect(gameDisplay, black, (x - tank_height, y, tank_width,tank_height))
    pygame.draw.line(gameDisplay, black, (x, y), possible_turrets[tur_pos], turret_width)


    start_x = 15
    for i in range(7):
        pygame.draw.circle(gameDisplay, black, (x - start_x, y + 20), wheel_width)
        start_x -= 5

    return possible_turrets[tur_pos]

def health_bars(player_health, enemy_health):
    if player_health > 75:
        player_health_color = green
    elif player_health > 50:
        player_health_color = yellow
    else:
        player_health_color = red

    if player_health < 0:
        player_health = 0

    if enemy_health > 75:
        enemy_health_color = green
    elif enemy_health > 50:
        enemy_health_color = yellow
    else:
        enemy_health_color = red

    if enemy_health < 0:
        enemy_health = 0

    pygame.draw.rect(gameDisplay, player_health_color, [680, 25, player_health, 25])
    pygame.draw.rect(gameDisplay, enemy_health_color, [20, 25, enemy_health, 25])


def power(level):
    text = small_font.render('Power: {}%'.format(level), True, black)
    gameDisplay.blit(text, [display_width / 2, 0])

def barrier(x_location, random_height, barrier_width):
    pygame.draw.rect(gameDisplay, black, [x_location, display_height - random_height, barrier_width, random_height])


def explosion(x, y, size=50):
    pygame.mixer.Sound.play(explosion_sound)
    explode = True
    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        startPoint = (x, y)
        colorChoices = [red, light_red, yellow, light_yellow]
        magnitude = 1
        while magnitude < size:
            exploding_bit_x = x + random.randrange(-1 * magnitude, magnitude)
            exploding_bit_y = y + random.randrange(-1 * magnitude, magnitude)

            color = random.choice(colorChoices)
            pygame.draw.circle(gameDisplay, color, (exploding_bit_x, exploding_bit_y), random.randrange(1, 5))
            magnitude += 1
            pygame.display.update()
        clock.tick(100)
        explode = False


def fire_shell(x_y, enemy_tank_x, enemy_tank_y, tur_pos, gun_power, barrier_x_location, barrier_width, barrier_random_height):
    #pygame.mixer.Sound.play(fire_sound)
    fire = True
    starting_shell = list(x_y)
    print("FIRE!")
    damage = 0

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.draw.circle(gameDisplay, red, (starting_shell[0], starting_shell[1]), 5)
        starting_shell[0] -= (12 - tur_pos) * 2
        starting_shell[1] += int(((starting_shell[0] - x_y[0]) * 0.015 / (gun_power / 50)) ** 2 - (tur_pos + tur_pos / (12 - tur_pos)))

        if starting_shell[1] > display_height - ground_height:
            print('Last shell: ({}, {})'.format(starting_shell[0], starting_shell[1]))
            hit_x = int(starting_shell[0] * (display_height - ground_height) / starting_shell[1])
            hit_y = display_height - ground_height
            print('Impact: ({}, {})'.format(hit_x, hit_y))
            if enemy_tank_x - 10 < hit_x < enemy_tank_x + 10:
                print('critical hit!')
                damage = 25
            elif enemy_tank_x - 15 < hit_x < enemy_tank_x + 15:
                print('hard hit!')
                damage = 18
            elif enemy_tank_x - 25 < hit_x < enemy_tank_x + 25:
                print('medium hit!')
                damage = 15
            elif enemy_tank_x - 35 < hit_x < enemy_tank_x + 35:
                print('light hit!')
                damage = 10
            explosion(hit_x, hit_y)
            fire = False


        check_x_1 = starting_shell[0] <= barrier_x_location + barrier_width
        check_x_2 = starting_shell[0] >= barrier_x_location
        check_y_1 = starting_shell[1] <= display_height
        check_y_2 = starting_shell[1] >= display_height - barrier_random_height

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            print('Last shell: ({}, {})'.format(starting_shell[0], starting_shell[1]))
            hit_x = int(starting_shell[0])
            hit_y = int(starting_shell[1])
            print('Impact: ({}, {})'.format(hit_x, hit_y))
            explosion(hit_x, hit_y, size=20)
            fire = False
        pygame.display.update()
        clock.tick(100)

    return damage

def enemy_fire_shell(x_y, p_tank_x, p_tank_y, tur_pos, gun_power, barrier_x_location, barrier_width, barrier_random_height):
    damage = 0
    current_power = 1
    power_found = False
    while not power_found and current_power < 100:
        current_power += 1
        fire = True
        starting_shell = list(x_y)

        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # pygame.draw.circle(gameDisplay, red, (starting_shell[0], starting_shell[1]), 5)
            starting_shell[0] += (12 - tur_pos) * 2
            starting_shell[1] += int(
                ((starting_shell[0] - x_y[0]) * 0.015 / (current_power / 50)) ** 2 - (tur_pos + tur_pos / (12 - tur_pos)))

            if starting_shell[1] > display_height - ground_height:
                hit_x = int(starting_shell[0] * (display_height - ground_height) / starting_shell[1])
                if p_tank_x - 15 < hit_x < p_tank_x + 15:
                    print('target aqcuired')
                    power_found = True
                elif p_tank_x - 15 < hit_x < p_tank_x + 15:
                    print('hard hit!')
                    damage = 18
                elif p_tank_x - 25 < hit_x < p_tank_x + 25:
                    print('medium hit!')
                    damage = 15
                elif p_tank_x - 35 < hit_x < p_tank_x + 35:
                    print('light hit!')
                    damage = 10
                fire = False

            check_x_1 = starting_shell[0] <= barrier_x_location + barrier_width
            check_x_2 = starting_shell[0] >= barrier_x_location
            check_y_1 = starting_shell[1] <= display_height
            check_y_2 = starting_shell[1] >= display_height - barrier_random_height

            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                fire = False


    fire = True
    starting_shell = list(x_y)
    print("FIRE!")

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #gun_power = current_power
        gun_power = random.randrange(int(current_power * 0.9), int(current_power * 1.1))

        pygame.draw.circle(gameDisplay, red, (starting_shell[0], starting_shell[1]), 5)
        starting_shell[0] += (12 - tur_pos) * 2
        starting_shell[1] += int(((starting_shell[0] - x_y[0]) * 0.015 / (gun_power / 50)) ** 2 - (tur_pos + tur_pos / (12 - tur_pos)))



        if starting_shell[1] > display_height - ground_height:
            print('Last shell: ({}, {})'.format(starting_shell[0], starting_shell[1]))
            hit_x = int(starting_shell[0] * (display_height - ground_height) / starting_shell[1])
            hit_y = display_height - ground_height
            print('Impact: ({}, {})'.format(hit_x, hit_y))
            if p_tank_x -15 < hit_x < p_tank_x + 15:
                print('hit target!')
                damage = 25
            explosion(hit_x, hit_y)
            fire = False


        check_x_1 = starting_shell[0] <= barrier_x_location + barrier_width
        check_x_2 = starting_shell[0] >= barrier_x_location
        check_y_1 = starting_shell[1] <= display_height
        check_y_2 = starting_shell[1] >= display_height - barrier_random_height

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            print('Last shell: ({}, {})'.format(starting_shell[0], starting_shell[1]))
            hit_x = int(starting_shell[0])
            hit_y = int(starting_shell[1])
            print('Impact: ({}, {})'.format(hit_x, hit_y))
            explosion(hit_x, hit_y, size=20)
            fire = False


        pygame.display.update()
        clock.tick(100)

    return damage

def pause_game():
    paused = True

    # gameDisplay.fill(white)
    message_to_screen('Game Paused', black, y_displace=-50, size='large')
    message_to_screen('Press p to get back to the game', black, y_displace=50, size='small')
    pygame.display.update()

    while paused:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

    clock.tick(15)

def game_controls():
    g_cont = True
    while g_cont:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        message_to_screen('Controls', green, y_displace=-100, size='large')
        message_to_screen('Fire: Spacebar', black, -30)
        message_to_screen('Move Turret: Up and Down arrows', black, 10)
        message_to_screen('Move Tank: Left and Right arraows', black, 50)
        message_to_screen('Power: A and D', black, 90)
        message_to_screen('Pause: P', black, 130)

        button('play', 150, 400, 100, 50, green, light_green, action='play')
        #button('main', 350, 400, 100, 50, yellow, light_yellow, action='main')
        button('quit', 550, 400, 100, 50, red, light_red, action='quit')

        pygame.display.update()
        clock.tick(15)


def game_intro():

    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        message_to_screen('Welcome to Tanks', green, y_displace=-100, size='large')
        message_to_screen('The objective of the game is to shoot and destroy', black, -30)
        message_to_screen('the enemy tank before they destroy you', black, 10)
        message_to_screen('The more enemies you destroy, the harder they are to be destroyed', black, 50)
        #message_to_screen('Press C to play or Q to quit.', black, 180)



        button('play', 150, 400, 100, 50, green, light_green, action='play')
        button('controls', 350, 400, 100, 50, yellow, light_yellow, action='controls')
        button('quit', 550, 400, 100, 50, red, light_red, action='quit')

        pygame.display.update()
        clock.tick(15)


def game_over():
    game_over = True
    while game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        message_to_screen('Game Over', green, y_displace=-100, size='large')
        message_to_screen('You died.', black, -30)

        button('Play Again', 150, 400, 150, 50, green, light_green, action='play')
        button('controls', 350, 400, 100, 50, yellow, light_yellow, action='controls')
        button('quit', 550, 400, 100, 50, red, light_red, action='quit')

        pygame.display.update()
        clock.tick(15)

def you_win():

    win = True
    while win:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        message_to_screen('You won', green, y_displace=-100, size='large')
        message_to_screen('Congratulations!.', black, -30)

        button('Play Again', 150, 400, 150, 50, green, light_green, action='play')
        button('controls', 350, 400, 100, 50, yellow, light_yellow, action='controls')
        button('quit', 550, 400, 100, 50, red, light_red, action='quit')

        pygame.display.update()
        clock.tick(15)


def game_loop():

    game_exit = False

    player_health = 100
    enemy_health = 100


    main_tank_x = display_width * 0.9
    main_tank_y = display_height * 0.9
    tank_move = 0

    enemy_tank_x = display_width * 0.1
    enemy_tank_y = display_height * 0.9

    current_tur_pos = 0
    change_tur = 0
    barrier_width = 50

    barrier_x_location = int((display_width / 2)) + random.randint(-0.1 * display_width, 0.1 * display_width)
    barrier_random_height = random.randrange(display_height * 0.1, display_height * 0.6)

    fire_power = 50
    power_change = 0

    while not game_exit:
        gameDisplay.fill(white)  # clear
        health_bars(player_health, enemy_health)
        barrier(barrier_x_location, barrier_random_height, barrier_width)
        gameDisplay.fill(green, rect=[0, display_height - ground_height, display_width, ground_height])
        gun = tank(main_tank_x, main_tank_y, current_tur_pos)
        enemy_gun = enemy_tank(enemy_tank_x, enemy_tank_y, 8)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
                pygame.quit()
                quit()
            # key press event handling to move the snake (change its direction)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tank_move = -5
                elif event.key == pygame.K_RIGHT:
                    tank_move = 5
                elif event.key == pygame.K_UP:
                    change_tur = 1
                elif event.key == pygame.K_DOWN:
                    change_tur = -1
                elif event.key == pygame.K_p:
                    pause_game()
                elif event.key == pygame.K_SPACE:
                    enemy_damage = fire_shell(gun, enemy_tank_x, enemy_tank_y, current_tur_pos, fire_power, barrier_x_location, barrier_width, barrier_random_height)

                    possible_movements = ['f', 'r']
                    movement = random.choice(possible_movements)
                    for x in range(random.randrange(0, 10)):
                        if display_width * 0.03 < enemy_tank_x < display_width * 0.3:
                            if movement == 'f':
                                enemy_tank_x += 5
                            else:
                                enemy_tank_x -= 5
                            gameDisplay.fill(white)
                            health_bars(player_health, enemy_health)
                            barrier(barrier_x_location, barrier_random_height, barrier_width)
                            gameDisplay.fill(green,
                                             rect=[0, display_height - ground_height, display_width, ground_height])
                            gun = tank(main_tank_x, main_tank_y, current_tur_pos)
                            enemy_gun = enemy_tank(enemy_tank_x, enemy_tank_y, 8)
                            clock.tick(FPS)
                    damage = enemy_fire_shell(enemy_gun, main_tank_x, main_tank_y, 8, 50, barrier_x_location,
                               barrier_width, barrier_random_height)
                    player_health -= damage
                    enemy_health -= enemy_damage
                elif event.key == pygame.K_a:
                    power_change = -1
                elif event.key == pygame.K_d:
                    power_change = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                    tank_move = 0
                if event.key == pygame.K_UP or pygame.K_DOWN:
                    change_tur = 0
                if event.key == pygame.K_a or pygame.K_d:
                    power_change = 0



        main_tank_x += tank_move
        current_tur_pos += change_tur
        fire_power += power_change

        if current_tur_pos < 0:
            current_tur_pos = 0
        elif current_tur_pos > 8:
            current_tur_pos = 8

        if main_tank_x - tank_width / 2 < barrier_x_location + barrier_width:
            main_tank_x += 5

        if fire_power < 1:
            fire_power = 1
        elif fire_power > 100:
            fire_power = 100


        power(fire_power)
        pygame.display.update()

        if player_health < 1:
            game_over()
        elif enemy_health < 1:
            you_win()

        clock.tick(FPS)

game_intro()
game_loop()
pygame.display.update()
pygame.quit()
quit()