import event_emitter
import asyncio
import websockets
import json
import subprocess

class Controller:
    websocketHost = "localhost"
    websocketPort = 8000
    events = None
    ignoredInputType = [
        "a", "b", "x", "y"
    ]
    websocket = None

    def __init__(self):
        self.events = event_emitter.EventEmitter()

    async def serverLoop(self, websocket, path):
        while True:
            rawBody = await websocket.recv()
            parsedBody = json.loads(rawBody)

            self.websocket = websocket
            if parsedBody["t"] == "detection":
                self.events.emit('controller_detected', controller=parsedBody["d"])

            elif parsedBody["t"] == "disconnection":
                self.events.emit('controller_disconnected')

            elif parsedBody["t"] == "input":
                # filter double input (right game pad)                
                if (parsedBody["d"][0] in self.ignoredInputType) == False:
                    self.events.emit('controller_input', data=parsedBody["d"])      
    
    def startNodeJs(self):
        subprocess.Popen(["node", "dualshock.js"])    

    async def setLed(self, r, g, b):
        await self.websocket.send(json.dumps({'t': 'led', 'd': [r, g, b]}))
                                
    def startServer(self):
        print('dualshock: socket server started')
        # self.startNodeJs()
        asyncio.get_event_loop().run_until_complete(websockets.serve(self.serverLoop, self.websocketHost, self.websocketPort))
        asyncio.get_event_loop().run_forever()
