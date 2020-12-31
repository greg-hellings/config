#!/usr/bin/env python
from __future__ import print_function
from argparse import ArgumentParser
from os import path
from .utils import call_ansible, install_dependencies


parser = ArgumentParser(description="Configures a system for Greg's use")
dirname = path.dirname(__file__)
default_inventory = path.join(dirname, "hosts")


def mkgreg(playbook='site.yml', more_args=[]):
    parser.add_argument('-i', '--inventory-file', default=default_inventory,
                        dest='inv', help='Ansible inventory file')
    args, extra_args = parser.parse_known_args()
    # Requires that an inventory be present
    if args.inv is None or not path.exists(args.inv):
        raise Exception('An inventory file must be specified')
    #install_dependencies()
    call_ansible(args.inv, playbook, extra_args + more_args)


def mkgreg_sudo():
    mkgreg(playbook='sudo.yml', more_args=['-K'])


def mkgreg_openwrt():
    mkgreg(playbook='openwrt.yml')


def mkgreg_authkey():
    mkgreg(playbook='authorized_key.yml', more_args=['-k'])

def mkgreg_dotfiles():
    mkgreg(playbook='userland.yml')
