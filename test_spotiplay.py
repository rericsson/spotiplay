from click.testing import CliRunner
from spotiplay import cli


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
    assert "No subcommand invoked." in result.output


def test_get_playlists():
    runner = CliRunner()
    result = runner.invoke(cli, ["get-playlists"])
    assert result.exit_code == 0


def test_create_and_unfollow_playlist():
    runner = CliRunner()
    result = runner.invoke(
        cli, ["create-playlist", "./test_data/covers/", "--name", "Foo"]
    )
    assert result.exit_code == 0
    result = runner.invoke(cli, ["unfollow-playlist", "--name", "Foo"])
    assert result.exit_code == 0
