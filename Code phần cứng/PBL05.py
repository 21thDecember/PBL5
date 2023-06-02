import RPi.GPIO as GPIO
import Adafruit_DHT
from time import sleep
import threading

motor_IN1=6
motor_IN2=13
switch1=17
switch2=27
button=2
rainsensor = 22
DHTpin = 10
sensor_light = 23
led = 21
sensor = Adafruit_DHT.DHT11

rack_status=0 #O is close and 1 is open
motor_status=0 #0 is stop and 1 is run

def setup():
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motor_IN1,GPIO.OUT)
    GPIO.setup(motor_IN2,GPIO.OUT)
    GPIO.setup(rainsensor,GPIO.IN)
    GPIO.setup(switch1,GPIO.IN)
    GPIO.setup(switch2,GPIO.IN)
    GPIO.setup(button,GPIO.IN)
    GPIO.setup(sensor_light,GPIO.IN)
    GPIO.setup(led,GPIO.OUT)
    for i in range(3):
        GPIO.output(led, GPIO.HIGH)
        sleep(0.25)
        GPIO.output(led, GPIO.LOW)
        sleep(0.25)

def motor_up():
    '''close the rack'''
    global motor_status
    motor_status=1
    GPIO.output(motor_IN1,GPIO.HIGH)
    GPIO.output(motor_IN2,GPIO.LOW)
    print('motor up')
    
def motor_down():
    '''open the rack'''
    global motor_status
    motor_status=1
    GPIO.output(motor_IN1,GPIO.LOW)
    GPIO.output(motor_IN2,GPIO.HIGH)
    print('motor down')
    
def motor_stop():
    '''stop motor rack'''
    global motor_status
    motor_status=0
    GPIO.output(motor_IN1,GPIO.LOW)
    GPIO.output(motor_IN2,GPIO.LOW)
    print('motor stop')
    
def switch_up(channel=0):
    global rack_status
    motor_stop() # Rack is opening
    rack_status=1 # Rack status is open
    print('rack switch up')
    GPIO.output(led, GPIO.HIGH)
    motor_down()
    sleep(0.05)
    motor_stop()
    
def switch_down(channel=0):
    global rack_status
    motor_stop()
    rack_status=0 #rack is closed
    print('rack switch down')
    GPIO.output(led, GPIO.LOW)
    motor_up()
    sleep(0.05)
    motor_stop()
    
def button_press(channel=0):
    if rack_status == 0 and motor_status == 0:
        motor_up()
    elif  rack_status == 1 and motor_status == 0:
        motor_down()
    else:
        motor_stop()
def reainseroron(channel=0):
    if rack_status == 1: # Rack is open 
        motor_down()

def print_tem_hur():
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, DHTpin)
        print(f'Nhiet do: {temperature}; Do am: {humidity}')
        sleep(10)

def lightsensor(channel=0):
    if rack_status == 1: # Rack is open 
        motor_down()
        

if __name__ == '__main__':
    setup()
    print('setup...Start!')
    motor_stop()
    GPIO.add_event_detect(switch1,GPIO.FALLING,callback=switch_up,bouncetime=300)
    GPIO.add_event_detect(switch2,GPIO.FALLING,callback=switch_down,bouncetime=300)
    GPIO.add_event_detect(button,GPIO.FALLING,callback=button_press,bouncetime=300)
    GPIO.add_event_detect(rainsensor,GPIO.FALLING,callback=reainseroron,bouncetime=300)
    GPIO.add_event_detect(sensor_light, GPIO.RISING, callback=lightsensor, bouncetime=300)
    threadtemp = threading.Thread(target=print_tem_hur)
    threadtemp.start()
    
    while True:
        pass

    
    GPIO.cleanup()