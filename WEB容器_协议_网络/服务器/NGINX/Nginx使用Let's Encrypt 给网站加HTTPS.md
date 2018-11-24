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
把 example.com 替换成自己的域名，配置文件内容：

```
# 写你的域名和邮箱
domains = example.com
rsa-key-size = 2048
email = your-email@example.com
text = True

# 把下面的路径修改为 example.com 的目录位置
authenticator = webroot
webroot-path = /var/www/example

```