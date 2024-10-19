import hashlib

import requests
from Crypto.Cipher import AES
import re
import json
import base64
import uuid
from Crypto.Util.Padding import unpad
import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs


class xigua:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "referer": self.url,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.77 Safari/537.36",
        }
        self.nonce = self.getNonce()
        self.cookie = {
            'UIFID': uuid.uuid4().hex,
            '__ac_signature': self.getSign(),
            'tt_scid': uuid.uuid4().hex,
            '__ac_nonce': self.nonce,
        }
        self.cookie['ttwid'] = self.get_ttwid()

        self.q = ['normal', 'dash_120fps']

    def getNonce(self):
        res = requests.get(self.url, headers=self.headers, )
        return res.cookies.get("__ac_nonce")

    def getSign(self):
        jscode = execjs.compile(open("./js/xigua.js").read())
        ctx = jscode.call("getSign", self.nonce, self.url)
        return ctx

    def get_ttwid(self):
        payload = json.dumps({
            "region": "cn",
            "aid": 1768,
            "needFid": False,
            "service": "www.ixigua.com",
            "cbUrlProtocol": "https",
            "union": True,
            "fid": "",
            "migrate_priority": 0
        })
        headers = self.headers
        headers['Content-Type'] = 'application/json'
        res = requests.post("https://ttwid.bytedance.com/ttwid/union/register/", headers=headers, data=payload,
                            cookies=self.cookie)
        return res.cookies.get("ttwid")

    def aes_decrypt(self, encrypted_data, key, vid):
        key = key.encode("utf8")[:32]
        iv = bytes.fromhex(hashlib.md5(f"{key.decode("utf8")}_{vid}".encode("utf8")).hexdigest())
        encrypted_data_bytes = base64.b64decode(encrypted_data)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_padded_data = cipher.decrypt(encrypted_data_bytes)
        decrypted_data = unpad(decrypted_padded_data, AES.block_size)
        result = f"{str(base64.b64decode(decrypted_data), encoding="utf-8")}&webid={self.cookie["UIFID"]}&wid={uuid.uuid4().hex}&fid={uuid.uuid4().hex}"
        return result

    def getVideoReouce(self, data):
        jscode = execjs.compile(f"getVideoReouce={data}")
        return jscode.call("getVideoReouce")

    def decrypt_main_url(self, body, ptk, json_key, vid):
        # 可以自行解析需要的格式这边只解析了normal
        if json_key == "normal":
            for i in body['video_list']:
                body['video_list'][i]['main_url'] = self.aes_decrypt(body['video_list'][i]['main_url'], ptk, vid)
                body['video_list'][i]['backup_url_1'] = self.aes_decrypt(body['video_list'][i]['backup_url_1'], ptk,
                                                                         vid)
            print(body['video_list'])

    def start(self):
        html = requests.get(url=self.url, cookies=self.cookie, headers=self.headers)
        html.encoding = "utf8"
        res = re.findall(r"window\.getSSRHydratedData\s*=(.*)</script>", html.text, re.S)[0]
        res = self.getVideoReouce(res)
        video_list = res["anyVideo"]['gidInformation']['packerData']['video']['videoResource']
        for i in video_list:
            if i in self.q:
                self.decrypt_main_url(video_list[i], video_list[i]['ptk'], i, video_list['vid'])


if __name__ == '__main__':
    xigua("https://www.ixigua.com/7405525381257626162?logTag=93d90688ada741c34133").start()
