import os
import time
from tkinter import (
    ACTIVE,
    BOTH,
    END,
    Button,
    Label,
    LabelFrame,
    Listbox,
    StringVar,
    Tk,
)
import pygame.mixer as mixer
import tksvg

# Initialize Mixer
mixer.init()


# Helper Functions
def load_songs(listbox: Listbox):
    """Load all songs from the audio directory."""

    directory = "./audio"
    os.chdir(directory)
    songs = [song for song in os.listdir() if song.endswith(".mp3")]
    listbox.delete(0, END)
    for song in songs:
        listbox.insert(END, song)


def play_song(song_list: Listbox):
    """Play the selected song."""
    global is_playing, is_paused, current_song_length

    if not song_list.curselection():
        song_list.selection_set(0)

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

    if not song_list.curselection():
        song_list.selection_set(0)

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

    if not song_list.curselection():
        song_list.selection_set(0)

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


# Styles

""" Color changes
main_bg_color = "#1E1E1E"
button_color = "#962d1a"
button_active_color = "#3fa157"
info_text_color = "#ed3e88"
playlist_bg_color = "#722991"
playlist_fg_color = "#de6a21"
select_playlist_bg_color = "#440c5e"
select_playlist_fg_color = "#3fa157"
playing_color="#1A1423" """

main_bg_color = "#EACDC2"
button_color = "#EACDC2"
button_active_color = "#840032"
playing_color = "#840032"
info_text_color = "#774C60"
playlist_bg_color = "#deb1ac"
playlist_fg_color = "#372549"
select_playlist_bg_color = "#774C60"
select_playlist_fg_color = "#d77a61"


# Frames and Styles
frame_style = {"border": 0, "bg": main_bg_color, "font": ("Arial", 15, "bold")}
button_style = {
    "bg": main_bg_color,
    "border": 0,
    "anchor": "center",
    "background": button_color,
    "activebackground": button_active_color,
}

# Initialize GUI
root = Tk()
root.geometry("400x400")
root.title("Mp3 Music Player")
root.configure(bg=main_bg_color)

# Global Variables
is_playing = False  # Tracks whether a song is playing
is_paused = False  # Tracks whether a song is paused
current_song_name = StringVar(value="")  # Tracks the current song name
current_song_length = 0  # Stores the length of the current song in seconds

# Frames
playlist_frame = LabelFrame(root, text="Playlist", fg=playing_color, **frame_style)
playlist_frame.grid(row=0, column=0, pady=5, padx=5, sticky="nsew")

info_frame = LabelFrame(
    root,
    border=0,
    font=("Arial", 12, "bold"),
)
info_frame.grid(
    row=1,
    column=0,
    padx=10,
    pady=5,
    sticky="ew",
)

controls_frame = LabelFrame(root, **frame_style)
controls_frame.grid(
    row=2,
    column=0,
    padx=10,
    pady=10,
)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

# Button Icons
play_icon = load_svg_icon("icons/play.svg")
pause_icon = load_svg_icon("icons/pause.svg")
stop_icon = load_svg_icon("icons/stop.svg")
prev_icon = load_svg_icon("icons/prev.svg")
next_icon = load_svg_icon("icons/next.svg")


# Playlist
playlist = Listbox(
    playlist_frame,
    font=("Arial", 14, "bold"),
    bg=playlist_bg_color,
    fg=playlist_fg_color,
    selectbackground=select_playlist_bg_color,
    selectforeground=select_playlist_fg_color,
    width=30,
    height=10,
)
playlist.pack(side="top", fill=BOTH, padx=5, pady=5)
playlist.bind("<Double-1>", lambda event: play_song(playlist))

# Info Display
label_layout = {
    "bg": main_bg_color,
    "fg": info_text_color,
    "anchor": "center",
    "font": ("Arial", 15, "bold"),
}
Label(
    info_frame,
    textvariable=current_song_name,
    **label_layout,
).grid(row=0, column=0, columnspan=3, sticky="ew")
info_frame.grid_columnconfigure(2, weight=1)

current_time_label = Label(
    info_frame,
    text="00:00 / 00:00",
    **label_layout,
)
current_time_label.grid(row=1, column=0, columnspan=3, sticky="ew")

# Previous Song Button
Button(
    controls_frame,
    image=prev_icon,
    **button_style,
    command=lambda: previous_song(playlist),
).grid(row=0, column=0, columnspan=3, padx=50)

# Play/Pause Button
play_btn = Button(
    controls_frame,
    image=play_icon,
    **button_style,
    command=lambda: handle_song_state(playlist),
)
play_btn.grid(row=0, column=1, columnspan=3, padx=50)

# Stop Button
Button(
    controls_frame,
    image=stop_icon,
    **button_style,
    command=stop_song,
).grid(row=0, column=2, columnspan=3, padx=50)

# Next Song Button
Button(
    controls_frame,
    image=next_icon,
    **button_style,
    command=lambda: next_song(playlist),
).grid(row=0, column=3, columnspan=3, padx=50)

# Run when the app opens
load_songs(playlist)

# Run the application
root.mainloop()
