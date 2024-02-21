import requests
import json
import csv
import os

def Draw_csv(filename):
    if filename == '消去.csv':
        with open(filename, 'r', encoding = 'utf_8_sig') as csv_file:
            csv_reader = csv.reader(csv_file)
            i=0
            pro_img = []
            pro_title = []
            pro_price = []
            pro_qty = []
            pro_asin = []
            for row in csv_reader:

                pro_img.append('')
                pro_title.append('')
                pro_price.append('')
                pro_qty.append('')
                pro_asin.append(row[0])
                i+=1

            
        return pro_img, pro_title, pro_price, pro_qty, pro_asin,i
    if filename != '消去.csv': 
        with open(filename, 'r', encoding = 'utf_8_sig') as csv_file:
            csv_reader = csv.reader(csv_file)
            i=0
            pro_img = []
            pro_title = []
            pro_price = []
            pro_qty = []
            pro_asin = []
            for row in csv_reader:
                if (row[3]):
                    pro_img.append(row[3])
                    pro_title.append(row[1])
                    pro_price.append(row[2])
                    pro_qty.append('10')
                    pro_asin.append(row[0])
                    i+=1
                else:
                    continue
            
        return pro_img, pro_title, pro_price, pro_qty, pro_asin,i
# end def

# result = Draw_csv('List.csv')
# print(result)