import os
import glob  # <-- Import glob to find files
from numpy import savetxt
from feature_extract.read_utils import prep_audio
from feature_extract.analysis_utils import cfar, detect_peaks

# --- Configuration ---
DATASET_FOLDER = "Dataset"
DATABASE_FOLDER = "DATABASE"
TARGET_FS = 10000  # Define your sample rate as a variable

# --- 1. Ensure the output DATABASE folder exists ---
if not os.path.exists(DATABASE_FOLDER):
    os.makedirs(DATABASE_FOLDER)
    print(f"Created output folder: {DATABASE_FOLDER}")

# --- 2. Find all audio files to process ---
# This will find all files ending in .mp3 or .wav in your Dataset folder
search_paths = [
    os.path.join(DATASET_FOLDER, "*.mp3"),
    os.path.join(DATASET_FOLDER, "*.wav")
]

song_files_to_process = []
for path in search_paths:
    song_files_to_process.extend(glob.glob(path))

if not song_files_to_process:
    print(f"Error: No .mp3 or .wav files found in '{DATASET_FOLDER}'")
else:
    print(f"Found {len(song_files_to_process)} songs to process.")

# --- 3. Loop through each file and process it ---
for file_path in song_files_to_process:
    print(f"\n--- Processing: {file_path} ---")
    
    try:
        # Get the song name (e.g., "Demons") from the path
        song_name = os.path.splitext(os.path.basename(file_path))[0]

        # Process the audio
        song, sxx, t_spec, f = prep_audio(file_path, fs=TARGET_FS, plot_spectrogram=False)
        
        # Check if prep_audio returned successfully
        if song is None:
            print(f"Skipping {file_path}, could not be prepped.")
            continue # Move to the next song

        print(f"Loaded '{song_name}', length: {len(song)} samples")

        # Extract features
        song_feat = cfar(sxx)
        
        # Detect peaks
        # Note: I changed 'sr=44100' to 'sr=TARGET_FS'
        # Assuming the 'sr' param should match your prep_audio 'fs'
        song_cfar_marker = detect_peaks(song_feat, t_spec, f, slices=(10, 30), selection_ratio=2e-4, plot=False, sr=TARGET_FS)

        # Define the output CSV file path
        output_filename = f"{DATABASE_FOLDER}/{song_name}.csv"

        # Save the feature array to the CSV
        savetxt(output_filename, song_cfar_marker, delimiter=",", fmt='%d')
        
        print(f"SUCCESS: '{song_name}' saved to '{output_filename}'")
        print(f"Feature map shape: {song_cfar_marker.shape}")

    except Exception as e:
    
        print(f"!!! ERROR processing {file_path}: {e} !!!")
        print("Continuing to the next file...")

print("\n--- Batch processing complete. ---")