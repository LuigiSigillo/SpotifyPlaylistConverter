import spotipy
import spotipy.util as util
import yaml
import json

def init():
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
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
    artist = artists[0]
    q = song['title']
    for a in artists:
        q = q.replace(a,"")
    q = q + " " + artist
    if ".mp3" in song['title']:
        q = song['title'][:-4] + " " + artist
    q = q.replace("ft","")
    q = q.replace("feat.","")
    print(q)
    return q
    

def convert_playlist(sp,data):
    lists = [[] for x in range(1 + int(len(data)/100))]
    strange = []
    i = 1
    for song in data:
        q = create_query(song)
        results = sp.search(q, limit=5, offset=0, type='track')
        for item in results['tracks']['items']:
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
            if len(lists[i-1])<100*i:
                lists[i-1].append(id_song)
            else:
                i = i+1
                lists[i-1].append(id_song)
            break
        if len(results) == 0:
            strange.append(song)
    return lists,strange     


sp,username = init()
data = get_data("./playlists/Zona Trap USA.json")
songs_lists,not_added = convert_playlist(sp,data)
write_data("strange.json",not_added)
for l in songs_lists:
    sp.user_playlist_add_tracks(username, "45qpRfTlvYUPqW6LnUfrMa", l)