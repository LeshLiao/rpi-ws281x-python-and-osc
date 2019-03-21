#!/bin/bash
cd rpi-ws281x-python-and-osc
git checkout master
git reset --hard 
sudo chmod 777 -R .git/objects
cd .git/objects
sudo chown -R : *
git pull
