
1。什么是linux惊群效应？    

惊群效应也叫雷鸣群体效应,简言之,就是多进程(线程)在同时阻塞等待同一个事件的时候(休眠状态),
如果等待的这个事件发生,那么他会唤醒等待的所有进程(线程), 
但是最终只可能有一个进程(线程)获得这个时间的"控制权",对该事件进行处理,
而其他进程(线程)获得"控制权"失败,只能重新进入休眠状态,这种现象和性能浪费叫做惊群；

消耗:

系统对用户进程/线程频繁地做无效的调度,上下文切换系统性能大打折扣
为了确保只有一个线程得到资源,用户必须对资源进行加锁保护,进一步加大系统开销

2。多线程的优缺点？    

优点:

- 能适当提高程序的执行效率
- 能适当提高资源的利用率(CPU&内存)
- 线程上的任务执行后自动销毁     

缺点:    
- 开启线程需要占用一定的内存空间    
- 如果开启大量的线程,会占用大量的内存空间,降低程序的性能    
- 线程越多,cpu在调用线程上的开销就越大    
- 程序设计更加复杂,比如线程简的通信,多线程的数据共享

3。Linux I/O模型一共有哪些？

1.同步模型（synchronous IO）

2.阻塞IO（bloking IO）

3.非阻塞IO（non-blocking IO）

4.多路复用IO（multiplexing IO）

5.信号驱动式IO（signal-driven IO）

signal driven IO在实际中并不常用

6.异步IO（asynchronous IO）


4。同步与异步的区别是什么？    

同步与异步的区别在于调用结果的通知方式上。     
同步执行一个方法后，需要等待结果返回，然后继续执行下去。     
异步执行一个方法后，不会等待结果的返回。


5。阻塞与非阻塞的区别是什么？

阻塞与非阻塞的区别在于进程/线程在等待消息时，进程/线程是否是挂起状态。

6。孤儿进程,僵尸进程,守护进程？

孤儿进程：在其父进程执行完成或被终止后仍继续运行的一类进程。
僵尸进程： 一个进程使用fork创建子进程，如果子进程退出，而父进程并没有调用wait或waitpid获取子进程的状态信息，那么子进程的进程描述符仍然保存在系统中。这种进程称之为僵尸进程。
守护进程：后台服务进程，因为它会有一个很长的生命周期提供服务，关闭终端不会影响服务，也就是说可以忽略某些信号。

- 实现守护进程     
  首先要保证进程在后台运行，可以在启动程序后面加&；然后是与终端、进程组、会话(Session)分离。
  使用Nohup nohup命令，是让程序以守护进程运行的方式之一，程序运行后忽略SIGHUP信号，也就说关闭终端不会影响进程的运行。
  类似的命令还有disown
  
7。什么是软链接?

什么是软链接符号链接(Symbolic Link)（symlink），又称软链接(Soft Link)，
是一种特殊的文件，它指向 Linux 系统上的另一个文件或目录。
这和 Windows 系统中的快捷方式有点类似，链接文件中记录的只是原始文件的路径，并不记录原始文件的内容。
符号链接通常用于对库文件进行链接，也常用于链接日志文件和网络文件系统(Network File System)（NFS）上共享的目录。

什么是硬链接硬链接是原始文件的一个镜像副本。
创建硬链接后，如果把原始文件删除，链接文件也不会受到影响，因为此时原始文件和链接文件互为镜像副本。
为什么要创建链接文件而不直接复制文件呢？当你需要将同一个文件保存在多个不同位置，而且还要保持持续更新的时候，
硬链接的重要性就体现出来了。如果你只是单纯把文件复制到另一个位置，
那么另一个位置的文件只会保存着复制那一刻的文件内容，后续也不会跟随着原始文件持续更新。
而使用硬链接时，各个镜像副本的文件内容都会同时更新。

        
