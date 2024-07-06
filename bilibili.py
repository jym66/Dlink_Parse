import requests
import re


class Bili:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36¬",
            "Host": "www.bilibili.com",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }

    def start(self):
        res = requests.get(self.url, headers=self.headers)
        res.encoding = "utf-8"
        result = re.findall("window.__playinfo__=(.*?)</script>", res.text)
        print(result)
        return result[0]


if __name__ == '__main__':
    Bili("https://www.bilibili.com/video/BV1PJ4m1M7jZ/?spm_id_from=333.1007.tianma.1-1-1.click").start()
