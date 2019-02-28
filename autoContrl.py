#coding=utf-8
import requests
from deal import *
class Login():
    def __init__(self,username,password,url):
        self.username=username
        self.password=password
        self.url=url
        self.header={"Content-Type":"application/x-www-form-urlencoded"}
    def login(self):
        session=requests.session()
        data={"user":self.username,"password":self.password}
        content=session.post(self.url,data=data,headers=self.header)
        print(content.status_code)
        return session
class AutoContrl():
    def __init__(self,username,password,url):
        self.session = Login(username, password, url).login()
        self.header={"Content-Type":"application/x-www-form-urlencoded"}
    def addPlan(self):
        url="http://p.sale.xinchao.mobi/index/ledplan/addplan.html"
        data={"saleUser": "4401","orderId": "1387","beginTime": "12/08/2018","endTime": "12/14/2018","trade": "H01701","saleType": "002",
              "singlePrice": "","productPrice": "","compactNum": "","regulateNum": "","city[]": "110100","seconds": "001","numbers":"001" ,
              "type": "001","deliveryMode": "002","photoRequire": "001","photoPack": "002","photoReport": "001","photoUp": "002","photoDown": "002",
              "planId": "","continuation": 0,"wholeNetwork": 0,"moreTwo": 0,"remark": "","name": "9089089","pointStatus": 0,"oldData": ""}
        session=self.login()
        context=session.post(url,data=data,headers=self.header)
        print(context.text)
    def get_can_add_premises(self,planId):#获取可添加楼盘数，排除单元数和设备数为0的楼盘
        url="http://p.sale.xinchao.mobi/index/ledplan/getpremises.html"
        params={"premisesType": [], "areas": [], "premisesPrice": [], "premisesName": "", "propertyCompany": "",
                 "premisesFloor": "", "occupancyRate": "", "propertyPrice": "", "intime": "", "medias": [],
                 "planId": planId}



username="shangguanrongjun"
password="1qaz2wsx"
url="http://p.sale.xinchao.mobi/index/common/checkuser.html"
f=AutoContrl(username,password,url)
a=f.addPlan()