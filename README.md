# werobot tdr2019 python code

## Install

```
pip3 -r requirements.txt
npm install
```

## arduino code

Install arduino [Encoder Library](https://github.com/PaulStoffregen/Encoder):

`arduino-cli lib install Encoder`

Arduino code is in `arduino` folder, to compile and upload using [Arduino Cli](https://github.com/arduino/arduino-cli)

```
make arduino
```

```
arduino-cli compile --fqbn arduino:avr:uno ./arduino

arduino-cli upload --fqbn arduino:avr:uno -p /dev/ttyACM0 ./arduino
```
