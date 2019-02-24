from IPython.display import Audio
import IPython, numpy as np, scipy as sp, matplotlib.pyplot as plt, matplotlib, librosa

def algoRhythm(audio_path, sheet_music, BPM, rhythm_leniency, pitch_leniency):
    '''
    Inputs: audio file (.wav), sheet music (.PNG), BPM,
    leninecy (0-5)
    Outputs: score for rhythmic accuracy, timesteps of any errors

    '''
    # Initialize files and globals
    signal, sr = librosa.load(audio_path, sr=None)
    actual_signal = extract_sheet_music(sheet_music)
    create_freq_dict()


    # Extract rhythm from user and from sheet music
    user_rhythm = extract_user_rhythm(signal)
    actual_rhythm = extract_actual_rhythm(actual_signal, BPM)


    # Extract pitch from user and from sheet music
    user_pitch = extract_user_pitch(signal)
    actual_pitch = extract_actual_pitch(actual_signal)


    # Compare user and correct rhythm
    rhythm_score, rhythm_errors = compare_rhythm(user_rhythm, actual_rhythm, rhythm_leniency)
    pitch_score, pitch_errors = compare_pitch(user_pitch, actual_pitch, pitch_leniency)

    return



###################################
##      utilities for rhythm     ##
###################################


def extract_user_rhythm(signal):
    '''
    Inputs: audio signal (1D np.array)
    Outputs: times (sec) of onsets (1D np.array)

    Uses librosa's onset_detection to extract a 1D np.array
    of the onsets in an audio signal

    '''
    rhythm_arr = librosa.onset.onset_detect(signal, sr=sr, units='time')
    raise NotImplementedError('Function not implemented.')
    return rhythm_arr


def extract_actual_rhythm(actual_signal, user_tempo):
    '''
    Inputs: user_tempo (BPM), signal of actual audio from sheet music (1D np.array)
    Outputs: time (sec) of onsets (1D np.array)

    Extracts actual rhythm from info from PNG and outputs
    a 1D np.array of times of timesteps of onsets
    '''
    raise NotImplementedError('Function not implemented.')
    return rhythm_act


def compare_rhythm(user_rhythm, actual_rhythm, leniency):
    '''
    Inputs: user's rhythm (np.array of timesteps of onsets), actual
    rhythm (np.array of timesteps of onsets)
    Outputs: score for accuracy (0-100), timesteps of errors (list)

    '''
    errors = []
    score=0
    raise NotImplementedError('Function not implemented.')

    return score, errors

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
    Inputs: user pitch (bertz)

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

