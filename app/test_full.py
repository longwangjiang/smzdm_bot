import os
import sys

os.environ['ANDROID_COOKIE'] = 'partner_name=xiaomi;sess=BB-0qAP%2FUcQQOnnFmsTWTzuP%2BZ2F9hHdrVanaWsgL%2BLeuZAAfNGslY%2FoxEZba0z78Om6V5q325iSOwnQqCXkKxahttae5k%3D;pid=9JggoXVEbcX9B%2BvRDvVl5EfR1skpzChaGbyeoXYHpzZzbfQDpoHn1A%3D%3D;device_type=RedmiM2007J3SC;basic_v=0;client_id=48832a1b7ebb2c592ff546ac3546e95c.1783307873305;pr_new_device_id=c3f522adhbihbbec4i53z6czc61462gz;network=1;device_system_version=12;partner_id=20;user_type=1;device_smzdm=android;apk_partner_name=xiaomi;smzdm_id=2429184121;pr_device_s=c3f522adhbihbbec4i53z6czc61462gz;device_push=1;f=android;pr_z_dr=c3f522adhbihbbec4i53z6czc61462gz;apk_partner_id=20;session_id=48832a1b7ebb2c592ff546ac3546e95c.1788190794243;device_rid=48832a1b7ebb2c592ff546ac3546e95c;active_time=1783307876;z_ai=b6c6083367f7e6e814cb2700192f5dd4;v=11.1.80;pr_device_id=c3f522adhbihbbec4i53z6czc61462gz;last_article_info=%7B%22article_id%22%3A%22181436132%22%2C%22article_channel_id%22%3A%221%22%7D;device_recfeed_setting=%7B%22haojia_recfeed_switch%22%3A%221%22%2C%22homepage_sort_switch%22%3A%221%22%2C%22other_recfeed_switch%22%3A%221%22%2C%22shequ_recfeed_switch%22%3A%221%22%7D;device_smzdm_version_code=1180'
os.environ['SK'] = ''

from utils.smzdm_bot import SmzdmBot
from utils.smzdm_tasks import SmzdmTasks
from utils.smzdm_daily_tasks import SmzdmDailyTasks

bot = SmzdmBot(ANDROID_COOKIE=os.environ['ANDROID_COOKIE'], SK=os.environ['SK'])
tasks = SmzdmTasks(bot)
daily = SmzdmDailyTasks(bot)

msg = ""
print("===== 签到 =====")
msg += tasks.checkin()
print("===== VIP =====")
msg += tasks.vip_info()
print("===== 奖励 =====")
msg += tasks.all_reward()
print("===== 每日任务 =====")
msg += daily.daily_tasks()
print("===== 抽奖 =====")
msg += daily.lucky_house()

print("\n===== 完整结果 =====")
print(msg)
