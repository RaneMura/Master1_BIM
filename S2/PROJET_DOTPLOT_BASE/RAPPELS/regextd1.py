#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 13:57:24 2023

@author: 3701883
"""

"""
Expressions régulières (regexp)
    Trouver des motifs dans des chaines de caractères
"""

import re
    
chaine = 'fjisosdciofgjschatojfpijgofsjgoz'
regex = re.compile('chat')
    
if regex.search(chaine):
    print('ok')

"""
    ^ -> début de chaîne
    $ -> fin de chaîne
    . -> n'importe quel caractère
    \w -> n'importe quel lettre
    \W -> tout sauf une lettre
    \d -> n'importe quel chiffre
    \D-> tout sauf un chiffre
    \s espace ou TAB
    \S tout sauf une espace ou TAB
    [abc] -> a ou b ou c
    [^abc] -> tout sauf a,b,c
    ? -> 0 ou 1 fois
    + -> au moins 1 fois
    * -> de 0 à n fois
    \ -> échappement
    \\ -> backslash
    \+ -> un plus
    \. -> un point 
    
"""

chaine2 = 'fjisosdciofgjscatojfpcratijgofsjgoz'
regex2 = re.compile('c.at')
if regex2.search(chaine2):
    print('ok2')
    
"""
c[abc]at -> caat,cbat,ccat
c[^abc]at -> cdat, ceat

c.?at -> cat, caat, cbat 
c.+at-> caat,cbat

trouver une séquence type __:234:___ -> :\d+:
trouver :26.76: -> :\d+\.?\d+: (au moins un chiffre, peut etre un point et un chiffre)
() -> capturer la valeur de la chaine

"""
chaine3 = 'djfqosjfqusonfgpqok:27.86:qosfsfff6hrjth5:66985.12:dfjsqhfouzheijfef:12:fksgljsdsgs'
regex3 = re.compile(':(\d+\.?\d+):')
resultat = regex3.search(chaine3)
if(resultat!=None):
    print(resultat.group(0))

resultat2 = regex3.findall(chaine3)
if(resultat2!=None):
    print(resultat2)
    
"""
Lire un fichier texte:
    infile = open('fichier.txt','r')
    for  line in infile : -> LIT LE FICHIER LIGNE PAR LIGNE
        ALGO
    infile.close()
    
EXO POSSIBLE : DICO : IDENTIFIANT: SEQUENCE dans un fasta

D = dict()
infile = open('fichier.fasta','r')
seq = ''
for line in infile :
    if line[0]=='>':
        if seq!='':
            D[ident]= seq
        ident = line[1:-1] (dernier caractère est un retour chariot)
        seq = ''
    else :
        seq = seq+line[:-1]
D[ident]=seq
    