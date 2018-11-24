# 给已经编译安装了的nginx 添加http_ssl_module和http_v2_module模块方法（让Web服务器支持SSL和http2）

## 1、看下编译安装nginx的时候，都编译安装的哪些模块。

```
[root@zabbix ~]# /usr/local/nginx/sbin/nginx -V

nginx version: nginx/1.10.2

built by gcc 4.4.7 20120313 (Red Hat 4.4.7-17) (GCC)

built with OpenSSL 1.0.1e-fips 11 Feb 2013

TLS SNI support enabled

configure arguments: –prefix=/usr/local/nginx
```

## 2、进入之前下载并解压了的源码包目录；重新编译nginx

```
[root@zabbix nginx-1.10.2]# cd /usr/local/src/nginx-1.10.0

[root@zabbix nginx-1.10.2]# ./configure –prefix=/usr/local/nginx –with-http_stub_status_module –with-http_ssl_module --with-http_v2_module

[root@zabbix nginx-1.10.2]# make
```
**这一步千万不能 make install ；不然会把之前已经安装的nginx 覆盖掉**

## 3、需要替换nginx二进制文件,先停止掉nginx进程；备份一下原来的启动脚本。
```
cp /usr/local/nginx/sbin/nginx /usr/local/nginx/sbin/nginx.old;

cp objs/nginx /usr/local/nginx/sbin/nginx;

```

## 4、查看nginx的模块，看下是否把需要的模块编译进去了
```
nginx -V
```

## 5、最后重新启动nginx
