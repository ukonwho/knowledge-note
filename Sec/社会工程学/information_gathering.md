

# Reconnaissance

## 1. Domain

### 1.1. collect subdomain

* [Sublist3r](https://github.com/aboul3la/Sublist3r)

> Sublist3r enumerates subdomains using many search engines such as 
> Google, Yahoo, Bing, Baidu, and Ask. Sublist3r also enumerates 
> subdomains using Netcraft, Virustotal, ThreatCrowd, DNSdumpster, and 
> ReverseDNS.
>
> Subbrute was integrated with Sublist3r to increase the possibility of 
> finding more subdomains using bruteforce with an improved wordlist.

```
pip install -r requirements.txt
# 注意需要使用ladder
python sublist3r.py -h
proxychains python sublist3r.py -d target.com -b -v # 实时结果
proxychains python sublist3r.py -d target.com -b -o output.txt #存成文本
note that you need turn the /etc/proxychains quite_mode option on
```

* [subDomainBrute](https://github.com/lijiejie/subDomainsBrute.git)

```
python subDomainsBrute.py target.com
```

* [dnscan](https://github.com/rbsec/dnscan)

> dnscan is a python wordlist-based DNS subdomain scanner. The script will first try to perform a zone transfer using each of the target domain's nameservers.If this fails, it will lookup TXT and MX records for the domain, and then perform a recursive subudomain scan using the supplied wordlist.

```
python dnscan.py -h
python dnscan.py -d target.com
```

* dnsmap

```
# kali-builtin
dnsmap target-domain.foo -w yourwordlist.txt -r /tmp/domainbf_results.txt

```

* layer子域名挖掘机

* fierce

```
# kali built-in
fierce -dns target.com -threads 100
```



#### Online Tools

* https://findsubdomains.com/(online)

* https://dnsdumpster.com/(online)
* [微步在线](https://x.threatbook.cn/en)(online)
* <https://virustotal.com/>(online)



### 1.2 DNS

* dig

```
# kali built-in
dig baidu.com any
```

* nslookup

```
# kali-builtin
nslookup -type=ns domain_name
```

* dnsenum

```
# kali-builtin
dnsenum --enum domain_name
```

* DNS zone transfer

  http://www.lijiejie.com/dns-zone-transfer-1/

* https://viewdns.info/(online)



### 1.3 CDN

查看是否存在cdn加速

a. nslookup domain_name    #返回结果addresses有多个地址说明有cdn

b. 使用不同地区的ip来ping它，如果得到的ip是不一样的，那么就可以判断出它使用了CDN了，在线ping服务：https://ping.aizhan.com/、http://ping.chinaz.com

c. 在线监测：https://www.cdnplanet.com/tools/cdnfinder/

d. 脚本检测：https://github.com/Nitr4x/whichCDN

whichCDN http://www.example.com | example.com

绕过cdn获取真实ip

a. 由于国内很多CDN提供商可能只提供国内服务，而对国外不提供服务，因此通过国外的dns就可能解析到真实的ip，nslookup 主域名 国外冷门的dns

b. 查看历史dns记录，因为在使用cdn之前应该是真实的ip，https://toolbar.netcraft.com/site_report

c. 查询子域名，子域名可能没有用cdn

d. 目录敏感文件泄露，phpinfo之类的探针获取真实ip



## 2. IP

* whois

```
# kali-builtin
whois domain_name
```

* host 

```
# kali-builtin
host domain_name
```

* https://whois.icann.org (online)

### 2.1 c段

* shodan 搜索

  命令行下使用shodan：http://www.freebuf.com/sectool/121339.html

* fping：扫描c段存活主机

```
# kali-builtin
fping -a -g 101.200.31.0/24
```

### 2.2 旁站查询

http://s.tool.chinaz.com/same (online)

工具：https://github.com/Xyntax/BingC

## 3. Mail

### 3.1 邮箱挖掘器

* [theHarvester](https://github.com/laramies/theHarvester)

> theHarvester is a tool for gathering subdomain names, e-mail addresses, virtual hosts, open ports/ banners, and employee names from different public sources (search engines, pgp key servers).
>
> data source: baidu, bing, bingapi, dogpile, google, googleCSE,
>                         googleplus, google-profiles, linkedin, pgp, twitter, vhost,
>                         virustotal, threatcrowd, crtsh, netcraft, yahoo, all

```
# kali-built
proxychains theharvester -d target.com -b all
proxychains theharvester -d microsoft.com -l 500 -b google -h myresults.html
proxychains theharvester -d microsoft.com -b pgp
proxychains theharvester -d microsoft -l 200 -b linkedin
proxychains theharvester -d apple.com -b googleCSE -l 500 -s 300
```

* 利用theharvester和hydra爆破邮箱

  1. 通过theharvester找到邮箱

     ```theharvester -d example.com -b all```

  2. 用awk处理数据，爆破时只要邮箱@之前的用户名

     ```cat user1.txt | awk -F "@" '{print $1}' > user.txt```

  3. 用hydra爆破邮箱

     ```hydra -L user.txt -P password.txt pop3://mail.example.com```

* Infoga

> Email Information Gathering

```
git clone https://github.com/m4ll0k/Infoga.git infoga
cd infoga
pip3 install requests
python3 infoga.py --domain cia.gov --source bing --verbose 3
```



## 4. 企业信息

###4.1. 备案信息

http://www.beianbeian.com

###4.2. 提取网址，电子邮件，文件，网站帐户等的高速爬虫

https://github.com/s0md3v/Photon

```
python3 photon.py -u domain -l 4 -t 100
```



## 5. Web information gathering

### 5.1 Web

#### 5.1.1 SiteMap

* [Visual Site Mapper](http://www.visualsitemapper.com/)(online)

* [httpscreenshot](https://github.com/breenmachine/httpscreenshot/)



####5.1.2 Fingerprinting

* [Wappalyzer](https://www.wappalyzer.com/)

* [WAF Detector](https://github.com/EnableSecurity/wafw00f)

```
# kali-builtin
wafw00f domain_name
```

* [punk.sh](https://punk.sh/#/)(online)

>  global web application vulnerability search engine

* [CMSeek](https://github.com/Tuhinshubhra/CMSeeK)

> cms指纹信息

```
python3 cmseek.py -u url
```

* whatweb

```
# kali-builtin
详细信息：whatweb -v domain_name
查看插件：whatweb -l domain_name
```



#### 5.1.3 Web Archive

https://web.archive.org/(online)

<https://gist.github.com/mhmdiaa/2742c5e147d49a804b408bfed3d32d07>

https://gist.github.com/mhmdiaa/adf6bff70142e5091792841d4b372050

#### 5.1.4 http method

```
nmap --script http-methods <target>
```

#### 5.1.5 统计网站中出现的单词数

```
kali-builtin
cewl -w example.txt -c -m 5 http://www.example.com
```

#### 5.1.6 目录、文件遍历

* ([Dirsearch](https://github.com/maurosoria/dirsearch) / dirb / dirbuster)+ [wordlist](https://github.com/danielmiessler/SecLists)

* [OpenDoor](https://github.com/stanislav-web/OpenDoor)

```
python3 opendoor.py --host url
```



#### 5.1.7 Find hidden GET & POST parameters

* [Arjun](https://github.com/UltimateHackers/Arjun)



#### 5.1.8  Manual pentest

* Burpsuite



#### 5.1.9 JS script

[relative-url-extractor](https://github.com/jobertabma/relative-url-extractor)

> This tool contains a nifty regular expression to find and extract the relative URLs in such files. This can help surface new targets for security researchers to look at. It can also be used to periodically compare the results of the same file, to see which new endpoints have been deployed.

#### 5.1.10 Virtual Host Discovery

[virtual-host-discovery](https://github.com/jobertabma/virtual-host-discovery)

> It’s called **Virtual Host Discovery** and this script can help you find **Vhost** behind a target.

https://pentest-tools.com/information-gathering/find-virtual-hosts(online)



#### 5.1.11 svn信息泄露

https://github.com/callmefeifei/SvnHack

```
python SvnHack.py -u http://x.x.x.x/.svn/entries
```



### 5.2 服务器信息

#### 5.2.1 服务器操作系统

```
nmap -O <target>
```

**tips: ping target**

> Windows NT/2000 TTL:128
>
> Windows 95/98 TTL:32
>
> UNIX TTL:255
>
> Linux: TTL 64
>
> Win7: TTL 64

### 5.2.2 扫描服务器信息漏洞

```
# kali built-in
nikto -h domain_name
```



#### 5.2.3 中间件信息

* 通过错误页面判断

* 自动化扫描器：[Sn1per](https://github.com/1N3/Sn1per)
* `nmap -sV target -Pn`
* [Wappalyzer](https://www.wappalyzer.com/)



## 6. Search Engine 

#### 6.1 Google (online)

```
site:target.com -www
site:target.com intitle:”test” -support
site:target.com ext:php | ext:html
site:subdomain.target.com
site:target.com inurl:auth
site:target.com inurl:dev

# sensitive infomation
site:target.com filetype:doc intext:pass
site:target.com filetype:xls intext:pass
site:target.com filetype:conf
site:target.com filetype:inc

# 收集邮箱信息
site:Github.com smtp @sina.com.cn
site:Github.com smtp password
site:Github.com String password smtp

# 数据库信息泄露
site:Github.com sa password
site:Github.com root password
site:Github.com User ID='sa';Password

# svn信息泄露
site:Github.com svn
site:Github.com svn username
site:Github.com svn password
site:Github.com svn username password

# 数据库备份文件
site:Github.com inurl:sql

# 综合信息泄露
site:Github.com password
site:Github.com ftp ftppassword
site:Github.com 密码
site:Github.com 内部

# management console
site:target.com 管理
site:target.com admin
site:target.com login

# mail search
site:target.com intext:@target.com
intext:@target.com

# sensitive site path
site:target.com intitle:mongodb inurl:28017
site:target.com inurl:sql.php
site:target.com inurl:phpinfo.php

# configuration files
site:example.com ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf | ext:rdp | ext:cfg | ext:txt | ext:ora | ext:ini
# data file
site:example.com ext:sql | ext:dbf | ext:mdb
# log file
site:example.com ext:log
# backup file
site:example.com ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup
# login
site:example.com inurl:login
# sql error page
site:example.com intext:"sql syntax near" | intext:"syntax error has occurred" | intext:"incorrect syntax near" | intext:"unexpected end of SQL command" | intext:"Warning: mysql_connect()" | intext:"Warning: mysql_query()" | intext:"Warning: pg_connect()"
# public doc
site:example.com ext:doc | ext:docx | ext:odt | ext:pdf | ext:rtf | ext:sxw | ext:psw | ext:ppt | ext:pptx | ext:pps | ext:csv
# phpinfo探针文件
site:example.com ext:php intitle:phpinfo "published by the PHP Group"
# index of 目录清单
site:example.com "index of /"
```

https://www.exploit-db.com/google-hacking-database/(online)

https://pentest-tools.com/information-gathering/google-hacking(online)

https://github.com/1N3/Goohak/

> Automatically launch google hacking queries against a target domain to find vulnerabilities and enumerate a target.

https://github.com/ZephrFish/GoogD0rker/

> GoogD0rker is a tool for firing off google dorks against a target domain, it is purely for OSINT against a specific target domain. 



#### 6.2 [Shodan.io](shodan.io)(online)

> for servers, IoT and all devices which can be connected to Internet

`hostname: google.com`

#### 6.3 [Censys.io]([https://censys.io](https://censys.io/))(online)

compare the result to Shodan.io

#### 6.4 [Fofa](https://fofa.so/)(online)

#### 6.5 [ZoomEye](https://www.zoomeye.org/)(online)

#### 6.6 [crt.sh](https://crt.sh)(online)

#### 6.7 github(online)

#### 	6.7.1 git 信息泄露

* [gitrob](https://github.com/michenriksen/gitrob)

> Gitrob is a tool to help find potentially sensitive files pushed to public repositories on Github. Gitrob will clone repositories belonging to a user or organization down to a configurable depth and iterate through the commit history and flag files that match signatures for potentially sensitive files.

* [truffleHog](https://github.com/dxa4481/truffleHog)

> Searches through git repositories for secrets, digging deep into commit history and branches. This is effective at finding secrets accidentally committed.

* [git-all-secrets](https://github.com/anshumanbh/git-all-secrets)
* [GitHack](https://github.com/BugScanTeam/GitHack)

```
python githack.py http://domain.com/.git
```

* [GitHarvester](https://github.com/metac0rtex/GitHarvester)

#### 6.8 virustotal (online)



## 7. Port

### 7.1 扫描端口

端口扫描的目的是识别目标系统中哪些端口是开启状态，哪些服务可以使用

* nmap

```
nmap -iL list.txt -T4 -sV -Pn -oN result.txt
nmap -p 1-65535 -sV ip/domain_name/
```

* masscan

### 7.2 端口爆破

```
hydra -l user -P passlist.txt ftp://192.168.0.1
hydra -L logins.txt -P pws.txt -M targets.txt ssh
```

### 7.3 扫描常见漏洞

```
nmap --script=vuln ip/domain/
```

详见: https://blog.csdn.net/qq_29277155/article/details/50977143

## 8. Combined tools

8.1 [recon-ng](https://bitbucket.org/LaNMaSteR53/recon-ng)

> Recon-ng is a full-featured Web Reconnaissance framework written in Python.

8.2 [DiscoverTarget](https://github.com/coco413/DiscoverTarget)

> 集360、百度、谷歌、Shodan、Zoomeye、Censys、Fofa于一体一键运行获取目标URL、IP等信息

8.3 [Sn1per](https://github.com/1N3/Sn1per)

> Sn1per Community Edition is an automated scanner that can be used during a penetration test to enumerate and scan for vulnerabilities. Sn1per Professional is Xero Security's premium reporting addon for Professional Penetration Testers, Bug Bounty Researchers and Corporate Security teams to manage large environments and pentest scopes.

```
in kali
proxychains ./install.sh
# note that it will try to create tables in msf
sniper -t <TARGET> -o -re
sniper -t <CIDR> -m discover -w <WORSPACE_ALIAS>
```

8.4 Maltego kali图形化信息收集工具，功能非常强

8.5 [Aquatone](https://github.com/michenriksen/aquatone)

> After subdomain discovery, AQUATONE can then scan the hosts for common
> web ports and HTTP headers, HTML bodies and screenshots can be gathered
> and consolidated into a report for easy analysis of the attack surface.

```
echo "aquatone-discover -d \$1 && aquatone-scan -d \$1 --ports huge && aquatone-takeover -d \$1 && aquatone-gather -d \$1" >> aqua.sh && chmod +x aqua.sh
./aqua.sh domain.com
```



## 9. Acknowledgement and Reference

https://medium.com/bugbountywriteup/whats-tools-i-use-for-my-recon-during-bugbounty-ec25f7f12e6d(online)

https://medium.com/secjuice/guide-to-basic-recon-bug-bounties-recon-728c5242a115(online)

https://github.com/EdOverflow/bugbounty-cheatsheet(online)

[Can I take over XYZ](https://github.com/EdOverflow/can-i-take-over-xyz)(online)

https://github.com/djadmin/awesome-bug-bounty(online)

https://blog.csdn.net/qq_29277155/article/details/50977143(online)

## 10. Contributor

[musicalpike](https://github.com/musicalpike)

[black-mirror](https://github.com/black-mirror)

[EnterpriseForever](https://github.com/EnterpriseForever)

[hktalent](https://github.com/hktalent)

[hanerkui](https://github.com/hanerkui)