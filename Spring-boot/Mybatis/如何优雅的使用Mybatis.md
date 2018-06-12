# spring-boot中如何优雅的使用mybatis
[原文地址](http://www.cnblogs.com/ityouknow/p/6037431.html)

***

## mybatis-spring-boot-starter
官方说明：MyBatis Spring-Boot-Starter will help you use MyBatis with Spring Boot  
其实就是myBatis看spring boot这么火热也开发出一套解决方案来凑凑热闹,但这一凑确实解决了很多问题，使用起来确实顺畅了许多。 
mybatis-spring-boot-starter主要有两种解决方案，一种是使用注解解决一切问题，一种是简化后的老传统。  

当然任何模式都需要首先引入mybatis-spring-boot-starter的pom文件,现在最新版本是1.1.1（刚好快到双11了 :)）

``` 
    <dependency>
        <groupId>org.mybatis.spring.boot</groupId>
        <artifactId>mybatis-spring-boot-starter</artifactId>
        <version>1.1.1</version>
    </dependency>
```

好了下来分别介绍两种开发模式


