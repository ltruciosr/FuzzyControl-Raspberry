
import RPi.GPIO as GPIO
import time

control_value = 70
# Setup GPIO pins
# Set the BCM mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Outputs
GPIO.setup( 4, GPIO.OUT) # heat command
GPIO.setup(17, GPIO.OUT) # cool command
GPIO.setup(27, GPIO.OUT) # no change command
# Ensure all LEDs are off to start
GPIO.output( 4, GPIO.LOW)
GPIO.output(17, GPIO.LOW)
GPIO.output(27, GPIO.LOW)
# The following should be appended to the existing code
if control_value > 65 and control_value < 75: # no change
    GPIO.output(27, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(27, GPIO.LOW)
elif control_value > 82 and control_value < 84: # heat
    GPIO.output(4, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(4, GPIO.LOW)
elif control_value > 56 and control_value < 68: # cool
    GPIO.output(17, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(17, GPIO.LOW)
else:
    print 'strange value calculated'
# This next statement used in debugging phase
print 'Thats all folks'

