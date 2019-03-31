from src.Robot import Robot
import os, sys

try:
    robot = Robot()
    robot.init()
except KeyboardInterrupt:
    robot.exit()
    print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
