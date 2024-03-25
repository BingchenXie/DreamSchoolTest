# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 11:18:10 2024

@author: Bingchen
"""


import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote


# 定义目标URL
url = 'https://srh.bankofchina.com/search/whpj/search_cn.jsp'

# 定义输出TXT文件
filePath = "result.txt"


# 定义请求头部
headers = {
    'Host': 'srh.bankofchina.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://srh.bankofchina.com',
    'Connection': 'keep-alive',
    'Referer': 'https://srh.bankofchina.com/search/whpj/search_cn.jsp',
}

#币种标准符号字典
currencyDict = {
    "HKD": "港币",
    "GBP": "英镑",
    "USD": "美元",
    "CHF": "瑞士法郎",
    "DEM": "德国马克",
    "FRF": "法国法郎",
    "SGD": "新加坡元",
    "SEK": "瑞典克朗",
    "DKK": "丹麦克朗",
    "NOK": "挪威克朗",
    "JPY": "日元",
    "CAD": "加拿大元",
    "AUD": "澳大利亚元",
    "EUR": "欧元",
    "MOP": "澳门元",
    "PHP": "菲律宾比索",
    "THB": "泰国铢",
    "NZD": "新西兰元",
    "KRW": "韩元",
    "RUB": "卢布",
    "MYR": "林吉特",
    "TWD": "新台币",
    "ESP": "西班牙比塞塔",
    "ITL": "意大利里拉",
    "NLG": "荷兰盾",
    "BEF": "比利时法郎",
    "FIM": "芬兰马克",
    "INR": "印度卢比",
    "IDR": "印尼卢比",
    "BRL": "巴西里亚尔",
    "AED": "阿联酋迪拉姆",
    "ZAR": "南非兰特",
    "SAR": "沙特里亚尔",
    "TRY": "土耳其里拉"
}



def main(date,currency):
    #将输入的币种转化为URL编码格式的中文币种名称
    encodedCurrency = quote(currencyDict[currency], 'utf-8');
        
    # 发送POST请求
    response = requests.post(url, headers=headers, json="erectDate="+date+"&nothing="+date+"&pjname="
                             +encodedCurrency+"&head=head_620.js&bottom=bottom_591.js")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 使用find_all()方法查找所有table标签
    tables = soup.find_all('table')
    
    if len(tables) > 1:
        # 获取第二个table标签
        secondTable = tables[1]
    
        # 使用find_all()方法查找第二个table标签下的所有tr标签
        rows = secondTable.find_all('tr')
    
        if len(rows) > 1:
            # 获取第二个tr标签的内容
            secondRow = rows[1]
    
            #查找此tr标签下全部td
            tds = secondRow.find_all('td')
            if len(tds) >3:
                result = tds[3].get_text(strip=True)
                if len(result)>0:
                    print(result)
                    # 使用格式化字符串确保每个字段长度达到预期，并用空格进行补足
                    with open(filePath, "a") as file:
                        file.write(date + "  " + currency + "  " +
                                result + "  " + currencyDict[currency] + "\n")
                    return result
                else:
                    print("未查询到相应的记录 ErrorType:04! td is empty.")
            else:
                print("未查询到相应的记录 ErrorType:03! Second tr does not have enough tds.")
        else:
            print("未查询到相应的记录 ErrorType:02! Second table does not have enough rows.")
    else:
        print("未查询到相应的记录 ErrorType:01! Second table not found.")
    return -1

def preprocess(input1,input2):
    try:
        # 使用datetime.strptime()方法将字符串解析为日期对象
        dateObj = datetime.strptime(input1, '%Y%m%d')
    except:
        print("请检查输入的日期")
        return -1
        
    # 使用strftime()方法将日期对象格式化为指定格式的字符串
    dateStr = dateObj.strftime('%Y-%m-%d')
    # 创建2014年1月1日的日期对象
    date2014 = datetime(2014, 1, 1)
    # 获取当前日期时间
    dateNow = datetime.now()
    if dateObj<=date2014:
        print("输入日期应晚于2014年1月1日");
        return -1
    elif dateObj>dateNow:
        print("输入日期不应晚于今日");
        return -1
    elif input2 not in currencyDict:
        print(currencyDict);
        print("币种符号输入错误，支持以上币种");
        return -1
    else:
        return main(dateStr,input2);

if __name__=="__main__":
    # 获取命令行参数
    args = sys.argv

    if len(args) != 3:
        print("输入错误，请仿照如下示例运行脚本: python3 quotation.py 20240325 HKD")
    else:
        # 提取输入参数
        input1 = args[1]
        input2 = args[2].upper() #转换以支持小写输入
        preprocess(input1,input2)