import pandas as pd
import csv
def update_csv(rate, filename):
    df1 = pd.read_csv(filename)
    old_price = df1['price'].iloc[:]

    ids = df1['ID'].iloc[:]
    title = df1['title'].iloc[:]
    price = old_price * rate
    image = df1['images'].iloc[:]
    print(ids)
    print(price)
    df1 = pd.DataFrame(ids, columns=['ID'])
    df2 = pd.DataFrame(title, columns=['title'])
    df3 = pd.DataFrame(price, columns=['price'])
    df4 = pd.DataFrame(image, columns=['images'])
    df = pd.concat([df1, df2, df3, df4], axis=1)
    df.to_csv(filename, index=False)


