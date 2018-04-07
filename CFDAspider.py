# -*- coding:utf-8 -*-
# @Date   : 2018/4/5 0005
# @Author : Dylan
# @File   : CFDAspider.py
# import csv
import json
import random
import re


import pymysql
import requests
import time



class CFDASpider:
    def __init__(self):
        self.url = "http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsList"
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            # 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Language': 'zh-CN',
            'Connection': 'keep-alive',
            # 'Content-Length': '76',
            'Content-Type': 'application/x-www-form-urlencoded;utf-8',
            # 'Host': '125.35.6.84:81',
            'Referer': 'http://125.35.6.84:81/xk/',
            'User-Agent': 'Mozilla/5.0(Windows NT 6.3;WOW64;Trident/7.0;rv:11.0) like Gecko',
            'X-Requested-With': 'XMLHttpRequest',
        }
        DBKWARGS = {
            "host": 'localhost',
            "user": 'root',
            "password": '123456',
            "db": 'cfda',
            "charset": 'utf8'

        }
        self.conn = pymysql.connect(**DBKWARGS)

    def parse_url(self):

        resp = requests.post(self.url, data=self.payload, headers=self.headers)
        assert resp.status_code == 200
        content = resp.text
        res = resp.json()
        return content, res
        # return resp,res

    def getData(self, content, res, ):
        # print(content)
        try:
            if content is not None:

                ID = re.findall(r'"ID":"(.*?)"', content, re.I)
                # 企业名称
                EPS_NAME = re.findall(r'"EPS_NAME":"(.*?)"', content, re.I)
                # 许可证编号
                PRODUCT_SN = re.findall(r'"PRODUCT_SN":"(.*?)"', content, re.I)
                CITY_CODE = re.findall(r'"CITY_CODE":"(.*?)"', content, re.I)
                # 发证机关
                QF_MANAGER_NAME = re.findall(r'"QF_MANAGER_NAME":"(.*?)"', content, re.I)
                # 有效期
                XK_DATE = re.findall(r'"XK_DATE":"(.*?)"', content, re.I)
                # 发证日期
                XC_DATE = re.findall(r'"XC_DATE":"(.*?)"', content, re.I)
                # print(len(res['list']))
                ID_list = ",".join(ID)
                for i in range(len(res['list'])):
                    # print(ID[i], EPS_NAME[i], PRODUCT_SN[i], CITY_CODE[i], QF_MANAGER_NAME[i], XK_DATE[i], XC_DATE[i])

                    try:

                        with self.conn.cursor() as cursor:

                            print("每页的第%s个列已处理" % i, time.asctime())
                            sql = "insert into CFDA(NAME_ID,EPS_NAME,PRODUCT_SN,CITY_CODE,QF_MANAGER_NAME,XK_DATE,XC_DATE) " \
                                  "values('%s','%s','%s','%s','%s','%s','%s')" % (
                                      ID[i], EPS_NAME[i], PRODUCT_SN[i], CITY_CODE[i], QF_MANAGER_NAME[i], XK_DATE[i],
                                      XC_DATE[i])
                            # self.save_tomysql(sql)

                            cursor.execute(sql)
                            self.conn.commit()
                            time.sleep(random.randint(2, 5))
                    finally:
                        self.conn.commit()
                    # TODO 不加返回值时,getData能取到整页15个数据
                    # except Exception as e:
                    #     print(e)





        except Exception as e:
            print('出现问题：%s' % e)
        finally:
            # print(ID_list)
            # print(type(ID_list))
            return ID_list

            # TODO print('出现问题:list index out of range') #尚未得到解决

    def get_Certificate_permit_card(self, ID_list):
        for ID in ID_list.split(','):
            self.header = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Content-Length": "35",
                "Content-Type": "application/x-www-form-urlencoded",
                "DNT": "1",
                "Host": "125.35.6.84:81",
                "Referer": "http://125.35.6.84:81/xk/itownet/portal/dzpz.jsp?id={}".format(ID),
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/59.0",
                "X-Requested-With": "XMLHttpRequest"
            }
            detail_page = "http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsById"

            Form_Data = {
                "id": ID,
            }
            # html_str=requests.post(detail_page,headers=self.headers,data=Form_Data).text
            content_list = requests.post(detail_page, headers=self.headers, data=Form_Data).content.decode()
            # print(content_list)
        # return content_list
        # with open('Certificate_permit_card.csv', 'w', encoding='utf-8',newline='') as csvfile:
        #     spamwriter = csv.DictWriter(csvfile,fieldnames=html,dialect='excel')
        #     spamwriter.writerows('bu')
    #
    # def save_content_list(self, content_list):
    #     print(content_list)
            file_path = '{}.txt'.format('Certificate_permit_card')
            comment_list=[]
            item = {}
            # 企业名称
            item['epsName'] = re.findall(r'"epsName":"(.*?)"', content_list, re.I)
            # 许可证编号
            item['productSn'] = re.findall(r'"productSn":"(.*?)"', content_list, re.I)
            # 许可项目
            item['certStr'] = re.findall(r'"certStr":"(.*?)"', content_list, re.I)
            # 企业住所
            item['EA'] = re.findall(r'"epsAddress":"(.*?)"', content_list, re.I)
            # 生产地址
            item['EPA'] = re.findall(r'"epsProductAddress":"(.*?)"', content_list, re.I)
            # 社会信用代码
            item['BLN'] = re.findall(r'"businessLicenseNumber":"(.*?)"', content_list, re.I)
            # 法定代表人
            item['LP'] = re.findall(r'"legalPerson":"(.*?)"', content_list, re.I)
            # 企业负责人
            item['BP'] = re.findall(r'"businessPerson":"(.*?)"', content_list, re.I)
            # 质量负责人
            item['QP'] = re.findall(r'"qualityPerson":"(.*?)"', content_list, re.I)
            # 发证机关
            item['QFMN'] = re.findall(r'"qfManagerName":"(.*?)"', content_list, re.I)
            # 签发人：
            item['xkName'] = re.findall(r'"xkName":"(.*?)"', content_list, re.I)
            # 日常监督管理机构
            item['RCMD'] = re.findall(r'"rcManagerDepartName":"(.*?)"', content_list, re.I)
            # 日常监督管理人员
            item['RCMU'] = re.findall(r'"rcManagerUser":"(.*?)"', content_list, re.I)
            # 有效期至
            item['XKD'] = re.findall(r'"xkDate":"(.*?)"', content_list, re.I)
            # 发证日期
            item['XKDS'] = re.findall(r'"xkDateStr":"(.*?)"', content_list, re.I)
            comment_list.append(item)
            with open(file_path, 'a')as f:
                for content in comment_list:
                    f.write(json.dumps(content, ensure_ascii=False, indent=2))
                    f.write('\n')
            # for key in html:
            #     print(key)
            #     spamwriter.writerow(key[1])

    # print(type(html))
    # html_str=etree.HTML(html)
    # print(html_str)
    # with open('Certificate_permit_card.csv','w',encoding='utf-8')as csvfile:
    #     spamwriter=csv.writer(csvfile,dialect='excel')
    #     spamwriter.writerrow(['企业名称','许可证编号','许可项目','企业住所','生产地址','社会信用代码','法定代表人','企业负责人','质量负责人','发证机关','签发人','日常监督管理机构','日常监督管理人员','有效期至','发证日期'])

    def main(self):
        for n in range(1, 297):
            print("第%s页抓取中。。。。" % n)
            self.payload = {
                'applyname': '',
                'applysn': '',
                'conditionType': '1',
                'on': 'true',
                'page': n,
                'pageSize': '15',
                'productName': '',
            }
            # 1 发送请求获取响应
            content, res = self.parse_url()
            time.sleep(random.randint(3, 5))
            ID_list = self.getData(content, res)
            # print(ID)
            # for i in range(15):

            # content_list=self.get_Certificate_permit_card(ID_list)
            self.get_Certificate_permit_card(ID_list)
            # self.save_content_list(content_list)

            # resp=self.parse_url()
            # self.getData(resp)


if __name__ == '__main__':
    cfda = CFDASpider()
    cfda.main()
