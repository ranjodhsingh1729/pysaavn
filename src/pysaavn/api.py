"""Services"""

from . import wrappers
from requests import Session


class PySaavn:
    def __init__(self):
        self.domain = "https://www.jiosaavn.com/api.php"
        self.session = Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
            }
        )
        self.query_calls = {
            "Song": "search.getResults",
            "Album": "search.getAlbumResults",
            "Artist": "search.getArtistResults",
            "Playlist": "search.getPlaylistResults",
        }

    def query(self, q, p=1, n=20, type="Song"):
        response = self.fetch_query(q, p, n, type)
        results = response.get("results", [])
        results = self.parse_query(results, type)
        return results

    def fetch_query(self, q, p, n, type):
        call = self.query_calls.get(type)
        uri = f"?p={p}&q={q}&_format=json&_marker=0&api_version=4&ctx=web6dot0&n={n}&__call={call}"
        url = self.domain + uri

        response = self.session.get(url)
        if response.ok:
            return response.json()

    def parse_query(self, results, type="Song"):
        res_obj = getattr(wrappers, type)

        __results = []
        for result in results:
            __result = res_obj(result)
            __results.append(__result)

        return __results

    def get_songs(self, obj, p=0, n=50):
        uri = obj.listing_uri(p, n)
        url = self.domain + uri

        response = self.session.get(url)
        if response.ok:
            results = response.json()
            obj.songs = results.get(obj.songs)
            obj.songs = self.parse_query(obj.songs)

        return obj.songs

if __name__ == "__main__":
    pass
