import os, time, serial
import threading, queue

class DcEncodeur(threading.Thread):
    """ A worker thread that takes directory names from a queue, finds all
        files in them recursively and reports the result.

        Input is done by placing directory names (as strings) into the
        Queue passed in pos_q.

        Output is done by placing tuples into the Queue passed in result_q.
        Each tuple is (thread name, dirname, [list of files]).

        Ask the thread to stop by calling its join() method.
    """
    def __init__(self,servo, esc,port,pos_q,vit):
        super(DcEncodeur, self).__init__()
        self.servo = servo
        self.esc = esc
        self.port = port
        self.pos_q = pos_q
        self.vit = vit
        self.stoprequest = threading.Event()
        self.ser = serial.Serial( port=self.port, baudrate = 9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

    def run(self):
        # As long as we weren't asked to stop, try to take new tasks from the
        # queue. The tasks are taken with a blocking 'get', so no CPU
        # cycles are wasted while waiting.
        # Also, 'get' is given a timeout, so stoprequest is always checked,
        # even if there's nothing in the queue.
        while not self.stoprequest.isSet():
            try:
                target_pos = self.pos_q.get(True,0.05)
                while self.pos_q.empty():
                    self.goto_postion(target_pos)
            except queue.Empty:
                continue

    def join(self, timeout=None):
        """
        arrête le thread après  le prochain ordre dans la queue
        le dernier ordre ne sera pas exécuté
        """
        self.stoprequest.set()
        super(DcEncodeur, self).join(timeout)
    
    def goto_postion(self,target_pos):
        current_pos = readEnc() # lit la position actuelle
        ecart = target_pos - current_pos
        while abs(ecart) > 5 :
            sign = ecart/abs(ecart)
            self.servo.set_pwm(self.esc,0,sign*self.vit)
    
    def readEnc(self):
        x = self.ser.readline()
        return int(x)
