
from whale_animation_functions.whale_trajectories import create_whale_trajectory
from whale_animation_functions.animation_zoomed_out import create_zoomed_out_animation
from whale_animation_functions.xy_animation import animate_xy
from whale_animation_functions.orientation_animation import animate_orientation
from whale_animation_functions.depth_animation import animate_depth
from whale_animation_functions.animation_zoomed_in_whale import create_zoomed_in_animation
# from whale_animation_functions.wav_animation import animate_wav_file

import json
import subprocess
import sys
import os

def create_animation(animations_info, debug=False):

    if debug:
        print('Creating animations...')

    save_directory = os.path.join('conversation_animations', animations_info['save_directory'])

    if not os.path.exists('upload'):
        os.mkdir('upload')

    if not os.path.exists('task_jsons'):
        os.mkdir('task_jsons')

    if not os.path.exists('conversation_animations'):
        os.mkdir('conversation_animations')

    if not os.path.exists(save_directory):
        os.mkdir(save_directory)

    prh_file_name = animations_info['prh_file'].split('/')[-1]
    if prh_file_name[-6:-4] != '10':
        return  # These ones do not have the correct head/pitch/roll computed so can't visualize.

    year = '20{}'.format(prh_file_name[2:4])

    # animations_info['wav_file'] = './data/{}/{}'.format(year, animations_info['wav_file'])

    whale_info = create_whale_trajectory(animations_info['prh_file'])

    print("whale_info: ")

    for key in whale_info:
        print(key)
        print(whale_info[key])

    # Create all of the individual components of the visualization.

    # if debug:
    #     print('Creating wav animation...')

    # cropped_wav_path = os.path.join(save_directory, '{}.flac'.format(animations_info['save_directory']))

    # animate_wav_file(animations_info['wav_file'], animations_info['wav_start'], animations_info['wav_end'], os.path.join(save_directory, 'wav_file_animation.mp4'), cropped_wav_path)

    if debug:
        print('Creating zoomed out animation...')

    create_zoomed_out_animation(whale_info, animations_info['animation_start'],
                                animations_info['animation_end'],
                                os.path.join(save_directory, 'zoomed_out_animation.mp4'))

    if debug:
        print('Creating zoomed in animation...')

    create_zoomed_in_animation(whale_info,
                               animations_info['animation_start'],
                               animations_info['animation_end'],
                               os.path.join(save_directory, 'zoomed_in_animation.mp4'))

    if debug:
        print('Creating XY animation...')

    animate_xy(whale_info['x'], whale_info['y'], whale_info['fs'],
               animations_info['animation_start'],
               animations_info['animation_end'],
               os.path.join(save_directory, 'xy_animation.mp4'))

    if debug:
        print('Creating orientation animation...')

    animate_orientation(whale_info['pitch'], whale_info['head'], whale_info['roll'],
                        whale_info['fs'],
                        animations_info['animation_start'],
                        animations_info['animation_end'],
                        os.path.join(save_directory, 'orientation_animation.mp4'))

    if debug:
        print('Creating depth animation...')
    animate_depth(whale_info['z'],
                  whale_info['fs'],
                  animations_info['animation_start'],
                  animations_info['animation_end'],
                  os.path.join(save_directory, 'depth_animation.mp4'))

    # Merge all of the videos to make one big visualizations

    merge_command = 'ffmpeg -i {} -i {} -filter_complex "[0:v][1:v]hstack" {}'.format(os.path.join(save_directory, 'zoomed_out_animation.mp4'),
                                                                                      os.path.join(save_directory, 'zoomed_in_animation.mp4'), os.path.join(save_directory, 'top.mp4'))
    res = subprocess.call(merge_command, shell=True)
    print("top.mp4 created.")

    # merge_command = 'ffmpeg -i {} -i {} -filter_complex "[0:v][1:v]hstack" {}'.format(os.path.join(save_directory, 'zoomed_in_animation.mp4'), os.path.join(save_directory, 'orientation_animation.mp4'), os.path.join(save_directory, 'middle.mp4'))
    # res = subprocess.call(merge_command, shell=True)
    # print("middle.mp4 created.")

    merge_command = 'ffmpeg -i {} -i {} -filter_complex "[0:v][1:v]hstack" {}'.format(os.path.join(save_directory, 'xy_animation.mp4'), os.path.join(save_directory, 'depth_animation.mp4'), os.path.join(save_directory, 'bottom.mp4'))
    res = subprocess.call(merge_command, shell=True)
    print("bottom.mp4 created.")

    merge_command = 'ffmpeg -i {} -i {} -filter_complex "[0:v][1:v]scale2ref=oh*mdar:ih[1v];[0:v][1v]vstack" {}'.format(os.path.join(save_directory, 'top.mp4'), os.path.join(save_directory, 'orientation_animation.mp4'), os.path.join(save_directory, 'temp.mp4'))
    res = subprocess.call(merge_command, shell=True)
    print("temp.mp4 created.")

    merge_command = 'ffmpeg -i {} -i {} -filter_complex "[0:v][1:v]scale2ref=oh*mdar:ih[1v];[0:v][1v]vstack" {}'.format(os.path.join(save_directory, 'temp.mp4'), os.path.join(save_directory, 'bottom.mp4'), os.path.join(save_directory, 'merged_animation.mp4'))
    res = subprocess.call(merge_command, shell=True)
    print("merged_animation.mp4 created.")

    # merge_command = 'ffmpeg -i {} -i {} -filter_complex "[0:v][1:v]scale2ref=oh*mdar:ih[1v];[0:v][1v]vstack" {}'.format(
    #     os.path.join(save_directory, 'top.mp4'), os.path.join(save_directory, 'middle.mp4'),
    #     os.path.join(save_directory, 'temp.mp4'))




    # merge_command = 'ffmpeg -i {} -i {} -c:v copy -c:a aac {}'.format(os.path.join(save_directory, 'merged_animation.mp4'), cropped_wav_path, os.path.join('upload', '{}.mp4'.format(animations_info['save_directory'])))
    # res = subprocess.call(merge_command, shell=True)

    task_json = {'video': '<video src=\'http://visiongpu10.csail.mit.edu:8080/upload/{}.mp4\' width=75% muted /><img src onerror="$=n=>document.getElementsByTagName(n)[0];a=$(\'audio\');v=$(\'video\');a.onseeked=()=>{{v.currentTime=a.currentTime}};a.onplay=()=>v.play();a.onpause=()=>v.pause()" />'.format(animations_info['save_directory']),
                 'audioSource': 'http://visiongpu10.csail.mit.edu:8080/upload/{}.mp4'.format(animations_info['save_directory'])}

    with open(os.path.join('task_jsons', '{}_task.json'.format(animations_info['save_directory'])), 'w') as outfile:
        json.dump(task_json, outfile)

    # os.remove(os.path.join(save_directory, 'temp.mp4'))
    # os.remove(os.path.join(save_directory, 'top.mp4'))
    # os.remove(os.path.join(save_directory, 'middle.mp4'))
    # os.remove(os.path.join(save_directory, 'bottom.mp4'))

    return