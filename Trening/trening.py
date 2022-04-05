# hide support prompt
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
#imports
from typing import Tuple
from mutagen.mp3 import MP3
from inputimeout import inputimeout, TimeoutOccurred
from os import listdir, path, remove
import pygame
import time
import random
import sys
import json


def main(args: list, music: pygame.mixer.music):
    args_num = len(args)
    if args_num == 1:
        play_music(music)
    elif args_num == 2:
        try:
            minutes = float(args[1])
            play_music(music, minutes)
        except ValueError:
            if args[1] == 'delete':
                delete_songs()
            else:
                update_songs()
    else:
        error_display()


def play_music(music: pygame.mixer.music, minutes: float = -1):
    songs, _ = get_songs_from_file()
    music.set_volume(1)
    idx = 0
    timer_start = time.time()
    while True:
        random.shuffle(songs)
        for song in songs:
            idx += 1
            try:
                length = song['song_length'] - \
                    song['start_skip'] - song['end_skip']
                music.load("songs/"+song['title'])
                music.play(start=song['start_skip'])
                print(f"{idx}. Now playing: " + song['title'] + "  ", end="")
                song_end = False
                while not song_end:
                    try:
                        text = inputimeout(
                            timeout=length - music.get_pos()/1000)
                        if text != '':  # pause
                            pause_start = time.time()
                            music.pause()
                            input()
                            music.unpause()
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


def log_missing_song(song_name: str):
    with open('trening.log', 'a', encoding="utf-8") as log_file:
        log_file.write(f"Cannot find file: {song_name}\n")


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


def error_display():
    print("Syntax:")
    print("'python trening.py' to play all songs")
    print("'python trening.py <duration>' to play songs for <duration> minutes")
    print("'python trening.py setup' to read songs to songs.json")
    print("'python trening.py delete' to delete songs from songs.json")


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    args = sys.argv
    try:
        main(args, pygame.mixer.music)
    except KeyboardInterrupt:
        print("\nExiting")
    finally:
        if (path.isfile("trening.log")):
            print("There is a problem with some files, check trening.log!")
