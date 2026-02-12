# 项目概览：生产级智能体 AI 系统 (Production-Grade Agentic AI System)

本项目是一个模块化的、生产就绪的智能体 AI 系统，基于 FastAPI、LangGraph 和 PostgreSQL 构建。它实现了编排、记忆管理、可观测性和安全性方面的先进模式。

## 核心技术栈
- **框架**: FastAPI (异步 Python 3.13+)
- **智能体编排**: LangGraph (有状态工作流)
- **数据库**: PostgreSQL + `pgvector` (用于向量存储和状态持久化)
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **记忆管理**: `mem0ai` 用于长期用户记忆的提取和检索
- **可观测性**:
    - **Langfuse**: LLM 追踪和监控
    - **Prometheus/Grafana**: 系统指标和仪表盘
    - **cAdvisor**: 容器资源监控
- **搜索工具**: DuckDuckGo Search 集成
- **LLM 供应商**: OpenAI (具备循环回退机制和自动重试)

## 项目结构
代码遵循模块化架构，主要位于 `src/` 目录：
- `src/agent/`: LangGraph 工作流定义、工具和提示词
- `src/config/`: 基于 Pydantic 风格的设置管理
- `src/data/`: 数据库管理器、SQLModel 模型和 Pydantic 模式
- `src/interface/`: API 路由和端点定义 (认证、聊天)
- `src/services/`: 核心业务逻辑和 LLM 供应商管理 (包含回退逻辑)
- `src/system/`: 基础设施关注点，如日志、限流和遥测
- `src/utils/`: 共享辅助工具 (清理、JWT 认证、图形处理等)
- `evals/`: 智能体行为的 LLM-as-a-judge 评估框架

## 构建与运行

### 环境准备
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (依赖管理工具)
- Docker 和 Docker Compose

### 本地开发
1. **安装依赖**:
   ```bash
   make install
   ```
2. **环境配置**:
   将 `.env.example` 复制为 `.env.development` 并填写必要的 API 密钥 (OpenAI, Langfuse 等)。
3. **启动服务器**:
   ```bash
   make dev ENV=development
   ```
   *注意：代码实际位于 `src/` 目录，启动命令已配置为使用 `src.main:app`。*

### Docker 部署
可以使用以下命令启动完整技术栈 (API, DB, Prometheus, Grafana):
```bash
make docker-compose-up ENV=development
```

## 开发规范
- **代码质量**: 使用 `ruff` 进行 Lint 检查和格式化。执行 `make lint` 和 `make format`。
- **环境管理**: 支持 `development`, `staging`, `production` 和 `test` 环境，通过 `.env.{env}` 文件区分。
- **安全性**: 
    - 使用 JWT 进行身份验证。
    - 强制执行输入清理 (Sanitization)。
    - 使用 `SlowAPI` 实现端点级的速率限制。
- **数据库迁移**: 采用 Code-first 方法，在初始化期间使用 SQLModel 的 `create_all` 创建表。

## 核心特性
- **循环 LLM 回退**: 当主要模型 (如 GPT-4o) 失败时，自动切换到候选模型 (如 GPT-4o-mini)。
- **长期记忆**: 利用 `mem0ai` 从对话中提取事实并存储在 `pgvector` 中，实现跨会话记忆。
- **有状态持久化**: LangGraph 将智能体状态持久化到 PostgreSQL，支持中断后的对话恢复。
- **结构化日志**: 使用 `structlog` 生成机器可读的 JSON 日志，便于生产环境分析。
- **评估驱动**: 内置评估框架，通过 `evals/` 目录下的指标对智能体表现进行量化评分。
