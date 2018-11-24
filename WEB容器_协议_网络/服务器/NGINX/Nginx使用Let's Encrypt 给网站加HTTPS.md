# Nginx使用Let's Encrypt 给网站加 HTTPS

## 1. 下载安装 certbot
安装很简单：

```
wget https://dl.eff.org/certbot-auto
chmod a+x certbot-auto
```

## 2. 创建配置文件
先创建存放配置文件的文件夹：
```
mkdir /etc/letsencrypt/configs

```
编辑配置文件：
```
vim /etc/letsencrypt/configs/example.com.conf

```
