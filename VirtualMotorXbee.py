# Python Script that opens pygame and reads commands from arrow keys, prepares a
# motor command and sends it
# *** Attempt with Xbee (aka XBox controller integration) - now we want camera
# to move via commands from xbox controller (info sent and recieved with xbee)
# - As Constructed the xboxArduino.ino script is unchanged so for now we are just
# trying to move the camera in the x direction (using left stick)


from xbee import XBee
from base.KaicongOutput import KaicongOutput
import urllib2
import serial

class VirtualCamMotor(KaicongOutput):
    
    # state commands for camera.
    CMDLIST = {
        "PTZ_UP": 0,
        "PTZ_UP_STOP": 1,
        "PTZ_DOWN": 2,
        "PTZ_DOWN_STOP": 3,
        "PTZ_LEFT": 4,
        "PTZ_LEFT_STOP": 5,
        "PTZ_RIGHT": 6,
        "PTZ_RIGHT_STOP": 7,
        "PTZ_LEFT_UP": 90,
        "PTZ_RIGHT_UP": 91,
        "PTZ_LEFT_DOWN": 92,
        "PTZ_RIGHT_DOWN": 93,
        "PTZ_STOP": 1,
        "PTZ_CENTER": 25,
        "PTZ_VPATROL": 26,
        "PTZ_VPATROL_STOP": 27,
        "PTZ_HPATROL": 28,
        "PTZ_HPATROL_STOP": 29,
        "IO_ON": 94, # TODO: What does this do?
        "IO_OFF": 95, # and this one?
    }
    
    # This table converts a vector-style direction to its command
    MOVELIST = {
        "00": "PTZ_STOP",
        "0+": "PTZ_UP",
        "0-": "PTZ_DOWN",
        "+0": "PTZ_RIGHT",
        "-0": "PTZ_LEFT",
        "++": "PTZ_RIGHT_UP",
        "+-": "PTZ_RIGHT_DOWN",
        "-+": "PTZ_LEFT_UP",
        "--": "PTZ_LEFT_DOWN",
    }
    
    URI = "http://{0}:81/decoder_control.cgi?loginuse={1}&loginpas={2}&command=%d&onestep=0"
    
    # user and pwd is your camera username and password
    def __init__(self, domain, user="rysm7991", pwd="rysm7991"):
        KaicongOutput.__init__(
            self, 
            domain, 
            VirtualCamMotor.URI, 
            user, 
            pwd
        )
        
        self.state = '00'
        
    def _to_symbol(self, v):
        if v > 0:
            return '+'
        if v < 0:
            return '-'
        else:
            return '0'

    # send our command to URL stream
    def send_command(self, cmdstr): 
        stream = urllib2.urlopen(self.uri % (VirtualCamMotor.CMDLIST[cmdstr]))
        result = stream.read()
        assert "ok" in result
        stream.close()

    # prepare specific move command given an x&y
    def move(self, xy):
        move_symbol = self._to_symbol(xy[0]) + self._to_symbol(xy[1])
        cmdstr = VirtualCamMotor.MOVELIST[move_symbol]
        if cmdstr != self.state:
            self.send_command(cmdstr)
        self.state = cmdstr
        
serialData = serial.Serial('/dev/ttyUSB0', 9600)
xbee = XBee(serialData)

if __name__ == "__main__":
    import pygame
    import sys
    
    if len(sys.argv) != 2:
    
        sys.exit(-1)
    
    pygame.init()
    screen = pygame.display.set_mode((320, 240))
    
    motor = VirtualCamMotor(sys.argv[1])
    
    def checkOurArrows():
        keys = pygame.key.get_pressed()
        x = 0
        y = 0
        if keys [pygame.K_LEFT]:
            x = -1
        if keys [pygame.K_DOWN]:
            y = -1
        if keys [pygame.K_RIGHT]:
            x = 1
        if keys [pygame.K_UP]:
            y = 1
            
        motor.move([x, y])
            
    while 1:
        for event in pygame.event.get():
            
            serialData = serial.Serial('/dev/ttyUSB0', 9600)
            xbee = XBee(serialData)

            if xbee == 3:
               x = -1
            if xbee == 4:
               x = 1

            motor.move([x, 0])
            
            if event.type == pygame.QUIT:
                 sys.exit()
        checkOurArrows()
        
        
