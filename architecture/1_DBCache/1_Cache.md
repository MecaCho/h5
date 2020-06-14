

# 使用缓存

## 选型----redis还是memcache

### 什么时候倾向于选择redis？

1。复杂数据结构
value是哈希，列表，集合，有序集合这类复杂的数据结构时，会选择redis，因为mc无法满足这些需求。
最典型的场景，用户订单列表，用户消息，帖子评论列表等。

2。持久化

mc无法满足持久化的需求，只得选择redis。
只读场景，或者允许一些不一致的业务场景，可以尝试开启redis的固化功能。

3。天然高可用

redis天然支持集群功能，可以实现主动复制，读写分离。

但是，这里要提醒的是，大部分业务场景，缓存真的需要高可用么？
（1）缓存场景，很多时候，是允许cache miss
（2）缓存挂了，很多时候可以通过DB读取数据
所以，需要认真剖析业务场景，高可用，是否真的是对缓存的主要需求？
画外音：即时通讯业务中，用户的在线状态，就有高可用需求。

4。存储的内容比较大

memcache的value存储，最大为1M，如果存储的value很大，只能使用redis。

### 什么时候倾向于memcache？

纯KV，数据量非常大，并发量非常大的业务，使用memcache或许更适合。

### 底层实现机制

#### 内存分配

memcache使用预分配内存池的方式管理内存，能够省去内存分配时间。
redis则是临时申请空间，可能导致碎片。

#### 虚拟内存使用

memcache把所有的数据存储在物理内存里。
redis有自己的VM机制，理论上能够存储比物理内存更多的数据，当数据超量时，会引发swap，把冷数据刷到磁盘上。

#### 网络模型

memcache使用非阻塞IO复用模型，
redis也是使用非阻塞IO复用模型，redis还提供一些非KV存储之外的排序，聚合功能，在执行这些功能时，复杂的CPU计算，会阻塞整个IO调度。。

#### 线程模型

memcache使用多线程，主线程监听，worker子线程接受请求，执行读写，这个过程中，可能存在锁冲突。
redis使用单线程，虽无锁冲突，但难以利用多核的特性提升整体吞吐量。


## 何时更新缓存

由于你只能在缓存中存储有限的数据，所以你需要选择一个适用于你用例的缓存更新策略。

### 1.缓存模式（旁路缓存）

应用从存储器读写。缓存不和存储器直接交互，应用执行以下操作：

1.在缓存中查找记录，如果所需数据不在缓存中    
2.从数据库中加载所需内容    
3.将查找到的结果存储到缓存中    
4.返回所需内容    

```python
import cache
import json

def get_user(self, user_id):
    user = cache.get("user.{0}", user_id)
    if user is None:
        user = db.query("SELECT * FROM users WHERE user_id = {0}", user_id)
        if user is not None:
            key = "user.{0}".format(user_id)
            cache.set(key, json.dumps(user))
    return user
```

缓存的缺点：
请求的数据如果不在缓存中就需要经过三个步骤来获取数据，这会导致明显的延迟。    
如果数据库中的数据更新了会导致缓存中的数据过时。这个问题需要通过设置TTL 强制更新缓存或者直写模式来缓解这种情况。    
当一个节点出现故障的时候，它将会被一个新的节点替代，这增加了延迟的时间。    

### 2.直写模式（穿透型缓存）

应用使用缓存作为主要的数据存储，将数据读写到缓存中，而缓存负责从数据库中读写数据。

1。应用向缓存中添加/更新数据    
2。缓存同步地写入数据存储    
3。返回所需内容        
应用代码：    
```
set_user(12345, {"foo":"bar"})
```

缓存代码：    
```
def set_user(user_id, values):
    user = db.query("UPDATE Users WHERE id = {0}", user_id, values)
    cache.set(user_id, user)
```

由于存写操作所以直写模式整体是一种很慢的操作，但是读取刚写入的数据很快。
相比读取数据，用户通常比较能接受更新数据时速度较慢。缓存中的数据不会过时。

直写模式的缺点：        
由于故障或者缩放而创建的新的节点，新的节点不会缓存，直到数据库更新为止。缓存应用直写模式可以缓解这个问题。
写入的大多数数据可能永远都不会被读取，用 TTL 可以最小化这种情况的出现。    

### 3.回写模式

在回写模式中，应用执行以下操作：    
- 在缓存中增加或者更新条目   
- 异步写入数据，提高写入性能。    

回写模式的缺点：    
缓存可能在其内容成功存储之前丢失数据。   

## 缓存的缺点：

需要保持缓存和真实数据源之间的一致性，比如数据库根据缓存无效。    
需要改变应用程序比如增加 Redis 或者 memcached。    
无效缓存是个难题，什么时候更新缓存是与之相关的复杂问题。    

## 使用误区

### 1。把缓存作为服务与服务之间传递数据的媒介

该方案存在的问题是：
数据管道，数据通知场景，MQ更加适合
多个服务关联同一个缓存实例，会导致服务耦合

### 2。使用缓存未考虑雪崩

什么时候会产生雪崩？
答：如果缓存挂掉，所有的请求会压到数据库，如果未提前做容量预估，可能会把数据库压垮（在缓存恢复之前，数据库可能一直都起不来），导致系统整体不可服务。

如何应对潜在的雪崩？
答：提前做容量预估，如果缓存挂掉，数据库仍能扛住，才能执行上述方案。

解决方案：
#### 高可用缓存
1。使用高可用缓存集群，一个缓存实例挂掉后，能够自动做故障转移。

#### 缓存水平切分

使用缓存水平切分，一个缓存实例挂掉后，不至于所有的流量都压到数据库上。

### 3。多服务共用缓存实例

可能导致key冲突，彼此冲掉对方的数据
不同服务对应的数据量，吞吐量不一样，共用一个实例容易导致一个服务把另一个服务的热数据挤出去
共用一个实例，会导致服务之间的耦合，与微服务架构的“数据库，缓存私有”的设计原则是相悖的

# 读写分离

## 如何来实施 MySQL 的读写分离方案。

你需要做两件事儿：
- 部署一主多从多个 MySQL 实例，并让它们之间保持数据实时同步。
- 分离应用程序对数据库的读写请求，分别发送给从库和主库。

### MYSQL配置

MySQL 自带主从同步的功能，经过简单的配置就可以实现一个主库和几个从库之间的数据同步，部署和配置的方法，
你看MySQL 的官方文档照着做就可以。

### 程序侧

分离应用程序的读写请求方法有下面这三种：
    1。纯手工方式：修改应用程序的 DAO 层代码，定义读写两个数据源，指定每一个数据库请求的数据源。
    2。组件方式：也可以使用像 Sharding-JDBC 这种集成在应用中的第三方组件来实现，
        这些组件集成在你的应用程序内，代理应用程序的所有数据库请求，自动把请求路由到对应数据库实例上。
    3。代理方式：在应用程序和数据库实例之间部署一组数据库代理实例，比如说 Atlas 或者 MaxScale。
        对应用程序来说，数据库代理把自己伪装成一个单节点的 MySQL 实例，应用程序的所有数据库请求被发送给代理，
        代理分离读写请求，然后转发给对应的数据库实例。
 这三种方式，我最推荐的是第二种，使用读写分离组件。这种方式代码侵入非常少，并且兼顾了性能和稳定性。如果你的应用程序是一个逻辑非常简单的微服务，简单到只有几个 SQL，或者是，你的应用程序使用的编程语言没有合适的读写分离组件，那你也可以考虑使用第一种纯手工的方式来实现读写分离。
 一般情况下，不推荐使用第三种代理的方式，原因是，使用代理加长了你的系统运行时数据库请求的调用链路，有一定的性能损失，并且代理服务本身也可能出现故障和性能瓶颈等问题。但是，代理方式有一个好处是，它对应用程序是完全透明的。所以，只有在不方便修改应用程序代码这一种情况下，你才需要采用代理方式。
 
 
 随着系统的用户增长，当单个 MySQL 实例快要扛不住大量并发的时候，读写分离是首选的数据库扩容方案。读写分离的方案不需要对系统做太大的改动，就可以让系统支撑的并发提升几倍到十几倍。推荐你使用集成在应用内的读写分离组件方式来分离数据库读写请求，如果很难修改应用程序，也可以使用代理的方式来分离数据库读写请求。如果你的方案中部署了多个从库，推荐你用“HAProxy+Keepalived”来做这些从库的负载均衡和高可用，这个方案的好处是简单稳定而且足够灵活，不需要增加额外的服务器部署，便于维护并且不增加故障点。主从同步延迟会导致主库和从库之间出现数据不一致的情况，我们的应用程序应该能兼容主从延迟，避免因为主从延迟而导致的数据错误。规避这个问题最关键的一点是，我们在设计系统的业务流程时，尽量不要在更新数据之后立即去查询更新后的数据。

## 数据库主从不一致，怎么解决？

常见的数据库集群架构如何？
答：一主多从，主从同步，读写分离。

为什么会出现不一致？
答：主从同步有时延，这个时延期间读从库，可能读到不一致的数据。

如何避免这种主从延时导致的不一致？
### 1。忽略----如果业务能接受，就忽略。别把系统架构搞得太复杂。
### 2。强制读主

    （1）使用一个高可用主库提供数据库服务
    （2）读和写都落到主库上
    （3）采用缓存来提升系统读性能
    
### 3。选择性读主

可以利用一个缓存记录必须读主的数据。
在cache里记录哪些记录发生过写请求，来路由读主还是读从


# questions

一、不同业务场景下的缓存选型    
什么是穿透型缓存，什么是旁路型缓存？
缓存模式----旁路型缓存        
直写模式---穿透型缓存    
回写模式----异步转发到消息    

什么时候用进程内缓存，什么时候用缓存服务？    

对于不变对象的较小规模的、可预见次数的访问，进程内缓存是一个理想解决方案，性能上它优于分布式缓存。
然而，对于要缓存的对象数量是未知的并且较大的情况下，同时要求读一致性，分布式缓存是一个更好的解决方案，
尽管它可能具备与进程内缓存相同的性能。
自不用说，应用程序可以同时应用两种类型的缓存，取决于最适用的应用场景。


啥时候用memcache，啥时候用redis？又或者？    

缓存在微服务体系架构中的位置，以及设计原则？    

 
二、关于缓存的设计折衷   
 
什么时候适合使用缓存？    
引入缓存后，对读写业务流程有什么影响？     
到底应该修改缓存，还是淘汰缓存？    
应该先操作数据库，还是操作缓存？    
 
三、关于缓存的架构设计
缓存失效会引发什么雪崩？
缓存是否需要保证高可用？如何保证高可用？
缓存如何保证与数据库中的数据一致性？
缓存如何保证无限量的扩展性？