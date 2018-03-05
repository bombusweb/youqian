#!/bin/sh
/usr/local/bin/redis-server  /etc/redis/6379.conf
nginx
gearmand -d -L 0.0.0.0
/usr/bin/supervisord -c /root/workspace/haichengyuan/conf/supervisor/super.conf
supervisorctl -c  /root/workspace/haichengyuan/conf/supervisor/super.conf restart all