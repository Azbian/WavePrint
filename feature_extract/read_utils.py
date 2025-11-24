import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import librosa  

def prep_audio(FILE_PATH, fs=44100, plot_spectrogram=False, **kwargs):
    try:
       
        y, sr = librosa.load(FILE_PATH, sr=fs, mono=True)
   

        print(f"Successfully loaded file. Target Sampling Rate (sr): {sr} Hz")
        print(f"Signal length: {y.shape[0]} samples")

    except FileNotFoundError:
        print(f"Error: Audio file not found at {FILE_PATH}")
        return None, None, None, None  # Return None instead of crashing
    except Exception as e:
        print(f"Error reading audio file: {e}")
        return None, None, None, None  # Return None

    

    nperseg_val = int(sr * 0.04)   # Segment length (e.g., 40ms)
    noverlap_val = int(sr * 0.02)  # Overlap length (e.g., 20ms)

    f, t_spec, Sxx = signal.spectrogram(
        y,
        fs=sr,
        window='hann',
        nperseg=nperseg_val,
        noverlap=noverlap_val,
        scaling='density'
    )

    # Add a check for silence to avoid division by zero
    max_sxx = np.max(Sxx)
    if max_sxx == 0:
        print("Warning: Audio appears to be silent. Spectrogram is empty.")
        Sxx_db = np.full_like(Sxx, -100.0) # Fill with -100dB
    else:
        Sxx = Sxx / max_sxx  # Normalize Sxx to [0, 1]
        # Use a small epsilon to avoid log(0)
        Sxx = np.maximum(Sxx, 1e-10)
        Sxx_db = 10 * np.log10(Sxx)

    if plot_spectrogram:
        plt.figure(figsize=(12, 6))
        plt.pcolormesh(t_spec, f, Sxx_db, shading='gouraud', cmap='viridis')
        plt.title('Spectrogram of Audio File (Power Spectral Density)')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.colorbar(label='Intensity [dB]')
        plt.ylim(0, sr / 2) # Show frequencies up to the Nyquist frequency
        plt.tight_layout()
        plt.show()
    
    # 'y' is now the loaded, resampled, mono audio data
    song = y

    return song, Sxx, t_spec, f
