# -*- coding:utf-8 -*-

from Lib2 import *

def duel():
	jeuA = JeuDeCartes()
	jeuA.battre()
	jeuB = JeuDeCartes()
	jeuB.battre()
	pointsA = 0
	pointsB = 0
	for n in range(52):
		A = jeuA.tirer()
		B = jeuB.tirer()
		if (A != None and B != None):
			#print (jeuA.nom_carte(A)+" CONTRE "+jeuB.nom_carte(B)+" :")
			if A[0] > B[0]:
				pointsA = pointsA+1
				#print ("A gagnant\n")
			elif B[0] > A[0]:
				pointsB = pointsB+1
				#print ("B gagnant\n")
			#else:
				#print ("Egalité\n")
	return(pointsA,pointsB)

print ("################### Tirage aléatoire sans remise des cartes du paquet ################")	
jeu = JeuDeCartes()
jeu.battre()
for n in range(53):
	c = jeu.tirer()
	if c == None:
		print("Terminé !")
	else:
		print(jeu.nom_carte(c))

print ("################### Jeu : Bataille ################")	
(a,b) = duel()
if (a>b):
	print ("A gagnant")
elif (b>a):
	print ("B gagnant")
else:
	print ("Egalité")

