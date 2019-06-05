#!/usr/bin/env python
from __future__ import print_function
from argparse import ArgumentParser
from os import path
from .utils import INVENTORIES, call_ansible, install_dependencies


parser = ArgumentParser(description="Configures a system for Greg's use")


def mkgreg(default=None, playbook='site.yml'):
    parser.add_argument('-i', '--inventory-file', default=default, dest='inv',
                        help='Ansible inventory file')
    args, extra_args = parser.parse_known_args()
    # Requires that an inventory be present
    if args.inv is None or not path.exists(args.inv):
        raise Exception('An inventory file must be specified')
    install_dependencies()
    call_ansible(args.inv, playbook, extra_args)


def mkgreg_gui():
    mkgreg(INVENTORIES['gui'])


def mkgreg_cli():
    mkgreg(INVENTORIES['cli'])


def mkgreg_dev():
    mkgreg(INVENTORIES['dev'])


def mkgreg_user():
    mkgreg(INVENTORIES['user'])


def mkgreg_sudo():
    mkgreg(playbook='sudo.yml')
