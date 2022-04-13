import pygame, sys # import pygame and sys
from pygame.locals import * # import pygame modules



def player_death(rect):
    if rect.y >= 300:
        rect.y = 99
        rect.x = 50

        print("DU DOG")

     
    

def send_back_to_main():
    import main_menu
    returnToMain = main_menu.the_main()
    returnToMain
    print("Got here")

def collision_test(rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    
    

    

    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

def platformer_file_main():
    clock = pygame.time.Clock() # set up the clock

    #DO NOT INITIALIZE PYGAME TWO TIMES IT WILL START A NEW WINDOW WHEN CLOSED
    #pygame.init() # initiate pygame

    pygame.display.set_caption('Pygame Window') # set the window name

    WINDOW_SIZE = (900,700) # set up window size

    screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate screen

    #this is how much you see of the world, could be good to put camera here
    display = pygame.Surface((300, 200))


    player_image = pygame.image.load('player.png').convert()
    #original image, needed to make this to make it go back if mirrored
    player_image_original = pygame.image.load('player.png').convert()
    #mirrored for left movement
    player_image_mirror = pygame.image.load('playermirror.png').convert()

    player_image.set_colorkey((255, 255, 255))
    player_image_original.set_colorkey((255, 255, 255))
    player_image_mirror.set_colorkey((255, 255, 255))


    grass_image = pygame.image.load('grass.png')
    TILE_SIZE = grass_image.get_width()

    dirt_image = pygame.image.load('dirt.png')

    #testing
    knd_image = pygame.image.load('KND.png')

    
    #loada mappen här för level
    game_map = load_map('level1')

    


    moving_right = False
    moving_left = False

    player_y_momentum = 0
    air_timer = 0

    player_rect = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height())
    test_rect = pygame.Rect(100,100,100,50)

    #this should be in the JSON file - irrelevant for now, always becomes type:Nonetype for some reason
    #lives = 9
    
    scroll = [0,0]

    while True: # game loop
        
        #Show this off
        #scroll[0] -= 1

        #real deal camera here
        scroll[0] += (player_rect.x-scroll[0]-200)
        scroll[1] += (player_rect.y-scroll[1]-80)


        display.fill((146,244,255))

        tile_rects = []
        y = 0
        for row in game_map:
            x = 0
            for tile in row:
                if tile == '1':
                    display.blit(dirt_image, (x * 16-scroll[0], y * 16-scroll[1]))
                if tile == '2':
                    display.blit(grass_image, (x * 16-scroll[0], y * 16-scroll[1]))
                #testing
                if tile == '3':
                    display.blit(knd_image, (x * 16-scroll[0], y * 16-scroll[1]))
                if tile != '0':
                    tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
                x += 1
            y += 1

        player_movement = [0, 0]
        if moving_right:
            player_movement[0] += 2
            #added 
            #print("movin right")
            player_image = player_image_original
        if moving_left:
            player_movement[0] -= 2
            #added
            #print("movin left")
            player_image = player_image_mirror
        player_movement[1] += player_y_momentum
        player_y_momentum += 0.2
        if player_y_momentum > 3:
            player_y_momentum = 3

        player_rect, collisions = move(player_rect, player_movement, tile_rects)

        if collisions['bottom']:
            player_y_momentum = 0
            air_timer = 0
        else:
            air_timer += 1

        display.blit(player_image, (player_rect.x+scroll[0], player_rect.y+scroll[1]))
        #display.blit(player_image_mirror, (player_rect.x, player_rect.y))

        #kollar om du dog JSON filen ska komma in här
        player_death(player_rect)

        for event in pygame.event.get(): # event loop
            if event.type == QUIT: # check for window quit
                pygame.quit() # stop pygame
                sys.exit() # stop script
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    moving_right = True
                if event.key == K_LEFT:
                    moving_left = True
                if event.key == K_UP:
                    if air_timer < 6:
                        player_y_momentum = -5
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving_right = False
                if event.key == K_LEFT:
                    moving_left = False
                    #print("Slide to the left")
                #return to menu
                if event.key == K_SPACE:
                    send_back_to_main()
                    print("Pressed SPACE")

            

        surf = pygame.transform.scale(display, WINDOW_SIZE)
        #screen.blit(surf, (0, 0))
        pygame.display.update() # update display
        clock.tick(60) # maintain 60 fps
