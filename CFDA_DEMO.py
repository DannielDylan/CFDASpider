# -*- coding:utf-8 -*-
# @Date   : 2018/4/2 0002
# @Author : Dylan
# @File   : CFDA_DEMO.py
import json
import random

import pymysql

import requests
import re

import time

from urllib.request import ProxyHandler


from postdata import PostData




class CFDA:
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

        self.file = open('company.json', 'a')
        DBKWARGS = {
            "host": 'localhost',
            "user": 'root',
            "password": '123456',
            "db": 'CFDA',
            "charset": 'utf8'

        }
        self.conn = pymysql.connect(**DBKWARGS)
        # self.cursor=self.conn.cursor()
    def save_tomysql(self,sql):
        # self.conn.query(sql)

        cursor=self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        # self.conn.close()
        # self.save_tomysql(sql)
    # def check_data(self):
    #     sql='select * from cfda'
    #     try:
    #         cursor = self.conn.cursor()
    #         cursor.execute(sql)
    #         result=cursor.fetchall()
    #         print(result)
    #         for row in result:
    #             ID=row[1]
    #             # print(ID)
    #         return ID
    #     except Exception as e:
    #         print(e)
    #     finally:
    #         self.conn.close()


        # self.check_data()
    def parse(self):

        resp = requests.post(self.url, data=self.payload, headers=self.headers)
        # print(resp.url)
        assert resp.status_code == 200
        data = resp.text
        r = resp.json()
        return data, r
        # print(resp)
        # print(res)
        # print(temp)

    def getData(self, data, r):
        # data=json.dumps(json_response)
        # data=json_response['list']
        try:
            ID = re.findall(r'"ID":"(.*?)"', data, re.I)
            # 企业名称
            EPS_NAME = re.findall(r'"EPS_NAME":"(.*?)"', data, re.I)
            # 许可证编号
            PRODUCT_SN = re.findall(r'"PRODUCT_SN":"(.*?)"', data, re.I)
            CITY_CODE = re.findall(r'"CITY_CODE":"(.*?)"', data, re.I)
            # 发证机关
            QF_MANAGER_NAME = re.findall(r'"QF_MANAGER_NAME":"(.*?)"', data, re.I)
            # 有效期
            XK_DATE = re.findall(r'"XC_DATE":"(.*?)"', data, re.I)
            # print(ID)
            # 发证日期
            XC_DATE = re.findall(r'"XK_DATE":"(.*?)"', data, re.I)
            # print(ID)
            x = len(r['list'])
            # print(x)
            for i in range(x):
                # content_list= (ID[i] , EPS_NAME[i] , PRODUCT_SN[i] ,CITY_CODE[i] , QF_MANAGER_NAME[i] , XK_DAT[i])
                #
                # postdata = "%s,%s,%s,%s,%s,%s,%s" % (ID[i], EPS_NAME[i], PRODUCT_SN[i], CITY_CODE[i], QF_MANAGER_NAME[i], XK_DATE[i], XC_DATE[i])
                # print(r['ID'])
                ID=ID[i]
                EPS_NAME = EPS_NAME[i]
                PRODUCT_SN = PRODUCT_SN[i]
                CITY_CODE = CITY_CODE[i]
                QF_MANAGER_NAME = QF_MANAGER_NAME[i]
                XK_DATE = XK_DATE[i]
                XC_DATE = XC_DATE[i]
                sql="insert into cfda(NAME_ID,EPS_NAME,PRODUC_SN,CITY_CODE,QF_MANAGER_NAME,XK_DATE,XC_DATE) values('%s','%s','%s','%s','%s','%s','%s')"%(ID,EPS_NAME,PRODUCT_SN,CITY_CODE,QF_MANAGER_NAME,XK_DATE,XC_DATE)
                self.save_tomysql(sql)
                print('存入数据库')
                # postdata = (ID[i] + "," + EPS_NAME[i] + "," + PRODUCT_SN[i] + "," + CITY_CODE[i] + "," +
                #             QF_MANAGER_NAME[i] + "," + XK_DATE[i] + "," + XC_DATE[i])
                # # print(postdata)
                # # time.sleep(2)
                # self.file.write(postdata + '\n\n')
                # json.dump(postdata,self.file)
                return ID
                # for x in range(len(ID)):
                #     id_name=ID[i]
                #     print(id_name)
                # return id_name
        except Exception as e:
            print('出现问题:', e)
        # return postdata
        # return postdata
        # A=ID[i]
        # B=EPS_NAME[i]
        # C=PRODUCT_SN[i]
        # D=CITY_CODE[i]
        # E=QF_MANAGER_NAME[i]
        # F=XK_DATE[i]
        # G=XC_DATE[i]
        # for n in (15):
        #     postdata = {ID[i], EPS_NAME[i], PRODUCT_SN[i], CITY_CODE[i], QF_MANAGER_NAME[i], XK_DAT[i]}
        # print(A,B,C,D,E,F,G)
        # for i in range(len(data['list'])):
        #     ID=data['list'][i]
        #     EPS_NAME=data['list'][i]
        #     PRODUCT_SN=data['list'][i]
        #     CITY_CODE=data['list'][i]
        #     QF_MANAGER_NAME=data['list'][i]
        #     XK_DAT=data['list'][i]
        # for n in range(len(temp['list'])):
        #     self.content = temp['list'][n]['EPS_NAME']
        # return self.content
        # print(res['list'][n]['EPS_NAME'])
        # return ID, EPS_NAME, PRODUCT_SN, CITY_CODE, QF_MANAGER_NAME,XK_DATE,XC_DATE

    # def save_toText(self,postdata):

    # self.file.write(self.content)
    def parse_content_list(self,ID):
        # print(postdata)
        # res=json.loads(postdata)
        # print(res)
        # print(postdata['ID'])
        # self.ID=postdata['ID']
        # ID=self.check_data
        # print(ID)

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
        # proxy_ip = random.choice(self.proxies)
        # print(proxy_ip)
        # assert hasattr(proxies, 'keys'), "proxies must be a mapping"
        # px=ProxyHandler({"http":"http://125.35.6.84:81"})

        # print(ID)
        # detail_url='http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsById'
        # detail_page=px + "/xk/itownet/portal/dzpz.jsp?id="+ID
        # detail_page = "http://125.35.6.84:81/xk/itownet/portal/dzpz.jsp?id=" + ID
        detail_page = "http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsById"
        # r = requests.post(detail_page, headers=self.headers, timeout=5, verify=False)
        Form_Data = {
            'id': ID,
            # 'id': 'e4cab289a13a44f192c592d3cee66316',
        }
        r = requests.post(detail_page, headers=self.headers, data=Form_Data)
        print(r.text)

    def main(self):
        for n in range(1, 20):
            print("第%s抓取中。。。。" % n)
            self.payload = {
                'applyname': '',
                'applysn': '',
                'conditionType': '1',
                'on': 'true',
                'page': n,
                'pageSize': '15',
                'productName': '',
            }
            data, r = self.parse()
            # self.getData(json_response)
            ID = self.getData(data, r)
            self.parse_content_list(ID)

            # time.sleep(2)

        #


if __name__ == '__main__':
    cfda = CFDA()
    cfda.main()
