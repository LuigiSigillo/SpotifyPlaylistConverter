import spotipy
import spotipy.util as util
import yaml
import json
import glob, os
from termcolor import colored

def init():
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    scope = 'playlist-modify-public'
    username = cfg['spotify']['username']
    token = util.prompt_for_user_token(
        username,
        scope,
        client_id=cfg['spotify']['client_id'],
        client_secret=cfg['spotify']['client_secret'],
        redirect_uri='http://localhost:5500'
        )
    if token:
        return spotipy.Spotify(auth=token),username
    else:
        print ("Can't get token")
        return 


def get_data(filename):
    with open(filename, 'r', encoding="utf-8") as fp:
        data = json.load(fp)
        for elem in data:
            try:
                a = elem['artist']
            except:
                elem['artist'] = ""
            try:
                a = elem['album']
            except:
                elem['album'] = ""
    return data


def write_data(filename,songs):
    with open(filename, 'w', encoding="utf-8") as fp:
        json.dump(songs, fp, sort_keys=True, indent=4,ensure_ascii=False)

def create_query(song):
    if song['artist'] == None:
        return song['title'],[]
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
    for song in data:
        if song != None:
            q,song_artists = create_query(song)
            results = sp.search(q, limit=3, offset=0, type='track')['tracks']['items']
            for j,item in enumerate(results):
                #album_url = item['album']['images'][0]['url']
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
            if len(results) == 0 or len(results) == j+1:
                strange.append(song)
    added,not_added = partial_add(sp, strange)
    return lists + added, not_added  


def partial_add(sp,data):
    lists,not_added = [],[]
    my_dict = {}
    for song in data:
        my_dict[song['id']] = []
        q,song_artists = create_query(song)
        #print(colored(json.dumps(song, indent=4),"cyan"))
        results = sp.search(q, limit=5, offset=0, type='track')['tracks']['items']
        for j,item in enumerate(results):
            #album_url = item['album']['images'][0]['url']
            album_name = item['album']['name']
            artists = []
            for a in item['artists']:
                artists.append(a['name'])
            id_song = item['id']
            song_title = item['name']
            if artists[0] == song_artists[0]:
                lists.append(id_song)
                #print(colored("added "+song_title,"green"))
                del my_dict[song['id']]
                break
            else:
                payload = { "original_info": song, "title": song_title, "artists": artists, "album": album_name, "id": id_song }
                my_dict[song['id']].append(payload)
        if song['id'] in my_dict and len(my_dict[song['id']]) == 0:
            not_added.append(song)
            del my_dict[song['id']]
    if input("I can search the songs for you and you choose if it is correct.\n Remainig songs = " + str(len(not_added))+" ") == "y":
        a,b = manual_add_precomputed(my_dict)
        return lists + a, b
    else:
        return lists, not_added

def manual_add_precomputed(results):
    lists,not_added = [],[]
    for j,item in enumerate(results):
        print(colored(
            "\nTitle " + results[item][0]["original_info"]["title"]+
            "\nArtists " + results[item][0]["original_info"]["artist"]+
            "\nAlbum " + results[item][0]["original_info"]["album"]
        ,"cyan"))
        for i,e in enumerate(results[item]):
            print ("Index = ",i,"\n\tTitle",e["title"],"\n\tArtists",e["artists"],"\n\tAlbum",e["album"])
        idx = input("\nWhich index? (-1 if not present) \n")
        if int(idx) >= 0:
            lists.append(results[item][int(idx)]["id"])
            try:
                print(colored("added {}".format(item[int(idx)]),"green"))
            except:
                continue
        else:
            not_added.append(results[item][0]["original_info"])
    return lists,not_added

def manual_add(sp,data):
    lists,not_added = [],[]
    for song in data:
        manual = False
        non_serve,song_artists = create_query(song)
        print(colored(json.dumps(song, indent=4),"cyan"))
        q = input("\n Write the search:\n")
        results = sp.search(q, limit=5, offset=0, type='track')['tracks']['items']
        for j,item in enumerate(results):
            #album_url = item['album']['images'][0]['url']
            album_name = item['album']['name']
            artists = []
            for a in item['artists']:
                artists.append(a['name'])
            id_song = item['id']
            song_title = item['name']
            if manual:
                print (song_title,artists,album_name)
                if input("Is this one ? \n") == 'y':
                    lists.append(id_song)
                    print(colored("added","green"))
                    break
                else:
                    continue
            if artists[0] == song_artists[0]:
                lists.append(id_song)
                print(colored("added","green"))
                break
            else:
                manual = True
        if len(results) == 0 or len(results) == j+1:
            print(colored("this song is unaddable :(","red"), song)
            not_added.append(song)
    return lists,not_added



def add_over_100_songs(songs_list,username,playlist_id):
    while songs_list: 
        sp.user_playlist_add_tracks(username, playlist_id, songs_list[:100])
        songs_list = songs_list[100:]



def add_songs_and_write_not_added_file(songs_list, not_added):
    add_over_100_songs(list(dict.fromkeys(songs_list)),username,playlist_id)
    write_data("not added/not_added_"+playlist_name+".json", not_added)
    print("Not added these songs, you can find them inside this file: not added/not_added_"+playlist_name+".json")
    for i,e in enumerate(not_added):
        try:
            print ("Index = ",i,"\n\tTitle",e["title"],"\n\tArtists",e["artist"],"\n\tAlbum",e["album"])
        except:
            continue



def print_playlists(parent_dir="./playlists"):
    for file in glob.glob(os.path.join(parent_dir, '*.json')):
        name = file.strip("./playlists\\")
        print (name.strip(".json"))



def main():
    sp,username = init()
    print_playlists()
    playlist_name = input("When prompted answer using 'y' as yes and 'n' as no.\nInsert playlist name to convert:\n")
    playlist_id = sp.user_playlist_create(username, playlist_name, public=True)['id']
    data = get_data("./playlists/"+playlist_name+".json")
    fst_songs_list,not_added = convert_playlist(sp,data)
    if len(not_added) > 0:
        answ = input(str(len(not_added)) + " tracks very hard to find, would you try to find them manually? (Like a normal research on spotify)\n Answer using 'y' as yes and 'n' as no. ")
        if answ == "y":
            snd_songs_list,def_not_added = manual_add(sp,not_added)
            add_songs_and_write_not_added_file(fst_songs_list+snd_songs_list,def_not_added)
        else:
            add_songs_and_write_not_added_file(fst_songs_list,not_added)
        
    

if __name__ == "__main__":
    main()