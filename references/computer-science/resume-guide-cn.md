# 简历写作指南 — 计算机科学（中文）

## 关键量化指标

| 维度 | 需要量化的内容 |
|------|-------------|
| 规模 | 用户量、数据量（GB/TB）、API QPS、服务节点数 |
| 性能 | 延迟降低（ms）、吞吐量提升（%）、模型加速（x 倍） |
| 团队 | 团队规模、管理实习生人数、跨团队项目数 |
| 影响力 | 收入贡献、成本节省、系统迁移规模、修复的关键 bug 数 |
| 模型 | 参数量、基准测试分数、SOTA 成果、论文发表 |

## 不同岗位的侧重点

### 后端工程师
- 微服务架构、API 设计、数据库优化
- 高可用：SLA 百分比、可用性、容错机制
- 分布式系统：消息队列、缓存、负载均衡
- CI/CD 流水线、部署自动化

### 前端工程师
- 框架精通（React/Vue/Angular）、性能优化
- Lighthouse 评分、包体积缩减、渲染时间改善
- 设计系统实现、组件库
- 跨浏览器/设备兼容性

### AI / 算法工程师
- 模型架构（Transformer、CNN、扩散模型）
- 训练数据规模、SFT/预训练管线、微调方法（LoRA、QLoRA）
- 基准测试提升（准确率、F1、BLEU、ROUGE）
- 生产部署：vLLM、TensorRT、ONNX、模型量化
- Agent 工作流：RAG、工具调用、多 Agent 协同

### 运维 / 平台工程师
- 基础设施规模：节点数、集群管理、GPU 编排
- CI/CD：构建时间、部署频率、回滚流程
- 可观测性：监控栈、告警、故障响应时间
- 成本优化：云支出缩减、资源利用率

### 全栈工程师
- 端到端负责：需求到部署
- 全技术栈广度 + 某一领域深度
- 跨职能协作、产品主导

## ATS 关键词（常用）

Java, Python, C++, Go, TypeScript, JavaScript, React, Vue, Node.js, Spring, Spring Cloud, FastAPI, Django, Flask, Kubernetes, Docker, AWS, GCP, Azure, MySQL, PostgreSQL, Redis, MongoDB, Elasticsearch, Kafka, RabbitMQ, PyTorch, TensorFlow, LLM, Agent, RAG, NLP, 计算机视觉, CI/CD, Git, Agile, REST API, GraphQL, gRPC, 微服务, 系统设计, 数据结构, 算法

## 写作示例 — 修改前 vs 修改后

### 弱
> "负责公司电商平台的后端服务开发。"

### 强
> "开发电商平台微服务，支撑 **日均 10,000+ 订单**。构建鉴权服务，实现集团 **90% 系统**单点登录（SSO）。"

### 弱
> "参与了 AI 模型训练和部署工作。"

### 强
> "使用 LoRA 微调 Qwen3 系列模型（最高 235B 参数），vLLM 部署于 K8s 集群。在 ACL 基准上论文解析准确率提升 **30%**。"

### 弱
> "管理小团队。"

### 强
> "带领 **4 人团队**（含实习生）完成 HyperAI 资讯站开发。制定开发范式（ORM → Pydantic → Service → Controller），API 迭代效率提升 **40%**。"

### 弱
> "搭建了 WebAdmin 后台系统。"

### 强
> "搭建并维护 WebAdmin CMS（wa-0.155+），支持多标签过滤、系列教程管理，管理 **9,000+ 学术论文**数据。"

### 弱
> "负责爬虫开发工作。"

### 强
> "部署 OpenClaw + Firecrawl 爬虫框架，爬取质量显著提升。设计 map-clustering-reduce 架构 SOTA 分析 pipeline，支持 CVPR/ACL 顶会数据自动化分析。"
