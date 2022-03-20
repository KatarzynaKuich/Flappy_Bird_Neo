import pygame, sys,random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))  # second floor to have long floor

def create_pipe():
    random_pipe_pos =random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos)) #700 created out of screen
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos-300))  # -300 space between pipes
    return bottom_pipe,top_pipe #tuple

def move_pipes(pipes):  # list of pipes left return new list pipes
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >=1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe =pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe) #flipped pipes

def check_collision(pipes):
    for pipe in pipes:
      if bird_rect.colliderect(pipe):
          print('true')
    if bird_rect.top <=-100 or bird_rect.bottom >=900: #check if bird is not to high or low
        print('collision')
# General setup
pygame.init()
clock = pygame.time.Clock()

# Game variables
gravity = 0.25
bird_movement = 0

# Game Screen
screen_width = 576
screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy game")

floor_x_pos = 0  # position of floor

# Creating the sprites and groups
bg_surface = pygame.image.load('sprites/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('sprites/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)

bird_surface = pygame.image.load('sprites/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center=(100, 512))

pipe_surface = pygame.image.load('sprites/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []  # rectangles
SPAWNPIPE = pygame.USEREVENT  # pipes spawn with clock 1200 milisec
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height =[400,600,800] #hights of pipes
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # if event.type == pygame.MOUSEBUTTONDOWN:  # on mouse click
        #  bird_movement =-12 #gravity bird down
        if event.type == pygame.KEYDOWN:  # on space
            if event.key == pygame.K_SPACE:  # on space
                bird_movement = 0
                bird_movement -= 12  # bird jump
        if event.type == SPAWNPIPE:  # our timer event spawn pipe
            pipe_list.extend(create_pipe())  # add new pipe to list
    # Drawing
    screen.fill((0, 0, 0))
    # Background
    screen.blit(bg_surface, (0, 0))

    # Bird
    bird_movement += gravity  # bird moves down with gravity
    bird_rect.centery += bird_movement
    screen.blit(bird_surface, bird_rect.center)  # put bird in the position of bird rect center
    # Pipes
    pipe_list = move_pipes(pipe_list)  # rectangles moving
    draw_pipes(pipe_list)
    check_collision(pipe_list)
    # Floor moving
    floor_x_pos -= 1  # floor move to left
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    # Set general
    pygame.display.flip()
    clock.tick(60)
