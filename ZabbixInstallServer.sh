wget
http://repo.zabbix.com/zabbix/3.2/debian/pool/main/z/zabbix-release/zabbix-release_3.2-1+jessie_all.deb
dpkg -i zabbix-release_3.2-1+jessie_all.deb
apt-get update

apt-get install zabbix-server-mysql zabbix-agent zabbix-frontend-php -y

mysql -uroot -p

create database zabbix character set utf8 collate utf8_bin;

grant all privileges on zabbix.* to zabbix@localhost identified by 'primer1';

exit;

zcat /usr/share/doc/zabbix-server-mysql/create.sql.gz | mysql -uzabbix -p zabbix
