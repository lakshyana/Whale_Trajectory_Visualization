from mpl_toolkits import mplot3d
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import cm
plt.rcParams["figure.figsize"] = 12.8, 9.6


def read_obj(filename):
    triangles = []
    vertices = []
    with open(filename) as file:
        for line in file:
            components = line.strip(' \n').split(' ')
            if components[0] == "f": # face data
                indices = list(map(lambda c: int(c.split('/')[0]) - 1, components[1:]))
                for i in range(0, len(indices) - 2):
                    triangles.append(indices[i: i+3])
            elif components[0] == "v": # vertex data
                vertex = list(map(lambda c: float(c), components[2:]))
                vertices.append(vertex)
    return np.array(vertices), np.array(triangles)



# Need to verify this is correct rotation
def make_rotation_matrix(head, pitch, roll):
    return np.array([
        [math.cos(head)*math.cos(pitch), -1*math.cos(head)*math.sin(pitch)*math.sin(roll) - math.sin(head)*math.cos(roll), -1*math.cos(head)*math.sin(pitch)*math.cos(roll) + math.sin(head)*math.sin(roll)], 
        [math.sin(head)*math.cos(pitch), -1*math.sin(head)*math.sin(pitch)*math.sin(roll) + math.cos(head)*math.cos(roll), -1*math.sin(head)*math.sin(pitch)*math.cos(roll) - math.cos(head)*math.sin(roll)], 
        [math.sin(pitch), math.cos(pitch)*math.sin(roll), math.cos(pitch)*math.cos(roll)]])


# vertices, triangles = read_obj("whale.obj")
# old_vertices = vertices.copy()
# xx = old_vertices[:,0]
# zz = old_vertices[:,1]
# yy = old_vertices[:,2]
# vertices[:,0] = -xx
# vertices[:,1] = yy
# vertices[:,2] = zz
# # rotation_matrix = make_rotation_matrix(0, 0, math.pi/4)
# # vertices = np.matmul(vertices, rotation_matrix)
# x = vertices[:,0]
# y = vertices[:,1]
# z = vertices[:,2]
# ax = plt.axes(projection='3d')
# ax.set_xlim([-200, 200])
# ax.set_ylim([-200, 200])
# ax.set_zlim([-200, 200])
# ax.set_xticklabels([])
# ax.set_yticklabels([])
# ax.set_zticklabels([])
# x_line, = ax.plot([0, 0], [0, 0], [-300, 300], color='red', label='Head Axis')
# y_line, = ax.plot([0, 0], [-300, 300], [0, 0], color='green', label='Pitch Axis')
# z_line, = ax.plot([-300, 300], [0, 0], [0, 0], color='purple', label='Roll Axis')
# plt.title("Rotation Axes")
# plot = ax.plot_trisurf(x, y, triangles, z, shade=True, color='gray')
# ax.legend()

# plt.savefig('rotation_axes.png')
