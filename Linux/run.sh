#!/bin/bash
# GitHub Actions CDK Mining Script
# 参数通过环境变量传入: FRONT_IP, CDK_THREADS

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== CDK Mining (Actions) ==="

# 前端 IP（来自 Actions），默认回退
FRONT_IP="${FRONT_IP:-127.0.0.1}"
export API_URL="http://${FRONT_IP}:5000"
echo "Front: $API_URL"

# CDK 线程数（来自 Actions），默认 1
export CDK_THREADS="${CDK_THREADS:-1}"

echo "Threads: $CDK_THREADS | Debug: ${DEBUG:-false}"

if [ "$DEBUG" = "true" ]; then
    export LOGURU_LEVEL="DEBUG"
fi

# 安装 Python 依赖
pip3 install -r "$SCRIPT_DIR/requirements.txt" --quiet --break-system-packages 2>&1 || \
pip3 install -r "$SCRIPT_DIR/requirements.txt" --quiet 2>&1

mkdir -p "$PARENT_DIR/profiles"

echo "Starting..."
cd "$PARENT_DIR"
python3 -m Linux.fQtPAqMG
echo "Done."
