#!/usr/bin/env python
"""This is a cli for working with spotify"""

import sys
import click
import glob
import html
import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def show_tracks(tracks):
    """Displays the tracks"""

    for i, item in enumerate(tracks["items"]):
        track = item["track"]
        print(f"{i} {track['artists'][0]['name']}-{track['name']}")


def show_playlist(sp, playlist):
    """Displays playlist"""

    print()
    print(f"{playlist['name']}")
    print(f"  tracks:{playlist['tracks']['total']}")
    results = sp.playlist(playlist["id"], fields="tracks, next")
    tracks = results["tracks"]
    show_tracks(tracks)
    while tracks["next"]:
        tracks = sp.next(tracks)
        show_tracks(tracks)


def get_track(title, artist):
    """Gets the list of title id for the given track"""

    track_ids = []
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
    q = f"track:{title} artist:{artist}"
    tracks = sp.search(q)
    for track in tracks["tracks"]["items"]:
        track_ids.append(track["id"])
    return track_ids


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("No subcommand invoked. Try --help option.")
    else:
        click.echo("Invoking: %s" % ctx.invoked_subcommand)


@cli.command()
@click.option(
    "--mine/--not-mine",
    default=False,
    help="Display all playlists (--not-mine) or just my creations (--mine)",
)
def get_playlists(mine):
    """Retrieves Spotify playlists for logged in user"""

    scope = "playlist-read-private"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    me = sp.current_user()
    playlists = sp.current_user_playlists()

    for playlist in playlists["items"]:
        if mine:
            if playlist["owner"]["id"] == me["id"]:
                show_playlist(sp, playlist)
        else:
            show_playlist(sp, playlist)


@cli.command()
@click.argument("source", type=click.Path(exists=True))
@click.option("--name", required=True, help="Name of playlist")
@click.option("--description", help="Description of playlist")
def create_playlist(source, name, description):
    """Create a playlist for the current user"""

    scope = "playlist-modify-public"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    me = sp.current_user()
    # create a playlist
    playlist = sp.user_playlist_create(
        me["id"], name=name, description=description, public=True
    )
    playlist_id = playlist["id"]

    # add the tracks from the Google Play Music playlist folder
    print(source)
    for filename in glob.glob(f"{source}/*.csv"):
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # the contents of the csv file are html encoded
                title = html.unescape(row["Title"])
                artist = html.unescape(row["Artist"])
                # get the tracks for the title and artist
                # there might be quite a few different versions
                track_ids = get_track(title=title, artist=artist)
                # if we get a result, take the first one(???) and add it.
                if track_ids:
                    sp.playlist_add_items(playlist_id, [track_ids[0]])
                else:
                    print(f"Could not find {title} by {artist}")

    # show what we created
    show_playlist(sp, playlist)


@cli.command()
@click.option("--name", required=True, help="Name of playlist")
def unfollow_playlist(name):
    """Unfollow a playlist"""

    scope = "playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    me = sp.current_user()
    playlists = sp.current_user_playlists()

    # get my playlists
    for playlist in playlists["items"]:
        if playlist["owner"]["id"] == me["id"]:
            if playlist["name"] == name:
                sp.current_user_unfollow_playlist(playlist["id"])


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
