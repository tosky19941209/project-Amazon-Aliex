import requests
import csv
import os
import json
import pandas as pd

#Qoo10 credentials
key = "BhiQeRsAhG1oMl8YdKh1k1hnbudfk599ESiJkN08SS4_g_3_"
user_id = "tourlife"
pwd = "kk1969"

#Definition Functions
#Get certification key
def get_certification_key():
    
    url = "https://api.qoo10.jp/GMKT.INC.Front.QAPIService/ebayjapan.qapi/CertificationAPI.CreateCertificationKey"
    
    params = {
        "key": key,
        "user_id": user_id,
        "pwd": pwd
    }
    
    response = requests.post(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
    else :
        data = None
        
    return data
#end def

#Listing new products
def listing_new_products(certification_key):
    certificationkey = certification_key
    df_arr = []
    if os.path.exists("Regsistered Products.json") and os.path.isfile("Regsistered Products.json"): 
        with open("Registered Products.json", "r", errors = "ignore") as json_file:
            data = json.load(json_file)
            
        with open('登録.csv', 'r', encoding = "utf_8_sig") as file:
            i = 0
            reader = csv.reader(file)
            for row in reader:
                if i == 0:
                    print("i = 0")
                    i += 1
                else:
                    ID = row[0]
                    title = row[1]
                    image = row[2]
                    price = row[3]                
                    qty = '10'
                    categoryNo = row[6]
                    print("categoryNo", categoryNo)
                    if categoryNo == 'None':
                        print("Input CategoryNo!")
                        break
                    if price == "0":
                        print("Price Error!")
                    if price != "0":
                        ItemList = listing_goods(title, price, image, qty, categoryNo, certificationkey)
                        ItemCode_ = ItemList.get("ResultObject")
                        print("ItemCode_: ", ItemCode_)
                        if ItemList.get("ResultObject") == None:
                            print("Register Error!")
                        if ItemList.get("ResultObject") != None:
                            ItemCode = ItemCode_.get("GdNo")
                            print("ItemCode", ItemCode)
                            df_arr.append(
                                {
                                    ID : ItemCode
                                }
                            )
                            
            print("df_arr: ", df_arr)
            df_total = data + df_arr
            with open("Registered Products.json", "wb") as write_file:
                write_file.write(json.dumps(df_total, ensure_ascii=False).encode('utf-8'))   
            print("Created Registered Products Json file!")    
    else:
        with open('登録.csv', 'r', encoding = "utf_8_sig") as file:
            i = 0
            reader = csv.reader(file)
            for row in reader:
                if i == 0:
                    print("i = 0")
                    i += 1
                else:
                    ID = row[0]
                    title = row[1]
                    image = row[2]
                    price = row[3]                
                    qty = '10'
                    categoryNo = row[6]
                    print("categoryNo", categoryNo)
                    if categoryNo == 'None':
                        print("Input CategoryNo!")
                        break
                    if price == "0":
                        print("Price Error!")
                    if price != "0":
                        ItemList = listing_goods(title, price, image, qty, categoryNo, certificationkey)
                        ItemCode_ = ItemList.get("ResultObject")
                        print("ItemCode_: ", ItemCode_)
                        if ItemList.get("ResultObject") == None:
                            print("Register Error!")
                        if ItemList.get("ResultObject") != None:
                            ItemCode = ItemCode_.get("GdNo")
                            print("ItemCode", ItemCode)
                            df_arr.append(
                                {
                                    ID : ItemCode
                                }
                            )
                            
            print("df_arr: ", df_arr)
            with open("Registered Products.json", "wb") as write_file:
                write_file.write(json.dumps(df_arr, ensure_ascii=False).encode('utf-8'))   
            print("Created Registered Products Json file!")  
    return "success" 
#end def

def listing_goods(title_, price_, image_, qty_, categoryNo_, key):
    
    certificationkey  =  key
    title = title_
    price = price_
    image = image_
    qty = qty_
    categoryNo = categoryNo_
  
    
    print("key: ", certificationkey)
    print("price: ", price)
    print("image: ", image)
    print("qty: ", qty)
    print("categoryNo: ", categoryNo)
    print("title: ", title)

    
    url = "https://api.qoo10.jp/GMKT.INC.Front.QAPIService/ebayjapan.qapi"

    params = {
        "key": certificationkey,
        "returnType" : "json",
        "method" : "ItemsBasic.SetNewGoods",
        "SecondSubCat": categoryNo,
        "ItemTitle": title,
        "SellerCode": '',
        "StandardImage": image,
        "RetailPrice" : "0",
        "ItemPrice": price,
        "ItemQty": qty,
        "AvailableDateType" : "0",
        "AvailableDateValue" : "1"
    }
    
    print("params", params)
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.post(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
    else :
        data = None
        
    print("data", data)   
    return data       
# end def

#Update product's price and qty
def updateProductInfo(certification_key):
    
    certificationkey_ = certification_key
    
    with open('更新.csv', 'r', encoding = "utf_8_sig") as file:
        i = 0
        reader = csv.reader(file)
        for row in reader:
            if i == 0:
                print("i = 0")
                i += 1
            else:
                ID = row[0]
                price = row[3]
                qty = '10'
                with open("Registered Products.json", "r", errors = "ignore") as json_file:
                    data = json.load(json_file)
                    for j in range(0, len(data)):
                        if ID in data[j]:
                           ItemCode = data[j][ID]
                           break
                print("ItemCode: ", ItemCode)
                if ItemCode == 'None':
                    print("Input ItemCode!")
                    break
                else:
                    result = updateInfo(ItemCode, price, qty, certificationkey_)
                    print(result.get("ResultMsg")) 
                    if result.get("ResultMsg") != "Success":
                        print("Update Error!")
                    if result.get("ResultMsg") == "Success":
                        print("Update Success!")
                    
    return "Update Succeed!"      
# end def

def updateInfo(ItemCode_, price_, qty_, key):
    
    certificationkey  =  key
    price = price_
    qty = qty_
    ItemCode = ItemCode_
    
    print("key: ", certificationkey)
    print("price: ", price)
    print("qty: ", qty)
    print("ItemCode: ", ItemCode)
    
    url = "https://api.qoo10.jp/GMKT.INC.Front.QAPIService/ebayjapan.qapi"

    params = {
        "key": certificationkey,
        "returnType" : "json",
        "method" : "ItemsOrder.SetGoodsPriceQty",
        "ItemCode": ItemCode,
        "Price": price,
        "Qty": qty,
    }
    
    print("params: ", params)
    
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
    else :
        data = None
    
    print("data: ", data)
    return data
#end def

#DELETE product' info
#Update product's price and qty
def deleteProductInfo(certification_key):
    
    certificationkey_ = certification_key
    
    with open('消去.csv', 'r', encoding = "utf_8_sig") as file:
        i = 0
        reader = csv.reader(file)
        for row in reader:
            if i == 0:
                print("i = 0")
                i += 1
            else:
                ID = row[0]
                with open("Registered Products.json", "r", errors = "ignore") as json_file:
                    data = json.load(json_file)
                    for j in range(0, len(data)):
                        if ID in data[j]:
                           ItemCode = data[j][ID]
                           break
                print("ItemCode: ", ItemCode)
                if ItemCode == 'None':
                    print("Input ItemCode!")
                    break
                else:
                    result_delete = deleteInfo(ItemCode, certificationkey_)
                    print(result_delete.get("ResultMsg"))
                    if result_delete.get("ResultMsg") != 'Success':
                        print("Delete Error!")
                    if result_delete.get("ResultMsg") == 'Success':
                        print("Dlete Successful!")
        return "Delete Succeed!"
    # end def        
    
# end def
def deleteInfo(ItemCode_, key):
    
    ItemCode = ItemCode_
    certificationkey = key
    
    
    print("certificationkey: ", certificationkey)
    print("ItemCode: ", ItemCode)
    
    url = "https://api.qoo10.jp/GMKT.INC.Front.QAPIService/ebayjapan.qapi"

    params = {
        "key": certificationkey,
        "returnType" : "json",
        "method" : "ItemsOrder.SetGoodsPriceQty",
        "ItemCode": ItemCode,
        "Price": '',
        "Qty": '',
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
    else :
        data = None
    
    print("data: ", data)
    return data
#end def

#Call functions
def main_id(status_market, in_userid, in_key, in_pwd):
    global key, user_id, pwd

    key = in_key
    user_id = in_userid
    pwd = in_pwd

    print(f'key : {key}')
    print(f'id : {user_id}')
    print(f'pwd : {pwd}')

    result_certificationkey = get_certification_key()
    if result_certificationkey == "None":
        print("Certification Errors!")
    else:
        certificationkey = get_certification_key().get("ResultObject")
        print(certificationkey)


        if(status_market == '登録.csv'):
            print('the market is 1.csv')
            result_listing = listing_new_products(certificationkey)
            if result_listing == "success":
                print("Register Succeed!")

        if(status_market == '更新.csv'):
            print('the market is 2.csv')
            result_updating = updateProductInfo(certificationkey)
            if result_updating == "Update Succeed!":
                print("Updated Succeed!")

        if(status_market == '消去.csv'):
            print('the market is 3.csv')
            result_remove = deleteProductInfo(certificationkey)
            if result_remove == "Delete Succeed!":
                print("Deleted Succeed!")