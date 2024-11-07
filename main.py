import yt_dlp
import customtkinter as ctk
from tkinter import messagebox
from YTDLPLogger import YTDLPLogger
import threading
import time
import subprocess
import os

start_time = time.time()

# appearance preferences
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# initialize window
window = ctk.CTk()
window.geometry("640x360")
window.resizable(False, False)
window.title("Universal Downloader")
window.iconbitmap("download.ico")

# entry variables
display_var = ctk.StringVar()
optionvar = ctk.StringVar()


def is_h264_codec(input_file):
    # Ensure file exists before running the check
    if not os.path.isfile(input_file):
        print(f"File '{input_file}' does not exist.")
        return False

    # FFprobe command to get codec information
    ffprobe_cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=codec_name",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        input_file,
    ]

    try:
        # FFprobe command and capture the codec name
        codec = subprocess.check_output(ffprobe_cmd, text=True).strip()
        return codec == "h264"
    except subprocess.CalledProcessError as e:
        print("Error checking codec:", e)
        return False


def convert_codec_to_h264(input_file):
    output_file = os.path.splitext(input_file)[0] + "_h264.mp4"
    ffmpeg_cmd = [
        "ffmpeg",
        "-i",
        input_file,
        "-c:v",
        "libx264",
        "-crf",
        "18",
        output_file,
    ]
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        os.remove(input_file)
        print("converted!")
    except subprocess.CalledProcessError as e:
        print("error", e)


def update_ui(text):
    progress_report.configure(text=text)


frame = ctk.CTkFrame(window)
frame.grid(row=4, column=0, columnspan=2)

frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

progress_report = ctk.CTkLabel(frame, text="Waiting for job...", font=("Playfair", 22))
eta = ctk.CTkLabel(frame, text="", font=("Playfair", 22))
title_label = ctk.CTkLabel(window, text="", font=("Playfair", 22), wraplength=540)
progress_report.grid(row=0, column=0, columnspan=2, pady=10, padx=10)
eta.grid(row=0, column=1, pady=10, padx=10)
title_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)


def get_video_title(url):
    ydl_opts = {
        "quiet": True,  # Suppresses additional output
        "skip_download": True,  # Only get metadata without downloading
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get("title", "Unknown Title")


def progress_hook(d):
    # Initialize downloaded and total bytes to avoid UnboundLocalError
    downloaded = d.get("downloaded_bytes", 0)
    total = d.get("total_bytes", 1)  # Avoid division by zero

    if d["status"] == "downloading":
        # Check if the download is fragmented
        if "fragment_index" in d and "fragment_count" in d:
            # Progress based on fragments
            fragment_index = d["fragment_index"]
            fragment_count = d["fragment_count"]
            percent = (fragment_index / fragment_count) * 100
        else:
            # Progress based on bytes for non-fragmented downloads
            percent = (downloaded / total) * 100

        # Calculate average speed based on elapsed time
        elapsed_time = time.time() - start_time
        if downloaded > 0 and elapsed_time > 0:
            average_speed = downloaded / elapsed_time  # average speed in bytes/s
        else:
            average_speed = None  # Unable to calculate yet

        # Calculate estimated time if average speed is available and meaningful
        if average_speed and average_speed > 0:
            remaining_bytes = total - downloaded
            eta_seconds = remaining_bytes / average_speed
            eta_formatted = time.strftime("%H:%M:%S", time.gmtime(eta_seconds))
        else:
            eta_formatted = "Calculating..."

        # Update progress and ETA labels
        progress_report.grid(row=0, column=0, columnspan=1, pady=10, padx=10)
        progress_report.configure(text=f"Progress: {percent:.2f}%")
        eta.configure(text=f" Remaining Time:\n {eta_formatted}")

    elif d["status"] == "finished":
        # Clear ETA and update title and progress report
        eta.configure(text="")
        title_label.configure(text="")
        progress_report.grid(row=0, column=0, columnspan=2, pady=10, padx=10)
        update_ui("Download complete! Processing...")
        display_var.set("")


ydl_opts_mp4 = {
    "format": "bestvideo+bestaudio/best",  # Selects best video and audio quality
    "outtmpl": "./Downloads/Video+Audio/%(title)s.%(ext)s",  # Saves to Downloads directory
    "progress_hooks": [progress_hook],  # Sets the hook to track progress
    "logger": YTDLPLogger(update_ui),  # Additional args for ffmpeg
}


ydl_opts_mp3 = {
    "format": "bestaudio/best",  # Selects best audio quality
    "outtmpl": "./Downloads/Audio-Only/%(title)s.%(ext)s",  # Saves to Downloads directory
    "progress_hooks": [progress_hook],  # Sets the hook to track progress
    "postprocessors": [
        {  # Converts the file to MP3
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",  # Bitrate of the MP3 file
        }
    ],
}


# general function for the button
def general(url1):
    # download videos
    def download_mp4(url):
        try:
            title = get_video_title(url=url)
            title_label.configure(text=title)

            with yt_dlp.YoutubeDL(ydl_opts_mp4) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)

        except Exception:
            messagebox.showerror("Error", f'"{url}"\nis not a valid URL!')
        else:
            if not is_h264_codec(file_path):
                update_ui("Converting to h264...")
                convert_codec_to_h264(file_path)
            # Update UI when done.
            update_ui("Download and processing complete!")

    # download audio only
    def download_mp3(url):
        try:
            title = get_video_title(url=url)
            title_label.configure(text=title)

            with yt_dlp.YoutubeDL(ydl_opts_mp3) as ydl:
                ydl.download([url])

        except Exception:
            messagebox.showerror("Error", f'"{url}"\nis not a valid URL!')
        else:
            # Update UI when done.
            update_ui("Download and processing complete!")

    if url1 == "" and optionvar.get() == "":
        messagebox.showerror("Error", "Make sure to insert a URL first!")
    if optionvar.get() == "":
        messagebox.showerror("Error", "Choose a download format.")

    if optionvar.get() == "Video+Audio":
        threading.Thread(target=download_mp4, args=(url1,)).start()
    elif optionvar.get() == "Audio-Only":
        threading.Thread(target=download_mp3, args=(url1,)).start()


# Window elements
def create_widgets():

    instruction_url = ctk.CTkLabel(
        master=window,
        text="Insert URL",
        font=("Playfair", 22),
    )
    instruction_format = ctk.CTkLabel(
        master=window,
        text="Select Download Format",
        font=("Playfair", 20),
        wraplength=200,
    )

    display = ctk.CTkEntry(
        master=window,
        textvariable=display_var,
        font=("Arial", 24),
        width=450,
        height=30,
        corner_radius=10,
    )
    button_config = {"font": ("Playfair", 24), "width": 200, "height": 40}
    download_button = ctk.CTkButton(
        master=window,
        text="Download",
        **button_config,
        command=lambda: general(display_var.get()),
        corner_radius=10,
    )
    optionMenu = ctk.CTkOptionMenu(
        window,
        values=["Video+Audio", "Audio-Only"],
        font=("Calibri", 16),
        dropdown_font=("Calibri", 16),
        variable=optionvar,
        width=140,
    )

    # Frame for line
    line = ctk.CTkFrame(window, height=2, width=600, fg_color="grey")

    instruction_url.grid(row=0, column=0, padx=10, pady=10)
    instruction_format.grid(row=0, column=1, padx=10, pady=10)
    display.grid(row=1, column=0, padx=5, pady=10)
    optionMenu.grid(row=1, column=1, padx=10, pady=10)
    download_button.grid(row=2, column=0, pady=20, columnspan=2)
    line.grid(row=3, column=0, columnspan=2)


create_widgets()


# Open Window
window.mainloop()
