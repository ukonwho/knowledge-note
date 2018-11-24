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

这里需要解释一下，上面配置文件用了 webroot 的验证方法，这种方法适用于已经有一个 Web Server 运行中的情况。certbot 会自动在 /var/www/example 下面创建一个隐藏文件 .well-known/acme-challenge ，通过请求这个文件来验证 example.com 确实属于你。外网服务器访问 http://www.example.com/.well-known/acme-challenge ，如果访问成功则验证OK。

我们不需要手动创建这个文件，certbot 会根据配置文件自动完成。

## 3. 执行证书自动化生成命令
一切就绪，我们现在可以运行 certbot 了。
```
$ certbot-auto -c /etc/letsencrypt/configs/example.com.conf certonly

## 片刻之后，看到下面内容就是成功了
IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at /etc/letsencrypt/live/example.com/fullchain.pem.
 
```
如果运行顺利，所有服务器所需要的证书就已经生成好了。他们被放在了 /etc/letsencrypt/live/example.com/ 下：
```
$ ls /etc/letsencrypt/live/example.com/
cert.pem #server cert only
privkey.pem #private key
chain.pem #intermediates
fullchain.pem #server cert + intermediates
```






