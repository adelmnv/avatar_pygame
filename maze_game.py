import pygame
import random
import sys

class MazeGame:
    """
    A class representing the 'Water - Flow Control' game.
    """
    def __init__(self):
        """
        Initialize the game.
        """
        pygame.init()

        # Colors
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (30, 144, 255)
        self.BLACK = (0, 0, 0)
        self.ORANGE = (255, 165, 0)
        self.BROWN = (139, 69, 19)

        # Screen dimensions
        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 600

        # Maze cell dimensions
        self.CELL_SIZE = 15

        # Number of cells in width and height
        self.GRID_WIDTH = self.SCREEN_WIDTH // self.CELL_SIZE
        self.GRID_HEIGHT = self.SCREEN_HEIGHT // self.CELL_SIZE

        # Player speed
        self.PLAYER_SPEED = 1

        # Create window
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Water - Flow Control")

        # Background image
        self.background = pygame.image.load("sources/images/water/maze_background.jpeg")
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Load background music
        pygame.mixer.music.load("sources/sounds/water/maze_music.mp3")
        pygame.mixer.music.play(-1)

        self.intro_shown = False

        self.clock = pygame.time.Clock()

    def generate_maze(self):
        """
        Generate a maze using a modified version of the recursive backtracking algorithm.

        Returns:
            list: A 2D list representing the generated maze.
        """
        maze = [[1] * self.GRID_WIDTH for _ in range(self.GRID_HEIGHT)]

        # Set starting point
        maze[1][1] = 0

        # Create maze
        stack = [(1, 1)]
        while stack:
            current_cell = stack[-1]
            maze[current_cell[1]][current_cell[0]] = 0

            neighbors = [(current_cell[0] + 2, current_cell[1]),
                         (current_cell[0] - 2, current_cell[1]),
                         (current_cell[0], current_cell[1] + 2),
                         (current_cell[0], current_cell[1] - 2)]
            unvisited_neighbors = [neighbor for neighbor in neighbors if
                                   0 < neighbor[0] < self.GRID_WIDTH - 1 and 0 < neighbor[1] < self.GRID_HEIGHT - 1 and
                                   maze[neighbor[1]][neighbor[0]] == 1]

            if unvisited_neighbors:
                next_cell = random.choice(unvisited_neighbors)
                wall = ((current_cell[0] + next_cell[0]) // 2, (current_cell[1] + next_cell[1]) // 2)
                maze[wall[1]][wall[0]] = 0
                stack.append(next_cell)
            else:
                stack.pop()

        return maze

    def draw_maze(self, maze):
        """
        Draw the maze on the screen.

        Args:
            maze (list): A 2D list representing the maze.
        """
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                if maze[y][x] == 1:
                    pygame.draw.circle(self.screen, self.BROWN, (x * self.CELL_SIZE + self.CELL_SIZE // 2, y * self.CELL_SIZE + self.CELL_SIZE // 2), self.CELL_SIZE // 2)

    def draw_start_end(self):
        """
        Draw the start and end points on the maze.
        """
        pygame.draw.circle(self.screen, self.GREEN, (self.CELL_SIZE + self.CELL_SIZE // 2, self.CELL_SIZE + self.CELL_SIZE // 2), self.CELL_SIZE // 2)
        pygame.draw.circle(self.screen, self.RED, ((self.GRID_WIDTH - 3) * self.CELL_SIZE + self.CELL_SIZE // 2, (self.GRID_HEIGHT - 3) * self.CELL_SIZE + self.CELL_SIZE // 2), self.CELL_SIZE // 2)

    def show_intro(self):
        """
        Display the game introduction.
        """
        # Display the intro only if it has not been displayed yet
        if not self.intro_shown:
            intro_image = pygame.transform.scale(pygame.image.load("sources/images/water/water_intro.jpg"), (600, 600))
            self.screen.blit(intro_image, (0, 0))
            pygame.display.update()
            intro_done = False
            while not intro_done:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        intro_done = True
                pygame.time.Clock().tick(30)  # Adjust as needed

            self.intro_shown = True

    def run(self):
        """
        Run the main game loop.

        Returns:
            bool: True if the player wins, False otherwise.
        """
        maze = self.generate_maze()
        player_x = 1
        player_y = 1
        keys = {'up': False, 'down': False, 'left': False, 'right': False}
        player_path = []
        game_over = False
        win = False
        self.show_intro()
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    game_over = True
                    return win
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        keys['up'] = True
                    elif event.key == pygame.K_DOWN:
                        keys['down'] = True
                    elif event.key == pygame.K_LEFT:
                        keys['left'] = True
                    elif event.key == pygame.K_RIGHT:
                        keys['right'] = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        keys['up'] = False
                    elif event.key == pygame.K_DOWN:
                        keys['down'] = False
                    elif event.key == pygame.K_LEFT:
                        keys['left'] = False
                    elif event.key == pygame.K_RIGHT:
                        keys['right'] = False

            if keys['up'] and player_y - self.PLAYER_SPEED > 0 and maze[player_y - self.PLAYER_SPEED][player_x] == 0:
                player_y -= self.PLAYER_SPEED
                player_path.append((player_x, player_y))
            if keys['down'] and player_y + self.PLAYER_SPEED < self.GRID_HEIGHT and maze[player_y + self.PLAYER_SPEED][player_x] == 0:
                player_y += self.PLAYER_SPEED
                player_path.append((player_x, player_y))
            if keys['left'] and player_x - self.PLAYER_SPEED > 0 and maze[player_y][player_x - self.PLAYER_SPEED] == 0:
                player_x -= self.PLAYER_SPEED
                player_path.append((player_x, player_y))
            if keys['right'] and player_x + self.PLAYER_SPEED < self.GRID_WIDTH and maze[player_y][player_x + self.PLAYER_SPEED] == 0:
                player_x += self.PLAYER_SPEED
                player_path.append((player_x, player_y))

            if (player_x, player_y) in player_path[:-1]:
                game_over = True
            if (player_x, player_y) == ((self.GRID_WIDTH - 3), (self.GRID_HEIGHT - 3)):
                game_over = True
                win = True

            self.screen.blit(self.background, (0, 0))
            self.draw_maze(maze)
            self.draw_start_end()

            for px, py in player_path:
                pygame.draw.rect(self.screen, self.BLUE, (px * self.CELL_SIZE, py * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))
            pygame.draw.circle(self.screen, self.BLUE, (player_x * self.CELL_SIZE + self.CELL_SIZE // 2, player_y * self.CELL_SIZE + self.CELL_SIZE // 2), self.CELL_SIZE // 2)

            pygame.display.flip()
            self.clock.tick(60)

        self.screen.fill(self.BLACK)
        font = pygame.font.SysFont('Papyrus', 32)
        if win:
            game_over_text = font.render("You've managed to master water!", True, self.GREEN)
        else:
            game_over_text = font.render("Flow can't be reversed...", True, self.RED)
        text_rect = game_over_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_text, text_rect)
        pygame.display.flip()

        pygame.time.delay(1000)

        return win

if __name__ == "__main__":
    game = MazeGame()
    game.run()