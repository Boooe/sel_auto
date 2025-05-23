# -*- coding: utf-8 -*-
# @文件名  : 1.py
# @日期    : 2025/5/23 11:23
# pip install selenium-wire[full]
import json

from selenium.webdriver.edge.options import Options
from seleniumwire import webdriver  # 注意：使用 seleniumwire 提供的 webdriver

# 创建 Edge 选项
options = Options()
options.use_chromium = True  # 确保是基于 Chromium 的 Edge
# options.add_argument('--disable-application-cache')  # 禁用应用缓存，防止页面加载使用本地缓存内容
# options.add_argument('--disable-cache')  # 完全禁用浏览器缓存（包括内存和磁盘缓存）
# options.add_extension(r'E:\Z\aqc_2025\tools\Anti.crx')  # 使用本地插件  Anti Debug
# options.add_argument("--disable-restore-session")  # 禁用会话恢复功能，防止浏览器异常退出后恢复上次会话或标签页
# options.add_argument("--ignore-ssl-errors=true")# 忽略所有 SSL 证书错误（不建议用于生产环境）
# options.add_argument("--ssl-protocol=TLSv1")# 指定使用 TLSv1 协议（较旧，不推荐，建议默认或使用更高版本）
# options.add_argument(fr'--user-data-dir=C:\edge\test')# 指定用户数据目录，保留 cookies、扩展、登录状态等（相当于模拟一个用户环境）
# options.add_argument("--window-size=1920,1080")  # 设置浏览器窗口大小（宽 1920，高 1080）
# options.add_argument("--disable-dev-usage")# 禁用开发者用途（不是标准参数，可能无效或忽略）
# options.add_argument('--auto-open-devtools-for-tabs') # 自动为每个新标签页打开开发者工具（调试用）
# options.add_argument("--disable-blink-features=AutomationControlled")# 屏蔽浏览器自动化特征，如 navigator.webdriver=true

# selenium-wire 配置
seleniumwire_options = {
    'verify_ssl': False,  # 避免 HTTPS 报错 忽略 SSL 证书验证
    'enable_har': True,  # 可选：导出 HAR 文件
    # 代理ip信息
    'proxy':{
        'http': 'http://b399.kdltps.com:15818',
        'https': 'http://b399.kdltps.com:15818',
        # 'no_proxy': 'localhost,127.0.0.1'
    },

    'disable_capture': False,  # 默认不禁用，等于开启请求捕获 如果关闭则无法获取请求响应的内容
    'request_storage_base_dir': './logs',  # 自定义请求数据存储位置
}

# 启动 Edge 浏览器
driver = webdriver.Edge(
    options=options,
    seleniumwire_options=seleniumwire_options
)

# 打开网站
driver.get("https://dev.kdlapi.com/testproxy")
input('wait...1')
driver.get("http://deal.ggzy.gov.cn/ds/deal/dealList.jsp")

# 可选：等待网络请求完成
input("wait...2")

# 遍历所有请求，打印 URL 和响应体（只打印 JSON 类型响应）
for request in driver.requests:
    if request.response:
        url: str = request.url.lower()  # 请求的完整url转为小写
        response_headers: dict = request.response.headers  # 响应头部字段
        content_type = response_headers.get('Content-Type', '')

        if "deallist_find.jsp" in url:
            print(f"\n📄 URL: {request.url}")
            print(f"🔄 Status: {request.response.status_code}")
            print("📦 Response Body:")
            try:
                body_bytes = request.response.body  # bytes 类型
                body_str = body_bytes.decode("utf-8", errors="replace")  # 转换为字符串
                body_json = json.loads(body_str)
                print(body_json)
            except Exception as e:
                print(f"(Error reading body: {e})")

# 可选：保存 HAR 文件
# with open("network.har", "w", encoding="utf-8") as f:
#     f.write(driver.har)

input('end')
driver.quit()
