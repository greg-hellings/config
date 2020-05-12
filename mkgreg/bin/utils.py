from __future__ import print_function

from os import path
from plumbum import local
from plumbum.commands.processes import ProcessExecutionError
from traceback import print_exc

import sys

TOP = path.normpath(path.join(path.dirname(__file__), '..'))
REQUIREMENTS = path.join(TOP, 'requirements.yml')


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


def install_dependencies():
    galaxy = local['ansible-galaxy']
    try:
        galaxy.run(['install', '-f', '-r', REQUIREMENTS], stdout=sys.stdout,
                   stderr=sys.stderr)
        galaxy.run(['collection', 'install', '-f', '-r', REQUIREMENTS],
                   stdout=sys.stdout, stderr=sys.stderr)
    except ProcessExecutionError as ex:
        print('Error installing Galaxy dependencies')
        print(ex.stderr, file=sys.stderr)
        print_exc()
        sys.exit(ex.retcode)
    except Exception as ex:
        print('Unknown error occurred: {0}'.format(ex), file=sys.stderr)
        print_exc()
        sys.exit(255)
