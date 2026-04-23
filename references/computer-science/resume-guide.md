# Technical Resume Writing Guide

## Core Principles

### FAB Pattern

Each experience bullet should answer three questions:

| | Meaning | Example |
|---|---|---|
| **F**eature | What you did | "Designed a Redis-cached user system" |
| **A**dvantage | Why it's good | "Response time dropped from 800ms to 80ms" |
| **B**enefit | Business value | "Supported 20M daily page views, reduced servers from 15 to 4" |

Listing facts alone isn't convincing. Provide evidence, let the recruiter draw the conclusion. When there's no quantifiable achievement, talk about growth: what problem you faced → how you solved it → why your approach was better → the outcome.

### Quantification

| Weak | Strong |
|---|---|
| "Significantly improved performance" | "P99 latency reduced from 1200ms to 200ms" |
| "Handled large user base" | "3.5M DAU, peak QPS 80K" |
| "Managed a team" | "6-person team, built XX platform from scratch" |

---

## Resume Structure (Reverse Chronological)

```
Contact Info (phone / email / GitHub / blog)
Personal Info (name, education, years of experience, target role)
Work Experience (grouped by company → by project within company)
Technical Skills
Open Source / Technical Articles / Talks (only if notable)
```

**Per-project template:**

```
[Project Name]
Responsibilities: [your specific role in this project]
Highlights: [unique contributions, technical rationale]
Results: [metrics, benchmarks, business impact]
```

Write 2-3 core projects per company. If there are many, merge by category — pick one representative to detail, mention the rest briefly.

---

## Per-Stack Focus Areas

When writing work experience, emphasize dimensions relevant to your target role. Keywords in parentheses are high-frequency ATS terms — pick 5-10 that match your profile and weave them in naturally.

### Backend / Java

**Emphasize:** High-concurrency design, microservice architecture, performance tuning (JVM/SQL), database design (sharding/replication), DDD

**Keywords:**
Spring Boot, Spring Cloud, MyBatis, MySQL, Redis, Kafka, RabbitMQ, Elasticsearch, Docker, K8s, Netty, Zookeeper, Nginx, gRPC, RocketMQ, Prometheus, Sentinel, TiDB, ClickHouse, seata, Feign, Hystrix

### Frontend / Web

**Emphasize:** Framework depth (React/Vue internals), performance (FCP/Lighthouse/SSR), engineering (Webpack/Vite/CI/CD), cross-platform (RN/Flutter/mini-programs)

**Keywords:**
React, Vue, Next.js, Nuxt, TypeScript, JavaScript, HTML5, CSS3, Sass/Less, Webpack, Vite, Node.js, WebSocket, GraphQL, Redux, Pinia, Tailwind CSS, Jest, Cypress, PWA, Flutter, Electron

### Mobile / iOS

**Emphasize:** System knowledge (RunLoop/GCD/Memory Management), performance (launch/memory/jank/binary size), networking (HTTP/2/weak network/Socket)

**Keywords:**
Swift, SwiftUI, UIKit, Combine, Core Data, Core Animation, AVFoundation, XCTest, Carthage, CocoaPods, SPM, Instruments, Crashlytics, Firebase, ARKit, MapKit, CloudKit

### Mobile / Android

**Emphasize:** System knowledge (Binder/Handler/Lifecycle), performance (ANR/memory leaks/launch/binary size), UI (Compose/Custom Views), architecture (MVVM/modularization)

**Keywords:**
Kotlin, Jetpack Compose, Room, WorkManager, Coroutines, Flow, Retrofit, OkHttp, Dagger Hilt, MVVM, Gradle, Profiler, LeakCanary, AndroidX, Material Design, ADB, FCM

### C / C++

**Emphasize:** Systems programming (memory management/multithreading/IPC), networking (Socket/epoll/gRPC), algorithms & data structures, build & debug (GCC/GDB/perf)

**Keywords:**
C++11/14/17/20, STL, Boost, Qt, OpenGL, Vulkan, FFmpeg, protobuf, gRPC, CMake, GDB, Valgrind, perf, eBPF, epoll, io_uring, pthread, lock-free, SIMD, AVX, ARM, GCC, Clang, LLVM

### Go / Node.js

**Emphasize:** High concurrency (goroutines/channels or Event Loop/async), microservices (gRPC/service discovery/circuit breaking), cloud-native (K8s/Service Mesh), observability

**Keywords (Go):**
Gin, gRPC, Protobuf, etcd, Consul, Kubernetes, Helm, Prometheus, OpenTelemetry, Kafka, Redis, TiDB, pprof, trace

**Keywords (Node.js):**
Express, Koa, Fastify, NestJS, Socket.io, TypeScript, Prisma, Jest, Next.js, Serverless, AWS Lambda, PM2

### Architect / Tech Lead

**Emphasize:** Technology selection & risk assessment, system design (HA/high-concurrency/scalability), team management (Code Review/mentorship/succession), cross-team collaboration

**Keywords:**
DDD, Microservices, Event Sourcing, CQRS, Saga, Service Mesh, Istio, K8s, Terraform, GitOps, ArgoCD, Prometheus, Grafana, ELK, OpenTelemetry, SLO, SLA, CAP, BASE, Distributed Transactions, Chaos Engineering, DR, Canary Release, Technical Debt, Architecture Governance

---

## Contact Info Best Practices

- **Phone:** Note area code for non-local numbers; include best contact hours if you often miss calls
- **Email:** Gmail or Outlook preferred (some HR teams filter QQ/163 email)
- **GitHub / Blog:** Original repos or quality technical articles significantly boost personal brand

---

## ATS Strategy

Your resume may pass through automated screening (ATS) or quick review by non-technical HR:

1. Pick 5-10 keywords from your target stack that genuinely match your skills
2. Weave keywords **naturally** into experience bullets — never dump them at the end
3. File name: `Name-Role-YearsExperience.pdf` (never `.doc`, formatting breaks)
