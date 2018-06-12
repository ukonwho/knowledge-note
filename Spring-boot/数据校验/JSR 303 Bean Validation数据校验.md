# JSR-303简介
JSR-303 是 JAVA EE 6 中的一项子规范，叫做 Bean Validation，官方参考实现是Hibernate Validator。
此实现与 Hibernate ORM 没有任何关系。 JSR 303 用于对 Java Bean 中的字段的值进行验证。 
Spring MVC 3.x 之中也大力支持 JSR-303，可以在控制器中对表单提交的数据方便地验证。 
注:可以使用注解的方式进行验证

# 准备校验时使用的JAR
validation-api-1.0.0.GA.jar：JDK的接口； 
hibernate-validator-4.2.0.Final.jar是对上述接口的实现；