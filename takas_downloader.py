# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 18:31:32 2024

@author: user
"""
from datetime import date ,timedelta
import json
import requests 
import pandas as pd

today=date.today()
day_to_go = 150
main_data = []
today_formatted=(today-timedelta(days=1)).strftime("%d-%m-%Y")

for i in range(1,day_to_go+1):
    prev_day = today-  timedelta(days=i)
    prev_day = prev_day.strftime("%d-%m-%Y")
    #print(today,prev_day)
    #print(today_formatted)
    url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Temel-Degerler-Ve-Oranlar.aspx#page-3"
    url2 = "https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/StockInfo/CompanyInfoAjax.aspx/GetYabanciOranlarXHR"
    headers = {"Content-Type": "application/json; charset=UTF-8"}
    payload = {
        "baslangicTarih": prev_day,
        "bitisTarihi": today_formatted,
        "sektor": None,
        "endeks": "09",
        "hisse": None
    }
    
    with requests.Session() as session:
        session.get(url)
        r = session.post(url2,data=json.dumps(payload),headers=headers)
        #print(r.content)
    data = json.loads(r.text)
    #print(data["d"][0]["HISSE_KODU"], data["d"][0]["YAB_ORAN_START"])
    if len(data["d"])>0:
        for item in data["d"]:
            #print(prev_day,item["HISSE_KODU"],item["YAB_ORAN_START"])
            main_data.append({"TARIH":prev_day,"HISSE":item["HISSE_KODU"],"TAKAS_ORANI":round(item["YAB_ORAN_START"],2)})
        print(prev_day," EKLENDİ")
df = pd.DataFrame(main_data)
df = df.pivot_table(columns="HISSE", index="TARIH",values="TAKAS_ORANI").sort_values("TARIH")
df.index = pd.to_datetime(df.index,format="%d-%m-%Y")
df.sort_index(inplace=True)

df.to_excel("takas.xlsx")


