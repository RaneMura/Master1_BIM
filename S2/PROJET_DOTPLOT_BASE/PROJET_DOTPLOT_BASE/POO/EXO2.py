import random

class JeuDeCartes:
	def __init__(self):
		self.liste = list()
		for i in range(13):
			for j in range(4):
				self.liste.append((i,j))
	
	def nom_carte(self,carte):
		couleur = ['coeur','pique','carreau','trefle']
		valeur = ['A','2','3','4','5','6','7','8','9','10','Valet','Dame','Roi']
		return valeur[carte[0]]+" de "+couleur[carte[1]]
	
	def battre(self):
		return random.shuffle(self.liste)
	
	def tirer(self):
		if len(self.liste)==0:
			return None
		a = self.liste[0]
		self.liste.remove(a)
		return a

#Q1
"""
jeu = JeuDeCartes()
jeu.battre()
for n in range(53):
	c = jeu.tirer()
	if c == None:
		print("Terminé !")
	else:
		print(jeu.nom_carte(c))

"""

#Q2
A = JeuDeCartes()
B = JeuDeCartes()
A.battre()
B.battre()
scoreA = 0
scoreB = 0
for n in range (53):
	c1 = A.tirer()
	c2 = B.tirer()
	if c1==None or c2 == None:
		print("Terminé !")
	else:
		if c1[0]>c2[0]:
			scoreA+=1
		if c1[0]<c2[0]:
			scoreB+=1
if scoreA>scoreB:
	print("Le gagnant est le joueur A\nScore du joueur A = "+str(scoreA)+"\nScore du joueur B = "+str(scoreB))
if scoreA<scoreB:
	print("Le gagnant est le joueur B\nScore du joueur A = "+str(scoreA)+"\nScore du joueur B = "+str(scoreB))
if scoreA==scoreB:
	print("Les deux joueurs sont à égalité\nScore du joueur A = "+str(scoreA)+"\nScore du joueur B = "+str(scoreB))    