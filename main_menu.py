import pygame
import pygame_menu

from level1 import game_loop

pygame.display.set_caption('Grupp 01')
pygame.init()
surface = pygame.display.set_mode((900, 700))

def the_main():
    def set_difficulty(value, difficulty):
        # Do the job here !
        pass

    def start_the_game():
        game_loop()
        

    menu = pygame_menu.Menu('Cats vs Aliens', 400, 300,
                        theme=pygame_menu.themes.THEME_BLUE)

    #Gör default name Boy Wonder
    menu.add.text_input('Name :', default='Eric Malmström')
    menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    menu.add.button('Play', start_the_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(surface)

