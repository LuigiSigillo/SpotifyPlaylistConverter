from ShazamAPI import Shazam
import json
import os
import glob

def write_data(filename,songs):
    with open(filename, 'w', encoding="utf-8") as fp:
        json.dump(songs, fp, sort_keys=True, indent=4,ensure_ascii=False)


def do_playlist(pl_name):
	d = []

	for f in glob.glob(os.path.join("./songs/"+pl_name, '*.mp3')):

		mp3_file_content_to_recognize = open(f, 'rb').read()

		shazam = Shazam(mp3_file_content_to_recognize)
		recognize_generator = shazam.recognizeSong()

		a = next(recognize_generator)[1]# current offset & shazam response to recognize requests
		try:
			it = {}
			it["id"] = a['tagid']
			it["title"] = a['track']['title']
			it["artist"] = a['track']['subtitle']
			it["album"] = a['track']['sections'][0]['metadata'][0]['text']
			d.append(it)
			continue
		except:
			print(f)

	write_data(pl_name+".json",d)




for dirname, dirnames, filenames in os.walk('./songs'):
	for subdirname in dirnames:
		print(subdirname)
		do_playlist(subdirname)