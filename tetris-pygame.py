import pygame, sys, random
from pygame.locals import *

class Grille:
    def __init__(self, x, y):
        self.matrice = [[ESPACE for i in range(y)] for j in range(x)]
        self.longueur = x
        self.largeur = y


class Piece:
    def __init__(self):
        piece_choisi = random.choice(PIECES)
        self.couleur = piece_choisi[0]
        self.centre = piece_choisi[1]
        self.liste_blocks = piece_choisi[2:]
        print(PIECES[0])

    def verif_pos(self):
        ### Vérifie et modifie les coordonés ###
        verif = True
        for block in self.liste_blocks:
            if grille.matrice[block[0]][block[1] + 1][0] == "block" and [block[0], block[1] + 1] not in self.liste_blocks:
                verif = False
                break
        return verif

    def actualise_pos(self):
        ### Efface ###
        for block in self.liste_blocks:
            grille.matrice[block[0]][block[1]] = ESPACE
            print("EFFACE")

        ### Actualise les valeurs ###
        for block in range(len(self.liste_blocks)):
            self.liste_blocks[block][1] += 1
            print("ACTUALISE VALEURS")

        ### Actualise la grille ###
        for block in self.liste_blocks:
            print("ACTUALISE GRILLE")
            grille.matrice[block[0]][block[1]] = ["block", self.couleur]



    # def verif_point_mange(self):
    #     if self.pos == point.pos:     ## Si le point est mangé
    #         point.spawn_point()
    #         self.blocks += 1
    #         Var.SCORE += 1
    #         pygame.display.set_caption('Snake - Score: {}'.format(Var.SCORE))
    #         Var.FPS += 0.25


def blocks2pixels(x, y):
    return (x * BLOCK_DIM), (y * BLOCK_DIM)

def dessine():
    ### Murs ###
    for block_y in range(GRILLE_LARG):
        x, y = blocks2pixels(0, block_y)
        if block_y == 0 or block_y == GRILLE_LARG - 1:
            for block_x in range(GRILLE_LONG):
                grille.matrice[block_x][block_y] = MUR
        else:
            grille.matrice[0][block_y] = MUR
            grille.matrice[GRILLE_LONG - 1][block_y] = MUR

    ### Éléments du jeu ###
    for block_x in range(GRILLE_LONG):
        for block_y in range(GRILLE_LARG):
            x, y = blocks2pixels(block_x, block_y)
            if grille.matrice[block_x][block_y] != ESPACE:
                pygame.draw.rect(DISPLAYSURF, grille.matrice[block_x][block_y][1], (x, y, BLOCK_DIM, BLOCK_DIM))


class Var:
    FPS = 20
    GAME_OVER = False
    PAUSED = False
    SCORE = 0

GRILLE_LONG = 12 # blocks
GRILLE_LARG = 24 # blocks
BLOCK_DIM = 20 # px
FENETRE_LONG = GRILLE_LONG * BLOCK_DIM
FENETRE_LARG = GRILLE_LARG * BLOCK_DIM

VERT = (0, 204, 0)
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
BG = (100, 100, 100)

CYAN = (0, 255, 255)
BLEU = (0, 0, 255)
ORANGE = (255, 128, 0)
JAUNE = (255, 255, 0)
LIME = (0,255,0)
MAUVE = (128, 0, 128)
ROUGE = (255, 0, 0)

ESPACE = ["espace", BG]
MUR = ["block", ORANGE]

BLOCK_CYAN = ["block", CYAN]
BLOCK_BLEU = ["block", BLEU ]
BLOCK_ORANGE = ["block", ORANGE]
BLOCK_JAUNE = ["block", JAUNE]
BLOCK_LIME = ["block", LIME]
BLOCK_MAUVE = ["block", MAUVE]
BLOCK_ROUGE = ["block", ROUGE]

BLOCKS = [BLOCK_CYAN, BLOCK_BLEU, BLOCK_ORANGE, BLOCK_JAUNE, BLOCK_LIME, BLOCK_MAUVE, BLOCK_ROUGE]

PIECE_I = [CYAN, [0, 0], [4, 1], [5, 1], [6, 1], [7, 1]]
PIECE_J = [BLEU, [0, 0], [4, 1], [4, 2], [5, 2], [6, 2]]
PIECE_L = [ORANGE, [0, 0], [6, 1], [4, 2], [5, 2], [6, 2]]
PIECE_O = [JAUNE, [0, 0], [5, 1], [6, 1], [5, 2], [6, 2]]
PIECE_S = [LIME, [0, 0], [5, 1], [6, 1], [4, 2], [5, 2]]
PIECE_T = [MAUVE, [0, 0], [5, 1], [4, 2], [5, 2], [6, 2]]
PIECE_Z = [ROUGE, [0, 0], [4, 1], [5, 1], [5, 2], [6, 2]]

PIECES = [PIECE_I]#, PIECE_J, PIECE_L, PIECE_O, PIECE_S, PIECE_T, PIECE_Z]

OBSTACLES = [MUR, BLOCKS, PIECES]

pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((FENETRE_LONG, FENETRE_LARG))
#pygame.display.set_caption('Snake - Score: {}'.format(Var.SCORE))
#message() # Juste pour l'initialisation

grille = Grille(GRILLE_LONG, GRILLE_LARG)

piece = Piece()

while True:
    #frame_direction = snake.direction

    DISPLAYSURF.fill(BG)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # if event.type == pygame.KEYDOWN:
        #     if Var.GAME_OVER == False and Var.PAUSED == False:
        #         if (event.key == pygame.K_UP or event.key == pygame.K_z) and frame_direction != "down":
        #             snake.direction = "up"
        #         elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and frame_direction != "up":
        #             snake.direction = "down"
        #         elif (event.key == pygame.K_LEFT or event.key == pygame.K_q) and frame_direction != "right":
        #             snake.direction = "left"
        #         elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and frame_direction != "left":
        #             snake.direction = "right"
        #
        #     if (event.key == pygame.K_SPACE or event.key == pygame.K_p) and Var.GAME_OVER == False:
        #         if Var.PAUSED == False:
        #             Var.PAUSED = True
        #             pygame.display.set_caption('Snake - Score: {} (Paused)'.format(Var.SCORE))
        #
        #         else:
        #             Var.PAUSED = False
        #             pygame.display.set_caption('Snake - Score: {}'.format(Var.SCORE))
        #
        #     if Var.GAME_OVER == True:
        #         if event.key == pygame.K_r:
        #             reset()
        #         elif event.key == pygame.K_ESCAPE:
        #             pygame.quit()
        #             sys.exit()


    if Var.GAME_OVER == False and Var.PAUSED == False:
        if piece.verif_pos() is True:
            piece.actualise_pos()
        else:
            piece = Piece()
    dessine()

    # if Var.PAUSED == True:
    #     message('Paused')
    #     DISPLAYSURF.blit(Var.textSurfaceObj, Var.textRectObj)
    #
    # if Var.GAME_OVER == True:
    #     message('Game Over')
    #     DISPLAYSURF.blit(Var.textSurfaceObj, Var.textRectObj)
    #     message('(appuyez [r] pour recommencer et [ESC] pour quitter)', 16, (FENETRE_LONG // 2, FENETRE_LARG // 2 + 30))
    #     DISPLAYSURF.blit(Var.textSurfaceObj, Var.textRectObj)
    #
    #     pygame.display.set_caption('Snake - Score: {} (Game Over)'.format(Var.SCORE))

    pygame.display.update()
    FPSCLOCK.tick(Var.FPS)
