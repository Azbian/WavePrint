import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve1d


def cfar(data, guard_len = 10, train_len = 100, p_fa = 0.05, order='F', **kwargs):
    r, c = data.shape
    data = data.flatten(order =order)
    a = train_len*(p_fa**(-1/train_len) - 1)
    cfar_kernel = np.ones((1 + 2*guard_len + 2*train_len), dtype=float) / (2*train_len)
    cfar_kernel[train_len: train_len + (2*guard_len) + 1] = 0.
    gaurd_cells = np.zeros_like(cfar_kernel)
    gaurd_cells[train_len: train_len + (2*guard_len) + 1] = cfar_kernel[0]
    gaurd_cells[len(gaurd_cells)//2] = 0.
    cut = np.zeros_like(cfar_kernel)
    cut[len(gaurd_cells)//2] = cfar_kernel[0]

    noise_level = convolve1d(data, cfar_kernel, mode='nearest')
    threshold = noise_level * a
    detected = data > threshold
    detected = detected.reshape(r, c, order='F')

    return detected

def detect_peaks(data, t_spec, f, slices = (10,30), selection_ratio=2e-4, plot=False, sr = 44100):
    rows, cols = data.shape
    window_cols = cols//slices[1]
    window_rows = rows//slices[0]
    print(f"Window size: {window_rows} rows")
    print(f"Window size: {window_cols} columns")
    marker = np.zeros_like(data)
    for j in range(0, rows - window_rows, window_rows):

        for i in range(0, cols - window_cols, window_cols):
            window = data[j:j+window_rows, i:i + window_cols]
            k = int(window.size*selection_ratio)
            top_value_indexes = np.argpartition(window.flatten(), -k)[-k:]
            top_values = window.flatten()[top_value_indexes]
            non_zero_mask = top_values > 0
            top_value_indexes = top_value_indexes[non_zero_mask]
            r, c = np.unravel_index(top_value_indexes, window.shape)
            marker[r + j, c + i] = 1

    if plot:
        row_indices, col_indices = np.where(marker == 1)
        freq_coords = f[row_indices]
        time_coords = t_spec[col_indices]

        plt.figure(figsize=(12, 6))
        plt.pcolormesh(t_spec, f, data, shading='gouraud', cmap='gray')
        plt.scatter(time_coords, freq_coords, c='red', s=10)
        plt.title('Detected Peaks in Spectrogram')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        #plt.ylim(0, sr / 2) # Show frequencies up to the Nyquist
        plt.tight_layout()
        plt.show()
        
    return marker

def main():
    pass

if __name__ ==  "__main__":
    main()