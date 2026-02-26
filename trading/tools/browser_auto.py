"""
小天浏览器自动化工具 - 使用 Playwright + Edge
用于数据采集、网页监控、自动化操作
"""
import asyncio
from playwright.async_api import async_playwright

async def test_browser():
    """测试浏览器自动化功能"""
    async with async_playwright() as p:
        # 使用系统已安装的 Microsoft Edge
        browser = await p.chromium.launch(channel="msedge", headless=False)
        page = await browser.new_page()
        
        # 访问东方财富网 - 沪深A股行情
        await page.goto("https://quote.eastmoney.com/center/gridlist.html#hs_a_board")
        await asyncio.sleep(3)
        
        # 获取页面标题
        title = await page.title()
        print(f"页面标题: {title}")
        
        # 获取页面主要内容
        content = await page.content()
        print(f"页面内容长度: {len(content)} 字符")
        
        # 截图保存
        await page.screenshot(path="screenshot_test.png")
        print("截图已保存: screenshot_test.png")
        
        await browser.close()
        return title

if __name__ == "__main__":
    result = asyncio.run(test_browser())
    print(f"测试完成！访问页面: {result}")
