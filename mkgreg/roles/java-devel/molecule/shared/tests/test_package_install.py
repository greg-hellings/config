import pytest


@pytest.mark.parameterize('name', [
    ('java-1.8.0-openjdk-headless'),
    ('java-11-openjdk-headless'),
    ('maven')
])
def test_package_installed(host, name):
    assert host.package(name).is_installed
