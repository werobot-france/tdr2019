import Adafruit_PCA9685
import time
import pypot.dynamixel
import pypot.robot
from . Controller import Controller

class Robot:

    # LESC = (6,5,0,1) # liste des ESC (avant gauche, avant droit, arrière gauche, arrière droit)
    escSlots = {
        'frontLeft': 6,
        'frontRight': 5,
        'backLeft': 0,
        'backRight': 1
        # 'arm': 2
    }

    pistonSlots = {
        'left': 3,
        'right': 4
    }

    # positons in degree of servo pistons
    pistonPositions = {
        'left': {
            'current': 100,
            'init': 100,
            'blocked': 325,
            'push': 365
        },
        'right': {
            'current': 500,
            'init': 500,
            'blocked': 275,
            'push': 230
        }
    }

    minSpeed = 25

    currentSpeed = 25

    armConfig = {
        'controllers': {
            'my_dxl_controller': {
                'sync_read': False,
                'attached_motors': ['base', 'claw'],
                'port': '/dev/ttyUSB0'
            }
        },
        'motorgroups': {
            'base': ['m2', 'm3'],
            'claw': ['m4', 'm5']
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
    
    # differents arm positons
    armPositions = {
        'base': {
            'middle': [0, 102],
            'up': [0, 0],
            'down': [-1, 10],
            'greatDispenser': [2, -29],
            'greatDispenserMiddle': [-50, 2, 52],
            'upRight': [-60, -27],
            'upLeft': [65, -22],
            'pushGoldenium': [0, 0, 0]
        },
        'claw': {
            'opened': [89, 89],
            'closed': [97, 97],
            'large': [40, 40]
        }
    }

    pistonStatus = {
        'left': False,
        'right': False
    }

    def __init__(self):
        self.servo = Adafruit_PCA9685.PCA9685()
        self.servo.set_pwm_freq(50)
        self.controller = Controller()

    def initEsc(self, slot):
        print(slot)
        self.servo.set_pwm(slot, 0, 307) #307 est le signal neutre sous 50 Hz (1.5 / 20 x 4096 = 307)
        time.sleep(1)
    
    def initServoPiston(self):
        self.servo.set_pwm(self.pistonSlots['left'], 0, self.pistonPositions['left']['init'])
        self.servo.set_pwm(self.pistonSlots['right'], 0, self.pistonPositions['right']['init'])

    # équivalent de la fonction map() de arduino
    def mappyt(self, x, inMin, inMax, outMin, outMax):
        return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin

    # fonction esc pour une vitesse de moteur de -100 à 100()
    def convertSpeedToEsc(self, speed):
        return round(self.mappyt(speed, 0, 100, 307, 410))

    # id (left or right)
    def togglePiston(self, id):        
        if self.pistonPositions[id]['current'] == self.pistonPositions[id]['init']:
            self.pistonStatus[id] = True
            self.pistonPositions[id]['current'] = self.pistonPositions[id]['push']
        else:
            self.pistonStatus[id] = False
            self.pistonPositions[id]['current'] = self.pistonPositions[id]['init']
        self.servo.set_pwm(self.pistonSlots[id], 0, self.pistonPositions[id]['current'])

    def stopAll(self):
        for slot in self.escSlots:
            self.servo.set_pwm(self.escSlots[slot], 0, self.convertSpeedToEsc(0))

    def northTranslation(self, speed):
        a = self.convertSpeedToEsc(speed)
        self.servo.set_pwm(self.escSlots['frontLeft'], 0, a)
        self.servo.set_pwm(self.escSlots['frontRight'], 0, a)
        self.servo.set_pwm(self.escSlots['backLeft'], 0, a)
        self.servo.set_pwm(self.escSlots['backRight'], 0, a)

    def southTranslation(self, speed):
        self.northTranslation(-speed)

    def eastTranslation(self, speed):
        a = self.convertSpeedToEsc(speed)
        r = self.convertSpeedToEsc(-speed)
        self.servo.set_pwm(self.escSlots['frontLeft'], 0, a)
        self.servo.set_pwm(self.escSlots['frontRight'], 0, r)
        self.servo.set_pwm(self.escSlots['backLeft'], 0, r)
        self.servo.set_pwm(self.escSlots['backRight'], 0, a)

    def westTranslation(self, speed):
        self.eastTranslation(- speed)

    def clockwiseRotation(self, speed):
        a = self.convertSpeedToEsc(speed)
        r = self.convertSpeedToEsc(-speed)
        self.servo.set_pwm(self.escSlots['frontLeft'], 0, a)
        self.servo.set_pwm(self.escSlots['frontRight'], 0, r)
        self.servo.set_pwm(self.escSlots['backLeft'], 0, a)
        self.servo.set_pwm(self.escSlots['backRight'], 0, r)
    
    def antiClockwiseRotation(self, speed):
        self.clockwiseRotation(-speed)

    def northEastTranslation(self, speed):
        a = self.convertSpeedToEsc(speed)
        s = self.convertSpeedToEsc(0)
        self.servo.set_pwm(self.escSlots['frontLeft'], 0, a)
        self.servo.set_pwm(self.escSlots['frontRight'], 0, s)
        self.servo.set_pwm(self.escSlots['backLeft'], 0, s)
        self.servo.set_pwm(self.escSlots['backRight'], 0, a)
    
    def southWestTranslation(self, speed):
        self.northEastTranslation(-speed)

    def northWestTranslation(self, speed):
        a = self.convertSpeedToEsc(speed)
        s = self.convertSpeedToEsc(0)
        self.servo.set_pwm(self.escSlots['frontLeft'], 0, s)
        self.servo.set_pwm(self.escSlots['frontRight'], 0, a)
        self.servo.set_pwm(self.escSlots['backLeft'], 0, a)
        self.servo.set_pwm(self.escSlots['backRight'], 0, s)

    def southEastTranslation(self, speed):
        self.northWestTranslation(-speed)

    def raiseArm(self, speed):
        self.servo.set_pwm(self.escSlots['arm'], 0, self.convertSpeedToEsc(-speed))

    def lowerArm(self, speed):
        self.raiseArm(-speed)

    def initArm(self):
        ports = pypot.dynamixel.get_available_ports()
        engines = pypot.dynamixel.DxlIO(ports[0])
        IDs = engines.scan(range(10))

        for a in IDs:
            print(engines.get_present_position((a,)))
            engines.set_moving_speed({a:30})
        
        engines.close()

        self.arm = pypot.robot.from_config(self.armConfig)

        self.arm.power_up()

    def armBaseGoTo(self, L, v = 30, wait = False):
        n = len(self.arm.base)
        if len(L) == n:
            if not wait :            
                for i in range(n) :
                    self.arm.base[i].moving_speed = v
                    self.arm.base[i].goal_position = L[i]
            else:
                for i in range(1,n):
                    delta = abs(self.arm.base[i].present_position - L[i])
                    duration = delta / v
                    self.arm.base[i].goto_position(L[i], duration, wait=True)
        else:
            print("ERREUR : il y a {} moteurs et la liste contient {} valeurs".format(n,len(L)))

    def armClawGoTo(self, L, v = 30, wait = False):
        n = len(self.arm.claw)
        if len(L) == n:
            if not wait :
                for i in range(n) :
                    self.arm.claw[i].moving_speed = v
                    self.arm.claw[i].goal_position = L[i]
            else:
                for i in range(n):
                    delta = abs(self.arm.claw[i].present_position - L[i])
                    duration = delta / v
                    self.arm.claw[i].goto_position(L[i], duration, wait=True)
        else:
            print("ERREUR : il y a {} moteurs et la liste contient {} valeurs".format(n,len(L)))

    def moveClaw(self, value):
        for m in self.arm.claw :
            m.moving_speed = 30
            m.goal_position = m.present_position + value
    
    def onControllerDetected(self, controller):
        print("A new controller was detected")
        self.controller.setLed(0, 255, 0)

    def onControllerDisconnected(self):
        print("Controller disconnected")

    def onControllerInput(self, inputType, data):
        if inputType == "digital":
            if data['left']:
                self.togglePiston('left')
                self.controller.setLed(255, 50, 50)
            if data['right']:
                self.controller.setLed(50, 50, 255)
                self.togglePiston('right')
            if data['triangle']:
                self.armBaseGoTo(self.armPositions['base']['up'], v = 70)
            if data['circle']:
                self.armBaseGoTo(self.armPositions['base']['upRight'], v = 70)
            if data['square']:
                self.armBaseGoTo(self.armPositions['base']['upLeft'], v = 70)
            if data['cross']:
                self.armBaseGoTo(self.armPositions['base']['greatDispenser'], v = 70)
            if data['start']:
                self.armClawGoTo(self.armPositions['claw']['large'], v = 70)
            if data['l1']:
                self.armClawGoTo(self.armPositions['claw']['opened'], v = 70)
            if data['r1']:
                self.armClawGoTo(self.armPositions['claw']['closed'], v = 70)
            # if data['up']:
            #     # self.moveClaw(2)
            #     # self.raiseArm(30)
            # if data['down']:
            #     # self.moveClaw(-2)
            #     # self.lowerArm(20)
            if data['ps']:
                self.stopAll()
        if inputType == "analog":
            seuil = 0

            print('analog')

            lStickX = data['lStickX'] - 127
            lStickY = -(data['lStickY'] - 127)
            rStickX = data['rStickX'] - 127
            rStickY = -(data['rStickY'] - 127)
            l2 = data['l2'] - 127 #accélération
            r2 = data['r2'] - 127 #accélération

            print([rStickX, rStickY])
            
            if (abs(lStickX) <= seuil and 
                abs(lStickY) <= seuil and 
                abs(lStickX) <= seuil and 
                abs(lStickY) <= seuil and
                (abs(l2+1) <= seuil or abs(l2) <= seuil) and
                (abs(r2+1) <= seuil or abs(r2) <= seuil)):
                self.stopAll()
            else:
                # if lStickX == -1:
                #     self.currentSpeed = self.minSpeed
                # elif lStickX != 0 :
                #     self.currentSpeed = self.mappyt(lStickX, -1, 1, 0, 1) * 100
                #     #print("lStickX = {0} et vt = {1}".format(lStickX,vt))
              
                # r stick ?              
                if rStickY < 0.5 * rStickX and rStickY >= -0.5 * rStickX:
                    self.eastTranslation(self.currentSpeed)
                if rStickY > 0.5 * rStickX and rStickY <= 2 * rStickX:
                    self.northEastTranslation(self.currentSpeed)
                if rStickY > 2 * rStickX and rStickY >= -2 * rStickX:
                    #print("ordre recu !")
                    self.northTranslation(self.currentSpeed)
                if rStickY < -2 * rStickX and rStickY >= -0.5 * rStickX:
                    self.northWestTranslation(self.currentSpeed)
                if rStickY < -0.5 * rStickX and rStickY >= 0.5 * rStickX:
                    self.westTranslation(self.currentSpeed)
                if rStickY < 0.5 * rStickX and rStickY >= 2 * rStickX:
                    self.southWestTranslation(self.currentSpeed)
                if rStickY < 2 * rStickX and rStickY <= -2 * rStickX:
                    self.southTranslation(self.currentSpeed)
                if rStickY > -2 * rStickX and rStickY <= -0.5 * rStickX:
                    self.southEastTranslation(self.currentSpeed)

                # left
                # if lStickY > 2 * lStickX and lStickY >= -2 * lStickX: #Lève le bras, stick gauche en haut
                #     self.raiseArm(30)
                # if lStickY < 2 * lStickX and lStickY <= -2 * lStickX: #Baisse le bras, stick gauche en bas                
                #     self.lowerArm(20)
                # if lStickY < 0.5 * lStickX and lStickY >= -0.5 * lStickX:
                #     self.clockwiseRotation(self.currentSpeed)
                # if lStickY < -0.5 * lStickX and lStickY >= 0.5 * lStickX:
                #     self.antiClockwiseRotation(self.currentSpeed)
        
        # do stuff...

    def startControllerService(self):
        # set event listeners
        self.controller.events.on('controller_detected', self.onControllerDetected)
        self.controller.events.on('controller_disconnected', self.onControllerDisconnected)
        self.controller.events.on('controller_input', self.onControllerInput)

        # start socket server
        self.controller.startServer()
        
    def init(self):
        print('Init....')

        # Init of all the esc
        for esc in self.escSlots:
            print('Init', esc)
            self.initEsc(self.escSlots[esc])

        print('Esc successfuly initialized')

        self.initServoPiston()

        print('Pistons successfuly initialized')

        # self.initArm()

        print('Arm successfuly initialized')

        # self.armBaseGoTo(self.armPositions['base']['down'])
        # self.armClawGoTo(self.armPositions['claw']['opened'], v = 70)

        # print('Starting controller service...')

        self.startControllerService()

