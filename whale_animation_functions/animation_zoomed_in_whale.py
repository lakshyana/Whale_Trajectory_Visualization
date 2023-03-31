# This is the most complex one of all of the animation. It needs to orient the whale and then have orientation lines coming out to mark up/down, left/right, front/back.
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from whale_animation_functions.data_functions.whale_orientation import read_obj, make_rotation_matrix

import math
import numpy as np


def create_zoomed_in_animation(whale_info, start_time, end_time, save_path):

    def init():  # Initialize the plot
        x = vertices[:,0]
        y = vertices[:,1]
        z = vertices[:,2]
        plot = ax.plot_trisurf(x, y, triangles, z, shade=True, color='gray') # Create a plot_trisurf object
        return plot,

    def animate(i): # Update the plot for each frame of the animation
        index = i # Get the index of the current frame
        ax.clear() # Clear the plot and set various properties
        ax.set_title('Whale Orientation')
        ax.set_xlim([-350, 350])
        ax.set_ylim([-350, 350])
        ax.set_zlim([-350, 350])
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])

        rotation_matrix = make_rotation_matrix(head[index], pitch[index], roll[index]) # Calculate the rotation matrix based on the pitch, roll, and head of the whale at the current frame
        new_vertices = np.matmul(vertices, rotation_matrix) # Apply the rotation matrix to the vertices of the 3D model
        x = new_vertices[:,0]
        y = new_vertices[:,1]
        z = new_vertices[:,2]
        plot = ax.plot_trisurf(x, y, triangles, z, shade=True, color='gray') # Create a plot_trisurf object with the new vertices

        # Add in lines coming out of the whale to show orientation.
        x_line_points_top = np.array([400, 0, 0])
        y_line_points_top = np.array([0, 400, 0])
        z_line_points_top = np.array([0, 0, 400])
        rotated_x_line_points_top = np.matmul(x_line_points_top, rotation_matrix) # Apply the rotation matrix to the points of the lines
        rotated_y_line_points_top = np.matmul(y_line_points_top, rotation_matrix)
        rotated_z_line_points_top = np.matmul(z_line_points_top, rotation_matrix)

        x_line_points_bottom = np.array([-400, 0, 0])
        y_line_points_bottom = np.array([0, -400, 0])
        z_line_points_bottom = np.array([0, 0, -400])

        rotated_x_line_points_bottom = np.matmul(x_line_points_bottom, rotation_matrix) # Rotate the end points of the up/down lines using the rotation matrix
        rotated_y_line_points_bottom = np.matmul(y_line_points_bottom, rotation_matrix)
        rotated_z_line_points_bottom = np.matmul(z_line_points_bottom, rotation_matrix)

        # Create plot objects for the up/down, left/right, and front/back lines
        x_line, = ax.plot([rotated_x_line_points_bottom[0], rotated_x_line_points_top[0]], [rotated_x_line_points_bottom[1], rotated_x_line_points_top[1]], [rotated_x_line_points_bottom[2], rotated_x_line_points_top[2]], color='purple')
        y_line, = ax.plot([rotated_y_line_points_bottom[0], rotated_y_line_points_top[0]], [rotated_y_line_points_bottom[1], rotated_y_line_points_top[1]], [rotated_y_line_points_bottom[2], rotated_y_line_points_top[2]], color='green')
        z_line, = ax.plot([rotated_z_line_points_bottom[0], rotated_z_line_points_top[0]], [rotated_z_line_points_bottom[1], rotated_z_line_points_top[1]], [rotated_z_line_points_bottom[2], rotated_z_line_points_top[2]], color='red')
        # Add markers at the endpoints of the up/down lines to indicate the top and bottom of the whale
        top_marker, = ax.plot([rotated_z_line_points_top[0], rotated_z_line_points_top[0]+1], [rotated_z_line_points_top[1], rotated_z_line_points_top[1]+1], [rotated_z_line_points_top[2], rotated_z_line_points_top[2]+1], color='black', markersize=100)
        bottom_marker, = ax.plot([rotated_z_line_points_bottom[0], rotated_z_line_points_bottom[0]+1], [rotated_z_line_points_bottom[1], rotated_z_line_points_bottom[1]+1], [rotated_z_line_points_bottom[2], rotated_z_line_points_bottom[2]+1], color='orange', markersize=100)
        
        # Add a circle in the XY plane of whale frame to show orientation.
        circle_x = [i*10 for i in range(-35, 36)]
        circle_x = circle_x + circle_x[::-1]
        circle_y = [math.sqrt(122500 - i**2) for i in circle_x[:71]] + [-math.sqrt(122500 - i**2) for i in circle_x[71:]]
        circle_z = [0 for i in circle_x]
        circle_combined = np.array([circle_x, circle_y, circle_z]).transpose()
        rotated_circle = np.matmul(circle_combined, rotation_matrix)
        circle, = ax.plot(rotated_circle[:,0], rotated_circle[:,1], rotated_circle[:,2], color='black')

        return plot, x_line, y_line, z_line, top_marker, bottom_marker, circle


    pitch = whale_info['pitch']
    roll = whale_info['roll']
    head = whale_info['head']

    pitch = pitch[int(whale_info['fs']*start_time): int(whale_info['fs']*end_time)]
    roll = roll[int(whale_info['fs']*start_time): int(whale_info['fs']*end_time)]
    head = head[int(whale_info['fs']*start_time): int(whale_info['fs']*end_time)]

    # Read in the whale object and make corrections for orientation.
    vertices, triangles = read_obj('whale.obj')
    old_vertices = vertices.copy()
    xx = old_vertices[:,0]
    zz = old_vertices[:,1]
    yy = old_vertices[:,2]
    vertices[:,0] = -xx
    vertices[:,1] = yy
    vertices[:,2] = zz

    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title('Whale Orientation')

    ax.set_xlim([-350, 350])
    ax.set_ylim([-350, 350])
    ax.set_zlim([-350, 350])

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])

    anim = animation.FuncAnimation(fig, animate, init_func=init, fargs=None, 
							frames=len(pitch), interval=(1/whale_info['fs'])*1000, blit=True)

    anim.save(save_path)
