import json
import random
import time
from loguru import logger
from utils.smzdm_bot import SmzdmBot


class SmzdmDailyTasks:
    def __init__(self, bot: SmzdmBot) -> None:
        self.bot = bot

    def daily_tasks(self) -> str:
        msg = "\n===== 每日任务 =====\n"
        try:
            resp = self.bot.request("POST", "https://user-api.smzdm.com/task/list_v2")
            if resp.status_code != 200 or int(resp.json().get("error_code", -1)) != 0:
                logger.error(f"获取任务列表失败: {resp.text}")
                return msg

            tasks = self._extract_tasks(resp.json())
            logger.info(f"发现 {len(tasks)} 个每日任务")

            for task in tasks:
                result = self._execute_task(task)
                logger.info(f"任务结果: {task.get('task_name', '未知')}: {result[:50] if result else '空'}")
                if result:
                    msg += f"{result}\n"
        except Exception as e:
            logger.error(f"每日任务执行失败: {e}")
        return msg

    def _extract_tasks(self, response: dict) -> list:
        tasks = []
        data = response.get("data", {})
        if not isinstance(data, dict):
            return tasks

        rows = data.get("rows", [])
        for row in rows:
            if not isinstance(row, dict):
                continue
            cell_data = row.get("cell_data", {})
            activity = cell_data.get("activity_task", {})
            for group in activity.get("default_list_v2", []):
                for task in group.get("task_list", []):
                    tasks.append(task)
        return tasks

    def _execute_task(self, task: dict) -> str:
        task_id = task.get("task_id", "")
        task_name = task.get("task_name", "未命名任务")
        task_status = task.get("task_status", 0)
        event_type = task.get("task_event_type", "")
        logger.info(f"任务: {task_name}, 状态: {task_status}, 事件: {event_type}")

        if task_status == 3:
            logger.info(f"领取奖励: {task_name}")
            time.sleep(random.randint(2, 5))
            return self._claim_reward(task_id, task_name)

        if task_status != 2:
            return ""

        if event_type == "interactive.view.article":
            return self._browse_article_task(task, task_id, task_name)
        elif event_type == "interactive.follow.user":
            return self._follow_task(task, task_id, task_name)

        logger.info(f"跳过不支持的任务: {task_name} (事件: {event_type})")
        return ""

    def _browse_article_task(self, task: dict, task_id: str, task_name: str) -> str:
        article_id = str(task.get("article_id", "") or "")
        if article_id == "0":
            article_id = ""
        if not article_id:
            redirect = task.get("task_redirect_url", {})
            article_id = str(redirect.get("link_val", "") or "")
            if article_id == "0":
                article_id = ""

        if not article_id:
            return ""

        logger.info(f"浏览文章 {article_id}...")
        time.sleep(random.randint(15, 25))

        try:
            resp = self.bot.request("POST", "https://user-api.smzdm.com/task/event_view_article_sync", extra_data={
                "article_id": article_id,
                "channel_id": "1",
                "task_id": task_id,
            })
            logger.info(f"浏览结果: {resp.status_code} - {resp.text[:100]}")
            time.sleep(random.randint(3, 6))
            return self._claim_reward(task_id, task_name)
        except Exception as e:
            logger.error(f"浏览任务失败: {e}")
            return ""

    def _follow_task(self, task: dict, task_id: str, task_name: str) -> str:
        logger.info(f"执行关注任务: {task_name}")
        time.sleep(random.randint(5, 10))

        try:
            resp = self.bot.request("POST", "https://dingyue-api.smzdm.com/dy/user/dingyue/tuijian_search", extra_data={
                "type": "user",
            })
            if resp.status_code == 200:
                data = resp.json().get("data", {})
                users = [u for u in data.get("rows", []) if u.get("type") == "user"]
                if users:
                    user = random.choice(users)
                    user_id = user.get("keyword_id") or user.get("smzdm_id")
                    if user_id:
                        self.bot.request("POST", "https://dingyue-api.smzdm.com/dingyue/create", extra_data={
                            "type": "user",
                            "keyword": user_id,
                        })
                        time.sleep(random.randint(5, 10))
                        self.bot.request("POST", "https://dingyue-api.smzdm.com/dingyue/destroy", extra_data={
                            "type": "user",
                            "keyword": user_id,
                        })
                        time.sleep(random.randint(2, 4))
                        return self._claim_reward(task_id, task_name)
        except Exception as e:
            logger.error(f"关注任务失败: {e}")
        return ""

    def _claim_reward(self, task_id: str, task_name: str) -> str:
        try:
            token_resp = self.bot.request("POST", "https://user-api.smzdm.com/robot/token")
            if token_resp.status_code != 200:
                return ""

            robot_token = token_resp.json().get("data", {}).get("token", "")
            if not robot_token:
                return ""

            self.bot.request("POST", "https://user-api.smzdm.com/task/activity_task_receive", extra_data={
                "robot_token": robot_token,
                "task_id": task_id,
                "geetest_seccode": "",
                "geetest_validate": "",
                "geetest_challenge": "",
                "captcha": "",
            })
            logger.info(f"奖励已领取: {task_name}")
            return f"✅ {task_name}"
        except Exception as e:
            logger.error(f"领取奖励失败: {e}")
            return ""

    def lucky_house(self) -> str:
        msg = ""
        msg += self.task_lottery()
        msg += self.crowd_lottery()
        return msg

    def task_lottery(self) -> str:
        msg = "\n===== 任务抽奖 =====\n"
        try:
            resp = self.bot.request("POST", "https://user-api.smzdm.com/task/lottery")
            if resp.status_code == 200:
                data = resp.json().get("data", {})
                if isinstance(data, dict):
                    result = data.get("gift_name") or data.get("description") or resp.json().get("error_msg", "抽奖完成")
                    msg += f"抽奖结果: {result}\n"
                else:
                    msg += "没有抽奖机会\n"
            else:
                msg += "抽奖失败\n"
        except Exception as e:
            logger.error(f"任务抽奖失败: {e}")
            msg += "抽奖失败\n"
        return msg

    def crowd_lottery(self) -> str:
        msg = "\n===== 幸运屋 =====\n"
        try:
            resp = self.bot.session.get(
                "https://zhiyou.smzdm.com/user/lottery/jsonp_get_current",
                headers=self.bot._web_headers(),
                params={
                    "callback": f"jQuery{random.randint(10000000, 99999999)}_{int(time.time())}",
                    "active_id": "A6X1veWE2O",
                    "_": int(time.time()),
                }
            )
            result = json.loads(resp.text.split("(", 1)[1].rsplit(")", 1)[0])
            free_count = result.get("remain_free_lottery_count", 0)

            if free_count > 0:
                logger.info(f"幸运屋免费次数: {free_count}")
                for _ in range(free_count):
                    time.sleep(random.randint(2, 5))
                    draw_resp = self.bot.session.get(
                        "https://zhiyou.smzdm.com/user/lottery/jsonp_draw",
                        headers=self.bot._web_headers(),
                        params={
                            "callback": f"jQuery{random.randint(10000000, 99999999)}_{int(time.time())}",
                            "active_id": "A6X1veWE2O",
                            "_": int(time.time()),
                        }
                    )
                    draw_result = json.loads(draw_resp.text.split("(", 1)[1].rsplit(")", 1)[0])
                    msg += f"抽奖结果: {draw_result.get('error_msg', '未知')}\n"
            else:
                msg += "今日无免费抽奖次数\n"
        except Exception as e:
            logger.error(f"幸运屋执行失败: {e}")
            msg += "执行失败\n"
        return msg
