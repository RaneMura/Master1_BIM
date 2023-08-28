import math
import tkinter as tk
from tkinter import filedialog as fd

class Motifs():

	compl = {'A':'T', 'C':'G', 'G':'C', 'T':'A'}

	def __init__(self):

		self.fichseq = ''
		self.fichpos = ''
		self.dicseq = {}
		self.seqnuc = ''
		self.seqnam = ''
		self.revcmp = ''
		self.motif = ''
		self.posmot = []
		self.creeInterface()
		self.fenetre.mainloop()

	def creeInterface(self):
		
		self.fenetre = tk.Tk()
		self.fenetre.title('Motifs')

		# Barre de menus
		self.barre = tk.Menu(self.fenetre)
		# Menu "Fichier"
		self.filemenu = tk.Menu(self.barre,tearoff=0)
		self.filemenu.add_command(label='Ouvrir...',	  command=self.ouvrir)
		self.filemenu.add_command(label='Sauvegarder...', command=self.sauver)
		self.barre.add_cascade(label='Fichier', menu=self.filemenu)
		self.fenetre.config(menu=self.barre)
		
		# zone pour associer la Listbox et sa Scrollbar
		self.zoneL = tk.Frame(self.fenetre)
		
		# Liste déroulante
		self.liseq = tk.Variable(value=list(self.dicseq.keys()))
		self.listbox = tk.Listbox(self.zoneL,listvariable=self.liseq,
		          height=8, width=20, selectmode=tk.SINGLE)
		self.listbox.bind('<<ListboxSelect>>', self.setseq)
		self.listbox.pack(side=tk.LEFT, fill="y")
		
		# Ascenseur
		self.scroll = tk.Scrollbar(self.zoneL, orient="vertical")
		self.scroll.config(command=self.listbox.yview)
		self.listbox.config(yscrollcommand=self.scroll.set)
		self.scroll.pack(side=tk.RIGHT, fill="y")

		# Boîte de saisie du motif
		self.labmot = tk.Label(self.fenetre,text='Motif :')
		self.txtmot = tk.Entry(self.fenetre)
		
		# Case à cocher : Inverse-complémentaire
		self.revseq = tk.BooleanVar(value=False)
		self.okrcmp = tk.Checkbutton(self.fenetre,
		             text='Inverse-complémentaire',
		             variable=self.revseq, offvalue=False, onvalue=True)
		
		# Bouton pour lancer la recherche
		self.lancer = tk.Button(self.fenetre,
					 text='Chercher', command=self.cherche)
		
		# Affichage du nombre de motifs trouvés
		self.cptmot = tk.Label(self.fenetre,text='--')
		
		self.zoneL.pack(side=tk.LEFT)
		self.okrcmp.pack(side=tk.TOP)
		self.lancer.pack(side=tk.BOTTOM)
		self.cptmot.pack(side=tk.BOTTOM)
		self.labmot.pack(side=tk.LEFT)
		self.txtmot.pack(side=tk.RIGHT)
	
	def setseq(self,_):
		
		self.seqnuc == ''
		self.revcmp == ''
		cursel = self.listbox.curselection()
		if len(cursel) > 0 and cursel[0] < len(self.liseq): 
			self.seqnam = self.liseq[self.listbox.curselection()[0]]
		self.posmot = []
		self.cptmot.config(text = '--')
		self.fichpos = ''

	def ouvrir(self):
		
		#self.fenetre.withdraw()             # Cache la fenêtre principale
		self.fichseq = fd.askopenfilename(   # Menu de choix de fichier
		                 title="Séquence")
		#self.fenetre.deiconify()            # Coucou, la revoilà !
		if len(self.fichseq) > 0:
			self.readseq()

	def sauver(self):
		
		#self.fenetre.withdraw()             # Cache la fenêtre principale
		self.fichpos = fd.asksaveasfilename( # Menu de choix de fichier
		               title="Sauvegarde",
		               initialfile=self.motfile)
		#self.fenetre.deiconify()            # Coucou, la revoilà !
		flxpos = open(self.fichpos, 'w')
		for pos in self.posmot:
			(b,e) = pos
			flxpos.write('{:d}\t{:d}\n'.format(b,e))
		flxpos.close()

	def complinv(self):
		
		self.revcmp = ''
		for nuc in self.seqnuc:
			self.revcmp = Motifs.compl[nuc] + self.revcmp

	def readseq(self):
		if len(self.fichseq) == 0:
			return
		self.dicseq = {}
		flxseq = open(self.fichseq,'r')
		nam = None
		nuc = ''
		for lin in flxseq:
			if lin[0] == '>':
				if nam is not None:
					self.dicseq[nam] = nuc.upper()
				nam = lin[1:].replace('\n','')
				nuc = ''
			else:
				nuc += lin.replace('\n','')
		if nam is not None:
			self.dicseq[nam] = nuc.upper()
		flxseq.close()
		
		# Mise à jour de la liste des séquences
		self.listbox.delete(0,tk.END)
		self.liseq = list(self.dicseq.keys())
		for nam in self.liseq:
			self.listbox.insert(tk.END, nam)

	def cherche(self):
				
		if self.seqnam is not None and self.seqnam in self.dicseq:
			self.seqnuc = self.dicseq[self.seqnam]
		else:
			return
		
		self.motif = self.txtmot.get().upper()
		if len(self.motif) < 1:
			return
		
		self.posmot = []
		self.trouve()
		if self.revseq.get():
			self.trouve(rev=True)
		self.cptmot.config(text = '- {:d} -'.format(len(self.posmot)))
		if len(self.posmot) > 0:
			self.motfile = self.seqnam+'_'+self.motif+'.tsv'

		# Fenêtre pop-up
		if len(self.posmot) > 0:
			# Calcul du nombre max de chiffres (pour le format)
			pmax = 0
			for pos in self.posmot:
				(deb,fin) = pos
				if deb > pmax:
					pmax = deb
				if fin > pmax : 
					pmax = fin
			ndigits = int(math.log10(pmax)+1)
	
			# Création du contenu de la fenêtre pop-up, comme une chaîne
			listocc = self.motif+' in '+self.seqnam+'\n'
			for pos in self.posmot:
				(deb,fin) = pos
				listocc += '{1:{0}d} - {2:{0}d}\n'.format(ndigits,deb,fin)
			tk.messagebox.showinfo("Résultat",listocc)

	def trouve(self,rev=False):

		if rev:
			self.complinv()
			seq = self.revcmp
		else:
			seq = self.seqnuc

		# print(seq[:10],'...',seq[-10:],':',len(seq))
		lmot = len(self.motif)
		lseq = len(seq)
		for pos in range(lseq-lmot):
			if seq[pos:pos+lmot] == self.motif:
				if rev:
					self.posmot.append((lseq-pos,lseq-pos-lmot+1))
				else:
					self.posmot.append((pos+1,pos+lmot))
		
graphmot = Motifs()
