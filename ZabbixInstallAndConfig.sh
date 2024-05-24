#!/bin/bash

SI="172.31.2.2"

apt-get install update
apt-get install zabbix-agent -y

sed -i "s/Server=127.0.0.1/Server=$SI/g" /etc/zabbix/zabbix_agentd.conf
sed -i "s/ServerActive=127.0.0.1/ServerActive=$SI/g" /etc/zabbix/zabbix_agentd.conf

systemctl restart zabbix-agent
