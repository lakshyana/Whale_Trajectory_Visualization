import csv
import json
import math
import numpy as np
import os

from numpy import genfromtxt 

#**********************************************************
'''
Code in here is to read in the annotated audio data, and get click times, speakers, and what movement (PRH) files they correspond to.
'''
def parseCoda(i, book):
    if i==-1:
        return [0,0,0,0,0,0]
    coda = book[i,:]
    whale_number = coda[0].astype(int)
    t_init = coda[1]    

    click_times = coda[2:42].astype(float).tolist()
    num_clicks = np.count_nonzero(click_times)+1
    click_times = click_times[0:num_clicks]

    average_power = coda[84]
    click_power = coda[43:83].astype(float).tolist()
    click_power = np.array(click_power[0:num_clicks])

    return [whale_number,t_init,num_clicks,click_times,average_power,click_power]


# Process the coda metadata csv file
def get_codas_and_prh():
    my_data = genfromtxt('coda_metadata.csv', delimiter=',',dtype=None,encoding="utf8")

    annotations = {}

    for i in range(1,my_data.shape[0]):
        file_name = str(my_data[i,1][:9]) #get the file name from the REC column
        annotations[file_name] = [] #create a new entry in the dictionary for each file name

    for i in range(1, my_data.shape[0]): #iterate over each row in the data and extract relevant data
        file_name = str(my_data[i,1][:9]) #get the file name from the REC column
        whale_number = int(my_data[i, 46]) #get the whale number from the Whale column
        coda_start_time = float(my_data[i,48])  #get the coda start time from the Tsto column
        avg_power = float(my_data[i,91]) #get the average power from the average Pw column
        click_times = []
        power = []
        click_times.append(0) #get the whale number from the Whale column
        power.append(float(my_data[i,92])) #get the first power value from the Pw1 column
        j = 4 #index of ICI1 column in the csv file

        while (float(my_data[i,j]) != 0): # get the rest of the click times and powers
            if float(my_data[i,j])> 0.0002:  # To ignore mistakes in annotations
                click_times.append(np.sum(my_data[i, 4:(j+1)].astype(float)) ) # sum the values in the columns
                # #row i, columns j through j+1
                # j:j+1].astype(float)) #sum the values in the columns
                power.append(my_data[i,j+89].astype(float))
            j = j+1
        annotations[file_name].append([click_times, coda_start_time, whale_number, power, avg_power])

    books = []
    for key in annotations.keys():
        story = annotations[key] # each entity is a line of a coda
        book = np.zeros((len(story),85))
        for j in range(len(story)):
            book[j,0] = story[j][2] # Whale number
            book[j,1] = story[j][1] # Coda start time
            book[j,2:len(story[j][0])+2] = story[j][0] # Click times
            book[j,43:len(story[j][3])+43] = story[j][3] # Powers
            if len(story[j][0])==41:
                book[j,83] = story[j][3][-1] # Duplicating the last column when num of icis is 41
            book[j,84] = story[j][4]
        books.append((book,key))

    edited = []
    for i in range(len(books)):
        book = books[i][0]
        sorted_array = book[np.argsort(book[:, 1])] # sort by coda start time
        edited.append((sorted_array,books[i][1])) # append the sorted array and the file name

    edited = sorted(edited, key=lambda book: book[1])

    prh_directory = './data/PRH_all/PRH/'

    prh_files = [os.path.join(prh_directory, o) for o in os.listdir(prh_directory)]

    prh_dict = {}
    for i in range(len(prh_files)):
        loc = prh_files[i]
        name = 'sw'+os.path.basename(loc)[5:9]

        prh_dict[name] = loc

    return edited, prh_dict

# Get file lenghts for each audio file
def get_file_lengths(csv_path):
    '''
    This gets the file lengths, so that we can 'undo' the file splitting and 
    match up audio times to movement times (since movement files were not split).
    '''
    file_lengths = dict()
    with open(csv_path) as csv_file:
        rowreader = csv.DictReader(csv_file)
        for row in rowreader:
            file_lengths[row['File Name'].split('/')[-1]] = int(row['Duration (Seconds)'])
    return file_lengths

def convert_prh_time_to_audio_time(name, time, file_lengths):
    '''
    This function does the correction to match up audio and movement times.
    '''
    sample_rate = 22050
    file_number = int(name[6:9])
    time_to_subtract = 0
    for i in range(1, file_number):
        time_to_subtract += file_lengths['{}{}{}.wav'.format(name[:6], '0'*(3 - len(str(i))), i)]
    return time - time_to_subtract/sample_rate

#**********************************************************

def make_animation_jsons(all_codas, prh_dict
                         # , file_lengths
                         ):
    '''
    Creates a folder of json files, which contain:
        - prh_file: the movement file location 
        - wav_file: the audio file location
        - save_directory: where the generated animations will be saved
        - animation_start: the timestep in the movement file where the animation will start
        - wav_start: the timestep in the wav file where the audio will start
        - animation_end: the timestep in the movement file where the animation will end
        - wav_end: the timestep in the wav file where the audio will end
    '''

    if not os.path.exists('conversation_animation_jsons'):
        os.mkdir('conversation_animation_jsons')

    for file_codas, name in all_codas:
        new_file = True
        latest_coda_start = 0
        convo_num = 1

        for i in range(file_codas.shape[0]):
            [whale_number, t_init, num_clicks, click_times, average_power, click_power] = parseCoda(i, file_codas)

            if latest_coda_start + 30 < t_init and not new_file:
                whale_json['animation_end'] = latest_coda_start + 30
                # whale_json['wav_end'] = convert_prh_time_to_audio_time(name, latest_coda_start + 30, file_lengths)
                with open(os.path.join('conversation_animation_jsons', '{}_{}.json'.format(name, convo_num)), 'w') as outfile:
                    json.dump(whale_json, outfile)
                convo_num += 1
                new_file = True

            latest_coda_start = t_init

            if new_file:
                whale_json = {}
                whale_json['prh_file'] = prh_dict[name[0:6]]

                whale_json['save_directory'] = '{}_{}'.format(name, convo_num)
                whale_json['animation_start'] = max(t_init - 30, 0)
                # whale_json['wav_start'] = convert_prh_time_to_audio_time(name, max(t_init - 30, 0), file_lengths)

                new_file = False

        whale_json['animation_end'] = latest_coda_start + 30
        # whale_json['wav_end'] = convert_prh_time_to_audio_time(name, latest_coda_start + 30, file_lengths)
        with open(os.path.join('conversation_animation_jsons', '{}_{}.json'.format(name, convo_num)), 'w') as outfile:
            json.dump(whale_json, outfile)


all_codas, prh_dict = get_codas_and_prh()
csv_path = 'wav_file_durations_2014_2015_2016.csv'
make_animation_jsons(all_codas, prh_dict)
