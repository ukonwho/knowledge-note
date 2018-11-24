# Nginx使用Let's Encrypt 给网站加 HTTPS

## 生成 Let's Encrypt 证书
### 1. 下载安装 certbot
安装很简单：

```
wget https://dl.eff.org/certbot-auto
chmod a+x certbot-auto
```

### 2. 创建配置文件
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

### 3. 执行证书自动化生成命令
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

## 配置 Nginx 加入证书
默认配置文件是这样的：
```
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    # Redirect all HTTP requests to HTTPS with a 301 Moved Permanently response.
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    # certs sent to the client in SERVER HELLO are concatenated in ssl_certificate
    ssl_certificate /path/to/signed_cert_plus_intermediates;
    ssl_certificate_key /path/to/private_key;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;

    # Diffie-Hellman parameter for DHE ciphersuites, recommended 2048 bits
    ssl_dhparam /path/to/dhparam.pem;

    # intermediate configuration. tweak to your needs.
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers 'ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:ECDHE-ECDSA-DES-CBC3-SHA:ECDHE-RSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:DES-CBC3-SHA:!DSS';
    ssl_prefer_server_ciphers on;

    # HSTS (ngx_http_headers_module is required) (15768000 seconds = 6 months)
    add_header Strict-Transport-Security max-age=15768000;

    # OCSP Stapling ---
    # fetch OCSP records from URL in ssl_certificate and cache them
    ssl_stapling on;
    ssl_stapling_verify on;

    ## verify chain of trust of OCSP response using Root CA and Intermediate certs
    ssl_trusted_certificate /path/to/root_CA_cert_plus_intermediates;

    resolver <IP DNS resolver>;

    ....
}
```

请根据自己的服务配置修改和添加内容，重点只需要关注6行：

```
server {
	listen 443 ssl http2;
	....
	ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
	ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
	ssl_dhparam /etc/nginx/ssl/dhparam.pem;

	ssl_trusted_certificate /etc/letsencrypt/live/example.com/root_ca_cert_plus_intermediates;

	resolver <IP DNS resolver>;
	....
}
```

这6行中，部分文件还不存在，逐个说明。

首先是第一行 listen 443 ssl http2; 作用是启用 Nginx 的 ngx_http_v2_module 模块 支持 HTTP2，Nginx 版本需要高于 1.9.5，且编译时需要设置 --with-http_v2_module 。Arch Linux 的 Nginx 安装包中已经编译了这个模块，可以直接使用。如果你的 Linux 发行版本中的 Nginx 并不支持这个模块，可以自行 Google 如何加上。

ssl_certificate 和 ssl_certificate_key ，分别对应 fullchain.pem 和 privkey.pem，这2个文件是之前就生成好的证书和密钥。

ssl_dhparam 通过下面命令生成:
```
$ mkdir /etc/nginx/ssl
$ openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048
```
（可选）ssl_trusted_certificate 需要下载 Let's Encrypt 的 Root Certificates，不过根据 Nginx 官方文档 所说，ssl_certificate 如果已经包含了 intermediates 就不再需要提供 ssl_trusted_certificate，这一步可以省略：
```
$ cd /etc/letsencrypt/live/example.com
$ wget https://letsencrypt.org/certs/isrgrootx1.pem
$ mv isrgrootx1.pem root.pem
$ cat root.pem chain.pem > root_ca_cert_plus_intermediates
```

resolver 的作用是 “resolve names of upstream servers into addresses”， 在這個配置中，resolver 是用來解析 OCSP 服務器的域名的，建议填写你的 VPS 提供商的 DNS 服务器，例如我的 VPN 在 Linode，DNS服务器填写：

resolver 106.187.90.5 106.187.93.5;

Nginx 配置完成后，重启后，用浏览器测试是否一切正常。
```
$ /usr/local/nginx/sbin/nginx -s reload
```
这时候你的站点应该默认强制使用了 HTTPS，并且浏览器地址栏左边会有绿色的小锁。

## 自动化定期更新证书
Let's Encrypt 证书有效期是3个月，我们可以通过 certbot 来自动化续期。




