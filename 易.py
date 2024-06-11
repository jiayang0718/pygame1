import pygame
import random
import time

# 游戏相关的常量
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 600
SCORE_BOARD_HEIGHT = 100
BLOCK_SIZE = 80
ROWS = 5
COLS = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 32
DELAY = 200  # 每次下落的延迟（毫秒）
GAME_TIME = 120  # 游戏总时间（秒）
WIN_SCORE = 10000  # 结束游戏的分数

# 颜色列表
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Candy Crush")

# 初始化字体
font = pygame.font.SysFont(None, FONT_SIZE)

# 生成随机的方块颜色
def generate_board():
    board = []
    for row in range(ROWS):
        row = []
        for col in range(COLS):
            row.append(random.randint(0, len(COLORS) - 1))
        board.append(row)
    return board

# 画出方块
def draw_board(board):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if board[row][col] == -1 else COLORS[board[row][col]]
            pygame.draw.rect(screen, color, (col * BLOCK_SIZE, SCORE_BOARD_HEIGHT + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# 交换方块
def swap(board, row1, col1, row2, col2):
    board[row1][col1], board[row2][col2] = board[row2][col2], board[row1][col1]

# 检查是否有匹配
def check_match(board):
    matches = set()

    for row in range(ROWS):
        for col in range(COLS - 2):
            if board[row][col] == board[row][col + 1] == board[row][col + 2]:
                matches.add((row, col))
                matches.add((row, col + 1))
                matches.add((row, col + 2))

    for col in range(COLS):
        for row in range(ROWS - 2):
            if board[row][col] == board[row + 1][col] == board[row + 2][col]:
                matches.add((row, col))
                matches.add((row + 1, col))
                matches.add((row + 2, col))

    return matches

# 消除匹配的方块
def remove_matches(board, matches):
    score = len(matches) * 100
    for row, col in matches:
        board[row][col] = -1  # 设置为白色
    return score

# 下落方块填充空缺
def fill_empty(board):
    for col in range(COLS):
        empty_cells = 0
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] == -1:
                empty_cells += 1
            elif empty_cells > 0:
                board[row + empty_cells][col] = board[row][col]
                board[row][col] = -1

# 添加新方块填充空缺
def add_new_blocks(board):
    for col in range(COLS):
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] == -1:
                board[row][col] = random.randint(0, len(COLORS) - 1)

# 动画显示新方块下落
def animate_fall(board):
    for _ in range(ROWS):
        fill_empty(board)
        draw_board(board)
        pygame.display.update()
        pygame.time.wait(DELAY)

# 主游戏循环
def main():
    board = generate_board()
    running = True
    dragging = False
    drag_start = None
    drag_end = None
    score = 0
    start_time = time.time()

    while running:
        screen.fill(BLACK)

        # 绘制分数板
        pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, SCORE_BOARD_HEIGHT))
        
        # 绘制分数
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # 计算剩余时间
        elapsed_time = time.time() - start_time
        remaining_time = max(GAME_TIME - elapsed_time, 0)
        
        # 绘制时间
        time_text = font.render(f"Time: {int(remaining_time)}", True, BLACK)
        screen.blit(time_text, (SCREEN_WIDTH - 150, 10))

        # 检查时间是否结束或者达到目标分数
        if remaining_time <= 0 or score >= WIN_SCORE:
            running = False

        # 绘制游戏画面
        draw_board(board)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not dragging:
                    dragging = True
                    drag_start = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    dragging = False
                    drag_end = pygame.mouse.get_pos()
                    diff_x = drag_end[0] - drag_start[0]
                    diff_y = drag_end[1] - drag_start[1]
                    row1 = (drag_start[1] - SCORE_BOARD_HEIGHT) // BLOCK_SIZE
                    col1 = drag_start[0] // BLOCK_SIZE
                    row2 = (drag_end[1] - SCORE_BOARD_HEIGHT) // BLOCK_SIZE
                    col2 = drag_end[0] // BLOCK_SIZE
                    if 0 <= row1 < ROWS and 0 <= col1 < COLS and 0 <= row2 < ROWS and 0 <= col2 < COLS:
                        if abs(diff_x) > abs(diff_y):
                            if diff_x > 0 and col1 + 1 < COLS:
                                swap(board, row1, col1, row1, col1 + 1)
                            elif diff_x < 0 and col1 - 1 >= 0:
                                swap(board, row1, col1, row1, col1 - 1)
                        else:
                            if diff_y > 0 and row1 + 1 < ROWS:
                                swap(board, row1, col1, row1 + 1, col1)
                            elif diff_y < 0 and row1 - 1 >= 0:
                                swap(board, row1, col1, row1 - 1, col1)

                        matches = check_match(board)
                        if matches:
                            score += remove_matches(board, matches)
                            animate_fall(board)
                            while matches:
                                fill_empty(board)
                                draw_board(board)
                                pygame.display.update()
                                pygame.time.wait(DELAY)
                                add_new_blocks(board)
                                draw_board(board)
                                pygame.display.update()
                                matches = check_match(board)
                                if matches:
                                    score += remove_matches(board, matches)

    # 显示游戏结束画面
    screen.fill(BLACK)
    if score >= WIN_SCORE:
        game_over_text = font.render(f"Congratulations! Final Score: {score}", True, WHITE)
    else:
        game_over_text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(3000)

    pygame.quit()

if __name__ == "__main__":
    main()
