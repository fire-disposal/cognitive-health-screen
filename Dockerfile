# ===============================
# 第一步：构建前端
# ===============================
FROM node:22.16.0 AS web

WORKDIR /opt/vue-fastapi-admin
COPY web ./web

RUN npm install -g pnpm && cd web && pnpm install && pnpm run build

# ===============================
# 第二步：构建后端（基于官方 uv 镜像）
# ===============================
FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /opt/vue-fastapi-admin

# 安装系统依赖（apk 包管理器适用于 alpine）
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk update && apk add --no-cache \
    gcc python3-dev bash nginx vim curl procps net-tools tzdata


# 设置时区
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone

# 拷贝依赖文件，使用 uv sync 安装依赖
COPY pyproject.toml uv.lock ./

RUN uv sync

# 拷贝项目源码
COPY . .

# 拷贝前端构建产物
COPY --from=web /opt/vue-fastapi-admin/web/dist /opt/vue-fastapi-admin/web/dist

#配置 nginx
RUN mkdir -p /etc/nginx/sites-available /etc/nginx/sites-enabled /etc/nginx/conf.d
COPY deploy/web.conf /etc/nginx/sites-available/web.conf

# 删除所有默认配置，防止冲突
RUN mkdir -p /etc/nginx/conf.d || true
RUN rm -f /etc/nginx/conf.d/default.conf || true
RUN ln -s /etc/nginx/sites-available/web.conf /etc/nginx/sites-enabled/web.conf
RUN sed -i '/http {/a \\tinclude /etc/nginx/sites-enabled/*;' /etc/nginx/nginx.conf

# 拷贝启动脚本并授权
COPY deploy/entrypoint.sh .
RUN chmod +x entrypoint.sh

ENV LANG=zh_CN.UTF-8
EXPOSE 80

ENTRYPOINT ["sh", "entrypoint.sh"]
