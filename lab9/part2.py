import Motor
import time

PWM = Motor.Motor()

def stop():
    PWM.setMotorModel(0, 0, 0, 0)

def move(l, r):
    PWM.setMotorModel(l, l, r, r)

def run():
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

    try:
        run(fast)
    except KeyboardInterrupt as e:
        stop()
        

