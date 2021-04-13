import requests

class migu:
    def __init__(self, url):
        self.url = url
        self.cid = self.url.split("cid=")[-1]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36¬"
        }

    def get_params(self):
        return {
            "contId": self.cid,
        }

    def str_cover_list(self, str):
        return list(str)

    def get_ddCalcu(self, puData_url):
        params_dict = {}
        query_string = puData_url.split("?")[-1]
        for i in query_string.split("&"):
            temp = i.split("=")
            params_dict[temp[0]] = temp[1]
        puData_list = self.str_cover_list(params_dict['puData'])
        p = 0
        result = []
        while (2 * p) < len(puData_list):
            result.append(puData_list[len(puData_list) - p - 1])
            if p < len(puData_list) - p - 1:
                result.append(params_dict['puData'][p])
            if p == 1:
                result.append('e')
            if p == 2:
                result.append(self.str_cover_list(params_dict['timestamp'])[6])
            if p == 3:
                result.append(self.str_cover_list(params_dict['ProgramID'])[2])
            if p == 4:
                result.append(self.str_cover_list(params_dict['Channel_ID'])[
                                  len(self.str_cover_list(params_dict['Channel_ID'])) - 4])
            p += 1
        return ''.join(result)

    def calc_url(self, url):
        ddCalcu = self.get_ddCalcu(url)
        return f"{url}&ddCalcu={ddCalcu}"

    def start(self):
        res = requests.get("https://webapi.miguvideo.com/gateway/playurl/v3/play/playurl", params=self.get_params(),
                           headers=self.headers)
        puData_url = res.json()['body']['urlInfo']['url']
        url = self.calc_url(puData_url)
        print(url)


if __name__ == '__main__':
    migu().start()
