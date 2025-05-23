# -*- coding: utf-8 -*-
# @文件名  : 测试请求全国公共资源交易平台.py
# @日期    : 2025/5/23 17:11
from src.tools.edge_browser import EdgeBrowser
from selenium.webdriver.common.by import By
ok_d = EdgeBrowser()

ok_d.open_url("http://deal.ggzy.gov.cn/ds/deal/dealList.jsp")
input('页面加载完成后按回车键')
next_page = ok_d.driver.find_element(By.XPATH, '//a[contains(text(),"下一页")]')  # 查找元素，搜索结果的下一页按钮
next_page.click()  # 点击下一页按钮

input('自动翻页后加载完成后按回车键')

requests = ok_d.get_requests("deallist_find.jsp")
for req in requests:
    print(f"\n📄 URL: {req['url']}")
    print(f"🔄 Status: {req['status']}")
    print("📦 Response Body:")
    print(req['body'])

input('测试获取数据完成,按回车关闭浏览器示例')
ok_d.close()