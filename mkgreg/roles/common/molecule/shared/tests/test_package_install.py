import pytest


@pytest.mark.parametrize('name', [
    ('vim-enhanced'),
    ('git'),
    ('python2-libselinux'),
    ('mlocate'),
    ('screen'),
    ('openssh-server'),
    ('patch')
])
def test_package_installed(host, name):
    assert host.package(name).is_installed