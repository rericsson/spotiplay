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
