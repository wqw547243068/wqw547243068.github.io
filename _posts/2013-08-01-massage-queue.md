---
layout: post
title:  "消息队列-Message Queue"
date:   2013-08-01 23:02:00
categories: 工具
tags:  kafka 消息队列 mq zookeeper
excerpt: 消息队列知识点、经验总结
author: 鹤啸九天
mathjax: true
permalink: /massage_queue
---

* content
{:toc}


# 消息队列


## 介绍

消息队列是分布式系统中重要的中间件，在高性能、高可用、低耦合等系统架构中扮演着重要作用。

分布式系统可以借助消息队列的能力，轻松实现以下功能：
- 解耦，将一个流程的上游和下游拆开，上游专注生产消息，下游专注处理消息。
- 广播，一个上游生产的消息轻松被多个下游服务处理。
- 缓冲，应对流量突然上涨，消息队列可以扮演一个缓冲器的作用，保护下游服务使其可以根据实际的消费能力处理消息。
- 异步，上游发送消息后可以马上返回，下游可以异步处理消息。
- 冗余，保留历史消息，处理失败或当出现异常时可以进行重试或者回溯防止丢失。

举例——小明收快递的烦恼

消息队列主要作用：**解耦**，**削峰**，**异步**，还有**提高接收者性能**。

**异步消息队列**作用
- 解耦，生产端和消费端不需要相互依赖
- 异步，生产端不需要等待消费端响应，直接返回，提高了响应时间和吞吐量
- 削峰，打平高峰期的流量，消费端可以以自己的速度处理，同时也无需在高峰期增加太多资源，提高资源利用率
- 提高消费端性能。消费端可以利用buffer等机制，做批量处理，提高效率。

快递员给小明送快递分为几步？分为3步，
- 第一步，把快递拿到小明家门口（省略了前n步，从小明家楼下开始）
- 第二步，敲门（类比编程世界的调用第三方接口）
- 第三步，小明开门拿走快递（第三方接口执行过程）

这简单的三步会有什么问题？
- （1）**耦合**
  - 快递员是否能顺利完成十分依赖于小明的响应速度。如果小明还没起床，听见敲门声再穿衣服开门，可能消耗很多时间。如果小明没在家呢？那就要配送失败了，如何判断配送失败呢？快递员需要判断等多久开门（超时时间），打电话判断是否在家（健康检查），最终郁闷的离开，下次再来一次（重试）。
  - 快递员直接与小明交互，对小明的状态强依赖，产生了**耦合**现象。那有办法避免这种耦合呢？
- （2）**同步**影响性能
  - 快递员的配送速度收到小明的响应速度影响极大，有一两个需要长时间等待的快件，快递员的配送效率（吞吐率）会收到很大影响。
- （3）高峰期**负载**很高
  - 双11，618，每次到购物节的时候，快递员都很烦躁。快递太多，来的比送得快，这可如何是好。
  - 小明也很烦躁，一天要收100个快递，可是家里的空间都满了，要边收拾出地方边进一件快递。
- （4）接收方还有其他事情
  - 如果小明准备和女朋友告白，此时来了一阵敲门声，你好，快递。
  - 还双11，小明买了100件商品，明天不定时一件件送到，小明这一天都要搭进去了。

接收快递也成为了一件烦心事，好想把其他事情处理完再收快递，也好想一块收100件快递。

这时候有个叫 丰巢（没收广告费）的**快递柜**出现了，快递员可以把快递放到柜子里，发条短信通知小明过来取快递。小明看到短信可以先做自己的事情，有空的时候过来拿走快递。

终于，小明和快递员都笑容满面。

快递柜就相当于是编程世界的**消息队列**。
- **解偶**
  - 此时，快递员只需要把快递放到柜子里，不需要关心小明是否在家，是否在睡觉。小明也不需要一直等待给快递员开门，两个人解耦了。
- **异步**
  - 快递员把快递放到柜子里发个信息就可以去送下一件，不需同步等待结果。
  - 这样每个快递的处理速度（响应时间）都变得极短，每天送的快递数量（吞吐量）也变多了。
- **削峰**
  - 这次又到了双十一，小明还是一天要到100个快递，由于小明一天只能消化10个快递，剩下的就放在了柜子里，等10天后才拿完。
  - 快递员由于是异步送快递，双11根本不是事，这点吞吐量完全搞得定。
- 提高消费端**性能**
  - 小明以前需要一件一件收取快递，现在放在了柜子（队列）里，那等攒够了10件去取一次（buffer->reduce），好省时间！其他时间都可以快快乐乐约会了。

[链接](https://www.jianshu.com/p/1ae35123329e)


## 技术原理

### 消息队列对比

【2022-2-25】[10分钟搞懂！消息队列选型全方位对比](https://www.toutiao.com/i7068118963414106631/?)

- 对Kafka、Pulsar、RocketMQ、RabbitMQ、NSQ这几个消息队列组件进行了一些调研，并整理了相关资料，为业务对MQ中间件选型提供参考。
- ![](https://p26.toutiaoimg.com/origin/tos-cn-i-tjoges91tu/SyKJE2l7zvRRoR)

结论：
- 日志处理、大数据处理等场景，**高吞吐量、低延迟**的特性考虑，**Kafka**依旧是一个较好的选型。
- 针对业务交易数据，有延迟消息、队列模式消费、异地容灾，多消息主题等场景，可以选用TDMQ/Pulsar。
- 其他一些业务自定义的使用场景，由于后台技术栈是Golang，可以考虑采用NSQ进行定制开发或研究学习。
- 消息中间件性能跟服务端、客户端参数、使用场景等方面上有很大关系，在系统上线前，还需要根据实际应用场景进行压测调优。

消息队列（MQ）选型和用法因产品差异较大, 通用核心 + 主流对比 + 最小可跑示例

核心模型

```
Producer ──发消息──> [ Topic/Queue ] ──拉取──> Consumer Group
                                      (分区/队列, 可多实例并行消费)
```

| 概念 | 含义 |
|------|------|
| **Topic** | 消息主题，逻辑分类（如 `order_created`） |
| **Partition/Queue** | 分区，并行消费的物理单元；同 key 进同分区保顺序 |
| **Producer** | 生产者，发消息的一方 |
| **Consumer Group** | 消费者组，组内分摊消费，组间各自独立消费全量 |
| **Offset** | 消费位点，记录消费到哪了 |

主流选型

| 产品 | 强项 | 典型场景 |
|------|------|----------|
| **Kafka** | 高吞吐（百万 TPS）、日志型、可重放 | 日志、事件流、大数据管道 |
| **RocketMQ** | 事务消息、顺序、定时、金融级可靠 | 订单、交易、计费 |
| **RabbitMQ** | 灵活路由、AMQP 协议、低延迟 | 任务分发、异步解耦 |
| **Pulsar** | 存算分离、多租户、地域复制 | 云原生、大规模流 |

滴滴内部常用 **DDMQ**（基于 Kafka/RocketMQ 封装的平台）。

四款 MQ 按「缓存机制 / 空间 / 过期时间」三维度重新整理：

缓存空间、时间

| 维度 | Kafka | RocketMQ | RabbitMQ | Pulsar |
|------|-------|----------|----------|--------|
| 缓存载体 | Page Cache | MMap/堆外 | 队列内存 | Broker Cache + BookKeeper |
| 默认内存上限 | 无限（OS 管理） | 1 GB 堆积阈值 | RAM 40% 流控 | 堆的 20% |
| 单条 TTL | ❌ 不支持 | ✅ 延迟消息 | ✅ 三档配置 | ✅ namespace 级 |
| 默认过期 | 7 天 | 72h | 需手动配 | 默认不过期 |
| 过期去向 | 直接删除 | 延迟投递/删除 | 死信队列 DLX | 自动 ack |
| 堆积影响吞吐 | 小（顺序盘） | 小 | 大（内存打满） | 无（存算分离） |

选型
- **要单条 TTL + 死信** → RabbitMQ
- **要延迟投递 + 金融可靠** → RocketMQ
- **海量日志 + 按时间清理** → Kafka
- **堆积不降吞吐 + 多租户** → Pulsar

### 示例

最小用法（以 Kafka + Python 为例）

```bash
pip install confluent-kafka
```

**生产者：**

```py
from confluent_kafka import Producer

p = Producer({"bootstrap.servers": "localhost:9092"})

def delivery(err, msg):
    if err: print(f"发送失败: {err}")
    else: print(f"已发到 {msg.topic()}[{msg.partition()}]@{msg.offset()}")

p.produce("order_created", key="user_123", value=b'{"order":"A"}', callback=delivery)
p.flush()  # 等待所有消息发完
```

**消费者：**

```py
from confluent_kafka import Consumer

c = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "order_service",
    "auto.offset.reset": "latest",  # 或 earliest
})
c.subscribe(["order_created"])

while True:
    msg = c.poll(1.0)
    if msg is None: continue
    if msg.error():
        print(f"消费错误: {msg.error()}")
        continue
    process(msg.value())          # 业务处理
    # 手动提交位点（关掉 enable.auto.offset.store 更可控）
```


关键配置与避坑

| 配置/做法 | 说明 |
|-----------|------|
| `acks=all`（Kafka） | 等所有副本确认才算成功，防丢消息 |
| 幂等生产者 `enable.idempotence=true` | 防重试导致重复 |
| 手动提交 offset | 处理完再提交，防"消费到但没处理完就提交"导致丢失 |
| 同 key 同分区 | 保序（如按 orderId 取 hash） |
| 消费者数 ≤ 分区数 | 超出会闲置 |
| 死信队列（DLQ） | 处理失败的消息别丢，单独存 |
| 消息大小 | Kafka 默认 1MB，超了改 `max.message.bytes` 或拆包 |

四大典型场景
1. **异步解耦**：下单后发 MQ，库存/积分/通知各自消费，主流程不等
2. **削峰填谷**：秒杀请求先进队列，消费端按能力处理
3. **日志/事件流**：埋点 → Kafka → Flink/数仓
4. **广播通知**：多服务订阅同一 topic 各自处理

可靠性三连问
- **不丢消息**：生产 `acks=all` + 消费手动提交 + 关闭自动位点
- **不重复**：生产端幂等 + 消费端幂等（用唯一 ID 去重，如 Redis SETNX）
- **保序**：同业务 key 路由同分区 + 单线程消费该分区



## RocketMQ

| 维度 | 说明 |
|------|------|
| **缓存机制** | CommitLog 用 **MMap 内存映射**，同样依赖 page cache；开启 `transientStorePoolEnable=true` 后用**堆外内存**写缓冲，绕过 page cache 直写；支持内存预读 |
| **空间** | 堆积内存阈值 `maxMessageMemory` 默认 **1 GB**，超阈值触发限流；磁盘存储受 `fileReservedTime` 和磁盘容量约束 |
| **过期时间** | `fileReservedTime` 默认 **72h**，过期文件自动物理删除；支持**延迟消息**（18 级：1s/5s/.../2h）；单条可设 `deliverTimeMs` 定时投递 |

## RabbitMQ

| 维度 | 说明 |
|------|------|
| **缓存机制** | 消息驻留**队列内存**，到水线换页落盘；ack 后从队列移除；无 page cache 概念，靠自身内存管理 |
| **空间** | `vm_memory_high_watermark` 默认 **RAM 的 40%**；到此水线触发**流控**阻塞 publisher；到 `paging_ratio`（0.5，即 20% RAM）开始**换页到磁盘**；队列长度可配 `x-max-length` |
| **过期时间** | TTL 最完整，三档可配：① 单条 `message.expiration`（ms）② 队列级 `x-message-ttl`（ms）③ 队列自身 `x-expires`（空闲多久自动删）；过期消息走 `x-dead-letter-exchange` 进死信队列 |

### Pulsar

| 维度 | 说明 |
|------|------|
| **缓存机制** | **存算分离**——broker 只缓存不持久化，数据存 BookKeeper；broker 用 **Managed Ledger Cache** 缓存最近读写消息 |
| **空间** | `managedLedgerCacheSizeMB` 默认 **可用堆的 20%**；到 `evictionWatermark`（0.9，即 90% 满）开始驱逐；堆积存 BookKeeper，不占 broker 内存 |
| **过期时间** | `messageTTL`（namespace 级，默认 **0 禁用**）——消息多久后自动标记 ack；`retention` 控制**已 ack 消息保留**多久；堆积无上限（受 BookKeeper 容量限制） |

## kafka

Kafka是一种分布式的基于**发布/订阅**的消息系统，它的高吞吐量、灵活的offset是其它消息系统所没有的。

一个Kafka集群由多个Broker和一个ZooKeeper集群组成，Broker作为Kafka节点的服务器。同一个消息主题Topic可以由多个分区Partition组成，分区物理存储在Broker上。负载均衡考虑，同一个Topic的多个分区存储在多个不同的Broker上，为了提高可靠性，每个分区在不同的Broker会存在副本。

![](https://p26.toutiaoimg.com/origin/tos-cn-i-tjoges91tu/SyKJE3YBz11RIa?from=pc)

【2021-5-23】[Kafka原理篇：图解kafka架构原理](https://www.toutiao.com/i6965046292519076384/)
- Kafka 架构设计哲学和原理
- Kafka 中 zookeeper 的作用
- Kafka Controller 实现原理
- Kafka Network 原理

![](https://p6-tt.byteimg.com/origin/pgc-image/c1a01e62d7e24f3c97007a84c4b8e0fe?from=pc)

资料
- [kafka入门简介](https://zhuanlan.zhihu.com/p/31731892)
- [Python操作Kafka的通俗总结](https://zhuanlan.zhihu.com/p/279784873)

kafka运行在集群上，集群包含一个或多个服务器。kafka把消息存在topic中，每一条消息包含键值（key），值（value）和时间戳（timestamp）。

基本概念
- `Topic`：一组消息数据的标记符；**主题**，由用户定义并配置在Kafka服务器，用于建立Producer和Consumer之间的订阅关系。生产者发送消息到指定的Topic下，消息者从这个Topic下消费消息。
- `Producer`：**生产者**，用于生产数据，可将生产后的消息送入指定的Topic；向kafka broker发消息的客户端
- `Consumer`：**消费者**，消息的使用方，负责消费Kafka服务器上的消息; 获取数据，可消费指定的Topic；
- `Consumer Group`：**消费者分组**，用于归组同类消费者。每个consumer属于一个特定的consumer group，多个消费者可以共同消息一个Topic下的消息，每个消费者消费其中的部分消息，这些消费者就组成了一个分组，拥有同一个分组名称，通常也被称为消费者集群。同一个group可以有多个消费者，一条消息在一个group中，只会被一个消费者获取；
- `Partition`：**分区** partition，每个partition是一个有序的队列。partition中的每条消息都会被分配一个有序的
id（offset）。为了保证kafka的吞吐量，一个Topic可以设置**多个**分区。同一分区只能被**一个**消费者订阅。
- `Broker`：一台kafka服务器就是一个broker。一个集群由多个broker组成。一个broker可以容纳多个topic。**备份**作用
- `Offset`：消息在partition中的偏移量。每一条消息在partition都有唯一的偏移量，消息者可以指定偏移量来指定要消费的消息。

| 维度 | 说明 |
|------|------|
| **缓存机制** | 不用 JVM 堆，靠 **OS Page Cache** 加速读写；消息先进 `log.buffer.list` 缓冲池再落盘 CommitLog；消费端优先从 page cache 命中，未命中读磁盘 |
| **空间** | Producer `buffer.memory` 默认 **32 MB**；broker 缓冲池自动管理，无硬上限（用尽可用内存）；最终落盘，受磁盘容量限制 |
| **过期时间** | 按 segment 级别清理，非单条。`log.retention.hours` 默认 **168h（7天）**；也可按大小 `retention.bytes`（默认 **-1 无限**）；topic 级可单独配 `retention.ms` |

kafka分布式架构
- ![](https://pic3.zhimg.com/80/v2-f04083507c2860e62a686c3e868c719a_720w.jpg)
解释
- kafka将topic中的消息存在不同的partition中。如果存在键值（key），消息按照键值（key）做分类存在不同的partiition中，如果不存在键值（key），消息按照轮询（Round Robin）机制存在不同的partition中。默认情况下，**键值**（key）决定了一条消息会被存在哪个partition中。
- partition中的消息序列是**有序**的消息序列。kafka在partition使用**偏移量**（offset）来指定消息的位置。一个topic的一个partition只能被一个consumer group中的一个consumer消费，多个consumer消费同一个partition中的数据是不允许的，但是一个consumer可以消费多个partition中的数据。
- kafka将partition的数据复制到不同的broker，提供了partition数据的**备份**。每一个partition都有一个broker作为leader，若干个broker作为follower。所有的数据读写都通过leader所在的服务器进行，并且leader在不同broker之间复制数据。
  - ![](https://pic3.zhimg.com/80/v2-e9b8513d58089eee6a131278ea949502_720w.jpg)


```shell
# 安装kafka
# ①下载解压
wget https://archive.apache.org/dist/kafka/0.10.0.0/kafka_2.11-0.10.0.0.tgz
tar -xzf kafka_2.11-0.10.0.0.tgz
cd kafka_2.11-0.10.0.0
# ②启动Kafka： kafka需要用到zookeeper，所以需要先启动zookeeper。用下载包里自带的单机版zookeeper。
bin/zookeeper-server-start.sh config/zookeeper.properties # 启动zk
bin/kafka-server-start.sh config/server.properties # 启动kafka
# ③创建topic，test，一个分区
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
# ④查看创建的topic
bin/kafka-topics.sh --list --zookeeper localhost:2181 # test
# ⑤向topic中发送消息
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
# This is a message
# This is another message
# ⑤从topicc中消费消息
bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic test --from-beginning
# This is a message
# This is another message

# python的kafka客户端
pip install kafka-python
```

kafka-python是一个python的Kafka客户端，可以用来向kafka的topic发送消息、消费消息。
- 一个producer和一个consumer，producer向kafka发送消息，consumer从topic中消费消息。
- ![](https://pic3.zhimg.com/80/v2-198d01ebb230395234999a3b8ac07502_720w.jpg)

【2022-3-18】[python kafka订阅](https://blog.csdn.net/qq_41048831/article/details/107660056)

Kafka发送消息主要有三种方式：
1. 发送并忘记：1.88s, 吞吐量是最高的，但是无法保证消息的可靠性
2. 同步发送：16s, 通过get方法等待Kafka的响应，判断消息是否发送成功
  - 一条一条的发送，对每条消息返回的结果判断， 可以明确地知道每条消息的发送情况，但是由于同步的方式会阻塞，只有当消息通过get返回future对象时，才会继续下一条消息的发送
3. 异步发送+回调函数：2.15s, 消息以异步的方式发送，通过回调函数返回消息发送成功/失败
  - 调用send方法发送消息的同时，指定一个回调函数，服务器在返回响应时会调用该回调函数，通过回调函数能够对异常情况进行处理，当调用了回调函数时，只有回调函数执行完毕生产者才会结束，否则一直会阻塞

三种方式虽然在时间上有所差别，但并不是说时间越快的越好，具体看业务应用场景：
- 场景1：如果业务要求消息必须是按顺序发送的，那么可以使用同步的方式，并且只能在一个partation上，结合参数设置retries的值让发送失败时重试，设置max_in_flight_requests_per_connection=1，可以控制生产者在收到服务器晌应之前只能发送1个消息，从而控制消息顺序发送；
- 场景2：如果业务只关心消息的吞吐量，容许少量消息发送失败，也不关注消息的发送顺序，那么可以使用发送并忘记的方式，并配合参数acks=0，这样生产者不需要等待服务器的响应，以网络能支持的最大速度发送消息；
- 场景3：如果业务需要知道消息发送是否成功，并且对消息的顺序不关心，那么可以用异步+回调的方式来发送消息，配合参数retries=0，并将发送失败的消息记录到日志文件中；


三种发送方法：

```python
import pickle
import time
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['192.168.33.11:9092'],
                         key_serializer=lambda k: pickle.dumps(k),
                         value_serializer=lambda v: pickle.dumps(v))
start_time = time.time()
# -------- (1) ----------
for i in range(0, 10000):
    print('------{}---------'.format(i))
    future = producer.send('test_topic', key='num', value=i, partition=0)
# 将缓冲区的全部消息push到broker当中
producer.flush()
producer.close()

# -------- (2) ----------
from kafka.errors import kafka_errors

for i in range(0, 10000):
    print('------{}---------'.format(i))
    future = producer.send(topic="test_topic", key="num", value=i)
    # 同步阻塞,通过调用get()方法进而保证一定程序是有序的.
    try:
        record_metadata = future.get(timeout=10)
        # print(record_metadata.topic)
        # print(record_metadata.partition)
        # print(record_metadata.offset)
    except kafka_errors as e:
        print(str(e))
# -------- (3) ----------
def on_send_success(*args, **kwargs):
    """
    发送成功的回调函数
    :param args:
    :param kwargs:
    :return:
    """
    return args

def on_send_error(*args, **kwargs):
    """
    发送失败的回调函数
    :param args:
    :param kwargs:
    :return:
    """
    return args

start_time = time.time()
for i in range(0, 10000):
    print('------{}---------'.format(i))
    # 如果成功,传进record_metadata,如果失败,传进Exception.
    producer.send(
        topic="test_topic", key="num", value=i
    ).add_callback(on_send_success).add_errback(on_send_error)
producer.flush()
producer.close()
# =================
end_time = time.time()
time_counts = end_time - start_time
print(time_counts)

```


producer代码
- [kafka-python基本使用](https://zhuanlan.zhihu.com/p/38330574)

```python
# producer.py
import time
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers="localhost:9092")
# 指定编码
# producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda m: json.dumps(m).encode('ascii'))
# 压缩发送
# producer = KafkaProducer(bootstrap_servers=['localhost:9092'], compression_type='gzip') # gzip
# producer = KafkaProducer(value_serializer=msgpack.dumps) # msgpack为MessagePack的简称，是高效二进制序列化类库，比json高效

i = 0
while True:
    ts = int(time.time() * 1000)
    producer.send(topic="test", value=str(i), key=str(i), timestamp_ms=ts)
    producer.flush()
    print i
    i += 1
    time.sleep(1)
```

consumer代码

```python
# consumer.py
from kafka import KafkaConsumer

consumer = KafkaConsumer("test", bootstrap_servers=["localhost:9092"])
# 自动解码
# consumer = KafkaConsumer(group_id= 'group2', bootstrap_servers= ['localhost:9092'], value_deserializer=lambda m: json.loads(m.decode('ascii')))
# 手工分配partition
# consumer = KafkaConsumer(group_id= 'group2', bootstrap_servers= ['localhost:9092'])
# consumer.assign([TopicPartition(topic= 'my_topic', partition= 0)])
# 超时处理
# consumer = KafkaConsumer('my_topic', group_id= 'group2', bootstrap_servers= ['localhost:9092'], consumer_timeout_ms=1000)

for message in consumer:
    print message
```

生产者和消费者的简易Demo演示：

```python
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import kafka_errors
import traceback
import json


def producer_demo():
    """ 生产者 """
    # 假设生产的消息为键值对（不是一定要键值对），且序列化方式为json
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'], 
        key_serializer=lambda k: json.dumps(k).encode(),
        value_serializer=lambda v: json.dumps(v).encode())
    # 发送三条消息
    for i in range(0, 3):
        future = producer.send(
            'kafka_demo',
            key='count_num',  # 同一个key值，会被送至同一个分区
            value=str(i),
            partition=1)  # 向分区1发送消息
        print("send {}".format(str(i)))
        try:
            future.get(timeout=10) # 监控是否发送成功           
        except kafka_errors:  # 发送失败抛出kafka_errors
            traceback.format_exc()

def consumer_demo():
    """ 消费者 """
    consumer = KafkaConsumer(
        'kafka_demo', 
        bootstrap_servers=':9092',
        group_id='test'
    )
    for message in consumer:
        print("receive, key: {}, value: {}".format(
            json.loads(message.key.decode()),
            json.loads(message.value.decode())
            )
        )
```

- 先执行消费者：consumer_demo()
- 再执行生产者：producer_demo()
- 会看到如下输出：

```shell
producer_demo()
# send 0
# send 1
# send 2

consumer_demo()
# receive, key: count_num, value: 0
# receive, key: count_num, value: 1
# receive, key: count_num, value: 2
```

[kafka多消费者](https://blog.csdn.net/weixin_39737224/article/details/112073632)

传统的消息引擎处理模型主要有两种：**队列模型**，和**发布-订阅模型**。
- `队列`模型：早期消息处理引擎就是按照队列模型设计的，所谓队列模型，跟队列数据结构类似，生产者产生消息，就是入队，消费者接收消息就是出队，并删除队列中数据，消息只能被消费一次。 但这种模型有一个问题，那就是只能由一个消费者消费，无法直接让多个消费者消费数据。基于这个缺陷，后面又演化出发布-订阅模型。 
- `发布-订阅`模型：发布订阅模型中，多了一个主题。消费者会预先订阅主题，生产者写入消息到主题中，只有订阅了该主题的消费者才能获取到消息。这样一来就可以让多个消费者消费数据。

借助kafka的消费者组机制，可以同时实现这两种模型。同时还能够对消费组进行动态扩容，让消费变得易于伸缩。

消费者组是由消费者组成的，组内可以有多个消费者实例，而这些消费者实例共享一个id，称为group id。
- 默认创建消费者的group id是在 KAFKA_HOME/conf/consumer.properties 文件中定义的，打开就能看到。
- 默认的group id值是test-consumer-group。

消费者组内的所有成员一起订阅某个主题的所有分区，注意一个消费者组中，每一个分区只能由组内的一消费者订阅。

注意：
- 消费者组内消费者小于或等于分区数，以及topic分区数刚好是消费者组内成员数的倍数。
- 消费者组内的消费者数量最好是与分区数持平，再不济，最好也是要是分区数的数量成比例。

重平衡（Rebalance）其实就是一个协议，它规定了如何让消费者组下的所有消费者来分配topic中的每一个分区。比如一个topic有100个分区，一个消费者组内有20个消费者，在协调者的控制下让组内每一个消费者分配到5个分区，这个分配的过程就是重平衡。

重平衡的触发条件主要有三个：
- 消费者组内成员发生变更，这个变更包括了增加和减少消费者。注意这里的减少有很大的可能是被动的，就是某个消费者崩溃退出了
- 主题的分区数发生变更，kafka目前只支持增加分区，当增加的时候就会触发重平衡
- 订阅的主题发生变化，当消费者组使用正则表达式订阅主题，而恰好又新建了对应的主题，就会触发重平衡
为什么说重平衡为人诟病呢？因为重平衡过程中，消费者无法从kafka消费消息，这对kafka的TPS影响极大，而如果kafka集内节点较多，比如数百个，那重平衡可能会耗时极多。数分钟到数小时都有可能，而这段时间kafka基本处于不可用状态。所以在实际环境中，应该尽量避免重平衡发生。

kafka提供了三种重平衡分配策略
- Range：基于每个主题的分区分配，如果主题的分区分区不能平均分配给组内每个消费者，那么对该主题，某些消费者会被分配到额外的分区。
- RoundRobin：基于全部主题的分区来进行分配的，同时这种分配也是kafka默认的rebalance分区策略。
- Sticky：最新的也是最复杂的策略，为了一定程度解决上面提到的重平衡非要重新分配全部分区的问题。称为粘性分配策略。

[原文链接](https://blog.csdn.net/weixin_39737224/article/details/112073632)

kafka订阅多个topic，可以同时接收多个topic消息

```python
from kafka import KafkaConsumer
# 订阅多个topic
# （1）直接指定topic名称
consumer = KafkaConsumer(group_id= 'group2', bootstrap_servers= ['localhost:9092'])
consumer.subscribe(topics= ['my_topic', 'topic_1'])
# （2）或 正则匹配topic
consumer = KafkaConsumer(group_id= 'group2', bootstrap_servers= ['localhost:9092'], value_deserializer=lambda m: json.loads(m.decode('ascii')))
consumer.subscribe(pattern= '^my.*')

for msg in consumer:
    print(msg)
```


# 结束

