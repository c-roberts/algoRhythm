from IPython.display import Audio
import IPython, numpy as np, scipy as sp, matplotlib.pyplot as plt, matplotlib, librosa
from librosa import display
import os, ly

standard_sr = 44100

def algoRhythm(audio_path, sheet_music, bpm, rhythm_leniency):
    '''
    Inputs: audio file (.wav), sheet music (.PNG), BPM,
    leniency (0-5)
    Outputs: score for rhythmic accuracy, timesteps of any errors

    '''
    # Initialize files and globals
    signal, sr = librosa.load(audio_path, sr=None)
    #actual_signal = extract_sheet_music(sheet_music)
    #create_freq_dict()

    # Extract rhythm from user and from sheet music
    user_rhythm = extract_user_rhythm(signal, sr)
    actual_rhythm = extract_actual_rhythm(sheet_music, bpm)

    # Compare user rhythm with correct rhythm
    rhythm_score, rhythm_errors = compare_rhythm(user_rhythm, actual_rhythm, rhythm_leniency)

    # Plot user rhythm against correct rhythm over time
    plot_bpm_over_time(user_rhythm, actual_rhythm, sr)

    # Plot onsets of user signal against the correct beat placements
    plot_performance(signal, actual_rhythm, sr)

    return rhythm_score, rhythm_errors


### Plotting functions ###

def plot_bpm_over_time(user, actual, sr):
    onset_env_user = librosa.onset.onset_strength(user, sr=sr)
    onset_env_actual = librosa.onset.onset_strength(actual, sr=sr)
    user_rhythm = librosa.beat.tempo(onset_envelope=onset_env_user, sr=sr, aggregate=None)
    actual_rhythm = librosa.beat.tempo(onset_envelope=onset_env_actual, sr=sr, aggregate=None)

    plt.figure(figsize=(8, 4))
    tg = librosa.feature.tempogram(onset_envelope=onset_env_actual, sr=sr)
    librosa.display.specshow(tg, x_axis='time', y_axis='tempo')
    user_time = librosa.frames_to_time(np.arange(len(user_rhythm)))
    actual_time = librosa.frames_to_time(np.arange(len(actual_rhythm)))
    plt.plot(user_time, user_rhythm, color='r', linewidth=1.5, label='User Signal')
    plt.plot(actual_time, actual_rhythm, color='g', linewidth=1.5, label='Actual Signal')
    plt.title('User BPM vs Target BPM Over Time')
    plt.legend(frameon=True)
    plt.show()


def plot_performance(user, actual, sr):
    onset_env_user = librosa.onset.onset_strength(user, sr=sr, aggregate=np.median)
    onset_env_actual = librosa.onset.onset_strength(actual, sr=sr, aggregate=np.median)
    user_rhythm, user_beats = librosa.beat.beat_track(onset_envelope=onset_env_user, sr=sr)
    actual_rhythm, actual_beats = librosa.beat.beat_track(onset_envelope=onset_env_actual, sr=sr)
    nrms = np.sqrt(((user_rhythm - actual_rhythm) ** 2).mean()) / np.mean(actual_rhythm)

    plt.figure(figsize=(8, 4))
    user_onset_times = librosa.frames_to_time(np.arange(len(onset_env_user)), sr=sr)
    actual_onset_times = librosa.frames_to_time(np.arange(len(onset_env_actual)), sr=sr)
    plt.plot(user_onset_times, librosa.util.normalize(onset_env_user), label='User Signal')
    plt.vlines(actual_onset_times[actual_beats], 0, 1, alpha=0.6, color='r', linestyle='--', label='Target Beats')
    plt.title('User Signal vs Target Beats')
    plt.legend(frameon=True)
    plt.show()

    return user_rhythm, actual_rhythm, nrms


###################################
##      utilities for rhythm     ##
###################################


def extract_user_bpm(signal):
    '''
    Inputs: audio signal (1D np.array)
    Outputs: estimated bpm of user signal

    Uses librosa's onset_detection to extract a 1D np.array
    of the onsets in an audio signal

    '''
    sr = standard_sr
    rhythm_arr = librosa.onset.onset_detect(signal, sr=sr, units='time')

    return rhythm_arr


def extract_user_rhythm(signal, sr):
    '''
    Inputs: audio signal (1D np.array)
    Outputs: times (sec) of onsets (1D np.array)

    Uses librosa's onset_detection to extract a 1D np.array
    of the onsets in an audio signal

    '''
    rhythm_arr = librosa.onset.onset_detect(signal, sr=sr, units='time')
    
    return rhythm_arr


def extract_actual_rhythm(filepath, user_tempo):
    '''
    Inputs: user_tempo (BPM), signal of actual audio from sheet music (1D np.array)
    Outputs: time (sec) of onsets (1D np.array)

    Extracts actual rhythm from info from PNG and outputs
    a 1D np.array of times of timesteps of onsets
    '''
    
    data = filepath
    #skip header information
    start = data.find('PartPOneVoiceOne') 
    #improper file type
    if start == -1:
        raise ValueError('Improper File Format. File is not Monophonic')
        
    #adjust start to begin at PPOVO node
    start +=  16
    while data[start] != '{':
        start += 1
        
    PPOVO = data[start:(len(data)-1)]
    
    #parse through to find note section
    onset_times = parse_PPOVO(user_tempo, PPOVO)
    
    return onset_times


def ly_onsets(bpm, data):
    '''
    INPUTS:
        bpm: beats per minute integer
        data: string of ly file
    --------------------------------
    RETURNS:
        onset_times: array of floats for time stamps ground truth onsets
    '''
    # skip header information
    start = data.find('PartPOneVoiceOne')
    # improper file type
    if start == -1:
        raise ValueError('Improper File Format. File is not Monophonic')

    # adjust start to begin at PPOVO node
    start += 16
    while data[start] != '{':
        start += 1

    PPOVO = data[start:(len(data) - 1)]

    # parse through to find note section
    onset_times = parse_PPOVO(bpm, PPOVO)

    return onset_times


def xml_to_ly(filepath, p = False):
    '''
    INPUTS: 
    filepath
    '''
    file = './dataset/'+filepath
    cmd = 'musicxml2ly -a '+file
    returned_value = os.system(cmd)
    if returned_value != 0:
        raise ValueError('File Not Found')
    if p ==  True:
        print('returned value:', returned_value)


def ly_to_text(filepath):
    '''
    INPUTS:    
        filepath: string to file path of .ly file
    -----------------------------------------
    RETURNS:
        data: string of encoded text from .ly file
    '''
    ly_file = filepath
    with open(ly_file, encoding='cp1252') as f: #Might have to change encoding depending on how the mac version is
        data = f.read()
    return data


def parse_PPOVO(bpm, PPOVO):
    '''
    INPUTS:
        bpm: beats per minute integer
        PPOVO: string of ly file containing note information
    --------------------------------
    RETURNS:
        onset_times: array of all float ground truth onset times
    '''
    time = 0.0
    onset_times = []
    prev = None
    i = 0
    #TODO ADD TRIPLET/TUPLE PARSING
    while i < len(PPOVO)-1:
        #c -> current char in .ly text
        c = PPOVO[i]
        c_next = PPOVO[i+1]
        c_next_dig = c_next.isdigit()
        if(c == "'" or (c == "r" and c_next_dig)): #note or rest found
            
            #add note onset
            if(c == "'"):
                onset_times.append(time)
            
            #parse through note length indicator
            while(c == "'"):
            #increment start to skip note indicator
                i += 1
                c = PPOVO[i]
                              
            
            #buffer to get note value
            buffer = ""
            #keep going until total note len is found (1,2,4,8th,16th,32th note etc)
            while (c.isdigit()):
                buffer+=c
                i+=1
                c = PPOVO[i]
            #convert buffer to int to get note typet
            if(buffer != ""):
                note_val = int(buffer)
                duration = note_to_seconds(bpm, note_val)
                time+=duration
        i+=1
            
    return onset_times


def note_to_seconds(bpm, note_val):
    '''
    INPUTS:
        beats per minute integer
        note_val: type of note in float
            1.0 = whole note
            0.5 = half note
            etc...

    -------------------------------
    RETURNS:
        duration: note duration in seconds
    '''
    duration = (60.0/bpm) * (1.0/note_val)
    return duration


def calculate_delta_time(onsets):
    '''
    Inputs: onsets from user signal or sheet music rhythm
    Outputs: difference in time from each onset to the next
    '''
    d_time = np.zeros(onsets.shape)
    for i in range(1, onsets.size-1, 1):
        d_time[i] = onsets[i] - onsets[i-1]

    return d_time


def compare_rhythm(user_rhythm, actual_rhythm, leniency):
    """
    Inputs: user's rhythm (np.array of timesteps of onsets), actual
    rhythm (np.array of timesteps of onsets)
    Outputs: score for accuracy (0-100), timesteps of errors (list)

    """
    errors = []

    diff = actual_rhythm.size - user_rhythm.size # extra or missing notes

    # calculate delta_time and align first note to zero
    d_user = calculate_delta_time(user_rhythm)
    d_actual = calculate_delta_time(actual_rhythm)

    for i in range(1, d_actual.size):
        if d_actual[i]-leniency < d_user[i] < d_actual[i]+leniency:
            # correct, move on
            #print("noice", i)
            print()

        else:
            # add timestep to errors
            #print("BAD", i)
            errors.append(user_rhythm[i])

            # try to figure out if extra
            # not implemented

    score = 100 - (len(errors) / actual_rhythm.size) * 100

    return score, errors


def search_onsets(onsets, lo, hi):
    """
    Binary search helper function to get user onset closest to target onset

    Inputs: array of onsets, lower leniency bound, upper leniency bound
    Outputs: array index of user onset closest to target onset, whether user onset is within leniency range
    """

    l = 0
    r = len(onsets) - 1

    while l <= r:

        m = int(l + (r - l) / 2)

        if lo <= onsets[m] <= hi:
            return m, True

        elif onsets[m] < hi:
            l = m + 1

        else:
            r = m - 1

    return m - 1, False


def compare_onsets(user_signal, actual_signal, leniency):
    '''
    Inputs: user signal, actual signal, leniency for error
    Outputs: evaluation score based on number of correctly placed onsets,
             error of user onset in seconds,
             timesteps of user onset errors
    '''
    user_onsets = librosa.onset.onset_detect(user_signal, sr=standard_sr, units='time')
    actual_onsets = librosa.onset.onset_detect(actual_signal, sr=standard_sr, units='time')

    # align first onset to time 0
    # user_onsets = np.subtract(user_onsets, user_onsets[0])
    # actual_onsets = np.subtract(actual_onsets, actual_onsets[0])

    error_margins = []
    error_timestamps = []
    last_ind = 0
    for i in range(1, len(actual_onsets)):
        # aligned = user_onsets[(user_onsets >= actual_onsets[i]-leniency) & (user_onsets <= actual_onsets[i]+leniency)]
        # if len(aligned) > 0:
        # if at least than one user onset is detected to fall within the leniency region around the actual onset
        #    error_margins.append(0)

        closest_onset = search_onsets(user_onsets, actual_onsets[i]-leniency, actual_onsets[i]+leniency)
        if closest_onset[1]: # if onset is within leniency range
            error_margins.append(0)
        else:
            ind = closest_onset[0]
            if ind != last_ind:
                error_timestamps.append(round(user_onsets[ind], 2))
                error_margins.append(round(user_onsets[ind] - actual_onsets[i], 2))
            last_ind = ind

    score = 100 - (len(error_timestamps) / actual_onsets.size) * 100

    return score, error_margins, error_timestamps


def extract_sheet_music(sheet_music):
    '''
    Inputs: sheet music (PNG)
    Outputs: audio signal of sheet music (1D np.array)

    Extracts midi from PNG and convert that to an audio signal
    '''
    raise NotImplementedError('Function not implemented.')
    return actual_signal


##################################
##      utilities for pitch     ##
##################################


def extract_user_pitch(signal):
    '''
    Inputs: audio signal (1D np.array)
    Outputs: fundamental freq at each sample (1D np.array)

    Extracts freq (hertz) of user's note at each sample from audio signal

    '''
    raise NotImplementedError('Function not implemented.')
    return pitch_arr


def extract_actual_pitch(actual_signal):
    '''
    Inputs: audio signal (1D np.array)
    Outputs: fundamental freq at each sample (1D np.array)

    Extracts freq (hertz) of actual note at each sample from audio signal

    '''
    raise NotImplementedError('Function not implemented.')
    return pitch_arr


def compare_pitch(user_pitch, actual_pitch, pitch_leniency):
    '''
    Inputs: user's pitch (np.array of fundamental freq at each sample), actual
    rhythm (np.array of fundamental freq at each sample)
    Outputs: score for accuracy (0-100), timesteps of errors (list)

    '''
    errors = []
    score=0
    raise NotImplementedError('Function not implemented.')
    return score, errors


def create_freq_dict(tuning_pitch=440):
    '''
    Inputs: tuning pitch of A4 (default=440)
    Outputs: 2D list [name,freq]

    Runs on startup and everytime the user changes the value of A4

    '''
    global freq_chart
    global notes
    freq_chart=[]
    
    notes = [	"C0","C#0","D0","D#0","E0","F0","F#0","G0","G#0","A0","A#0","B0",
                "C1","C#1","D1","D#1","E1","F1","F#1","G1","G#1","A1","A#1","B1",
                "C2","C#2","D2","D#2","E2","F2","F#2","G2","G#2","A2","A#2","B2",
                "C3","C#3","D3","D#3","E3","F3","F#3","G3","G#3","A3","A#3","B3",
                "C4","C#4","D4","D#4","E4","F4","F#4","G4","G#4","A4","A#4","B4",
                "C5","C#5","D5","D#5","E5","F5","F#5","G5","G#5","A5","A#5","B5",
                "C6","C#6","D6","D#6","E6","F6","F#6","G6","G#6","A6","A#6","B6",
                "C7","C#7","D7","D#7","E7","F7","F#7","G7","G#7","A7","A#7","B7",
                "C8","C#8","D8","D#8","E8","F8","F#8","G8","G#8","A8","A#8","B8",
                "C9","C#9","D9","D#9","E9","F9","F#9","G9","G#9","A9","A#9","B9" ]
    
    A4_INDEX = 57

    for i in range(0, len(notes)-1,1):
        distance = i - A4_INDEX
        freq = tuning_pitch * (2 ** (distance/12))
        freq_chart.append([notes[i], freq])
    
    return


def get_cent_diff(user_pitch):
    '''
    Inputs: frequency of user's note
    Outputs: difference from closest in-tune freq (cents)

    Calculates the difference between closest in-tune freq and user's freq
    by finding closest pitch and calculating the difference in cents
    '''

    # find the closest freq from freq_chart (min distance)
    cent_diff=0
    actual_pitch=freq_chart[find_closest(user_pitch)][1]
 
    cent_diff=1200* np.log(user_pitch/actual_pitch)/np.log(2)

    return cent_diff


def find_closest(pitch):
    '''
    Inputs: user pitch (hertz)

    Returns index of closest in-tune pitch
    '''
    min_distance=abs(float( freq_chart[0][1] - pitch ))
    for index in range(1,len(freq_chart)-1,1):
        cur_distance = abs(float( freq_chart[index][1] - pitch ))
        if (min_distance <= cur_distance):
            break
        else:
            min_distance = cur_distance
        
    return (index-1)


### Testing functions ###

def test1():
    '''
    my_signal, sr = librosa.load("Testing Data/test5.wav", sr=None)
    test=extract_user_rhythm(my_signal)
    print(test)
    d_test= calculate_delta_time(test)
    print(d_test)
    test_xml = extract_actual_rhythm("./Testing Data/test5.xml", 120)
    print(test_xml)
    '''
    audio_path = "./Testing Data/User Ex1 - 80bpm correct.wav"
    sheet_music = "./Testing Data/User Ex1 score.xml"
    bpm=80
    rhythm_leniency = .5

    signal, sr = librosa.load(audio_path, sr=None)

    user_rhythm = extract_user_rhythm(signal, sr)
    #print(user_rhythm)
    #actual_rhythm = extract_actual_rhythm(sheet_music, bpm)
    incorrect, sr = librosa.load( "./Testing Data/User Ex1 - 80bpm incorrect1.wav", sr=None)
    #print(actual_rhythm)
    incorrect_rhythm = extract_user_rhythm(incorrect, sr)
    #print(incorrect_rhythm)
    rhythm_score, rhythm_errors = compare_rhythm(user_rhythm, incorrect_rhythm, rhythm_leniency)

    print("\n\n------------ Results ------------")
    print("\nIncorrect length: " + str(incorrect_rhythm.size))
    print("Correct length: " + str(user_rhythm.size))
    print("Rhythm Score: " + str(rhythm_score))
    print("Number of errors: " + str(len(rhythm_errors)))


    #test_score, test_errors = algoRhythm(audio_path, sheet_music, bpm, rhythm_leniency)


def test2():
    path = './Testing Data/'
    correct = '/User Ex1 - 80bpm correct.wav'
    incorrect = '/User Ex1 - 80bpm incorrect1.wav'
    signal, sr = librosa.load(path + correct)
    actual_signal, sr = librosa.load(path + incorrect)
    bpm = 80
    user_rhythm = extract_user_rhythm(signal, sr)
    actual_rhythm = extract_user_rhythm(actual_signal, sr)

    # Compare user rhythm with correct rhythm
    rhythm_leniency = .05
    #rhythm_score, rhythm_errors = compare_rhythm(user_rhythm, actual_rhythm, rhythm_leniency)
    score, error_margins, error_timestamps = compare_onsets(signal, actual_signal, rhythm_leniency)
    print('Error margins per onset:', error_margins)
    print('Timesteps of Errors:', error_timestamps)
    print('Score:', score)

    # Plot user rhythm against correct rhythm over time
    plot_bpm_over_time(signal, actual_signal, sr)

    # Plot onsets of user signal against the correct beat placements
    user_bpm, target_bpm, nrmse = plot_performance(signal, actual_signal, sr)
    print('User BPM:', round(user_bpm, 1))
    print('Target BPM:', round(target_bpm, 1))
    print('Normalized Root Mean Squared Error:', round(nrmse, 3))


### Run tests ###

test2()