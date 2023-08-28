import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

class Find():

	def __init__(self):
		self.name = 'inconnu'
		self.creeInterface()
		#self.dataSeq = dict()
		 	
		
	def creeInterface(self):
		self.liste = list()
		self.combo = ["Aucun"]
		self.fichier=''
		
		self.dataSeq = dict()
		
		self.fenetre = tk.Tk()
		self.fenetre.title('Motifs')
		
		self.barre = tk.Menu(self.fenetre)

		
		self.filemenu = tk.Menu(self.barre,tearoff=0)
		self.filemenu.add_command(label="Ouvrir ..",command = self.ouvrir)
		self.filemenu.add_command(label="Sauver sous forme tsv ...",command = self.sauver)
		self.filemenu.add_command(label="Fichier",command = self.filemenu)

		self.barre.add_cascade(label="Fichier", menu=self.filemenu)
		self.combox = ttk.Combobox(self.fenetre,values = self.combo)
		self.fenetre.config(menu=self.barre)
		self.combox.pack()
		
		
		self.PanH = tk.PanedWindow(self.fenetre)
		self.txt = tk.Label(self.PanH, text='Motif :')
		self.txt.pack(side=tk.LEFT)
		self.zt = tk.Entry(self.PanH)
		self.zt.pack(side=tk.RIGHT)
		
		self.bf = tk.Button(self.fenetre, text = 'Chercher', command = self.recherche)
		
		self.icval = tk.IntVar(value = 0)
		self.ic = tk.Checkbutton(self.fenetre,text = 'Inverse-complémentaire', variable=self.icval, offvalue=0, onvalue=1)
		self.PanH.pack(side = tk.TOP)
		self.ic.pack(side =tk.BOTTOM)
		self.bf.pack()
		
		self.fenetre.mainloop()
	
	def readFasta(self):
		
		infile = open(self.fichier,'r')
		seq = ''
		ident=''
		for line in infile :
			if line[0]=='>':
				if len(seq)>0:
					self.combo.append(ident)
					self.dataSeq[ident]= seq
				ident = line[1:-1]
				seq = ''
			else :
				seq+=line[:-1]
		self.dataSeq[ident]=seq

	def ouvrir(self):
		self.fenetre.withdraw()
		self.fichier = fd.askopenfilename()
		self.fenetre.deiconify()
		
		self.dataSeq = self.readFasta
		print(self.dataSeq)
		
	def sauver(self):
	
		self.fenetre.withdraw()
		self.fichier = fd.asksaveasfile(initialfile = 'Untitled.tsv',defaultextension=".tsv",filetypes=[("All Files","*.*"),("Text Documents","*.tsv")])
		self.fenetre.deiconify()

		with open(self.fichier, "w") as f:
			for i in range(len(self.liste)):
				name,pos1,pos2=self.liste[i]
				string = str(name)+" : "+str(pos1)+"	-	"+str(pos2)+"\n" 
				f.write(string)
		f.close()
		
		
	def recherche(self):
		self.name = self.zt.get()
		
		L = len(self.name)
		for i in self.dataSeq:
			for j in range(len(self.dataSeq[i])-L+1):
				if self.dataSeq[i][j:j+L]==self.name:
					self.liste.append((i,j,j+L-1))
					print(i+" : ",j,"	-	",j+L-1)
		if self.icval.get() == 1:
			for i in self.dataSeq:
				rev = self.reverse(self.dataSeq[i])
				for j in range(len(rev)-L+1):
					if rev[j:j+L]==self.name:
						self.liste.append((i,len(rev)-j,len(rev)-j-L-1))
						print(i+" : ",len(rev)-j,"	-	",len(rev)-j-L+1)
	
	
	def reverse(self,chaine):
		revchain = chaine[::-1]
		seq = ''
		diconucl = {'A':'T','T':'A','G':'C','C':'G'}
		for i in range(len(revchain)):
			seq+=diconucl[revchain[i]]
		
		return seq 
		
test = Find()
