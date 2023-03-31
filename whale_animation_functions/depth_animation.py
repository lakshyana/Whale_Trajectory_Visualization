# Rolling window showing the depth of the whale.
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

def animate_depth(depth, frame_rate, start_time, end_time, save_path, anim_width=8):

    def init():
        line.set_data([], [])
        return line,
    
    def animate(i):
        ax.set_xlim(i/10 - 20, i/10 + 60)
        line.set_data([i/10, i/10], [min_depth, max_depth])
        return line,


    plot_depth = depth[int(frame_rate*start_time) : int(frame_rate*(end_time+60))]
    min_depth, max_depth = (min(-600, min(depth)), 20)

    fig = plt.figure(figsize=(anim_width, 4))
    ax = fig.add_subplot(111)
    ax.set_ylim(min_depth, max_depth)

    plot = ax.plot([i/frame_rate for i in range(len(plot_depth))], plot_depth, color='blue')

    ax.set_title('Depth')
    ax.set_ylabel('Depth (m)')

    line, = ax.plot([0, 0], [min_depth, max_depth], color='green')

    anim = animation.FuncAnimation(fig, animate, init_func=init, fargs=None, 
							frames=int(frame_rate*end_time) - int(frame_rate*start_time), interval=(1/frame_rate)*1000, blit=True)

    anim.save(save_path)
