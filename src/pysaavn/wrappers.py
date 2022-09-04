"""Wrappers"""


import re
import pyDes
import base64
from html import unescape

expression = re.compile("https://www.jiosaavn.com/.*/(.*)")
encryption = pyDes.des(b"38346591", pyDes.ECB,
                       b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)


def get_token(perma_url):
    token = expression.match(perma_url).group(1)
    return token


def decrypt_media_url(enc_url):
    enc_url = base64.b64decode(enc_url)
    dec_url = encryption.decrypt(
        enc_url, padmode=pyDes.PAD_PKCS5).decode("utf-8")
    return dec_url


class BRO:
    @property
    def token(self):
        return get_token(self.perma_url)

    @property
    def high_res_image(self):
        return self.image_url.replace("-150x150.jpg", "-500x500.jpg")

    def __str__(self):
        return unescape(self.title)


class Song(BRO):
    def __init__(self, response):
        self.response = response

        self.title = self.response.get("title")
        self.subtitle = self.response.get("subtitle")
        self.language = self.response.get("language")
        self.perma_url = self.response.get("perma_url")
        self.image_url = self.response.get("image")
        self.play_count = self.response.get("play_count")
        self.release_date = self.response.get("release_date")
        self.release_year = self.response.get("year")

        self.music = self.response["more_info"].get("music")
        self.album = self.response["more_info"].get("album")
        self.album_url = self.response["more_info"].get("album_url")
        self.duration = self.response["more_info"].get("duration")
        self.is_320kbps = self.response["more_info"].get("320kbps")
        self.has_lyrics = self.response["more_info"].get("has_lyrics")
        self.lyrics_snippet = self.response["more_info"].get("lyrics_snippet")
        self.preview_url = self.response["more_info"].get("vlink")


    @property
    def media_url(self):
        encrypted_media_url = self.response["more_info"].get(
            "encrypted_media_url")
        decrypted_media_url = decrypt_media_url(encrypted_media_url)
        decrypted_media_url = decrypted_media_url.replace("_96.mp4", "_320.mp4")
        return decrypted_media_url


class Album(BRO):
    def __init__(self, response):
        self.response = response

        self.title = self.response.get("title")
        self.subtitle = self.response.get("subtitle")
        self.language = self.response.get("language")
        self.perma_url = self.response.get("perma_url")
        self.image_url = self.response.get("image")
        self.release_date = self.response.get("release_date")
        self.release_year = self.response.get("year")

        self.music = self.response["more_info"].get("music")
        self.song_count = self.response["more_info"].get("song_count")

        self.songs = "list"

    def listing_uri(self, p, n):
        uri = f"?__call=webapi.get&token={self.token}&type=album&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0"
        return uri


class Artist(BRO):
    def __init__(self, response):
        self.response = response

        self.name = self.response.get("name")
        self.role = self.response.get("role")
        self.rating = self.response.get("ctr")
        self.perma_url = self.response.get("perma_url")
        self.image_url = self.response.get("image")

        self.songs = "topSongs"

    def listing_uri(self, p, n):
        uri = f"?__call=webapi.get&token={self.token}&type=artist&p={p}&n_song={n}&n_album={n}&sub_type=&category=&sort_order=&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0"
        return uri

    def __str__(self):
        return f"{self.name} - {self.role}"


class Playlist(BRO):
    def __init__(self, response):
        self.response = response

        self.title = self.response.get("title")
        self.subtitle = self.response.get("subtitle")
        self.rating = self.response.get("ctr")
        self.perma_url = self.response.get("perma_url")
        self.image_url = self.response.get("image")

        self.language = self.response["more_info"].get("language")
        self.song_count = self.response["more_info"].get("song_count")

        self.userid = self.response["more_info"].get("uid")
        self.artists = self.response["more_info"].get("artist_name")

        self.songs = "list"

    def listing_uri(self, p, n):
        uri = f"?__call=webapi.get&token={self.token}&type=playlist&p={p}&n={n}&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0"
        return uri


if __name__ == "__main__":
    pass
