#exo1 
import math

class Cercle:
	def __init__(self,rayon):
		self.rayon = rayon

	def surface(self):
		return self.rayon*self.rayon*math.pi

class Cylindre(Cercle):
	def __init__(self,rayon,hauteur):
		super().__init__(rayon)
		self.hauteur= hauteur
	def volumeCylindre(self):
		return self.hauteur * Cercle.surface(self)

class Cone(Cylindre):
	def __init__(self,rayon,hauteur):
		super().__init__(rayon,hauteur)
	def volumeCone(self):
		return self.volumeCylindre()/3


r = 2
h = 5
c1 = Cercle(r)
cy1 = Cylindre(r,h)
co1 = Cone(r,h)
print("surface cercle = "+str(c1.surface()))
print("volume cylindre = "+str(cy1.volumeCylindre()))
print("volume cone = "+str(co1.volumeCone()))
print("volume de la base du cone = "+str(co1.surface()))
print("volume du pseudo-cylindre = "+str(co1.volumeCylindre()))

print(1/2)
