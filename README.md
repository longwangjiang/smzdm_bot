成功开启
# 什么值得买每日签到脚本

<p>
    <img src="https://img.shields.io/github/actions/workflow/status/Chasing66/smzdm_bot/checkin.yml?label=CheckIn">
    <img src="https://img.shields.io/github/actions/workflow/status/Chasing66/smzdm_bot/build.yml?label=Build">
    <img src="https://img.shields.io/github/license/Chasing66/smzdm_bot">
    <img src="https://img.shields.io/docker/pulls/enwaiax/smzdm_bot">
</p>

## 更新日志

- 2022-12-08, 签到失败，浏览器端签到需要滑动验证码认证
- 2023-01-11, 更改`User-Agent`为`iPhone`后可`bypass`滑块认证
- 2023-01-14, 登录认证失败, 签到失效
- 2023-02-18, 通过安卓端验证登录，感谢 [jzksnsjswkw/smzdm-app](https://github.com/jzksnsjswkw/smzdm-app) 的思路. 旧版代码查看 [old](https://github.com/Chasing66/smzdm_bot/tree/old) 分支
- 2023-02-25, 新增`all_reward` 和`extra_reward`两个接口，本地支持多用户运行
- 2023-02-27, 修复本地 docker-compose 运行问题; 本地 docker-compose 支持多账号运行
- 2023-03-01, 支持青龙面板且支持多账号

## 1. 实现功能

- 每日签到, 额外奖励，随机奖励
- 多种运行方式: GitHub Action, 本地运行，docker， 青龙面板
- 多种通知方式: `pushplus`, `server酱`, `telegram bot`(支持自定义反代`Telegram Bot API`. [搭建教程](https://anerg.com/2022/07/25/reverse-proxy-telegram-bot-api-using-cloudflare-worker.html))
- 支持多账号(需配置`config.toml`)

## 2. 配置

支持两种读取配置的方法，从`环境变量`或者`config.toml`中读取

### 2.1 从环境变量中读取配置

```conf
# Cookie
USER_AGENT = ""
ANDROID_COOKIE = ""
SK = ""
TOKEN = ""

# Notification
PUSH_PLUS_TOKEN = ""
SC_KEY = ""
TG_BOT_TOKEN = ""
TG_USER_ID = ""

# 用于自定义反代的Telegram Bot API(按需设置)
TG_BOT_API = ""

# 用于docker运行的定时设定(可选)，未设定则随机定时执行
SCH_HOUR=
SCH_MINUTE=
```

### 2.2 从`config.toml`中读取

参考模板 [app/config/config_example.toml](https://github.com/Chasing66/smzdm_bot/blob/main/app/config/config_example.toml)

```toml
[user.A]
USER_AGENT = ""
ANDROID_COOKIE = ""
SK = ""
TOKEN = ""

[user.B]
USER_AGENT = ""
ANDROID_COOKIE = ""
SK = ""
TOKEN = ""

[notify]
PUSH_PLUS_TOKEN = ""
SC_KEY = ""
TG_BOT_TOKEN = ""
TG_USER_ID = ""
```

## 3. 使用

### 3.1 青龙面板

```
ql repo https://github.com/Chasing66/smzdm_bot "smzdm_ql.py"
```

默认情况下从环境变量读取配置,仅支持单用户.

如果需要支持多用户，推荐使用`config.toml`, 配置参考 [2.2 从`config.toml`中读取](#22-从configtoml中读取).
配置完成后, 拷贝`config.toml`到青龙容器内的`/ql/data/repo/Chasing66_smzdm_bot/app/config`

```
docker cp config.toml <你的青龙容器名称>:/ql/data/repo/Chasing66_smzdm_bot/app/config
```

### 3.2 本地直接运行

克隆本项目到本地, 按照需求配置，配置参考 [2.2 从`config.toml`中读取](#22-从configtoml中读取)

```bash
python3 -m venv .venv
source .venv/bin/activate
cd app
pip install -r requirements.txt
python main.py
```

### 3.3 本地 docker-compose 运行

配置参考[2.2 从`config.toml`中读取](#22-从configtoml中读取)

修改 [docker-compose.yaml](https://github.com/Chasing66/smzdm_bot/blob/main/docker-compose.yml), 将`app/config/config.toml`mout 到容器内`/smzdm_bot/config/config.toml`

```yaml
version: "3.9"
services:
  smzdm_bot:
    image: enwaiax/smzdm_bot
    container_name: smzdm_bot
    restart: on-failure
    logging:
      driver: "json-file"
      options:
        max-size: "1m"
        max-file: "1"
    volumes:
      - ./app/config/config.toml:/smzdm_bot/config/config.toml
```

### 3.4 Git Action 运行

> GitHub Action 禁止对于 Action 资源的滥用，请尽可能使用其他方式

GitHub Action 仅支持`env`配置方式, **务必自行更改为随机时间**

1. Fork[此仓库项目](https://github.com/Chasing66/smzdm_bot)>, 欢迎`star`~
2. 修改 `.github/workflows/checkin.yml`里的下面部分, 取消`schedule`两行的注释，自行设定时间

```yaml
# UTC时间，对应Beijing时间 9：30
schedule:
  - cron: "30 1 * * *"
```

3. 配置参考 [2.1.1 从环境变量中读取配置](#21-从环境变量中读取配置)

## 4. 其它

### 4.1 手机抓包

> 抓包有一定门槛，请酌情尝试.

抓包工具可使用 HttpCanary，教程参考[HttpCanary 抓包](https://juejin.cn/post/7177682063699968061)

1. 按照上述教程配置好 HttpCanary
2. 开始抓包，并打开什么值得买 APP
3. 过滤域名为`user-api.smzdm.com`的 post 请求
4. 点击右上角分享，复制 cURL，转换 curl 请求为 python 格式，[方法](https://curlconverter.com/)
5. 抓包地址：https://user-api.smzdm.com/checkin   这里面信息都齐全。

## 5. Stargazers over time

[![Stargazers over time](https://starchart.cc/Chasing66/smzdm_bot.svg)](https://starchart.cc/Chasing66/smzdm_bot)
