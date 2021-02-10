# Spotify playlists converter (from local folder or Google Play Music)

This can be useful if you have uploaded your own music on Google Play Music, there are some tools that convert the playlists but not the one composed by music not present on the Play music store.

UPDATE

In this updated version you can even convert your local playlist folder in spotify playlists.

I hope it will works on all computers, since I have only tested on mine. This project could be helpful now that GPlayMusic is closing.

## How to configure

### PlayMusic configuration

1. **Navigate to [Google Takeout.](https://takeout.google.com/)**
Google Takeout is the central hub for anyone who wants to download their data from any of Google's products. It's also the place to grab your uploaded or purchased music as MP3s, along with metadata for your playlists, radio stations, and tracks in CSV format.
2. **Select Google Play Music.**
By default, all of the products are selected, so, to isolate Google Play Music, tap "Deselect all," scroll down to Google Play Music, and tap the checkbox next to it. Scroll all the way to the bottom and tap the "Next step" button to proceed.
3. Put the folder containg the csv inside the csv folder.
The structure should be:
    
    csv/*playlist_name/track/song_1.csv*

#### Old PlayMusic configuration (Not working anymore)

Google play music has been shutted down so this configuration is not needed anymore, so follow the NEXT configuration.

<del>
Unfortunately Google play music does not provide a method to see what are your device ids. So what we can do to discover what are ours we need to proceed in this way:

1. Launch the script gmusic.py
2. See the InvalidDeviceId exception and copy one on the authorized ids.
3. Paste into the config.yml file:
    ```yml
    device_id: 123456abcdf
    ```
</del>

### Spotify configuration

1. Go to [this link](https://developer.spotify.com/dashboard/applications) and create a new application
2. Now goto edit settings and add this redirect uri: http://localhost:5500
3. Copy the client id string and the client secret into the config.yml file:
    ```yml
    client_id: 123456abcdf12345qwerty
    client_secret: 123456abcdf12345qwerty
    ```
4. You have to find your Spotify account id, in order to do this share your profile link, and it should be after 'http://open.spotify.com/user/'. Copy the userid in the config.yml
    ```yml
    username: "12345678"
    ```

### General configuration

Execute the command to install the required packages:
```
pip install -r requirements.txt
```

### Local configuration

If you have playlist saved locally for example you have a folder with you rock music and you want to convert it into spotify, then this section is for you.
Put your playlist_folder inside the songs folder.
The structure should be: 

songs/*playlist_name/song_1.mp3*

## How to use

1. Launch the main script with argument -m amd the convert mode desired between f (from local files) and gp (from google play music csv). If you have saved the local files inside a different folder, specify it with the -p paramter.

```
python main.py -m gp -p path_to_local_playlist
```

### Second execution

If you have yet converted the playlist in a json format (done in a first execution with the main.py), you can run the spotify.py script stand alone.

Inserting the name of the playlist you want to convert. You will be asked to use differently method of research. Answer using "y" as yes and "n" as no.

The same concept apply for all the scripts, they can be runned standalone but without parameter, so you have to follow the folders structure proposed.
```
python spotify.py
```