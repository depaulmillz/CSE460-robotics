from numpy import *
from matplotlib.pyplot import *

def euler_method(dt, x, u):
    #Euler method
    x += u * dt
    return x

class Simulator:
    
    def __init__(self, control, sense, solver = euler_method):
        self.control = control
        self.sense = sense
        self.solver = solver
    
    def run(self, start_time = 0, end_time = 1, start_position=array([0., 0.]), dt = 1e-3):
        time = linspace(start_time, end_time, int(end_time / dt) + 1)

        x = copy(start_position)
        x_t = [copy(x)]

        for t in time:
            y = self.sense(x)
            u = self.control(t, y)
            x = self.solver(dt, x, u)
            x_t.append(copy(x))

        return array(x_t)
    
    def run_and_plot_2d(self, start_time = 0, end_time = 1, start_position=array([0., 0.]), dt = 1e-3):
        x_t = self.run(start_time, end_time, start_position, dt)
        grid()
        plot(x_t[:,0], x_t[:,1])
        if len(x_t) > 1:
            arrow(x_t[0, 0], x_t[0, 1], x_t[1, 0] - x_t[0, 0], x_t[1, 1] - x_t[0, 1], shape='full', lw=10, length_includes_head=True, head_width=.05, color='r')

