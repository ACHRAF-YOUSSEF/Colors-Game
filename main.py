import pygame
import engine
import os

grid = [8, 16, 32, 64]
grid_index = 1

WIDTH, HEIGHT = 800, 800
DIMENTION = grid[grid_index]
SQ_SIZE = HEIGHT // DIMENTION
MAX_FPS = 15

play = False
start = False
options = False

# colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

colors = {"white":WHITE, "red":RED, "green":GREEN, "grey":GREY, "blue":BLUE}

gs = engine.GameState()

gameType = ["inverted", "normal", "diagonal", "squared"]
gameType_index = 3

musicList = [f"./music/{song}" for song in os.listdir("./music")]
music_index = 0

# functions
def draw_text(screen, txt, x, y, police, color):
    texte_font = pygame.font.Font(None,police)
    texte = texte_font.render(txt,True,color)
    txt_rect = texte.get_rect()
    txt_rect.center =  (x,y)
    screen.blit(texte,txt_rect)
    
def getSongName(song):
    pos = song.find("/")
    while (pos != -1) :
        song = song[pos+1::]
        pos = song.find("/")
        
    return song
    
def menu(screen, clock):
    screen.fill(BLACK)
    pygame.display.set_caption("main menu")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    startButton.draw(screen, "start")
    optionsButton.draw(screen, "options")
    quitButton.draw(screen, "exit")
    
    clock.tick(MAX_FPS)
    pygame.display.flip()
    
def optionsMenu(screen, clock):
    screen.fill(BLACK)
    pygame.display.set_caption("options menu")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    txt = f"{getSongName(musicList[music_index])}"
    
    draw_text(screen, txt, 400, 315, 50, colors["white"])
    musicSelector.draw(screen, "music")

    optionsBackButton.draw(screen, "backFromOptions")
    
    clock.tick(MAX_FPS)
    pygame.display.flip()

def playMenu(screen, gs, clock):
    screen.fill(BLACK)
    pygame.display.set_caption("play menu")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    playButton.draw(screen, "play")
    
    txt = "red" if gs.player_1 else "green"
    texte = "play as "+txt+" color"

    if len(texte) == 17:
        x, y = 300, 370
    else:
        x, y = 280, 370
    
    draw_text(screen, texte, x, y, 50, colors[txt])
    playerSelector.draw(screen, "player")
    
    txt_1 = f"grid {DIMENTION}x{DIMENTION}"
    draw_text(screen, txt_1, 350, 415, 50, colors["white"])
    gridSelector.draw(screen, "grid")
    
    txt_2 = f"game type = {gameType[gameType_index]}"
    draw_text(screen, txt_2, 266, 465, 50, colors["grey"])
    gameTypeSelector.draw(screen, "game_type")
    
    backButton.draw(screen, "back")
    
    clock.tick(MAX_FPS)
    pygame.display.flip()

def game(screen, gs, sqSelected, clock):
    pygame.display.set_caption("main game")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            location = pygame.mouse.get_pos()

            col = location[0] //SQ_SIZE
            row = location[1] //SQ_SIZE
                
            sqSelected = (row, col)
            
            color = "red" if gs.player_1 else "green"
                
            move = engine.Move(sqSelected, color, gameType[gameType_index])
            
            gs.makeMove(move)

    drawGameState(screen, gs)
    
    clock.tick(MAX_FPS)
    pygame.display.flip()

def gameOverScreen(screen, gs, clock):
    screen.fill(BLACK)
    pygame.display.set_caption("game over screen")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            
    nb_red = gs.color_count("red")
    nb_green = gs.color_count("green")

    txt = "red" if (nb_red > nb_green) else "green"
    texte = txt+" wins !" if nb_red != nb_green else "draw"
    
    draw_text(screen, f"score = red {nb_red} vs green {nb_green}", 400, 250, 50, colors["grey"])
    draw_text(screen, "game over!", 400, 300, 50, colors["white"])
    draw_text(screen, texte, 400, 350, 50, colors[txt])
    
    clock.tick(MAX_FPS)
    pygame.display.flip()

def main():
    global play, start, gs

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    screen.fill(WHITE)
    
    createBoard(gs)

    sqSelected = ()

    while True:
        if start:
            if play:
                if not gs.end_game():
                    game(screen, gs, sqSelected, clock)
                else:
                    gameOverScreen(screen, gs, clock)
            else:
                playMenu(screen, gs, clock)
        elif options:
            optionsMenu(screen, clock)
        else:
            menu(screen, clock)

def createBoard(gs):
    gs.board = [["white" for _ in range(DIMENTION)] for _ in range(DIMENTION)]

def drawGameState(screen, gs):
    drawBoard(screen, gs)
    
def drawBoard(screen, gs):
    for row in range(DIMENTION):
        for col in range(DIMENTION):
            color = colors["grey"]
            box_color = colors[gs.board[row][col]]
            pygame.draw.rect(screen, box_color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE), 1)

def do_function(x):
    global play, start, grid, grid_index, gs, gameType, gameType_index, options, musicList, music_index, DIMENTION, SQ_SIZE
    
    if x == "play":
        play = True
        pygame.mixer.music.load(musicList[music_index])
        pygame.mixer.music.play(-1)
        print("begining...!")
        
    if x == "start":
        start = True
        print("starting...!")
        
    if x == "exit":
        print("exiting...!")
        quit()
        
    if x == "options":
        print("opening options menu...!")
        options = True
    
    if x == "backFromOptions":
        options = False
        
    if x == "back":
        start = False
    
    if x == "player":
        gs.player_1 = not gs.player_1
    
    if x == "grid":
        grid_index += 1
        
        if grid_index >= len(grid):
            grid_index = 0
            
        DIMENTION = grid[grid_index]
        SQ_SIZE = HEIGHT // DIMENTION
        
        createBoard(gs)
        
    if x == "game_type":
        gameType_index += 1
        
        if gameType_index >= len(gameType):
            gameType_index = 0
            
    if x == "music":
        print("changing...!")
        
        music_index += 1
        
        if music_index >= len(musicList):
            music_index = 0


# classes
class Button:
    def __init__(self, text, width, height, pos, elevation):
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'

        # text
        self.text_surf = gui_font.render(text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen, x):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click(x)

    def check_click(self,x):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed:
                    do_function(x)
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    
    gui_font = pygame.font.Font(None, 30)
    
    # play menu buttons
    playButton = Button("play", 200, 40, (300, 300), 5)
    playerSelector = Button("change", 100, 40, (450, 355), 5)
    gridSelector = Button("change", 100, 40, (450, 400), 5)
    gameTypeSelector = Button("change", 100, 40, (450, 450), 5)
    backButton = Button("back", 200, 40, (300, 500), 5)
    
    # main menu buttons
    startButton = Button("start", 200, 40, (300, 300), 5)
    optionsButton = Button("options", 200, 40, (300, 350), 5)
    quitButton = Button("exit", 200, 40, (300, 400), 5)
    
    # options menu buttons
    musicSelector = Button("change", 100, 40, (350, 350), 5)
    optionsBackButton = Button("back", 200, 40, (300, 400), 5)
    
    main()
