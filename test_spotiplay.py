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

def test_get_track():
    runner = CliRunner()
    result = runner.invoke(cli, ["get-track", "--title", "Sunspots", "--artist", "Julian Cope"])
    assert result.exit_code == 0
    assert "Sunspots: 3kqG0YpTHcg2oPG6cDB8jx" in result.output
