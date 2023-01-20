#!/bin/bash

# List of packages to install
packages=("python3" "vlc" "python3-pip" "pulseaudio")

# Update package list
sudo apt-get update

# Loop through the package list and install each package
for package in "${packages[@]}"
do
    sudo apt-get install -y $package
done

# Upgrade any remaining packages
sudo apt-get upgrade -y

sudo pip3 install python-vlc

pulseaudio -D
