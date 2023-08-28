import numpy as np
import matplotlib.pyplot as plt

#I MATRICE DE SCORE

#a)

#Lecture de Blosum62 et retour dico pairs:score
def read_bs(nomfi):

	#Initialisation dico
	Bs = {}
	
	#Ouverture du file
	with open(nomfi,'r') as ip :
		
		#Parcours by line
		i = 0
		for line in ip:
			#Zapper les commentaires
			if line[0]=='#':
				continue
			#Recuperation de alphabet
			if line[0]==' ':
				alpha=line.split()[:]
				continue
			#Isolement des scores
			else:
				lb = line.split()[1:]
				
				#Ajout des scores dans le dico
				for j in range(len(lb)):
					Bs[alpha[i]+alpha[j]] = int(lb[j])
			i+=1
	
	return Bs

#b)

def sous_mat(liste_an1,liste_an2,blosum):
	
	mat = np.empty((len(liste_an1),len(liste_an2)))
	
	for i in range(len(liste_an1)):
		for j in range(len(liste_an2)):
			mat[i,j] = blosum[liste_an1[i]+liste_an2[j]]
	return mat
	
bs = read_bs("BLOSUM62.txt")

ssmat1 = sous_mat(['D','E','K'],['D','E','K'],bs)
ssmat2 = sous_mat(['V','I','L'],['V','I','L'],bs)
ssmat3 = sous_mat(['D','E','K'],['V','I','L'],bs)

#print(ssmat1)
#print(ssmat2)
#print(ssmat3)

#c) score blosum62
print("Score moyen de blosum62 = ",np.mean(bs.values()))

#d) score ssmat
print("Score moyen de ssmat1 = ",np.mean(ssmat1))
print("Score moyen de ssmat2 = ",np.mean(ssmat2))
print("Score moyen de ssmat3 = ",np.mean(ssmat3))

#e) Score positif quand AA du même type, Score négatif quand AA de type différent



