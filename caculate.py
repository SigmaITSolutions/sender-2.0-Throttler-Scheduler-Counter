import csv
import sys
total1 = 0.0
count1 = 0
with open('/Volumes/WorkPlace/Sigma/Sender/sender2.0/performance/nats_600_7.csv', mode ='r') as file:
    spamreader = csv.reader(file, delimiter='|', quotechar=' ')
    for row in spamreader:
        total1 = total1 + float(row[2])
        count1 = count1 + 1


avg1 = total1/count1 

print(f"total:{count1}--avg:{avg1}")
total2 = 0.0
count2 = 0
with open('/Volumes/WorkPlace/Sigma/Sender/sender2.0/performance/nats_600_6.csv', mode ='r') as file:
    spamreader = csv.reader(file, delimiter='|', quotechar=' ')
    for row in spamreader:
        total2 = total2 + float(row[2])
        count2 = count2 + 1
avg2 = total2/count2 
print(f"total:{count2}--avg:{avg2}")


total3 = 0.0
count3 = 0
with open('/Volumes/WorkPlace/Sigma/Sender/sender2.0/performance/nats_600_5.csv', mode ='r') as file:
    spamreader = csv.reader(file, delimiter='|', quotechar=' ')
    for row in spamreader:
        total3 = total3 + float(row[2])
        count3 = count3 + 1
avg3 = total3/count3 
print(f"total:{count3}--avg:{avg3}")

total4 = 0.0
count4 = 0
with open('/Volumes/WorkPlace/Sigma/Sender/sender2.0/performance/nats_600_4.csv', mode ='r') as file:
    spamreader = csv.reader(file, delimiter='|', quotechar=' ')
    for row in spamreader:
        total4 = total4 + float(row[2])
        count4 = count4 + 1
avg4 = total4/count4 
print(f"total:{count4}--avg:{avg4}")

total5 = 0.0
count5 = 0
with open('/Volumes/WorkPlace/Sigma/Sender/sender2.0/performance/nats_600_8.csv', mode ='r') as file:
    spamreader = csv.reader(file, delimiter='|', quotechar=' ')
    for row in spamreader:
        total5 = total5 + float(row[2])
        count5 = count5 + 1


avg5 = total5/count5 

print(f"total:{count5}--avg:{avg5}")
