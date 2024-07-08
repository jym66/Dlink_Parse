import requests
from Crypto.Cipher import AES
import re
import json
import base64
import uuid
from Crypto.Util.Padding import unpad
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

    def aes_decrypt(self, encrypted_data, key, iv):
        key = key.encode("utf8")[:32]
        iv = iv.encode("utf8")[:16]
        encrypted_data_bytes = base64.b64decode(encrypted_data)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_padded_data = cipher.decrypt(encrypted_data_bytes)
        decrypted_data = unpad(decrypted_padded_data, AES.block_size)
        result = f"{str(base64.b64decode(decrypted_data), encoding="utf-8")}&webid={self.cookie["UIFID"]}&wid={uuid.uuid4().hex}&fid={uuid.uuid4().hex}"
        return result

    def decrypt_main_url(self, body, ptk, json_key):
        # 可以自行解析需要的格式这边只解析了normal
        if json_key == "normal":
            for i in body['video_list']:
                body['video_list'][i]['main_url'] = self.aes_decrypt(body['video_list'][i]['main_url'], ptk, ptk)
                body['video_list'][i]['backup_url_1'] = self.aes_decrypt(body['video_list'][i]['backup_url_1'], ptk,
                                                                         ptk)
            print(body['video_list'])
        # if json_key == "dash_120fps":
        #     print(body['dynamic_video'])
        #     body['dynamic_video']['main_url'] = self.aes_decrypt(body['dynamic_video']['main_url'], ptk, ptk)
        #     for dynamic_video in body['dynamic_video']['dynamic_video_list']:
        #         dynamic_video['main_url'] = self.aes_decrypt(dynamic_video['main_url'], ptk, ptk)
        #         dynamic_video['backup_url_1'] = self.aes_decrypt(dynamic_video['backup_url_1'], ptk, ptk)
        #     for dynamic_audio_list in body['dynamic_video']['dynamic_audio_list']:
        #         dynamic_audio_list['main_url'] = self.aes_decrypt(dynamic_audio_list['main_url'], ptk, ptk)
        #         dynamic_audio_list['backup_url_1'] = self.aes_decrypt(dynamic_audio_list['backup_url_1'], ptk, ptk)

    def start(self):
        html = requests.get(url=self.url, cookies=self.cookie, headers=self.headers)
        html.encoding = "utf8"
        res = re.findall("window._SSR_HYDRATED_DATA=(.*?)</script>", html.text)[0].replace("undefined", 'null')
        video_list = json.loads(res)["anyVideo"]['gidInformation']['packerData']['video']['videoResource']
        for i in video_list:
            if i in self.q:
                self.decrypt_main_url(video_list[i], video_list[i]['ptk'], i)


if __name__ == '__main__':
    xigua("").start()
