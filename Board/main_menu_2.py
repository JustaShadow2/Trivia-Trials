import pygame
import sys
from queryManager import *
from main import *
from const import *
WIDTH = 1280
HEIGHT = 800
FPS = 60
timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Trivia Trials')
main_menu = False
exit_menu = False
show_too_many_user_error = False
show_no_user_error = False
show_empty_name = False
show_existing_user = False
entering_user_data = False
username_enter = ''
password_enter = ''
player_list = []
username_enter_active = False
password_enter_active = False
font_heading = pygame.font.Font('freesansbold.ttf', 36)
font = pygame.font.Font('freesansbold.ttf', 24)
other_font = pygame.font.get_default_font()
game_data = None
new_game = None
# Load image
bg = pygame.transform.scale(pygame.image.load('assets/transparentduck.png'), (100, 100))
ball = pygame.transform.scale(pygame.image.load('assets/transparentduck.png'), (150, 150))
menu_command = 0

# Load logo image
logo = pygame.image.load('assets/transparentduck.png')  # Replace 'logo.png' with the path to your logo image
logo = pygame.transform.scale(logo, (100, 100))  # Scale the logo to an appropriate size


class Button:
    def __init__(self, txt, pos, width=260, height=40):
        self.text = txt
        self.pos = pos
        self.width = width
        self.height = height
        self.button = pygame.Rect(self.pos, (self.width, self.height))

    def draw(self):
        pygame.draw.rect(screen, 'light gray', self.button, 0, 5)
        pygame.draw.rect(screen, 'dark gray', self.button, 5, 5)
        text2 = font.render(self.text, True, 'black')
        text_rect = text2.get_rect(center=self.button.center)
        screen.blit(text2, text_rect.topleft)

    def check_clicked(self):
        return self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]


def draw_heading():
    heading_text = font_heading.render("Trivia Trials", True, 'white')
    screen.blit(heading_text, ((WIDTH - heading_text.get_width()) // 2, 50))
    # Blit logo onto the screen above all buttons
    screen.blit(logo, ((WIDTH - logo.get_width()) // 2, 100))  # Adjust position as needed


def draw_menu():
    command = -1
    menu_width = 300
    menu_height = 400
    menu_x = (WIDTH - menu_width) // 2
    menu_y = (HEIGHT - menu_height) // 2
    pygame.draw.rect(screen, 'black', [menu_x, menu_y, menu_width, menu_height])

    tutorials_button = Button('Tutorials', (menu_x + 20, menu_y + 20))
    tutorials_button.draw()

    button1 = Button('Start', (menu_x + 20, menu_y + 80))  # Adjusted position
    button1.draw()
    button2 = Button('Load Save', (menu_x + 20, menu_y + 140))  # Adjusted position
    button2.draw()
    button3 = Button('Highscore', (menu_x + 20, menu_y + 200))  # Adjusted position
    button3.draw()

    exit_button = Button('Exit Game', (menu_x + 20, menu_y + 260))  # Adjusted position
    exit_button.draw()

    if tutorials_button.check_clicked():
        command = 4
    if exit_button.check_clicked():
        command = 5
    if button1.check_clicked():
        command = 1
    if button2.check_clicked():
        command = 2
    if button3.check_clicked():
        command = 3

    return command


def draw_game():
    menu_btn = Button('Main Menu', ((WIDTH - 200) // 2, HEIGHT - 150))
    menu_btn.draw()
    menu = menu_btn.check_clicked()

    screen.blit(ball, ((WIDTH - 150) // 2, (HEIGHT - 150) // 2))

    return menu
def drawText(text, fontname, fontsize, text_col, x, y):
    font = pygame.font.Font(fontname, fontsize)
    text_surface = font.render(text, True, text_col)
    screen.blit(text_surface, ((x, y)))

def draw_save_screen():
    save_menu_width = 300
    save_menu_height = 400
    save_menu_x = (WIDTH - save_menu_width) // 2
    save_menu_y = (HEIGHT - save_menu_height) // 2
    pygame.draw.rect(screen, 'black', [save_menu_x, save_menu_y, save_menu_width, save_menu_height])
    pygame.draw.rect(screen, 'green', [save_menu_x, save_menu_y, save_menu_width, save_menu_height], 5)

    button_width = 260
    button_height = 40
    button_margin = 20
    button_start_y = save_menu_y + 50

    save1_btn = Button('Save 1', (save_menu_x + (save_menu_width - button_width) // 2, button_start_y),
                       width=button_width, height=button_height)
    save1_btn.draw()

    save2_btn = Button('Save 2', (
        save_menu_x + (save_menu_width - button_width) // 2, button_start_y + button_height + button_margin),
                       width=button_width, height=button_height)
    save2_btn.draw()

    save3_btn = Button('Save 3', (
        save_menu_x + (save_menu_width - button_width) // 2, button_start_y + 2 * (button_height + button_margin)),
                       width=button_width, height=button_height)
    save3_btn.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if save1_btn.check_clicked():
                game_data =  find_game_by_id(1)
                new_game = False
            elif save2_btn.check_clicked():
                game_data =  find_game_by_id(2)
                new_game = False
            elif save3_btn.check_clicked():
                game_data =  find_game_by_id(3)
                new_game = False
            if game_data == None:
                pass
            else:
                game(new_game=new_game, game_data=game_data)
    return 0


def draw_highscore_screen():
    highscore_menu_width = 400
    highscore_menu_height = 400
    highscore_menu_x = (WIDTH - highscore_menu_width) // 2
    highscore_menu_y = (HEIGHT - highscore_menu_height) // 2
    pygame.draw.rect(screen, 'black', [highscore_menu_x, highscore_menu_y, highscore_menu_width, highscore_menu_height])
    pygame.draw.rect(screen, 'green', [highscore_menu_x, highscore_menu_y, highscore_menu_width, highscore_menu_height],
                     5)

    # Display high scores
    high_scores = get_player_scores() # Get high scores from the database

    y_offset = highscore_menu_y + 50
    for player, score in high_scores.items():
        text_surface = font.render(f'{player}: {score}', True, 'white')
        screen.blit(text_surface, (highscore_menu_x + 50, y_offset))
        y_offset += 40


def draw_back_button():
    back_button = Button('Back', (20, 20), width=100, height=40)
    back_button.draw()
    if back_button.check_clicked():
        return True
    return False

def draw_player_login():
    entering_user_data = True
    rect_x = (WIDTH - 880) // 2
    rect_y = (HEIGHT - 600) // 2
    pygame.draw.rect(screen, 'black', [0, 0, 1280, 800])
    pygame.draw.rect(screen, 'white', [rect_x, rect_y, 880, 600])
    pygame.draw.rect(screen, 'black', [rect_x+BOARD_OUTLINE_OFFSET, rect_y+BOARD_OUTLINE_OFFSET, 880-(BOARD_OUTLINE_OFFSET*2), 600-(BOARD_OUTLINE_OFFSET*2)])
    #text, fontname, fontsize, text_col, x, y)
    drawText("Add Players", other_font, 40, WHITE, rect_x*2+150, rect_y+40)
    drawText("Username: ", other_font, 30, WHITE, rect_x+90, rect_y+200)
    pygame.draw.rect(screen, 'white', [rect_x+275, rect_y+200, 220, 40])
    pygame.draw.rect(screen, 'black', [rect_x+275+USER_ENTER_OFFSET, rect_y+200+USER_ENTER_OFFSET, 220-(USER_ENTER_OFFSET*2), 40-(USER_ENTER_OFFSET*2)])
    drawText("Password: ", other_font, 30, WHITE, rect_x+90, rect_y+270)
    drawText(("Player Count: "+str(len(player_list))), other_font, 30, WHITE, rect_x+90, rect_y+340)
    pygame.draw.rect(screen, 'white', [rect_x+275, rect_y+270, 220, 40])
    pygame.draw.rect(screen, 'black', [rect_x+275+USER_ENTER_OFFSET, rect_y+270+USER_ENTER_OFFSET, 220-(USER_ENTER_OFFSET*2), 40-(USER_ENTER_OFFSET*2)])
    drawText(username_enter, other_font, 30, WHITE, rect_x+277, rect_y+205)
    drawText(str("*"*len(password_enter)), other_font, 30, WHITE, rect_x+277, rect_y+275)
    add_new_user_button = Button('Add User', ((WIDTH - 880) // 2 + 160, (HEIGHT - 600) // 2 + 500))
    add_new_user_button.draw()
    add_new_user_button = Button('Start Game', ((WIDTH - 880) // 2 + 450, (HEIGHT - 600) // 2 + 500))
    add_new_user_button.draw()
    if show_too_many_user_error:
        drawText("Too Many Users Added To Game", other_font, 30, RED, (WIDTH - 880) // 2 + 230, (HEIGHT - 600) // 2 +400)
    elif show_no_user_error:
        drawText("No Users Added", other_font, 30, RED, (WIDTH - 880) // 2+ 320, (HEIGHT - 600) // 2+ 400)
    elif show_empty_name:
        drawText("You Must Fill In Username and Password Field", other_font, 30, RED, (WIDTH - 880) // 2+ 130, (HEIGHT - 600) // 2+ 400)
    elif show_existing_user:
        drawText("Name Taken", other_font, 30, RED, (WIDTH - 880) // 2+ 325, (HEIGHT - 600) // 2+ 400)
run = True
while run:
    screen.fill('black')
    timer.tick(FPS)

    draw_heading()

    if main_menu:
        menu_command = draw_menu()
        if menu_command != -1:
            main_menu = False
            if menu_command == 5:  # Exit Menu button pressed
                pygame.quit()
                sys.exit()
    else:
        if menu_command == 2:
            save_command = draw_save_screen()
            if draw_back_button():
                main_menu = True
            if save_command != 0:
                print(f'{save_command}')
                main_menu = True
        elif menu_command == 3:  # Highscore button pressed
            draw_highscore_screen()
            if draw_back_button():
                main_menu = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        elif menu_command == 1:  # Start button pressed
            screen.fill('black')
            # Display role selection screen
            dev_button = Button('Developer', (WIDTH // 2 - 100, HEIGHT // 2 - 50), width=200)
            dev_button.draw()
            instructor_button = Button('Instructor', (WIDTH // 2 - 100, HEIGHT // 2 + 20), width=200)
            instructor_button.draw()
            player_button = Button('Player', (WIDTH // 2 - 100, HEIGHT // 2 + 90), width=200)
            player_button.draw()

            menu_btn = Button('Main Menu', ((WIDTH - 200) // 2, HEIGHT - 150))
            menu_btn.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if dev_button.check_clicked():
                        # Perform actions for developer
                        pass
                    elif instructor_button.check_clicked():
                        # Perform actions for instructor
                        pass
                    elif player_button.check_clicked():
                        menu_command = 4
                    elif menu_btn.check_clicked():
                        main_menu = True

        elif menu_command == 4:
            draw_player_login()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key != pygame.K_RETURN:
                    if (username_enter_active):
                        if event.key == pygame.K_BACKSPACE:
                            username_enter = username_enter[0:-1]
                        else:
                            username_enter += event.unicode
                    elif (password_enter_active):
                        if event.key == pygame.K_BACKSPACE:
                            password_enter = password_enter[0:-1]
                        else:
                            password_enter += event.unicode
                    else:
                        pass
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if (WIDTH - 880) // 2 + 275 <= mouse_pos[0] <= (WIDTH - 880) // 2 + 495 and (HEIGHT - 600) // 2 + 200 <= mouse_pos[1] <=(HEIGHT - 600) // 2 + 240:
                        username_enter_active = True
                        password_enter_active = False
                    elif (WIDTH - 880) // 2 + 275 <= mouse_pos[0] <= (WIDTH - 880) // 2 + 495 and (HEIGHT - 600) // 2 + 270 <= mouse_pos[1] <=(HEIGHT - 600) // 2 + 310:
                        username_enter_active = False
                        password_enter_active = True
                    elif (WIDTH - 880) // 2 + 160 <= mouse_pos[0] <= (WIDTH - 880) // 2 + 420 and (HEIGHT - 600) // 2 + 500 <= mouse_pos[1] <= (HEIGHT - 600) // 2 + 540:
                        if len(player_list) < 3 and username_enter != '' and password_enter != '' and username_enter not in player_list:
                            player_list.append({"name":username_enter,"password":password_enter,"streak":0,"duck_count":0,"score":0})
                            username_enter = ''
                            password_enter = ''
                            show_no_user_error = False
                            show_empty_name = False
                            show_existing_user = False
                            show_too_many_user_error = False
                        elif username_enter == '' or password_enter == '':
                            show_empty_name = True
                            show_no_user_error = False
                            show_too_many_user_error = False
                            show_existing_user = False
                        elif username_enter in player_list:
                            show_existing_user = True
                            show_empty_name = False
                            show_no_user_error = False
                            show_too_many_user_error = False
                        else:
                            show_too_many_user_error = True
                            show_no_user_error = False
                            show_empty_name = False
                            show_existing_user = False

                    elif (WIDTH - 880) // 2 + 450 <= mouse_pos[0] <= (WIDTH - 880) // 2 + 710 and (HEIGHT - 600) // 2 + 500 <= mouse_pos[1] <= (HEIGHT - 600) // 2 + 540:
                        if len(player_list) > 0:
                            game(True, player_list=player_list)
                            username_enter = ''
                            password_enter = ''
                        else:
                            show_too_many_user_error = False
                            show_empty_name = False
                            show_no_user_error = True
                    else:
                        username_enter_active = False
                        password_enter_active = False


        else:
            main_menu = draw_game()
            if menu_command > 0:
                text = font.render(f'Button {menu_command} pressed!', True, 'black')
                screen.blit(text, (150, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if main_menu:  # Only show exit menu in the main menu screen
                    pygame.quit()
                    sys.exit()
    pygame.display.flip()

pygame.quit()