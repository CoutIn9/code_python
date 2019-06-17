from selenium import webdriver
from time import sleep
import datetime
import urllib.parse
from pymongo import MongoClient
from red_csv import get_kb
import requests
import json
from lxml import etree
# chrome_ons = webdriver.ChromeOptions()
# chrome_ons.add_argument('--headless')

host='192.168.30.135'
port= 27017
dbName='db'
client=MongoClient("mongodb://root:" + urllib.parse.quote("") + "")
   # 创建连接对象client
db = client[dbName]
post = db['']

key = ''
driver = webdriver.Chrome()


driver.get('http://www.catalog.update.microsoft.com/Search.aspx?q=Windows%20server%202003%20%EF%BC%8C%E5%AE%89%E5%85%A8%E6%9B%B4%E6%96%B0%E7%A8%8B%E5%BA%8F')
# print(driver.page_source)
# print(r.text)
# driver.find_element_by_id('ctl00_searchTextBox').send_keys(key)
# driver.find_element_by_id('searchButtonLink').click()
# sleep(1)

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Content-Type':
    'text/html'
}
post_header = {
    'Content-Type':'application/json'
}

data ,kb_li = get_kb()

main_window = driver.window_handles
while True:
    res_li = []
    li = driver.find_elements_by_xpath("//div[@class='resultsBackGround']/table//tr")
    li.remove(li[0])
    for i in li:
        try:
            jsonData={}
            des=i.find_element_by_xpath('./td[2]')
            i.find_element_by_xpath('./td[8]/input').click()
            des.click()
            sleep(3)

            all_handles = driver.window_handles

            driver.switch_to.window(all_handles[1])
            sleep(0.5)
            jsonData['patch_desc'] = driver.find_element_by_id('ScopedViewHandler_desc').text
            # sleep(3)

            driver.close()
            driver.switch_to.window(all_handles[2])
            sleep(0.5)
            dl = driver.find_element_by_xpath("//div['downloadFiles']/div/a")
            download= dl.get_attribute('href')
            driver.close()
            driver.switch_to.window(all_handles[0])
            sleep(0.5)
            products=i.find_element_by_xpath('./td[3]').text
            classification = i.find_element_by_xpath('./td[4]').text
            times = i.find_element_by_xpath('./td[5]').text
            # sleep(100)
            jsonData["patch_id"] = des.text.split('(')[-1].replace(")","")
            if jsonData["patch_id"] in kb_li:
                print(data.get(jsonData["patch_id"]))
                cve = data.get(jsonData["patch_id"]) if data.get(jsonData["patch_id"]) else ''
                cve = cve.split(',')
                url = 'http://39.108.9.131:59815/exploit/'
                param = {
                    "cve": cve
                }
                r = requests.post(url,json= param,headers=post_header)
                jsonData['cve'] = json.loads(r.text)['results']
            else:
                print('未匹配到')
                jsonData['cve'] = []

            jsonData["os_name"] =products
            jsonData["patch_type"] =classification
            jsonData["release_time"] = times
            jsonData["download_link"] = download
            jsonData["store_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(jsonData)
            res_li.append(jsonData)
        except:
            all_handles = driver.window_handles
            for handle in all_handles:
                if handle !=main_window[0]:
                    driver.switch_to.window(handle)
                    driver.close()
            driver.switch_to.window(main_window[0])
            continue
    post.insert(res_li)
        # 下一页
    try:
        driver.find_element_by_id('ctl00_catalogBody_nextPageLinkText').click()
        sleep(2)
    except Exception as e:
        driver.close()



# driver.close()
