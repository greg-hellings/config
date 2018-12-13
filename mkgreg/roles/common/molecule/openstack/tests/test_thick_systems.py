def test_selinux_disabled(host):
    conf = host.file('/etc/selinux/config')
    assert 'SELINUX=disabled' in conf.content


def test_sshd_enabled(host):
    service = host.service('sshd')
    assert service.is_running
    assert service.is_enabled
