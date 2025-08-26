#!/bin/sh
set -e

# 确保 nginx 配置目录存在
mkdir -p /etc/nginx/conf.d /etc/nginx/http.d /run/nginx

# 再次确保删除所有默认配置，防止冲突
rm -f /etc/nginx/conf.d/default.conf || true
rm -f /etc/nginx/http.d/default.conf || true

# 检查 nginx 配置文件
echo "Checking Nginx configuration files..."
find /etc/nginx -type f -name "*.conf" | xargs ls -la
echo "Checking sites-enabled directory..."
ls -la /etc/nginx/sites-enabled/

# 测试 nginx 配置
echo "Testing Nginx configuration..."
nginx -t

# 启动 nginx，保持前台
echo "Starting Nginx..."
nginx -g "daemon off;" &

# 等待 nginx 完全启动
sleep 2
echo "Nginx status:"
ps aux | grep nginx

# 激活虚拟环境
. /opt/vue-fastapi-admin/.venv/bin/activate

echo "Using python: $(which python)"

# 设置生产环境变量，跳过自动数据初始化
# 数据库初始化相关的环境变量应该由外部传入，例如通过 docker run -e 或 CI/CD 配置
# export SKIP_DATA_INIT=true
# export AUTO_DETECT_INIT=false
# export FORCE_INIT=false

# echo "Production environment configured:"
# echo "  SKIP_DATA_INIT: $SKIP_DATA_INIT"
# echo "  AUTO_DETECT_INIT: $AUTO_DETECT_INIT"
# echo "  FORCE_INIT: $FORCE_INIT"

# 启动后端服务（阻塞）
echo "Starting backend service..."
python run.py
