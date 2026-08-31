import hashlib
import re
import time
import base64
from random import randint
from urllib.parse import unquote

import requests

try:
    from Crypto.Cipher import DES
    from Crypto.Util.Padding import pad
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False


class SmzdmBot:
    SIGN_KEY = "apr1$AwP!wRRT$gJ/q.X24poeBInlUJC"
    SK_KEY = "geZm53XAspb02exN"

    def __init__(self, ANDROID_COOKIE: str, SK=None, **kwargs):
        self.cookies = unquote(ANDROID_COOKIE)
        self.cookies_dict = self._cookies_to_dict()

        if SK:
            self.sk = SK
        else:
            self.sk = self._generate_sk()

        self.session = requests.Session()
        self.session.headers.update(self._headers())

    def _generate_sk(self):
        if not HAS_CRYPTO:
            logger.warning("pycryptodome not installed, cannot generate SK")
            return ""
        try:
            smzdm_id = self.cookies_dict.get("smzdm_id", "")
            device_id = self.cookies_dict.get("pr_device_id", "") or self.cookies_dict.get("device_rid", "")
            if not smzdm_id or not device_id:
                logger.warning("Cannot generate SK: missing smzdm_id or device_id")
                return ""
            des_key = self.SK_KEY.encode()[:8]
            plaintext = (smzdm_id + device_id).encode()
            cipher = DES.new(des_key, DES.MODE_ECB)
            ciphertext = cipher.encrypt(pad(plaintext, 8))
            return base64.b64encode(ciphertext).decode()
        except Exception as e:
            logger.error(f"Failed to generate SK: {e}")
            return ""

    def _timestamp(self):
        sleep = randint(1, 5)
        time.sleep(sleep)
        timestamp = int(time.time())
        return timestamp

    def _cookies_to_dict(self):
        cookies_dict = {k: v for k, v in re.findall("(.*?)=(.*?);", self.cookies)}
        return cookies_dict

    def _get_version(self):
        # 兼容新旧版本APP: 旧版用 device_smzdm_version, 新版(v11.1.80+)用 v
        return self.cookies_dict.get("device_smzdm_version") or self.cookies_dict.get("v", "10.4.26")

    def _user_agent(self):
        try:
            device_smzdm = self.cookies_dict["device_smzdm"]
            device_smzdm_version = self._get_version()
            device_smzdm_version_code = self.cookies_dict["device_smzdm_version_code"]
            device_system_version = self.cookies_dict["device_system_version"]
            device_type = self.cookies_dict["device_type"]
            user_agent = f"smzdm_{device_smzdm}_V{device_smzdm_version} rv:{device_smzdm_version_code} ({device_type};{device_smzdm.capitalize()}{device_system_version};zh)smzdmapp"
        except KeyError:
            user_agent = "smzdm_android_V10.4.26 rv:866 (MI 8;Android10;zh)smzdmapp"
        return user_agent

    def _headers(self):
        headers = {
            "User-Agent": self._user_agent(),
            "Accept-Encoding": "gzip",
            "Content-Type": "application/x-www-form-urlencoded",
            **{
                "Request_Key": f"{randint(10000000, 100000000) * 10000000000 + self._timestamp()}",
                "Cookie": self.cookies,
            },
        }
        return headers

    def _web_headers(self):
        headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Cookie": self.cookies,
            "Referer": "https://m.smzdm.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48",
        }
        return headers

    def _sign_data(self, data):
        sign_str = (
            "&".join(f"{key}={value}" for key, value in sorted(data.items()) if value)
            + f"&key={self.SIGN_KEY}"
        )
        sign = hashlib.md5(sign_str.encode()).hexdigest().upper()
        data.update({"sign": sign})
        return data

    def data(self, extra_data=None):
        data = {
            "weixin": "1",
            "captcha": "",
            "f": self.cookies_dict["device_smzdm"],
            "v": self._get_version(),
            "touchstone_event": "",
            "time": self._timestamp() * 1000,
            "token": self.cookies_dict["sess"],
        }
        if self.sk:
            data.update({"sk": self.sk})
        if extra_data:
            data.update(extra_data)
        return self._sign_data(data)

    def request(self, method, url, params=None, extra_data=None):
        data = self.data(extra_data)
        return self.session.request(method, url, params=params, data=data)


if __name__ == "__main__":
    android_cookie_str = ""
    smzdm_bot = SmzdmBot(android_cookie_str)
    data = smzdm_bot.data()
    print(data)
