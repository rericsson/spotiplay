#!/usr/bin/env python
"""This is a cli for working with spotify"""

import sys
import click
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def show_tracks(tracks):
    """Displays the tracks"""

    for i, item in enumerate(tracks['items']):
        track = item['track']
        print(f"{i} {track['artists'][0]['name']}-{track['name']}")

def show_playlist(sp, playlist):
    """Displays playlist"""

    print()
    print(f"{playlist['name']}")
    print(f"  tracks:{playlist['tracks']['total']}")
    results = sp.playlist(playlist['id'], fields='tracks, next')
    tracks = results['tracks']
    show_tracks(tracks)
    while tracks['next']:
        tracks = sp.next(tracks)
        show_tracks(tracks)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("No subcommand invoked. Try --help option.")
    else:
        click.echo("Invoking: %s" % ctx.invoked_subcommand)


@cli.command()
@click.option("--mine/--not-mine", default=False, help="Display all playlists (--not-mine) or just my creations (--mine)")
def get_playlists(mine):
    """Retrieves Spotify playlists for logged in user"""

    scope = "playlist-read-private"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    me = sp.current_user()
    playlists = sp.current_user_playlists()

    for playlist in playlists['items']:
        if mine:
            if playlist['owner']['id'] == me['id']:
                show_playlist(sp, playlist)
        else:
            show_playlist(sp, playlist)



@cli.command()
@click.option("--title", required=True, help="Track title to look up")
@click.option("--artist", help="Track artist")
def get_track(title, artist):
    """Gets the title id for the given track"""

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
    q = f"track:{title} artist:{artist}"
    tracks = sp.search(q)
    for track in tracks['tracks']['items']:
        print(f"{track['name']}: {track['id']}")


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
