#must install x11-xserver-utils on host 
import time
import RPi.GPIO as GPIO

GPIO.setmode (GPIO.BCM ) 
GPIO.setwarnings (False)

GPIO.setup(PIR_PIN,GPIO.IN)
GPIO.setup (DISPLAY_CTRL,GPIO.OUT)
#os.environ['DISPLAY'] = ":0"
GPIO.output (DISPLAY_CTRL,GPIO.LOW)

dorun = False
display_is_on = True
display_is_sleeping = False
lastsignaled =0

modules = None
def pulseDisplayPin():
    GPIO.output (DISPLAY_CTRL,GPIO.HIGH)
    time.sleep(PULSE_LEN)
    GPIO.output (DISPLAY_CTRL,GPIO.LOW)

def set(mod_list):
    global modules
    modules = mod_list

def run():
    global dorun
    global display_is_on
    global display_is_sleeping
    
    dorun = True  
    print("Staring wakeup on PIR...")

    while dorun is True:
        now=time.time()
        if GPIO.input(PIR_PIN):
            lastsignaled = now
            if not display_is_on:
                pulseDisplayPin()
                display_is_on = True
                
            if display_is_sleeping:
                subprocess.call('xset dpms force on', shell=True)
                display_is_sleeping = False
                global modules
                for m in modules:
                    m.activate()
        else:
            #put the screen to sleep if short threshold exceeded
            if not display_is_sleeping and now-lastsignaled > SLEEP_THRESH:     
                subprocess.call('xset dpms force off', shell=True)
                display_is_sleeping = True
                global modules
                for m in modules:
                    m.inactivate()
            #shut the screen off if long threshold exceeded
            if display_is_on and now-lastsignaled > OFF_THRESH:
                pulseDisplayPin()
                display_is_on = False
                    
        time.sleep(1)

    GPIO.cleanup()
    if not display_is_on:
        pulseDisplayPin()
    
    subprocess.call('xset dpms force on', shell=True)
    print("Stopped wakeup on PIR...")

def stop():
    global dorun
    dorun = False
