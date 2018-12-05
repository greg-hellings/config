def test_package_installed(host):
    assert host.package('fedora-review').is_installed
