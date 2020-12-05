#!/usr/bin/bash

cd "/home/guillaume/pur-beurre-p11"

$(git pull)
$(tox -e prod)
