#!/bin/bash

apt update && apt install curl gnupg2 -y
echo 'deb http://download.opensuse.org/repositories/security:/zeek/Debian_12/ /' > /etc/apt/sources.list.d/zeek.list
curl -fsSL https://download.opensuse.org/repositories/security:zeek/Debian_12/Release.key | gpg --dearmor > /etc/apt/trusted.gpg.d/security_zeek.gpg

apt install zeek
apt install zeekctl
