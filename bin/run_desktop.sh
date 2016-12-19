#!/usr/bin/env sh
set -ve
TOP="$(readlink -f "$(dirname "$0")/..")"
ansible-playbook -i "${TOP}/inventories/desktop/hosts" \
    "${TOP}/site.yml" \
    -K \
    "$@"
