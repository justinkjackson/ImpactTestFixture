import time
import sys
#import RPi.GPIO as GPIO

EMULATE_HX711 =False

referenceUnit = 431

if not EMULATE_HX711:
        
        import RPi.GPIO as GPIO
	from hx711 import HX711
else:
	from emulated_hx711 import HX711

def cleanAndExit():
        
	print("Cleaning")
	
	if not EMULATE_HX711:
		GPIO.cleanup()
	print("Bye")
	sys.exit()

hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()
print("Sensor ready, please run tool!")

count = 0
#while loop for 7 iterations thatll give enough time to capture torque
while(count < 11):
	#collect value
	val = hx.get_weight(5)
	#print value
	print(val)
	count = count + 1
	#power up and down to get output again
	hx.power_down()
	hx.power_up()
	

#outside the loop, set the torque value collected to the text box on the GUI
#self.torqueNumber.setText(str(val))

cleanAndExit()

