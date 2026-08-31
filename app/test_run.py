import os
import sys
from loguru import logger
from utils.smzdm_bot import SmzdmBot
from utils.smzdm_tasks import SmzdmTasks

logger.add("smzdm.log", retention="10 days")

ANDROID_COOKIE = os.environ.get("ANDROID_COOKIE", "partner_name=xiaomi;sess=BB-0qAP%2FUcQQOnnFmsTWTzuP%2BZ2F9hHdrVanaWsgL%2BLeuZAAfNGslY%2FoxEZba0z78Om6V5q325iSOwnQqCXkKxahttae5k%3D;pid=9JggoXVEbcX9B%2BvRDvVl5EfR1skpzChaGbyeoXYHpzZzbfQDpoHn1A%3D%3D;device_type=RedmiM2007J3SC;basic_v=0;client_id=48832a1b7ebb2c592ff546ac3546e95c.1783307873305;pr_new_device_id=c3f522adhbihbbec4i53z6czc61462gz;network=1;device_system_version=12;partner_id=20;user_type=1;device_smzdm=android;apk_partner_name=xiaomi;smzdm_id=2429184121;pr_device_s=c3f522adhbihbbec4i53z6czc61462gz;device_push=1;f=android;pr_z_dr=c3f522adhbihbbec4i53z6czc61462gz;apk_partner_id=20;session_id=48832a1b7ebb2c592ff546ac3546e95c.1788190794243;device_rid=48832a1b7ebb2c592ff546ac3546e95c;active_time=1783307876;z_ai=b6c6083367f7e6e814cb2700192f5dd4;v=11.1.80;pr_device_id=c3f522adhbihbbec4i53z6czc61462gz;last_article_info=%7B%22article_id%22%3A%22181436132%22%2C%22article_channel_id%22%3A%221%22%7D;device_recfeed_setting=%7B%22haojia_recfeed_switch%22%3A%221%22%2C%22homepage_sort_switch%22%3A%221%22%2C%22other_recfeed_switch%22%3A%221%22%2C%22shequ_recfeed_switch%22%3A%221%22%7D;device_smzdm_version_code=1180")
SK = os.environ.get("SK", "")

print(f"Cookie length: {len(ANDROID_COOKIE)}")
print(f"Cookie first 50 chars: {ANDROID_COOKIE[:50]}")

bot = SmzdmBot(ANDROID_COOKIE=ANDROID_COOKIE, SK=SK)
resp = bot.request('POST', 'https://user-api.smzdm.com/checkin')
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text}")
