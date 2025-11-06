from feature_extract.read_utils import prep_audio
from feature_extract.analysis_utils import cfar, detect_peaks
import os
from numpy import savetxt

PATH = "Dataset/ONE_OK_ROCK_SAVE_YOURSELF_OFFICIAL_VIDEO_Fueled_By_Ramen.wav"
song_name = os.path.splitext(os.path.basename(PATH))[0]

song, sxx, t_spec,f = prep_audio(PATH,fs = 10000, plot_spectrogram=False)
print(len(song))

song_feat = cfar(sxx)
song_cfar_marker = detect_peaks(song_feat, t_spec, f, slices = (10,30), selection_ratio=2e-4, plot=False, sr = 44100)

output_filename = f"DATABASE/{song_name}.csv"

savetxt(output_filename, song_cfar_marker, delimiter=",", fmt='%d')
print(f"The song {song_name} saved successfully!")
print(song_cfar_marker.shape)