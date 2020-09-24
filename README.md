# Google Play Music to Spotify playlists converter
This can be useful if you have uploaded your own music on Google Play Music, there are some tools that convert the playlists but not the one composed by music not present on the Play music store.

I hope it will works on all computers, since I have only tested on mine. This project could be helpful now that GPlayMusic is closing.

## How to configure

### PlayMusic configuration
Unfortunately Google play music does not provide a method to see what are your device ids. So what we can do to discover what are ours we need to proceed in this way:

1. Launch the script gmusic.py
2. See the InvalidDeviceId exception and copy one on the authorized ids.
3. Paste into the config.yml file:
    ```yml
    device_id: 123456abcdf
    ```
    
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

## How to use

The first operation has to be done only the first time, and if and only if we update some of the playlists on Google Play Music.

1. Launch the gmusic.py script and follow the instructions to past correctly the oauth token
```
python gmusic.py
```

2. Launch the spotify.py script and insert the name of the playlist you want to convert. You will be asked to use differently method of research. Answer using "y" as yes and "n" as no.
```
python spotify.py
```