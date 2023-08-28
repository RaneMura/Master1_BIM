import tkinter as tk

class Dessin():
	def __init__(self):
		self._fenetre = tk.Tk()
		self._fenetre.title('Dessin')
		
		self._tableau = tk.Canvas(self._fenetre,width=600,height=400,bg='blue')
		self._tableau.pack(padx=10,pady=10)
		
		self._rond = self._tableau.create_oval(250,150,350,250,fill='yellow')
		
		self._boutonG=tk.Button(self._fenetre,text='<',command=self.gauche)
		self._boutonG.pack(side=tk.LEFT)

		self._boutonD=tk.Button(self._fenetre,text='>',command=self.droite)
		self._boutonD.pack(side=tk.RIGHT)		
		
		self._fenetre.mainloop()
	
	def gauche(self):
		(x1,y1,x2,y2) = self._tableau.coords(self._rond)
		if x1 > 20:
			x1 -= 20
			x2 -= 20
		self._tableau.coords(self._rond,x1,y1,x2,y2)
			
	def droite(self):
		(x1,y1,x2,y2) = self._tableau.coords(self._rond)
		if x2 < 580:
			x1 += 20
			x2 += 20
		self._tableau.coords(self._rond,x1,y1,x2,y2)	
		
oeuvre = Dessin()
