import requests
import time
import re
import execjs
from urllib.parse import quote


class tencent:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36¬"
        }
        self.int_time = int(time.time())
        self.cookie = ""
        self.cookie_dict = {}
        self.parse_cookie()

    def parse_cookie(self):
        if self.cookie:
            for i in self.cookie.split(";"):
                kv = i.split("=")
                self.cookie_dict[kv[0].strip()] = kv[1]

    def get_vid(self):
        res = requests.get(self.url, headers=self.headers)
        vid = re.findall(f'{self.url.split(".html")[0]}/(.*?).html', res.text)
        return vid[0]

    def get_adparams(self):
        pf = "in"
        ad_type = quote("LD|KB|PVL")
        pf_ex = "pc"
        url = quote(self.url)
        refer = quote("https://v.qq.com/")
        ty = "web"
        plugin = "1.0.0"
        v = "3.5.57"
        coverid = re.search("cover/(.*?).html", self.url).group(1)
        vid = self.get_vid()
        pt = ""
        flowid = "f48222928272c7950a794ffbea32022c_10901"
        vptag = quote("vptag=www_baidu_com|channel")
        pu = "1"
        chid = "0"
        adaptor = "2"
        dtype = "1"
        live = "0"
        resp_type = "json"
        guid = "2634e72faf052aa51f98971b2a68718c"
        req_type = 1
        # from = "0"
        appversion = "1.0.157"
        uid = self.cookie_dict['vqq_vuserid']
        tkn = self.cookie_dict['vqq_vusession']
        lt = "qq"
        platform = "10901"
        opid = self.cookie_dict['vqq_openid']
        atkn = self.cookie_dict['vqq_access_token']
        appid = self.cookie_dict['vqq_appid']
        tpid = "1"
        result = f"pf={pf}&ad_type={ad_type}&pf_ex={pf_ex}&url={url}&refer={refer}&ty={ty}&plugin={plugin}&v={v}&coverid={coverid}&vid={vid}&pt={pt}&flowid={flowid}&vptag={vptag}&pu={pu}&chid={chid}&adaptor={adaptor}&dtype={dtype}&live={live}&resp_type={resp_type}&guid={guid}&req_type={req_type}&from=0&appversion={appversion}&" \
                 f"uid={uid}&tkn={tkn}&lt={lt}&platform={platform}&opid={opid}&atkn={atkn}&appid={appid}&tpid={tpid}"
        return result

    def get_vinfoparams(self):
        spsrt = "1"
        charge = "1"
        defaultfmt = "auto"
        otype = "ojson"
        guid = "2634e72faf052aa51f98971b2a68718c"
        # 随机数 + platform
        flowid = "f48222928272c7950a794ffbea32022c_10901"
        platform = "10901"
        sdtfrom = "v1010"
        defnpayver = "1"
        appVer = "3.5.57"
        host = "v.qq.com"
        ehost = quote(self.url)
        refer = "v.qq.com"
        sphttps = "1"
        tm = self.int_time
        spwm = "4"
        logintoken = quote(str({"main_login": self.cookie_dict['main_login'], "openid": self.cookie_dict['vqq_openid'],
                                "appid": self.cookie_dict['vqq_appid'],
                                "access_token": self.cookie_dict['vqq_access_token'],
                                "vuserid": self.cookie_dict['vqq_vuserid'],
                                "vusession": self.cookie_dict['vqq_vusession']}))
        vid = self.get_vid()
        defn = "fhd"
        fhdswitch = "0"
        show1080p = "1"
        isHLS = "1"
        dtype = "3"
        sphls = "2"
        spgzip = "1"
        dlver = "2"
        drm = "32"
        hdcp = "1"
        spau = "1"
        spaudio = "15"
        defsrc = "1"
        encryptVer = "9.1"
        cKey = self.get_cKey(platform, appVer, vid, guid, tm)
        fp2p = "1"
        spadseg = "3"
        result = f"spsrt={spsrt}&charge={charge}&defaultfmt={defaultfmt}&otype={otype}&guid={guid}&flowid={flowid}&platform={platform}&sdtfrom={sdtfrom}&defnpayver={defnpayver}&appVer={appVer}&host={host}&ehost={ehost}&refer={refer}&sphttps={sphttps}&tm={tm}&spwm={spwm}&logintoken={logintoken}&vid={vid}&defn={defn}&fhdswitch={fhdswitch}&show1080p={show1080p}&isHLS={isHLS}&dtype={dtype}&sphls={sphls}&spgzip={spgzip}&dlver={dlver}&drm={drm}&hdcp={hdcp}&spau={spau}&spaudio={spaudio}&defsrc={defsrc}&encryptVer={encryptVer}&cKey={cKey}&fp2p={fp2p}&spadseg={spadseg}"
        return result

    def get_cKey(self, platform, version, vid, guid, tm):
        file = './js/getck.js'
        ctx = execjs.compile(open(file).read())
        params = ctx.call("getckey", platform, version, vid, '', guid,
                          tm)
        return params

    def get_buid(self):
        return "vinfoad"

    def start(self):
        ad_params = self.get_adparams()
        vinfoparams = self.get_vinfoparams()
        buid = self.get_buid()
        params = {"buid": buid,
                  "adparam": ad_params,
                  "vinfoparam": vinfoparams}
        res = requests.post("https://vd.l.qq.com/proxyhttp", headers=self.headers, json=params)
        print(res.text)
        return res.json()


if __name__ == '__main__':
    tencent().start()
