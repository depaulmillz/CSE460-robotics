import numpy as np
import apis
import time
import sys
import networkx as nx
import os

if __name__ == "__main__":

    x_range = [4.5, 5.2, 5.9, 6.6] #[4.475320816040039, 5.118253231048584, 5.675119400024414, 6.3023295402526855]
    y_range = [-.9, -.2, .5, 1.2, 1.9] #[-0.8638476133346558, -0.28133079409599304,  0.3373686373233795, 0.9117316603660583, 1.538606762886047]

    obstacle_nodes = [1, 10, 14]

    nodes = list()

    pos_to_node_num = dict()

    for x in x_range:
        node_row = list()
        for y in y_range:
            node_row.append([x,y])
        nodes.append(node_row)

    grid = np.array(nodes)

    #print(grid)

    G = nx.Graph()

    def get_node_num(i, j):
        return j * grid.shape[0] + i

    def get_node_weight(i1, j1, i2, j2):
        return np.linalg.norm(grid[i1][j1] - grid[i2][j2])

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if get_node_num(i, j) not in obstacle_nodes:
                G.add_node(j * grid.shape[0] + i, pos=grid[i,j])

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):

            if get_node_num(i, j) not in obstacle_nodes:

                pos_to_node_num[(grid[i][j][0], grid[i][j][1])] = get_node_num(i, j)

                # i, j is next to
                # i + 1, j
                # i - 1, j
                # i, j + 1
                # i, j - 1

                if i + 1 < grid.shape[0] and get_node_num(i + 1, j) not in obstacle_nodes:
                    G.add_edge(get_node_num(i, j), get_node_num(i + 1, j), weight=get_node_weight(i, j, i + 1, j))
                if j + 1 < grid.shape[1] and get_node_num(i, j + 1) not in obstacle_nodes:
                    G.add_edge(get_node_num(i, j), get_node_num(i, j + 1), weight=get_node_weight(i, j, i, j + 1))

    #nx.draw(G)

    #print(pos_to_node_num)

    #sys.exit(0)

    IP_ADDRESS = '192.168.0.207'

    robot = apis.Robot(IP_ADDRESS)

    start_node = 15

    end_node = 13

    path = nx.astar_path(G, start_node, end_node, heuristic = lambda x,y: np.linalg.norm(G.nodes[x]["pos"] - G.nodes[y]["pos"]))

    x_ds = [G.nodes[p]['pos'] for p in path]

    print(x_ds)

    x_f = np.copy(x_ds[0])

    node_count = 0

    print("Starting")
    try:
        # hostname = socket.gethostname()
        # ip_addr = socket.gethostbyname(hostname)
        clientAddress = "192.168.0.126"
        optitrackServerAddress = "192.168.0.172"
        robot_id = 307
        
        # Start up the streaming client now that the callbacks are set up.
        # This will run perpetually, and operate on a separate thread.
        position = apis.Position(clientAddress, optitrackServerAddress, robot_id)

        K1 = 1000
        K2 = 2000
        
        start = time.time()

        init, angle = position.get()

        slope = x_f - init
                
        while True:

            x_t, angle = position.get()

            curr = time.time() - start

            if curr > 3.0:
                node_count += 1
                if node_count >= len(x_ds):
                    #node_count = len(x_ds) - 1
                    slope = np.array([0.0, 0.0])
                    init = x_ds[len(x_ds) - 1]
                    start = time.time()
                    curr = time.time() - start
                else:
                    x_f = x_ds[node_count]
                    print(x_f)
                    slope = x_f - x_t
                    init = x_t
                    start = time.time()
                    curr = time.time() - start

            x_d = (curr / 3.0) * (slope) + init

            dist, desiredAngle = apis.dist_and_angle(x_d, x_t)

            v = K1 * dist
            angleDiff = apis.angle_diff(desiredAngle, angle)
            omega = K2 * angleDiff

            u = np.array([v - omega, v + omega])
            u[u > 1500.] = 1500.
            u[u < -1500.] = -1500.
            
            robot.set_motor(u[0], u[0], u[1], u[1])
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Shutting down")
        pass
    
    robot.stop_motor()
    robot.shutdown()
    print("Done")
    os._exit(0)
