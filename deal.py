#coding=utf-8
import json

class Premises():
    ROBOT_LIBRARY_SCOPE = 'TEST CASE'
    ROBOT_LIBRARY_VERSION = '0.3'
    def get_premises_info(self,premises,num=5):#提取楼盘相关信息,premises为项目选择里（1001014接口）楼盘列表，num为提取楼盘的数量，默认5
          # 获取aaData数据,列表
        # print(aaData)
        premisesList = []#单元数和设备数都不为0的列表
        premiseIdList=[]#提取id
        for premise in premises:
            if premise['units'] != 0 and premise['machines'] != 0:
                premisesList.append(premise)
        if len(premisesList)<=num:
            for i in premisesList:
                premiseIdList.append(i['id'])
            return (premiseIdList,premisesList)
        else:
            premiseIdList1=premisesList[:num]
            for i in premiseIdList1:
                premiseIdList.append(i['id'])
            return (premiseIdList,premiseIdList1)
    def get_code(self,premiseCode):#获取已添加某一个楼盘的设备数
        premiseMachineList=premiseCode[1]['aaData']#某楼盘设备列表
        premiseMachineCodeList=[]#某楼盘设备编码列表
        for premiseMachine in premiseMachineList:
            premiseMachineCodeList.append(premiseMachine['code'])
        return (premiseMachineCodeList)
    def get_machine_count(self,premiseinfo):#获取已调度楼盘的设备总数和单元总数，用于调度成功后，判断调度数是否正确
        countMachines=0
        countUnits=0
        for premise in premiseinfo[1]:
            countMachines=countMachines+premise['machines']
            countUnits=countUnits+premise['units']
        return (countUnits,countMachines)








if __name__=="__main__":
    premises = {"sEcho": 1, "iTotalRecords": 1324, "iTotalDisplayRecords": 1324,
                "aaData": [{"id": "1185696", "name": "6", "units": 0, "machines": 0},
                           {"id": "1185697", "name": "7", "units": 10, "machines": 10},
                           {"id": "249506", "name": "7克拉", "units": 10, "machines": 16},
                           {"id": "1185698", "name": "8", "units": 1, "machines": 40},
                           {"id": "1185699", "name": "9", "units": 3, "machines": 2}]}
    #premisesList=[{'units': 8, 'id': '249506', 'machines': 16, 'name': '7\xe5\x85\x8b\xe6\x8b\x89'}, {'units': 39, 'id': '1185698', 'machines': 40, 'name': '8'}]
    f=Premises()
    #premisesId=f.get_premises_info(premises)
    #print(premisesId)
    #premiseCode=[{"sEcho":9,"iTotalRecords":0,"iTotalDisplayRecords":0,"aaData":[]},{"sEcho":9,"iTotalRecords":0,"iTotalDisplayRecords":0,"aaData":[{"unit":"东门","code":"BJA-E70-028","elevator":"右2","size":"19寸AB","building":"5号楼"},{"unit":"东门","code":"BJA-E70-027","elevator":"右1","size":"19寸AB","building":"5号楼"},{"unit":"西门","code":"BJA-E70-025","elevator":"右1","size":"19寸AB","building":"5号楼"}]}]
    #premiseMachineCodeList=f.get_code(premiseCode)
    #print premiseMachineCodeList
    premiseinfo=(['1185697', '249506'], [{'units': 10, 'id': '1185697', 'machines': 10, 'name': '7'}, {'units': 10, 'id': '249506', 'machines': 16, 'name': '7\xe5\x85\x8b\xe6\x8b\x89'}, {'units': 1, 'id': '1185698', 'machines': 40, 'name': '8'}])
    b=f.get_machine_count(premiseinfo)
    print(b)