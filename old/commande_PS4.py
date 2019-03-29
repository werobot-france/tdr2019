#version du proramme pour la manette PS4 filaire ou non filaire

#importation du fichier des initialisations
from initialisations_PS4 import* #importer tout (libraries, initialisations, fonctions)

#CONSTANTES et VARIABLES
#canaux de la manette PS4
#button
BCR = 0     #button bouton croix
BCE = 1     #button bouton cercle
BTR = 2     #button bouton trianble
BCA = 3     #button bouton carré
BL1 = 4     #button bouton L1 gauche
BR1 = 5     #button bouton R1 droit
BL2 = 6     #button bouton L2 gauche - avec axis
BR2 = 7     #button bouton R2 droit - avec axis
BSH = 8     #button bouton SHARE
BOP = 9     #button bouton OPTIONS
BPS = 10    #button bouton PS4
BSG = 11    #button bouton stick gauche
BSD = 12    #button bouton stick droit
BPT = 13    #button bouton pavet tactile

#axis
AGX = 0     #axis stick gauche axe des x
AGY = 1     #axis stick gauche axe des y
AL2 = 2     #axis du bouton L2 g - acceleration
ADX = 3     #axis stick droit axe des x
ADY = 4     #axis stick droit axe des x
AR2 = 5     #axis du bouton R2 droit - acceleration

#hat
HAT = 0     #hat croix directionnelle

werobot = 1 #break quand continuer égal 0
VT = 25     #vitesse minimum
vt = VT     #initialisation de la variable vt à la vitaesse minimum
S = 0       #seuil stick - si zéro pas de seuil

#FONCTIONS
def axesZero(seuil) :
    return abs(adx)<=seuil and abs(ady)<=seuil and abs(agx)<=seuil and abs(agy)<=seuil and (abs(al2+1)<=seuil or abs(al2)<=seuil) and (abs(ar2+1)<=seuil or abs(ar2)<=seuil)

#PROGRAMME
ar()

while werobot:
    for event in pygame.event.get():
        print("event = ",event)
        if event.type == pygame.JOYBUTTONDOWN and event.button == BSH: #bouton SHARE
            werobot = 0 #sortie du programme
        #if event.type == pygame.JOYAXISMOTION :#or event.type == pygame.JOYHATMOTION:
        elif event.type == pygame.JOYBUTTONDOWN and event.button == BTR: #bouton TRIANGLE
            baseGoto(baseMilieu,v = 70)
        elif event.type == pygame.JOYBUTTONDOWN and event.button == BCE: #bouton CERCLE
            if monRobot.m3.present_position < 10 : # La pince est au niveau du grd distributeur
                baseGoto(baseGdistriM,v = 70)
            else : # La pince est au niveau du sol
                baseGoto(baseMilieu, v = 70)
            time.sleep(1)
            baseGoto(baseHautDroit, v = 70)
        elif event.type == pygame.JOYBUTTONDOWN and event.button == BCA: #bouton CARRE
            if monRobot.m3.present_position < 10 : # La pince est au niveau du grd distributeur
                baseGoto(baseGdistriM,v = 70)
            else : # La pince est au niveau du sol
                baseGoto(baseMilieu, v = 70)
            time.sleep(1)
            baseGoto(baseHautGauche, v = 70)
        elif event.type == pygame.JOYBUTTONDOWN and event.button == BCR: #bouton CROIX
            baseGoto(baseBas, v = 70)
        elif event.type == pygame.JOYBUTTONDOWN and event.button == BL1: #bouton L1
            baseGoto(baseGdistri, v = 70)
        elif event.type == pygame.JOYBUTTONDOWN and event.button == BR1: #bouton R1
            if isClawOpen:
                pinceGoto(pinceFermee, v = 70)
            else :
                pinceGoto(pinceOuverte, v = 70)
            isClawOpen = not isClawOpen
        elif event.type == pygame.JOYBUTTONDOWN and event.button == BSG: #bouton Stick Gauche
            baseGoto(baseGold, v = 70)

        agx = mon_joystick.get_axis(AGX)
        agy = -mon_joystick.get_axis(AGY)
        adx = mon_joystick.get_axis(ADX)
        ady = -mon_joystick.get_axis(ADY)
        hat = mon_joystick.get_hat(HAT)
        al2 = mon_joystick.get_axis(AL2) #accélération
        ar2 = mon_joystick.get_axis(AR2) #accélération
        if axesZero(S):
            ar()
        else:
            if al2 == -1:
                vt = VT
            elif al2 != 0 :
                vt = mappyt(al2,-1,1,0,1) * 100
                print("al2 = {0} et vt = {1}".format(al2,vt))
            if ady < 0.5 * adx and ady >= -0.5 * adx:
                te(vt)
            if ady > 0.5 * adx and ady <= 2 * adx:
                tne(vt)
            if ady > 2 * adx and ady >= -2 * adx:
                print("ordre recu !")
                tn(vt)
            if ady < -2* adx and ady >= -0.5 * adx:
                tno(vt)
            if ady < -0.5 * adx and ady >= 0.5 * adx:
                to(vt)
            if ady < 0.5 * adx and ady >= 2 * adx:
                tso(vt)
            if ady < 2 * adx and ady <= -2 * adx:
                ts(vt)
            if ady > -2 * adx and ady <= -0.5 * adx:
                tse(vt)
            if hat[0] == -1 :
                rah(vt)
            if hat[0] == 1 :
                rh(vt)
            if hat[1] == 1 : # serre un peu plus la pince
                bougePince(1)
            if hat[1] == -1 : #desserre un peu la pince
                bougePince(-1)
                #~ if abs(ady) <= S and abs(adx) <= S and abs(hat[0]) <= 0 :
                    #~ ar()
            #~ if hat[0] == -1:
                #~ rah(vt)
            #~ if hat[0] == 1 :
                #~ rh(vt)
            #~ pygame.event.clear() #vide la queue - annule plusieurs appuis sur A vert
esc_zero()
monRobot.close()
print ("")
print ("fin du programme")
