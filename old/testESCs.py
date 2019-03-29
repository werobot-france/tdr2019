#version du proramme pour la manette PS4 filaire ou non filaire
from __future__ import division
HZ = 50     #fréquence du signal vers les ESC
ESC_BRAS = 2 
SERVO_PISTON_G = 3
SERVO_PISTON_D = 4
# variable contenant la position en degré des pistons
pd_pos = 500
pd_init = 500
pd_bloc = 275
pd_pouss = 230
pg_pos = 100
pg_init = 100
pg_bloc = 325
pg_pouss = 365
LESC = (6,5,0,1) #liste des ESC (avant gauche, avant droit, arrière gauche, arrière droit)

import Adafruit_PCA9685, time, pygame, sys

#initialiser le PCA9685 Ã  l'adresse par défaut 0x40
servo=Adafruit_PCA9685.PCA9685()

#définir la fréquence du signal de sortie à 50hz
servo.set_pwm_freq(HZ)

#procédure d'initialisation d'un ESC
def ini_esc(slot):
    servo.set_pwm(slot,0,307) #307 est le signal neutre sous 50 Hz (1.5 / 20 x 4096 = 307)
    time.sleep(1)

def initialiser_esc():
    ini_esc(LESC[0]) #initialiser l'ESC roue avant gauche slot 0
    ini_esc(LESC[1]) #initialiser l'ESC roue avant droite slot 1
    ini_esc(LESC[2]) #initialiser l'ESC roue arrière gauche slot 14
    ini_esc(LESC[3]) #initialiser l'ESC roue arrière droite slot 15
    ini_esc(ESC_BRAS) #initialiser l'ESC base du bras slot ESC_BRAS

def init_servos():
    servo.set_pwm(SERVO_PISTON_D,0,pd_ini)
    servo.set_pwm(SERVO_PISTON_G,0,pg_ini)

#équivalent de la fonction map() de arduino
def mappyt(x, in_min, in_max, out_min, out_max):
    return (x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min

#fonction esc pour une vitesse de moteur de -100 à 100()
def esc(v):
    return round(mappyt(v,0,100,307,410))

#translation nord (avance)
def tn(vit):
    a = esc(vit)
    servo.set_pwm(LESC[0],0,a) #canal 0 : roue avant gauche
    servo.set_pwm(LESC[1],0,a) #canal 1 : roue avant droite
    servo.set_pwm(LESC[2],0,a) #canal 14 : roue arrière gauche
    servo.set_pwm(LESC[3],0,a) #canal 15 : roue arrière droite

#translation sud (recule)
def ts(vit):
    tn(-vit)

#translation est (droite)
def te(vit):
    a = esc(vit)
    r = esc(-vit)
    servo.set_pwm(LESC[0],0,a) #roue avant gauche
    servo.set_pwm(LESC[1],0,r) #roue avant droite
    servo.set_pwm(LESC[2],0,r) #roue arrière gauche
    servo.set_pwm(LESC[3],0,a) #roue arrière droit

#translation ouest (gauche)
def to(vit):
    te(-vit)

#rotation horaire
def rh(vit):
    a = esc(vit)
    r = esc(-vit)
    servo.set_pwm(LESC[0],0,a) #roue avant gauche
    servo.set_pwm(LESC[1],0,r) #roue avant droite
    servo.set_pwm(LESC[2],0,a) #roue arrière gauche
    servo.set_pwm(LESC[3],0,r) #roue arrière droite

# rotation anti horaire
def rah(vit):
    rh(-vit)

# translation nord est
def tne(vit):
    a = esc(vit)
    s = esc(0)
    servo.set_pwm(LESC[0],0,a) #roue avant gauche
    servo.set_pwm(LESC[1],0,s) #roue avant droite
    servo.set_pwm(LESC[2],0,s) #roue arrière gauche
    servo.set_pwm(LESC[3],0,a) #roue arrière droite

#translation sud ouest
def tso(vit):
    tne (-vit)

#translation nord ouest
def tno(vit):
    a = esc(vit)
    s = esc(0)
    servo.set_pwm(LESC[0],0,s) #roue avant gauche
    servo.set_pwm(LESC[1],0,a) #roue avant droit
    servo.set_pwm(LESC[2],0,a) #roue arrière gauche
    servo.set_pwm(LESC[3],0,s) #roue arrière droit

#translation sud est
def tse(vit):
    tno(-vit)

#leve le bras:
def lb(vit):
    a = esc(-vit)
    servo.set_pwm(ESC_BRAS,0,a)

#baisse bras:
def bb(vit):
    lb(-vit)

#arrêt du robot
def ar():
    a = esc(0)
    servo.set_pwm(LESC[0],0,a)
    servo.set_pwm(LESC[1],0,a)
    servo.set_pwm(LESC[2],0,a)
    servo.set_pwm(LESC[3],0,a)
    servo.set_pwm(ESC_BRAS,0,a) #arrêt base bras
    #servo.set_pwm(SERVO_PISTON_G,0,a) 
    #servo.set_pwm(SERVO_PISTON_D,0,a) 

#zéro signal vers les ESC
def esc_zero():
    a=4096
    servo.set_pwm(LESC[0],0,a)
    servo.set_pwm(LESC[1],0,a)
    servo.set_pwm(LESC[2],0,a)
    servo.set_pwm(LESC[3],0,a)
    servo.set_pwm(ESC_BRAS,0,a)

def vitesse (vit):
    return round(mappyt(vit,0,1,307,410))



def pistonGauche():
    global pg_pos, pg_init, pg_pouss, SERVO_PISTON_G
    if pg_pos == pg_init:
        pg_pos = pg_pouss
    else:
        pg_pos = pg_init
    servo.set_pwm(SERVO_PISTON_G,0,pg_pos)

def pistonDroit():
    global pd_pos, pd_init, pd_pouss, SERVO_PISTON_D
    if pd_pos == pd_init:
        pd_pos = pd_pouss
    else:
        pd_pos = pd_init
    servo.set_pwm(SERVO_PISTON_D,0,pd_pos)


#####################################################################
#                                                                   #
#          INITIALISATION ET FONCTIONS BRAS                         #
#                                                                   #
#####################################################################


import pypot.dynamixel
import time
import pypot.robot

# Procédure intermédiaire pour récupérer le contrôle du bras en cas de fail


#Pour obtenir une liste de ports
ports = pypot.dynamixel.get_available_ports()
moteurs = pypot.dynamixel.DxlIO(ports[0])
IDs = moteurs.scan(range(10))

for a in IDs:
    print(moteurs.get_present_position((a,)))
    moteurs.set_moving_speed({a:30})

moteurs.close()

# Dictionnaire contenant la description de notre bras

robot_config = {
    'controllers': {
        'my_dxl_controller': {
            'sync_read': False,
            'attached_motors': ['base', 'pince'],
            'port': '/dev/ttyUSB0'
        }
    },
    'motorgroups': {
        'base': ['m2', 'm3'],
        'pince': ['m4', 'm5']
    },
    'motors': {
        'm2': {
           'orientation': 'direct',
            'type': 'AX-12',
            'id': 6,
            'angle_limit': [-150.0, 150.0],
            'offset': 0.0
        },
        'm3': {
            'orientation': 'indirect',
            'type': 'AX-12',
            'id': 3,
            'angle_limit': [-150.0, 150.0],
            'offset': 0.0
        }
            ,
        'm4': {
            'orientation': 'direct',
            'type': 'AX-12',
            'id': 4,
            'angle_limit': [0.0, 150.0],
            'offset': 0.0
        },
        'm5': {
            'orientation': 'indirect',
            'type': 'AX-12',
            'id': 5,
            'angle_limit': [-150.0, 0.0],
            'offset': 0.0
        }
    }
}

monRobot = pypot.robot.from_config(robot_config)

#Fonction de déplacement de la base du bras
def baseGoto(L,v=30,wait = False):
    n = len(monRobot.base)
    if len(L) == n:
        posBase.put(L[0],block=False)
        if not wait :            
            for i in range(1,n) :
                monRobot.base[i].moving_speed = v
                monRobot.base[i].goal_position = L[i]
        else:
            for i in range(1,n):
                delta = abs(monRobot.base[i].present_position - L[i])
                duration = delta / v
                monRobot.base[i].goto_position(L[i],duration,wait=True)
    else:
        print("ERREUR : il y a {} moteurs et la liste contient {} valeurs".format(n,len(L)))

#Fonction de déplacement de la pince
def pinceGoto(L,v=30,wait = False):
    n = len(monRobot.pince)
    if len(L) == n:
        if not wait :
            for i in range(n) :
                monRobot.pince[i].moving_speed = v
                monRobot.pince[i].goal_position = L[i]
        else:
            for i in range(n):
                delta = abs(monRobot.pince[i].present_position - L[i])
                duration = delta / v
                monRobot.pince[i].goto_position(L[i],duration,wait=True)
    else:
        print("ERREUR : il y a {} moteurs et la liste contient {} valeurs".format(n,len(L)))

def bougePince(val):
    for m in monRobot.pince :
        m.moving_speed = 30
        m.goal_position = m.present_position + val

baseMilieu = [-2,102]  # position de repos basse
baseHaut = [0,0,0] # position verticale - inutile ?
baseBas = [-1,10] # position basse
baseGdistri = [2,-29] # position pour attraper les palets dans le grd distributeur
baseGdistriM = [-50,2,52] # position intermédiaire après saisie sur le grd distributeur
baseHautDroit = [-60,-27] # position pour dépôt goulotte droite A COMPLETER
baseHautGauche = [65,-22] # position pour dépôt goulotte gauche A COMPLETER
baseGold = [0,0,0] # position pour pousser le Goldenium et pour l'accelérateur de particule A COMPLETER

pinceOuverte = [85,85]
pinceFermee = [100,100]

monRobot.power_up()

pinceGoto(pinceOuverte, v = 70)
isClawOpen = True

