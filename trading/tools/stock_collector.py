"""
股票数据采集工具 - 沪深A股列表抓取
使用 Playwright + Edge 访问东方财富网获取A股列表
"""
import asyncio
import json
import csv
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

class StockDataCollector:
    """股票数据采集器"""
    
    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir) if output_dir else Path(__file__).parent.parent / "data"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    async def fetch_hs_a_stocks(self) -> list:
        """
        抓取沪深A股列表
        数据来源：东方财富网
        """
        stocks = []
        
        async with async_playwright() as p:
            # 使用系统 Edge 浏览器
            browser = await p.chromium.launch(channel="msedge", headless=True)
            page = await browser.new_page()
            
            try:
                # 访问东方财富沪深A股行情页面
                url = "https://quote.eastmoney.com/center/gridlist.html#hs_a_board"
                print(f"正在访问: {url}")
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(3)  # 等待动态内容加载
                
                # 尝试多种可能的表格选择器
                selectors = ["#table_wrapper-table", ".table-data", "table", ".quote_table"]
                table_found = False
                for selector in selectors:
                    try:
                        await page.wait_for_selector(selector, timeout=5000)
                        print(f"找到表格选择器: {selector}")
                        table_found = True
                        break
                    except:
                        continue
                
                if not table_found:
                    print("未找到表格，保存页面源码分析...")
                    html = await page.content()
                    debug_html = self.output_dir / f"debug_html_{datetime.now():%Y%m%d_%H%M%S}.txt"
                    with open(debug_html, "w", encoding="utf-8") as f:
                        f.write(html[:5000])  # 保存前5000字符
                    print(f"页面源码已保存: {debug_html}")
                
                # 获取总页数
                pagination = await page.query_selector(".paginate_page")
                if pagination:
                    total_pages_text = await pagination.inner_text()
                    print(f"发现分页信息: {total_pages_text}")
                
                # 提取当前页数据
                rows = await page.query_selector_all("#table_wrapper-table tbody tr")
                print(f"当前页找到 {len(rows)} 行数据")
                
                for row in rows[:10]:  # 先取前10条测试
                    cells = await row.query_selector_all("td")
                    if len(cells) >= 6:
                        stock = {
                            "序号": await cells[0].inner_text() if len(cells) > 0 else "",
                            "代码": await cells[1].inner_text() if len(cells) > 1 else "",
                            "名称": await cells[2].inner_text() if len(cells) > 2 else "",
                            "最新价": await cells[3].inner_text() if len(cells) > 3 else "",
                            "涨跌幅": await cells[4].inner_text() if len(cells) > 4 else "",
                            "涨跌额": await cells[5].inner_text() if len(cells) > 5 else "",
                            "采集时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        stocks.append(stock)
                        print(f"  抓取: {stock['代码']} {stock['名称']}")
                
                # 截图保存
                screenshot_path = self.output_dir / f"screenshot_hs_a_{datetime.now():%Y%m%d_%H%M%S}.png"
                await page.screenshot(path=str(screenshot_path))
                print(f"截图已保存: {screenshot_path}")
                
            except Exception as e:
                print(f"抓取过程出错: {e}")
                # 出错时保存截图用于调试
                debug_path = self.output_dir / f"debug_error_{datetime.now():%Y%m%d_%H%M%S}.png"
                await page.screenshot(path=str(debug_path))
                print(f"错误截图已保存: {debug_path}")
                
            finally:
                await browser.close()
        
        return stocks
    
    def save_to_json(self, stocks: list, filename: str = None):
        """保存为JSON格式"""
        if not filename:
            filename = f"hs_a_stocks_{datetime.now():%Y%m%d_%H%M%S}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(stocks, f, ensure_ascii=False, indent=2)
        print(f"JSON数据已保存: {filepath}")
        return filepath
    
    def save_to_csv(self, stocks: list, filename: str = None):
        """保存为CSV格式"""
        if not filename:
            filename = f"hs_a_stocks_{datetime.now():%Y%m%d_%H%M%S}.csv"
        filepath = self.output_dir / filename
        
        if not stocks:
            print("没有数据可保存")
            return None
        
        with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=stocks[0].keys())
            writer.writeheader()
            writer.writerows(stocks)
        print(f"CSV数据已保存: {filepath}")
        return filepath


async def main():
    """主程序"""
    print("=" * 50)
    print("沪深A股数据采集工具")
    print("=" * 50)
    
    collector = StockDataCollector()
    
    # 采集数据
    print("\n开始抓取沪深A股数据...")
    stocks = await collector.fetch_hs_a_stocks()
    
    if stocks:
        print(f"\n成功抓取 {len(stocks)} 条股票数据")
        
        # 保存数据
        collector.save_to_json(stocks)
        collector.save_to_csv(stocks)
        
        # 显示前5条
        print("\n前5条数据预览:")
        for stock in stocks[:5]:
            print(f"  {stock['代码']} | {stock['名称']} | {stock['最新价']} | {stock['涨跌幅']}")
    else:
        print("未获取到数据")
    
    print("\n采集完成!")


if __name__ == "__main__":
    asyncio.run(main())
