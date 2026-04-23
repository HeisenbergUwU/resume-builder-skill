# 技术简历写作指南

## 核心原则

### FAB 模式

每条经历都应回答三个问题：

| | 含义 | 示例 |
|---|---|---|
| **F**eature | 做了什么 | "设计了基于 Redis 缓存的用户系统" |
| **A**dvantage | 好在哪 | "响应时间从 800ms 降至 80ms" |
| **B**enefit | 带来什么价值 | "支撑日均 2000 万 PV，服务器从 15 台缩至 4 台" |

只堆砌事实没有说服力。提供论据，把论点留给招聘方自己得出。讲不出成绩时讲成长：遇到了什么问题 → 怎么解决的 → 方案好在哪 → 最终效果。

### 量化

| 差 | 好 |
|---|---|
| "性能大幅提升" | "P99 从 1200ms 降至 200ms" |
| "用户量很大" | "日活 350 万，峰值 QPS 8w" |
| "管理了一个团队" | "6 人小组，从 0 到 1 搭建 XX 平台" |

---

## 简历结构（逆序排列，最新在前）

```
联系方式（手机 / 邮箱 / GitHub / 博客）
个人信息（姓名、学历、工作年限、期望职位）
工作经历（按公司分组 → 公司内按项目分组）
技能清单
开源项目 / 技术文章 / 演讲（选有说服力的）
```

**每条项目经历模板：**

```
[项目名]
负责：[你在这个项目中具体负责的部分]
亮点：[你的独特贡献，技术选型理由]
成果：[量化指标，性能对比，业务影响]
```

每家公司写 2-3 个核心项目即可。项目多则按类合并，每类选一个典型详写，其余一笔带过。

---

## 各技术栈侧重点

写工作经历时，根据目标岗位突出以下维度。括号中的是 JD 高频关键词，选 5-10 个与自己匹配的融入描述中。

### 后端 / Java

**突出：** 高并发设计、微服务拆分、性能优化（JVM/SQL）、数据库设计（分库分表/读写分离）、DDD 建模

**高频关键词：**
Spring Boot, Spring Cloud, MyBatis, MySQL, Redis, Kafka, RabbitMQ, Elasticsearch, Docker, K8s, Netty, Zookeeper, Nginx, gRPC, RocketMQ, Prometheus, Sentinel, TiDB, ClickHouse, seata, Feign, Hystrix

### 前端 / Web

**突出：** 框架深度（React/Vue 原理）、性能优化（首屏/Lighthouse/SSR）、工程化（Webpack/Vite/CI/CD）、跨端（RN/Flutter/小程序）

**高频关键词：**
React, Vue, Next.js, Nuxt, TypeScript, JavaScript, HTML5, CSS3, Sass/Less, Webpack, Vite, Node.js, WebSocket, GraphQL, Redux, Pinia, Tailwind CSS, Jest, Cypress, PWA, 微信小程序, Flutter, Electron

### 移动端 / iOS

**突出：** 系统知识（RunLoop/GCD/Memory Management）、性能优化（启动/内存/卡顿/包体积）、网络（HTTP/2/弱网/Socket）

**高频关键词：**
Swift, SwiftUI, UIKit, Combine, Core Data, Core Animation, AVFoundation, XCTest, Carthage, CocoaPods, SPM, Instruments, Crashlytics, Firebase, ARKit, MapKit, CloudKit

### 移动端 / Android

**突出：** 系统知识（Binder/Handler/生命周期）、性能（ANR/内存泄漏/启动/包体积）、UI（Compose/自定义 View）、架构（MVVM/组件化）

**高频关键词：**
Kotlin, Jetpack Compose, Room, WorkManager, Coroutines, Flow, Retrofit, OkHttp, Dagger Hilt, MVVM, Gradle, Profiler, LeakCanary, AndroidX, Material Design, ADB, FCM

### C / C++

**突出：** 系统编程（内存管理/多线程/进程通信）、网络（Socket/epoll/gRPC）、算法数据结构、编译调试（GCC/GDB/perf）

**高频关键词：**
C++11/14/17/20, STL, Boost, Qt, OpenGL, Vulkan, FFmpeg, protobuf, gRPC, CMake, GDB, Valgrind, perf, eBPF, epoll, io_uring, pthread, lock-free, SIMD, AVX, ARM, GCC, Clang, LLVM

### Go / Node.js

**突出：** 高并发（goroutine/channel 或 Event Loop/async）、微服务（gRPC/服务发现/熔断）、云原生（K8s/Service Mesh）、可观测性

**高频关键词（Go）：**
Gin, gRPC, Protobuf, etcd, Consul, Kubernetes, Helm, Prometheus, OpenTelemetry, Kafka, Redis, TiDB, pprof, trace

**高频关键词（Node.js）：**
Express, Koa, Fastify, NestJS, Socket.io, TypeScript, Prisma, Jest, Next.js, Serverless, AWS Lambda, PM2

### 架构师 / 技术管理

**突出：** 技术选型与风险评估、系统设计（高可用/高并发/可扩展）、团队管理（Code Review/mentorship/梯队建设）、跨部门协作

**高频关键词：**
DDD, Microservices, Event Sourcing, CQRS, Saga, Service Mesh, Istio, K8s, Terraform, GitOps, ArgoCD, Prometheus, Grafana, ELK, OpenTelemetry, SLO, SLA, CAP, BASE, 分布式事务, 混沌工程, 容灾, 灰度发布, 技术债, 架构治理

---

## 联系方式要点

- **手机：** 外地号注明地区；经常关机写最佳联系时间
- **邮箱：** 建议 Gmail/Outlook（部分 HR 反感 QQ 邮箱）
- **GitHub / 博客：** 有原创 repo 或高质量文章显著提升个人品牌

---

## ATS 策略

简历可能经过机器筛选（ATS）或不懂技术的 HR 快速浏览：

1. 从对应技术栈的高频关键词中选 5-10 个与自己匹配的
2. 关键词要**自然融入**经历描述，不要堆砌在末尾
3. 文件名用 `姓名-职位-工作年限.pdf`（不用 `.doc`，排版易错乱）
