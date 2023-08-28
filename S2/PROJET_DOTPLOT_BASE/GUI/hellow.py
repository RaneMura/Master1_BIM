import tkinter as tk

class HelloWorld():
	def __init__(self):
		self.fenetre =tk.Tk()
		self.w = tk.Label(self.fenetre, text="Hello, MU4BM748 world !")
		self.w.pack()
		self.fenetre.mainloop()

hello = HelloWorld()
