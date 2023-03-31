
"""

This file contains the function to create a zoomed out animation of the whale trajectory.

By creatin a 3D animation of a whale's trajectory based on the data in `whale_info`.

The function `create_zoomed_out_animation()` takes as input the `whale_info` dictionary,
    which should contain the whale's x, y, and z coordinates over time,
     as well as the start and end times for the animation,
    and a save path for the output animation file.

The function first extracts a subset of the whale's coordinates corresponding to the specified time range,
    with a step size of 25.
    It then creates a 3D scatter plot of the whale's trajectory using the extracted coordinates,
     with the color of each point representing the depth of the whale.
      The function also creates an empty line object that will be used to visualize the whale's current position in the animation.

The `animate()` function is defined to update the position of the `line` object at each time step,
 based on the current index `i`. The `index` variable is set to `i` to account for the step size of 25
 used to extract the subset of coordinates. The `xdata`, `ydata`, and `zdata` variables are then updated to
 contain the current position of the whale, based on the coordinates at the current index. The `line` object is
  then updated with the new position data, and returned along with the updated scatter plot.

The `init()` function simply returns an empty line object to initialize the animation.

The `FuncAnimation` class from the `matplotlib.animation` module is used to create the animation, with the `animate()`
function as the update function and the `init()` function as the initialization function. The `frames` argument is set
 to the length of the `x` array, and the `interval` argument is set to the time between frames in milliseconds,
  calculated as `(1/whale_info['fs'])*1000`. The resulting animation is then saved to the specified `save_path`.

Overall, this function generates a 3D animation of a whale's trajectory based on sensor data,
 providing a visualization of the whale's movement over time.
"""



# Plot 3D visualization of the entire whale trajectory.
import matplotlib.pyplot as plt 
import matplotlib.animation as animation 
import numpy as np


def create_zoomed_out_animation(whale_info,
                                start_time,
                                end_time,
                                save_path):

    def init(): 
	    line.set_data([], [])
	    return line, 

    def animate(i): 
        index = i
        xdata = np.array([x[index]])
        ydata = np.array([y[index]])
        zdata = np.array([z[index]])
        line.set_data(xdata, ydata)
        line.set_3d_properties(zdata)
        return line, 

    xdata, ydata = [], []

    # Extract a subset of the whale's coordinates corresponding to the specified time range, with a step size of 25.
    x_full = whale_info['x'][max(0, int(whale_info['fs']*(start_time
    # -900 is used to add a buffer to the start and end times of the animation, so that the whale is not at the
                                                          # edge of the plot at the beginning and end of the animation.
                                                          - 900))):min(len(whale_info['x']), int(whale_info['fs']*(end_time
    # +900 is used to add a buffer to the start and end times of the animation, so that the whale is not at the

                                                                                                                   + 900))):
                             # 25 is the step size used to extract the subset of coordinates.
                             25]

    y_full = whale_info['y'][max(0, int(whale_info['fs']*(start_time - 900))):min(len(whale_info['y']), int(whale_info['fs']*(end_time + 900))):25]  
    z_full = whale_info['z'][max(0, int(whale_info['fs']*(start_time - 900))):min(len(whale_info['z']), int(whale_info['fs']*(end_time + 900))):25]

    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title('Whale Trajectory')

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])

    # Create a 3D scatter plot of the whale's trajectory using the extracted coordinates, with the color of each point
    scatter = ax.scatter(x_full, y_full, z_full, c=z_full, cmap=plt.get_cmap('autumn'), s=5)
    fig.colorbar(scatter, label='Depth')




    x = whale_info['x'][int(whale_info['fs']*start_time): int(whale_info['fs']*end_time)]
    y = whale_info['y'][int(whale_info['fs']*start_time): int(whale_info['fs']*end_time)]
    z = whale_info['z'][int(whale_info['fs']*start_time): int(whale_info['fs']*end_time)]

    # Create an empty line object that will be used to visualize the whale's current position in the animation.
    line, = ax.plot([], [], [], marker='o', markersize=20, color=whale_info['color']) 

    # Create the animation.
    anim = animation.FuncAnimation(fig, animate, init_func=init, fargs=None, 
							frames=len(x), interval=(1/whale_info['fs'])*1000, blit=True)
    
    anim.save(save_path)




"""
This snippet is used to extract a subset of the whale's x, y, and z coordinates, which are used to create the 3D scatter plot of the whale's trajectory in the animation.

The code uses the `max()` and `min()` functions to ensure that the start and end indices for the coordinate arrays are within the bounds of the data. It first calculates the start and end indices based on the `start_time` and `end_time` arguments, respectively, using the `int()` function to convert the time values to integer indices. The `whale_info['fs']` value represents the sampling rate of the sensor data, and is used to convert the time values to indices.

The `max()` function is used to ensure that the start index is not less than zero (i.e., the beginning of the data), and the `min()` function is used to ensure that the end index is not greater than the length of the coordinate arrays. The `900` value represents a buffer of 900 seconds (15 minutes) added to the start and end times, to provide some additional context for the animation.

Finally, the `:25` notation at the end of each line is used to extract every 25th element of the coordinate arrays, to reduce the number of points in the scatter plot and improve performance.

Overall, this snippet is used to extract a subset of the whale's coordinates that will be used to create the 3D scatter plot of the whale's trajectory in the animation. The extracted coordinates are limited to a specific time range and reduced in frequency to reduce the number of points in the scatter plot.
"""