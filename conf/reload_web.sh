#!/bin/sh
default_nginx_conf_path=/etc/nginx/conf.d/fls.conf
all_nginx_conf_path=/etc/nginx/conf.d/fls.conf.all
master_nginx_conf_path=/etc/nginx/conf.d/fls.conf.masteronly
slave_nginx_conf_path=/etc/nginx/conf.d/fls.conf.slaveronly

# switch to slaveronly
yes|cp $slave_nginx_conf_path $default_nginx_conf_path
nginx -s reload
sleep 2

# sync master
cd /root/workspace/fls/master
git pull  

master_list=(
fls_master:fls_m0
fls_master:fls_m1
)
slave_list=(
fls_slave:fls_s0
fls_slave:fls_s1
)
# restart master_list
for item in ${master_list[@]}
    do supervisorctl -c  /root/conf/supervisor/super.conf restart $item
done

sleep 2
# switch to masteronly
yes| cp $master_nginx_conf_path $default_nginx_conf_path
nginx -s reload
sleep 3

# sync slave
cd /root/workspace/fls/slave
git pull  

# restart slave_list
for item in ${slave_list[@]}
    do supervisorctl -c  /root/conf/supervisor/super.conf restart $item
done

sleep 2
# switch to all
yes| cp $all_nginx_conf_path $default_nginx_conf_path
nginx -s reload