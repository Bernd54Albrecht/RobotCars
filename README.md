# RobotCars
Several Example Codes for Robot Cars with HC-12, nRF24, Bluetooth, automous; Arduino and MicroPython

Most examples are based on a own-defined code for radio transmission:
- first two digits (1 to 31) for speed, second two digits for steering, last digit for status of three buttons
- e.g. 16160 means stand still, no buttons pressed; 31163 means full forward, buttons 1 and 2 pressed
- 22221 means slowly forward, right curve, values below 15 mean backward or left

RobotCarBlueDot for Raspberry Pi requires Android App Bluedot by Martin O'Hanlon
