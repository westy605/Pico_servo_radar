from machine import Pin, PWM
import time

# Setup
servo_pin = Pin(16)  # Servo PWM pin
ir_pin = Pin(17, Pin.IN)  # IR sensor digital output pin

# Initialize PWM at 50Hz
servo = PWM(servo_pin)
servo.freq(50)

# Safe duty limits for most hobby servos (on Pico: 0.5ms to 2.5ms pulse width)
MIN_DUTY = 1638   # ~0.5ms pulse (0°)
MAX_DUTY = 8192   # ~2.5ms pulse (230°)

def set_servo_angle(angle):
    # Clamp angle to 0–230
    angle = max(0, min(230, angle))
    # Map angle to duty (using 16-bit range)
    duty = int(MIN_DUTY + (MAX_DUTY - MIN_DUTY) * angle / 230)
    servo.duty_u16(duty)

try:
    print("Servo is moving smoothly. IR activation will stop it.")

    angle = 0
    direction = 1  # Move forward initially

    while True:
        if ir_pin.value() == 0:  # IR sensor triggered
            print("IR sensor activated. Stopping servo.")
            servo.deinit()
            break

        set_servo_angle(angle)
        angle += direction

        if angle >= 230:
            angle = 230
            direction = -1
        elif angle <= 0:
            angle = 0
            direction = 1

        time.sleep(0.01)  

except KeyboardInterrupt:
    print("Stopped manually.")
finally:
    servo.deinit()
