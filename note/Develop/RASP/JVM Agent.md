# JVM
## 原理
- RASP 将会尝试启动 JVM 的 attach 功能，并将探针 jar 植入到 JVM 中。
- 植入的探针将会利用 Java 提供的 instrument 能力（文档：https://docs.oracle.com/javase/8/docs/api/java/lang/instrument/Instrumentation.html），对部分函数的字节码进行修改，在函数入口插入拦截函数参数的字节码。
- 此时如果目标函数被执行，拦截的函数参数将会拷贝到跨线程的队列中，并由另一线程完成数据上报。

## 介绍一下 JVM 的 attach 功能
JVM 的 attach 功能是指在运行中的 Java 虚拟机上动态地加载和卸载 Java 代理程序。通过使用 attach 功能，可以在不重启 JVM 的情况下向正在运行的 Java 应用程序注入代理程序，以实现一些诊断、监控和调试等功能。

attach 功能的实现需要两个组件：JVM TI 接口和 JVM Attach API。JVM TI 接口是 Java 虚拟机提供的一组 C/C++ 接口，用于在运行时监控和管理 Java 应用程序。JVM Attach API 是 Java SE 提供的一组 Java 接口，用于在运行中的 Java 虚拟机上加载和卸载 Java 代理程序。

通过使用 attach 功能，可以实现以下功能：

- 监控 Java 应用程序的运行状态，例如 CPU 占用率、内存使用情况等。

- 动态地修改 Java 应用程序的行为，例如修改 JVM 参数、修改类加载器策略等。

- 在 Java 应用程序运行时进行调试，例如动态地修改变量的值、设置断点等。

总之，attach 功能为 Java 应用程序的调试、监控和管理提供了强大的支持。

## attach 功能 支持哪些jvm版本

JVM 的 attach 功能在 Java SE 5 及以上版本中提供支持。具体来说，可以在以下版本中使用 attach 功能：

- Java SE 5.0 Update 5 及以上版本
- Java SE 6 及以上版本
- Java SE 7 及以上版本
- Java SE 8 及以上版本
需要注意的是，不同版本的 JVM 实现对 attach 功能的支持程度可能会有所不同。例如，一些 JVM 实现可能不支持在运行中的 JVM 上动态加载代理程序。因此，在使用 attach 功能时，需要根据具体的 JVM 实现来选择合适的方式和工具。

## JVM Agent简介
JVM Agent是一个按一定规则编写的特殊程序库，可以在启动阶段通过命令行参数传递给JVM，作为一个伴生库与目标JVM运行在同一个进程中。在Agent中可以通过固定的接口获取JVM进程内的相关信息。Agent既可以是用C/C++/Rust编写的JVMTI Agent，也可以是用Java编写的Java Agent。
执行Java命令，我们可以看到Agent相关的命令行参数：

```bash
Plain Text
    -agentlib:<库名>[=<选项>]
                  加载本机代理库 <库名>, 例如 -agentlib:jdwp
                  另请参阅 -agentlib:jdwp=help
    -agentpath:<路径名>[=<选项>]
                  按完整路径名加载本机代理库
    -javaagent:<jar 路径>[=<选项>]
                  加载 Java 编程语言代理, 请参阅 java.lang.instrument
```
### JVMTI Agent
JVMTI（JVM Tool Interface）是JVM提供的一套标准的C/C++编程接口，是实现Debugger、Profiler、Monitor、Thread Analyser等工具的统一基础，在主流Java虚拟机中都有实现。
当我们要基于JVMTI实现一个Agent时，需要实现如下入口函数：

```java
// $JAVA_HOME/include/jvmti.h
​
JNIEXPORT jint JNICALL Agent_OnLoad(JavaVM *vm, char *options, void *reserved);
```

复制代码使用C/C++实现该函数，并将代码编译为动态连接库（Linux上是.so），通过-agentpath参数将库的完整路径传递给Java进程，JVM就会在启动阶段的合适时机执行该函数。在函数内部，我们可以通过JavaVM指针参数拿到JNI和JVMTI的函数指针表，这样我们就拥有了与JVM进行各种复杂交互的能力。

更多JVMTI相关的细节可以参考[官方文档](https://docs.oracle.com/en/java/javase/12/docs/specs/jvmti.html)。

### Java Agent
在很多场景下，我们没有必要必须使用C/C++来开发JVMTI Agent，因为成本高且不易维护。JVM自身基于JVMTI封装了一套Java的Instrument API接口，允许使用Java语言开发Java Agent（只是一个jar包），大大降低了Agent的开发成本。社区开源的产品如Greys、Arthas、JVM-Sandbox、JVM-Profiler等都是纯Java编写的，也是以Java Agent形式来运行。
在Java Agent中，我们需要在jar包的MANIFEST.MF中将Premain-Class指定为一个入口类，并在该入口类中实现如下方法：

```java
public static void premain(String args, Instrumentation ins) {
    // implement
}
```
复制代码这样打包出来的jar就是一个Java Agent，可以通过-javaagent参数将jar传递给Java进程伴随启动，JVM同样会在启动阶段的合适时机执行该方法。
在该方法内部，参数Instrumentation接口提供了Retransform Classes的能力，我们利用该接口就可以对宿主进程的Class进行修改，实现方法耗时统计、故障注入、Trace等功能。Instrumentation接口提供的能力较为单一，仅与Class字节码操作相关，但由于我们现在已经处于宿主进程环境内，就可以利用JMX直接获取宿主进程的内存、线程、锁等信息。无论是Instrument API还是JMX，它们内部仍是统一基于JVMTI来实现。

更多Instrument API相关的细节可以参考[官方文档](https://docs.oracle.com/en/java/javase/12/docs/api/java.instrument/java/lang/instrument/package-summary.html)。