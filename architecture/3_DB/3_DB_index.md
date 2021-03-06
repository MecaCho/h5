
# 数据结构

## 哈希表

哈希型的索引，对于排序查询时间复杂度会退化为O(n)，而树型的“有序”特性，依然能够保持O(log(n)) 的高效率。
所以，哈希表这种结构适用于只有等值查询的场景，比如 Memcached 及其他一些 NoSQL 引擎。

## 数组

如果仅仅看查询效率，有序数组就是最好的数据结构了。但是，在需要更新数据的时候就麻烦了，你往中间插入一个记录就必须得挪动后面所有的记录，成本太高。
有序数组索引只适用于静态存储引擎，比如你要保存的是 2017 年某个城市的所有人口信息，这类不会再修改的数据。

## 二叉树

二叉树是搜索效率最高的，但是实际上大多数的数据库存储却并不使用二叉树。其原因是，索引不止存在内存中，还要写到磁盘上。
想象一下一棵 100 万节点的平衡二叉树，树高 20。一次查询可能需要访问 20 个数据块。
在机械硬盘时代，从磁盘随机读一个数据块需要 10 ms 左右的寻址时间。
也就是说，对于一个 100 万行的表，如果使用二叉树来存储，单独访问一个行可能需要 20 个 10 ms 的时间，这个查询可真够慢的。

为什么不适合用作数据库索引？
(1)当数据量大的时候，树的高度会比较高，数据量大的时候，查询会比较慢；
(2)每个节点只存储一个记录，可能导致一次查询有很多次磁盘IO；

## “N 叉”树

为了让一个查询尽量少地读磁盘，就必须让查询过程访问尽量少的数据块。
那么，我们就不应该使用二叉树，而是要使用“N 叉”树。这里，“N 叉”树中的“N”取决于数据块的大小。

以 InnoDB 的一个整数字段索引为例，这个 N 差不多是 1200。
这棵树高是 4 的时候，就可以存 1200 的 3 次方个值，这已经 17 亿了。
考虑到树根的数据块总是在内存中的，一个 10 亿行的表上一个整数字段的索引，查找一个值最多只需要访问 3 次磁盘。其实，树的第二层也有很大概率在内存中，那么访问磁盘的平均次数就更少了。

### B树

B树，它的特点是：
(1)不再是二叉搜索，而是m叉搜索；
(2)叶子节点，非叶子节点，都存储数据；
(3)中序遍历，可以获得所有节点；

B树被作为实现索引的数据结构被创造出来，是因为它能够完美的利用“局部性原理”。

B树为何适合做索引？
(1)由于是m分叉的，高度能够大大降低；
(2)每个节点可以存储j个记录，如果将节点大小设置为页大小，例如4K，能够充分的利用预读的特性，极大减少磁盘IO；

### B+树

B+树，仍是m叉搜索树，在B树的基础上，做了一些改进：
(1)非叶子节点不再存储数据，数据只存储在同一层的叶子节点上；
    B+树中根到每一个节点的路径长度一样，而B树不是这样。
(2)叶子之间，增加了链表，获取所有节点，不再需要中序遍历；

这些改进让B+树比B树有更优的特性：
(1)范围查找，定位min与max之后，中间叶子节点，就是结果集，不用中序回溯；
    画外音：范围查询在SQL中用得很多，这是B+树比B树最大的优势。
(2)叶子节点存储实际记录行，记录行相对比较紧密的存储，适合大数据量磁盘存储；非叶子节点存储记录的PK，用于查询加速，适合内存存储；
(3)非叶子节点，不存储实际记录，而只存储记录的KEY的话，那么在相同内存的情况下，B+树能够存储更多索引；

## 跳表

## LSM 树

# InnoDB 的索引模型

在 MySQL 中，索引是在存储引擎层实现的，所以并没有统一的索引标准，即不同存储引擎的索引的工作方式并不一样。

每一个表是好几棵B+树, 树结点的key值就是某一行的主键，value是该行的其他数据。新建索引就是新增一个B+树，查询不走索引就是遍历主B+树。

## B+ 树

InnoDB 使用了 B+ 树索引模型，所以数据都是存储在 B+ 树中的。每一个索引在 InnoDB 里面对应一棵 B+ 树。

## 聚簇索引（clustered index）--主键索引

主键索引的叶子节点存的是整行数据。在 InnoDB 里，主键索引也被称为聚簇索引（clustered index）。

## 非主键索引

非主键索引的叶子节点内容是主键的值。在 InnoDB 里，非主键索引也被称为二级索引（secondary index）。

- 基于主键索引和普通索引的查询有什么区别？

如果语句是 select * from T where ID=500，即主键查询方式，则只需要搜索 ID 这棵 B+ 树；
如果语句是 select * from T where k=5，即普通索引查询方式，则需要先搜索 k 索引树，
得到 ID 的值为 500，再到 ID 索引树搜索一次。这个过程称为回表。

# 怎样维护索引

显然，主键长度越小，普通索引的叶子节点就越小，普通索引占用的空间也就越小。
从性能和存储空间方面考量，自增主键往往是更合理的选择。

## 页分裂

如果插入的数据不是在索引最后，或者最后一页索引所在的数据页已经满了，根据 B+ 树的算法，这时候需要申请一个新的数据页，然后挪动部分数据过去。这个过程称为页分裂。在这种情况下，性能自然会受影响。除了性能外，页分裂操作还影响数据页的利用率。原本放在一个页的数据，现在分到两个页中，整体空间利用率降低大约 50%。当然有分裂就有合并。当相邻两个页由于删除了数据，利用率很低之后，会将数据页做合并。合并的过程，可以认为是分裂过程的逆过程。

## 有没有什么场景适合用业务字段直接做主键的呢？

还是有的。比如，有些业务的场景需求是这样的：
1. 只有一个索引；
2. 该索引必须是唯一索引。
典型的 KV 场景。

## 索引重建?

非主键:
```
alter table T drop index k;
alter table T add index(k);
```

删除重建普通索引貌似影响不大，不过要注意在业务低谷期操作，避免影响业务。

主键：
```
alter table T drop primary key;
alter table T add primary key(id);
```

如果删除，新建主键索引，会同时去修改普通索引对应的主键索引，性能消耗比较大。
drop主键索引会导致其他索引失效，但drop普通索引不会。
顺序应是先删除k列索引，主键索引。然后再创建主键索引和k列索引。

1. 直接删掉主键索引是不好的，它会使得所有的二级索引都失效，并且会用ROWID来作主键索引；
2. 看到mysql官方文档写了三种措施，
    第一个是整个数据库迁移，先dump出来再重建表（这个一般只适合离线的业务来做）；
    第二个是用空的alter操作，比如ALTER TABLE t1 ENGINE = InnoDB;这样子就会原地重建表结构（真的吗？）；
    第三个是用repaire table，不过这个是由存储引擎决定支不支持的（innodb就不行）。

# 正确使用索引

数据库表中添加索引后确实会让查询速度起飞，但前提必须是正确的使用索引来查询，如果以错误的方式使用，则即使建立索引也会不奏效。

即使建立索引，索引也不会生效：

- like '%xx'
       select * from tb1 where name like '%cn';

- 使用函数
       select * from tb1 where reverse(name) = 'qwq';

- or
   select * from tb1 where nid = 1 or email = 'seven@live.com';
   特别的：当or条件中有未建立索引的列才失效，以下会走索引
           select * from tb1 where nid = 1 or name = 'seven';
           select * from tb1 where nid = 1 or email = 'seven@live.com' and name = 'alex'

- 类型不一致
   如果列是字符串类型，传入条件是必须用引号引起来，不然...
   select * from tb1 where name = 999;

- !=
   select * from tb1 where name != 'alex'
   特别的：如果是主键，则还是会走索引
       select * from tb1 where nid != 123

- >
   select * from tb1 where name > 'alex'
   特别的：如果是主键或索引是整数类型，则还是会走索引
       select * from tb1 where nid > 123
       select * from tb1 where num > 123

- order by
   select email from tb1 order by name desc;
   当根据索引排序时候，选择的映射如果不是索引，则不走索引
   特别的：如果对主键排序，则还是走索引：
       select * from tb1 order by nid desc;

- 组合索引最左前缀
   如果组合索引为：(name,email)
   name and email       -- 使用索引
   name                 -- 使用索引
   email                -- 不使用索引


# 覆盖索引是什么？    

就是假如有一个联合索引(a,b,c)，如果我们只是需要a,b,c这几个字段的数据，查询时就不需要根据主键id去聚集索引里面回表查询了

SELECT a,b,c FROM user where a = 1

这个就是覆盖索引。

# “N叉树”的N值在MySQL中是可以被人工调整的么？

可以按照调整key的大小的思路来说；

如果你能指出来5.6以后可以通过page大小来间接控制应该能加分吧

# 现在一般自增索引都设置为bigint?

特别合理，因为现在很多业务插入数据很凶残，容易超过int 上限，

实际上是建议设置bigint unsigned

# 如果插入的数据是在主键树叶子结点的中间，后面的所有页如果都是满的状态，是不是会造成后面的每一页都会去进行页分裂操作，直到最后一个页申请新页移过去最后一个值?

1. 不会不会，只会分裂它要写入的那个页面。每个页面之间是用指针串的，改指针就好了，不需要“后面的全部挪动

# 插入数据如果是在某个数据满了页的首尾，为了减少数据移动和页分裂，会先去前后两个页看看是否满了，如果没满会先将数据放到前后两个页上，不知道是不是有这种情况?

2. 对，减为了增加空间利用率

# 非聚集索引上为啥叶子节点的value为什么不是地址，这样可以直接定位到整条数据，而不用再次对整棵树进行查询?

作者回复: 这个叫作“堆组织表”，MyISAM就是这样的，各有利弊。你想一下如果修改了数据的位置的情况，InnoDB这种模式是不是就方便些

# questions

1、什么情况下创建索引才有意义？有哪些限制？比如字段长度
2、如何查看索引占用多少空间？
3、查看索引数的结构，比如多少个层，多少节点？
4、如何查看索引的利用率。比如我创建了一个索引，是否可以有记录这个索引被调用了多少次？

1. 有这个索引带来的查询收益，大于维护索引的代价，就该建😄 对于可能变成大表的表，实际上如果不建索引会导致全表扫描，这个索引就是必须的。
2. 可以估算出来的，根据表的行数和索引的定义。
3.跟2一样。 如果要精确的，就要解数据文件，这个工具可以看看 https://github.com/jeremycole/innodb_diagrams
4. performance_schema.table_io_waits_summary_by_index_usage能看到一些信息

# 外键

外键可以用来做约束
但是这种约束关系是在数据库里面做的（类似于存储过程，其实是一种逻辑）

这种情况下，等于你的数据库里面也有业务逻辑，
这个就要看项目管理上做得怎么样

如果能够把这些关系也作为代码的一部分，其实是可以的
之前很多人会觉得说加了存储过程、触发器、外键这些以后，代码逻辑混乱，
一个原因也是因为没有把数据库里的逻辑像代码一样管理好

# InnoDB到底支不支持哈希索引？

对于InnoDB的哈希索引，确切的应该这么说：    
（1）InnoDB用户无法手动创建哈希索引，这一层上说，InnoDB确实不支持哈希索引；    
（2）InnoDB会自调优(self-tuning)，如果判定建立自适应哈希索引(Adaptive Hash Index, AHI)，
    能够提升查询效率，InnoDB自己会建立相关哈希索引，这一层上说，InnoDB又是支持哈希索引的；
    
 当业务场景为下面几种情况时：
- 很多单行记录查询（例如passport，用户中心等业务）

- 索引范围查询（此时AHI可以快速定位首行记录）

- 所有记录内存能放得下

AHI往往是有效的。

当业务有大量like或者join，AHI的维护反而可能成为负担，降低系统效率，此时可以手动关闭AHI功能。



