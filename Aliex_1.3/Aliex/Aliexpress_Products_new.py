from parsel import Selector
import re
import httpx
import json
import asyncio
import jmespath
import pandas as pd
import os

flag = 0
IDs = []

# Let's use browser like request headers for this scrape to reduce chance of being blocked or asked to solve a captcha
BASE_HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US;en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
}

def parse_product(response):
    """parse product HTML page for product data"""
    sel = Selector(text=response.text)

    # find the script tag containing our data:
    script_with_data = sel.xpath('//script[contains(text(),"window.runParams")]/text()').get()
    # extract data using a regex pattern:    
    print('show', script_with_data)
    if script_with_data != None:
        data = re.findall(r".+?data:\s*({.+?)};", script_with_data, re.DOTALL)
        data = json.loads(data[0])
        # print(data)
        # with open("data1.json", "w", encoding="utf-8") as file:
        #     json.dump(data, file, indent=2, ensure_ascii=False)
        if "skuModule" in data:
            product = jmespath.search("""{
                name: titleModule.subject,
                description_short: pageModule.description,
                images: imageModule.imagePathList,
                stock: quantityModule.totalAvailQuantity,
                variants: skuModule.skuPriceList[].{
                    name: skuAttr,
                    sku: skuId,
                    available: skuVal.availQuantity,
                    stock: skuVal.inventory,
                    full_price: skuVal.skuAmount.value,
                    discount_price: skuVal.skuActivityAmount.value,
                    currency: skuVal.skuAmount.currency
                }
            }""", data)
        else:
            product = jmespath.search("""{
                name: productInfoComponent.subject,
                description_short: metaDataComponent.description,
                images: imageComponent.imagePathList,
                stock: inventoryComponent.totalAvailQuantity,
                variants: priceComponent.skuPriceList[].{
                    name: skuAttr,
                    sku: skuId,
                    available: skuVal.availQuantity,
                    stock: skuVal.inventory,
                    full_price: skuVal.skuAmount.value,
                    discount_price: skuVal.skuActivityAmount.value,
                    currency: skuVal.skuAmount.currency
                }
            }""", data)
        # product['specification'] = dict([v.values() for v in product.get('specification', {})])
        # print(product)
        return product
    else:
        print("数分後にもう一度試してみてください！")
        return "error"
        
async def scrape_products(ids, session, flag: httpx.AsyncClient):
    """scrape aliexpress products by id"""
    print(f"scraping {len(ids)} products")
    responses = await asyncio.gather(*[session.get(f"https://www.aliexpress.com/item/{id_}.html") for id_ in ids])
    results = []
    blon = 0
    for response in responses:
        result_response = parse_product(response)
        if result_response ==  "error":
            print("オユ!")
            blon = 1
            break
        else:
            results.append(result_response)
    
    # print(results)
    if blon != 1:
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(results, file, indent=2, ensure_ascii=False)
        
        if flag == 0:
            df = pd.read_json('data.json')

            title = []
            images = []
            price = []
            stock = []
            
            
            df1 = df.get("name")
            df2 = df.get("images")
            df3 = df.get("variants")
            df4 = df.get("stock")

            for i in range(0, len(df1)):
                title.append(df1[i])
                images.append(df2[i][0])
                price.append(str(df3[i][0]['full_price'])+df3[i][0]['currency'])
                stock.append(df4[i])
            
            df_ID = pd.DataFrame({"ID": ids})
            df_name = pd.DataFrame({"title": title})
            df_price = pd.DataFrame({"price": price})
            df_images = pd.DataFrame({"images": images})
            df_stock = pd.DataFrame({"stock": stock})

            df = pd.concat([df_ID, df_name, df_images, df_price, df_stock], axis=1)
            df.to_csv('登録.csv', index=False)
        
        if flag == 1 :
            df = pd.read_json('data.json')

            title = []
            images = []
            price = []
            stock = []

            df1 = df.get("name")
            df2 = df.get("images")
            df3 = df.get("variants")
            df4 = df.get("stock")

            for i in range(0, len(df1)):
                title.append(df1[i])
                images.append(df2[i][0])
                price.append(str(df3[i][0]['full_price'])+df3[i][0]['currency'])
                stock.append(df4[i])

            df_ID = pd.DataFrame({"ID": ids})
            df_name = pd.DataFrame({"title": title})
            df_price = pd.DataFrame({"price": price})
            df_images = pd.DataFrame({"images": images})
            df_stock = pd.DataFrame({"stock": stock})

            df = pd.concat([df_ID, df_name, df_images, df_price, df_stock], axis=1)
            df.to_csv('アリエクスプレス製品(1).csv', index=False)
        
        if flag ==2 :
            df = pd.read_json('data.json')

            title = []
            images = []
            price = []
            stock = []
            currency = []

            df1 = df.get("name")
            df2 = df.get("images")
            df3 = df.get("variants")
            df4 = df.get("stock")

            for i in range(0, len(df1)):
                title.append(df1[i])
                images.append(df2[i][0])
                price.append(str(df3[i][0]['full_price'])+df3[i][0]['currency'])
                stock.append(df4[i])
                currency.append(df3[i][0]['currency'])

            df_ID = pd.DataFrame({"ID": ids})
            df_name = pd.DataFrame({"title": title})
            df_price = pd.DataFrame({"price": price})
            df_images = pd.DataFrame({"images": images})
            df_stock = pd.DataFrame({"stock": stock})
            df_currency = pd.DataFrame({"currency": currency})

            df = pd.concat([df_ID, df_name, df_images, df_price, df_stock, df_currency], axis=1)
            if (os.path.exists('アリエクスプレス製品(1).csv') and os.path.isfile('アリエクスプレス製品(1).csv')):
                df.to_csv('アリエクスプレス製品(2).csv', index=False)
                print("アリエクスプレス製品(2).csv create!")    
            else:
                print("アリエクスプレス製品(1) file not existed!")    
                df.to_csv('アリエクスプレス製品(1).csv', index=False) 
                print("アリエクスプレス製品(1).csv create!")
            
            df_old = pd.read_csv('アリエクスプレス製品(1).csv')
            df_new = pd.read_csv('アリエクスプレス製品(2).csv')
            
            df_asin_diff = df_new[df_new['price'].iloc[:] != df_old['price'].iloc[:]]
            title = df_asin_diff['title'].iloc[:]
            
            remove_rows = df_asin_diff[title == '0']
            remove_asins = remove_rows['ID']
            update_rows = df_asin_diff[title != '0']
            update_asins = update_rows['ID']
            
            if(len(remove_asins.iloc[:])):
                remove_asins.to_csv('削除.csv', index=False)
                print("削除 file created!")
            else:
                print("Nothing remove products!")
            if(len(update_asins.iloc[:])):
                update_rows.to_csv('更新.csv', index=False)
                print("更新 file created!")
            else:
                print("Nothing update products!")
            
        return results
    else:
        print("オユ!")
        return "error"

async def run():
    IDs = []
    if flag == 0 :
        if(os.path.exists('新しいID.csv') and os.path.isfile('新しいID.csv')):

            print("新しいID file exist!")
            df_ID = pd.read_csv('新しいID.csv', header=None)
            ids = df_ID.iloc[:,0]

            for i in range(0, len(ids)):
                di = (ids.iloc[i:]).tolist()
                print(di[0])
                IDs.append(di[0])
            print(IDs)
            
            Total_ID = []
            if(os.path.exists('合計ID.csv') and os.path.isfile('合計ID.csv')):
                df_ID = pd.read_csv('合計ID.csv')
                total_ids = df_ID.iloc[:,0]
                 
                for i in range(0, len(total_ids)):
                    di = (total_ids.iloc[i:]).tolist()
                    print(di[0])
                    Total_ID.append(di[0])
                print(Total_ID)
                info = Total_ID + IDs
                infot = pd.DataFrame({'ID' : info})
                infot.to_csv('合計ID.csv', index=False)
            else:
                info2 = pd.DataFrame({'ID': IDs})
                info2.to_csv('合計ID.csv', index=False)
            print("合計ID Created!")

        else:
            print("新しいID file not exist!")
            exit(0)

    if flag == 1 :
        if(os.path.exists('合計ID.csv') and os.path.isfile('合計ID.csv')):
            df_ID = pd.read_csv('合計ID.csv')
            ids = df_ID.iloc[:,0]

            for i in range(0, len(ids)):
                di = (ids.iloc[i:]).tolist()
                print(di[0])
                IDs.append(di[0])
            print(IDs)
        else:
            print("合計ID file not exists!")
            exit(0)
    
    if flag == 2 :
        if(os.path.exists('合計ID.csv') and os.path.isfile('合計ID.csv')):
            df_ID = pd.read_csv('合計ID.csv')
            ids = df_ID.iloc[:,0]

            for i in range(0, len(ids)):
                di = (ids.iloc[i:]).tolist()
                print(di[0])
                IDs.append(di[0])
            print(IDs)
        else:
            print("合計ID file not exists!")
            exit(0)

    async with httpx.AsyncClient(headers=BASE_HEADERS, follow_redirects=True) as session:
        json.dumps(await scrape_products(IDs, session, flag), indent=2, ensure_ascii=False)
   

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())

