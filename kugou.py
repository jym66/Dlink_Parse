import requests
import time
import uuid
import hashlib


class KuGou:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36¬"
        }
        self.encode_album_audio_id = url.split("#")
        if len(self.encode_album_audio_id) == 1 and self.encode_album_audio_id[0] == url:
            self.encode_album_audio_id = url.split("/")[-1].split(".")[0]
        self.uuid = uuid.uuid4().hex
    def get_md5_params(self, params):
        sign_params = f"NVPh5oo715z5DIWAeQlhMDsWXXQV4hwtappid={params["appid"]}clienttime={params["clienttime"]}clientver={params["clientver"]}dfid={params["dfid"]}encode_album_audio_id={params["encode_album_audio_id"]}mid={params["mid"]}platid={params["platid"]}srcappid={params["srcappid"]}token=userid={params["userid"]}uuid={params["uuid"]}NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"
        return hashlib.md5(sign_params.encode('utf-8')).hexdigest()

    def start(self):
        params = {
            "srcappid": "2919",
            "clientver": "20000",
            "clienttime": int(time.time() * 1000),
            "mid": self.uuid,
            "uuid": self.uuid,
            "dfid": "74a7fd31239b4df8a624e8ef94c45d70",
            "appid": "1014",
            "platid": "4",
            "encode_album_audio_id": self.encode_album_audio_id,
            "token": "",
            "userid": "0",
        }
        params["signature"] = self.get_md5_params(params)
        res = requests.get("https://wwwapi.kugou.com/play/songinfo", params=params, headers=self.headers)
        print(res.json())
        return res.json()


if __name__ == '__main__':
    KuGou("https://www.kugou.com/mixsong/apasko1a.html").start()
