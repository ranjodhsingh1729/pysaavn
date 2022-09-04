"""Interface"""


import wget
from . import api
from InquirerPy import inquirer


app = api.PySaavn()


def main():
    q = inquirer.text(message="Enter Search Keywords:").execute()
    type = inquirer.select("Select Search Type:", ["Song", "Album", "Artist", "Playlist"], multiselect=False).execute()

    results = app.query(q, type=type)
    selection = inquirer.select(f"Select Some {type}(s):", results, multiselect=True).execute()

    if type == "Song":
        download(selection)
    else:
        selection = batch_select(selection)
        download(selection)


def batch_select(collections):
    Selection = []
    for collection in collections:
        songs = app.get_songs(collection)
        selection = inquirer.select("Select Your Song(s):", songs, multiselect=True).execute()
        Selection.extend(selection)

    return Selection


def download(song_list):
    for song in song_list:
        out = f"{song}.m4a"
        url = song.media_url
        print("\n", out, " - ", url, "\n")
        wget.download(url=url, out=out)


if __name__ == "__main__":
    main()