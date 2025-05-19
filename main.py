import pygame
from game import Game

# set up the app window
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# set the font for text
font = pygame.font.SysFont("Georgia", 30, bold=True)

# buttons for the menu
quit_text = font.render("Quit", True, "black")
quit_button = pygame.Rect(250, 400, 100, 60)
quit_text_center = quit_text.get_rect(center = quit_button.center)

vs_ai_text = font.render("Versus AI", True, "black")
vs_ai_button = pygame.Rect(175, 300, 250, 60)
vs_ai_text_center = vs_ai_text.get_rect(center = vs_ai_button.center)

vs_player_text = font.render("Versus Player", True, "black")
vs_player_button = pygame.Rect(175, 200, 250, 60)
vs_player_text_center = vs_player_text.get_rect(center = vs_player_button.center)

# game over buttons
play_again_text = font.render("Play Again", True, "black")
play_again_button = pygame.Rect(175, 300, 250, 60)
play_again_text_center = play_again_text.get_rect(center = play_again_button.center)

main_menu_text = font.render("Main Menu", True, "black")
main_menu_button = pygame.Rect(175, 400, 250, 60)
main_menu_text_center = main_menu_text.get_rect(center = main_menu_button.center)

# title text
chess_font = font.render("Chess", True, "black")

# game states
state = "menu"  # "menu", "game_player", "game_ai"

game = Game()
clock = pygame.time.Clock()

running = True

while running:
    screen.fill((255, 255, 255))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # main menu code
    if state == "menu":

        # draw buttons
        if quit_button.x <= mouse_x <= quit_button.x + 100 and quit_button.y <= mouse_y <= quit_button.y + 60:
            pygame.draw.rect(screen, (180, 180, 180), quit_button)
        else:
            pygame.draw.rect(screen, (110, 110, 110), quit_button)

        if vs_ai_button.x <= mouse_x <= vs_ai_button.x + 250 and vs_ai_button.y <= mouse_y <= vs_ai_button.y + 60:
            pygame.draw.rect(screen, (180, 180, 180), vs_ai_button)
        else: 
            pygame.draw.rect(screen, (110, 110, 110), vs_ai_button)

        if vs_player_button.x <= mouse_x <= vs_player_button.x + 250 and vs_player_button.y <= mouse_y <= vs_player_button.y + 60:
            pygame.draw.rect(screen, (180, 180, 180), vs_player_button)
        else:
            pygame.draw.rect(screen, (110, 110, 110), vs_player_button)


        screen.blit(quit_text, quit_text_center)
        screen.blit(vs_ai_text, vs_ai_text_center)
        screen.blit(vs_player_text, vs_player_text_center)
        screen.blit(chess_font, (250, 100))

    # play vs another person
    elif state == "game_player":
        game.board.draw(screen)

        # end of game logic
        if game.is_over:
            winner_text = ""
            if game.winner == "Draw":
               winner_text = "Draw"
            else:
                winner_text = f"{game.winner} Wins!"

            text_surface = font.render(winner_text, True, "red")
            text_rect = text_surface.get_rect(center = (300, 200))
            screen.blit(text_surface, text_rect)

            if play_again_button.x <= mouse_x <= play_again_button.x + 250 and play_again_button.y <= mouse_y <= play_again_button.y + 60:
                pygame.draw.rect(screen, (180, 180, 180), play_again_button)
            else:
                pygame.draw.rect(screen, (110, 110, 110), play_again_button)

            if main_menu_button.x <= mouse_x <= main_menu_button.x + 250 and main_menu_button.y <= mouse_y <= main_menu_button.y + 60:
                pygame.draw.rect(screen, (180, 180, 180), main_menu_button)
            else: 
                pygame.draw.rect(screen, (110, 110, 110), main_menu_button)

            screen.blit(play_again_text, play_again_text_center)
            screen.blit(main_menu_text, main_menu_text_center)

    # play vs an AI. the same as "game_player" until AI is added
    elif state == "game_ai":
        game.board.draw(screen)

        # end of game logic
        if game.is_over:
            winner_text = ""
            if game.winner == "Draw":
               winner_text = "Draw"
            else:
                winner_text = f"{game.winner} Wins!"

            text_surface = font.render(winner_text, True, "red")
            text_rect = text_surface.get_rect(center = (300, 200))
            screen.blit(text_surface, text_rect)

            if play_again_button.x <= mouse_x <= play_again_button.x + 250 and play_again_button.y <= mouse_y <= play_again_button.y + 60:
                pygame.draw.rect(screen, (180, 180, 180), play_again_button)
            else:
                pygame.draw.rect(screen, (110, 110, 110), play_again_button)

            if main_menu_button.x <= mouse_x <= main_menu_button.x + 250 and main_menu_button.y <= mouse_y <= main_menu_button.y + 60:
                pygame.draw.rect(screen, (180, 180, 180), main_menu_button)
            else: 
                pygame.draw.rect(screen, (110, 110, 110), main_menu_button)

            screen.blit(play_again_text, play_again_text_center)
            screen.blit(main_menu_text, main_menu_text_center)

    if game.promoting_pawn:
        game.handle_promotion(screen, mouse_x, mouse_y)

    pygame.display.update()

    # event handling
    for event in pygame.event.get():
        # quit
        if event.type == pygame.QUIT:
            running = False

        # mouse down
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if state == "menu":
                # button select logic
                if quit_button.collidepoint(mouse_x, mouse_y):
                    running = False
                elif vs_player_button.collidepoint(mouse_x, mouse_y):
                    state = "game_player"
                    game.__init__()
                elif vs_ai_button.collidepoint(mouse_x, mouse_y):
                    state = "game_ai"
                    game.__init__()

            # select piece logic
            elif state == "game_player":
                if not game.is_over:
                    game.board.handle_mouse_down(mouse_x, mouse_y, game)
                else:
                    if play_again_button.collidepoint(mouse_x, mouse_y):
                        game.__init__()
                    elif main_menu_button.collidepoint(mouse_x, mouse_y):
                        state = "menu"
                        game.is_over = False

            elif state == "game_ai":
                if game.is_over:
                    game.board.handle_mouse_down(mouse_x, mouse_y, game)

                else:
                    if play_again_button.collidepoint(mouse_x, mouse_y):
                        game.__init__()
                    elif main_menu_button.collidepoint(mouse_x, mouse_y):
                        state = "menu"
                        game.is_over = False
                
        # drag piece logic
        elif event.type == pygame.MOUSEMOTION:
            if state in ["game_player", "game_ai"]:
                if game.board.dragging:
                    mouse_x, mouse_y = event.pos
                    game.board.handle_mouse_motion(mouse_x, mouse_y)

        # release piece logic
        elif event.type == pygame.MOUSEBUTTONUP:
            if state in ["game_player", "game_ai"]:
                if not game.promoting_pawn:
                    mouse_x, mouse_y = event.pos
                    game.board.handle_mouse_up(mouse_x, mouse_y, game)

    # limit the frame rate so that my laptop does not sound like a jet engine
    clock.tick(60)

# closes the game when running = False
pygame.quit()
