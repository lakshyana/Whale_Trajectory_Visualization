from create_full_animation import create_animation

import json
import os
import sys


def generate_single_animations(json_directory, completed_directory):
    '''
    Loops through each animation json set of directions and creates the corresponding animation.
    '''
    for animation_json in os.listdir(json_directory)[:1]:

        current_path = os.path.join(json_directory, animation_json)
        completed_path = os.path.join(completed_directory, animation_json)

        if not os.path.exists(completed_directory):
            os.mkdir(completed_directory)

        print("loading json: {}".format(animation_json))
        with open(current_path) as f:
            animation_info = json.load(f)
            print("loaded json: {}".format(animation_json))

        create_animation(animation_info, debug=True)
        print("created animation: {}".format(animation_json))

        os.rename(current_path, completed_path)

if __name__=="__main__":
    if len(sys.argv) != 3:
        raise ValueError('Expected 2 command line arguments, got {}.'.format(len(sys.argv) - 1))

    generate_single_animations(sys.argv[1], sys.argv[2])

