# RobotCars
Several Example Codes for Robot Cars with HC-12, nRF24, Bluetooth, autonomous; Arduino and MicroPython

Detailed explanations in German Language in eBook "Smart Robot Cars", available i.a. in amazon's Kindle Shop
https://www.amazon.de/Smart-Robot-Cars-Fernsteuerungen-L%C3%B6sungsans%C3%A4tze-ebook/dp/B0DKJMB1QZ/ref=sr_1_2?crid=3ASJ132TAIN4S&dib=eyJ2IjoiMSJ9._wJaJboM_aVYbFQ4YbZfOfeTxEVCcxAjVBRy7ZN-EYRWMRhnTsUIhcZngYIoc9lN6HulUC1p1THiX5-Ud3LZOOwqH3G5Ji9w3T5G8wCeCBx1EI2fsvq_3IChSoZtG26ecEalwGOE18pDmKFJ9sxUdo2GSg392f8Aphp9BUxXisnqOWN_FlvAxvteGMz_ntche6U5c_9XULT3_AGV9wAjXFAAB68pqQM4VMGZdNMTjyA.pk8eWtL2HFAgKio7CSDCJbTdZVQsFXsDqT663XWIhNo&dib_tag=se&keywords=ebook+smart+robot+car&qid=1729760896&s=digital-text&sprefix=%2Cdigital-text%2C80&sr=1-2


Most examples are based on an own-defined code for radio transmission:
- first digit or first two digits (1 to 31) for speed, second two digits (01 to 31) for steering, last digit for status of three buttons
- e.g. 16160 means stand still, no buttons pressed; 31163 means full forward, buttons 1 and 2 pressed
- 22221 means slowly forward, right curve, button 1 pressed;    values below 16 mean backward or left

RobotCarBlueDot for Raspberry Pi requires Android App Bluedot by Martin O'Hanlon
