import matplotlib.pyplot as plt 
import matplotlib.animation as animation

import math

def animate_orientation(pitch, head, roll, frame_rate, start_time, end_time, save_path, anim_width=8):

    def init():
        line.set_data([], [])
        return line,
    
    def animate(i):
        ax.set_xlim(i/10 - 20, i/10 + 60)
        line.set_data([i/10, i/10], [min_angle-10, max_angle+10])
        return line,

    plot_pitch = pitch[int(frame_rate*start_time) : int(frame_rate*(end_time+60))]
    plot_head = head[int(frame_rate*start_time) : int(frame_rate*(end_time+60))]
    plot_roll = roll[int(frame_rate*start_time) : int(frame_rate*(end_time+60))]

    # Correct radians to degrees.
    plot_pitch = [i*180/math.pi for i in plot_pitch]
    plot_head = [i*180/math.pi for i in plot_head]
    plot_roll = [i*180/math.pi for i in plot_roll]

    min_angle, max_angle = (min(plot_pitch) - 5, max(plot_pitch) + 5)

    fig = plt.figure(figsize=(anim_width, 4))
    ax = fig.add_subplot(111)
    ax.set_ylim(min_angle, max_angle)

    # One set of axes for pitch, since it has a smaller range.
    plot1 = ax.plot([i/frame_rate for i in range(len(plot_pitch))], plot_pitch, color='green', label='Pitch')
    ax.set_ylabel('Pitch Angle (degrees)', color='green')
    ax.tick_params(axis='y', labelcolor='green')

    ax2 = ax.twinx()
    # Other axis for Head and Roll which have the same range.
    plot2 = ax2.plot([i/frame_rate for i in range(len(plot_head))], plot_head, color='red', label='Head')
    plot3 = ax2.plot([i/frame_rate for i in range(len(plot_roll))], plot_roll, color='purple', label='Roll')
    ax2.set_ylabel('Head and Roll Angle (degrees)', color='purple')
    ax2.tick_params(axis='y', labelcolor='red')

    ax2.legend()

    ax.set_title('PRH')

    line, = ax.plot([0, 0], [min_angle, max_angle], color='green')

    anim = animation.FuncAnimation(fig, animate, init_func=init, fargs=None, 
							frames=int(frame_rate*end_time) - int(frame_rate*start_time), interval=(1/frame_rate)*1000, blit=True)

    anim.save(save_path)
