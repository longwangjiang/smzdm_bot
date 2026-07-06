# 什么值得买每日签到脚本

> 基于 [Chasing66/smzdm_bot](https://github.com/Chasing66/smzdm_bot)，已适配新版 APP (v11.1.80+)

## 1. 实现功能

- `什么值得买`每日签到
- Github Action 定时执行，**务必自行更改为随机时间**
- 本地运行（支持多用户）
- 通过`pushplus`推送运行结果到微信
- 通过`server酱`推送运行结果到微信
- 通过`telegram bot`推送
- 通过`企业微信机器人`推送

## 2. 使用方法

### 2.1 GitHub Actions 运行（推荐）

**务必自行更改为随机时间**

1. Fork [此仓库](https://github.com/longwangjiang/smzdm_bot)
2. 修改 `.github/workflows/checkin.yml` 中的 cron 时间：

```yaml
# UTC时间，对应Beijing时间 9：30
schedule:
  - cron: "30 1 * * *"
```

3. 仓库 Settings → Secrets and variables → Actions，新增以下 Secrets：

| Secret | 必填 | 说明 |
|--------|------|------|
| `ANDROID_COOKIE` | ✅ | 抓包获取的完整 Cookie 字符串 |
| `SK` | ✅ | 抓包请求体中的 sk 值 |

4. （可选）推送通知 Secrets：

| Secret | 说明 |
|--------|------|
| `PUSH_PLUS_TOKEN` | [PushPlus](https://www.pushplus.plus/) |
| `SC_KEY` | [Server酱](https://sct.ftqq.com/) |
| `TG_BOT_TOKEN` + `TG_USER_ID` | Telegram Bot |
| `TG_BOT_API` | 自定义反代 Telegram Bot API |

### 2.2 本地运行（支持多用户）

复制 `app/config/config_example.toml` 为 `app/config/config.toml`，填入配置：

```toml
[user.A]
ANDROID_COOKIE = "你的Cookie字符串"
SK = "你的SK值"

[notify]
PUSH_PLUS_TOKEN = ""
SC_KEY = ""
TG_BOT_TOKEN = ""
TG_USER_ID = ""
TG_BOT_API = ""
WECOM_BOT_WEBHOOK = ""
```

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

cd app
pip install -r requirements.txt
python main.py
```

### 2.3 Docker 运行

本地创建 `.env` 文件：

```env
ANDROID_COOKIE=你的Cookie字符串
SK=你的SK值

# 可选推送
PUSH_PLUS_TOKEN=
SC_KEY=
TG_BOT_TOKEN=
TG_USER_ID=

# 定时设定（可选），不设则随机时间
SCH_HOUR=
SCH_MINUTE=
```

```bash
docker-compose up -d
```

## 3. 手机抓包

> 抓包有一定门槛，请酌情尝试。

抓包工具可使用 HttpCanary，教程参考 [HttpCanary 抓包](https://juejin.cn/post/7177682063699968061)

1. 配置好 HttpCanary，开始抓包，打开什么值得买 APP
2. 过滤域名为 `user-api.smzdm.com` 的 POST 请求
3. 从请求中提取：
   - **ANDROID_COOKIE**: 请求头中 `cookie:` 后面的完整字符串
   - **SK**: 请求体中 `sk=` 的值

## 更新日志

- 2024-07-06, 兼容新版 APP (v11.1.80+)，版本号字段从 `device_smzdm_version` 变为 `v`
- 2024-07-06, GitHub Actions 改为直接运行源码，不再依赖过时的 Docker 镜像
- 2023-02-25, 新增`all_reward` 和`extra_reward`两个接口，本地支持多用户运行
- 2023-02-18, 通过安卓端验证登录
- 2023-01-11, 更改`User-Agent`为`iPhone`后可`bypass`滑块认证
