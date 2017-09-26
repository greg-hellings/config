#!/usr/bin/env python
from __future__ import print_function
from argparse import ArgumentParser
from os import path
from utils import INVENTORIES, call_ansible


parser = ArgumentParser(description="Configures a system for Greg's use")


def mkgreg(default=None):
    parser.add_argument('-i', '--inventory-file', default=default, dest='inv',
                        help='Ansible inventory file')
    args, extra_args = parser.parse_known_args()
    print(args.inv)
    # Requires that an inventory be present
    if args.inv is None or not path.exists(args.inv):
        raise Exception('An inventory file must be specified')
    call_ansible(args.inv, 'site.yml', extra_args)


def mkgreg_gui():
    mkgreg(INVENTORIES['gui'])


def mkgreg_cli():
    mkgreg(INVENTORIES['cli'])


def mkgreg_dev():
    mkgreg(INVENTORIES['dev'])


def mkgreg_user():
    mkgreg(INVENTORIES['user'])
