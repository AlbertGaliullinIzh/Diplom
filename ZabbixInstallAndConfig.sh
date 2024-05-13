#!/bin/bash

SI=""

#dpkg -i zabbix-release_6.4-1+debian12_all.deb
#apt-get install -f -y

apt-get install update
apt-get install zabbix-agent -y

#sed -i "s/ServerActive=/ServerActive=$SI/g" /etc/zabbix/zabbix_agentd.conf
#sed -i "s/Server=/Server=$SI/g" /etc/zabbix/zabbix_agentd.conf

sed -i "s/Server=127.0.0.1/Server=$SI/g" /etc/zabbix/zabbix_agentd.conf
sed -i "s/ServerActive=127.0.0.1/ServerActive=$SI/g" /etc/zabbix/zabbix_agentd.conf

systemctl restart zabbix-agent
