import json
import re

import prettytable as pt
from loguru import logger
from utils.smzdm_bot import SmzdmBot


class SmzdmTasks:
    def __init__(self, bot: SmzdmBot) -> None:
        self.bot = bot

    def checkin(self):
        url = "https://user-api.smzdm.com/checkin"
        resp = self.bot.request("POST", url)
        if resp.status_code == 200 and int(resp.json()["error_code"]) == 0:
            resp_data = resp.json()["data"]
            checkin_num = resp_data["daily_num"]
            gold = resp_data["cgold"]
            point = resp_data["cpoints"]
            exp = resp_data["cexperience"]
            rank = resp_data["rank"]
            cards = resp_data["cards"]
            tb = pt.PrettyTable()
            tb.field_names = ["签到天数", "金币", "积分", "经验", "等级", "补签卡"]
            tb.add_row([checkin_num, gold, point, exp, rank, cards])
            logger.info(f"\n{tb}")
            msg = f"""\n⭐签到成功{checkin_num}天
            🏅金币: {gold}
            🏅积分: {point}
            🏅经验: {exp}
            🏅等级: {rank}
            🏅补签卡: {cards}"""
            return msg
        else:
            logger.error(f"Failed to sign in, status: {resp.status_code}, response: {resp.text}")
            msg = "Fail to login in"
            return msg

    def vip_info(self):
        msg = ""
        url = "https://user-api.smzdm.com/vip"
        resp = self.bot.request("POST", url)
        if resp.status_code == 200 and int(resp.json()["error_code"]) == 0:
            resp_data = resp.json()["data"]
            rank = resp_data["vip"]["exp_level"]
            exp_current_level = resp_data["vip"]["exp_current_level"]
            exp_level_expire = resp_data["vip"]["exp_level_expire"]
            tb = pt.PrettyTable()
            tb.field_names = ["值会员等级", "值会员经验", "值会员有效期"]
            tb.add_row([rank, exp_current_level, exp_level_expire])
            logger.info(f"\n{tb}")
            msg = f"""
            🏅值会员等级: {rank}
            🏅值会员经验: {exp_current_level}
            🏅值会员有效期: {exp_level_expire}"""
        return msg

    def all_reward(self):
        msg = ""
        url = "https://user-api.smzdm.com/checkin/all_reward"
        resp = self.bot.request("POST", url)
        if resp.status_code == 200 and int(resp.json()["error_code"]) == 0:
            resp_data = resp.json()["data"]
            if resp_data["normal_reward"]["gift"]["title"]:
                msg = f"\n{resp_data['normal_reward']['gift']['title']}: {resp_data['normal_reward']['gift']['content_str']}"
            elif resp_data["normal_reward"]["gift"]["content_str"]:
                msg = f"\n{resp_data['normal_reward']['gift']['content_str']}: {resp_data['normal_reward']['gift']['sub_content']}"
            logger.info(msg)
        else:
            logger.info("No reward today")
        return msg

    def _get_lottery_chance(self, params):
        headers = self.bot._web_headers()
        url = "https://zhiyou.smzdm.com/user/lottery/jsonp_get_current"
        resp = self.bot.session.get(url, headers=headers, params=params)
        try:
            result = json.loads(re.findall("({.*})", resp.text)[0])
            if result["remain_free_lottery_count"] < 1:
                logger.warning("No lottery chance left")
                return False
            else:
                return True
        except Exception:
            logger.warning("No lottery chance left")
            return False

    def _draw_lottery(self, params):
        msg = """
            🏅没有抽奖机会
        """
        headers = self.bot._web_headers()
        url = "https://zhiyou.smzdm.com/user/lottery/jsonp_draw"
        resp = self.bot.session.get(url, headers=headers, params=params)
        try:
            result = json.loads(re.findall("({.*})", resp.text)[0])
            msg = f"""
            🏅{result["error_msg"]}"""
        except Exception:
            logger.warning("Fail to parser lottery result")
        return msg

    def lottery(self):
        msg = """
            🏅没有抽奖机会
        """
        timestamp = self.bot._timestamp()
        params = {
            "callback": "jQuery34100013381784658652585_{timestamp}",
            "active_id": "A6X1veWE2O",
            "_": timestamp,
        }
        if self._get_lottery_chance(params):
            msg = self._draw_lottery(params)
        return msg

    def extra_reward(self):
        continue_checkin_reward_show = False
        userdata_v2 = self._show_view_v2()
        try:
            for item in userdata_v2["data"]["rows"]:
                if item["cell_type"] == "18001":
                    continue_checkin_reward_show = item["cell_data"][
                        "checkin_continue"
                    ]["continue_checkin_reward_show"]
                    break
        except Exception as e:
            logger.error(f"Fail to check extra reward: {e}")
        if not continue_checkin_reward_show:
            return
        url = "https://user-api.smzdm.com/checkin/extra_reward"
        resp = self.bot.request("POST", url)
        logger.info(resp.json()["data"])

    def _show_view_v2(self):
        url = "https://user-api.smzdm.com/checkin/show_view_v2"
        resp = self.bot.request("POST", url)
        if resp.status_code == 200 and int(resp.json()["error_code"]) == 0:
            return resp.json()
