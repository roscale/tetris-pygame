#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Rosca Alex 4TB
# tetris-pygame.py – 21.04.16

import pygame, sys, random
from pygame.locals import *
import copy
import pygame.gfxdraw

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Pour pouvoir comparer la position des bloques entre eux
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
        self.lignes_par_lvl = 5

    def efface_lignes_completes(self):
        collone = 1
        ligne = self.largeur - 2
        nbre_lignes_completes = 0
        lignes_completes = []

        ### Vérifie si la ligne est complète
        for ligne in range(self.largeur - 2, 0, -1):
            complete = True
            for collone in range(1, self.longueur - 1):
                if self.matrice[collone][ligne].type_block != "obstacle":
                    complete = False

            if complete is True:
                print("Effacé: ({}, {})\n********".format(ligne, collone)) # Debug
                nbre_lignes_completes += 1
                lignes_completes.append(ligne)
                Var.LIGNES_TOTAL += 1

        ### Si il y a des lignes complètes, fais l'animation
        if lignes_completes:
            self.efface_ligne_animation(lignes_completes)

        ### Efface les lignes complètes
        while lignes_completes:
            ligne = lignes_completes[0]
            for ligne_courrente in range(ligne, 1, -1):
                for collone_courrente in range(1, self.longueur - 1):
                    # Remplace le bloque actuel avec le block au dessous
                    self.matrice[collone_courrente][ligne_courrente] = self.matrice[collone_courrente][ligne_courrente - 1]

            lignes_completes.remove(ligne)
            for elem in range(len(lignes_completes)):
                lignes_completes[elem] += 1


        ### Augumente le score
        if nbre_lignes_completes == 1:
            Var.SCORE += 40 * (Var.LVL + 1)
        elif nbre_lignes_completes == 2:
            Var.SCORE += 100 * (Var.LVL + 1)
        elif nbre_lignes_completes == 3:
            Var.SCORE += 300 * (Var.LVL + 1)
        elif nbre_lignes_completes == 4:
            Var.SCORE += 1200 * (Var.LVL + 1)

        ### Augumente le niveau à chaque 5eme ligne complete
        if Var.LIGNES_TOTAL >= self.lignes_par_lvl:
            Var.VITESSE -= 25
            Var.LVL += 1
            self.lignes_par_lvl += 5

    def efface_ligne_animation(self, lignes_completes):
        ### Actualise l'écran pour l'avoir à jour
        dessine()
        pygame.display.update()

        ### Commence l'animation
        liste_rect_update = []
        for transparence in range(0, 250, 10):
            for ligne in lignes_completes:
                for collone_courrente in range(1, self.longueur - 1):
                    # Dessine juste les bloques qui doivent être animé
                    pygame.gfxdraw.box(DISPLAYSURF, (*blocks2pixels(collone_courrente, ligne), BLOCK_DIM, BLOCK_DIM),  (*self.matrice[collone_courrente][ligne].couleur, 255))

                # Crée un rectangle d'une ligne
                rectangle = pygame.Rect(BLOCK_DIM, (ligne - 2) * BLOCK_DIM, BLOCK_DIM * 10, BLOCK_DIM)
                # Ajoute-le dans la liste pour actualiser juste cette partie(+ rapide que d'actualiser tout l'écran)
                liste_rect_update.append(rectangle)
                # Applique l'éffet sur la ligne
                pygame.gfxdraw.box(DISPLAYSURF, rectangle, (*BLANC, transparence))

            pygame.time.delay(15) # 15
            # Actualise l'écran dans les zones de rectangles
            pygame.display.update(liste_rect_update)
            # Vider la liste pour qu'elle se regénère
            liste_rect_update = []


class Piece:
    directions = {"1up":(0, -1), "2up":(0, -2), "1down":(0, +1), "2down":(0, +2), "1left":(-1, 0), "2left":(-2, 0), "1right":(+1, 0), "2right":(+2, 0), "meme":(0, 0)}

    def __init__(self, pos):
        piece_choisi = Piece.genere_piece_aleatoire(pos.x, pos.y)

        self.couleur = piece_choisi[0]
        self.centre = piece_choisi[1]
        self.liste_blocks = piece_choisi[2:6]

    def genere_piece_aleatoire(x, y):
        PIECE_I = [CYAN, Point(x, y), Point(x-1, y), Point(x, y), Point(x+1, y), Point(x+2, y)]
        PIECE_J = [BLEU, Point(x, y), Point(x-1, y-1), Point(x-1, y), Point(x, y), Point(x+1, y)]
        PIECE_L = [ORANGE, Point(x, y), Point(x+1, y-1), Point(x-1, y), Point(x, y), Point(x+1, y)]
        PIECE_O = [JAUNE, Point(x, y), Point(x, y-1), Point(x+1, y-1), Point(x, y), Point(x+1, y)]
        PIECE_S = [LIME, Point(x, y), Point(x, y-1), Point(x+1, y-1), Point(x-1, y), Point(x, y)]
        PIECE_T = [MAUVE, Point(x, y), Point(x, y-1), Point(x-1, y), Point(x, y), Point(x+1, y)]
        PIECE_Z = [ROUGE, Point(x, y), Point(x-1, y-1), Point(x, y-1), Point(x, y), Point(x+1, y)]

        PIECES = (PIECE_I, PIECE_J, PIECE_L, PIECE_O, PIECE_S, PIECE_T, PIECE_Z)

        liste_pieces = copy.deepcopy(PIECES)
        piece_choisi = random.choice(liste_pieces)

        return piece_choisi

    def verif_pos(self, direction="meme"):
        if not isinstance(direction, tuple):
            direction = Point(*Piece.directions[direction])

        ### Vérifie les coordonés ###
        verif = True
        for block in self.liste_blocks:
            if grille.matrice[block.x + direction.x][block.y + direction.y].type_block == "obstacle":
                verif = False
                break

        return verif

    def actualise_pos(self, direction="meme"):
        if not isinstance(direction, tuple):
            direction = Point(*Piece.directions[direction])

        ### Efface ###
        for block in self.liste_blocks:
            grille.matrice[block.x][block.y] = ESPACE

        ### Actualise les valeurs ###
        for block_pos in range(len(self.liste_blocks)):
            self.liste_blocks[block_pos].x += direction.x
            self.liste_blocks[block_pos].y += direction.y
        self.centre.x += direction.x
        self.centre.y += direction.y

        ### Actualise la grille ###
        for block in self.liste_blocks:
            grille.matrice[block.x][block.y] = Block("block", self.couleur)

    def verif_tourne(self):
        verif = True
        for block in self.liste_blocks:
            x = block.x
            y = block.y

            # Calcule les coordonées relatives au centre
            x -= self.centre.x
            y -= self.centre.y

            # Tourne
            x, y = -y, x

            # Transforme dans des coordonées absolues
            x += self.centre.x
            y += self.centre.y

            if grille.matrice[x][y].type_block == "obstacle":
                verif = False
                break

        return verif

    def tourne(self):
        ### Efface ###
        for block in self.liste_blocks:
            grille.matrice[block.x][block.y] = ESPACE

        ### Actualise les valeurs ###
        for block_pos in range(len(self.liste_blocks)):
            x = self.liste_blocks[block_pos].x
            y = self.liste_blocks[block_pos].y

            # Calcule les coordonées relatives au centre
            x -= self.centre.x
            y -= self.centre.y

            # Tourne
            x, y = -y, x

            # Transforme dans des coordonées absolues
            x += self.centre.x
            y += self.centre.y

            # Actualise les coordonées
            self.liste_blocks[block_pos].x = x
            self.liste_blocks[block_pos].y = y

        ### Actualise la grille ###
        for block in self.liste_blocks:
            print("({}, {})".format(block.x, block.y)) # Debug
            grille.matrice[block.x][block.y] = Block("block", self.couleur)
        print("********") # Debug

    def move2pos(self, pos):
        x = pos.x - self.centre.x
        y = pos.y - self.centre.y

        for block in self.liste_blocks:
            block.x += x
            block.y += y

        self.centre.x += x
        self.centre.y += y




def blocks2pixels(x, y):
    # y-2 parcequ'il y a 2 lignes caché en haut(spawn zone), donc (0, 0) commence à la ligne 2
    return x * BLOCK_DIM, (y - 2) * BLOCK_DIM

def dessine():
    ### Murs ###
    for block_y in range(GRILLE_LARG - 1):
        grille.matrice[0][block_y] = MUR
        grille.matrice[GRILLE_LONG - 1][block_y] = MUR

    ### Sol ###
    for block_x in range(GRILLE_LONG):
        grille.matrice[block_x][block_y + 1] = MUR

    ### Pièces de la grille ###
    for block_x in range(GRILLE_LONG):
        for block_y in range(2, GRILLE_LARG):
            x, y = blocks2pixels(block_x, block_y)
            if grille.matrice[block_x][block_y] != ESPACE:
                pygame.gfxdraw.box(DISPLAYSURF, (x, y, BLOCK_DIM, BLOCK_DIM), (*grille.matrice[block_x][block_y].couleur, 255))

    ### Pièce prochaine ###
    for block in piece_prochaine.liste_blocks:
        x, y = blocks2pixels(block.x, block.y)
        pygame.gfxdraw.box(DISPLAYSURF, (x, y, BLOCK_DIM, BLOCK_DIM), (*piece_prochaine.couleur, 255))

    ### Stats ###
    message('Score: {}'.format(Var.SCORE), STATS_TEXT_DIM, (blocks2pixels(GRILLE_LONG + 3, 8)))
    DISPLAYSURF.blit(Var.textSurfaceObj, Var.textRectObj)

    message('Niveau: {}'.format(Var.LVL), STATS_TEXT_DIM, (blocks2pixels(GRILLE_LONG + 3, 9)))
    DISPLAYSURF.blit(Var.textSurfaceObj, Var.textRectObj)

    message('Lignes: {}'.format(Var.LIGNES_TOTAL), STATS_TEXT_DIM, (blocks2pixels(GRILLE_LONG + 3, 10)))
    DISPLAYSURF.blit(Var.textSurfaceObj, Var.textRectObj)

def message(msg, dim, pos):
    Var.fontObj = pygame.font.Font('freesansbold.ttf', int(dim))
    Var.textSurfaceObj = Var.fontObj.render(msg, True, BLANC)
    Var.textRectObj = Var.textSurfaceObj.get_rect()
    Var.textRectObj.center = pos

def reset():
    global grille
    global piece
    global piece_prochaine
    Var.GAME_OVER = False
    Var.VITESSE = 500
    Var.SCORE = 0
    Var.LVL = 0
    Var.LIGNES_TOTAL = 0
    grille = Grille(GRILLE_LONG, GRILLE_LARG)
    piece = Piece(Point(*PIECE_SPAWN_POS))
    piece.actualise_pos()
    piece_prochaine = Piece(Point(*PIECE_PROCHAINE_SPAWN_POS))
    Var.TICKS = pygame.time.get_ticks()

class Var:
    TICKS = 0
    VITESSE = 500
    FPS = 30
    GAME_OVER = False
    SCORE = 0
    LVL = 0
    LIGNES_TOTAL = 0

GRILLE_LONG = 12 # blocks
GRILLE_LARG = 23 # blocks
BLOCK_DIM = 30 # px
FENETRE_LONG = GRILLE_LONG * BLOCK_DIM + 6 * BLOCK_DIM
FENETRE_LARG = GRILLE_LARG * BLOCK_DIM - 2 * BLOCK_DIM
PIECE_SPAWN_POS = (GRILLE_LONG // 2 - 1, 1)
PIECE_PROCHAINE_SPAWN_POS = (GRILLE_LONG + 2, 5)
STATS_TEXT_DIM = BLOCK_DIM * 0.9

BLANC = (255, 255, 255)
GRIS = (175, 175, 175)
ROUGE_FONCE = (150, 0, 0)
BG = (100, 100, 100)

CYAN = (0, 255, 255)
BLEU = (0, 0, 255)
ORANGE = (255, 128, 0)
JAUNE = (255, 255, 0)
LIME = (0,255,0)
MAUVE = (128, 0, 128)
ROUGE = (255, 0, 0)

ESPACE = Block("espace", BG)
MUR = Block("obstacle", GRIS)


pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((FENETRE_LONG, FENETRE_LARG))
pygame.key.set_repeat(100, 40)

grille = Grille(GRILLE_LONG, GRILLE_LARG)

piece = Piece(Point(*PIECE_SPAWN_POS))
piece_prochaine = Piece(Point(*PIECE_PROCHAINE_SPAWN_POS))
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
                    if piece.verif_tourne() is True:
                        piece.tourne()
                    else:
                        ### Fais un wall-kick
                        sort = False
                        for kick_pos, kick_pos_inv in zip(("up", "left", "right"), ("down", "right", "left")):
                            for fois in ("1", "2"):
                                if piece.verif_pos(fois + kick_pos):
                                    piece.actualise_pos(fois + kick_pos)
                                    if piece.verif_tourne() is True:
                                        piece.tourne()
                                        sort = True
                                        break
                                    else:
                                        # Si ça échoue, mets la pièce ou elle était avant
                                        piece.actualise_pos(fois + kick_pos_inv)
                            if sort is True:
                                break

                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if piece.verif_pos("1down") is True:
                        piece.actualise_pos("1down")
                        Var.SCORE += 1
                        Var.TICKS = pygame.time.get_ticks()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_q:
                    if piece.verif_pos("1left") is True:
                        piece.actualise_pos("1left")
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if piece.verif_pos("1right") is True:
                        piece.actualise_pos("1right")
                elif event.key == pygame.K_SPACE:
                    while piece.verif_pos("1down") is True:
                        piece.actualise_pos("1down")
                        Var.SCORE += 2
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
            if piece.verif_pos("1down") is True:
                piece.actualise_pos("1down")
            else:
                ### Transforme la pièce dans un obstacle
                for block in piece.liste_blocks:
                    grille.matrice[block.x][block.y] = Block("obstacle", piece.couleur)

                ### Verifie et efface les lignes complètes
                grille.efface_lignes_completes()

                ### Copie la piece prochaine et fais une nouvelle
                piece = copy.deepcopy(piece_prochaine)
                piece.move2pos(Point(GRILLE_LONG // 2 - 1, 1))
                piece_prochaine = Piece(Point(GRILLE_LONG + 2, 5))

                ### Verifie si la position de départ est valide, sinon tout est rempli -> Game Over
                if piece.verif_pos() is True:
                    piece.actualise_pos()
                else:
                    Var.GAME_OVER = True

            ### Reset le timer
            Var.TICKS = pygame.time.get_ticks()

    dessine()

    if Var.GAME_OVER is True:
        pygame.gfxdraw.box(DISPLAYSURF, (0, FENETRE_LARG // 2 - BLOCK_DIM, FENETRE_LONG, BLOCK_DIM * 3), (*ROUGE_FONCE, 200))
        message('Game Over', BLOCK_DIM + 2, (FENETRE_LONG // 2, FENETRE_LARG // 2))
        DISPLAYSURF.blit(Var.textSurfaceObj, Var.textRectObj)
        message('(appuyez [r] pour recommencer ou [ESC] pour quitter)', BLOCK_DIM * 0.6, (FENETRE_LONG // 2, FENETRE_LARG // 2 + BLOCK_DIM))
        DISPLAYSURF.blit(Var.textSurfaceObj, Var.textRectObj)

    pygame.display.update()
    FPSCLOCK.tick(Var.FPS)
