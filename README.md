# WavePrint: A Simple Audio Fingerprinting and Song Recognition System

WavePrint is a Python-based project that implements a simplified system for recognizing songs from short audio snippets. It utilizes **audio fingerprinting** techniques to convert songs into unique, time-series data points that can be quickly searched and matched against a database.

This project is intended for educational purposes, demonstrating the core concepts behind popular music recognition services such as Shazam.

## Features

  * **Database Generation:** Processes a directory of audio files to create a searchable database of unique audio "fingerprints."
  * **Feature Extraction:** Employs common signal processing techniques (likely based on frequency analysis or spectrograms) to capture the unique characteristics of each song.
  * **Song Matching:** Identifies the original song from a short, clipped audio snippet using correlation analysis.
  * **Demonstration Scripts:** Includes scripts for easily creating the database and testing the recognition system.

## Technical Details

The core functionality of this system relies on three principal components:

1.  **Audio Fingerprinting:** Extracting robust, repeatable features from audio data that remain consistent even when the audio is noisy or truncated.
2.  **Hashing/Indexing:** Storing these features in a structured format (likely a local database or key-value store) for fast retrieval.
3.  **Correlation Analysis:** Comparing the features of an unknown snippet against the database fingerprints to determine the highest match.

### Key Files

| File/Folder | Purpose |
| :--- | :--- |
| `create_database.py` | Python script to ingest audio files from the `Dataset` folder and process them into the `DATABASE` fingerprints. |
| `find_song.py` | The core recognition module, containing functions to process a snippet and search the database for a match. |
| `find_song_demo.py` | A simple script to run a recognition test on a sample snippet from the `song_snippet` folder. |
| `feature_extraction.ipynb`| Jupyter Notebook used for initial development, visualization, and fine-tuning of the feature extraction algorithms. |
| `correlation_plot.png` | An example visualization illustrating how the correlation score aids in identifying the correct match. |
| `Dataset/` | Folder designated for storing the original, full audio files for fingerprinting. |
| `DATABASE/` | Folder containing the generated fingerprint files (the database). |
| `song_snippet/` | Folder containing short audio clips used for testing the recognition capability. |

## Installation and Setup

### Prerequisites

You will require **Python 3.x** and the necessary libraries, which typically include:

  * `numpy`
  * `scipy`
  * `librosa` (highly recommended for audio feature extraction)
  * `matplotlib` (for plotting and visualization)

To install these dependencies, execute the following command:
*(Note: Additional dependencies may be required depending on the specific Python packages utilized.)*

### Step 1: Prepare Your Dataset

1.  Place your full audio files (e.g., MP3, WAV) into the `Dataset/` folder.
2.  Place short clips of those songs into the `song_snippet/` folder for testing.

### Step 2: Create the Database

Execute the database generation script to process your audio files:

```bash
python create_database.py

This script analyzes all files in `Dataset/` and populates the `DATABASE/` folder with unique fingerprints.

### Step 3: Run the Demo

Test the song recognition system using a prepared snippet:

```bash
python find_song_demo.py

The output will display the recognized song title and the correlation score, indicating the system's confidence in the match. 

## Contributing

Contributions are welcome. If you discover bugs, have suggestions for new features (such as different fingerprinting algorithms), or wish to improve performance, please feel free to open an issue or submit a pull request.

1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## License

This project is licensed under the MIT License. Please refer to the repository for the full details of the license.

```bash
pip install numpy scipy librosa matplotlib
