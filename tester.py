import RPi.GPIO as GPIO
from hx711 import HX711
GPIO.setmode(GPIO.BCM)
hx = HX711(dout_pin=29, pd_sck_pin=31)
print(hx.get_raw_data_mean())
GPIO.cleanup()