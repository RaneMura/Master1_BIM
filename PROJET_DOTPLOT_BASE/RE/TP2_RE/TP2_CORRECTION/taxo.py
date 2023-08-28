import re 

###########################################################################
############    fonctions                ##################################
###########################################################################

# fonction de remplacement, remplace ch1 par ch2
def remplace(fictaxo,ch1,ch2):
	fop = open(fictaxo,'r')
	for line in fop:
		print(re.sub(ch1,ch2,line.rstrip('\n')))
	fop.close()

# fonction de suppression de ligne de taxonomie ch1
def supprime(fictaxo,ch1):
	fop = open(fictaxo,'r')
	for line in fop:
		tmp=line.split()
		if tmp[1] != ch1+";":
			print(line.rstrip('\n'))
	fop.close()
	
###########################################################################
############    code principal           ##################################
###########################################################################

MonficTaxo = './Taxonomy.liste'
#remplace(MonficTaxo,'[Bb]acteria',"BACTERIA")
supprime(MonficTaxo,'Bacteria')
#supprime(MonficTaxo,'Eukaryota')