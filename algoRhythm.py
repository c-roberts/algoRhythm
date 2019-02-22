from IPython.display import Audio
import IPython, numpy as np, scipy as sp, matplotlib.pyplot as plt, matplotlib, librosa

def algoRhythm(audio_path, sheet_music, BPM, leniency):
    '''
    Inputs: audio file (.wav), sheet music (.PNG), BPM,
    leninecy (0-5)
    Outputs: score for rhythmic accuracy, timesteps of any errors

    '''
    signal, sr = librosa.load(audio_path, sr=sr)
    


def extract_user_rhythm(signal):
    '''
    Inputs: audio signal (1D np.array)
    Outputs: times (sec) of onsets (1D np.array)

    Uses librosa's onset_detection to extract a 1D np.array
    of the onsets in an audio signal

    '''
    rhythm_arr = librosa.onset.onset_detect(signal, sr=sr, units='time')




    return rhythm_arr


def extract_actual_rhythm(user_tempo):
    '''
    Inputs: user_tempo (BPM)
    Outputs: time (sec) of onsets (1D np.array)

    Extracts actual rhythm from info from PNG and outputs
    a 1D np.array of times of timesteps of onsets
    '''
    return rhythm_act


def compare_rhythm(user_rhythm, actual_rhythm, leniency):
    '''
    Inputs: user's rhythm (np.array of timesteps of onsets), actual
    rhythm (np.array of timesteps of onsets)
    Outputs: score for accuracy (0-100), timesteps of errors (1D np.array)

    '''

    return score, errors
