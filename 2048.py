import pygame
import random

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 400, 500
GRID_SIZE = 4
CELL_SIZE = WIDTH // GRID_SIZE
GRID_COLOR = (184, 175, 169)
EMPTY_CELL_COLOR = (255, 213, 181)
FONT_COLOR_GAME_OVER = (255, 255, 255)
WINNER_BG = (255, 204, 0)
LOSER_BG = (163, 148, 137)
FONT_SCORE_LABEL = pygame.font.Font(None, 72)
FONT_SCORE = pygame.font.Font(None, 72)
FONT_GAME_OVER = pygame.font.Font(None, 72)
FONT_CELL_NUMBER = {
    2: pygame.font.Font(None, 72),
    4: pygame.font.Font(None, 72),
    8: pygame.font.Font(None, 72),
    16: pygame.font.Font(None, 64),
    32: pygame.font.Font(None, 64),
    64: pygame.font.Font(None, 64),
    128: pygame.font.Font(None, 48),
    256: pygame.font.Font(None, 48),
    512: pygame.font.Font(None, 48),
    1024: pygame.font.Font(None, 36),
    2048: pygame.font.Font(None, 36),
}

# Define colors for different cell values
CELL_COLORS = {
    0: EMPTY_CELL_COLOR,
    2: (252, 239, 230),
    4: (242, 232, 203),
    8: (245, 182, 130),
    16: (242, 148, 70),
    32: (255, 119, 92),
    64: (230, 76, 46),
    128: (237, 226, 145),
    256: (252, 225, 48),
    512: (255, 219, 74),
    1024: (240, 185, 34),
    2048: (250, 215, 77),
}

# Define text colors for different cell values
TEXT_COLORS = {
    2: (105, 92, 87),
    4: (105, 92, 87),
    8: (255, 255, 255),
    16: (255, 255, 255),
    32: (255, 255, 255),
    64: (255, 255, 255),
    128: (255, 255, 255),
    256: (255, 255, 255),
    512: (255, 255, 255),
    1024: (255, 255, 255),
    2048: (255, 255, 255),
}

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')

class Game:
    def __init__(self):
        self.matrix = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.add_tile()
        self.add_tile()
        self.game_over = False
        self.win = False
        print(self.matrix)

    def add_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.matrix[i][j] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.matrix[row][col] = random.choice([2, 4])

    def stack(self):
        ''' Stacks all the elements to the left of the matrix '''
        new_matrix = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        for i in range(GRID_SIZE):
            fill_position = 0
            for j in range(GRID_SIZE):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix

    def combine(self):
        ''' Combines two elements if they are of same value into one and updates the matrix '''
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE - 1):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]

    def reverse(self):
        ''' Mirrors the matrix. Ex. [[2,4,8,8],...] will give [[8,8,4,2],...] '''
        new_matrix = []
        for i in range(GRID_SIZE):
            new_matrix.append([])
            for j in range(GRID_SIZE):
                new_matrix[i].append(self.matrix[i][GRID_SIZE - 1 - j])
        self.matrix = new_matrix

    def transpose(self):
        ''' Takes the transpose of matrix. Ref : https://www.geeksforgeeks.org/program-to-find-transpose-of-a-matrix/ '''
        new_matrix = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    def can_move(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.matrix[i][j] == 0:
                    return True
                if j < GRID_SIZE - 1 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
                if i < GRID_SIZE - 1 and self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False

    def check_game_over(self):
        if any(2048 in row for row in self.matrix):
            self.win = True
        elif not self.can_move():
            self.game_over = True

    def move(self, direction):
        if direction == 'left':
            self.stack()
            self.combine()
            self.stack()
        elif direction == 'right':
            self.reverse()
            self.stack()
            self.combine()
            self.stack()
            self.reverse()
        elif direction == 'up':
            self.transpose()
            self.stack()
            self.combine()
            self.stack()
            self.transpose()
        elif direction == 'down':
            self.transpose()
            self.reverse()
            self.stack()
            self.combine()
            self.stack()
            self.reverse()
            self.transpose()
        self.add_tile()
        self.check_game_over()

    def draw(self):
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, GRID_COLOR, (0, 100, WIDTH, WIDTH), 0)
        
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.matrix[i][j]
                rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE + 100, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, CELL_COLORS[value], rect)
                if value != 0:
                    text = FONT_CELL_NUMBER[value].render(str(value), True, TEXT_COLORS[value])
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

        score_text = FONT_SCORE_LABEL.render(f"Score: {self.score}", True, (0, 0, 0))
        screen.blit(score_text, (20, 20))

        if self.win:
            self.show_game_over("YOU WIN!", WINNER_BG)
        elif self.game_over:
            self.show_game_over("GAME OVER", LOSER_BG)

    def show_game_over(self, message, color):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        game_over_text = FONT_GAME_OVER.render(message, True, FONT_COLOR_GAME_OVER)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        pygame.draw.rect(screen, color, game_over_rect.inflate(20, 20))
        screen.blit(game_over_text, game_over_rect)

game = Game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game.game_over and not game.win:
                if event.key == pygame.K_LEFT:
                    game.move('left')
                elif event.key == pygame.K_RIGHT:
                    game.move('right')
                elif event.key == pygame.K_UP:
                    game.move('up')
                elif event.key == pygame.K_DOWN:
                    game.move('down')
            elif event.key == pygame.K_r:
                game = Game()
    
    game.draw()
    pygame.display.update()

pygame.quit()
