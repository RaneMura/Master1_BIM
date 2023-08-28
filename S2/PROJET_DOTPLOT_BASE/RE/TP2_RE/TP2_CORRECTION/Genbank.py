import re
import string

####################################################################################
###############################       Fonctions         ############################
####################################################################################

# fonction qui affiche les aa d'un CDS au format fasta
def affiche(pos,sens,typ,trans,foutaa):
	taille_gene = abs(int(pos[1]) - int(pos[0]))
	if (trans == ""):
		trans = "It is a tRNA sequence ..."
	if sens ==0:
		sens = "direct"
	else:
		sens = "indirect"
	aff = ">"+str(pos[0])+".."+str(pos[1])+"\t"+str(sens)+"\t"+str(typ)
	#print(aff)
	foutaa.write(aff+'\n')
	end=0
	for i in range(0,len(trans)-79,80):
		#print(trans[i:i+80])
		foutaa.write(trans[i:i+80]+'\n')
		end = i+80
	if end<len(trans):
		#print(trans[end:len(trans)])
		foutaa.write(trans[end:len(trans)]+'\n')

# fonction qui affiche les nucleotides d'un CDS au format fasta		
def affiche_nuc(lpos,seqnuc,foutn):
	for tu in lpos:
		#print(">nuc"+str(tu[0])+".."+str(tu[1]))
		foutn.write(">nuc"+str(tu[0])+".."+str(tu[1])+'\n')
		c = seqnuc[int(tu[0]):int(tu[1])+1]
		for i in range(0,len(c)-79,80):
			#print(c[i:i+80])
			foutn.write(c[i:i+80]+'\n')
			end = i+80
		if end<len(c):
			#print(c[end:len(c)])
			foutn.write(c[end:len(c)]+'\n')

# fonction qui récupère les éléments d'intérêt et appèle les affichages
def extract_from(fic):
	of = open(fic,'r') # fichier lu (.dat)
	foutprot = open(fic[:-4]+".aa",'w') # fichier sortie cds en aa (.aa)
	foutnuc = open(fic[:-4]+".nuc",'w') # fichier sortie cds en nt (.nuc)
	trans = ""
	pos=""
	seq=""
	tem=0 # variable témoin traitement nouveau fichier .dat
	lpos=[] # Liste de stockage es positions des CDS
	ligne = of.readline()
	while (ligne != ""): 
		ligne = ligne.rstrip('\n')
		m = re.match("FT\s+(CDS|tRNA)\s+(complement|join)*(\()*(\d+)\..*\.(\d+)(\))*",ligne)
		if m :
			if (pos != ""):
				affiche(pos,sens,typ,trans,foutprot) # à chaque nouveau CDS aa, on affiche le précédent
				trans=""
			liste = m.groups()
			typ = liste[0]
			if (liste[0] == "tRNA"): # on ne récupère pas les séquences de tRNA ici
				protid = "NULL"
			if (liste[1] == "complement") : # récupération du sens 
				sens = 1 # indirect
			else :
				sens = 0 # direct
			pos = liste[3:5] # récupération des positions
			lpos.append(pos) # stockage des positions dans liste lpos
		m = re.match("FT\s+(\/translation=\")*([A-Z]+)(\")*$",ligne)
		if m : # récupération seq prot (en aa) dans variable trans
			liste = m.groups()
			trans += liste[1]
		m = re.match("FT\s+\/protein_id=\"([a-zA-Z0-9\.]+)",ligne)
		if m : # récupération identifiant prot
			liste = m.groups()
			protid = liste[0]
		if re.match("\s+",ligne): # si la ligne commence par des blancs, on est dans la séquence nucléique
			maliste=ligne.split()
			seq += "".join(maliste[0:-1]) # concaténation sequence nuc
		if tem==1:
			L = ligne.split()
			ch = "".join(L[:-1])
			seqnuc+=ch
		if re.match("SQ\s+",ligne): # variable témoin nouvelle séquence (gestion multifichier)
			seqnuc="" # vide la chaine de stockage de la séquence nuc
			tem=1		
		ligne = of.readline()
	of.close()
	affiche(pos,sens,typ,trans,foutprot) # affichage du dernier CDS aa
	affiche_nuc(lpos,seqnuc,foutnuc) # affichage de tous les CDS nuc
	foutprot.close()
	foutnuc.close()

####################################################################################
###############################       Code principal    ############################
####################################################################################

# Vous devez mettre les chemins de vos propres fichiers .dat  
files =['/Users/sophiepasek/Documents/Enseignt_20_21/MU4BM748/TP2/AE009952_GR.dat','/Users/sophiepasek/Documents/Enseignt_20_21/MU4BM748/TP2/AY129337_GR.dat','/Users/sophiepasek/Documents/Enseignt_20_21/MU4BM748/TP2/AL009126_GR.dat']
#files =["/Users/sophiepasek/Documents/Enseignt_20_21/MU4BM748/TP2/AE009952_GR.dat"]

for nomF in files :
	print("Traitement du fichier",nomF)
	print("Création",nomF[:-4]+".aa")
	print("Création",nomF[:-4]+".nuc")
	extract_from(nomF)

	
