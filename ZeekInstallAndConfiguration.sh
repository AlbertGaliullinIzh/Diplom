#!/bin/bash

IP=""

apt install curl

curl -fsSL https://download.opensuse.org/repositories/security:zeek/Debian_12/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/security_zeek.gpg > /dev/null
echo 'deb http://download.opensuse.org/repositories/security:/zeek/Debian_12/ /' | sudo tee /etc/apt/sources.list.d/security:zeek.list

apt update
apt install zeek-lts -y

echo "export PATH=$PATH:/opt/zeek/bin" >> ~/.bashrc
source ~/.bashrc
echo $PATH
which zeek
zeek --version
zeek --help

#config files
file="/opt/zeek/etc/networks.cfg"
text1="$IP/12       Private IP space"
text2="192.168.0.0/16      Private IP space"

cat /dev/null > "$file"

echo "$text1" >> "$file"
echo "$text2" >> "$file"

