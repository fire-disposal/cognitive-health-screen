
# IoMT Digital Twin Platform

基于 [vue-fastapi-admin](https://github.com/mizhexiaoxiao/vue-fastapi-admin.git) \
二次开发，新增 MQTT 支持、WebSocket、健康数据管理业务、数据库及数据初始化重构、多源健康数据解析验证模型、前端业务页面等功能。

> **说明**：本项目聚焦后端与管理后台开发，用户端页面请另行新建项目维护。

---

## 项目概述

- **后端**：FastAPI + Tortoise ORM  
- **前端**：Vue 3 + Vite + Naive UI  
- **数据库**：PostgreSQL  
- **依赖管理**：UV (Python)、NPM (Node.js)  

---

## 项目结构

```

app/               # 后端应用
web/               # 前端项目
scripts/           # 数据库及辅助脚本
deploy/            # 部署相关文件
.env.example       # 环境变量示例
pyproject.toml     # Python 项目配置
run.py             # 后端启动入口

```

---

## 分支说明

- **master**：生产环境  
- **dev**：日常开发  
- 建议基于 `dev` 新建功能分支，完成后通过 Pull Request 合并  

---

## License

本项目基于 MIT 协议开源，需保留原始版权及许可声明。  


