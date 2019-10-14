# encoding:utf-8
import re
import requests
import bs4
from bs4 import BeautifulSoup

def getHtmlText(url):
    headers = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"}
    cookies = {}
    cookiestext = '_cc_=UtASsssmfA==; _m_h5_tk=78ddc6b3026b64698b73398dd47ad101_1571042279684; _m_h5_tk_enc:e3eb56fe87925cc576967bf5dc97881a; _tb_token_=73533d8e3d7b3; alitrackid=www.taobao.com; alitrackid=www.taobao.com; cna=3vj8FeVLW0oCAT23dVrCmvyh; cookie2=102b1469929968a238cbc5e74e077731; enc=PAIQ3iAq3ryPKcddaKzghwwMURKDVb6ylJyMmweZUbcJzTV1ozk6dKW/HLCAY4QNvIvWuS/s6vsmbXNsZykWfA==; hng=CN|zh-CN|CNY|156; isg=BPT0IstkFYMeKYES279cNF8mxrSmZSXCLUnXII5VgH8C-ZRDtt3oR6o7efGEGlAP; JSESSIONID=1A17B8ABC4CADE917E6DE5370882680C; l=dBPzdlL7qwhdynfzBOCNiuI-WF7OSIOYYuPRw6hvi_5aG6L_Fg7OkgQYNFp6VsWfTwYB4f7Vpep9-etbi-y06Pt-g3fPaxDc.; lastalitrackid=www.taobao.com; lgc=\u90AA\u738B\u7231\u4E0A\u6697\u708E\u9F99; mt=ci=43_1; t=e8fa04d0ad9bacb7d364de0b8386dd83; tg=0; thw=cn; tracknick=\u90AA\u738B\u7231\u4E0A\u6697\u708E\u9F99; uc1=cookie14=UoTbnKMDmiw8dw==; uc3=id2=UU6jWcDkFqrJlw==&nk2=szhglVj9Vpawr3UcLKo=&lg2=W5iHLLyFOGW7aA==&vt3=F8dByuDlIe/FYO+Hdo4=; uc4=nk4=0@sUflIhQbu2POIuFzvaZrNPaf7wxp+hesGw==&id4=0@U2xuA/MQI/8e2Y+jIFcvCR1MyJqA'
    for line in cookiestext.split(";"):
        name, value = line.strip().split('=',1)
        cookies[name] = value
    try:
        r = requests.get(url, cookies=cookies, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "爬取异常"

def parsePage(ilt, html):
     try:
         # 正则表达式
         plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
         tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
         for i in range(len(plt)):
             price = eval(plt[i].split(':')[1])
             title = eval(tlt[i].split(':')[1])
             ilt.append([price, title])
     except:
         return "failed"


def printGoodsLits(ilt):
    tplt = "{:4}\t{:8}\t{:16}"
    print(tplt.format("序号", "价格", "商品名称"))
    count = 0
    for g in ilt:
        count += 1
        print(tplt.format(count, g[0], g[1]))




if __name__ == '__main__':
    goods = "aoc+CQ27G1"
    depth = 3
    start_url = 'http://s.taobao.com/search?q=' + goods
    info_list = []
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(48*i)
            html = getHtmlText(url)
            parsePage(info_list, html)
        except:
            continue
    printGoodsLits(info_list)