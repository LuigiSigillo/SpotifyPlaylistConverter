import spotipy
import spotipy.util as util
import yaml
import json

def init():
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    scope = 'playlist-modify-public'
    username = cfg['provaspotify']['username']
    token = util.prompt_for_user_token(
        username,
        scope,
        client_id=cfg['provaspotify']['client_id'],
        client_secret=cfg['provaspotify']['client_secret'],
        redirect_uri='http://localhost:5500'
        )
    if token:
        return spotipy.Spotify(auth=token),username
    else:
        print ("Can't get token")
        return 


def get_data(filename):
    with open(filename, 'r', encoding="utf-8") as fp:
        return json.load(fp)

def write_data(filename,songs):
    with open(filename, 'w', encoding="utf-8") as fp:
        json.dump(songs, fp, sort_keys=True, indent=4,ensure_ascii=False)

def create_query(song):
    artists = song['artist'].split(",")
    if "/" in song['artist']:
        artists = song['artist'].split("/")
    if ";" in song['artist']:
        artists = song['artist'].split(";")
    artist = artists[0]
    q = song['title']
    if ".mp3" in song['title']:
        q = song['title'][:-4]
    for a in artists[1:]:
        q = q.replace(a,"")
    if not artist in q:
        q = q + " " + artist
  
    #q = q.replace("ft","")
    #q = q.replace("feat.","")
    return q,artists
    

def convert_playlist(sp,data):
    lists,strange = [],[]
    i = 0
    for song in data:
        q,song_artists = create_query(song)
        results = sp.search(q, limit=3, offset=0, type='track')['tracks']['items']
        for j,item in enumerate(results):
            album_url = item['album']['images'][0]['url']
            album_name = item['album']['name']
            artists = []
            for a in item['artists']:
                artists.append(a['name'])
            id_song = item['id']
            song_title = item['name']
            if "Originally" in song_title or "Karaoke" in artists[0]:
                strange.append(song)
                break
            if artists[0] == song_artists[0]:
                lists.append(id_song)
                break 
        if len(results) == 0 or len(results) == j-1:
            strange.append(song)
    return lists,strange     


sp,username = init()
playlist_id = sp.user_playlist_create(username, "Indie", public=True)['id']
data = get_data("./playlists/Indie.json")
songs_list,not_added = convert_playlist(sp,data)
write_data("strangeTrapITA.json",not_added)
while songs_list: 
    sp.user_playlist_add_tracks(username, playlist_id, songs_list[:100])
    songs_list = songs_list[100:]