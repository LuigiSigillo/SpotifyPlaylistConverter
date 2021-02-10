import csv
import os
import glob
import json

def write_data(filename,songs):
    with open(filename, 'w', encoding="utf-8") as fp:
        json.dump(songs, fp, sort_keys=True, indent=4,ensure_ascii=False)


def print_playlists(parent_dir="./csv"):
    for dirname, dirnames, filenames in os.walk(parent_dir):
        for subdirname in dirnames:
            create_playlist(parent_dir, subdirname)



def create_playlist(parent_dir, pathname):
    songs = []
    for dirname_, dirnames_, filenames_ in os.walk(parent_dir+"/"+pathname):
        for f in filenames_:
            try:
                with open(parent_dir+"/"+pathname+'/Tracce/'+f) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    for row in csv_reader:
                        if line_count == 0:
                            line_count +=1
                            continue
                        else:
                            a = {
                            "title": row[0],
                            "artist": row[2],
                            "album": row[1],
                            'id': hash(row[0])
                            }
                    songs.append(a)
            except:
                continue
    write_data("playlists/"+pathname+".json",songs)


#print_playlists()