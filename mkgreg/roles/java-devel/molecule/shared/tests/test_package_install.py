import pytest


@pytest.mark.parametrize('name', [
    ('java-latest-openjdk-headless'),
    ('maven')
])
def test_package_installed(host, name):
    assert host.package(name).is_installed
