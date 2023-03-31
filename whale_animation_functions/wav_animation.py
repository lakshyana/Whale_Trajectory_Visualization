# Plots the wav file, and lines corresponding to where clicks are annotated.
import librosa
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import math
import soundfile as sf
import numpy as np
from numpy import genfromtxt


import csv

def get_file_lenghts():
    # Correction for annotated time (time since tag was started) to time in the split audio file.
    file_lengths = dict()
    with open('../wav_file_durations_2014_2015_2016.csv') as csv_file:
        rowreader = csv.DictReader(csv_file)
        for row in rowreader:
            file_lengths[row['File Name'].split('/')[-1]] = int(row['Duration (Seconds)'])
    return file_lengths


def get_clicks(whale_name):
    # Goes in to the annotated data and finds when the clicks are happening.
    my_data = genfromtxt('../coda_metadata.csv', delimiter=',',dtype=None,encoding="utf8")
    clicks = {}
    for i in range(1,my_data.shape[0]):
        file_name = str(my_data[i,1][:9])
        if file_name == whale_name:
            whale_number = int(my_data[i, 46])
            coda_start_time = float(my_data[i,48])
            click_times = []
            power = []


            click_times.append(coda_start_time)
            power.append(float(my_data[i,92]))
            j = 4
            while (float(my_data[i,j]) != 0): 
                if float(my_data[i,j])> 0.0002:  # To ignore mistakes in annotations
                    click_times.append(coda_start_time + np.sum(my_data[i,4:(j+1)].astype(float)))
                j = j+1
            if whale_number in clicks:
                clicks[whale_number] += click_times
            else:
                clicks[whale_number] = click_times
    return clicks


def animate_wav_file(wav_file, start_time, end_time, save_path, cropped_wav_path, anim_width=8):
    # The actual animation generation code, just does a sliding window over the audio plot.
    def init():
        line.set_data([0, 0], [min_sig, max_sig])
        return line,
    
    def animate(i):
        ax.set_xlim(i/10 - 2, i/10 + 6)
        line.set_data([i/10, i/10], [min_sig, max_sig])
        return line,

    (sig_full, rate) = librosa.load(wav_file, sr=None)

    sig = sig_full[int(rate*start_time): int(rate*end_time)]
    sf.write(cropped_wav_path, sig, rate)

    whale_name = wav_file[:9]
    global_click_times = get_clicks(whale_name)
    file_number = int(wav_file[6:9])
    if file_number > 1:
        offset_time = 0
        file_lengths = get_file_lenghts()
        for i in range(1, file_number):

            offset_time += file_lengths['{}00{}.flac'.format(wav_file[:6], i)]
    click_times = [click_time - offset_time for click_time in global_click_times]

    ylim = max(max(sig), max(-sig))

    fig = plt.figure(figsize=(anim_width, 4))
    ax = fig.add_subplot(111)

    ax.set_title('Hydrophone Audio')
    ax.set_ylabel("Audio Signal")

    ax.set_ylim(-ylim, ylim)

    plot = ax.plot([i/rate for i in range(len(sig))], sig, color='orange')
    min_sig, max_sig = (-2, 2)
    line, = ax.plot([0, 0], [min_sig, max_sig], color='blue')
    for click_time in click_times:
        _, = ax.plot([click_time, click_time], [min_sig, max_sig], color='red')

    anim = animation.FuncAnimation(fig, animate, init_func=init, fargs=None, 
							frames=(len(sig)//rate)*10, interval=100, blit=True)

    anim.save(save_path)
