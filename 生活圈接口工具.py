#coding=utf-8
import requests
import json
import csv
import MySQLdb
conn = MySQLdb.connect(host='rm-bp13v3n2k602o06wdco.mysql.rds.aliyuncs.com',user='sale',passwd='vMdO8rG74IVDY3O',db='sale',port=3306)
cur=conn.cursor()
cur.execute('select name from sale_led_plan where planNum="L3868446"')
print(cur.rowcount)
rs=cur.fetchall()
print(cur)