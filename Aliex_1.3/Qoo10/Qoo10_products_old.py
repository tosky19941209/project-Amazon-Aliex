import requests
import csv
import os
import json

#Qoo10 credentials
# key = "BhiQeRsAhG13j4AisoBKMNJWZLneJKF5j0QlC6mtaOI_g_3_"
# user_id = "tk.1112"
# pwd = "Aa202222"
key = ''
user_id = ''
pwd = ''
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
def listing_new_products():
    ItemCode_arr = ["ItemCode"]
    with open('List.csv', 'r', encoding = "utf_8_sig") as file:
        reader = csv.reader(file)
        for row in reader:
            asin = row[0]
            title = row[1]
            price = row[2]
            image = row[3]
            qty = '10'
            categoryNo = row[4]
            ItemList = listing_goods(title, price, image, qty, categoryNo)
            if ItemList == 'None':
                print("Register Error!")
                ItemCode_arr.append("Error")
            else:
                ItemCode = ItemList.ResultObject["GdNo"]
                ItemCode_arr.append(ItemCode)
        print("ItemCode_arr", ItemCode_arr)
            
    with open ("listed_products.json", "w") as json_file:
        json.dump(ItemCode_arr, json_file)
    return "success" 
#end def

def listing_goods(title, price, image, qty, categoryNo):
    
    url = "https://api.qoo10.jp/GMKT.INC.Front.QAPIService/ebayjapan.qapi"

    params = {
        "key": certificationkey,
        "v " : "1.1",
        "returnType" : "json",
        "method" : "ItemsBasic.SetNewGoods",
        "SecondSubCat": categoryNo,
        "ItemTitle": title,
        "StandardImage": image,
        "RetailPrice" : "0",
        "ItemPrice": price,
        "ItemQty": qty,
        "AvailableDateType" : "0",
        "AvailableDateValue" : "1"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
    else :
        data = None
        
    return data       
# end def

#Update product's price and qty
def updateProductInfo():
    with open('Update.csv', 'r', encoding = "utf_8_sig") as file:
        reader = csv.reader(file)
        for row in reader:
            ItemCode = row[4]
            price = row[2]
            qty = '10'
            result = updateInfo(ItemCode, price, qty)
    return "Update Succeed!"      
# end def

def updateInfo(ItemCode, price, qty):
        url = "https://api.qoo10.jp/GMKT.INC.Front.QAPIService/ebayjapan.qapi"

        params = {
            "key": certificationkey,
            "v " : "1.1",
            "returnType" : "json",
            "method" : "ItemsOrder.SetGoodsPriceQty",
            "ItemCode": ItemCode,
            "Price": price,
            "Qty": qty,
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
        else :
            data = None
            
        return data
#end def

#DELETE product' info
#Update product's price and qty
def deleteProductInfo():

    with open('Remove.csv', 'r', encoding = "utf_8_sig") as file:
        reader = csv.reader(file)
        for row in reader:
            ItemCode = row[4]
            price = row[2]
            qty = "0"
            result_delete = deleteInfo(ItemCode, price, qty)
            if result_delete == 'None' :
                print("Delete Error!")
            else:
                print("Dlete Successful!")
        return "Delete Succeed!"
    # end def        
    
# end def
def deleteInfo(ItemCode, price, qty):
    url = "https://api.qoo10.jp/GMKT.INC.Front.QAPIService/ebayjapan.qapi"

    params = {
        "key": certificationkey,
        "v " : "1.1",
        "returnType" : "json",
        "method" : "ItemsOrder.SetGoodsPriceQty",
        "ItemCode": ItemCode,
        "Price": price,
        "Qty": qty,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
    else :
        data = None
        
    return data
#end def

#Call functions

certificationkey = ''
def main_id(status_market, in_key, in_userid, in_pwd):

    global certificationkey, key, user_id, pwd
    key = in_key
    user_id = in_userid
    pwd = in_pwd

    print(f'key:', key)
    print(f'userid:', user_id)
    print(f'pwd:', pwd)

    result_certificationkey = get_certification_key()
    if result_certificationkey != "None":
        print("Certification Errors!")
    else:
        certificationkey = get_certification_key().get("ResultObject")
        print(certificationkey)


        if(status_market == '登録.csv'):
            print('the market is 1.csv')
            result_listing = listing_new_products()
            if result_listing == "success":
                print("Register Succeed!")

        if(status_market == '更新.csv'):
            print('the market is 2.csv')
            result_updating = updateProductInfo()
            if result_updating == "Update Succeed!":
                print("Updated Succeed!")

        if(status_market == '消去.csv'):
            print('the market is 3.csv')
            result_remove = deleteProductInfo()
            if result_remove == "Delete Succeed!":
                print("Deleted Succeed!")