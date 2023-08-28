# -*- coding:utf-8 -*-

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Rectangle:
	#ang: objet de type Point, coord. coin inf. gauche
	def __init__(self, ang, lar, hau):
		self.ang = ang
		self.lar = lar
		self.hau = hau
	def trouve_centre(self):
		xc = self.ang.x + self.lar/2
		yc = self.ang.y + self.hau/2
		return Point(xc,yc)
	def surface(self):
		return self.lar*self.hau

class Carre(Rectangle):
	def __init__(self, coin, cote):
		Rectangle.__init__(self, coin, cote, cote)


## 3 exemples d'instanciation et utilisation

# exemple 1
p = Point(0,2)
print ("Coordonnées du point (0,2) : x =", p.x, "; y =", p.y)

# exemple 2
r = Rectangle(p,10,5)
cen = r.trouve_centre()
print ("Coordonnées du centre du rectangle (angle inf. gauche (0,2), largeur 10 et hauteur 5) : x =", cen.x, "; y =", cen.y)

# exemple 3
c = Carre(Point(0,0),10)
print ("Surface du carré (angle inf. gauche (0,0) et côté 10) =", c.surface())
centre = c.trouve_centre()
print ("Coordonnées du centre de ce carré : x =", centre.x, "; y =", centre.y)
