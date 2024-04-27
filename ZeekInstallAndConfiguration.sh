#!/bin/bash

IP=""
interface=""

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

file="/opt/zeek/etc/node.cfg"

cat /dev/null > "$file"


echo "[zeek-logger]" >> "$file"
echo "type=logger" >> "$file"
echo "host=$IP" >> "$file"

echo "" >> "$file"
echo "[zeek-manager]" >> "$file"
echo "type=manager" >> "$file"
echo "host=$IP" >> "$file"
echo "" >> "$file"
echo "[zeek-proxy]" >> "$file"
echo "type=proxy" >> "$file"
echo "host=$IP" >> "$file"

echo "" >> "$file"
echo "[zeek-worker]" >> "$file"
echo "type=worker" >> "$file"
echo "host=$IP" >> "$file"
echo "interface=$interface" >> "$file"

echo "" >> "$file"
echo "[zeek-worker-lo]" >> "$file"
echo "type=worker" >> "$file"
echo "host=localhost" >> "$file"
echo "interface=lo" >> "$file"

cd /opt/zeek/bin
./zeekctl check
./zeekctl deploy

cd /opt/zeek/logs
file_url="https://github.com/AlbertGaliullinIzh/Diplom/blob/master/DetectionScanningPorts.py"
file="DetectionScanningPorts.py"

wget -O "$file" "$file_url"

