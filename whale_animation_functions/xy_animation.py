# Plots an overhead view of the whales movement.
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

def animate_xy(x, y, frame_rate, start_time, end_time, save_path):

    def init():
        line.set_data([], [])
        return line,
    
    def animate(i):
        ax.set_xlim(cropped_x[i]-20, cropped_x[i]+20)
        ax.set_ylim(cropped_y[i]-20, cropped_y[i]+20)
        line.set_data([cropped_x[i]], [cropped_y[i]])
        return line,


    cropped_x = x[int(frame_rate*start_time) : int(frame_rate*end_time)]
    cropped_y = y[int(frame_rate*start_time) : int(frame_rate*end_time)]

    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(111)
    ax.set_xlim(cropped_x[0]-20, cropped_x[0]+20)
    ax.set_ylim(cropped_y[0]-20, cropped_y[0]+20)

    plot = ax.plot(cropped_x, cropped_y, color='orange')

    ax.set_title('XY Movement')
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    line, = ax.plot([], [], marker='o', markersize=20, color='black')

    anim = animation.FuncAnimation(fig, animate, init_func=init, fargs=None, 
							frames=len(cropped_x), interval=(1/frame_rate)*1000, blit=True)

    anim.save(save_path)