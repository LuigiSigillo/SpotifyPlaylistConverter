from gmusicapi import Mobileclient
from gmusicapi import Webclient
import json
mc = Mobileclient()
#mc.perform_oauth()


mc.oauth_login(device_id="36d23bfa893d28bd")

#"7f30ce56-a743-3326-88ff-8a6d94d9c111"
#songs = mc.get_all_songs()
#print(len(songs))

'''with open('data.json', 'w', encoding="utf-8") as fp:
    json.dump(songs, fp, sort_keys=True, indent=4,ensure_ascii=False)
    print("CI SIAMO?")
'''
with open('data.json', 'r', encoding="utf-8") as fp:
    data = json.load(fp)

def get_songs_info(songs, id_song):
    for e in songs:
        if e['id'] == id_song:
            return {
                "title": e['title'],
                "artist": e['artist'],
                "album": e['album']
            }


def write_playlists(songs):
    playlists = mc.get_all_user_playlist_contents()
    for p in playlists:
        p_dict_list = []
        name = p["name"]
        for track in p['tracks']:
                p_dict_list.append(get_songs_info(songs,track['trackId']))
        
        with open(p["name"]+'.json', 'w', encoding="utf-8") as fp:
            json.dump(p_dict_list, fp, sort_keys=True, indent=4, ensure_ascii=False)
        

write_playlists(data)





def get_songs_of_playlist(playlist_name):
    playlists = mc.get_all_user_playlist_contents()
    for p in playlists:
        p_dict_list = []
        if playlist_name == p["name"]:
            for track in p['tracks']:
                p_dict_list.append(get_songs_info(track['trackId']))
            return p_dict_list