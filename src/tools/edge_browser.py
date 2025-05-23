# -*- coding: utf-8 -*-
# @文件名  : edge_browser.py
# @日期    : 2025/5/23
import json
from typing import Dict, Optional

from selenium.webdriver.edge.options import Options
from seleniumwire import webdriver


class EdgeBrowser:
    def __init__(self, 
                 proxy: Optional[Dict[str, str]] = None,
                 user_data_dir: Optional[str] = None,
                 window_size: Optional[tuple] = None,
                 headless: bool = False,
                 enable_har: bool = True):
        """
        初始化Edge浏览器
        
        :param proxy: 代理配置，格式如 {'http': 'http://proxy:port', 'https': 'https://proxy:port'}
        :param user_data_dir: 用户数据目录路径
        :param window_size: 浏览器窗口大小，如 (1920, 1080)
        :param headless: 是否无头模式
        :param enable_har: 是否启用HAR记录
        """
        self.options = Options()
        self.options.use_chromium = True
        
        # 配置浏览器选项
        if user_data_dir:
            self.options.add_argument(f'--user-data-dir={user_data_dir}')
        if window_size:
            self.options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')
        if headless:
            self.options.add_argument('--headless=new')
            
        # selenium-wire配置
        self.seleniumwire_options = {
            'verify_ssl': False,
            'enable_har': enable_har,
            'disable_capture': False,
            'request_storage_base_dir': './logs'
        }
        
        if proxy:
            self.seleniumwire_options['proxy'] = proxy
            
        # 初始化driver
        self.driver = webdriver.Edge(
            options=self.options,
            seleniumwire_options=self.seleniumwire_options
        )
    
    def open_url(self, url: str):
        """打开指定URL"""
        self.driver.get(url)
    
    def get_requests(self, url_filter: Optional[str] = None) -> list:
        """
        获取所有请求
        
        :param url_filter: URL过滤字符串，如 'deallist_find.jsp'
        :return: 过滤后的请求列表
        """
        requests = []
        for request in self.driver.requests:
            if request.response:
                url = request.url.lower()
                if url_filter and url_filter.lower() not in url:
                    continue
                    
                try:
                    body_str = request.response.body.decode("utf-8", errors="replace")
                    body_json = json.loads(body_str)
                    requests.append({
                        'url': request.url,
                        'status': request.response.status_code,
                        'body': body_json
                    })
                except Exception:
                    continue
        return requests
    
    def save_har(self, file_path: str):
        """保存HAR文件"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.driver.har)
    
    def close(self):
        """关闭浏览器"""
        self.driver.quit()


if __name__ == "__main__":
    # 使用示例
    browser = EdgeBrowser(
        proxy={
            'http': 'http://b399.kdltps.com:15818',
            'https': 'http://b399.kdltps.com:15818'
        },
        window_size=(1920, 1080)
    )
    
    try:
        browser.open_url("https://dev.kdlapi.com/testproxy")
        input('等待...1')
        browser.open_url("http://deal.ggzy.gov.cn/ds/deal/dealList.jsp")
        input('等待...2')
        
        # 获取特定请求
        requests = browser.get_requests("deallist_find.jsp")
        for req in requests:
            print(f"\n📄 URL: {req['url']}")
            print(f"🔄 Status: {req['status']}")
            print("📦 Response Body:")
            print(req['body'])
            
        # 可选：保存HAR文件
        browser.save_har(file_path="network.har")
        
    finally:
        input('结束')
        browser.close()