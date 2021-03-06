import csv
from _csv import reader
from collections import defaultdict
"""""
#ratinglerin bulunması

f = csv.reader(open('venv/include/TKY.csv','r'))
writer = csv.writer(open('venv/include/tokyo.csv','w'))
repeated = set()
repeated = defaultdict(int)
for row in f:
    repeated[row[0]+' '+row[3]]+=1

for x in range(len(repeated)):
    values=list(repeated.values())[x]
    keys = list(repeated.keys())[x]
    writer.writerow(keys.split(' ',1)+[values])

#ratinglerin puanlanması
"""
newyork = []
with open('venv/include/newtokyo.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    for row in csv_reader:
         newyork.append(row)

for j in newyork:
    if(0 < int(j[2]) <=5):
      j[2] = 0.5
    elif(5 < int(j[2]) <=15):
        j[2] = 1
    elif(15 < int(j[2]) <=30):
        j[2] = 1.5
    elif(30 < int(j[2]) <=50):
        j[2] = 2
    elif(50 < int(j[2]) <=80):
        j[2] = 2.5
    elif(80 < int(j[2]) <=120):
        j[2] = 3
    elif(120 < int(j[2]) <=170):
      j[2] = 3.5
    elif(170< int(j[2]) <=240):
        j[2] = 4
    elif(240< int(j[2]) <=400):
        j[2] = 4.5
    elif(400<int(j[2])):
        j[2] = 5


with open('venv/include/tokyoNew.csv', 'w') as file:
  writer = csv.writer(file, delimiter=',')
  for item in newyork:
    writer.writerow(item)