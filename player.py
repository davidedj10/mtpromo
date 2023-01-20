import vlc
import os
import json
import urllib.request
import requests
from typing import List
from urllib.request import Request, urlopen
import requests
import sqlite3

def insert_into_database(filename, path):
    conn = sqlite3.connect("mtpromo.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO files (filename, path) VALUES (?,?)", (filename, path)
    )
    conn.commit()
    print(f"{filename} inserted into the database.")
    conn.close()

def get_filenames():
    filenames = []
    try:
        conn = sqlite3.connect("mtpromo.db")
        c = conn.cursor()
        c.execute("SELECT filename FROM files")
        filenames = [row[0] for row in c.fetchall()]
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()
    return filenames


def check_file_exists(folder, filename):
    file_path = os.path.join(folder, filename)
    return os.path.isfile(file_path)

def get_volume(url: str):

    head = {'User-Agent': 'XYZ/3.0'}

    # Parse the JSON response
    req = Request(url, headers={'User-Agent': 'XYZ/3.0'})
    res = urlopen(req, timeout=10).read()
    data = json.loads(res)
    print(data['volume'])
    return data['volume']


def download_files(url: str, dest_folder: str) -> List[str]:
    """
    Download files from a JSON response containing a list of files.
    :param url: The URL of the JSON endpoint containing the list of files.
    :param dest_folder: The destination folder where the files will be saved.
    :return: A list of file names that were downloaded.
    """
    downloaded_files = []

    head = {'User-Agent': 'XYZ/3.0'}

    # Parse the JSON response
    try:
        req = Request(url, headers={'User-Agent': 'XYZ/3.0'})
        res = urlopen(req, timeout=10).read()
        data = json.loads(res)

    except json.decoder.JSONDecodeError as json_error:
        print("Error while parsing the json: ", json_error)
        return downloaded_files

    # Loop through the list of files and download each one
    for file in data["data"]:
        url = file["path"]
        filename = file["name"]
        try:
             if not check_file_exists(dest_folder, filename):
                response = requests.get(url , headers=head)
                response.raise_for_status()
                with open(f"{dest_folder}/{filename}", "wb") as f:
                    f.write(response.content)
                downloaded_files.append(filename)
                insert_into_database(filename, url)
             else:
                 print("already downloaded")

        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error while fetching {filename}: {errh}")
            continue

    return downloaded_files


download_files('https://mtpromo.dflabs.dev/deliver.php', "mtpromo_assets")



# List of videos to play
videos = get_filenames()

# Create VLC instance
instance = vlc.Instance()

# Create a MediaPlayer object
player = instance.media_player_new()

while True:
    for video in videos:
        # Set the media to play
        media = instance.media_new(video)
        player.set_media(media)

        # Play the video
        player.play()
        player.audio_set_volume(get_volume('https://mtpromo.dflabs.dev/deliver.php'));

        # Wait for the video to finish
        while True:
            if player.get_state() == vlc.State.Ended:
                break
