import subprocess
from email.quoprimime import decode
import subprocess
from functools import partial

import requests
from urllib.parse import urlencode

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs


class DouYin:
    def __init__(self, url):
        self.url = url
        self.cookie = ""
        if self.cookie == "":
            print("请先写入cookie")
            exit()

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "Cookie": self.cookie,
        }
        self.video_url = "https://www.douyin.com/aweme/v1/web/aweme/detail/"
        self.cookies = {}
        for item in self.cookie.split('; '):
            if '=' in item:
                key, value = item.split('=', 1)
                self.cookies[key] = value

    def get_a_bogus(self, params, ua):
        # 用js实现的，可以自行改写成别的语言版本
        jscode = execjs.compile(open("./js/dy.js", encoding="utf-8").read())
        ctx = jscode.call("get_a_bogus", params, ua)
        return ctx

    def get_params(self, aweme_id):
        # 将cookie字符串拆分成键值对
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "aweme_id": aweme_id,
            "update_version_code": "170400",
            "pc_client_type": "1",
            "pc_libra_divert": "Windows",
            "version_code": "190500",
            "version_name": "19.5.0",
            "cookie_enabled": "true",
            "screen_width": "2560",
            "screen_height": "1440",
            "browser_language": "zh-CN",
            "browser_platform": "Win32",
            "browser_name": "Chrome",
            "browser_version": "130.0.0.0",
            "browser_online": "true",
            "engine_name": "Blink",
            "engine_version": "130.0.0.0",
            "os_name": "Windows",
            "os_version": "10",
            "cpu_core_num": "12",
            "device_memory": "8",
            "platform": "PC",
            "downlink": "10",
            "effective_type": "4g",
            "round_trip_time": "50",
            "webid": "7432962412016240178",
            # "uifid": "63bdc4b4b456901f349a081bfd3a24da10a1c6623f0a2d5eadd83f51c9f4d112da4a060d6a60033c789dae6e72bd6ae27e8fafa4126646d08d4298a45dab3a8f52beaeb91023ead87c5396f2d2c53c2a",
            "msToken": "arAHq-Wn0mHQslyoOvoEQglvThVW7h_7HtyoAdzzq6Gbu7rpl09XFtHpE9g_HsBt1GmQaKiJALUj0590_xz3G4a7zWj8iAilqfzsnYsLrbyg6WY4my9p16tKmWL8YCjUK8uOL6FkFcRJ82YR1kKwhJ0bxMim-mgLFDaqdjam9o2_06Fip9oa3Q=="
        }
        url_params = urlencode(params)
        a_bogus = self.get_a_bogus(url_params, self.headers["User-Agent"])
        params["a_bogus"] = a_bogus
        params["verifyFp"] = "verify_m31bbntm_ie8aqBf6_Zeo2_4UFn_84QI_VebYb6IKFqjR"
        params["fp"] = "verify_m31bbntm_ie8aqBf6_Zeo2_4UFn_84QI_VebYb6IKFqjR"
        return params

    def start(self):
        aweme_id = self.url.split("/")[-1]
        headers = self.headers.copy()
        headers["Referer"] = f"https://www.douyin.com/video/{aweme_id}"
        headers["Host"] = "www.douyin.com"
        params = self.get_params(aweme_id)
        res = requests.get(url=self.video_url, headers=headers, params=params)
        # 有时候响应还是为空不知道为啥
        print(res.text)


if __name__ == '__main__':
    DouYin("https://www.douyin.com/video/7414051930047106342").start()
