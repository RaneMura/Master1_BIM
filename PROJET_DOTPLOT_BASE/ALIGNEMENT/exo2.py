import numpy as np
import matplotlib.pyplot as plt


#II ALIGNEMENT GLOBAL

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


#a)

#gap = -2

def constMat(s1,s2,gap):
	mat = np.zeros((len(s1)+1,len(s2)+1))
	for i in range(1,len(s1)+1):
		mat[i,0] = i*gap
	for j in range(1,len(s2)+1):
		mat[0,j] = j*gap
	return mat
#b)
def bestScore(M,i,j,score_ij,gap):
	score_gauche = 	M[i,j-1] + gap
	score_diag = M[i-1,j-1] + score_ij  
	score_haut = M[i-1,j] + gap 
	
	sm = max(score_gauche,score_diag,score_haut)
	M[i,j]=sm
	
	if sm == score_diag:
		return 'd'
	if sm == score_gauche:
		if  score_gauche > score_haut:
			return 'g'
	return 'h'
#c)
def aliNWS(s1,s2,bs,gap):
	matScore = constMat(s1,s2,gap)
	liste_tr = []
	for i in range(1,len(s1)+1):
		liste_trbis = []
		for j in range(1,len(s2)+1):
			sc = bs[s1[i-1]+s2[j-1]]
			liste_trbis.append(bestScore(matScore,i,j,sc,gap))
		liste_tr.append(liste_trbis)
	
	return matScore, np.asarray(liste_tr)

def cheminAli(s1,s2,tray):
	i = len(s1)-1
	j = len(s2)-1
	
	s1f = ""
	s2f = ""
	while i>=0 and j>=0:
		if tray[i,j]=='d':
			s1f = s1f + s1[i]
			s2f = s2f + s2[j]
			i = i-1
			j = j-1
		
		if tray[i,j]=='g':
			s1f = s1f + "_"
			s2f = s2f + s2[j]
			j = j-1
			
		if tray[i,j]=='h':
			s1f = s1f + s1[i]
			s2f = s2f + "_"
			i = i-1

	if i==-1:
		while j>=0:
			s1f = s1f + "_"
			s2f = s2f+ s2[j]
			j =j-1
	else: 
		while i>=0:
			s1f = s1f + s1[i]
			s2f = s2f+ "_"
			i=i-1
			
	return np.asarray([s1f[::-1],s2f[::-1]])


bs = read_bs("BLOSUM62.txt")
s1 = "PYRCKCR"
s2 = "MPRCLCQR"

ms,lister = aliNWS(s1,s2,bs,-2)

alig = cheminAli(s1,s2,lister)
print(alig)
	
	

