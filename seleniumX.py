import sys
from datetime import datetime
from urllib.parse import quote
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

#设置日志级别
import logging
log_file_path = 'selenium.log'
logging.basicConfig(filename=log_file_path, level=logging.WARNING)

# 定义输出TXT文件
filePath = "result.txt"

#currency字典
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

monthDict = {
    1 : "一月",
    2 : "二月",
    3 : "三月",
    4 : "四月",
    5 : "五月",
    6 : "六月",
    7 : "七月",
    8 : "八月",
    9 : "九月",
    10 : "十月",
    11 : "十一月",
    12 : "十二月",
}

def main(year,month,day,currency):
    usedYear = str(year) + '年'
    usedMonth = monthDict[month]
    # 创建 WebDriver 对象，并设置 Chrome 浏览器的日志级别
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--log-level=3')  # 设置日志级别为 WARNING
    driver = webdriver.Chrome(options=chrome_options)

    # 打开网页
    driver.get("https://www.boc.cn/sourcedb/whpj/")

    #起始时间erectDate
    elementStart = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "erectDate"))
    )
    elementStart.click()
    # 年
    elementYear = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "calendarYear"))
    )
    select = Select(elementYear)
    select.select_by_visible_text(usedYear)
    #月
    elementMonth = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "calendarMonth"))
    )
    select = Select(elementMonth)
    select.select_by_visible_text(usedMonth)
    #日
    elementDay = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table[@id='calendarTable']//td[text()='"+str(day)+"']"))
    )
    elementDay.click()

    #结束时间nothing
    elementEnd = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "nothing"))
    )
    elementEnd.click()
    # 年
    elementYear = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "calendarYear"))
    )
    select = Select(elementYear)
    select.select_by_visible_text(usedYear)
    #月
    elementMonth = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "calendarMonth"))
    )
    select = Select(elementMonth)
    select.select_by_visible_text(usedMonth)
    #日
    elementDay = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table[@id='calendarTable']//td[text()='"+str(day)+"']"))
    )
    elementDay.click()


    #选择币种pjname
    try:
        elementCurrency = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "pjname"))
        )
        select = Select(elementCurrency)
        select.select_by_value(currencyDict[currency])
    except:
        print("ERROR01:未查询到相应的记录。currency error")
        return -1

    #点击按钮executeSearch
    elementIcon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@onclick, 'executeSearch')]"))
    )
    elementIcon.click()

    #现汇卖出价所在行
    elementRow = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[@class='wrapper']/div[@class='BOC_main publish']/table/tbody/tr[2]"))
    )
    # 在 elementRow 中查找所有的<td>元素
    elements = elementRow.find_elements(By.TAG_NAME, "td")

    if len(elements) >= 4:
        result = elements[3].text
        if len(result)>0:
            print(result)
        else:
            print("ERROR02:未查询到相应的记录。 number error")
            return -3
    else:
        print("ERROR03:未查询到相应的记录。 table error")
        return -2

    # 关闭浏览器
    # input("按回车键结束")
    driver.quit()

    with open(filePath, "a") as file:
        file.write("{}-{}-{}".format(year, month, day) + "  " + currency + "  " +
                result + "  " + currencyDict[currency] + "\n")

    return result

def preprocess(input1,input2):
    # 提取输入参数
    input1 = args[1]
    input2 = args[2].upper() #转换以支持小写输入
    
    # 使用datetime.strptime()方法将字符串解析为日期对象
    try:
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
        return main(dateObj.year,dateObj.month,dateObj.day,input2);
    


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
