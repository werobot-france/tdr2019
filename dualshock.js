// const WebSocket = require('ws');
const Dualshock = require('dualshock')

// const ws = new WebSocket('ws://localhost:8000');

let digital = JSON.stringify({
    a: false,
    b: false,
    x: false,
    y: false,
    up: false,
    down: false,
    left: false,
    right: false,
    l1: false,
    l2: false,
    l3: false,
    r1: false,
    r2: false,
    r3: false,
    select: false,
    start: false,
    ps: false,
    pad: false,
    t1: false,
    t2: false
})

let analog = JSON.stringify({
    lStickX: 127,
    lStickY: 127,
    rStickX: 127,
    rStickY: 127,
    l2: 0,
    r2: 0,
    // t1X: 180,
    // t1Y: 639,
    // t2X: 0,
    // t2Y: 0
})

// ws.on('open', function open() {
//     ws.send(JSON.stringify({ t: 'init' }))
//     
// });

// ws.on('close', function close() {
//     console.log('> disconnected');
// });

function connect() {
    let devicesList = Dualshock.getDevices();
    if (devicesList.length != 0) {

        let device = devicesList[0]
        let gamepad = Dualshock.open(device, {
            smoothAnalog: 10,
            smoothMotion: 15,
            joyDeadband: 4,
            moveDeadband: 4
        })

        console.log(JSON.stringify({
            t: 'detection',
            d: device
        }))

        let ignoredIndex = ["t1X", "t1Y", "t2X", "t2Y"]

        gamepad.onmotion = false;
        gamepad.onstatus = false;
        gamepad.onupdate = function () {
            if (JSON.stringify(this.digital) != digital) {
                digital = JSON.stringify(this.digital)
                console.log(JSON.stringify({
                    t: 'input',
                    i: 'digital',
                    d: this.digital
                }))
            }
            let analogRaw = {
                lStickX: this.analog.lStickX,
                lStickY: this.analog.lStickY,
                rStickX: this.analog.rStickX,
                rStickY: this.analog.rStickY,
                l2: this.analog.l2,
                r2: this.analog.r2
            }
            if (JSON.stringify(analogRaw) != analog) {
                //console.log((new Date()).toString() + ' > send analog')
                analog = JSON.stringify(analogRaw)
                console.log(JSON.stringify({
                    t: 'input',
                    i: 'analog',
                    d: this.analog
                }))
            }
        }

        // gamepad.ondigital = function (button, value) {
        //     ws.send(JSON.stringify({
        //         t: 'input',
        //         d: [button, value]
        //     }))
        // }
        // gamepad.onanalog = function (axis, value) {
        //     ws.send(JSON.stringify({
        //         t: 'input',
        //         d: [axis, value]
        //     }))
        // }
        gamepad.ondisconnect = function () {
            connect()
            
            console.log(JSON.stringify({
                t: 'disconnection'
            }))
        }
        // ws.on('message', (data) => {
        //     let body = JSON.parse(data)
        //     if (body.t == 'led') {
        //         gamepad.setLed(body.d[0], body.d[1], body.d[2])
        //     }
        // })
        return true
    } else {
        setTimeout(connect, 2000)
    }
}
connect()