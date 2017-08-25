from __future__ import print_function

from os import path
from plumbum import local
from plumbum.commands.processes import ProcessExecutionError
from traceback import print_exc

import sys

TOP = path.normpath(path.join(path.dirname(__file__), '..'))
INVENTORIES = {
    'gui' : path.join(TOP, 'inventories', 'gui'),
    'cli' : path.join(TOP, 'inventories', 'cli'),
    'dev' : path.join(TOP, 'inventories', 'dev'),
    'user' : path.join(TOP, 'inventories', 'user')
}


def call_ansible(inventory, playbook, *args):
    ansible_args = [
        path.join(TOP, playbook),
        '-i', inventory,
        '--ssh-common-args=-o StrictHostKeyChecking=no'
    ]
    ansible_args.extend(args)
    ansible = local['ansible-playbook']
    try:
        ansible.run(ansible_args, stdout=sys.stdout, stderr=sys.stderr)
    except ProcessExecutionError as ex:
        print('Error encountered while executing Ansible', file=sys.stderr)
        print(ex.stderr, file=sys.stderr)
        print_exc()
        sys.exit(ex.retcode)
    except Exception as ex:
        print('Unknown error occurred: {0}'.format(ex), file=sys.stderr)
        print_exc()
        sys.exit(255)
