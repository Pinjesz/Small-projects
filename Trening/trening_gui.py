import threading
import tkinter as tk
from typing import Callable, Tuple
from mutagen.mp3 import MP3
from inputimeout import inputimeout, TimeoutOccurred
from os import listdir, path, remove
import pygame
import time
import random
import sys
import json


class Player:
    def __init__(self, music: pygame.mixer.music) -> None:
        self.pause = False
        self.unpause = False
        self.skip = False
        self.end = False
        self.music = music
        self.thread = None

    def play(self, minutes: int):
        self.thread = threading.Thread(
            target=play_music, args=(self, minutes), name="Player")
        self.thread.start()


class Window(tk.Tk):
    def __init__(self, music: pygame.mixer.music):
        super().__init__()
        self.title("Trening")
        self.geometry("500x500")
        self.coordinator = Coordinator(music)
        self.place()

    def place(self):
        font = "none 20 bold"
        self.pause_button = tk.Button(
            self, text="Pause", font=font, command=self.command_pause)
        self.pause_button.grid(row=0, column=0, columnspan=1, sticky=tk.E)

        self.skip_button = tk.Button(
            self, text="Skip", font=font, command=self.command_skip)
        self.skip_button.grid(row=1, column=0, rowspan=1, sticky=tk.W)

        self.get_songs_button = tk.Button(
            self, text="Get songs", font=font, command=update_songs)
        self.get_songs_button.grid(row=2, column=0, columnspan=1, sticky=tk.E)

        self.delete_songs_button = tk.Button(
            self, text="Delete songs", font=font, command=delete_songs)
        self.delete_songs_button.grid(row=3, column=0, rowspan=1, sticky=tk.W)

        play_songs = self.make_play_songs()
        self.play_button = tk.Button(
            self, text="Play", font=font, command=play_songs)
        self.play_button.grid(row=4, column=0, rowspan=1, sticky=tk.W)

        self.entry_box = tk.Entry(self, font=font)
        self.entry_box.grid(row=5, column=0)

    def make_play_songs(self) -> Callable:
        def _function():
            minutes = int(self.entry_box.get())
            self.coordinator.player.play(minutes)
        return _function

    def command_pause(self):
        self.coordinator.player.pause = True
        self.pause_button.configure(
            text="Unpause", command=self.command_unpause)

    def command_unpause(self):
        self.coordinator.player.unpause = True
        self.pause_button.configure(text="Pause", command=self.command_pause)

    def command_skip(self):
        self.coordinator.player.skip = True

    def command_end(self):
        print("dupa")
        self.coordinator.player.end = True
        self.coordinator.player.music.stop()
        self.coordinator.player.thread.join()
        exit(0)


class Coordinator:
    def __init__(self, music: pygame.mixer.music) -> None:
        self.player = Player(music)

    def start_playing(self):
        songs, _ = get_songs_from_file()
        self.player.music.set_volume(1)
        timer_start = time.time()
        while not self.player.end:
            random.shuffle(songs)
            for song in songs:
                pass

    def coordinate(self):
        while not self.player.end:
            pass


def play_music(player: Player, minutes: int):
    songs, _ = get_songs_from_file()
    player.music.set_volume(1)
    idx = 0
    timer_start = time.time()
    while not player.end:
        random.shuffle(songs)
        for song in songs:
            idx += 1
            try:
                length = song['song_length'] - \
                    song['start_skip'] - song['end_skip']
                player.music.load("songs/"+song['title'])
                player.music.play(start=song['start_skip'])
                print(f"{idx}. Now playing: " + song['title'] + "  ", end="")
                song_end = False
                while not (song_end or player.end):
                    try:
                        text = inputimeout(
                            timeout=length - player.music.get_pos()/1000)
                        if text != '':  # pause
                            pause_start = time.time()
                            player.music.pause()
                            input()
                            player.music.unpause()
                            pause_duration = time.time() - pause_start
                            timer_start += pause_duration
                        else:  # skip
                            song_end = True
                    except TimeoutOccurred:
                        song_end = True
            except pygame.error:
                if (path.isdir("songs")):
                    log_missing_song(song['title'])
                else:
                    print("Place songs in directory '/songs'.")
                    exit(1)

            if minutes >= 0:
                if time.time() - timer_start > 60*minutes:
                    print("Finished")
                    return

            if player.end:
                print("Exiting")
                return


def get_songs_from_file() -> Tuple[list, int]:
    songs = []
    try:
        with open('songs.json', 'r') as json_file:
            jf = json.load(json_file)
            songs = jf['songs']
            song_num = jf["song_num"]
        return songs, song_num
    except FileNotFoundError:
        print("Run 'python trening.py setup' first.")
        exit(1)


def update_songs():
    files = listdir("songs")
    songs, song_num = get_songs_from_file()
    song_titles = []
    for song in songs:
        song_titles.append(song['title'])
    new_songs_counter = 0
    for file in files:
        if file not in song_titles:
            new_songs_counter += 1
            song_length = MP3("songs/"+file).info.length
            new_song = {"title": file, "song_length": song_length,
                        "start_skip": 0, "end_skip": 0}
            songs.append(new_song)
    song_num += new_songs_counter
    with open('songs.json', 'w') as json_file:
        json_input = {"song_num": song_num, "songs": songs}
        json.dump(json_input, json_file, indent=4)
    print(f"Successfully added {new_songs_counter} new songs to songs.json")


def delete_songs():
    empty_dict = {"song_num": 0, "songs": []}
    with open('songs.json', 'w') as json_file:
        json.dump(empty_dict, json_file)
    if (path.isfile("trening.log")):
        remove('trening.log')
    print("Successfully deleted songs from songs.json")


def log_missing_song(song_name: str):
    with open('trening.log', 'a', encoding="utf-8") as log_file:
        log_file.write(f"Cannot find file: {song_name}\n")


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    window = Window(pygame.mixer.music)
    window.protocol("WM_DELETE_WINDOW", window.command_end)
    window.mainloop()
