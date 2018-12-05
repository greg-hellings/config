import pytest


@pytest.mark.parameterize('cmd', [
    ('g++'),
    ('jq'),
    ('python3'),
    ('tox'),
    ('ansible-lint'),
    ('make'),
    ('ffmpeg'),
    ('packer'),
    ('vagrant')
])
def test_command(host, cmd):
    assert host.exists(cmd)