#author:"赵婷"
#date:2021/8/19
import requests,json
from lxml import etree
import re
import time

headers = {
    'Content-Type':"application/json",
    'Cookie':"TYCID=c2ddfb60ffc511ebac83bd4430511b3c; CLOUDID=1cc8f59d-5045-44f9-8f0e-005ebc072953",
    'User-Agent': 'PostmanRuntime/7.28.3',
    'X-AUTH-TOKEN':"eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzM3MTU3MTU5MCIsImlhdCI6MTYyOTI1MDc3OSwiZXhwIjoxNjYwNzg2Nzc5fQ.-1WIyuoyvSJSDgUNIN-VldMM4Qgkd2p7tvSXoMOitOlLy4t2sHxkRmNMCyzLOuY8y1zpEYt4zmPbmOvxR6g6dw"
}
def GetCompanyNameAddress(name):
    url="https://tax.tianyancha.com/search/%s" % name
    response = requests.get(url, headers=headers)
    # response.encoding = response.apparent_encoding
    data = response.content.decode('utf-8', 'ignore')
    html = etree.HTML(data)
    #获取全部item
    xpath_items = '//div[@id="search"]/div[@class="content"]/div[@class="item"]'
    #对每个item解析
    title='./div[@class="right-content"]/a/@title'
    detailUrl = './div[@class="right-content"]/a/@href'
    #税号
    intro='./div[@class="right-content"]/div[@class="intro"]/span/text()'
    items = html.xpath(xpath_items)
    data=[]
    for item in items:
        name=item.xpath(title)[0]
        url = item.xpath(detailUrl)[0]
        name=re.sub('\s|\t|\n', '', name)
        sh=item.xpath(intro)[0]
        address=item.xpath(intro)[1]
        data.append({"name":name,"sh":sh,"address":address,"url":url})
    print(data)
    return data


if __name__ == '__main__':
    GetCompanyNameAddress("正泰中自")
