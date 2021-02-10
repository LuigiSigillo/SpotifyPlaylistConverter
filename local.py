import os
import win32com.client
import json

def get_data(filename):
    with open(filename, 'r', encoding="utf-8") as fp:
        return json.load(fp)

def write_data(filename,songs):
    with open(filename, 'w', encoding="utf-8") as fp:
        json.dump(songs, fp, sort_keys=True, indent=4,ensure_ascii=False)



def convert_local(pathname):
    sh=win32com.client.gencache.EnsureDispatch('Shell.Application',0)
    ns = sh.NameSpace(pathname)
    colnum = 0
    columns = []
    while True:
        colname=ns.GetDetailsOf(None, colnum)
        if not colname:
            break
        columns.append(colname)
        colnum += 1
    dic = []
    for item in ns.Items():
        #print (item.Name)
        it = {}
        for colnum in range(len(columns)):
            colval=ns.GetDetailsOf(item, colnum)
            if colval:
                if columns[colnum] =="Nome":
                    #print(columns[colnum],":", colval)
                    it["title"] = colval.replace("CD","")
                elif columns[colnum] =="Autori":
                    it["artist"] = colval
                elif columns[colnum] =="Album":
                    it["album"] = colval
        it["id"] = hash(it['title'])
        dic.append(it)
    return dic

def print_dir(pathname="./songs"):
    for dirname, dirnames, filenames in os.walk(pathname):
        for subdirname in dirnames:
            print(subdirname)


def main_local(path):
    print_dir(path)
    pl_name = input("Insert playlist name\n")
    write_data("playlists/"+pl_name+".json",convert_local(r'./songs/'+pl_name))


if __name__ == "__main__":
    main_local()
#data = get_data("./playlists/"+playlist_name+".json")

