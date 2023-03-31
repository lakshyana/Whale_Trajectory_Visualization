import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
import scipy.io
from whale_animation_functions.data_functions.whale_orientation import make_rotation_matrix


def create_whale_trajectory(prh_file, horizontal_x_offset=0, horizontal_y_offset=0, time_offset=0, color='gray'):
    # Create the whale trajectories from the PRH file, using just the head angle for direction.
    whale_data = scipy.io.loadmat(prh_file)

    name = prh_file.split('/')[-1]
    frame_rate = whale_data['fs'][0][0]

    x = [horizontal_x_offset]*(time_offset*frame_rate + 1)
    y = [horizontal_y_offset]*(time_offset*frame_rate + 1)
    z = [0]*(time_offset*frame_rate + 1)

    if 'head' in whale_data.keys():
        for num, i in enumerate(whale_data['head']):
            x.append(x[-1] + math.cos(i[0])*0.2)
            y.append(y[-1] + math.sin(i[0])*0.2)
            z.append(-1 * whale_data['p'][num][0])
        pitch = whale_data['pitch']
        roll = whale_data['roll']
        head = whale_data['head']
    else:
        # TODO: Implement for when not given transformed data, not sure if this is necessary.
        raise ValueError('Need to implement transformation when not given pitch, roll and head explicitly.')

    return {'name': name, 'x': x, 'y': y, 'z': z, 'fs': frame_rate, 'pitch': pitch, 'roll': roll, 'head': head, 'color': color}


def updated_create_whale_trajectory(prh_file, horizontal_x_offset=0, horizontal_y_offset=0, time_offset=0, color='black'):
    # Create the whale trajectories from the PRH file, using rotation matrix to get direction angle.
    whale_data = scipy.io.loadmat(prh_file)

    name = prh_file.split('/')[-1]
    frame_rate = whale_data['fs'][0][0]

    x = [horizontal_x_offset]*(int(time_offset*frame_rate) + 1)
    y = [horizontal_y_offset]*(int(time_offset*frame_rate) + 1)
    z = [0]*(int(time_offset*frame_rate) + 1)
    speed_list = [0]*(int(time_offset*frame_rate) + 1)

    if 'head' in whale_data.keys():
        for i in range(len(whale_data['head'])):
            rotation_matrix = make_rotation_matrix(whale_data['head'][i][0], whale_data['pitch'][i][0], whale_data['roll'][i][0])
            if i != len(whale_data['head']) - 1 and abs(whale_data['pitch'][i][0]) > math.pi/6:
                speed = abs(whale_data['p'][i][0] - whale_data['p'][i+1][0])/math.cos(abs(whale_data['pitch'][i][0]))
            else:
                speed = 0.15
            whale = np.array([speed, 0, 0])
            rotated_whale = np.matmul(whale, rotation_matrix)
            x.append(x[-1] + rotated_whale[0])
            y.append(y[-1] + rotated_whale[1])
            z.append(-1 * whale_data['p'][i][0])
            speed_list.append(speed)
        pitch = whale_data['pitch']
        roll = whale_data['roll']
        head = whale_data['head']
    else:
        # TODO: Implement for when not given transformed data, not sure if this is necessary.
        raise ValueError('Need to implement transformation when not given pitch, roll and head explicitly.')

    return {'name': name, 'x': x, 'y': y, 'z': z, 'fs': frame_rate, 'pitch': pitch, 'roll': roll, 'head': head, 'color': color, 'speed': speed_list}
