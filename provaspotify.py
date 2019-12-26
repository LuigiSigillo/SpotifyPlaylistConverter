import spotipy
import spotipy.util as util
import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
#sp.user_playlist_add_tracks(username, cfg['provaspotify']['playlist_id'], track_ids)
#search(q, limit=10, offset=0, type='track', market=None)

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
    q = ""
    sp = spotipy.Spotify(auth=token)
    results = sp.search(q, limit=5, offset=0, type='track')
    for item in results['tracks']['items']:
        album_url = item['album']['images'][0]['url']
        album_name = item['album']['name']
        artists = []
        for a in item['artists']:
            artists.append(a['name'])
        id_song = item['id']
        song_title = item['name']
        print(album_name,album_url,artists,id_song,song_title)
else:
    print ("Can't get token for", username)

    