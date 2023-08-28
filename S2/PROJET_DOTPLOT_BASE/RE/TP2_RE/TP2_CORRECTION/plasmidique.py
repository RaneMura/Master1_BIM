import re 

###########################################################################
############    fonctions                ##################################
###########################################################################

# fonction qui compte les effectifs pour chaque banque
# cette fonction est indépendante du nbre et du nom des banques
def effbanque(ficfasta):
	dicoeff={}
	fop = open(ficfasta,'r')
	for line in fop:
		if line[0]=='>':
			tmp = line.split()
			bk = testbanque(tmp[0])
			if bk in dicoeff:
				dicoeff[bk]=dicoeff[bk]+1
			else:
				dicoeff[bk]=1
	fop.close()
	return dicoeff

# fonction qui teste l'appartenance à une banque	
def testbanque(ch):
	moplasmid = re.search(':',ch)
	moother = re.search('|',ch)
	#print(ch,ch[1:8])
	if moplasmid: # banque plasmid_db
		return ch[9:16]+"_db"
	elif moother:
		#print(ch,ch[1:8])
		if ch[1:8] == "uniprot" : # banque uniprot
			return ch[1:8]
		else: # banque sp ou tr
			return ch[1:3]
	
# fonction de formatage de la sortie
def ecritsortie(dico,ficsortie):
	fw = open(ficsortie,'w')
	fw.write("#Banque\teffectif\n")
	for i in dico:
		fw.write(i+'\t'+str(dico[i])+'\n')
	fw.close()


###########################################################################
############    code principal           ##################################
###########################################################################

Monficfasta = './PLCplasmidiques.fasta'
Monficsortie = 'effBanque.txt'
dicoeffbk = effbanque(Monficfasta)
ecritsortie(dicoeffbk, Monficsortie)

