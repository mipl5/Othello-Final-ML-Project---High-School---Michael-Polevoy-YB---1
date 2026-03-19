import pygame
from board import Board
from constants import *
from ai_agent import AIAgent
import os
import platform

if platform.system() == "Windows":
    import ctypes
    # arbitrary string that tells windows this is a separate app from Python
    myappid = 'micha.othello.game.final'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
pygame.init()

icon_path = os.path.join(os.path.dirname(__file__), 'images', 'othello_game_logo.png')
if os.path.exists(icon_path):
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Othello (You: Black, AI: White)")

bg_path = os.path.join(os.path.dirname(__file__), 'images', 'othello_background.jpg')
if os.path.exists(bg_path):
    menu_bg = pygame.transform.scale(pygame.image.load(bg_path).convert(), (WINDOW_WIDTH, WINDOW_HEIGHT))
else:
    menu_bg = None

clock = pygame.time.Clock()

board = Board()
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend-othello', 'othello_model.keras')
agent = AIAgent(model_path)

current_player = BLACK

running = True

font = pygame.font.SysFont('Arial', 32, bold=True)

def draw_status(surface, board, current_player, agent):
    black_count, white_count = board.get_counts()
    
    pygame.draw.rect(surface, (50, 50, 50), (0, 0, WINDOW_WIDTH, HEADER_HEIGHT))
    
    black_text = font.render(f"You (B): {black_count}", True, (255, 255, 255))
    white_text = font.render(f"AI (W): {white_count}", True, (255, 255, 255))
    
    turn_color = "Black's" if current_player == BLACK else "White's"
    turn_text = font.render(f"{turn_color} Turn", True, (255, 215, 0))
    
    surface.blit(black_text, (20, 10))
    surface.blit(white_text, (WINDOW_WIDTH - white_text.get_width() - 20, 10))
    surface.blit(turn_text, (WINDOW_WIDTH // 2 - turn_text.get_width() // 2, 10))
    
    # Difficulty indicator instead of buttons
    diff_font = pygame.font.SysFont('Arial', 14, bold=True)
    diff_txt = diff_font.render(f"Difficulty: {int(agent.difficulty * 100)}%", True, (0, 200, 0))
    surface.blit(diff_txt, (10, 50))
    
    reset_font = pygame.font.SysFont('Arial', 24, bold=True)
    reset_text = reset_font.render("Menu", True, (255, 255, 255))  # Change "Reset" to "Menu"
    reset_rect = pygame.Rect(WINDOW_WIDTH // 2 - 40, 45, 80, 30)
    pygame.draw.rect(surface, (200, 0, 0), reset_rect, border_radius=5)
    surface.blit(reset_text, (reset_rect.centerx - reset_text.get_width() // 2, reset_rect.centery - reset_text.get_height() // 2))

ai_think_timer = 0
game_over = False

STATE_MENU = 0
STATE_DIFFICULTY = 1
STATE_PLAYING = 2
game_state = STATE_MENU

def draw_menu(surface):
    if menu_bg:
        surface.blit(menu_bg, (0, 0))
    else:
        surface.fill(GREEN)
    title_font = pygame.font.SysFont('Arial', 48, bold=True)
    title_text = title_font.render("OTHELLO", True, (255, 255, 255))
    surface.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 80))
    
    btn_font = pygame.font.SysFont('Arial', 24, bold=True)
    
    h_rect = pygame.Rect(WINDOW_WIDTH // 2 - 120, 200, 240, 50)
    pygame.draw.rect(surface, (100, 100, 100), h_rect, border_radius=10)
    h_text = btn_font.render("Play Vs Human", True, (200, 200, 200))
    surface.blit(h_text, (h_rect.centerx - h_text.get_width() // 2, h_rect.centery - h_text.get_height() // 2))
    
    ai_rect = pygame.Rect(WINDOW_WIDTH // 2 - 120, 280, 240, 50)
    pygame.draw.rect(surface, (50, 50, 200), ai_rect, border_radius=10)
    ai_text = btn_font.render("Play Vs AI", True, (255, 255, 255))
    surface.blit(ai_text, (ai_rect.centerx - ai_text.get_width() // 2, ai_rect.centery - ai_text.get_height() // 2))
    
    return h_rect, ai_rect

def draw_difficulty_menu(surface):
    surface.fill(GREEN)
    title_font = pygame.font.SysFont('Arial', 36, bold=True)
    title_text = title_font.render("Select AI Difficulty", True, (255, 255, 255))
    surface.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 80))
    
    btn_font = pygame.font.SysFont('Arial', 24, bold=True)
    diffs = [(1.0, "100% - Hard"), (0.75, "75% - Medium"), (0.5, "50% - Easy"), (0.25, "25% - Very Easy")]
    
    rects = []
    start_y = 180
    for diff_val, label in diffs:
        rect = pygame.Rect(WINDOW_WIDTH // 2 - 120, start_y, 240, 40)
        pygame.draw.rect(surface, (0, 150, 0), rect, border_radius=10)
        txt = btn_font.render(label, True, (255, 255, 255))
        surface.blit(txt, (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2))
        rects.append((rect, diff_val))
        start_y += 60
        
    return rects

while running:

    clock.tick(FPS)
    
    if game_state == STATE_MENU:
        h_rect, ai_rect = draw_menu(screen)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if ai_rect.collidepoint(x, y):
                    game_state = STATE_DIFFICULTY
                # h_rect does nothing for now
                
    elif game_state == STATE_DIFFICULTY:
        rects = draw_difficulty_menu(screen)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for rect, diff_val in rects:
                    if rect.collidepoint(x, y):
                        agent.difficulty = diff_val
                        board = Board()
                        current_player = BLACK
                        ai_think_timer = 0
                        game_over = False
                        game_state = STATE_PLAYING

    elif game_state == STATE_PLAYING:

        if current_player == WHITE and running and not game_over:
            if board.get_valid_moves(WHITE):
                if ai_think_timer == 0:
                    ai_think_timer = pygame.time.get_ticks()
                
                if pygame.time.get_ticks() - ai_think_timer > 1000:
                    move = agent.get_move(board)
                    if move:
                        board.make_move(move[0], move[1], WHITE)
                    if board.get_valid_moves(BLACK):
                        current_player = BLACK
                    elif not board.get_valid_moves(WHITE):
                        game_over = True
                    ai_think_timer = 0
            else:
                if not board.get_valid_moves(BLACK):
                    game_over = True
                else:
                    current_player = BLACK
                    
        if current_player == BLACK and running and not game_over:
            if not board.get_valid_moves(BLACK):
                if board.get_valid_moves(WHITE):
                    current_player = WHITE
                else:
                    game_over = True

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                
                # Check Menu button click
                reset_rect = pygame.Rect(WINDOW_WIDTH // 2 - 40, 45, 80, 30)
                if reset_rect.collidepoint(x, y):
                    game_state = STATE_MENU
                    continue

                if current_player == BLACK and not game_over:
                    y -= HEADER_HEIGHT

                    if y >= 0:
                        col = x // CELL_SIZE
                        row = y // CELL_SIZE

                        if board.make_move(row, col, BLACK):
                            if board.get_valid_moves(WHITE):
                                current_player = WHITE
                            elif not board.get_valid_moves(BLACK):
                                game_over = True

        screen.fill(GREEN)
        board.draw(screen)
        draw_status(screen, board, current_player, agent)

        if game_over:
            black_count, white_count = board.get_counts()
            if black_count > white_count:
                msg = "Black Wins!"
            elif white_count > black_count:
                msg = "White Wins!"
            else:
                msg = "Tie!"
                
            go_font = pygame.font.SysFont('Arial', 64, bold=True)
            go_text = go_font.render(msg, True, (255, 0, 0))
            shadow = go_font.render(msg, True, (0, 0, 0))
            screen.blit(shadow, (WINDOW_WIDTH // 2 - go_text.get_width() // 2 + 2, WINDOW_HEIGHT // 2 - go_text.get_height() // 2 + 2))
            screen.blit(go_text, (WINDOW_WIDTH // 2 - go_text.get_width() // 2, WINDOW_HEIGHT // 2 - go_text.get_height() // 2))

        pygame.display.flip()

pygame.quit()