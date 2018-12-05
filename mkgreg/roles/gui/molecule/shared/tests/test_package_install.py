def test_package_installed(host):
    assert host.package("sound-juicer").is_installed
