from trajectory.polynomial import *
import numpy as np

def spline_2d(X, Y, Vx, Vy, T):
    """
    Takes X, Y, Vx, Vy, and Times and returns time, trajectory in x, trajectory in y,
    trajectory dx, and trajectory dy
    """
    time, trajectory_x, trajectory_y, trajectory_dx, trajectory_dy = [], [], [], [], []

    # number of time intervals
    n = len(T)

    # For each time interval
    for i in range(n-1):
        # duration of the interval
        duration = T[i + 1] - T[i]
        # Discretizing time in the interval
        dis_time = np.linspace(0, duration, 100, endpoint=False)

        # Compute the coefficients
        poly_x = poly3_coefficients(X[i], Vx[i], X[i + 1], Vx[i + 1], duration)
        poly_y = poly3_coefficients(Y[i], Vy[i],  Y[i + 1], Vy[i + 1], duration)
        # Evaluate trajectory at each time step of the interval
        traj_xi = evaluate_polynomial3_vector(dis_time, poly_x)
        traj_yi = evaluate_polynomial3_vector(dis_time, poly_y)
        # Evaluate derivative
        traj_dxi = evaluate_derivative_poly3(dis_time, poly_x)
        traj_dyi = evaluate_derivative_poly3(dis_time, poly_y)

        trajectory_x += traj_xi.tolist()
        trajectory_y += traj_yi.tolist()
        trajectory_dx += traj_dxi.tolist()
        trajectory_dy += traj_dyi.tolist()

        # time starts at ti
        dis_time += T[i]
        time = dis_time.tolist()

    return time, trajectory_x, trajectory_y, trajectory_dx, trajectory_dy
