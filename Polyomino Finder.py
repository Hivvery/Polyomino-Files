#SETUP
import math, pygame, sys
pygame.init()

#DICTIONARIES
Config = {
    #Frames per second
    "framerate": 60,
    #Window name
    "screen_caption": "Polyomino Finder",
    #Window width and height in pixels
    "screen_x": 360,
    "screen_y": 360,
}
Variables = {
    #Starting amount of cells the polyominoes will be made of
    "cells": 1,
    #Grid width and height
    "grid_x": 1,
    "grid_y": 1,
    #Type of polyomino based on rotations and symmetry
    "polyomino_type": "",
    #Size of each tile in pixels
    "tile_size": 0,
}

#LISTS
#Grid information
Grid = [[0 for i in range(Variables["grid_y"])] for i in range(Variables["grid_x"])]
#Polyominoes found
Polyominoes = []
Polyominoes_Grid = []
#Amounts of the types of polyominoes found
Polyomino_Types = [0, 0, 0, 0, 0, 0, 0, 0]
Polyomino_Types_Grid = [0, 0, 0, 0, 0, 0, 0, 0]
#Tiles checked for tile chunks
Tiles_Chunk = []

#FUNCTIONS
#Find a chunk of cells connected together
def chunk(tile):
    Tiles_Chunk.append(tile)
    #Check left tile
    if tile[0] > 0 and Grid[tile[0] - 1][tile[1]] == 1 and not [tile[0] - 1, tile[1]] in Tiles_Chunk:
        chunk([tile[0] - 1, tile[1]])
    #Check right tile
    if tile[0] < Variables["grid_x"] - 1 and Grid[tile[0] + 1][tile[1]] == 1 and not [tile[0] + 1, tile[1]] in Tiles_Chunk:
        chunk([tile[0] + 1, tile[1]])
    #Check up tile
    if tile[1] > 0 and Grid[tile[0]][tile[1] - 1] == 1 and not [tile[0], tile[1] - 1] in Tiles_Chunk:
        chunk([tile[0], tile[1] - 1])
    #Check down tile
    if tile[1] < Variables["grid_y"] - 1 and Grid[tile[0]][tile[1] + 1] == 1 and not [tile[0], tile[1] + 1] in Tiles_Chunk:
        chunk([tile[0], tile[1] + 1])
#Find all permutations with an amount of tiles and an amount of cells
def generate_permutations(items, cells):
    Numbers = [0] * (items - cells) + [1] * cells
    Permutations = []
    def generate(Current, remaining):
        if len(Current) == items:
            Permutations.append(Current)
            return
        if remaining > 0:
            generate(Current + [1], remaining - 1)
        if len(Current) + remaining < items:
            generate(Current + [0], remaining)
    generate([], cells)
    return Permutations
#Display the most recently found polyomino on the screen
def draw(screen):
    screen.fill((  0,   0,   0))
    #Set tile size based on grid width
    Variables["tile_size"] = Config["screen_x"] / Variables["grid_x"]
    #Use a lighter black color for the grid
    pygame.draw.rect(screen, (  0,  32,  64), [0, 0, Config["screen_x"], Variables["grid_y"] * Variables["tile_size"]])
    for i in range(Variables["grid_x"]):
        for j in range(Variables["grid_y"]):
            if Grid[i][j] == 1:
                #Draw cells with a certain color based on the polyomino type
                if Variables["polyomino_type"] == "1R-HD":
                    pygame.draw.rect(screen, (128, 255, 255), [i * Variables["tile_size"], j * Variables["tile_size"], math.ceil(Variables["tile_size"]), math.ceil(Variables["tile_size"])])
                if Variables["polyomino_type"] == "1R":
                    pygame.draw.rect(screen, (255, 255, 128), [i * Variables["tile_size"], j * Variables["tile_size"], math.ceil(Variables["tile_size"]), math.ceil(Variables["tile_size"])])
                if Variables["polyomino_type"] == "2R-H":
                    pygame.draw.rect(screen, (255, 128, 255), [i * Variables["tile_size"], j * Variables["tile_size"], math.ceil(Variables["tile_size"]), math.ceil(Variables["tile_size"])])
                if Variables["polyomino_type"] == "2R-D":
                    pygame.draw.rect(screen, (255, 191, 128), [i * Variables["tile_size"], j * Variables["tile_size"], math.ceil(Variables["tile_size"]), math.ceil(Variables["tile_size"])])
                if Variables["polyomino_type"] == "2R":
                    pygame.draw.rect(screen, (128, 128, 255), [i * Variables["tile_size"], j * Variables["tile_size"], math.ceil(Variables["tile_size"]), math.ceil(Variables["tile_size"])])
                if Variables["polyomino_type"] == "4R-H":
                    pygame.draw.rect(screen, (255, 128, 128), [i * Variables["tile_size"], j * Variables["tile_size"], math.ceil(Variables["tile_size"]), math.ceil(Variables["tile_size"])])
                if Variables["polyomino_type"] == "4R-D":
                    pygame.draw.rect(screen, (128, 255, 128), [i * Variables["tile_size"], j * Variables["tile_size"], math.ceil(Variables["tile_size"]), math.ceil(Variables["tile_size"])])
                if Variables["polyomino_type"] == "4R":
                    pygame.draw.rect(screen, (255, 255, 255), [i * Variables["tile_size"], j * Variables["tile_size"], math.ceil(Variables["tile_size"]), math.ceil(Variables["tile_size"])])
    pygame.display.update()
def main():
    #Make lists global
    global Grid
    global Permutations
    global Polyomino_Types
    global Polyomino_Types_Grid
    global Tiles_Chunk
    #Setup window
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((Config["screen_x"], Config["screen_y"]))
    pygame.display.set_caption(Config["screen_caption"])
    while True:
        Permutations = generate_permutations(Variables["grid_x"] * Variables["grid_y"], Variables["cells"])
        for j in range(len(Permutations)):
            #Set grid based on a permutation
            Grid = [[Permutations[j][k + l * Variables["grid_x"]] for l in range(Variables["grid_y"])] for k in range(Variables["grid_x"])]
            #Check for at least one cell in every row and column
            Columns_Ones = []
            for k in range(Variables["grid_x"]):
                Columns_Ones.append(1 in Grid[k])
            Rows_Ones = []
            for k in range(Variables["grid_y"]):
                Rows_Ones.append(1 in [Grid[l][k] for l in range(Variables["grid_x"])])
            if not (False in Columns_Ones or False in Rows_Ones):
                #Check for all the cells connected together
                chunk_1 = 0
                while Grid[chunk_1][0] != 1:
                    chunk_1 += 1
                Tiles_Chunk = []
                chunk([chunk_1, 0])
                if len(Tiles_Chunk) == Variables["cells"]:
                    #Find flipped and rotated versions of the polyomino
                    Polyomino_Variants = []
                    #Find polyomino
                    Polyomino_Variants.append(Grid)
                    #Find polyomino rotated 180 degrees
                    Polyomino_New = [[Grid[Variables["grid_x"] - i - 1][Variables["grid_y"] - j - 1] for j in range(Variables["grid_y"])] for i in range(Variables["grid_x"])]
                    Polyomino_Variants.append(Polyomino_New)
                    #Find polyomino flipped
                    Polyomino_New = [[Grid[Variables["grid_x"] - i - 1][j] for j in range(Variables["grid_y"])] for i in range(Variables["grid_x"])]
                    Polyomino_Variants.append(Polyomino_New)
                    #Find polyomino flipped and rotated 180 degrees
                    Polyomino_New = [[Grid[i][Variables["grid_y"] - j - 1] for j in range(Variables["grid_y"])] for i in range(Variables["grid_x"])]
                    Polyomino_Variants.append(Polyomino_New)
                    if Variables["grid_x"] == Variables["grid_y"]:
                        #Find polyomino rotated 90 degrees
                        Polyomino_New = [[Grid[j][Variables["grid_y"] - i - 1] for j in range(Variables["grid_y"])] for i in range(Variables["grid_x"])]
                        Polyomino_Variants.append(Polyomino_New)
                        #Find polyomino rotated 270 degrees
                        Polyomino_New = [[Grid[Variables["grid_x"] - j - 1][i] for j in range(Variables["grid_y"])] for i in range(Variables["grid_x"])]
                        Polyomino_Variants.append(Polyomino_New)
                        #Find polyomino flipped and rotated 90 degrees
                        Polyomino_New = [[Grid[Variables["grid_x"] - j - 1][Variables["grid_y"] - i - 1] for j in range(Variables["grid_y"])] for i in range(Variables["grid_x"])]
                        Polyomino_Variants.append(Polyomino_New)
                        #Find polyomino flipped and rotated 270 degrees
                        Polyomino_New = [[Grid[j][i] for j in range(Variables["grid_y"])] for i in range(Variables["grid_x"])]
                        Polyomino_Variants.append(Polyomino_New)
                    #Check that the polyomino is not a flipped/rotated version of an already found one
                    if len(Polyomino_Variants) == 4 and not (Polyomino_Variants[0] in Polyominoes or Polyomino_Variants[1] in Polyominoes or Polyomino_Variants[2] in Polyominoes or Polyomino_Variants[3] in Polyominoes) or len(Polyomino_Variants) == 8 and not (Polyomino_Variants[0] in Polyominoes or Polyomino_Variants[1] in Polyominoes or Polyomino_Variants[2] in Polyominoes or Polyomino_Variants[3] in Polyominoes or Polyomino_Variants[4] in Polyominoes or Polyomino_Variants[5] in Polyominoes or Polyomino_Variants[6] in Polyominoes or Polyomino_Variants[7] in Polyominoes):
                        Polyominoes.append(Grid)
                        Polyominoes_Grid.append(Grid)
                        #Check for symmetry
                        #1 rotation and symmetry (shown cyan)
                        if len(Polyomino_Variants) == 8 and Polyomino_Variants[0] == Polyomino_Variants[1] and Polyomino_Variants[0] == Polyomino_Variants[2] and Polyomino_Variants[0] == Polyomino_Variants[3] and Polyomino_Variants[0] == Polyomino_Variants[4] and Polyomino_Variants[0] == Polyomino_Variants[5] and Polyomino_Variants[0] == Polyomino_Variants[6] and Polyomino_Variants[0] == Polyomino_Variants[7]:
                            Variables["polyomino_type"] = "1R-HD"
                            Polyomino_Types[0] += 1
                            Polyomino_Types_Grid[0] += 1
                        #1 rotation (shown yellow)
                        elif len(Polyomino_Variants) == 8 and Polyomino_Variants[0] == Polyomino_Variants[1] and Polyomino_Variants[0] == Polyomino_Variants[4]:
                            Variables["polyomino_type"] = "1R"
                            Polyomino_Types[1] += 1
                            Polyomino_Types_Grid[1] += 1
                        #2 rotations and horizontal symmetry (shown pink)
                        elif Polyomino_Variants[0] == Polyomino_Variants[1] and (Polyomino_Variants[0] == Polyomino_Variants[2] or Polyomino_Variants[0] == Polyomino_Variants[3]):
                            Variables["polyomino_type"] = "2R-H"
                            Polyomino_Types[2] += 1
                            Polyomino_Types_Grid[2] += 1
                        #2 rotations and diagonal symmetry (shown orange)
                        elif len(Polyomino_Variants) == 8 and Polyomino_Variants[0] == Polyomino_Variants[1] and (Polyomino_Variants[0] == Polyomino_Variants[7] or Polyomino_Variants[0] == Polyomino_Variants[6]):
                            Variables["polyomino_type"] = "2R-D"
                            Polyomino_Types[3] += 1
                            Polyomino_Types_Grid[3] += 1
                        #2 rotations (shown blue)
                        elif Polyomino_Variants[0] == Polyomino_Variants[1]:
                            Variables["polyomino_type"] = "2R"
                            Polyomino_Types[4] += 1
                            Polyomino_Types_Grid[4] += 1
                        #4 rotations and horizontal symmetry (shown red)
                        elif Polyomino_Variants[0] == Polyomino_Variants[2] or Polyomino_Variants[0] == Polyomino_Variants[3]:
                            Variables["polyomino_type"] = "4R-H"
                            Polyomino_Types[5] += 1
                            Polyomino_Types_Grid[5] += 1
                        #4 rotations and diagonal symmetry (shown green)
                        elif len(Polyomino_Variants) == 8 and (Polyomino_Variants[0] == Polyomino_Variants[7] or Polyomino_Variants[0] == Polyomino_Variants[6]):
                            Variables["polyomino_type"] = "4R-D"
                            Polyomino_Types[6] += 1
                            Polyomino_Types_Grid[6] += 1
                        #4 rotations (shown white)
                        else:
                            Variables["polyomino_type"] = "4R"
                            Polyomino_Types[7] += 1
                            Polyomino_Types_Grid[7] += 1
                        draw(screen)
                        clock.tick(Config["framerate"])
        #Print results for grid size
        if len(Polyominoes_Grid) > 0:
            print(" " * (2 - len(str(Variables["cells"]))) + str(Variables["cells"]) + "C-" + str(Variables["grid_y"]) + "x" + str(Variables["grid_x"]) + ": " + " " * (6 - len(str(len(Polyominoes_Grid)))) + str(len(Polyominoes_Grid)) + " (" + " " * (2 - len(str(Polyomino_Types_Grid[0]))) + str(Polyomino_Types_Grid[0]) + " 1R-HD, " + " " * (2 - len(str(Polyomino_Types_Grid[1]))) + str(Polyomino_Types_Grid[1]) + " 1R, " + " " * (4 - len(str(Polyomino_Types_Grid[2]))) + str(Polyomino_Types_Grid[2]) + " 2R-H, " + " " * (4 - len(str(Polyomino_Types_Grid[3]))) + str(Polyomino_Types_Grid[3]) + " 2R-D, " + " " * (4 - len(str(Polyomino_Types_Grid[4]))) + str(Polyomino_Types_Grid[4]) + " 2R, " + " " * (4 - len(str(Polyomino_Types_Grid[5]))) + str(Polyomino_Types_Grid[5]) + " 4R-H, " + " " * (4 - len(str(Polyomino_Types_Grid[6]))) + str(Polyomino_Types_Grid[6]) + " 4R-D, " + " " * (6 - len(str(Polyomino_Types_Grid[7]))) + str(Polyomino_Types_Grid[7]) + " 4R)")
            Polyominoes_Grid.clear()
            Polyomino_Types_Grid = [0, 0, 0, 0, 0, 0, 0, 0]
        #Update grid dimensions
        Variables["grid_x"] += 1
        if Variables["grid_x"] + Variables["grid_y"] > Variables["cells"] + 1:
            Variables["grid_y"] += 1
            Variables["grid_x"] = Variables["grid_y"]
            if Variables["grid_y"] > math.ceil(Variables["cells"] / 2):
                #Print results
                print(" " * (2 - len(str(Variables["cells"]))) + str(Variables["cells"]) + "C-T: " + " " * (6 - len(str(len(Polyominoes)))) + str(len(Polyominoes)) + " (" + " " * (2 - len(str(Polyomino_Types[0]))) + str(Polyomino_Types[0]) + " 1R-HD, " + " " * (2 - len(str(Polyomino_Types[1]))) + str(Polyomino_Types[1]) + " 1R, " + " " * (4 - len(str(Polyomino_Types[2]))) + str(Polyomino_Types[2]) + " 2R-H, " + " " * (4 - len(str(Polyomino_Types[3]))) + str(Polyomino_Types[3]) + " 2R-D, " + " " * (4 - len(str(Polyomino_Types[4]))) + str(Polyomino_Types[4]) + " 2R, " + " " * (4 - len(str(Polyomino_Types[5]))) + str(Polyomino_Types[5]) + " 4R-H, " + " " * (4 - len(str(Polyomino_Types[6]))) + str(Polyomino_Types[6]) + " 4R-D, " + " " * (6 - len(str(Polyomino_Types[7]))) + str(Polyomino_Types[7]) + " 4R)")
                print()
                #Reset polyomino lists
                Polyominoes.clear()
                Polyomino_Types = [0, 0, 0, 0, 0, 0, 0, 0]
                Variables["cells"] += 1
                Variables["grid_x"] = Variables["cells"]
                Variables["grid_y"] = 1
if __name__ == "__main__":
    main()