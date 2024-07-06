import base64
import requests
import uuid
import time


class MGTV:
    def __init__(self, url):
        self.url = url

    def get_video_id(self):
        return self.url.split("/", 5)[-1].split(".")[0]

    def start(self):
        params = {
            "video_id": self.get_video_id(),
        }
        res = requests.get("https://pcweb.api.mgtv.com/video/streamList", params=params, verify=True).json()
        print(res)
        return res


if __name__ == '__main__':
    MGTV("https://www.mgtv.com/b/648602/21257227.html?fpa=1663&fpos=&lastp=ch_movie").start()
