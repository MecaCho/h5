
# QPS

1、基于 Benchmark Test 给出压力模型指标，比如说，1核cpu，1g内存（jvm内存配置最好详情说明一下, 
    开了多少线程等性能指标的情况下，qps 多少，cpu使用率，内存使用率，gc时间等作出说明，
    一般的cpu，内存在模型当中最好大于70% ，压测最好给出资源模型比如说(0.5c cpu、700M内存）
    压测能达到cpu和内存的使用率都大于70% gc频率和gc时长等。
    这样压测出的模型 不会浪费资源，主要的目的是确定资源使用规则和资源组成占比（区分io密集型和cpu密集型）。  
    假设模型为（0.5核cpu、800m内存（默认配置，线程数100的情况下，cpu使用率和内存使用率都超过70%时的 qps 稳定在300左右)
2、基于以上压测模型，预计部署规模，比如说预估峰值qps1000 根据以上假设的压测模型部署4个实例即可。
3、以上部署模型如果是传统的部署很难去限制cpu为0.5核，可以考虑容器化部署。
    通过docker来限制一个docker启动时资源的限制。
    也可以通过类型k8s等服务编排工具来实施。
4、有条件的可以根据cpu、内存等监控的 metric指标来进行动态的扩容缩容。
    白天qps高的时候可以跑在线服务，晚上qps小的时候缩容，把节省的资源跑离线任务达到资源的最大化利用。
5、当然话说回来，每个开发人员可能对代码级别的性能优化水平不同，在具体使用什么组件，具体哪种优化方案等都必须以性能测试为前提。
6、我个人而言，资源的浪费才是应该优化的重点，一个服务，一段代码性能再高，
    部署的时候不根据服务或压力模型去部署都是耍流氓，都是做无用功。
    一个qps再高的服务，本来只需要1核cpu, 1g内存即可，一上线就直接申请4核cpu，8g甚至16g内存的大有人在。
    cpu、内存使用率一辈子都没有超过5%这不是浪费是什么？
    
# 高并发问题
 
所谓高并发，就是同一时间有很多流量(通常指用户)访问程序的接口、页面及其他资源，解决高并发就是当流量峰值到来时保证程序的稳定性。

我们一般用QPS(每秒查询数，又叫每秒请求数)来衡量程序的综合性能，数值越高越好，一般需要压测(ab工具)得到数据。

假设我们的一个进程(也可以是线程或者协程)处理一次请求花费了50毫秒(业内达标范围一般是20毫秒至60毫秒)，那么1秒钟就可以处理20个请求，一台服务器是可以开很多这样的进程并行去处理请求的，比如开了128个，那么这台机器理论上的QPS=2560。

千万不要小瞧这个数字，当你的QPS真有这么高的时候意味着你的DAU(用户日活)有2560*200=51.2万，业内一般是放大200倍计算，有这样的日活说明做得很不错了。

一台服务器能够达到的最大QPS受很多因素的影响，比如机器参数配置、机房地理位置、CPU性能、内存大小、磁盘性能、带宽大小、程序语言、数据库性能、程序架构等，我们一一细说。

## 1.机器参数配置

这个很好理解，比如服务器最大可以开启128个进程，你设置了最大只开启100个，这属于服务器调优。

2.机房地理位置
如果你做海外用户，服务器机房应该选择国外的，反之应该选择国内的，因为机房距离用户越近，在传输上的时间损耗就越低。

3.CPU性能
CPU性能越好，处理速度就越快，核心数越多，能够并行开启的进程就越多。

4.内存大小
内存越大，程序就能把更多的数据直接放到内存，从内存读取数据比从磁盘读取数据的速度快很多。

5.磁盘性能
这个不用多说吧，一般固态硬盘的性能比机械硬盘的性能好很多，性能越好读写数据的速度就越快。

6.带宽大小
服务器的带宽一般指流出带宽，单位为Mb/S，比如带宽为8Mb/S即1MB/S，如果提供文件下载服务，可能一个用户的下载行为就把服务器带宽用完了。

一般把图片、视频、css文件、JavaScript脚本等资源放到第三方的CDN去，按流量计费，这样就不占用服务器带宽了。

如果用户规模小，基本上一台服务器就好了，这个时候一般会选按固定带宽大小计费。

如果用户规模很大了，基本上会用到负载均衡器来分流，即把流量按照一定的规则分配到不同的服务器上，负载均衡器一般会按流量来计费。

如果平均一次请求返回的数据大小为50KB，为了达到1000QPS这个指标，需要的带宽峰值=1000*50*8/1024=390.625Mb/S。

我们在设计接口的时候应该尽量减少返回的数据大小，比如user_id就可以简化为uid，像图片、视频、css等文件压缩的目的就是减少数据的大小。

7.程序语言
编译型语言的性能一般好于解释型语言的性能，比如go语言性能就好于php语言性能，当语言短期不会替换时，可以通过堆机器解决高并发问题。

8.数据库性能
一台服务器上部署的数据库总是有一个瓶颈的，比如每秒查询数、每秒写入数。

我们可以通过增加很多从库解决查询(select语句)的瓶颈，称之为多从库模型，需要注意的是主从同步数据可能有延迟，当修改数据后马上需要查询时需要设置强制从主库读取。

我们可以将业务拆分，让某些表存储在一个数据库实例上，另一些表存储在其他数据库实例上，虽然一个数据库实例有自己的瓶颈，但是很多的数据库实例堆积起来性能就会大大改善，多个数据库实例的方案称之为多主库模型，主要是为了解决写入瓶颈(insert语句、update语句、delete语句)。

如果你有多个主库又有多个从库，你就实现了多主多从模型。

如果一个表存储的数据量很大，这个时候就要考虑分表了(一般用中间件实现)，比如按时间分表或者按用户分表，当把一个表的所有分表都放在一个数据库实例上都满足不了要求的时候，你应该把某些分表存储在新的数据库实例上，这个时候一个表的数据分布到了不同的数据库实例上，这就是所谓的分布式数据库方案了，你需要处理的事情就很复杂了，比如处理分布式事务。

数据库的并发连接数也是有限制的，我们可以用连接池技术来应对，就是保持一定数量的和数据库的连接不断开的长连接，需要连接数据库的时候就从池子里选择一个连接，用完放回去就好了，这个一般也是用中间件来实现。

好的索引也能提高数据库的性能，有时候比堆多个从库的方案还要好。

如果能够减少数据库的读写，也算间接提高了数据库的性能，比如我们用redis来做缓存，用消息队列异步落库等。

有时候某些数据用数据库来计算需要很长时间，可以取到元数据(最小粒度的数据)用程序来计算，这称之为用内存换时间。

9.程序架构
比如实现同样的功能，初级程序员写的程序需要循环100次，而高级程序员写的程序只需要循环10次，效果肯定不一样。

总结
一般大型项目基本是前后端分离的，从性能方面说就是为了将页面渲染的处理在客户端运行，降低服务器的压力。

从带宽层面考虑，css、图片、视频、JavaScript等文件资源能用CDN的就用CDN，能压缩的就尽量压缩，接口能减小返回数据的大小就尽量减小。

为了解决编程语言的不足或者单台服务器的瓶颈，可以先堆机器应对。

索引、多主多从、分布式数据库、缓存、连接池、消息队列等是从数据库方便考虑如何优化性能。

有时候程序的低耦合性比程序的高性能更重要，不要一味地追求高性能。


# wrk

测试环境找好测试工具后，我们还不能直接开始压力测试，还需要把测试环境给检查一遍，测试环境需要检查的主要有四项，
下面我分别来详细讲讲。
检查项一：关闭 SELinux如果你是 CentOS/RedHat 系列的操作系统，建议你关闭 SELinux，不然可能会遇到不少诡异的权限问题。
    我们通过下面这个命令，
    查看 SELinux 是否开启：$ sestatusSELinux status: disabled如果显示是开启的（enforcing），
    你可以通过$ setenforce 0来临时关闭；同时修改 /etc/selinux/config 文件来永久关闭，
    将 SELINUX=enforcing 改为 SELINUX=disabled。
检查项二：最大打开文件数然后，你需要用下面的命令，
    查看下当前系统的全局最大打开文件数：$ cat /proc/sys/fs/file-nr3984 0 3255296这里的最后一个数字，
    就是最大打开文件数。
    如果你的机器中这个数字比较小，那就需要修改 /etc/sysctl.conf 文件来增大：
    fs.file-max = 1020000
    net.ipv4.ip_conntrack_max = 1020000
    net.ipv4.netfilter.ip_conntrack_max = 1020000
    修改完以后，还需要重启系统服务来生效：
    sudo sysctl -p /etc/sysctl.conf
检查项三：进程限制除了系统的全局最大打开文件数，一个进程可以打开的文件数也是有限制的，
    你可以通过命令 ulimit 来查看：$ ulimit -n1024你会发现，这个值默认是 1024，是一个很低的数值。
    因为每一个用户请求都会对应着一个文件句柄，而压力测试会产生大量的请求，
    所以我们需要增大这个数值，把它改为百万级别，
    你可以用下面的命令来临时修改：$ ulimit -n 1024000
    也可以修改配置文件 /etc/security/limits.conf 来永久生效：
    * hard nofile 1024000* soft nofile 1024000
检查项四：Nginx 配置最后，你还需要对 Nginx 的配置，做一个小的修改，
    也就是下面这两行代码的操作：
    events { worker_connections 10240;}
    这样，我们就可以把每个 worker 的连接数增大了。
    因为它的默认值只有 512，这在大压力的测试下显然是不够的。
    压测前检查到此为止，测试环境已经准备好了。
    毕竟，人总会犯错，换个角度来做一次交叉测试，是非常重要的。
    最后的这次检测，可以分为两步。
第一步，使用自动化工具 c1000k。
    它来自 SSDB 的作者：https://github.com/ideawu/c1000k。从名字你就能看出来，这个工具的目的，
    就是用来检测你的环境是否可以满足 100 万并发连接的要求。这个工具的使用也很简单。
    我们分别启动一个 server 和 client，对应着监听 7000 端口的服务端程序，以及发起压力测试的客户端程序，
    目的是为了模拟真实环境下的压力测试：./server 7000./client 127.0.0.1 7000紧接着，
    client 会向 server 发送请求，检测当前的系统环境能否支持 100 万并发连接。
    你可以自己去运行一下，看看结果。
第二步，检测服务端程序是否正常运行。
    如果服务端的程序不正常，那么压力测试可能就成了错误日志刷新测试，或者是 404 响应测试。
    所以，测试环境检测的最后一步，也是最重要的一步，就是跑一遍服务端的单元测试集，
    或者手动调用几个主要的接口，来保证 wrk 测试的所有接口、返回的内容和 http 响应码都正常，
    并且在 logs/error.log 中没有出现任何错误级别的信息。发送请求好了，
到现在，万事俱备，只欠东风了。让我们开始用 wrk 来做压力测试吧！
    $ wrk -d 30 http://127.0.0.2:9080/hello
    
# 测试数据


wrk -t5 -c5 -d10s -T10s
```
wrk -t5 -c5 -d10s -T10s --script=post.lua --latency http://127.0.0.1:8082/v1/projects
Running 10s test @ http://127.0.0.1:8082/v1/projects
  5 threads and 5 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    55.53ms   76.11ms 604.34ms   94.94%
    Req/Sec    24.94      8.67    40.00     77.31%
  Latency Distribution
     50%   36.52ms
     75%   48.16ms
     90%   76.76ms
     99%  496.06ms
  1177 requests in 10.05s, 2.99MB read
  Socket errors: connect 0, read 7, write 0, timeout 0
Requests/sec:    117.08
Transfer/sec:    304.26KB
```

wrk -t10 -c10 -d10s 
```
wrk -t10 -c10 -d10s -T10s --script=post.lua --latency http://127.0.0.1:8082/v1/projects
Running 10s test @ http://127.0.0.1:8082/v1/projects
  10 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    43.45ms   21.68ms 176.14ms   85.69%
    Req/Sec    23.45      8.42    40.00     76.07%
  Latency Distribution
     50%   36.59ms
     75%   48.97ms
     90%   69.07ms
     99%  132.16ms
  2346 requests in 10.08s, 5.92MB read
  Socket errors: connect 0, read 14, write 0, timeout 0
  Non-2xx or 3xx responses: 16
Requests/sec:    232.75
Transfer/sec:    601.13KB
```

wrk -t20 -c20 -d10s -T10s
```
wrk -t20 -c20 -d10s -T10s --script=post.lua --latency http://127.0.0.1:8082/v1/projects
Running 10s test @ http://127.0.0.1:8082/v1/projects
  20 threads and 20 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    93.60ms   79.36ms 554.93ms   88.63%
    Req/Sec    13.77      6.98    30.00     81.44%
  Latency Distribution
     50%   65.73ms
     75%  105.20ms
     90%  187.79ms
     99%  417.05ms
  2460 requests in 10.10s, 6.22MB read
  Socket errors: connect 0, read 15, write 0, timeout 0
  Non-2xx or 3xx responses: 10
Requests/sec:    243.49
Transfer/sec:    630.61KB
```

wrk -t50 -c50 -d10s -T10s
```
wrk -t50 -c50 -d10s -T10s --script=post.lua --latency http://127.0.0.1:8082/v1/projects
Running 10s test @ http://127.0.0.1:8082/v1/projects
  50 threads and 50 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   226.13ms  157.02ms   1.02s    86.08%
    Req/Sec     5.89      3.29    20.00     73.53%
  Latency Distribution
     50%  176.65ms
     75%  272.22ms
     90%  408.91ms
     99%  872.40ms
  2382 requests in 10.10s, 5.99MB read
  Socket errors: connect 0, read 11, write 0, timeout 0
  Non-2xx or 3xx responses: 25
Requests/sec:    235.74
Transfer/sec:    606.65KB
```

wrk -t100 -c100 -d10s -T10s
```
wrk -t100 -c100 -d10s -T10s --script=post.lua --latency http://127.0.0.1:8082/v1/projects
Running 10s test @ http://127.0.0.1:8082/v1/projects
  100 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   460.69ms  230.42ms   1.48s    71.76%
    Req/Sec     2.26      1.73    20.00     78.97%
  Latency Distribution
     50%  418.09ms
     75%  585.80ms
     90%  774.01ms
     99%    1.18s 
  2112 requests in 10.09s, 5.33MB read
  Socket errors: connect 0, read 13, write 0, timeout 0
  Non-2xx or 3xx responses: 13
Requests/sec:    209.28
Transfer/sec:    540.73KB
```