import tkinter as tk

class Boutons1():
	def __init__(self):
		self.fenetre =tk.Tk()
		self.fenetre.title(':-) 1')
		self.boutG = tk.Button(self.fenetre,text = "Gauche")
		self.boutD = tk.Button(self.fenetre,text = "Droite")
		self.boutH = tk.Button(self.fenetre,text = "Haut")
		self.boutB = tk.Button(self.fenetre,text = "Bas")
		self.boutH.pack(side = tk.TOP)
		self.boutB.pack(side = tk.BOTTOM)
		self.boutG.pack(side = tk.LEFT)
		self.boutD.pack(side = tk.RIGHT)
		self.fenetre.mainloop()

class Boutons2():
	def __init__(self):
		self.fenetre =tk.Tk()
		self.fenetre.title(':-) 2')
		self.boutG = tk.Button(self.fenetre,text = "Gauche")
		self.boutD = tk.Button(self.fenetre,text = "Droite")
		self.boutH = tk.Button(self.fenetre,text = "Haut")
		self.boutB = tk.Button(self.fenetre,text = "Bas")

		self.boutG.pack(side = tk.LEFT)
		self.boutD.pack(side = tk.RIGHT)
		self.boutH.pack(side = tk.TOP)
		self.boutB.pack(side = tk.BOTTOM)


		self.fenetre.mainloop()

b1 = Boutons1()
b2 = Boutons2()
