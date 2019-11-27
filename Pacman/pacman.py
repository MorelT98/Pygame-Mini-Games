import pygame
import random
import pickle

pygame.init()
pygame.display.set_caption('Pacman')

# cell size
cell_size = 20

icon = pygame.image.load('pacman.png')
pygame.display.set_icon(icon)


# load images
pacman_img = pygame.image.load('pacman.png')
pacman_img = pygame.transform.scale(pacman_img, (cell_size, cell_size))
ghost_cyan_img = pygame.image.load('ghost_cyan.png')
ghost_cyan_img = pygame.transform.scale(ghost_cyan_img, (cell_size, cell_size))
ghost_orange_img = pygame.image.load('ghost_orange.png')
ghost_orange_img = pygame.transform.scale(ghost_orange_img, (cell_size, cell_size))
ghost_pink_img = pygame.image.load('ghost_pink.png')
ghost_pink_img = pygame.transform.scale(ghost_pink_img, (cell_size, cell_size))
ghost_red_img = pygame.image.load('ghost_red.png')
ghost_red_img = pygame.transform.scale(ghost_red_img, (cell_size, cell_size))


# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 155, 0)
yellow = (200, 200, 0)
light_green = (0, 255, 0)
light_yellow = (255, 255, 0)
light_red = (255, 0, 0)
blue = (0, 0, 155)
light_blue = (0, 0, 255)

# pacman directions
left = [0, -1]
right = [0, 1]
up = [-1, 0]
down = [1, 0]

# Ghost movement speed (1 - 100)
ghosts_speed = 50
min_ghosts_speed = 10
max_ghosts_speed = 100


# 1 = blue square
# 0 = black square
tiles = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# food
food = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 1, 1, 1, 1, 1, 2, 0, 2, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 2, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 1, 1, 2, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 2, 0, 2, 1, 1, 1, 1, 2, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 2, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# food parameters
small_food_size = 1
small_food_radius = 2 * small_food_size
small_food_score = 1

big_food_size = 2
big_food_radius = 2 * big_food_size
big_food_score = 5

# corners
corners = [(1, 1), (17, 1), (1, 15), (17, 15)]

# cell color dictionary
cell_color = {0: black, 1: light_blue}

# window dimensions
windows_size = (400, 400)
game_display = pygame.display.set_mode(windows_size)

# frames per second
FPS = 30

clock = pygame.time.Clock()

# fonta
mini_font = pygame.font.SysFont('comicsansms', 10)
small_font = pygame.font.SysFont('comicsansms', 15)
med_font = pygame.font.SysFont('comicsansms', 25)
large_font = pygame.font.SysFont('comicsansms', 50)

# score and highest score locations
score_i = 1
score_j = 17
highest_score_i = 2
highest_score_j = 17

def get_max_score():
    max_score = 0
    for i in range(len(food)):
        for j in range(len(food[i])):
            if food[i][j] == small_food_size:
                max_score += small_food_score
            elif food[i][j] == big_food_size:
                max_score += big_food_score
    return max_score

max_score = get_max_score()

def load_highest_score():
    try:
        highest_score = pickle.load(open('score.p', 'rb'))
        return int(highest_score)
    except:
        return 0

def save_highest_score(score, highest_score):
    if score > highest_score:
        pickle.dump(score, open('score.p', 'wb'))

def idx_to_coord(i, j):
    return cell_size * j, cell_size * i

def reset_food():
    global food
    # food
    food = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 1, 1, 1, 1, 1, 2, 0, 2, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 2, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 1, 1, 2, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 2, 0, 2, 1, 1, 1, 1, 2, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 2, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

def text_objects(text, color, size):
    if size == 'small':
        text_surface = small_font.render(text, True, color)
    elif size == 'large':
        text_surface = large_font.render(text, True, color)
    else:
        text_surface = med_font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def message_to_screen(msg, color, y_displace=0, size='small'):
    text_surface, text_rect = text_objects(msg, color, size)
    text_rect.center = (windows_size[0] / 2, windows_size[1] / 2 + y_displace)
    game_display.blit(text_surface, text_rect)

def create_ghosts():
    # shuffle the corners and assign them to the ghosts
    random.shuffle(corners)
    ghost_dict = {}

    # each ghost is assigned an initial location and initial direction
    ghost_dict[ghost_red_img] = [list(corners[0]), [0, 0]]
    ghost_dict[ghost_pink_img] = [list(corners[1]), [0, 0]]
    ghost_dict[ghost_orange_img] = [list(corners[2]), [0, 0]]
    ghost_dict[ghost_cyan_img] = [list(corners[3]), [0, 0]]

    return ghost_dict

def draw_food():
    for i in range(len(food)):
        for j in range(len(food[i])):
            x, y = idx_to_coord(i, j)
            x += cell_size / 2
            y += cell_size / 2
            x = int(x)
            y = int(y)
            if food[i][j] == small_food_size:
                pygame.draw.circle(game_display, yellow, [x, y], small_food_radius)
            elif food[i][j] == big_food_size:
                pygame.draw.circle(game_display, yellow, [x, y], big_food_radius)

def draw_board():
    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            # Get the corresponding coordinates of the tile
            x, y = idx_to_coord(i, j)
            # Get the corresponding color
            color = cell_color[tiles[i][j]]
            # Draw tile
            pygame.draw.rect(game_display, color, [x, y, cell_size, cell_size])

def draw_score(score, i, j, color):
    # draw score
    #i, j = (1, 17)
    x, y = idx_to_coord(i, j)
    text = mini_font.render(str(score), True, color)
    text_rect = text.get_rect()
    text_rect.center = (x + cell_size / 2, y + cell_size / 2)
    game_display.blit(text, text_rect)


def in_bounds(i, j):
    return i in range(len(tiles)) and j in range(len(tiles))

def move(i, j, direction):
    new_i = i + direction[0]
    new_j = j + direction[1]
    if in_bounds(new_i, new_j) and tiles[new_i][new_j] > 0:
        return new_i, new_j
    return i, j

def move_ghosts(ghost_dict, speed):
    for ghost in ghost_dict:
        i, j = ghost_dict[ghost][0][0], ghost_dict[ghost][0][1]
        direction = ghost_dict[ghost][1]
        if move(i, j, direction) == (i, j):
            possible_directions = []
            for new_direction in [up, down, left, right]:
                if move(i, j, new_direction) != (i, j):
                    possible_directions.append(new_direction)
            direction = random.choice(possible_directions)
            ghost_dict[ghost][1] = direction
        if random.randint(0, 100) < speed:
            ghost_dict[ghost][0][0], ghost_dict[ghost][0][1] = move(i, j, direction)


def get_ghosts_speed(score):
    return int(((max_ghosts_speed - min_ghosts_speed) / max_score) * score + min_ghosts_speed)

def draw_pacman(i, j, direction):
    head = pacman_img
    if direction == up:
        head = pygame.transform.rotate(head, 90)
    elif direction == down:
        head = pygame.transform.rotate(head, 270)
    elif direction == left:
        head = pygame.transform.rotate(head, 180)
    game_display.blit(head, list(idx_to_coord(i, j)))

def draw_ghosts(ghost_dir):
    for ghost in ghost_dir.keys():
        i, j = ghost_dir[ghost][0][0], ghost_dir[ghost][0][1]
        x, y = idx_to_coord(i, j)
        game_display.blit(ghost, [x, y])

def game_over(i, j, ghost_dict):
    # If pacman hits any of the ghosts, return -1 (game over)
    for ghost in ghost_dict.keys():
        if ghost_dict[ghost][0][0] == i and ghost_dict[ghost][0][1] == j:
            return -1

    # If pacman ate all the food, return 1 (game won)
    for i in range(len(food)):
        for j in range(len(food[i])):
            if food[i][j] > 0:
                return 0
    return 1


def game_over_loop(message, score, highest_score):
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        # save score
        save_highest_score(score, highest_score)

        message_to_screen(message, white, y_displace=-10, size='medium')
        message_to_screen('Press Enter to play again, Esc to exit', white, y_displace=20, size='small')
        pygame.display.update()
        clock.tick(100)

def game_loop():
    gaming = True

    highest_score = load_highest_score()
    score = 0
    reset_food()

    # get an initial location for pacman
    i, j = (0, 0)
    while (i, j) in corners or tiles[i][j] == 0:
        i, j = (random.randrange(0, len(tiles)), random.randrange(0, len(tiles[0])))

    # starting direction
    direction = [0, 0]
    last_direction = [0, 0]

    # Get starting location and direction of ghosts
    ghost_dict = create_ghosts()

    while gaming:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = up
                elif event.key == pygame.K_DOWN:
                    direction = down
                elif event.key == pygame.K_LEFT:
                    direction = left
                elif event.key == pygame.K_RIGHT:
                    direction = right
                last_direction = direction
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or pygame.K_DOWN or pygame.K_LEFT or pygame.K_RIGHT:
                    direction = [0, 0]

        # clear screen
        game_display.fill(black)

        draw_board()
        draw_food()

        # move pacman
        i, j = move(i, j, direction)

        # check if pacman eats food
        if food[i][j] == small_food_size:
            score += small_food_score
        elif food[i][j] == big_food_size:
            score += big_food_score
        food[i][j] = 0

        # move ghosts
        speed = get_ghosts_speed(score)
        move_ghosts(ghost_dict, speed)

        # draw ghosts
        draw_ghosts(ghost_dict)

        # draw pacman
        draw_pacman(i, j, last_direction)

        # draw score
        draw_score(score, score_i, score_j, white)
        draw_score(highest_score, highest_score_i, highest_score_j, yellow)

        # check if pacman hits any ghost or eats all the food
        game_over_ = game_over(i, j, ghost_dict)
        if game_over_ == -1:
            game_over_loop('Game Over.', score, highest_score)
        elif game_over_ == 1:
            game_over_loop('You win!', score, highest_score)

        pygame.display.update()
        clock.tick(FPS)

game_loop()