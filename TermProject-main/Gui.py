import pygame

class Gui:
    
    #Creating initial screen
    screen_width, screen_height = 1080, 720
    screen = pygame.display.set_mode((screen_width, screen_height))

    #Game Variables
    ROW_COUNT = 6
    COLUMN_COUNT = 7

    # Load images for GUI
    bg_img = pygame.image.load('Yellowbackground.jpg')
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
    wooden_button_image = pygame.image.load('wooden_button.png')
    wooden_button_image = pygame.transform.scale(wooden_button_image, (250, 75))
    instructions_image = pygame.image.load('game_rules.png')
    instructions_image = pygame.transform.scale(instructions_image, (350, 400))

    # Set the size of the individual game board sections
    SECTIONS = 100
    RADIUS = int(SECTIONS/2-5)
    game_width = COLUMN_COUNT * SECTIONS
    game_height = (ROW_COUNT+1) * SECTIONS
    size = (game_width, game_height)

    # Set color for main text
    blacktextcolor = (0,0,0)

    # Set the size of the individual game board sections
    SECTIONS = 100
    RADIUS = int(SECTIONS/2-5)
    game_width = COLUMN_COUNT * SECTIONS
    game_height = (ROW_COUNT+1) * SECTIONS
    size = (game_width, game_height)
