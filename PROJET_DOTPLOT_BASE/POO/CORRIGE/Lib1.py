# -*- coding:utf-8 -*-

import math

class Cercle:
	def __init__(self,rayon):
		self.rayon=rayon
	def surface(self):
		surf=math.pi*self.rayon*self.rayon
		return surf

class Cylindre(Cercle):
	def __init__(self,rayon,hauteur):
		Cercle.__init__(self,rayon)
		self.hauteur=hauteur
	def volume_cyl(self):
		vol=self.surface()*self.hauteur
		return vol

class Cone(Cylindre):
	def __init__(self,rayon,hauteur):
		Cylindre.__init__(self,rayon,hauteur)
	def volume_cone(self):
		vol=self.volume_cyl()/3
		return vol
