import Motor
import time
import Ultrasonic

PWM = Motor.Motor()
sensor = Ultrasonic.Ultrasonic()

def stop():
    PWM.setMotorModel(0, 0, 0, 0)

def move_forward_backward(val):
    PWM.setMotorModel(val, val, val, val)


def q1():
    for x in [500, 1000, 1500, 2000, 2500]:
        move_forward_backward(x)
        time.sleep(2)
        stop()
        time.sleep(1)
        move_forward_backward(-x)
        time.sleep(2)
        stop()
        time.sleep(1)

def q2():
    while True:
        print(sensor.get_distance())
        time.sleep(1)

def q3():
    K = -100

    x = sensor.get_distance()
    
    while x != 50:
        u = K * (50 - x) 
        print(u, x)
        move_forward_backward(u)
        time.sleep(0.01)
        x = sensor.get_distance()
    stop()

def run(K):
    x = sensor.get_distance()
   
    start = time.time()
    while x != 50:
        u = K * (50 - x) 
        print(u, x)
        move_forward_backward(u)
        time.sleep(0.01)
        x = sensor.get_distance()
    stop()
    end = time.time()
    print(end - start)


if __name__ == '__main__':
    slow = -25
    fast = -100
    aggressive = -2000

    try:
        run(fast)
    except KeyboardInterrupt as e:
        stop()
        
    #try:
    #    run(fast)
    #except KeyboardInterrupt as e:
    #    stop()
    #   
    #try:
    #    run(aggressive)
    #except KeyboardInterrupt as e:
    #    stop() 
