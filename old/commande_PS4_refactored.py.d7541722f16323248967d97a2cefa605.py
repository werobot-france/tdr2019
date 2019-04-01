#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
BPT = 13    #button bouton pave tactile

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

oldtimePince = 0
oldtimePdroit = 0
oldtimePgauche = 0
isBL1RePressed = True
isHatUpRepressed = True
isHatDownRepressed = True
isHatLeftRepressed = True
isHatRightRepressed = True

#FONCTIONS
def axesZero(seuil) :
    return abs(adx)<=seuil and abs(ady)<=seuil and abs(agx)<=seuil and abs(agy)<=seuil and (abs(al2+1)<=seuil or abs(al2)<=seuil) and (abs(ar2+1)<=seuil or abs(ar2)<=seuil)

#PROGRAMME
ar()

pygame.init()


#pistonDroit()
#pistonGauche()


while werobot:
    for event in pygame.event.get():
        #print("event = ",event)
##        #if event.type == pygame.JOYBUTTONDOWN:
##        if event.type == pygame.JOYBUTTONDOWN and event.button == BPS: #bouton PS4
##            werobot = 0 #sortie du programme
##        if event.type == pygame.JOYBUTTONDOWN and event.button == BTR: #bouton TRIANGLE
##            baseGoto(baseHaut,v = 70)
##        if event.type == pygame.JOYBUTTONDOWN and event.button == BCE: #bouton CERCLE
####				if monRobot.m3.present_position < 10 : # La pince est au niveau du grd distributeur
####					baseGoto(baseGdistriM,v = 70)
####				else : # La pince est au niveau du sol
####					baseGoto(baseMilieu, v = 70)
####				time.sleep(1)
##            baseGoto(baseHautDroit, v = 70)
##        if event.type == pygame.JOYBUTTONDOWN and event.button == BCA: #bouton CARRE
####				if monRobot.m3.present_position < 10 : # La pince est au niveau du grd distributeur
####					baseGoto(baseGdistriM,v = 70)
####				else : # La pince est au niveau du sol
####					baseGoto(baseMilieu, v = 70)
####				time.sleep(1)
##            baseGoto(baseHautGauche, v = 70)
##        if event.type == pygame.JOYBUTTONDOWN and event.button == BCR: #bouton CROIX
##            baseGoto(baseBas, v = 70)
####            elif event.button == BL1: #bouton L1
####                baseGoto(baseGdistri, v = 70)
##        if event.type == pygame.JOYBUTTONDOWN and event.button == BR1: #bouton R1
##            if isClawOpen:
##                pinceGoto(pinceFermee, v = 70)
##            else :
##                pinceGoto(pinceOuverte, v = 70)
##            isClawOpen = not isClawOpen
####            elif event.button == BSG: #bouton Stick Gauche
####                baseGoto(baseGold, v = 70)
##        if event.type == pygame.JOYBUTTONDOWN and event.button == BSH: #bouton SHARE
##            pistonGauche() # Toggle le piston gauche
##        if event.type == pygame.JOYBUTTONDOWN and event.button == BOP: #bouton OPTION
##            pistonDroit() # Toggle le piston droit
##
##        hat = mon_joystick.get_hat(HAT)
####        if hat[0] == -1 :
####            rah(vt)
####        if hat[0] == 1 :
####            rh(vt)
##        if hat[1] == 1 : #Serre un peu plus la pince
##            bougePince(1)
##        if hat[1] == -1 : #Desserre un peu la pince
##            bougePince(-1)
			

        mon_joystick = pygame.joystick.Joystick(0)
        mon_joystick.init()
        # for i in range(mon_joystick.get_numbuttons()):
        #     if mon_joystick.get_button(i) == 1 :
        #         #print("bouton {} pressed !".format(i))
        #         if i == BPS:
        #             werobot = 0
        #         if i == BTR :
        #             baseGoto(baseHaut,v = 70)
        #         if i == BCE :
        #             baseGoto(baseHautDroit, v = 70)
        #         if i == BCA :
        #             baseGoto(baseHautGauche, v = 70)
        #         if i == BCR :
        #             baseGoto(baseGdistri, v = 70)
        #             #baseGoto(baseBas, v = 70)
        #         #if i == BL1:
        #             #baseGoto(baseGdistri, v = 70)
        #         if i == BSH :
        #             pinceGoto([40,40],v=70)
        #         if i == BOP :
        #             pinceGoto([40,40],v=70)
        #         if i == BR1:
        #             pinceGoto(pinceFermee, v= 70)
        #         if i == BL1:
        #             pinceGoto(pinceOuverte, v=70)
        for i in range(mon_joystick.get_numbuttons()):
            if mon_joystick.get_button(i) == 1 :
                #print("bouton {} pressed !".format(i))
                if i == BPS:
                    werobot = 0
                if i == BTR :
                    baseGoto(baseHaut,v = 70)
                if i == BCE :
                    baseGoto(baseHautDroit, v = 70)
                if i == BCA :
                    baseGoto(baseHautGauche, v = 70)
                if i == BCR :
                    baseGoto(baseGdistri, v = 70)
                if i == BSH :
                    pinceGoto([40,40],v=70)
                if i == BOP :
                    pinceGoto([40,40],v=70)
                """ if i == BR1:
                    pinceGoto(pinceFermee, v= 70)
                    ser.write(b"LED\n") """
                if i == BL1:
                    if isBL1RePressed :
                        if isClawOpen :
                            pinceGoto(pinceFermee, v = 70)
                        else :
                            pinceGoto(pinceOuverte, v=70)
                        isClawOpen = not isClawOpen
                        ser.write(b"LED\n")
                        isBL1RePressed = False
            else :
                if i == BL1:
                    isBL1RePressed = True
##                if i == BR1:
##                    if (time.clock() - oldtimePince) > 0.3 :
##                        if isClawOpen:
##                            pinceGoto(pinceFermee, v = 70)
##                        else :
##                            pinceGoto(pinceOuverte, v = 70)
##                        isClawOpen = not isClawOpen
##                        oldtime = time.clock()
##                if i == BSH :
##                    pistonGauche()
##                if i == BOP :
##                    pistonDroit()
        for i in range(mon_joystick.get_numhats()):
            hat = mon_joystick.get_hat(i)
            if hat[1] == 1 and isHatUpRepressed :
                ser.write(b"plus\n")
                isHatUpRepressed = False
                #bougePince(2)
            if hat[1] == 0 :
                isHatUpRepressed = True
                isHatDownRepressed = True
            
            if hat[1] == -1 and isHatDownRepressed :
                ser.write(b"moins\n")
                isHatDownRepressed = False
                #bougePince(-2)
            if hat[0] == 1 and isHatRightRepressed:
                pistonDroit()
                isHatRightRepressed = False
##                if (time.clock() - oldtimePdroit) > 0.3 :
##                    pistonDroit()
##                    oldtimePdroit = time.clock()
            if hat[0] == 0 :
                isHatRightRepressed = True
                isHatLeftRepressed = True
            if hat[0] == -1 and isHatLeftRepressed:
                pistonGauche()
                isHatLeftRepressed = False
##                if (time.clock() - oldtimePgauche) > 0.3 :
##                    pistonGauche()
##                    oldtimePgauche = time.clock()
        #time.sleep(0.1)           
        pygame.event.clear()
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
                #print("al2 = {0} et vt = {1}".format(al2,vt))
            if ady < 0.5 * adx and ady >= -0.5 * adx:
                te(vt)
            if ady > 0.5 * adx and ady <= 2 * adx:
                tne(vt)
            if ady > 2 * adx and ady >= -2 * adx:
                #print("ordre recu !")
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
            if agy > 2 * agx and agy >= -2 * agx: #Lève le bras, stick gauche en haut
                lb(30)
            if agy < 2 * agx and agy <= -2 * agx: #Baisse le bras, stick gauche en bas
                bb(20)
            if agy < 0.5 * agx and agy >= -0.5 * agx:
                rh(vt)
            if agy < -0.5 * agx and agy >= 0.5 * agx:
                rah(vt)
            
                #~ if abs(ady) <= S and abs(adx) <= S and abs(hat[0]) <= 0 :
                    #~ ar()
            #~ if hat[0] == -1:
                #~ rah(vt)
            #~ if hat[0] == 1 :
                #~ rh(vt)
            #~ pygame.event.clear() #vide la queue - annule plusieurs appuis sur A vert
esc_zero()
monRobot.close()
##baseBras.join()
##posBase.put(0,block=False) #ordre non executé permetant l'arrêt du thread.
print ("")
print ("fin du programme")
