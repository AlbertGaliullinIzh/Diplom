#!/bin/bash

IP_monitoring="IP1"
list_IP=("IP1" "IP2")
list_interface=("Int1" "Int2")

apt install curl -y
apt install gpg -y

curl --proxy http://proxy.istu.ru:8080 -fsSL https://download.opensuse.org/repositories/security:zeek/Debian_12/Release.key |
gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/security_zeek.gpg > /dev/null
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
text1="$IP_monitoring/12       Private IP space"
text2="192.168.0.0/16      Private IP space"

cat /dev/null > "$file"

echo "$text1" >> "$file"
echo "$text2" >> "$file"

file="/opt/zeek/etc/node.cfg"

cat /dev/null > "$file"

echo "[zeek-logger]" >> "$file"
echo "type=logger" >> "$file"
echo "host=$IP_monitoring" >> "$file"
echo "" >> "$file"

echo "[zeek-manager]" >> "$file"
echo "type=manager" >> "$file"
echo "host=$IP_monitoring" >> "$file"
echo "" >> "$file"

echo "[zeek-proxy]" >> "$file"
echo "type=proxy" >> "$file"
echo "host=$IP_monitoring" >> "$file"


list_length=${#list_IP[@]}
counter=0
while [ $counter -lt $list_length ]; do
    echo "" >> "$file"
    echo "[zeek-worker-$counter]" >> "$file"
    echo "type=worker" >> "$file"
    echo "host=${list_IP[$counter]}" >> "$file"
    echo "interface=${list_interface[counter]}" >> "$file"    
    ((counter++))
done



echo " @load policy/tuning/json-logs.zeek" >> /opt/zeek/share/zeek/site/local.zeek
./zeekctl check
./zeekctl deploy



#echo "" >> "$file"
#echo "[zeek-worker-lo]" >> "$file"
#echo "type=worker" >> "$file"
#echo "host=localhost" >> "$file"
#echo "interface=lo" >> "$file"

#mkdir /bin/monitoringProccess
#cd -
#cp "DetectionScanningPorts.py" "/bin/monitoringProccess"
#sed -i "s/machineIP=""/machineIP=$IP_server/g" /bin/monitoringProccess/DetectionScanningPorts.py
