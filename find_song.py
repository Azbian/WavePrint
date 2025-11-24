from pandas import read_csv
import numpy as np
from feature_extract.analysis_utils import cfar, detect_peaks
from feature_extract.read_utils import prep_audio
import matplotlib.pyplot as plt
import scipy.signal as sig


song_cfar_marker = read_csv("DATABASE/oh_lord.csv", header=None).values

# snippet start time 38 sec end time 52 sec
snippet_path = "song_snippet/snippet2.wav"
snippet, sxx, t_spec, f = prep_audio(snippet_path, fs=10000)
snippet_marker = cfar(sxx)
snippet_cfar_marker = detect_peaks(snippet_marker, t_spec, f, selection_ratio=0.01, plot=True)

# This is the key to converting your result to seconds.
# We find the time duration of a single frame from the t_spec array.
time_per_frame = 0.0
if len(t_spec) > 1:
    time_per_frame = t_spec[1] - t_spec[0]
    print(f"Calculated time per frame: {time_per_frame:.4f} seconds")
else:
    print("Warning: Could not determine time per frame. Time output will be in frames.")
# --- End of new code ---


# now taking the cross correlation between the song the song snippet
correlation_output = sig.correlate2d(song_cfar_marker, snippet_cfar_marker, mode='valid')

# --- 3. Plot the Correlation Result ---
plt.figure(figsize=(10, 6))
plt.imshow(correlation_output, cmap='hot', aspect='auto')
plt.title('2D Cross-Correlation Result')
plt.xlabel('Time Offset (frames)')
plt.ylabel('Frequency Offset (bins)')
plt.colorbar(label='Correlation Score')


# --- 4. Find the Peak Programmatically ---
# The plot is great for visuals, but your code needs the *location* of the peak.
# We find the (row, col) of the highest value in the correlation output.
peak_loc = np.unravel_index(np.argmax(correlation_output), correlation_output.shape)

# --- MODIFIED: Calculate offsets in bins, frames, and seconds ---
freq_offset_bins = peak_loc[0]
time_offset_frames = peak_loc[1]

# This is the final conversion you asked for
time_offset_seconds = time_offset_frames * time_per_frame
# --- End of modified code ---


# --- MODIFIED: Final Print Output ---
# Print the results in a more readable format, including seconds.
print(f"\nShape of database song map: {song_cfar_marker.shape}")
print(f"Shape of query snippet map: {snippet_cfar_marker.shape}")
print(f"Shape of correlation output: {correlation_output.shape}")
correlation_peak = np.argmax(correlation_output)

print(f"\nMatch Found!")
print(f"Highest correlation peak found:{correlation_peak}")
#print(f"  Frequency Bin Offset: {freq_offset_bins} bins")
#print(f"  Time Frame Offset:    {time_offset_frames} frames")
print(f"  ==> Snippet starts at: {time_offset_seconds:.2f} seconds into the song.")

plt.show()
