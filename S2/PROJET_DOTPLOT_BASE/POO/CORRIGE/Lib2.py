# -*- coding:utf-8 -*-

import math
import random

class JeuDeCartes:
	def __init__(self):
		cartes = []
		for couleur in range(4):
			for valeur in range(13):
				cartes.append((valeur,couleur))
		self.cartes = cartes
		self.couleurs = ["Pique","Coeur","Carreau","Trèfle"]
		self.valeurs = ["Deux","Trois","Quatre","Cinq","Six","Sept","Huit","Neuf","Dix","Valet","Dame","Roi","As"]
	def nom_carte(self,t):
		texte = str(self.valeurs[t[0]])+" de "+str(self.couleurs[t[1]])
		return texte
	def battre(self):
		count = len(self.cartes)
		for i in range(count):
			j = random.randint(0,count-1)
			self.cartes[i], self.cartes[j] = self.cartes[j], self.cartes[i]
	def tirer(self):
		c = None
		if (len(self.cartes)>0):
			c = self.cartes[0]
			self.cartes.remove(c)
		return c

