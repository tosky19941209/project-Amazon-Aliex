import requests
import pandas as pd
import json
import csv
import os

#credentials
refresh_token = "Atzr|IwEBIBgdJx-yaUbIifMn5yy2tPy6DLd3EqxQHhORCJDxmnKxaCPlfhjffvqSd0yVsrsy3o2FvzK5mhb56zKKPqk4v87IU84Y8upkTBCtzR0GicIE8Ps8WOi9fVWxXNhkh6VD0vIhVbjTvQiiArl0sxcu1JsryQiM34LeNgeWuHSdeDIC3ODcGtvYvdRF-cAFOxEf_MIDdZc2_wdtFZbz-TsQ0kzJfBycEdNUutLvLNFQIbMKl55VqznIe0ksFEK31TNVdPSPH4s1O9ZfExgpTHdElJFD4ZARph6ET7tNdI-Yl8ZwE_2cUNkBwW9coVtfJQreMrKqXkoKvraFzed53moFCbl_"
client_id = "amzn1.application-oa2-client.ec207927b55d47e89a89e3d62eecc896"
client_secret = "amzn1.oa2-cs.v1.9dde5b257fa384d04ee9cf108b6987d1c4323430dec8a64d847215af0672a8b6"

data = []
product_title_arr = []
products_images = []
products_prices = []
products_currency = []
flag = 1


#FUCNTIONS!
#To get access_token from credentials
def get_access_token():
    
    #create the request URL.
    url = "https://api.amazon.co.jp/auth/o2/token"
    
    #create the request headers.
    headers = {
        "Content-Type" : "application/x-www-form-urlencoded",
    }
    
    #create the request body.
    body = {
        "grant_type" : "refresh_token",
        "refresh_token" : refresh_token,
        "client_id" : client_id,
        "client_secret" : client_secret,
        "scope" : "sellingpatnerapi::migration"
    }
    
    #make the request.
    response = requests.post(url, headers = headers, data = body)
    
    #check the response status code.
    if response.status_code == 200:
        #get access_token from the response
        return response.json()
    else:
        #print an error
        print("Error: " + str(response.status_code))
        return None


#Get products_info with asin
def get_categoryItem(Asin):
    # access_token = 'Atza|IwEBIDHdN8T6Zfj_oHbh0yup4pR9-ws2Jy4AlS0gk8QeELW6jMDeOl3QRw9hlSgoSxQqmkmVrdHKRceW38dOGu9aHgExiaomxmhcckJX8Pt-F4psejlHX7mLq5bGCUYSFfavN9n9jkAxKj_RyoW_uDY5-MLS2pNk17DED42utScSHHfDKygWDbFWUe9z0sMxXRV3QPgnditrM_0xn32-41ZflVHhfktopZwHIpwbSJWTCrcnHLv-BuRDycRyhjcW5dyCGwKVUB8cM0b4X1_zbvfNPjh1cqACEGN7sKnor7qlRfxixF5tJTFwKnXld7d5HSPVoKf1ZRxT5xaQsxoWepRKV12FWJzgbz5qARkwPjrzpNJ0iA'
    asin = Asin
    url = f"https://sellingpartnerapi-fe.amazon.com/catalog/2022-04-01/items/{asin}"

    #create the request headers.
    #headers
    headers = {
            "Content-Type" : "application/json",
            "Accept" : "application/json",
            "x-amz-access-token" : access_token,
        }
    params = {
        "marketplaceIds" : ["A1VC38T7YXB528"],
        "includedData"   : "images,summaries,productTypes,attributes"
    }
    #make the requests.
    response = requests.get(url, headers = headers, params = params)
        
    if response.status_code == 200:
            #get reportID.
        return response.json()
    else:
        #print an error
        print("Error: " + str(response.status_code))
        return None


#Create New_Input_ProductsInfo_csv file
def New_Input_ProductsInfo_csv():
    if(os.path.exists('新しいアシン.csv') and os.path.isfile('新しいアシン.csv')):
        print("新しいアシン file exist!")
        Asin_list = []
        product_title_arr = []
        products_images = []
        products_prices = []
        with open('新しいアシン.csv', 'r', errors='ignore') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                Asin_list.append(row[0])   
        Total_Asin_list = []
        if(os.path.exists('合計アシン.csv') and os.path.isfile('合計アシン.csv')):
            with open('合計アシン.csv', 'r', errors='ignore') as csv_file:
                csv_reader = csv.reader(csv_file)
                index = 0
                for row in csv_reader:
                    if index == 0:
                       index += 1
                       continue
                    Total_Asin_list.append(row[0])
            print("Total_asin", Total_Asin_list)
            info = Total_Asin_list + Asin_list
            infot = pd.DataFrame({'asin' : info})
            infot.to_csv('合計アシン.csv', index=False)
        else:
            info2 = pd.DataFrame({'asin': Asin_list})
            info2.to_csv('合計アシン.csv', index=False)
    
        print("Total_Asin Created!")
        
        if(os.path.exists('合計アシン.csv') and os.path.isfile('合計アシン.csv')):
            os.remove("新しいアシン.csv")
            print("Asin_new file deleted!")
        print("Get Started Input Products Info!:") 
        for inter in range(0, len(Asin_list)):
            asin = Asin_list[inter]
            if (asin):
                CategoryItem = get_categoryItem(asin)
                if(CategoryItem):
                    data.append(CategoryItem)
                #Save title
                if(CategoryItem):
                    CategoryItem_attributes = CategoryItem.get("attributes")
                    product_title = CategoryItem_attributes['item_name'][0]['value']
                    product_title_arr.append(product_title)
                    print("CategoryItem_producttitle:", product_title_arr)
                else:
                    product_title = "0"
                    product_title_arr.append(product_title)
                    print("CategoryItem_producttitle", product_title_arr)
                #Save image_urls
                if (CategoryItem):
                    CategoryItem_image = CategoryItem.get("images")
                    image_url = CategoryItem_image[0]['images'][0]['link']
                    products_images.append(image_url)   
                    print("CategoryItem_products_images:", products_images)
                else:
                    image_url = "0"
                    products_images.append(image_url)  
                    print("CategoryItem_products_images", products_images) 
                # #Save price
                if (CategoryItem):
                    CategoryItem_attributes = CategoryItem.get("attributes")
                    if('list_price' in CategoryItem_attributes):
                        product_price = CategoryItem_attributes['list_price'][0]['value']
                        products_prices.append(product_price) 
                    else:
                        product_price = "0"
                        products_prices.append(product_price)
                    print("CategoryItem_products_prices:", products_prices)
                else:
                    product_price = "0"
                    products_prices.append(product_price) 
                    print("CategoryItem_products_price", products_prices)
                #save currency
                if (CategoryItem):
                    CategoryItem_attributes = CategoryItem.get("attributes")
                    if('list_price' in CategoryItem_attributes):
                        product_currency = CategoryItem_attributes['list_price'][0]['currency']
                        products_currency.append(product_currency)
                    else:
                        product_currency = "0"
                        products_currency.append(product_currency)
                    print("CategoryItem_products_currency:", products_currency)
                else:
                    product_currency = "0"
                    products_currency.append(product_currency)
                    print("CategoryItem_products_currency", products_currency)
        print("Success!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        df1 = pd.DataFrame(Asin_list, columns=['asin'])
        print("Success_asin!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        df2 = pd.DataFrame(product_title_arr, columns=['title'])
        df3 = pd.DataFrame(products_prices, columns=['price'])
        df4 = pd.DataFrame(products_images, columns=['images'])
        df5 = pd.DataFrame(products_currency, columns=['currency'])
        df = pd.concat([df1, df2, df3, df4, df5], axis=1)
        df.to_csv('登録.csv', index=False)
        
        return "Successful input_products!"
    else:
        print("Asin_new file not exist!")
        return "Asin_new file not exist! Input Asin_new fiile!"
# end def


#Create All_productsInfo_csv file
def All_productsInfo_csv(flag):
    Asin_list = []
    product_title_arr = []
    products_images = []
    products_prices = []
    products_currency = []
    if(os.path.exists('合計アシン.csv') and os.path.isfile('合計アシン.csv')):
        with open('合計アシン.csv', 'r', errors = 'ignore') as csv_file:
            csv_reader = csv.reader(csv_file)
            index = 0
            for row in csv_reader:
                if index == 0:
                    index += 1
                    continue
                Asin_list.append(row[0])
                print(row[0])
            print("Asin Length", len(Asin_list))    
        print("Get Started Input Products Info!:")
    
        for inter in range(0, len(Asin_list)):
            asin = Asin_list[inter]
            if (asin):
                CategoryItem = get_categoryItem(asin)
                if(CategoryItem):
                    data.append(CategoryItem)
                #Save title
                if(CategoryItem):
                    CategoryItem_title = CategoryItem.get("attributes")
                    product_title = CategoryItem_title['item_name'][0]['value']
                    product_title_arr.append(product_title)
                    print("All_CategoryItem_producttitle", product_title_arr)
                else:
                    product_title = "0"
                    product_title_arr.append(product_title)
                    print("All_CategoryItem_producttitle", product_title_arr)
                #Save image_urls
                if (CategoryItem):
                    CategoryItem_image = CategoryItem.get("images")
                    image_url = CategoryItem_image[0]['images'][0]['link']
                    products_images.append(image_url)  
                    print("All_CategoryItem_products_images", products_images) 
                else:
                    image_url = "0"
                    products_images.append(image_url)  
                    print("All_CategoryItem_products_images", products_images) 
                #Save price
                if (CategoryItem):
                    CategoryItem_attributes = CategoryItem.get("attributes")
                    if('list_price' in CategoryItem_attributes):
                        product_price = CategoryItem_attributes['list_price'][0]['value']
                        products_prices.append(product_price)
                    else:
                        product_price = "0"
                        products_prices.append(product_price) 
                    print("All_CategoryItem_products_price", products_prices)
                else:
                    product_price = "0"
                    products_prices.append(product_price) 
                    print("All_CategoryItem_products_price", products_prices)
                #save currency
                if (CategoryItem):
                    CategoryItem_attributes = CategoryItem.get("attributes")
                    if('list_price' in CategoryItem_attributes):
                        product_currency = CategoryItem_attributes['list_price'][0]['currency']
                        products_currency.append(product_currency)
                    else:
                        product_currency = "0"
                        products_currency.append(product_currency)
                    print("CategoryItem_products_currency:", products_currency)
                else:
                    product_currency = "0"
                    products_currency.append(product_currency)
                    print("CategoryItem_products_currency", products_currency)
        df1 = pd.DataFrame(Asin_list, columns=['asin'])
        df2 = pd.DataFrame(product_title_arr, columns=['title'])
        df3 = pd.DataFrame(products_prices, columns=['price'])
        df4 = pd.DataFrame(products_images, columns=['images'])
        df5 = pd.DataFrame(products_currency, columns=['currency'])
        df = pd.concat([df1, df2, df3, df4, df5], axis=1)
        if(flag == 0):
            df.to_csv('Amazon_製品(1).csv', index=False)
            print("Amazon_製品(1).csv create!")
        #    compare_csv_create()
        if(flag == 1):
            if (os.path.exists('Amazon_製品(1).csv') and os.path.isfile('Amazon_製品(1).csv')):
                    df.to_csv('Amazon_製品(2).csv', index=False)
                    print("Amazon_製品(2).csv create!")
            else:
                print("Amazon_製品(1).csv not existed!")
                df.to_csv('Amazon_製品(1).csv', index=False)
                print("Amazon_製品(1).csv create!")
           
        return "Successful Amazon_products!"
    
    else:
        return "Total_Asin file not existed!"
# end def


#Compare and Create Update_csv file and Remove_csv file
def compare_csv_create():
    flag = 1
    compare_create_result = All_productsInfo_csv(flag)
    print("compare_file_result", compare_create_result)
    
    df_old = pd.read_csv('Amazon_製品(1).csv')
    df_new = pd.read_csv('Amazon_製品(2).csv')
    
    df_asin_diff = df_new[df_new['price'].iloc[:] != df_old['price'].iloc[:]]
    title = df_asin_diff['title'].iloc[:]
    
    remove_rows = df_asin_diff[title == '0']
    remove_asins = remove_rows['asin']
    update_rows = df_asin_diff[title != '0']
    update_asins = update_rows['asin']
    
    if(len(remove_asins.iloc[:])):
        remove_asins.to_csv('消去.csv', index=False)
        print("消去 file created!")
    else:
        print("Nothing remove products!")
    if(len(update_asins.iloc[:])):
        update_rows.to_csv('更新.csv', index=False)
        print("更新 file created!")
    else:
        print("Nothing update products!")
    
    return "OK"
# end def

#Call functions
#Get access_token from Amazon
access_token = ''
def Amazon_products(flag_input):
    global flag, access_token
    access_token = get_access_token().get("access_token")
    print("Access Token: ", access_token)
    flag = flag_input
    print("flag:", flag)

    if (flag == 0):
        # Get input_Amazon_products_info from Amazon category
        Input_products_result = New_Input_ProductsInfo_csv()
        if (Input_products_result == "Successful input_products!"):
            print("Input_products_result: ", Input_products_result)
            All_productsInfo_result = All_productsInfo_csv(flag)
            print("All_products_info_result: ", All_productsInfo_result)

    if (flag == 1):
        compare_result = compare_csv_create()
        print("result: ", compare_result)
