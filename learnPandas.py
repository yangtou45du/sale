import pandas as pd
import  numpy as np
import csv
list=[]
with open("city1.csv") as f:
    csv_reader=csv.reader(f)
    print(csv_reader)
    for row in csv_reader:
        #print(row)
        list.append(row[0].split("=")[1])
    f.close()
print(list)
with open("city.csv","a")as f:
    w=csv.writer(f)

    for i in list:
        w.writerow(i)
    f.close()