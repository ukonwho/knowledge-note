# Supervisor 安装配置和使用详解

## Supervisor
Supervisor 是用Python开发的一个client/server服务，是Linux/Unix系统下的一个进程管理工具，不支持Windows系统。它可以很方便的监听、启动、停止、重启一个或多个进程。用Supervisor管理的进程，当一个进程意外被杀死，supervisort监听到进程死后，会自动将它重新拉起，很方便的做到进程自动恢复的功能，不再需要自己写shell脚本来控制。（http://supervisord.org/）

## 安装
由于搜索的各种教程在我的虚拟机测试有行不通，我们就直接简单的源码安装

首先确定你使用的root用户

## python3.x上supervisor安装
supervisor依赖于meld3包所以将它一块下载

```
wget https://share.imwnk.cn/down/Other/meld3-1.0.2.tar.gz
```

安装 supervisor 支持 python3 的版本

```
pip install git+https://github.com/Supervisor/supervisor@master
```

或者git clone 后，直接用 **python setup.py install** 安装


## 检查安装是否成功
安装完成之后多了3个工具：echo_supervisord_conf、supervisorctl和supervisord。

### 重启supervisord进程
```
supervisorctl -c supervisord.conf reload
```

注意：每次修改配置文件，都需要执行此命令。

### supervisorctl的用法
```
supervisord : 启动supervisor
supervisorctl reload :修改完配置文件后重新启动supervisor
supervisorctl status :查看supervisor监管的进程状态
supervisorctl start 进程名 ：启动XXX进程
supervisorctl stop 进程名 ：停止XXX进程
supervisorctl stop all：停止全部进程，注：start、restart、stop都不会载入最新的配置文件。
supervisorctl update：根据最新的配置文件，启动新配置或有改动的进程，配置没有改动的进程不会受影响而重启
```

## 开机启动Supervisor服务
### 配置systemctl服务
1.进入 /lib/systemd/system 目录，并创建supervisord.service文件写入以下代码

```
[Unit]
Description=supervisor
After=network.target

[Service]
Type=forking
ExecStart=/usr/bin/supervisord -c /etc/supervisord.conf
ExecStop=/usr/bin/supervisorctl $OPTIONS shutdown
ExecReload=/usr/bin/supervisorctl $OPTIONS reload
KillMode=process
Restart=on-failure
RestartSec=42s

[Install]
WantedBy=multi-user.target
```

2.设置开机启动

```
systemctl enable supervisord.service
systemctl daemon-reload
```

3.修改文件权限为766

```
chmod 766 supervisord.service
```

### 配置service类型服务
```
#!/bin/bash
#
# supervisord   This scripts turns supervisord on
#
# Author:       Mike McGrath <mmcgrath@redhat.com> (based off yumupdatesd)
#
# chkconfig:    - 95 04
#
# description:  supervisor is a process control utility.  It has a web based
#               xmlrpc interface as well as a few other nifty features.
# processname:  supervisord
# config: /etc/supervisor/supervisord.conf
# pidfile: /var/run/supervisord.pid
#

# source function library
. /etc/rc.d/init.d/functions

RETVAL=0

start() {
    echo -n $"Starting supervisord: "
    daemon "supervisord -c /etc/supervisord.conf "
    RETVAL=$?
    echo
    [ $RETVAL -eq 0 ] && touch /var/lock/subsys/supervisord
}

stop() {
    echo -n $"Stopping supervisord: "
    killproc supervisord
    echo
    [ $RETVAL -eq 0 ] && rm -f /var/lock/subsys/supervisord
}

restart() {
    stop
    start
}

case "$1" in
  start)
    start
    ;;
  stop) 
    stop
    ;;
  restart|force-reload|reload)
    restart
    ;;
  condrestart)
    [ -f /var/lock/subsys/supervisord ] && restart
    ;;
  status)
    status supervisord
    RETVAL=$?
    ;;
  *)
    echo $"Usage: $0 {start|stop|status|restart|reload|force-reload|condrestart}"
    exit 1
esac

exit $RETVAL
```

将上述脚本内容保存到/etc/rc.d/init.d/supervisord文件中，修改文件权限为755，并设置开机启动

```
chmod 755 /etc/rc.d/init.d/supervisord
chkconfig supervisord on
```

启动演示

```
 service supervisord reload
 supervisorctl status
```

## 其他
* 默认配置文件：/etc/supervisord.conf

* 进程管理配置文件放到：/etc/supervisor/目录下即可

* Supervisor只能管理非daemon的进程，也就是说Supervisor不能管理守护进程。否则提示Exited too quickly (process log may have details)异常。

* Supervisord主要用来管理进程，而不是调度任务，因此如果有定时任务的需求，跟结合crontab一起使用。

## program配置模板
* 完整

```
[program:cat]
command=/bin/cat
process_name=%(program_name)s
numprocs=1
directory=/tmp
umask=022
priority=999
autostart=true
autorestart=true
startsecs=10
startretries=3
exitcodes=0,2
stopsignal=TERM
stopwaitsecs=10
user=chrism
redirect_stderr=false
stdout_logfile=/a/path
stdout_logfile_maxbytes=1MB
stdout_logfile_backups=10
stdout_capture_maxbytes=1MB
stderr_logfile=/a/path
stderr_logfile_maxbytes=1MB
stderr_logfile_backups=10
stderr_capture_maxbytes=1MB
environment=A="1",B="2"
serverurl=AUTO
```

* 简化

```
[program:test]
command=python test.py
directory=/home/supervisor_test/
autorestart=true
stopsignal=INT
user=root
stdout_logfile=test_out.log
stdout_logfile_maxbytes=1MB
stdout_logfile_backups=10
stdout_capture_maxbytes=1MB
stderr_logfile=test_err.log
stderr_logfile_maxbytes=1MB
stderr_logfile_backups=10
stderr_capture_maxbytes=1MB
```

* 说明 为必须填写项; [program:应用名称][program:cat]

```
;*命令路径,如果使用python启动的程序应该为 python /home/test.py, 
;不建议放入/home/user/, 对于非user用户一般情况下是不能访问
command=/bin/cat

;当numprocs为1时,process_name=%(program_name)s
;当numprocs>=2时,%(program_name)s_%(process_num)02d
process_name=%(program_name)s

;进程数量
numprocs=1

;执行目录,若有/home/supervisor_test/test1.py
;将directory设置成/home/supervisor_test
;则command只需设置成python test1.py
;否则command必须设置成绝对执行目录
directory=/tmp

;掩码:--- -w- -w-, 转换后rwx r-x w-x
umask=022

;优先级,值越高,最后启动,最先被关闭,默认值999
priority=999

;如果是true,当supervisor启动时,程序将会自动启动
autostart=true

;*自动重启
autorestart=true

;启动延时执行,默认1秒
startsecs=10

;启动尝试次数,默认3次
startretries=3

;当退出码是0,2时,执行重启,默认值0,2
exitcodes=0,2

;停止信号,默认TERM
;中断:INT(类似于Ctrl+C)(kill -INT pid),退出后会将写文件或日志(推荐)
;终止:TERM(kill -TERM pid) //信号量参考文章（http://c.biancheng.net/cpp/html/2784.html）
;挂起:HUP(kill -HUP pid),注意与Ctrl+Z/kill -stop pid不同
;从容停止:QUIT(kill -QUIT pid)
;KILL, USR1, USR2其他见命令(kill -l),说明1
stopsignal=TERM

stopwaitsecs=10

;*以root用户执行
user=root

;重定向
redirect_stderr=false

stdout_logfile=/a/path
stdout_logfile_maxbytes=1MB
stdout_logfile_backups=10
stdout_capture_maxbytes=1MB
stderr_logfile=/a/path
stderr_logfile_maxbytes=1MB
stderr_logfile_backups=10
stderr_capture_maxbytes=1MB

;环境变量设置
environment=A="1",B="2"

serverurl=AUTO
```

## 解决supervisor.sock no such file 的问题
1. 打开配置文件

```
vim /etc/supervisord.conf
```

这里把所有的/tmp路径改掉，/tmp/supervisor.sock 改成 /var/run/supervisor.sock，/tmp/supervisord.log 改成 /var/log/supervisor.log，/tmp/supervisord.pid 改成 /var/run/supervisor.pid 要不容易被linux自动清掉

2. 修改权限

```
sudo chmod 777 /run
sudo chmod 777 /var/log
```

如果没改，启动报错 IOError: [Errno 13] Permission denied: '/var/log/supervisord.log'

3. 创建supervisor.sock

```
sudo touch /var/run/supervisor.sock
sudo chmod 777 /var/run/supervisor.sock
```

4. 启动supervisord，注意stop之前的实例或杀死进程


## 参考文档：

1. [https://blog.csdn.net/python36/article/details/80571888](https://blog.csdn.net/python36/article/details/80571888) 

2. [https://blog.csdn.net/xyang81/article/details/51555473](https://blog.csdn.net/xyang81/article/details/51555473) 

3. [https://thief.one/2018/06/01/1/ ](https://thief.one/2018/06/01/1/)

4. [https://www.cnblogs.com/sfnz/p/5578417.html ](https://www.cnblogs.com/sfnz/p/5578417.html)

5. [https://blog.csdn.net/xyang81/article/details/51555473](https://blog.csdn.net/xyang81/article/details/51555473)


