#!/usr/bin/env sh
set -ve
TOP="$(readlink -f "$(dirname "$0")/..")"
# Set config file path
ANSIBLE_CONFIG="${TOP}/ansible.cfg"
export ANSIBLE_CONFIG
# Run ansible
ansible-playbook -i "${TOP}/inventories/desktop/hosts" \
    "${TOP}/site.yml" \
    -K \
    "$@"
