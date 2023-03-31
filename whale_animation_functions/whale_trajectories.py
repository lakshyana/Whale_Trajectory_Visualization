
# This function creates the whale trajectory estimates, which are used to create various movement plots.
import math
import numpy as np
import pandas as pd
import scipy.io

def make_rotation_matrix(head, pitch, roll):
    '''
    Create a rotation matrix based on head, pitch, and roll angles that can be used to obtain the orientation of the whale in 3 dimensions.
    '''
    return np.array([
        [math.cos(head)*math.cos(pitch), -1*math.cos(head)*math.sin(pitch)*math.sin(roll) - math.sin(head)*math.cos(roll), -1*math.cos(head)*math.sin(pitch)*math.cos(roll) + math.sin(head)*math.sin(roll)],
        [math.sin(head)*math.cos(pitch), -1*math.sin(head)*math.sin(pitch)*math.sin(roll) + math.cos(head)*math.cos(roll), -1*math.sin(head)*math.sin(pitch)*math.cos(roll) - math.cos(head)*math.sin(roll)],
        [math.sin(pitch), math.cos(pitch)*math.sin(roll), math.cos(pitch)*math.cos(roll)]])

def create_whale_trajectory(prh_file):
    '''
    This function creates the whale trajectory estimates, which are used to create various movement plots.
    The function reads the PRH file of the whale, creates a rotation matrix based on the head, pitch, and roll angles, and uses it to obtain the 3D orientation of the whale.
    The speed of the whale is computed based on the difference in depth readings between consecutive time steps and the time elapsed between them.
    '''
    # load the PRH file
    whale_data = scipy.io.loadmat(prh_file)

    # file name
    name = prh_file.split('/')[-1]
    # frame rate of the data
    frame_rate = whale_data['fs'][0][0]

    # create empty lists to store the whale trajectory
    x = [0]
    y = [0]
    z = [0]
    speed_list = [0]
    # loop through the data and compute the whale trajectory
    if 'head' in whale_data.keys(): # check if the whale data contains head, pitch, and roll angles
        
        for i in range(len(whale_data['head'])): # len(whale_data['head']) is the number of time steps in the data
            
            # create a rotation matrix based on the head, pitch, and roll angles
            rotation_matrix = make_rotation_matrix(whale_data['head'][i][0], whale_data['pitch'][i][0], whale_data['roll'][i][0])


            # use the rotation matrix to obtain the 3D orientation of the whale
            no_speed_whale = np.array([1, 0, 0]) # unit vector in the x direction
            
            # get a 3D vector representing whale's orientation in space after applying the rotation matrix 
            # the rotation matrix is computed based on the head, pitch, and roll angles of the whale, and is used to 
            # transform the 3D unit vector [1, 0, 0] to the current  orientation of the whale in space
            
            rotated_whale_vector = np.matmul(no_speed_whale, rotation_matrix)
            # rotated whale vector is then used to compute the speed and direction of the whale's movement at each time step


            # compute the speed of the whale
            if i != len(whale_data['head']) - 1 \
                    and abs(math.atan(rotated_whale_vector[2] / (math.sqrt(rotated_whale_vector[0]**2
                                                   + rotated_whale_vector[1]**2)))) > math.pi/6:
                # Checks if the angle is large enough for a dive and computes the speed from the change in depth.
                # p stands for pressure readings to get depth.
                # The difference in pressure is divided by the time between the two readings to get the speed.
                speed_multiplier = abs(whale_data['p'][i][0] - whale_data['p'][i+1][0])/rotated_whale_vector[2]


            else:
                # Assumes the whale moves at 1.5 m/s at the surface if it is not diving. This value can be changed if incorrect.
                speed_multiplier = 1.5/frame_rate

            speed_list.append(speed_multiplier)

            # velocity estimate for the whale
            whale = speed_multiplier * rotated_whale_vector

            x.append(x[-1] + whale[0])
            y.append(y[-1] + whale[1])
            z.append(-1 * whale_data['p'][i][0])

            speed_list.append(speed_multiplier)

        pitch = whale_data['pitch']
        roll = whale_data['roll']
        head = whale_data['head']
        acc = whale_data['Aw']

    else:
        raise ValueError('The implementation for transformation is needed when pitch, roll, and head angles are not given explicitly.')

    return {'name': name,
            'x': x,
            'y': y,
            'z': z,
            'fs': frame_rate,
            'pitch': pitch,
            'roll': roll,
            'head': head,
            'color': 'red',
            'speed': speed_list}

