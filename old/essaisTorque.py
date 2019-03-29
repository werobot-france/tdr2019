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

# position initiale : [-100,0,100,100,100]
moteurs.set_goal_position({2: 100.0})
moteurs.set_goal_position({1: 0.0})
moteurs.set_goal_position({3: -100.0})
moteurs.set_goal_position({4: 100.0})
moteurs.set_goal_position({5: -100.0})

moteurs.close()

# Dictionnaire contenant la description de notre bras

robot_config = {
    'controllers': {
        'my_dxl_controller': {
            'sync_read': False,
            'attached_motors': ['base', 'pince'],
            'port': ports[0]
        }
    },
    'motorgroups': {
        'base': ['m1', 'm2', 'm3'],
        'pince': ['m4', 'm5']
    },
    'motors': {
        'm1': {
            'orientation': 'indirect',
            'type': 'AX-12',
            'id': 2,
            'angle_limit': [-120.0, 120.0],
            'offset': 0.0
        },
        'm2': {
           'orientation': 'direct',
            'type': 'AX-12',
            'id': 1,
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

#Définition du bras :

monRobot = pypot.robot.from_config(robot_config)

#Fonction de déplacement de la base du bras
def baseGoto(L,v=30,wait = False):
    n = len(monRobot.base)
    if len(L) == n:
        if not wait :
            for i in range(n) :
                monRobot.base[i].moving_speed = v
                monRobot.base[i].goal_position = L[i]
        else:
            for i in range(n):
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

pinceGoto(pinceOuverte, v = 70)
isClawOpen = True
