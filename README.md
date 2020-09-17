# spotiplay
A very basic command line tool to import google play music playlists to spotify.

Before you get started, you are going to need to an account on Spotify and register an app on the [Dashboard](https://developer.spotify.com/dashboard/applications) to get the credentials used. Be sure to set the redirect URI to http://localhost:8888 to enable it to use your local web browser for authentication. 

You will also need to set three environmental variables:
```
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='http://localhost:8888'
```

Next, clone the repo and make a virtual environment for the project. Run 'make all'. That will download all of the requirements  and run the tests to make sure it's all working.

If the test works, try it on an exported Google Play Music Playlist folder from Google Takeout. Note that I ran detox on the folders because of all of the spaces and characters that are sent down with the export. The command looks like:

```
$ python spotiplay.py create-playlist /home/rob/Takeout/Google_Play_Music/Playlists/Thumbs_Up/ --name "GPM Thumbs Up" --description "Thumbs up tracks from Google Play Music"

```
It's not 100% (maybe because the names vary?) and YMMV (I got 752 out of 803 from my Thumbs Up list) but was able to find and add most of the tracks to Spotify playlists and beats doing it by hand. 

Notes:
- the first time you run it, you will have to allow the scope on the Spotify service
- pytest will occassional fail due to service unavailability (503 error)
- I didn't see a way of deleting playlists so I used unfollow which seems to do the same thing
