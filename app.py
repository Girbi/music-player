import os
import time
from tkinter import (
    ACTIVE,
    BOTH,
    END,
    RIGHT,
    VERTICAL,
    Button,
    Label,
    LabelFrame,
    Listbox,
    Scrollbar,
    StringVar,
    Tk,
)

import pygame.mixer as mixer
import tksvg

# Initialize Mixer
mixer.init()


# Helper Functions
def load_songs(listbox: Listbox):
    """Load all songs from a directory."""

    directory = "./audio"
    os.chdir(directory)
    songs = [song for song in os.listdir() if song.endswith(".mp3")]
    listbox.delete(0, END)
    for song in songs:
        listbox.insert(END, song)


def play_song(song_list: Listbox):
    """Play the selected song."""
    global is_playing, is_paused, current_song_length

    selected_song = song_list.get(ACTIVE)
    if not selected_song:
        return  # No song selected

    # Update the current song name
    nameSize = len(selected_song) - 4
    current_song_name.set(selected_song[0:nameSize])

    # Load and play the selected song
    mixer.music.load(selected_song)
    mixer.music.play()

    # Cache the song length
    current_song_length = get_song_length(selected_song)

    is_playing = True
    is_paused = False
    play_btn.config(image=pause_icon)

    # Update the current time display
    update_time_display()


def handle_song_state(song_list: Listbox):
    """Play, pause, or resume the selected song."""
    global is_playing, is_paused

    if is_playing and not is_paused:
        # Pause the song
        mixer.music.pause()
        is_paused = True
        play_btn.config(image=play_icon)
    elif is_paused:
        # Resume the song
        mixer.music.unpause()
        is_paused = False
        play_btn.config(image=pause_icon)
    else:
        # Play the song
        play_song(song_list)


def stop_song():
    """Stop the current song."""
    global is_playing, is_paused
    mixer.music.stop()
    is_playing = False
    is_paused = False
    play_btn.config(image=play_icon)


def next_song(song_list: Listbox):
    """Play the next song in the playlist."""
    global is_playing, is_paused
    current_index = song_list.curselection()
    if current_index:
        # Select the next song
        next_index = (current_index[0] + 1) % song_list.size()
        song_list.selection_clear(0, END)
        song_list.selection_set(next_index)
        song_list.activate(next_index)

        # Reset and play the next song
        is_playing = False
        is_paused = False
        play_song(song_list)


def previous_song(song_list: Listbox):
    """Play the previous song in the playlist."""
    global is_playing, is_paused
    current_index = song_list.curselection()
    if current_index:
        # Select the previous song
        prev_index = (current_index[0] - 1) % song_list.size()
        song_list.selection_clear(0, END)
        song_list.selection_set(prev_index)
        song_list.activate(prev_index)

        # Reset and play the previous song
        is_playing = False
        is_paused = False
        play_song(song_list)


def update_time_display():
    """Update the time display as the song plays."""
    if is_playing and not is_paused:
        # Get the current time
        current_time = mixer.music.get_pos() // 1000

        # Update the current time label
        current_time_label.config(
            text=f"{time.strftime('%M:%S', time.gmtime(current_time))} / {time.strftime('%M:%S', time.gmtime(current_song_length))}"
        )

        if current_time < current_song_length:
            # Schedule the next update
            root.after(1000, update_time_display)


def get_song_length(song_path):
    """Get the total length of a song."""
    try:
        song_path = os.path.abspath(song_path)
        return int(mixer.Sound(song_path).get_length())
    except Exception as e:
        print(f"Error getting song length: {e}")
    return 0


def load_svg_icon(file_path, size=(24, 24)):
    """Load an SVG icon and resize it."""
    return tksvg.SvgImage(
        master=controls_frame,
        file=file_path,
        width=size[0],
        height=size[1],
    )


# Initialize GUI
root = Tk()
root.geometry("400x400")
root.title("Mp3 Music Player")
root.resizable(False, False)
root.configure(bg="#2f2f2f")

# Global Variables
is_playing = False  # Tracks whether a song is playing
is_paused = False  # Tracks whether a song is paused
current_song_name = StringVar(value="")  # Tracks the current song name
current_song_length = 0  # Stores the length of the current song in seconds

# Frames and Layout
playlist_frame = LabelFrame(
    root,
    text="Playlist",
    bg="#0c0556",
    border=0,
    fg="white",
    font=("Arial", 10, "bold"),
    # padx=5,
    # pady=5,
)
playlist_frame.grid(row=0, column=0, pady=10, sticky="ns")

info_frame = LabelFrame(
    root, bg="#0c0556", fg="white", border=0, font=("Arial", 10, "bold")
)
info_frame.grid(
    row=1,
    column=0,
    padx=(0, 10),
    pady=5,
    sticky="ew",
)

controls_frame = LabelFrame(root, bg="#0c0556", border=0, font=("Arial", 11, "bold"))
controls_frame.grid(row=2, column=0, padx=(0, 10), pady=5)

# root.grid_columnconfigure(0, weight=1)  # Playlist column
# root.grid_columnconfigure(1, weight=1)  # Info and controls columns
# root.grid_columnconfigure(2, weight=1)


# Playlist
playlist = Listbox(
    playlist_frame,
    font=("Arial", 10, "bold"),
    bg="white",
    fg="black",
    selectbackground="#1b0cb1",
    width=25,
)
playlist.pack(side="left", fill=BOTH, padx=5, pady=5)
scrollbar = Scrollbar(playlist_frame, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=BOTH)
playlist.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=playlist.yview)


# Info Display
Label(
    info_frame,
    text="Playing: ",
    bg="#0c0556",
    fg="white",
    font=("Arial", 10, "bold"),
).grid(row=0, column=0, padx=5, sticky="w")

Label(
    info_frame,
    textvariable=current_song_name,
    bg="#0c0556",
    fg="white",
    font=("Arial", 10),
).grid(row=0, column=1, sticky="w")

info_frame.grid_columnconfigure(2, weight=1)

current_time_label = Label(
    info_frame,
    text="00:00 / 00:00",
    bg="#0c0556",
    fg="white",
    font=("Arial", 10, "bold"),
)
current_time_label.grid(row=1, column=0, columnspan=3, padx=5, sticky="ew")

# Button Icons
play_icon = load_svg_icon("icons/play.svg")
pause_icon = load_svg_icon("icons/pause.svg")
stop_icon = load_svg_icon("icons/stop.svg")
prev_icon = load_svg_icon("icons/prev.svg")
next_icon = load_svg_icon("icons/next.svg")

# Previous Song Button
Button(
    controls_frame,
    image=prev_icon,
    bg="white",
    command=lambda: previous_song(playlist),
).grid(row=0, column=0, padx=10, pady=5)

# Play/Pause Button
play_btn = Button(
    controls_frame,
    image=play_icon,
    bg="white",
    command=lambda: handle_song_state(playlist),
)
play_btn.grid(row=0, column=1, padx=10, pady=5)

# Stop Button
Button(controls_frame, image=stop_icon, bg="white", command=stop_song).grid(
    row=0, column=2, padx=10, pady=5
)

# Next Song Button
Button(
    controls_frame, image=next_icon, bg="white", command=lambda: next_song(playlist)
).grid(row=0, column=3, padx=10, pady=5)

load_songs(playlist)
# Run the application
root.mainloop()
