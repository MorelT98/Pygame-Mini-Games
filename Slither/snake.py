import pygame
import random

def dist(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

pygame.init()

FPS = 10    # frames per second

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

# screen size
display_width = 800
display_height = 600

# Set size and title
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Slither')
icon = pygame.image.load('snake_icon.png')
pygame.display.set_icon(icon)

block_size = 20

img = pygame.image.load('snake_head.png')
apple_img = pygame.image.load('red_apple.png')

img = pygame.transform.scale(img, (block_size, block_size))
apple_img = pygame.transform.scale(apple_img, (block_size, block_size))

clock = pygame.time.Clock()     # used to set frames per second

# fonta
small_font = pygame.font.SysFont('comicsansms', 25)
med_font = pygame.font.SysFont('comicsansms', 50)
large_font = pygame.font.SysFont('comicsansms', 75)



def score(score):
    text = small_font.render('Score: {}'.format(score), True, black)
    gameDisplay.blit(text, [0, 0])

# Display all blocks in the snake list
def snake(block_size, snake_list):
    if direction == 'right':
        head = pygame.transform.rotate(img, 270)

    if direction == 'left':
        head = pygame.transform.rotate(img, 90)

    if direction == 'up':
        head = img

    if direction == 'down':
        head = pygame.transform.rotate(img, 180)

    gameDisplay.blit(head, [snake_list[-1][0], snake_list[-1][1]])
    for x_y in snake_list[:-1]:
        pygame.draw.rect(gameDisplay, green, [x_y[0], x_y[1], block_size, block_size])

def text_objects(text, color, size):
    if size == 'small':
        text_surface = small_font.render(text, True, color)
    elif size == 'medium':
        text_surface = med_font.render(text, True, color)
    elif size == 'large':
        text_surface = large_font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def message_to_screen(msg, color, y_displace=0, size = 'small'):
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = (display_width / 2, display_height / 2 + y_displace)
    gameDisplay.blit(text_surf, text_rect)

def pause_game():
    paused = True

    # gameDisplay.fill(white)
    message_to_screen('Game Paused', black, y_displace=-50, size='large')
    message_to_screen('Press space bar to get back to the game', black, y_displace=50, size='small')
    pygame.display.update()

    while paused:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False

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
        message_to_screen('Welcome to Slither', green, y_displace=-100, size='large')
        message_to_screen('The objective of the game is to eat red apples', black, -30)
        message_to_screen('The more apples you eat, the longer you get', black, 10)
        message_to_screen('If you run into yourself, or the edges, you die!', black, 50)
        message_to_screen('Press C to play or Q to quit.', black, 180)
        pygame.display.update()
        clock.tick(15)


def game_loop():
    global direction

    game_exit = False
    game_over = False

    # snake head position
    lead_x = display_width / 2
    lead_y = display_height / 2

    # snake head direction
    lead_x_change = 10
    lead_y_change = 0

    # apple position
    rand_apple_x = random.randrange(0, display_width - block_size, 10)
    rand_apple_y = random.randrange(0, display_height - block_size, 10)

    snake_list = [[lead_x, lead_y]]

    direction = 'right'
    while not game_exit:
        if game_over == True:
            #gameDisplay.fill(white)  # clear screen
            message_to_screen('Game over', red, y_displace=-50, size='large')
            message_to_screen('Press C to play again or Q to quit', black, y_displace=50, size='medium')
            pygame.display.update()

        while game_over == True:

            # se set game over to false to get out of the loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    game_over = False
                    if event.key == pygame.K_q: # if press q, close the game
                        game_exit = True
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            # key press event handling to move the snake (change its direction)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                    direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                    direction = 'right'
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                    direction = 'up'
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0
                    direction = 'down'
                elif event.key == pygame.K_SPACE:
                    pause_game()

        # if the snake goes out of bounds
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            game_over = True


        # Move snake head
        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(white)     # clear

        # draw apple
        gameDisplay.blit(apple_img, [rand_apple_x, rand_apple_y])
        #pygame.draw.rect(gameDisplay, red, [rand_apple_x, rand_apple_y, block_size, block_size])

        snake_head = [lead_x, lead_y]

        # move snake body: add new snake head and remove the oldest block, since it now moved
        snake_list.append(snake_head)
        snake_list.pop(0)

        # display the snake
        snake(block_size, snake_list)

        # display the score
        score(len(snake_list) - 1)

        pygame.display.update()


        # if the snake eats itself
        if len(snake_list) > 1:
            for block in snake_list[:-1]:
                if block[0] == lead_x and block[1] == lead_y:
                    game_over = True
                    break

        # if the snake eats the apple
        if dist(lead_x, lead_y, rand_apple_x, rand_apple_y) < block_size:
            # get a new random location for the apple
            rand_apple_x = random.randrange(0, display_width - block_size, 10)
            rand_apple_y = random.randrange(0, display_height - block_size, 10)
            # Add the old apple to the snake body
            snake_list.append(snake_head)
        clock.tick(FPS)

game_intro()
game_loop()
pygame.display.update()
pygame.quit()
quit()