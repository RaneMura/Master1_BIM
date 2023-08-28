import tkinter as tk 
from tkinter import filedialog as fd

class Menu():
	def __init__(self):
		self.fichier =''
		self.fenetre = tk.Tk()
		self.barre = tk.Menu(self.fenetre)
		
		self.filemenu = tk.Menu(self.barre,tearoff=0)
		self.filemenu.add_command(label="New",command = self.rien)
		self.filemenu.add_command(label="Open..",command = self.ouvrir)
		self.filemenu.add_command(label="Save",command = self.rien)
		self.filemenu.add_command(label="File",command = self.filemenu)

		self.barre.add_cascade(label="File", menu=self.filemenu)
		self.fenetre.config(menu=self.barre)
		self.fenetre.mainloop()
		
	def rien(self):
		print("OK")
		
	def ouvrir(self):
		self.fenetre.withdraw()
		self.fichier = fd.askopenfilename()
		self.fenetre.deiconify()
		print(self.fichier)
		
hello = Menu()
