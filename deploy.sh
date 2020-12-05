#!/usr/bin/bash

$(cd /home/guillaume/pur-beurre-p11)
$(git pull)
$(tox -e prod)
$(supervisorctl restart pur-beurre-p11)
$(exit)
