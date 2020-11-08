import time
import sys


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


hx = HX711(5,6)
hx.set_reading_format("MSB","MSB")
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()
print("sensor ready, please run tool")

count = 0

while(count < 11):
    val - hx.get_weight(5)
    print(val)
    count = count + 1
    hx.power_down()
    hx.power_up()

cleanAndExit()
