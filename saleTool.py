#coding=utf-8
import requests
import json
import csv
import threading
class SaleTool():
    def __init__(self):
        self.password="a123456"
        self.productKey="6b31a18e-db6e-4e63-b823-7e60cda7b11d"
        self.username="lidan"
        self.loginUrl="http://t.zuul.xinchao.mobi/auth/api/open/login"
        self.header={"Content-Type":"application/json"}
        self.url="http://t.sale.api.xinchao.mobi/service/dispatch?node="
    def Login(self):#登录
        data={"username":self.username,"password":self.password,"productKey":self.productKey}
        re=requests.post(self.loginUrl,json=data,headers=self.header)
        re_to_dict=json.loads(re.content)
        return re_to_dict['data']['token']
    def remove_plan(self,token,id):#删除方案
        self.header['token'] = str(token)
        url = self.url + "1001038"
        payload={"id":id}
        re=requests.post(url,json=payload,headers=self.header)
        code=json.loads(re.content)['code']
        #print(json.loads(re.content))
        return code
    def turn_retain(self,token,id):#转保留
        self.header['token'] = str(token)
        url = self.url + "1001080"
        id_change_string=str(id)
        payload = {"id": id_change_string}
        re = requests.post(url, json=payload, headers=self.header)
        code = json.loads(re.content)['code']
        #print(json.loads(re.content))
        return code#成功
    def turn_book(self,token,id):#转预定
        self.header['token'] = str(token)
        url = self.url + "3003010"
        id_change_string = str(id)
        payload = {"planId": id_change_string}
        re = requests.post(url, json=payload, headers=self.header)
        code = json.loads(re.content)['code']
        #print(json.loads(re.content))
        return code#方案转预定成功

    def main_remove_plan(self,cityCompany,beginTime):#执行删除方案操作
        count=0
        token=self.Login()
        self.header['token']=str(token)
        url=self.url+"1001001"
        playload={"cityCompany":cityCompany,"name":"","beginTime":beginTime,"saleUser":" ","createMan":" ","type":"","photoRequire":" ",
                   "status":" ","check":" ","page":1,"pageSize":20000}

        search=requests.post(url,json=playload,headers=self.header)
        search_to_dict=json.loads(search.content)
        search_data=search_to_dict["data"]["data"]
        search_count=search_to_dict["data"]["count"]
        #print(search_count)
        print("总共方案"+str(search_count)+"条")
        if search_count==0:
            print "目前没有可删除方案"
        else:
            for plan in search_data:
                if plan['status']=="003":#如果方案时销售状态

                    code1=self.turn_retain(token,plan['id'])#转保留
                    code2=self.turn_book(token,plan['id'])#转预定
                    code3=self.remove_plan(token,plan['id'])#删除方案
                    if str(code3)!="000":
                        print(str(plan['id'])+"删除销售方案失败")
                    else:
                        count=count+1

                elif plan['status']=="002":#如果方案是保留状态
                    code1 = self.turn_book(token, plan['id'])  # 转预定
                    code2= self.remove_plan(token, plan['id'])  # 删除方案
                    if str(code2)!="000":
                        print(str(plan['id'])+"删除保留方案失败")
                    else:
                        count = count + 1

                elif plan['status']=="001":#如果方案是预定状态
                    code = self.remove_plan(token, plan['id'])  # 删除方案
                    if str(code)!="000":
                        print(str(plan['id'])+"删除预定方案失败")
                    else:
                        count=count+1

                else:
                    print str(plan['id'])+"删除方案失败"
        return count
    def remove(self,time):
        count=0
        with open("city.csv") as f:
            reader=csv.reader(f)
            for i in reader:

                city=''.join(i)
                print "==============正在删除"+str(city)+"方案=========================="
                count1=self.main_remove_plan(city,time)
                print "==============已删除" + str(city) + "方案========================"
                count=count1+count
        print("已删除方案"+str(count)+"个")
    def get_city_premises_id(self):
        """

        :param id: 某城市的方案id
        :return: 返回某城市下所有楼盘id,以字符串的形式返回
        """
        premisesIdList=[]
        token = self.Login()
        self.header['token'] = str(token)
        url = self.url + "1001015"
        payload={"id":"104759","name":""}
        results = requests.post(url, json=payload, headers=self.header)
        results_to_dict = json.loads(results.content)
        results_data = results_to_dict["data"]
        for i in results_data:
            premisesIdList.append(str(i["id"]))
        print len(premisesIdList)
        print ",".join(premisesIdList)
    def compare_file(self,aFile,bFile):
        """

        :param aFile: a文件
        :param bFile: b文件
        :return:
        """
        f1=open(aFile)
        f2=open(bFile)
        count=1
        msg=[]
        for line1 in f1:
            line2=f2.readline()
            if(line1!=line2):
                msg.append(line1+line2)
            count+=1
        f1.close()
        f2.close()
        print (msg)
    def get_preject_id(self,id):
        """
        获取1001015接口楼盘id，并保存到csv中
        :param id:
        :return:
        """
        self.header['token'] = self.Login()
        url = self.url + "1001015"
        id_change_string = str(id)
        payload = {"id":id,"name":""}
        re = requests.post(url, json=payload, headers=self.header)
        data = json.loads(re.content)['data']
        #print(data)
        with open("projectId.csv","wb") as f:
            writer=csv.writer(f)
            for i in data:
                list=[]
                #print type(i["id"])
                list.append(i["id"])
                writer.writerow(list)
    def code_formate(self):
        """
        处理codeAndCity.csv数据格式
        :return:
        """
        list=[]
        with open("codeAndCity.csv","r") as f:
            reader=csv.reader(f)
            for row in reader:
                list.append(row)
        dict={}
        print(dict.keys())
        for i in range(len(list)):
            if list[i][1] in dict.keys():
                dict[list[i][1]]=dict[list[i][1]]+","+list[i][0]
            else:
                dict[list[i][1]] = list[i][0]
        print(dict)
        list_all=[]
        for i in dict:
            list1=[]
            list1.append(i)
            list1.append(dict[i])
            list_all.append(list1)
        print(list_all)
        with open("code_and_city.csv","wb")as f:
            for i in list_all:
                writer=csv.writer(f)
                writer.writerow(i)
    def project_formate(self):
        """
                处理projectAndCity.csv数据格式
                :return:
                """
        list = []
        with open("projectAndCity.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                list.append(row)
        dict = {}
        print(list)
        for i in range(len(list)):

            if list[i][1] in dict.keys():
                dict1="{ 'deviceNum': 110,'premiseId': '"+str(list[i][0])+"'}"
                dict[list[i][1]].append(dict1)
            else:
                list1=[]
                dict1 = "{ 'deviceNum': 110,'premiseId': '" + str(list[i][0]) + "'}"
                list1.append(dict1)
                dict[list[i][1]] = list1
        print(dict)
        list_all = []
        for i in dict:
            list1 = []
            list1.append(i)
            list1.append(dict[i])
            list_all.append(list1)
        print(list_all)
        with open("project_and_city.csv", "wb")as f:
            for i in list_all:
                writer = csv.writer(f)
                writer.writerow(i)




if __name__=="__main__":
    f = SaleTool()
    #print(f.Login())
    #a=f.main_remove_plan("510100-a0001","2019-02-02")#删除单个城市
    #print(a)
    #f.remove("2019-02-02")#删除所有城市
    #f.compare_file("a.txt","b.txt")
    #f.get_preject_id("107178")
    f.project_formate()
