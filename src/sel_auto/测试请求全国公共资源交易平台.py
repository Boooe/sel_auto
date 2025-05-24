# -*- coding: utf-8 -*-
# @文件名  : 测试请求全国公共资源交易平台.py
# @日期    : 2025/5/23 17:11
from src.tools.edge_browser import EdgeBrowser
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
ok_d = EdgeBrowser()

ok_d.open_url("http://deal.ggzy.gov.cn/ds/deal/dealList.jsp")
input('点击开发者工具中的网络查看下过,页面加载完成后按回车键')
# 翻页方法1
next_page = ok_d.driver.find_element(By.XPATH, '//a[contains(text(),"下一页")]')  # 查找元素，搜索结果的下一页按钮
next_page.click()  # 点击下一页按钮

# 翻页方法2
current_date = datetime.now().date()
seven_days_ago = current_date - timedelta(days=7)
current_date_str = current_date.strftime('%Y-%m-%d')
seven_days_ago_str = seven_days_ago.strftime('%Y-%m-%d')
see_page = 3
js = f'''fetch("https://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp", {{
    "headers": {{
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "pragma": "no-cache",
        "sec-ch-ua": "\\"Chromium\\";v=\\"136\\", \\"Microsoft Edge\\";v=\\"136\\", \\"Not.A/Brand\\";v=\\"99\\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\\"Windows\\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
        "Referer": "https://deal.ggzy.gov.cn/ds/deal/dealList.jsp",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }},
    "body": "TIMEBEGIN_SHOW={seven_days_ago_str}&TIMEEND_SHOW={current_date_str}&TIMEBEGIN={seven_days_ago_str}&TIMEEND={current_date_str}&SOURCE_TYPE=1&DEAL_TIME=02&DEAL_CLASSIFY=00&DEAL_STAGE=0000&DEAL_PROVINCE=0&DEAL_CITY=0&DEAL_PLATFORM=0&BID_PLATFORM=0&DEAL_TRADE=0&isShowAll=1&PAGENUMBER={see_page}&FINDTXT=",
    "method": "POST"
}});
'''
ok_d.driver.execute_script(js)
input('两个网络请求加载完成后按回车查看请求效果')

resp = ok_d.get_requests("deallist_find.jsp")
for item in resp:
    print(item)
    # print(f"\n📄 URL: {item['url']} ")
    # print(f"🔄 Status: {item['status']}")
    # print("📦 Response Body:")
    # print(item['body'])

input('测试获取数据完成,按回车关闭浏览器示例')
ok_d.close()
