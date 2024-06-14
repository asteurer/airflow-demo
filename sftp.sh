#!/bin/bash

docker pull atmoz/sftp

docker run -p 6000:22 -d -t atmoz/sftp \
  andyboi:asdf:1000::/home/andyboi

ssh-keygen -f "/home/andyboi/.ssh/known_hosts" -R "[localhost]:6000"

sudo chown -R 1000:1000 test-files
sudo chmod 755 test-files
sshfs andyboi@localhost:/home/andyboi test-files -p 6000

# sftp -P 6000 andyboi@localhost


