import os
from pandas import read_csv
from feature_extract.analysis_utils import cfar, detect_peaks
from feature_extract.read_utils import prep_audio
import matplotlib.pyplot as plt
import scipy.signal as sig
import numpy as np
import playsound


data_base = "DATABASE"

def find_song():
    pass

#loading the song snippet
snippet_path = "song_snippet/snippet2.wav"

snippet, sxx, t_spec, f = prep_audio(snippet_path, fs=10000)
snippet_marker = cfar(sxx)
snippet_cfar_marker = detect_peaks(snippet_marker, t_spec, f, selection_ratio=0.01, plot=False)


best_match = 0
song_name = " "
for filename in os.listdir(data_base):
    file_path = os.path.join(data_base, filename)
    if os.path.isfile(file_path):
        song_cfar_marker = read_csv(file_path, header=None).values
        correlation_output = sig.correlate2d(song_cfar_marker,snippet_cfar_marker, mode="valid")
        correlation_peak = np.max(correlation_output)
        if correlation_peak>best_match:
            best_match = correlation_peak
            song_name = os.path.splitext(filename)[0]

playsound.playsound(snippet_path)
print(f"!! Best match found with the song:  {song_name}")




        