import csv
from _csv import reader

""""
outfile = []

with open('venv/include/new.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    for row in csv_reader:
      outfile.append(row)


with open('venv/include/new.csv', 'w') as file:
  writer = csv.writer(file, delimiter=',')
  for item2 in outfile:
      print(item2[2])
      if(item2[2]=="0"):
        writer.writerow([item2[0],item2[1],0])
      else:
        writer.writerow([item2[0], item2[1], item2[2]])
"""

tokyoNew = []
with open("venv/include/tokyoNewFinal.csv", 'r') as read_obj:
    csv_reader = reader(read_obj)
    for row in csv_reader:
        tokyoNew.append(row)

predictionTokyo = []
with open("venv/include/predictionTokyoItem.csv", 'r') as read_obj:
    csv_reader = reader(read_obj)
    for row in csv_reader:
        predictionTokyo.append(row)

for i in predictionTokyo:
    for j in tokyoNew:
        if (i[0] == j[0] and i[1] == j[1]):
            print(i,j)
            j[6] = i[3]
            break

with open("venv/include/finalItemTokyo.csv", 'w') as file:
    writer = csv.writer(file, delimiter=',')
    for item2 in tokyoNew:
        writer.writerow(item2)