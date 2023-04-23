- [前言](#前言)
- [操作步骤](#操作步骤)
  - [第一步：查看和操作时间戳](#第一步查看和操作时间戳)
  - [步骤二：组织Shell脚本](#步骤二组织shell脚本)
  - [步骤三：开始脚本](#步骤三开始脚本)
  - [步骤四：将时间戳写入文件](#步骤四将时间戳写入文件)
  - [步骤五：恢复文件的时间戳](#步骤五恢复文件的时间戳)
  - [步骤六：使用脚本](#步骤六使用脚本)
- [总结](#总结)


# 前言

寻找攻击证据就从攻击者留下的这些痕迹开始，如文件的修改日期。每一个Linux文件系统中的每个文件都保存着修改日期。系统管理员发现文件的最近修改时间，便提示他们系统受到攻击，采取行动锁定系统。然而幸运的是，修改时间不是绝对可靠的记录，修改时间本身可以被欺骗或修改，通过编写 Shell脚本，攻击者可将备份和恢复修改时间的过程自动化。

# 操作步骤

## 第一步：查看和操作时间戳
多数Linux系统中包含一些允许我们快速查看和修改时间戳的工具，其中最具影响的当数“Touch”，它允许我们创建新文件、更新文件 /文件组最后一次被“touched”的时间。

```bash
touch file
```

若该文件不存在,运行上面的命令将创建一个名为“file”的新文件；若它已经存在，该命令将会更新修改日期为当前系统时间。我们也可以使用一个通配符，如下面的字符串。

```bash
touch *
```

这个命令将更新它运行的文件夹中的每个文件的时间戳。在创建和修改文件之后，有几种方法可以查看它的详细信息，第一个使用的为“stat”命令。

```bash
stat file
```
![图 1](/assets/img/2023-04/d3f62470ff7cd5b2cb3d85a3a35f48eeb97617add4cd9d90cd70a46f166cc9e9.png)  

运行stat会返回一些关于文件的信息，包含访问、修改或更新时间戳。针对一批文件可使用ls参数查看各文件的时间戳，使用“ -l”或者“long”，该命令会列出文件详细信息，包含输出时间戳。

```bash
ls –l
```

![图 2](/assets/img/2023-04/b1db0adccfabbe5aca4a53b201565a91bcae762c790ca394dfe44e7ee5046024.png)  

现在就可以设置当前时间戳并查看已经设置的时间戳，也可使用touch来定义一个自定义时间戳，可使用“d”标志，用yyyy-mm-dd格式定义日期，紧随其后设置时间的小时、分钟及秒，如下：

```bash
touch -d"2001-01-01 20:00:00" file
```

通过ls命令来确认修改信息：

```bash
ls -l file
```

![图 3](/assets/img/2023-04/1a881f174d06090289cfbd17cc0fb759543f8e13da34ea9908abc15bcdf2b78d.png)  

这种方法适用于修改个别时间戳，对于隐藏服务器上的操作痕迹，这个方法不太奏效，可以使用shell脚本将该过程自动化。

## 步骤二：组织Shell脚本

在开始编写脚本之前需要考虑清楚需要执行哪些过程。为了在服务器上隐藏痕迹，攻击者需要将文件夹的原始时间戳写入一个文件，同时能够在我们进行任何修改设置之后还能回到原始文件。

这两个不同的功能会根据用户的输入或者参数的不同而触发，脚本会根据这些参数执行相应的功能，同时我们需要有一种方法来处理错误。根据用户的输入将会进行三种可能的操作：

- 没有参数——返回错误消息；

- 保存时间戳标记——将时间戳保存到文件中；

- 恢复时间戳标记——根据保存列表恢复文件的时间戳。

我们可以使用嵌套语句if/or语句来创建脚本，也可以根据条件将每个函数分配给自己的“if”语句，可选择在文本编辑器或者nano中开始编写脚本。

## 步骤三：开始脚本

从命令行启动nano并创建一个名为“timestamps.sh”的脚本，命令如下：

```bash
nano timestamps.sh
```

然后进行下列命令：

```bash
#!/bin/bash
if [ $# -eq 0 ];then
echo “Use asave (-s) or restore (-r) parameter.”
exit 1
fi
```

![图 4](/assets/img/2023-04/154a4442b605c05d941b2a3a138952dd098bba9131b2052ac7b742dafd4f371c.png)  

在nano中按下Ctrl + O保存这个文件，通过chmod命令将它标记为可运行的脚本。

```bash
chmod +x timestamps.sh
```

然后运行脚本，测试无参数时返回错误信息的功能。如果脚本返回我们的echo语句，我们就可以继续下一个条件了。

```bash
./timestamps.sh
```

![图 5](/assets/img/2023-04/10999af8a5093e7b771f51cece5bfc12e4c095f8dd9bfb1998439c577021864f.png)  

## 步骤四：将时间戳写入文件

定义if语句的条件，“-s”表示执行保存功能：

```bash
if [ $1 ="-s" ] ; then
fi
```

当然，需要检查计划保存的时间戳文件是否存在，如果存在，我们可以删除它（名为timestamps的文件），避免重复或错误的输入，使用下面的命令：

```bash
rm -f timestamps;
```

然后使用“ls”命令列出所有文件和它的修改时间，可将其输出到另一个程序，如sed，以帮助我们稍后清理这个输入。

```bash
ls –l
```

通常会出现下面的显示结果：

```bash
-rw-r--r-- 1 user user 0 Jan 1 2017 file
```

为了保存时间戳，我们只需要年、月、日及文件名，下面命令可以清除“Jan”之前的信息：

```bash
ls -l file | sed 's/^.*Jan/Jan/p'
```

这样显示的就是我们程序需要的信息，只是需要修改月份格式为数字格式：

```bash
ls -l file | sed 's/^.*Jan/01/p'
```

将所有月份都替换为数字：

```bash
ls -l | sed -n 's/^.*Jan/01/p;s/^.*Feb/02/p;s/^.*Mar/03/p;s/^.*Apr/04/p;s/^.*May/05/p;s/^.*Jun/06/p;s/^.*Jul/07/p;s/^.*Aug/08/p;s/^.*Sep/09/p;s/^.*Oct/10/p;s/^.*Nov/11/p;s/^.*Dec/12/p;'
```

在一个文件夹中运行我们会看到如下图所示的结果：

![图 7](/assets/img/2023-04/03da4eed2da58742b8e068acb10be50b40f389595dd4dc44fab36edbe3d08033.png)  

然后将输出结果通过“>>”发送到名为“timestamps”的文件中：

```bash
do echo $x | ls -l | sed -n 's/^.*Jan/01/p;s/^.*Feb/02/p;s/^.*Mar/03/p;s/^.*Apr/04/p;s/^.*May/05/p;s/^.*Jun/06/p;s/^.*Jul/07/p;s/^.*Aug/08/p;s/^.*Sep/09/p;s/^.*Oct/10/p;s/^.*Nov/11/p;s/^.*Dec/12/p;' >> timestamps
```

此脚本的前两个操作就完成了：

![图 9](/assets/img/2023-04/d1e0c677c9673836bbe5fa0bbc01eafc80be929f78a15c1b4190059229cb77e0.png)  

```bash
#!/bin/bash
if [ $# -eq 0 ];then
    echo “Use asave (-s) or restore (-r) parameter.”
    exit 1
fi
if [ $1 ="-s" ] ; then
    rm -f timestamps;
    ls -l | sed -n 's/^.*Jan/01/p;s/^.*Feb/02/p;s/^.*Mar/03/p;s/^.*Apr/04/p;s/^.*May/05/p;s/^.*Jun/06/p;s/^.*Jul/07/p;s/^.*Aug/08/p;s/^.*Sep/09/p;s/^.*Oct/10/p;s/^.*Nov/11/p;s/^.*Dec/12/p;' >> timestamps
fi
```

下面可用“-s”标示测试脚本，用cat检查保存的信息

```bash
./timestamps.sh –s
cat timestamps
```

![图 8](/assets/img/2023-04/5ddf7bce00957babc1f364ce42b87563250a99f5ee4ba176cc89fa410b60cb83.png)  

## 步骤五：恢复文件的时间戳

在保存好原始时间戳后，需要恢复时间戳让别人觉察不到文件被修改过，可使用下面命令：

```bash
if $1 = "-r" ; then
fi
```

然后使用下面命令，转发文本文件的内容，并一行一行运行：

```bash
cat timestamps |while read line
do
done
```

然后再分配一些变量让文件数据的使用更简单

```bash
MONTH=$(echo $line | cut -f1 -d\ );
DAY=$(echo $line| cut -f2 -d\ );
FILENAME=$(echo $line | cut -f4 -d\ );
YEAR=$(echo $line | cut -f3 -d\ )
```

虽然这四个变量在保存的时间戳文件中是一致的，但是如果时间戳是在过去一年中发生的，它只会显示时间而不是年份。如果需要确定当前年份，我们可以分配为写脚本的年份，也可以从系统中返回年份，使用cal命令可以查看日历。

![图 10](/assets/img/2023-04/9bfefff9a5a5c7886fe60a48b4090dfedfa17ac3880dc739152c945a79ff3a7c.png)  

然后检索第一行，只让显示想要的年份信息：

```bash
CURRENTYEAR=$(cal | head -1 | cut -f6- -d\ | sed 's/ //g')
```

![图 11](/assets/img/2023-04/684b1a949717af4d5497a3e5d01264e86c83d3d1201f6c525babdadbbf162c09.png)  

定义了所有变量之后可以使用“if else”语句，根据格式化的日期更新文件的时间戳，使用touch语法：

```bash
touch -d "2001-01-01 20:00:00" file
```

由于每个时间都包含冒号，因此可使用下面的“ifelse”语句完成操作，整体操作如下图所示：

```bash
if [ $YEAR == *:* ]; then
touch -d $CURRENTYEAR-$MONTH-$DAY\ $YEAR:00 $FILENAME;
else
touch -d ""$YEAR-$MONTH-$DAY"" $FILENAME;
fi
```

![图 12](/assets/img/2023-04/292a0555a01e48ee654cf2cde18a2ed4057fc421e1c7462a5199afa66af644c4.png)  

```bash
#!/bin/bash
if [ $# -eq 0 ];then
    echo “Use asave (-s) or restore (-r) parameter.”
    exit 1
fi
if [ $1 ="-s" ] ; then
    rm -f timestamps;
    ls -l | sed -n 's/^.*Jan/01/p;s/^.*Feb/02/p;s/^.*Mar/03/p;s/^.*Apr/04/p;s/^.*May/05/p;s/^.*Jun/06/p;s/^.*Jul/07/p;s/^.*Aug/08/p;s/^.*Sep/09/p;s/^.*Oct/10/p;s/^.*Nov/11/p;s/^.*Dec/12/p;' >> timestamps
fi
if [ $1 ="-r" ] ; then
    cat timestamps |while read line
    do
        MONTH=$(echo $line | cut -f1 -d\ );
        DAY=$(echo $line| cut -f2 -d\ );
        FILENAME=$(echo $line | cut -f4 -d\ );
        YEAR=$(echo $line | cut -f3 -d\ );
        CURRENTYEAR=$(cal | head -1 | cut -f6- -d\ | sed 's/ //g');
        if [ $YEAR == *:* ]; then
            touch -d $CURRENTYEAR-$MONTH-$DAY\ $YEAR:00 $FILENAME;
        else
            touch -d ""$YEAR-$MONTH-$DAY"" $FILENAME;
        fi
    done
fi
```

## 步骤六：使用脚本

使用的命令主要有以下几个：

- ./timestamps.sh –s   保存文件时间戳

- touch -d “2050-10-12 10:00:00″ *   修改目录下的所有文件时间戳

- ls –a   确认修改的文件

- ./timestamps.sh –r   恢复文件原始时间戳

最后可以再次运行“ls -a”来查看文件的时间戳是否和之前备份的时间戳一致，整个的脚本就执行完成了，如下图所示：

![图 6](/assets/img/2023-04/1ff819cd6207cb5f2b57b8eb9e8a57f0213fcba275db941ecf8f3ada6f2d3c1a.png)  

# 总结