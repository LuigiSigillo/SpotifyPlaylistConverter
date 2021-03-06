from gmusicapi import Mobileclient
from gmusicapi import Webclient
import json
import yaml

def get_songs_info(songs, id_song):
    for e in songs:
        if e['id'] == id_song:
            return {
                "title": e['title'],
                "artist": e['artist'],
                "album": e['album'],
                'id': e['id']
            }
    return None

def write_playlists(songs,mc):
    playlists = mc.get_all_user_playlist_contents()
    names = []
    for p in playlists:
        p_dict_list = []
        name = p["name"]
        for track in p['tracks']:
            track_info = get_songs_info(songs,track['trackId'])
            p_dict_list.append(track_info)
            if track_info == None:
                print(track)
        with open("./playlists/" + p["name"]+'.json', 'w', encoding="utf-8") as fp:
            json.dump(p_dict_list, fp, sort_keys=True, indent=4, ensure_ascii=False)
        names.append(name)
    return names

def init():
    mc = Mobileclient()
    with open("config.yml") as ymlfile:
        cfg = yaml.load(ymlfile)
    mc.perform_oauth()
    try:
        mc.oauth_login(device_id=cfg['gmusic']['device_id'])
    except:
        mc.oauth_login(123456)
    

    #"7f30ce56-a743-3326-88ff-8a6d94d9c111"
    with open('./playlists/data.json', 'r', encoding="utf-8") as fp:
        data = json.load(fp)
    if len(data) == 0:
        data = mc.get_all_songs()
        with open('./playlists/data.json', 'w', encoding="utf-8") as fp:
            json.dump(data, fp, sort_keys=True, indent=4, ensure_ascii=False)
    return data,mc




import os

def parse_data(rootdir="C:/Users/luigi/Music/Playlist"):
    """
    Parse all the files presents in the rootdir and its subdirectories
    :param string:
    :return: None 
    """
    lst = []
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            filename_fullpath = os.path.join(subdir, file)
            print(file)
    #write_json(lst,file+".json")





if __name__ == "__main__":
    #data,mc = init()
    #write_playlists(data, mc)
    parse_data()






''' not used for now'''
def get_songs_of_playlist(playlist_name,songs):
    playlists = mc.get_all_user_playlist_contents()
    for p in playlists:
        p_dict_list = []
        if playlist_name == p["name"]:
            for track in p['tracks']:
                p_dict_list.append(get_songs_info(songs,track['trackId']))
            return p_dict_list