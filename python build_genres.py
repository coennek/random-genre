import json
import re
import urllib.request
from urllib.parse import quote

print("Fetching genres from EveryNoise...")
req = urllib.request.Request(
    "https://everynoise.com/everynoise1d.html",
    headers={"User-Agent": "Mozilla/5.0"},
)
html = urllib.request.urlopen(req).read().decode("utf-8")

genres = []
rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.DOTALL | re.IGNORECASE)

for row in rows:
    playlist_match = re.search(
        r'href=["\'](https://open\.spotify\.com/playlist/[^"\']+)["\']', row
    )
    playlist_url = playlist_match.group(1) if playlist_match else None

    links = re.findall(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', row)
    genre_name = None
    for href, text in links:
        clean_text = text.strip()
        if (
            not href.startswith("javascript")
            and clean_text
            and clean_text not in [">>", "note", "map", "preview"]
        ):
            genre_name = clean_text
            break

    if genre_name:
        if not playlist_url:
            playlist_url = f"https://open.spotify.com/search/{quote('The Sound of ' + genre_name)}/playlists"
        genres.append({"name": genre_name, "url": playlist_url})

with open("genres.json", "w", encoding="utf-8") as f:
    json.dump(genres, f, indent=2)

print(f"✅ Saved {len(genres)} genres to genres.json!")
