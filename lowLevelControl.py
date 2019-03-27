import pypot.dynamixel
import time
import threading
import pypot.robot

# Procédure intermédiaire pour récupérer le contrôle du bras en cas de fail


#Pour obtenir une liste de ports
ports = pypot.dynamixel.get_available_ports()
moteurs = pypot.dynamixel.DxlIO(ports[0])
IDs = moteurs.scan(range(10))

for a in IDs:
    print(moteurs.get_present_position((a,)))
    moteurs.set_moving_speed({a:30})

# position initiale : [-100,0,100,100,100]
moteurs.set_goal_position({2: 100.0})
moteurs.set_goal_position({1: 0.0})
moteurs.set_goal_position({3: -100.0})
moteurs.set_goal_position({4: 100.0})
moteurs.set_goal_position({5: -100.0})


class Rmotors:
	def __init__(self,id,orientation,lowLimAngle,highLimAngle,moteurs):
		self.id = id
		self.orientation = orientation
		self.lowLimAngle = lowLimAngle
		self.highLimAngle = highLimAngle
		self.moteurs = moteurs
		self.moteurs.set_angle_limit({self.id: (self.lowLimAngle,self.highLimAngle)})
		self.moteurs.set_angle_limit({self.id: (self.lowLimAngle,self.highLimAngle)})
		threading.Thread(target = self.checkAlarm).start()
		
	def set_speed(self,speed):
		self.moteurs.set_moving_speed({self.id: speed})
	
	def set_pos(self,pos):
		self.moteurs.set_goal_position({self.id: pos *  self.orientation})
	
	def get_pos(self):
		return self.orientation * self.moteurs.get_present_position((self.id,))[0]
	
	def checkAlarm(self):
		ok = True
		while ok:
			if self.moteurs.is_led_on((self.id,))[0]:
				#Problème sur moteur à régler
				print("pb sur moteur id = {}".format(self.id))
				print("temp ={}".format(moteurs.get_present_temperature((self.id,))))p
				print("load : {}".format(moteurs.get_present_load((self.id,))))
				print("exiting thread ...")
				ok = False
				time.sleep(0.05)

m1 = Rmotors(2,-1,-120.0,120.0,moteurs)
m2 = Rmotors(1,1,-150.0,150.0,moteurs)
m3 = Rmotors(3,-1,-150.0,150.0,moteurs)
m4 = Rmotors(4,1,0.0,150.0,moteurs)
m5 = Rmotors(5,-1,-150.0,0.0,moteurs)



base = [m1,m2,m3]
pince  = [m4,m5]

baseMilieu = [-100,0,100]  # position de repos basse
baseHaut = [0,0,0] # position verticale - inutile ?
baseBas = [-100,0,10] # position basse
baseGdistri = [-50,2,-29] # position pour attraper les palets dans le grd distributeur
baseGdistriM = [-50,2,52] # position intermédiaire après saisie sur le grd distributeur
baseHautDroit = [0,0,0] # position pour dépôt goulotte droite A COMPLETER
baseHautGauche = [0,0,0] # position pour dépôt goulotte gauche A COMPLETER
baseGold = [0,0,0] # position pour pousser le Goldenium et pour l'accelérateur de particule A COMPLETER

pinceOuverte = [85,85]
pinceFermee = [100,100]

def baseGoto(L,v=30, wait=False):
	if len(L) == 3:
		if not wait:
			for i in range(3):
				base[i].set_speed(v)
				base[i].set_pos(L[i])
		else:
			for i in range(3):
				delta = abs(L[i]-base[i].get_pos())
				duration = delta/v 
				base[i].set_speed(v)
				base[i].set_pos(L[i])
				time.sleep(duration)
	else:
		print("ERREUR : il y a {} moteurs et la liste contient {} valeurs".format(3,len(L)))
				

def pinceGoto(L,v=30, wait=False):
	if len(L) == 2:
		if not wait:
			for i in range(3):
				pince[i].set_speed(v)
				pince[i].set_pos(L[i])
		else:
			for i in range(3):
				delta = abs(L[i]-pince[i].get_pos())
				duration = delta/v 
				pince[i].set_speed(v)
				pince[i].set_pos(L[i])
				time.sleep(duration)
	else:
		print("ERREUR : il y a {} moteurs et la liste contient {} valeurs".format(2,len(L)))				

def bougePince(val):
	for m in pince:
		m.set_speed(30)
		m.set_pos(m.get_pos() + val)
		
pinceGoto(pinceOuverte, v = 70)
isClawOpen = True
		


				
