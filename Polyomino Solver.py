#Import modules
import pygame, random, sys
pygame.init()

#DICTIONARIES
#Window information
Config = {
    "Framerate": 30,
    "ScreenCaption": "Polyomino Solver",
    "ScreenX": 1280,
    "ScreenY": 720,
}
#Variables used
Variables = {
    "cell_select_x": -1,
    "cell_select_y": -1,
    "click_ready": True,
    "click_used_left": False,
    "click_used_right": False,
    "grid_size_x": 5,
    "grid_size_y": 4,
    "mouse_x": 0,
    "mouse_y": 0,
    "page": 0,
    "piece_drag": -1,
    "piece_select": -1,
    "piece_size_x": 0,
    "piece_size_y": 0,
    "pieces": 0,
    "solved": False,
}

#LISTS
Grid = [[-1 for i in range(Variables["grid_size_y"])] for i in range(Variables["grid_size_x"])]
Pieces = []
Pieces_Color = []
Pieces_Placed = []
Pieces_Position = []
Pieces_Type = []
#Types of pieces
Pieces_Type_All = [
    #Monomino
    [[1]],
    #Domino
    [[1], [1]],
    #Triominoes
    [[1], [1], [1]],
    [[1, 1], [1, 0]],
    #Tetrominoes
    [[1], [1], [1], [1]],
    [[1, 1], [1, 1]],
    [[1, 1], [1, 0], [1, 0]],
    [[1, 0], [1, 1], [1, 0]],
    [[1, 0], [1, 1], [0, 1]],
    #Pentominoes
    [[1], [1], [1], [1], [1]],
    [[1, 1], [1, 1], [1, 0]],
    [[1, 1], [1, 0], [1, 1]],
    [[1, 1], [1, 0], [1, 0], [1, 0]],
    [[1, 0], [1, 1], [1, 0], [1, 0]],
    [[1, 0], [1, 0], [1, 1], [0, 1]],
    [[1, 1, 1], [1, 0, 0], [1, 0, 0]],
    [[1, 0, 0], [1, 1, 1], [1, 0, 0]],
    [[1, 0, 0], [1, 1, 1], [0, 1, 0]],
    [[1, 0, 0], [1, 1, 0], [0, 1, 1]],
    [[1, 0, 0], [1, 1, 1], [0, 0, 1]],
    [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
]
Puzzle_Places = []

#Make sprite groups
sprites_group_piece, sprites_group_tile, sprites_group_ui = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()

#CLASSES
#Pieces to remove
class Piece(pygame.sprite.Sprite):
    def __init__(self, identity):
        pygame.sprite.Sprite.__init__(self)
        self.identity = identity
        self.pos_x = Pieces_Position[self.identity][0]
        self.pos_y = Pieces_Position[self.identity][1]
        self.type = Pieces_Type[self.identity]
        self.size_x = len(Pieces_Type_All[self.type]) * 20
        self.size_y = len(Pieces_Type_All[self.type][0]) * 20
        self.color = Pieces_Color[self.identity]
        self.image = pygame.Surface((self.size_x, self.size_y))
        self.image.fill((  0,  24,  48))
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos_x, self.pos_y)
        for i in range(len(Pieces_Type_All[self.type])):
            for j in range(len(Pieces_Type_All[self.type][i])):
                if Pieces_Type_All[self.type][i][j] == 1:
                    pygame.draw.rect(self.image, self.color, [i * 20, j * 20, 20, 20])
    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1:
            Variables["pieces"] -= 1
            Pieces.remove(Pieces[self.identity])
            Pieces_Color.remove(Pieces_Color[self.identity])
            Pieces_Position.remove(Pieces_Position[self.identity])
            Pieces_Type.remove(Pieces_Type[self.identity])
            self.kill()
            draw(screen)
#Tiles to turn on/off
class Tile(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        pygame.sprite.Sprite.__init__(self)
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pos_x = self.grid_x * 45 + Config["ScreenX"] / 3 + 25
        self.pos_y = self.grid_y * 45 + 120
        self.size_x = 40
        self.size_y = 40
        self.image = pygame.Surface((self.size_x, self.size_y))
        self.image.fill(( 79, 103, 128))
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos_x, self.pos_y)
    def update(self):
        if self.grid_x > Variables["grid_size_x"] - 1 or self.grid_y > Variables["grid_size_y"] - 1 or Grid[self.grid_x][self.grid_y] == -2:
            self.image.fill((  0,  32,  64))
        else:
            self.image.fill(( 79, 103, 128))
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1 and Variables["click_ready"] and self.grid_x < Variables["grid_size_x"] and self.grid_y < Variables["grid_size_y"]:
            Variables["click_ready"] = False
            if Grid[self.grid_x][self.grid_y] == -1:
                Grid[self.grid_x][self.grid_y] = -2
                self.image.fill((  0,  32,  64))
            else:
                Grid[self.grid_x][self.grid_y] = -1
                self.image.fill(( 79, 103, 128))
            draw(screen)
#Buttons
class UI_Button(pygame.sprite.Sprite):
    def __init__(self, identity, pos_x, pos_y, size_x, size_y, color, text_color, text_font, text_size, text):
        pygame.sprite.Sprite.__init__(self)
        self.identity = identity
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y
        self.text_style = pygame.font.SysFont(text_font, text_size)
        self.text = self.text_style.render(text, 1, text_color)
        self.image = pygame.Surface((self.size_x, self.size_y))
        self.image.fill(color)
        self.image.blit(self.text, self.text.get_rect(center=(self.size_x / 2, self.size_y / 2)))
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos_x, self.pos_y)
    def update(self):
        global Grid
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1 and Variables["click_ready"]:
            Variables["click_ready"] = False
            if self.identity == 0 and Variables["grid_size_y"] < 20:
                Variables["grid_size_y"] += 1
                Grid = [[-1 for j in range(Variables["grid_size_y"])] for i in range(Variables["grid_size_x"])]
                for i in range(Variables["grid_size_x"]):
                    sprite = Tile(i, Variables["grid_size_y"] - 1)
                    sprites_group_tile.add(sprite)
            elif self.identity == 1 and Variables["grid_size_y"] > 1:
                Variables["grid_size_y"] -= 1
                Grid = [[-1 for j in range(Variables["grid_size_y"])] for i in range(Variables["grid_size_x"])]
            elif self.identity == 2 and Variables["grid_size_x"] < 20:
                Variables["grid_size_x"] += 1
                Grid = [[-1 for j in range(Variables["grid_size_y"])] for i in range(Variables["grid_size_x"])]
                for i in range(Variables["grid_size_y"]):
                    sprite = Tile(Variables["grid_size_x"] - 1, i)
                    sprites_group_tile.add(sprite)
            elif self.identity == 3 and Variables["grid_size_x"] > 1:
                Variables["grid_size_x"] -= 1
                Grid = [[-1 for j in range(Variables["grid_size_y"])] for i in range(Variables["grid_size_x"])]
            elif self.identity == 4:
                Variables["page"] = 1
                draw(screen)
                puzzle_solve()
            draw(screen)
#Piece creating buttons
class UI_Button_Piece(pygame.sprite.Sprite):
    def __init__(self, identity, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.identity = identity
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = 50
        self.size_y = 50
        self.image = pygame.Surface((self.size_x, self.size_y))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos_x, self.pos_y)
        for i in range(len(Pieces_Type_All[self.identity])):
            for j in range(len(Pieces_Type_All[self.identity][i])):
                if Pieces_Type_All[self.identity][i][j] == 1:
                    pygame.draw.rect(self.image, (  0,   0,   0), [4 + i * (self.size_x - 8) / 3, 4 + j * (self.size_y - 8) / 3, (self.size_x - 8) / 3, (self.size_y - 8) / 3])
    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1 and Variables["click_ready"]:
            Variables["click_ready"] = False
            Variables["pieces"] += 1
            Pieces.append(Pieces_Type_All[self.identity])
            Pieces_Color.append((random.randint(4, 15) * 16, random.randint(4, 15) * 16, random.randint(4, 15) * 16))
            Pieces_Position.append([random.randint(45, round(Config["ScreenX"] / 3) - 45), random.randint(300, Config["ScreenY"] - 45)])
            Pieces_Type.append(self.identity)
            sprite = Piece(len(Pieces) - 1)
            sprites_group_piece.add(sprite)
            draw(screen)

#Find all ways to put a piece in the grid
def puzzle_find(piece):
    Pieces_Variants = []
    #Find piece
    Pieces_Variants.append(Pieces_Type_All[Pieces_Type[piece]])
    #Find piece rotated 90 degrees
    Pieces_Variants.append([[Pieces_Variants[0][j][len(Pieces_Variants[0][0]) - i - 1] for j in range(len(Pieces_Variants[0]))] for i in range(len(Pieces_Variants[0][0]))])
    #Find piece rotated 180 degrees
    Pieces_Variants.append([[Pieces_Variants[0][len(Pieces_Variants[0]) - i - 1][len(Pieces_Variants[0][0]) - j - 1] for j in range(len(Pieces_Variants[0][0]))] for i in range(len(Pieces_Variants[0]))])
    #Find piece rotated 270 degrees
    Pieces_Variants.append([[Pieces_Variants[0][len(Pieces_Variants[0]) - j - 1][i] for j in range(len(Pieces_Variants[0]))] for i in range(len(Pieces_Variants[0][0]))])
    #Find piece flipped
    Pieces_Variants.append([[Pieces_Variants[0][len(Pieces_Variants[0]) - i - 1][j] for j in range(len(Pieces_Variants[0][0]))] for i in range(len(Pieces_Variants[0]))])
    #Find piece flipped and rotated 90 degrees
    Pieces_Variants.append([[Pieces_Variants[4][j][len(Pieces_Variants[0][0]) - i - 1] for j in range(len(Pieces_Variants[0]))] for i in range(len(Pieces_Variants[0][0]))])
    #Find piece flipped and rotated 180 degrees
    Pieces_Variants.append([[Pieces_Variants[4][len(Pieces_Variants[0]) - i - 1][len(Pieces_Variants[0][0]) - j - 1] for j in range(len(Pieces_Variants[0][0]))] for i in range(len(Pieces_Variants[0]))])
    #Find piece flipped and rotated 270 degrees
    Pieces_Variants.append([[Pieces_Variants[4][len(Pieces_Variants[0]) - j - 1][i] for j in range(len(Pieces_Variants[0]))] for i in range(len(Pieces_Variants[0][0]))])
    Puzzle_Places.append([])
    for i in range(len(Pieces_Variants)):
        Variables["piece_size_x"] = len(Pieces_Variants[i])
        Variables["piece_size_y"] = len(Pieces_Variants[i][0])
        for j in range(Variables["grid_size_x"] - Variables["piece_size_x"] + 1):
            for k in range(Variables["grid_size_y"] - Variables["piece_size_y"] + 1):
                Puzzle_Places[piece].append([])
                for l in range(Variables["piece_size_x"]):
                    for m in range(Variables["piece_size_y"]):
                        if Pieces_Variants[i][l][m] == 1:
                            Puzzle_Places[piece][len(Puzzle_Places[piece]) - 1].append([j + l, k + m])
    #Remove duplicate places
    Puzzle_Places[piece].reverse()
    for i in Puzzle_Places[piece]:
        if Puzzle_Places[piece].count(i) > 1:
            for j in range(Puzzle_Places[piece].count(i) - 1):
                Puzzle_Places[piece].remove(i)
    Puzzle_Places[piece].reverse()
#Solve a puzzle
def puzzle_solve():
    for i in range(Variables["pieces"]):
        puzzle_find(i)
    puzzle_tile([0, 0])
    Variables["page"] = 2
#Check all ways of placing a piece
def puzzle_tile(tile):
    #Check next empty tile
    if Grid[tile[0]][tile[1]] > -1 or Grid[tile[0]][tile[1]] == -2:
        if tile[1] == Variables["grid_size_y"] - 1:
            puzzle_tile([tile[0] + 1, 0])
        elif tile[0] < Variables["grid_size_x"] - 1 and tile[1] < Variables["grid_size_y"] - 1:
            puzzle_tile([tile[0], tile[1] + 1])
    else:
        for i in range(len(Puzzle_Places)):
            for j in range(len(Puzzle_Places[i])):
                if tile in Puzzle_Places[i][j] and not i in Pieces_Placed:
                    #Find whether tiles are empty or not
                    Empty_Tiles = [Grid[Puzzle_Places[i][j][k][0]][Puzzle_Places[i][j][k][1]] == -1 for k in range(len(Puzzle_Places[i][j]))]
                    #Place piece if all tiles are empty
                    if not False in Empty_Tiles:
                        for k in range(len(Puzzle_Places[i][j])):
                            Grid[Puzzle_Places[i][j][k][0]][Puzzle_Places[i][j][k][1]] = i
                        Pieces_Placed.append(i)
                        #Draw screen to show piece
                        draw(screen)
                        #Check for no empty tiles
                        Grid_Empty = [-1 in Grid[i] for i in range(Variables["grid_size_x"])]
                        if not (True in Grid_Empty):
                            Variables["solved"] = True
                        if not Variables["solved"]:
                            #Check next empty tile
                            if tile[1] == Variables["grid_size_y"] - 1:
                                puzzle_tile([tile[0] + 1, 0])
                            elif tile[0] < Variables["grid_size_x"] - 1 and tile[1] < Variables["grid_size_y"] - 1:
                                puzzle_tile([tile[0], tile[1] + 1])
                            #Remove piece
                            if not Variables["solved"]:
                                for k in range(len(Puzzle_Places[i][j])):
                                    Grid[Puzzle_Places[i][j][k][0]][Puzzle_Places[i][j][k][1]] = -1
                                Pieces_Placed.remove(i)
def draw(screen):
    screen.fill((  0, 32,  64))
    if Variables["page"] == 0:
        pygame.draw.rect(screen, (  0,  24,  48), [0, 0, Config["ScreenX"] / 3, Config["ScreenY"]])
        font = pygame.font.SysFont("bahnschrift", 40)
        text = font.render("Pieces", True, (255, 255, 255))
        text_rect = text.get_rect(center=(Config["ScreenX"] / 6, 40))
        screen.blit(text, text_rect)
        font = pygame.font.SysFont("bahnschrift", 60)
        text = font.render("Polyomino Solver", True, (255, 255, 255))
        text_rect = text.get_rect(center=(Config["ScreenX"] * (2 / 3), 40))
        screen.blit(text, text_rect)
        sprites_group_tile.draw(screen)
        sprites_group_ui.draw(screen)
        sprites_group_piece.draw(screen)
    elif Variables["page"] == 1:
        font = pygame.font.SysFont("bahnschrift", 60)
        text = font.render("Solving...", True, (255, 255, 255))
        text_rect = text.get_rect(center=(Config["ScreenX"] / 2, 40))
        screen.blit(text, text_rect)
    elif Variables["page"] == 2:
        if Variables["solved"]:
            font = pygame.font.SysFont("bahnschrift", 60)
            text = font.render("Solution", True, (255, 255, 255))
            text_rect = text.get_rect(center=(Config["ScreenX"] / 2, 40))
            screen.blit(text, text_rect)
        else:
            screen.fill((  0,   0,   0))
            font = pygame.font.SysFont("bahnschrift", 60)
            text = font.render("There is no solution.", True, (255, 255, 255))
            text_rect = text.get_rect(center=(Config["ScreenX"] / 2, Config["ScreenY"] / 2))
            screen.blit(text, text_rect)
    if Variables["page"] == 1 or Variables["solved"]:
        for i in range(Variables["grid_size_x"]):
            for j in range(Variables["grid_size_y"]):
                if Grid[i][j] > -2:
                    pygame.draw.rect(screen, ( 79, 103, 128), [i * 60 + 2 + Config["ScreenX"] / 2 - Variables["grid_size_x"] * 30, j * 60 + 2 + Config["ScreenY"] / 2 - Variables["grid_size_y"] * 30, 56, 56])
                    if Grid[i][j] > -1:
                        pygame.draw.rect(screen, Pieces_Color[Grid[i][j]], [i * 60 + Config["ScreenX"] / 2 - Variables["grid_size_x"] * 30, j * 60 + Config["ScreenY"] / 2 - Variables["grid_size_y"] * 30, 60, 60])
    pygame.display.update()
def main():
    global screen
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((Config["ScreenX"], Config["ScreenY"]))
    pygame.display.set_caption(Config["ScreenCaption"])
    #Make buttons
    sprite = UI_Button(0, Config["ScreenX"] * (2 / 3), Config["ScreenY"] - 90, 120, 40, (255, 255, 255), (  0,   0,   0), "bahnschrift", 20, "Add Row")
    sprites_group_ui.add(sprite)
    sprite = UI_Button(1, Config["ScreenX"] * (2 / 3), Config["ScreenY"] - 40, 120, 40, (255, 255, 255), (  0,   0,   0), "bahnschrift", 20, "Remove Row")
    sprites_group_ui.add(sprite)
    sprite = UI_Button(2, Config["ScreenX"] * (2 / 3) + 130, Config["ScreenY"] - 90, 120, 40, (255, 255, 255), (  0,   0,   0), "bahnschrift", 20, "Add Column")
    sprites_group_ui.add(sprite)
    sprite = UI_Button(3, Config["ScreenX"] * (2 / 3) + 130, Config["ScreenY"] - 40, 120, 40, (255, 255, 255), (  0,   0,   0), "bahnschrift", 20, "Remove Column")
    sprites_group_ui.add(sprite)
    sprite = UI_Button(4, Config["ScreenX"] * (2 / 3) - 130, Config["ScreenY"] - 40, 120, 40, (191, 255, 191), (  0,   0,   0), "bahnschrift", 20, "Solve")
    sprites_group_ui.add(sprite)
    #Make piece buttons
    for i in range(7):
        for j in range(3):
            sprite = UI_Button_Piece(i * 3 + j, i * 55 + 30, j * 55 + 120)
            sprites_group_ui.add(sprite)
    #Make tiles
    for i in range(Variables["grid_size_x"]):
        for j in range(Variables["grid_size_y"]):
            sprite = Tile(i, j)
            sprites_group_tile.add(sprite)
    draw(screen)
    while True:
        Variables["mouse_x"], Variables["mouse_y"] = pygame.mouse.get_pos()
        Variables["click_used_left"] = False
        Variables["click_used_right"] = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        sprites_group_piece.update()
        sprites_group_tile.update()
        sprites_group_ui.update()
        if not Variables["click_used_left"] and pygame.mouse.get_pressed()[0] == 1:
            Variables["click_used_left"] = True
            Variables["piece_drag"] = -1
            Variables["piece_select"] = -1
        else:
            Variables["click_ready"] = True
        if not Variables["click_used_right"] and pygame.mouse.get_pressed()[2] == 1:
            Variables["click_used_right"] = True
            Variables["piece_drag"] = -1
        clock.tick(Config["Framerate"])
if __name__ == "__main__":
    main()