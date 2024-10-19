import requests
import execjs
import re
import time
from urllib.parse import quote, unquote
import hashlib


class iqiyi:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36¬"
        }
        self.authkey = self.load_auth_js()
        self.cmd5js = self.load_cmd5x_js()

    def load_auth_js(self):
        return execjs.compile(open("./js/iqiyi.js").read())

    def load_cmd5x_js(self):
        return execjs.compile(open("./js/cmd5x.js").read())

    def get_tvid(self):
        accelerator = "https://mesh.if.iqiyi.com/player/lw/lwplay/accelerator.js"
        headers = self.headers.copy()
        headers["Referer"] = self.url.split("?")[0]
        res = requests.get(accelerator, headers=headers)
        tvid = re.search('"tvid":([A-Za-z0-9]+)', res.text)
        vid = re.search('"vid":"([A-Za-z0-9]+)"', res.text)
        return tvid.group(1), vid.group(1)

    def join_params(self):
        tvid, vid = self.get_tvid()
        _time = int(time.time() * 1000)
        params = {
            "tvid": tvid,
            "bid": "300",
            "vid": vid,
            "src": "01080031010000000000",
            "vt": "0",
            "rs": "1",
            "uid": "",
            "ori": "pcw",
            "ps": "1",
            "k_uid": "1bf80ab6e72de7ab4a42f4db91bd530b",
            "pt": "0",
            "d": "0",
            "s": "",
            "lid": "0",
            "cf": "0",
            "ct": "0",
            "authKey": self.authkey.call("auth", self.authkey.call("auth", "") + f"{_time}{tvid}"),
            "k_tag": "1",
            "dfp": "a05f71a09d3d594d61999d8de6456cae27c93252e9ce61cd4246848a76eafcb3ec",
            "locale": "zh_cn",
            "pck": "38Dklg6YLDVPnQ2URa80m1AvEn7v0bVvq4MgAHwm3m1Vm3ai5115qb9dHm1vNXAv4ytm2qAF17",
            "k_err_retries": "0",
            "up": "",
            "qd_v": "a1",
            "tm": _time,
            "k_ft1": "706436220846084",
            "k_ft4": "1162321298202628",
            "k_ft5": "137573171201",
            "k_ft6": "128",
            "k_ft7": "671612932",
            "fr_300": "120_120_120_120_120_120",
            "fr_500": "120_120_120_120_120_120",
            "fr_600": "120_120_120_120_120_120",
            "fr_800": "120_120_120_120_120_120",
            "fr_1020": "120_120_120_120_120_120",
            "bop": quote(
                '{"version":"10.0","dfp":"a05f71a09d3d594d61999d8de6456cae27c93252e9ce61cd4246848a76eafcb3ec"},"b_ft1":24'),
            "ut": "0"
        }
        temp = "/dash?"
        for k, v in params.items():
            temp += k + "=" + str(v) + "&"
        vf_str = self.authkey.call("addChar", temp[:-1])
        vf = hashlib.md5(vf_str.encode("utf-8")).hexdigest()
        params['vf'] = vf
        params["bop"] = unquote(params["bop"])
        return params

    def start(self):
        params = self.join_params()
        res = requests.get("https://cache.video.iqiyi.com/dash", params=params, headers=self.headers).json()
        print(res["data"]["program"]["video"])


if __name__ == '__main__':
    iqiyi(
        "https://www.iqiyi.com/v_195j9pmsbng.html?ht=0&ischarge=false&tvname=%E4%BA%BA%E6%B0%91%E8%AD%A6%E5%AF%9F%E7%AC%AC1%E9%9B%86&vid=769a149b0b9512b38e3e78f45c6646c2&vtype=0&f_block=selector_bk&s2=wna_tvg_1st&s3=wna_tvg_select&s4=1&vfrm=pcw_dianshiju&vfrmblk=pca_2_hot&vfrmrst=image_4&pb2=bkt%3D%26c1%3D%26e%3D%26fatherid%3D%26position%3D5%26r_area%3D%26r_source%3D%26recext%3D%26sc1%3D%26sqpid%3D%26stype%3D&ab=8883_B%2C8185_A%2C8971_A%2C7332_B%2C8739_B%2C9419_A%2C9379_B%2C9683_A%2C8665_E%2C6237_B%2C8983_B%2C8004_B%2C5257_B%2C9634_C%2C7024_C%2C5592_B%2C9117_A%2C6031_B%2C7581_B%2C9506_C%2C8873_A%2C9517_A%2C9394_B%2C7423_C%2C8542_B%2C8401_A%2C6050_B%2C9167_D%2C6249_C%2C7996_B%2C9469_B%2C8812_B%2C6832_C%2C7074_C%2C7682_C%2C5924_D%2C6151_C%2C5468_B%2C6704_C%2C8808_B%2C5465_B%2C6843_B%2C9365_B%2C8497_B%2C8342_B%2C6578_B%2C6312_B%2C6091_B%2C8690_A%2C8871_C%2C9355_A%2C8760_B%2C9292_B%2C8737_D%2C6629_B%2C5670_B%2C9158_A%2C8742_B%2C6082_B%2C5335_B%2C9484_A%2C6752_C%2C9340_A").start()
