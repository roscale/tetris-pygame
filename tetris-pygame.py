#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Rosca Alex 4TB
# tetris-pygame.py – 21.04.16

import pygame, sys, random
from pygame.locals import *
import copy

class Point:
    def __init__(self, tup):
        self.x = tup[0]
        self.y = tup[1]

    # Pour pouvoir comparer la position des bloques entre elles
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Block:
    def __init__(self, type_block, couleur):
        self.type_block = type_block
        self.couleur = couleur

class Grille:
    def __init__(self, x, y):
        self.matrice = [[ESPACE for i in range(y)] for j in range(x)]
        self.longueur = x
        self.largeur = y

    def efface_lignes_completes(self):
        collone = 1
        ligne = self.largeur - 2

        while ligne >= 1:
            ### Vérifie si la ligne est complète
            complete = True
            for collone in range(1, self.longueur - 1):
                #print(self.matrice[collone][ligne].type_block)
                if self.matrice[collone][ligne].type_block != "obstacle":
                    complete = False
                    #print("({}, {})".format(ligne, collone))

            if complete is True:
                print("({}, {})".format(ligne, collone))
                for ligne_c in range(ligne, 1, -1):
                    for collone_c in range(1, self.longueur - 1):
                        print(self.matrice[collone_c][ligne_c].type_block)
                        self.matrice[collone_c][ligne_c] = self.matrice[collone_c][ligne_c - 1]
                Var.SCORE += 10
                Var.VITESSE -= 10
            else:
                ligne -= 1
            #print("\n")


class Piece:
    directions = {"down":(0, +1), "left":(-1, 0), "right":(+1, 0), "meme":(0, 0)}

    def __init__(self):
        copyP = copy.deepcopy(PIECES)
        piece_choisi = random.choice(copyP)

        self.rotation = 0
        self.rotation_actuelle = 0
        self.couleur = piece_choisi[0]

        self.liste_blocks = []
        for i in range(1, 14, 4):
            self.liste_blocks.append(piece_choisi[i:i+4])
        #print(PIECES[0])
        self.deja_bouge = False


    def verif_pos(self, direction="meme", rotation=None):
        direction = Point(Piece.directions[direction])

        if rotation is None:
            rotation = self.rotation_actuelle

        ### Vérifie et modifie les coordonés ###
        verif = True
        for block in self.liste_blocks[rotation]:
            # try:
            # print(grille.matrice[block.x + direction.x][block.y + direction.y].type_block)
            print(block.x + direction.x)
            if grille.matrice[block.x + direction.x][block.y + direction.y].type_block == "obstacle":
                # print("DA")
                verif = False
                break
        # except:
            # verif = False
            # break
        return verif

    def actualise_pos(self, direction="meme", rotation=None):
        if direction is not tuple:
            direction = Point(Piece.directions[direction])

        if rotation is None:
            rotation = self.rotation_actuelle

        ### Efface ###
        #print(self.liste_blocks[0])
        for block in self.liste_blocks[self.rotation_actuelle]:
            grille.matrice[block.x][block.y] = ESPACE
            #print("EFFACE")

        c = 0
        ### Actualise les valeurs ###
        for rot in range(len(self.liste_blocks)):
            for block_pos in range(len(self.liste_blocks[rot])):
                self.liste_blocks[rot][block_pos].x += direction.x
                self.liste_blocks[rot][block_pos].y += direction.y
                #print("ACTUALISE VALEURS")
                c += 1
                # print("len rot {}".format(len(self.liste_blocks)))
                # print("({}, {})".format(self.liste_blocks[rot][block_pos].x, self.liste_blocks[rot][block_pos].y))
        print(c)

        ### Actualise la grille ###
        for block in self.liste_blocks[rotation]:
            #print("ACTUALISE GRILLE")
            grille.matrice[block.x][block.y] = Block("block", self.couleur)

        self.rotation_actuelle = rotation

    def tourne(self):
        ### Faire le cycle des rotations
        self.rotation += 1
        if self.rotation > 3:
            self.rotation = 0
        ### Verifier et actialiser la rotation
        if self.verif_pos(rotation=self.rotation) is True:
            self.actualise_pos(rotation=self.rotation)
        else:
            ### Revenir à la rotation précédente
            self.rotation -= 1

    def bouge2pos(self, pos):
        if self.deja_bouge == False:
            for block in self.liste_blocks[0]:
                block.x += pos.x
                block.y += pos.y
            self.deja_bouge = True

        for block in self.liste_blocks[0]:
            x, y = blocks2pixels(block.x, block.y - 2)
            pygame.draw.rect(DISPLAYSURF, self.couleur, (x, y, BLOCK_DIM, BLOCK_DIM))




def blocks2pixels(x, y):
    return (x * BLOCK_DIM), (y * BLOCK_DIM)

def dessine_grille():
    ### Murs ###
    for block_y in range(GRILLE_LARG - 1):
        grille.matrice[0][block_y] = MUR
        grille.matrice[GRILLE_LONG - 1][block_y] = MUR

    ### Sol
    for block_x in range(GRILLE_LONG):
        grille.matrice[block_x][block_y + 1] = MUR

    ### Éléments du jeu ###
    for block_x in range(GRILLE_LONG):
        for block_y in range(2, GRILLE_LARG):
            x, y = blocks2pixels(block_x, block_y - 2)
            if grille.matrice[block_x][block_y] != ESPACE:
                pygame.draw.rect(DISPLAYSURF, grille.matrice[block_x][block_y].couleur, (x, y, BLOCK_DIM, BLOCK_DIM))

def message(msg='', dim=32, pos=None):
    if pos is None:
        pos = FENETRE_LONG // 2, FENETRE_LARG // 2
    Var.fontObj = pygame.font.Font('freesansbold.ttf', dim)
    Var.textSurfaceObj = Var.fontObj.render(msg, True, (255, 255, 255))
    Var.textRectObj = Var.textSurfaceObj.get_rect()
    Var.textRectObj.center = pos

def reset():
    global grille
    global piece
    Var.GAME_OVER = False
    Var.VITESSE = 500
    Var.SCORE = 0
    grille = Grille(GRILLE_LONG, GRILLE_LARG)
    piece = Piece()
    piece.actualise_pos()
    Var.TICKS = pygame.time.get_ticks()

class Var:
    TICKS = 0
    VITESSE = 500
    FPS = 30
    GAME_OVER = False
    SCORE = 0

GRILLE_LONG = 12 # blocks
GRILLE_LARG = 23 # blocks
BLOCK_DIM = 30 # px
FENETRE_LONG = GRILLE_LONG * BLOCK_DIM# + 5 * BLOCK_DIM
FENETRE_LARG = GRILLE_LARG * BLOCK_DIM + 2 * BLOCK_DIM# - 2 * BLOCK_DIM

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

ESPACE = Block("espace", BG)
MUR = Block("obstacle", ORANGE)

PIECE_I = [CYAN, Point((4, 1)), Point((5, 1)), Point((6, 1)), Point((7, 1)),
                 Point((5, -1)), Point((5, 0)), Point((5, 1)), Point((5, 2)),
                 Point((4, 1)), Point((5, 1)), Point((6, 1)), Point((7, 1)),
                 Point((5, -1)), Point((5, 0)), Point((5, 1)), Point((5, 2))]

PIECE_J = [BLEU, Point((4, 0)), Point((4, 1)), Point((5, 1)), Point((6, 1)),
                 Point((5, 0)), Point((6, 0)), Point((5, 1)), Point((5, 2)),
                 Point((4, 1)), Point((5, 1)), Point((6, 1)), Point((6, 2)),
                 Point((5, 0)), Point((5, 1)), Point((4, 2)), Point((5, 2))]

PIECE_L = [ORANGE, Point((6, 0)), Point((4, 1)), Point((5, 1)), Point((6, 1)),
                   Point((5, 0)), Point((5, 1)), Point((5, 2)), Point((6, 2)),
                   Point((4, 1)), Point((5, 1)), Point((6, 1)), Point((4, 2)),
                   Point((4, 0)), Point((5, 0)), Point((5, 1)), Point((5, 2))]

PIECE_O = [JAUNE, Point((5, 0)), Point((6, 0)), Point((5, 1)), Point((6, 1)),
                  Point((5, 0)), Point((6, 0)), Point((5, 1)), Point((6, 1)),
                  Point((5, 0)), Point((6, 0)), Point((5, 1)), Point((6, 1)),
                  Point((5, 0)), Point((6, 0)), Point((5, 1)), Point((6, 1))]

PIECE_S = [LIME, Point((5, 0)), Point((6, 0)), Point((4, 1)), Point((5, 1)),
                 Point((5, -1)), Point((5, 0)), Point((6, 0)), Point((6, 1)),
                 Point((5, 0)), Point((6, 0)), Point((4, 1)), Point((5, 1)),
                 Point((5, -1)), Point((5, 0)), Point((6, 0)), Point((6, 1))]

PIECE_T = [MAUVE, Point((5, 0)), Point((4, 1)), Point((5, 1)), Point((6, 1)),
                  Point((5, 0)), Point((5, 1)), Point((6, 1)), Point((5, 2)),
                  Point((4, 1)), Point((5, 1)), Point((6, 1)), Point((5, 2)),
                  Point((5, 0)), Point((4, 1)), Point((5, 1)), Point((5, 2))]

PIECE_Z = [ROUGE, Point((4, 0)), Point((5, 0)), Point((5, 1)), Point((6, 1)),
                  Point((6, -1)), Point((5, 0)), Point((6, 0)), Point((5, 1)),
                  Point((4, 0)), Point((5, 0)), Point((5, 1)), Point((6, 1)),
                  Point((6, -1)), Point((5, 0)), Point((6, 0)), Point((5, 1))]


PIECES = (PIECE_I, PIECE_J, PIECE_L, PIECE_O, PIECE_S, PIECE_T, PIECE_Z)

pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((FENETRE_LONG, FENETRE_LARG))
pygame.key.set_repeat(200, 50)

grille = Grille(GRILLE_LONG, GRILLE_LARG)

piece = Piece()
piece_prochaine = Piece()
piece_prochaine.bouge2pos(Point((0, GRILLE_LARG + 1)))

# piece_prochaine.actualise_pos
piece.actualise_pos()


while True:
    DISPLAYSURF.fill(BG)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if Var.GAME_OVER is False:
                if event.key == pygame.K_UP or event.key == pygame.K_z:
                    piece.tourne()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if piece.verif_pos("down") is True:
                        piece.actualise_pos("down")
                        Var.TICKS = pygame.time.get_ticks() ###
                elif event.key == pygame.K_LEFT or event.key == pygame.K_q:
                    if piece.verif_pos("left") is True:
                        piece.actualise_pos("left")
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if piece.verif_pos("right") is True:
                        piece.actualise_pos("right")
                elif event.key == pygame.K_SPACE:
                    while piece.verif_pos("down") is True:
                        piece.actualise_pos("down")

                    Var.TICKS = pygame.time.get_ticks() - Var.VITESSE

            else:
                if event.key == pygame.K_r:
                    reset()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    if Var.GAME_OVER is False:
        pygame.display.set_caption('Tetris - Score: {}'.format(Var.SCORE))
        ### Attend le moment d'actualiser la pièce
        if pygame.time.get_ticks() - Var.TICKS > Var.VITESSE:
            if piece.verif_pos("down") is True:
                piece.actualise_pos("down")
            else:
                ### Transforme la pièce dans un obstacle
                for block in piece.liste_blocks[piece.rotation_actuelle]:
                    print("ACTUALISE GRILLE")
                    grille.matrice[block.x][block.y] = Block("obstacle", piece.couleur)

                ### Verifie et efface les lignes complètes
                grille.efface_lignes_completes()

                ### Copie la piece prochaine et fais une nouvelle
                piece = copy.deepcopy(piece_prochaine)
                piece.deja_bouge = False
                piece.bouge2pos(Point((0, -(GRILLE_LARG + 1))))
                piece_prochaine = Piece()
                piece_prochaine.bouge2pos(Point((0, GRILLE_LARG + 1)))

                if piece.verif_pos() is True:
                    piece.actualise_pos()
                else:
                    Var.GAME_OVER = True

            Var.TICKS = pygame.time.get_ticks()

    dessine_grille()
    piece_prochaine.bouge2pos(Point((0, GRILLE_LARG + 1)))

    if Var.GAME_OVER is True:
        message('Game Over')
        DISPLAYSURF.blit(Var.textSurfaceObj, Var.textRectObj)
        message('(appuyez [r] pour recommencer ou [ESC] pour quitter)', 13, (FENETRE_LONG // 2, FENETRE_LARG // 2 + 30))
        DISPLAYSURF.blit(Var.textSurfaceObj, Var.textRectObj)

    pygame.display.update()
    FPSCLOCK.tick(Var.FPS)
