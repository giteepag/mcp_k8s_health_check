# 🚀 MCP-Based Kubernetes Cluster Health Platform

A lightweight **MCP-style observability layer** that provides unified, structured insights into Kubernetes cluster health using Prometheus metrics.

This project exposes cluster telemetry (CPU, memory, restarts, pod health) through a **tool-based API layer**, enabling both machine and user-driven queries.

---

## 📌 Problem Statement

Kubernetes clusters generate large volumes of metrics via Prometheus, but:
- Data is fragmented across dashboards and queries
- Engineers must manually write PromQL
- No unified “cluster health API” exists

---

## 💡 Solution

This project introduces an **MCP-inspired tool layer** that:
- Abstracts Prometheus queries into reusable tools
- Provides structured cluster health responses
- Normalizes CPU, memory, and pod metrics
- Enables future integration with CLI / chatbot / automation systems

---

## 🏗️ Architecture

```mermaid
flowchart TD

U[User / CLI / UI] --> API[MCP Server - FastAPI]

API --> R[Tool Router Layer]

R --> T1[Cluster Health Tool]
R --> T2[Pod CPU Tool]
R --> T3[Memory Tool]
R --> T4[Namespace Health Tool]

T1 --> P[Prometheus]
T2 --> P
T3 --> P
T4 --> P

P --> K[Kubernetes Metrics / cAdvisor]

T1 --> O[Response Aggregator]
T2 --> O
T3 --> O
T4 --> O

O --> API
