import BlynkLib
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
from time import sleep
try:
 import urllib.request as urllib2
except ImportError:
 import urllib2
baseURL1 = 'http://api.thingspeak.com/update?api_key=Y8C2YRBY4RMT2JJ1&field1='
baseURL2 = 'http://api.thingspeak.com/update?api_key=Y8C2YRBY4RMT2JJ1&field2='
baseURL3 = 'http://api.thingspeak.com/update?api_key=Y8C2YRBY4RMT2JJ1&field3='
sensor=Adafruit_DHT.DHT11
gpio=17
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)
blynk = BlynkLib.Blynk('suRqXEuwi6u8OKcyYJH6MWXpAjbfz9XF')
delayt = .1
value = 0
ldr = 7
buzzer=23
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
def rc_time (ldr):
 count = 0
 #Output on the pin for ldr
 GPIO.setup(ldr, GPIO.OUT)
 GPIO.output(ldr, False)
 time.sleep(delayt)
 #Change the pin back to input
 GPIO.setup(ldr, GPIO.IN)
 #Count until the pin goes high
 while (GPIO.input(ldr) == 0):
 count += 1
 return count
@blynk.VIRTUAL_WRITE(0)
def my_write_handler(value):
 print('Current V0 value: {}'.format(value))
 if value==['1']:
 GPIO.output(21,True)
 print('on')
 else:
 GPIO.output(21,False)
 print('off')
@blynk.VIRTUAL_READ(2)
def my_read_handler():
 blynk.virtual_write(2,temperature)
 blynk.virtual_write(1,humidity)
 blynk.virtual_write(3,value)
GPIO.output(buzzer,GPIO.LOW)
while True:

 humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
 print('LDR Value:')
 value = rc_time(ldr)
 print(value)
 if humidity is not None and temperature is not None:
 print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))

 if temperature>32 or humidity>50:
 GPIO.output(buzzer,GPIO.HIGH)
 print ("Beep")
 sleep(0.5) # Delay in seconds
 GPIO.output(buzzer,GPIO.LOW)
 #Switch on Fan
 #GPIO.output(11,GPIO.HIGH)
 else:
 print('Failed to get reading. Try again!')

 f1 = urllib2.urlopen(baseURL1 +str(temperature))
 f1.read()
 f1.close()
 f2 = urllib2.urlopen(baseURL2 +str(humidity))
 f2.read()
 f2.close()
 f3 = urllib2.urlopen(baseURL3 +str(value))
 f3.read()
 f3.close()
 blynk.run()
 try:
 while True:
 print("Ldr Value:")
 value = rc_time(ldr)
 print(value)
 if ( value <= 10000 ):
 print("Lights are ON")
 GPIO.output(21,GPIO.HIGH)
 time.sleep(2)
 if (value > 10000):
 print("Lights are OFF")
 GPIO.output(21,GPIO.LOW)
 time.sleep(2)
 except KeyboardInterrupt:
 pass
 finally:
 GPIO.cleanup()
 blynk.run()