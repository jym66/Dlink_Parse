from email.quoprimime import decode

import requests
from urllib.parse import urlencode


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
        self.a_bogus_url = "http://47.76.52.210/get_ab"  # 暂时先提供一个获取接口，后续开源
        self.video_url = "https://www.douyin.com/aweme/v1/web/aweme/detail/"
        self.cookies = {}
        for item in self.cookie.split('; '):
            if '=' in item:
                key, value = item.split('=', 1)
                self.cookies[key] = value

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
            "round_trip_time": "100",
            "webid": "7432163470647150130",
            "uifid": self.cookies["UIFID"],
            "msToken": "vH0DvUu1rqyf9x9kB4N3JOJYh7Aj15xpJ2nKT09keEyDduGA_pwbKMkQdynI3e2K-oXyv2FtBU8UvhnHerJIAfPW9Jbzx0TT-Hj5gRg_yEDLcmBx4V_nQBjBoYMcmI4Zlj-s1hoZVISRZtAB9ZjCH1VMHsaKSTT-XW3u7VYnfhEfU_sm6FXReA=="
        }
        url_params = urlencode(params)
        a_bogus = requests.post(self.a_bogus_url, json={"params": url_params, "ua": self.headers["User-Agent"]}).json()
        if a_bogus["error"] == 0:
            params["a_bogus"] = a_bogus["a_bogus"]
        params["verifyFp"] = "verify_m2y8ko6y_A8gkuYBl_bYrD_4HO8_9u2D_CrteLrO2Ucln"
        params["fp"] = "verify_m2y8ko6y_A8gkuYBl_bYrD_4HO8_9u2D_CrteLrO2Ucln"
        return params

    def start(self):

        aweme_id = self.url.split("/")[-1]
        headers = self.headers.copy()
        headers["Referer"] = f"https://www.douyin.com/video/{aweme_id}"
        # headers['uifid'] = self.cookies["UIFID"]
        headers["Host"] = "www.douyin.com"
        params = self.get_params(aweme_id)
        res = requests.get(url=self.video_url, headers=headers, params=params)
        # 如果发现响应为空，可能是因为msToken的问题，但是msToken还不知道如何生成的,可以去浏览器复制一下
        print(res.text)


if __name__ == '__main__':
    DouYin("https://www.douyin.com/video/7431771207013272868").start()
