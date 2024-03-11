import pygame
from sys import exit
from math import floor
from Button import Button
from Board import Board
from Gui import Gui
from Database import Database

#Initialization
record = Database()
pygame.init()
running = True
mainfont = pygame.font.SysFont('comicsans', 100)
smallfont = pygame.font.SysFont('comicsans', 40)

def main_menu():
    
     pygame.display.set_caption("Connect Four - Team 15")
     screen = pygame.display.set_mode((Gui.screen_width, Gui.screen_height))

     while running:
         
          screen.blit(Gui.bg_img, (0, 0))

          menu_mouse_pos = pygame.mouse.get_pos()

          menu_text = mainfont.render('Connect Four', True, Gui.blacktextcolor)
          menu_rect = menu_text.get_rect(center=(540, 100))
         
          play_button = Button(image=Gui.wooden_button_image, pos=(540, 250),
                            text_input="Play", font=smallfont, base_color ="#d7fcd4", hovering_color="White")
          instructions_button = Button(image=Gui.wooden_button_image, pos=(540, 350),
                            text_input="Instructions", font=smallfont, base_color ="#d7fcd4", hovering_color="White")

          screen.blit(menu_text, menu_rect)

          for button in [play_button,instructions_button]:
               button.changeColor(menu_mouse_pos)
               button.update(screen)

          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
               if event.type == pygame.MOUSEBUTTONUP:
                    if play_button.checkForInput(menu_mouse_pos):
                         play()
                    if instructions_button.checkForInput(menu_mouse_pos):
                         instructions()

          pygame.display.update() 
          
def local():
    roundID = record.storeRound("Sarah", 1, "Cassidy", 2) #create the log for the round
    screen = pygame.display.set_mode((Gui.game_width, Gui.game_height))
    board = Board.create_board()
    turn = Board.goes_first()
    game_over = False
 
    Board.draw_board(board)
    pygame.display.update()
    
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    
            if event.type == pygame.MOUSEMOTION and (not game_over):
                pygame.draw.rect(screen, "Black", (0,0, Gui.game_width, Gui.SECTIONS))
                x = event.pos[0]
                pygame.draw.circle(screen, "Yellow" if turn else "Red", (x, int(Gui.SECTIONS/2)), Gui.RADIUS)
                playerturn = "Player " + str(turn + 1) + "'s Turn"
                label = smallfont.render(playerturn, True, "Yellow" if turn else "Red")
                screen.blit(label, (40, 10))
                
            pygame.display.update()
    
            if event.type == pygame.MOUSEBUTTONUP:
                if game_over:
                    review_screen()
                    
                pygame.draw.rect(screen, "Black", (0,0, Gui.game_width, Gui.SECTIONS))                
                x = event.pos[0]
                col = int(floor(x/Gui.SECTIONS))

                if Board.check_empty_space(board, col):
                    row = Board.get_next_open_row(board, col)
                    Board.fill_space(board, row, col, (turn + 1))
                    print(roundID[0])
                    record.storeMove((turn + 1), col, roundID[0])
                    
                    if Board.check_for_win(board, (turn + 1)):
                        game_over = True
                        message = "Player " + str(turn + 1) + " wins!!"
                        color = "Yellow" if turn else "Red"
                        label = smallfont.render(message, 1, color)
                        screen.blit(label, (40, 10))
                    elif Board.checkfortie(board):
                        game_over = True
                        message = "It's a tie... really?"
                        color = "White"
                        label = smallfont.render(message, 1, color)
                        screen.blit(label, (40, 10))
                        
                    turn += 1
                    turn = turn % 2
                    
                else:
                    label = smallfont.render("Invalid Move", 1, "Orange")
                    screen.blit(label, (40,10))
                        
                    
    
                Board.print_board(board)
                Board.draw_board(board)        

def review():
    
    screen = pygame.display.set_mode((Gui.game_width, Gui.game_height))
    board = Board.create_board()

    turn = record.printMoves()[1] - 1
    record.setNextMove(0)
    print("REVIEW START, Turn: Player ", (turn + 1))
    print()
    game_over = False
 
    Board.draw_board(board)
    pygame.display.update()
    
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            if event.type == pygame.MOUSEMOTION and not game_over:
                pygame.draw.rect(screen, "Black", (0,0, Gui.game_width, Gui.SECTIONS))
                x = event.pos[0]
                pygame.draw.circle(screen, "Yellow" if turn else "Red", (x, int(Gui.SECTIONS/2)), Gui.RADIUS)
                playerturn = "Review Mode: Player " + str(turn + 1) + "'s Turn"
                label = smallfont.render(playerturn, True, "Orange")
                screen.blit(label, (40, 10))
            pygame.display.update()
                
            if event.type == pygame.MOUSEBUTTONUP:
                
                review = record.printMoves()
                if review[0] == 0:
                    print("Review Over")
                    game_over = True
                    
                print("TURN: Player: ", review[1]) #Debug
                
                pygame.draw.rect(screen, "Black", (0, 0, Gui.game_width, Gui.SECTIONS))
                
                col = review[2]
                row = Board.get_next_open_row(board, col)
                Board.fill_space(board, row, col, (turn + 1))
                    
                if Board.check_for_win(board, (turn + 1)):
                    game_over = True
                    message = "Review Mode: Player " + str(turn + 1) + " wins!!"
                    label = smallfont.render(message, 1, "Orange")
                    screen.blit(label, (40, 10))
                elif Board.checkfortie(board):
                    game_over = True
                    message = "Review Mode: It's a tie... really?"
                    label = smallfont.render(message, 1, "White")
                    screen.blit(label, (40, 10))
                
                turn += 1
                turn = turn % 2

                Board.print_board(board)
                Board.draw_board(board)
                print() #end of loop
                
                if game_over and not review[0]:
                    record.currentmove = 0
                    review_screen()

def instructions():
    
     pygame.display.set_caption("Instructions")

     while running:
          Gui.screen.fill("black")
          Gui.screen.blit(Gui.bg_img,(0, 0))
          Gui.screen.blit(Gui.instructions_image, (365, 200))

          instructions_mouse_pos = pygame.mouse.get_pos()

          instructions_text = mainfont.render('Instructions', True, Gui.blacktextcolor)
          instructions_rect = instructions_text.get_rect(center = (540, 100))

          menu_button = Button(image = Gui.wooden_button_image, pos = (540, 650),
                            text_input="Main Menu", font=smallfont, base_color = "#d7fcd4", hovering_color="White")

          Gui.screen.blit(instructions_text, instructions_rect)

          for button in [menu_button]:
               button.changeColor(instructions_mouse_pos)
               button.update(Gui.screen)

          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
               if event.type == pygame.MOUSEBUTTONUP:
                    if menu_button.checkForInput(instructions_mouse_pos):
                         main_menu()

          pygame.display.update()

def play():
    
     pygame.display.set_caption("Connect 4 - Team 15")

     while running:
          Gui.screen.fill("black")
          Gui.screen.blit(Gui.bg_img, (0, 0))

          play_mouse_pos = pygame.mouse.get_pos()

          play_text = mainfont.render('Select Game Mode', True, Gui.blacktextcolor)
          play_rect = play_text.get_rect(center = (540, 100))

          local_multiplayer_button = Button(image = Gui.wooden_button_image, pos = (540,250),
                            text_input="2 Player", font=smallfont, base_color = "#d7fcd4", hovering_color="White")
          menu_button = Button(image = Gui.wooden_button_image, pos=(540,650),
                            text_input="Main Menu", font=smallfont, base_color = "#d7fcd4", hovering_color="White")

          Gui.screen.blit(play_text, play_rect)

          for button in [local_multiplayer_button, menu_button]:
               button.changeColor(play_mouse_pos)
               button.update(Gui.screen)

          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
               if event.type == pygame.MOUSEBUTTONUP:
                    if menu_button.checkForInput(play_mouse_pos):
                         main_menu()
                    if local_multiplayer_button.checkForInput(play_mouse_pos):
                         local()

          pygame.display.update()
          
def review_screen():
    
     pygame.display.set_caption("Connect 4 - Team 15")
     screen = pygame.display.set_mode((Gui.screen_width, Gui.screen_height))

     while running:
          screen.blit(Gui.bg_img, (0, 0))

          review_mouse_pos = pygame.mouse.get_pos()
          
          play_text = mainfont.render('Select Option', True, Gui.blacktextcolor)
          play_rect = play_text.get_rect(center = (540, 100))
         
          local_multiplayer_button = Button(image = Gui.wooden_button_image, pos = (540, 250),
                            text_input="New game", font=smallfont, base_color = "#d7fcd4", hovering_color="White")
          review_button = Button(image = Gui.wooden_button_image, pos = (540, 350),
                            text_input="Review Game", font=smallfont, base_color ="#d7fcd4", hovering_color="White")
          menu_button = Button(image = Gui.wooden_button_image, pos = (540, 450),
                            text_input="Main Menu", font=smallfont, base_color = "#d7fcd4", hovering_color="White")
          
          Gui.screen.blit(play_text, play_rect)
          
          for button in [local_multiplayer_button,review_button,menu_button]:
               button.changeColor(review_mouse_pos)
               button.update(Gui.screen)

          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
               if event.type == pygame.MOUSEBUTTONUP:
                    if local_multiplayer_button.checkForInput(review_mouse_pos):
                        local()
                    if review_button.checkForInput(review_mouse_pos):
                        review()
                    if menu_button.checkForInput(review_mouse_pos):
                        main_menu()

          pygame.display.update() 


main_menu()

