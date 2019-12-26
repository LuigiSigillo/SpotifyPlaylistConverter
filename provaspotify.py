import spotipy
import spotipy.util as util
import yaml


def init():
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    scope = 'playlist-modify-public'
    username = cfg['provaspotify']['username']
    return util.prompt_for_user_token(
        username,
        scope,
        client_id=cfg['provaspotify']['client_id'],
        client_secret=cfg['provaspotify']['client_secret'],
        redirect_uri='http://localhost:5500'
        ),username


def get_data(filename):
    with open(filename, 'r', encoding="utf-8") as fp:
        return json.load(fp)

def create_query(song):
    artist = song['artist'].split(",")[0]
    q = song['title'] + " " + artist
    if ".mp3" in song['title']
        q = song['title'][:-4] + " " + artist
    return q
    

def convert_playlist(token,data):
    if token:
        sp = spotipy.Spotify(auth=token)
        lista = []
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
                lista.append(id_song)
                break
        return lista      
    else:
        print ("Can't get token")
        return []


token,username = init()
data = get_data("non_aggiunti.json")
songs_list = convert_playlist(token,playlist)
sp.user_playlist_add_tracks(username, cfg['provaspotify']['playlist_id'], songs_list)