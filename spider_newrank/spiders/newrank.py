# -*- coding: utf-8 -*-
import scrapy, json, re, sys, hashlib
from urllib.parse import urlencode
from http.cookies import SimpleCookie

class NewrankSpider(scrapy.Spider):
    name = 'newrank'

    def start_requests(self):
        urls = []

        type = "22" # 财富经营类目
        AppKey = "joker" # AppKey
        uri = "/xdnphb/ade/v1/api/account/search"

        # 拼接需要爬取的链接
        for i in range(1, 6):
            p = str(i)
            parameters = "keyword=&orderBy=avg_article_clicks_count_top_line&pageNum="+p+"&pageSize=20&sort=DESC&type="+type+"&wxId="

            # 知识点：需要计算一下 nonce 以及 xyz
            # 任意六位数字字母组合，固定一个值也没有问题

            nonce = "629dedcfa"

            # 生成请求签名规则：uri?AppKey={appKey}&{将所有请求参数按照字母表升序排序然后以key=value形式拼接}&nonce={nonce}，
            # 然后对上述拼接后的字符串计算md5值，计算结果就是方法签名

            init_xyz = uri+"?"+"AppKey="+AppKey+"&"+parameters+"&nonce="+nonce
            xyz = hashlib.md5(str(init_xyz).encode('utf-8')).hexdigest()

            url = "https://a.newrank.cn/xdnphb/ade/v1/api/account/search?keyword=&orderBy=avg_article_clicks_count_top_line&pageNum="+p+"&pageSize=20&sort=DESC&type="+type+"&wxId=&nonce="+nonce+"&xyz="+xyz
            urls.append(url)

        cookies = {
            "token":"C2C1B306B4C7F4A3387ACF09DB36FFFB",
            "UM_distinctid":"167760cc293a17-0df3095120a613-35607400-13c680-167760cc29415e",
            "__root_domain_v":".newrank.cn",
            "_qddaz":"QD.o7dlpb.smzltb.jp8ult80",
            "CNZZDATA1253878005":"488234887-1544995501-https%253A%252F%252Fa.newrank.cn%252F%7C1544995501",
            "token":"C2C1B306B4C7F4A3387ACF09DB36FFFB",
            "Hm_lvt_a19fd7224d30e3c8a6558dcb38c4beed":"1550467769,1550467856,1550467881,1550555321",
            "_qdda":"3-1.3dsf61",
            "_qddab":"3-e1u858.jsbe82h2",
            "Hm_lvt_ee5b2d8cb0e6152b26e761ea02aa099d":"1550555369,1550555430,1550555432,1550559234",
            "_qddamta_2852150610":"3-0",
            "Hm_lpvt_a19fd7224d30e3c8a6558dcb38c4beed":"1550562275",
            "Hm_lpvt_ee5b2d8cb0e6152b26e761ea02aa099d":"1550565980"
        }

        for url in urls:
            request = scrapy.Request(
                url = url,
                callback = self.parse,
                cookies = cookies
            )
            yield request

    def parse(self, response):
        parsedJson = json.loads(response.text)
        try:
            data = parsedJson['value']['data']['list']

            if len(data):
                for i in range(len(data)):
                    item = data[i]
                    newrank_commit_fans_count = 0
                    avg_article_clicks_count_top_line = 0
                    certified_text = ""

                    try:
                        if item['name']:
                            name = item['name']
                    except Exception as e:
                        pass

                    try:
                        if item['account']:
                            account = item['account']
                    except Exception as e:
                        pass

                    try:
                        if item['newrank_commit_fans_count']:
                            newrank_commit_fans_count = item['newrank_commit_fans_count']
                    except Exception as e:
                        pass

                    try:
                        if item['avg_article_clicks_count_top_line']:
                            avg_article_clicks_count_top_line = item['avg_article_clicks_count_top_line']
                    except Exception as e:
                        pass

                    try:
                        if item['certified_text']:
                            certified_text = item['certified_text']
                    except Exception as e:
                        pass

                    scraped_info = {
                        '名称': name,
                        '微信号': account,
                        '参考粉丝数': newrank_commit_fans_count,
                        '阅读数': avg_article_clicks_count_top_line,
                        '是否是原创': item["is_ori_user"],
                        '新榜指数': item["max_nri"],
                        '微信id': item["account_id"],
                        '微信认证': certified_text
                    }
                    yield scraped_info
            else:
                print(parsedJson)
        except Exception as e:
            pass
