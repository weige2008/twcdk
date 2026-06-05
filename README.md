# Twitch CDK 挂宝机（GitHub Actions）

## 使用方法

1. **Fork 本仓库** 到你的 GitHub 账号
2. **修改前端 IP**：编辑 `cdk_linux/config.txt`，把 `FRONT_IP` 改成你的服务器IP
3. 其他配置无需修改

## 配置说明

所有参数在 `cdk_linux/config.txt` 中修改：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `FRONT_IP` | 前端服务器IP（**必须修改**） | `8.138.198.37` |
| `API_TOKEN` | API认证密钥 | `twitch-cdk-api-token-2024` |
| `CDK_THREADS` | 并发线程数 | `1` |
| `STREAM_URL` | 要挂的直播链接 | 空（不监控固定流） |
| `DEBUG` | 调试模式 | `false` |

## 运行

- **自动运行**：每6小时一次
- **手动运行**：Actions → Twitch CDK Mining → Run workflow
