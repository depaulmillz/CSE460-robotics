import Motor
import time
import Buzzer
import Led

def stop(PWM):
    PWM.setMotorModel(0, 0, 0, 0)

def turn_90deg_left(PWM):
    stop(PWM)
    time.sleep(.2)
    PWM.setMotorModel(-500, -500, 2000, 2000)
    time.sleep(.84)

def move_forward_2_sec(PWM):
    PWM.setMotorModel(500, 500, 500, 500)
    time.sleep(2)


def main():
    PWM = Motor.Motor()
 
    led = Led.Led()
    led.ledIndex(0x1 ^ 0x2 ^ 0x4 ^ 0x8, 0, 0, 0)

    move_forward_2_sec(PWM)
    turn_90deg_left(PWM)
    # color red on led 0
    led.ledIndex(0x1, 255, 0, 0)
    move_forward_2_sec(PWM)
    turn_90deg_left(PWM)
    # color blue on led 1
    led.ledIndex(0x2, 0, 0, 255)
    move_forward_2_sec(PWM)
    turn_90deg_left(PWM)
    # color green on led 2
    led.ledIndex(0x4, 0, 255, 0)
    move_forward_2_sec(PWM)
    turn_90deg_left(PWM)
    # color yellow on led 3
    led.ledIndex(0x8, 255, 255, 0)

    stop(PWM)
    B = Buzzer.Buzzer()
    B.run('1')
    time.sleep(1)
    B.run('0')
    time.sleep(10)
    led.ledIndex(0x1 ^ 0x2 ^ 0x4 ^ 0x8, 0, 0, 0)

if __name__ == '__main__':
    main()

