# UniversalDownloader

Universal Downloader is a Python application built with yt-dlp and customtkinter that allows users to download videos and audio from various sources. The app provides an intuitive GUI where users can paste URLs, select download formats, and track download progress. It also includes automatic codec conversion to H.264, if needed, to improve video compatibility.

![DA54E5D3-7128-48FB-91CA-B26C76EAA076](https://github.com/user-attachments/assets/4d4a7325-aad5-4599-9e5c-f54d9d5b52e7)

## Features

- Download videos and audio with selectable formats.
- Automatic conversion of video files to H.264 codec for better compatibility.
- Visual download progress and estimated time display.
- Simple, dark-themed interface built with customtkinter.

## Prerequisites

To run Universal Downloader, you’ll need:

- Python 3.7+

- ffmpeg and ffprobe: Required for video processing and codec conversion.

## Installation

1. Clone the repository:

```
git clone https://github.com/Iosif-Christogeorgos/UniversalDownloader.git
```

```
cd universal-downloader
```

2. Install dependencies: Install the necessary packages from requirements.txt:

```
pip install -r requirements.txt
```

3. Download ffmpeg and ffprobe:

- Visit the [FFmpeg download page](https://www.ffmpeg.org/download.html#build-windows) to download the latest version.

- Extract the downloaded folder, and copy ffmpeg.exe and ffprobe.exe to the same directory as main.py.

## Usage

1. Run the application:

```
python main.py
```

2. Paste the video URL in the input box.

3. Select a download format from the dropdown:

- Video+Audio: Downloads the full video with audio.
- Audio-Only: Downloads only the audio as an MP3.

4. Press "Download". The app will display progress and an estimated time remaining.

## Example Use Case

If a video is not already in the H.264 codec, the app will automatically convert it upon download, ensuring compatibility with most players.

## Files Overview

**main.py**: The main script for running the application.

**YTDLPLogger.py**: Logger for tracking download progress.

**requirements.txt**: Lists required Python packages.

**ffmpeg.exe and ffprobe.exe**: Place these files in the project root for video processing (required but not included in the repository).

## Dependencies

**yt-dlp**: For video and audio downloading.

**customtkinter**: For the graphical user interface.

**tkinter**: Core library for UI elements (comes with Python).

**ffmpeg and ffprobe**: For handling video codec conversion and metadata extraction.

## Notes

- **Codec Conversion**: The application checks if the downloaded video is in H.264 format. If not, it converts it automatically.

- **Progress Tracking**: Download progress and estimated time are updated in real-time.

- **Compatibility**: Tested on Windows (additional OS compatibility can be added based on testing).
