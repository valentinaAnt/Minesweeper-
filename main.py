import pygame 
import time
from elements import TILESIZE, BGCOLOUR, TITLE, FPS, DIFFICULTY_LEVELS, WHITE, BLACK, LIGHTGREY
from sprites import Board

class Game:
    def __init__(self):
        pygame.init()
        self.difficulty = 'easy'
        self.set_difficulty(self.difficulty)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.time_left = self.TIME_LIMIT
        self.start_time = None
        self.player_name = ""

        pygame.mixer.init()
        self.background_music = pygame.mixer.Sound("audios/background_music.wav")
        self.mine_sound = pygame.mixer.Sound("audios/mine_sound.wav")

        

    def show_difficulty_screen(self):
        selecting = True
        while selecting:
            self.screen.fill(BGCOLOUR)
            title_text = self.font.render("Choose Difficulty", True, WHITE)
            title_rect = title_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 4))
            self.screen.blit(title_text, title_rect)
            
            easy_button = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT // 2 - 50, 200, 50)
            medium_button = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT // 2, 200, 50)
            hard_button = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT // 2 + 50, 200, 50)
            
            pygame.draw.rect(self.screen, LIGHTGREY, easy_button)
            pygame.draw.rect(self.screen, LIGHTGREY, medium_button)
            pygame.draw.rect(self.screen, LIGHTGREY, hard_button)

            easy_text = self.font.render("Easy", True, BLACK)
            medium_text = self.font.render("Medium", True, BLACK)
            hard_text = self.font.render("Hard", True, BLACK)
            
            self.screen.blit(easy_text, (easy_button.centerx - easy_text.get_width() // 2, 
                                         easy_button.centery - easy_text.get_height() // 2))
            self.screen.blit(medium_text, (medium_button.centerx - medium_text.get_width() // 2, 
                                           medium_button.centery - medium_text.get_height() // 2))
            self.screen.blit(hard_text, (hard_button.centerx - hard_text.get_width() // 2, 
                                         hard_button.centery - hard_text.get_height() // 2))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if easy_button.collidepoint(mx, my):
                        self.difficulty = 'easy'
                        self.set_difficulty(self.difficulty)
                        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
                        selecting = False
                    elif medium_button.collidepoint(mx, my):
                        self.difficulty = 'medium'
                        self.set_difficulty(self.difficulty)
                        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
                        selecting = False
                    elif hard_button.collidepoint(mx, my):
                        self.difficulty = 'hard'
                        self.set_difficulty(self.difficulty)
                        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
                        selecting = False

    def set_difficulty(self, diff):
        params = DIFFICULTY_LEVELS[diff]
        self.ROWS = params['rows']
        self.COLS = params['cols']
        self.AMOUNT_MINES = params['mines']
        self.TIME_LIMIT = params['time']
        self.TILESIZE = 40
        self.WIDTH = self.TILESIZE * self.COLS
        self.HEIGHT = self.TILESIZE * self.ROWS + 50  # добавяме място за таймера
        print(f"Difficulty {diff}: {self.ROWS}x{self.COLS}, {self.AMOUNT_MINES} mines, {self.TIME_LIMIT}s")


    def new(self):
        self.board = Board(self.ROWS, self.COLS, self.AMOUNT_MINES, self.TILESIZE)
        self.start_time = time.time() 

        pygame.mixer.music.stop()
        self.mine_sound.stop()

        pygame.mixer.music.load("audios/background_music.wav")
        pygame.mixer.music.play(-1, 0.0) 

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
            self.update_timer()
        else:
            self.end_screen()

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.board.draw(self.screen)  
        self.display_timer()
        pygame.display.flip()



    def display_timer(self):
        elapsed_time = int(time.time() - self.start_time)  
        time_text = self.font.render(f"Time: {elapsed_time}s", True, WHITE)
        self.screen.blit(time_text, (self.WIDTH -210, 330)) 


    def update_timer(self):
        if self.start_time and time.time() - self.start_time >= self.TIME_LIMIT:
            self.playing = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mx //= self.TILESIZE
                my //= self.TILESIZE
                if event.button == 1 and not self.board.board_list[mx][my].flagged:
                    if not self.board.dig(mx, my):
                        self.playing = False
                        self.mine_sound.play()
                    elif self.check_win():
                        self.playing = False
                if event.button == 3 and not self.board.board_list[mx][my].revealed:
                    self.board.board_list[mx][my].flagged = not self.board.board_list[mx][my].flagged

    def check_flags(self):
        flagged_mines = 0
        for row in self.board.board_list:
            for tile in row:
                if tile.flagged and tile.type == "X":
                    flagged_mines += 1
        return flagged_mines == self.AMOUNT_MINES

    def check_win(self):
        return self.check_flags() or all(tile.revealed or tile.type == "X" for col in self.board.board_list for tile in col)

    def get_player_name(self):
        name = ""
        active = True
        prompt = "Enter your name: "
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
            self.screen.fill(BGCOLOUR)
            prompt_surface = self.font.render(prompt + name, True, WHITE)
            self.screen.blit(prompt_surface, (50, self.HEIGHT // 2))
            pygame.display.flip()
            self.clock.tick(30)
        return name

    def update_leaderboard(self, difficulty, name, time_score):
        try:
            with open("lederboar.txt", "a") as f:
                f.write(f"{difficulty},{name},{time_score}\n")
        except Exception as e:
            print("Error writing leaderboard:", e)

    def end_screen(self):
        if self.check_win():
            elapsed_time = int(time.time() - self.start_time)
            self.player_name = self.get_player_name()
            self.update_leaderboard(self.difficulty, self.player_name, elapsed_time)
        
        message = "You Win!" if self.check_win() else "Game Over!"
        self.screen.fill(BGCOLOUR)
        text = self.font.render(message, True, WHITE)
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(text, text_rect)

        new_game_button = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT // 2 + 50, 200, 50)
        pygame.draw.rect(self.screen, LIGHTGREY, new_game_button)
        new_game_text = self.font.render("New Game", True, BLACK)
        self.screen.blit(new_game_text, (new_game_button.centerx - new_game_text.get_width() // 2, 
                                         new_game_button.centery - new_game_text.get_height() // 2))
        pygame.display.flip()

        selecting = True
        while selecting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if new_game_button.collidepoint(mx, my):
                        selecting = False
                        self.new() 
                        self.run()  

        pygame.time.delay(2000)

game = Game()
game.show_difficulty_screen() 

while True:
    game.new()
    game.run()
