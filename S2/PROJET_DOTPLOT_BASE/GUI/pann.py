import tkinter as tk

class pann():
	def __init__(self):
		self.fenetre = tk.Tk()
		self.fenetre.title('Test Panel')
		
		self.PanG = tk.PanedWindow(self.fenetre)
		self.boutNW = tk.Button(self.PanG,text = "NW")
		self.boutNW.pack(side=tk.TOP)
		self.boutSW = tk.Button(self.PanG,text = "SW")
		self.boutSW.pack(side=tk.BOTTOM)
		
		self.PanD = tk.PanedWindow(self.fenetre)
		self.boutNE = tk.Button(self.PanD,text = "NE")
		self.boutNE.pack(side=tk.TOP)
		self.boutSE = tk.Button(self.PanD,text = "SE")
		self.boutSE.pack(side=tk.BOTTOM)
		
		self.PanG.pack(side = tk.LEFT)
		self.PanD.pack(side = tk.RIGHT)
		self.fenetre.mainloop()
		
p = pann()
