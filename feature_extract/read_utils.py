import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.signal import resample

def prep_audio(FILE_PATH,fs = 44100,plot_spectrogram=False, **kwargs):
    try:
        # Read the WAV file:
        # sr: Sampling rate (e.g., 44100 Hz)
        # data: Audio signal data (a NumPy array)
        sr, data = wavfile.read(FILE_PATH)

        tar_sr = fs
        num_tar_sample = int(len(data)*tar_sr/sr)
        data = resample(data, num_tar_sample)
        sr= tar_sr

        print(f"Successfully loaded file. Sampling Rate (sr): {sr} Hz")
        
        # If the audio is stereo (2 channels), use only the first channel (mono)
        if data.ndim > 1:
            y = np.mean(data, axis=1)  # Take the mono
            print("Note: Converted stereo audio to mono (left channel).")
        else:
            y = data

        
        print(f"Signal length: {y.shape[0]} samples")


    except FileNotFoundError:
        print(f"Error: WAV file not found at {FILE_PATH}")
        exit()
    except Exception as e:
        print(f"Error reading WAV file: {e}")
        exit()


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

    Sxx = Sxx/np.max(Sxx)  # Normalize Sxx to [0, 1]

    Sxx_db = 10 * np.log10(Sxx, out=np.full_like(Sxx, -100.0), where=Sxx>0)

    if plot_spectrogram:
        plt.figure(figsize=(12, 6))


        plt.pcolormesh(t_spec, f, Sxx_db, shading='gouraud', cmap='viridis')

        plt.title('Spectrogram of WAV Audio File (Power Spectral Density)')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.colorbar(label='Intensity [dB]')
        plt.ylim(0, sr / 2) # Show frequencies up to the Nyquist frequency
        plt.tight_layout()
        plt.show()
    
    song = data

    return song, Sxx, t_spec, f