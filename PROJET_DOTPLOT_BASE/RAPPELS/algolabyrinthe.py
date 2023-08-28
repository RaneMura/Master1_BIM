#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 14:47:16 2023

@author: 3701883
"""

"""
LABYRINTHE:
    ENSEMBLE DE CASES AVEC DES ESPACES et des MURS
    DES CASES SONT REMPLIS PAR LES MURS
    IL NE FAUT PAS DE CYCLE SINON CA SORT PAS
    LABYRINTHE : ON TOURNE TOUJOURS A DROITE
    
    MATRICE OU LISTE[LISTE]
    EXEMPLE : [[1,1,1,1,1],[1,0,0,0,1],[1,1,1,0,1],[1,0,0,0,1],[1,1,1,1,1]]
    
    SI Y A N PIECES, FAUT CASSER N-1 MURS
    METTRE DES CHIFFRES, COMMENCER DU PLUS ELEVE, CASSER LE MUR ET DONNER A
    L'ESPACE LIBÉRÉ LE CHIFFRE DU PLUS PETIT
    
    LOCALISER LES MURS EN 0
    LOCALISER LES PIÈCES EN CHIFFRES CROISSANTS

DÉBUT D'ALGO
    1) Créér une liste de listes avec des murs partout(0) et des numéros de pièces.
    
"""

import random 
import matplotlib.pyplot as plt

def init(N):
    L= [[] for k in range(N)]
    case = 1
    for i in range(N):
        for j in range(N):
            if(i%2!=0 and j%2!=0):
                L[i].append(case)
                case=case+1
            else:
                L[i].append(0)
    return L

L1 = init(11)

plt.imshow(L1,cmap=plt.get_cmap('gray'),interpolation='None')
plt.show()

def findw(L):
    n = len(L)
    tpw = []
    for i in range(1,n-1):
        for j in range(1,n-1):
            if(i%2==1 and j%2==0 and L[i][j-1]!=L[i][j+1]):
               tpw.append((i,j,L[i][j-1],L[i][j+1]))
            if(i%2==0 and j%2==1 and L[i-1][j]!=L[i+1][j]):
               tpw.append((i,j,L[i-1][j],L[i+1][j]))
           
               
    return tpw

def breakawall(L):
    walls = findw(L)
    N = (((len(L)-1)//2)**2)-1
    for w in range(N):
        x,y,v1,v2 = random.choice(walls)
        L[x][y] = min(v1,v2)
        for i in range(len(L)):
            for j in range(len(L)):
                if L[i][j]== max(v1,v2):
                    L[i][j]=min(v1,v2)        
        walls = findw(L)
    return L
    
L2 = breakawall(L1)
#plt.imshow(L2,cmap=plt.get_cmap('gray'),interpolation='None')
#plt.show()
plt.imshow(L2,cmap=plt.get_cmap('gray'),interpolation='None')
plt.show()

#RAY CASTING 
#FAIRE LE LABYRINTHE EN 3D
            
    
