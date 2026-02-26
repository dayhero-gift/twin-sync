"""
股票数据采集工具 - 通过API获取沪深A股列表
使用东方财富API接口，无需浏览器渲染
"""
import asyncio
import json
import csv
import aiohttp
from datetime import datetime
from pathlib import Path

class StockDataCollector:
    """股票数据采集器 - API方式"""
    
    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir) if output_dir else Path(__file__).parent.parent / "data"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    async def fetch_hs_a_stocks(self, page: int = 1, page_size: int = 20) -> list:
        """
        通过东方财富API获取沪深A股列表
        """
        stocks = []
        
        # 东方财富API接口
        api_url = "https://push2.eastmoney.com/api/qt/clist/get"
        params = {
            "pn": page,  # 页码
            "pz": page_size,  # 每页条数
            "po": 1,  # 排序方式
            "np": 1,
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "fltt": 2,
            "invt": 2,
            "fid": "f12",  # 按代码排序
            "fs": "m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23",  # 沪深A股
            "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f27,f28,f29,f30,f31,f32,f33,f34,f35,f36,f37,f38,f39,f40,f41,f42,f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65,f66,f67,f68,f69,f70,f71,f72,f73,f74,f75,f76,f77,f78,f79,f80,f81,f82,f83,f84,f85,f86,f87,f88,f89,f90,f91",
            "_": int(datetime.now().timestamp() * 1000)
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.0 Edg/120.0.0.0",
            "Referer": "https://quote.eastmoney.com/"
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(api_url, params=params, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if data.get("data") and data["data"].get("diff"):
                            raw_stocks = data["data"]["diff"]
                            total = data["data"].get("total", 0)
                            print(f"获取成功！总股票数: {total}，当前页: {len(raw_stocks)} 条")
                            
                            for item in raw_stocks:
                                # 字段映射
                                stock = {
                                    "代码": item.get("f12", ""),
                                    "名称": item.get("f14", ""),
                                    "最新价": self._format_price(item.get("f2")),
                                    "涨跌幅": self._format_percent(item.get("f3")),
                                    "涨跌额": self._format_price(item.get("f4")),
                                    "成交量(手)": item.get("f5", ""),
                                    "成交额": item.get("f6", ""),
                                    "振幅": self._format_percent(item.get("f7")),
                                    "最高": self._format_price(item.get("f15")),
                                    "最低": self._format_price(item.get("f16")),
                                    "今开": self._format_price(item.get("f17")),
                                    "昨收": self._format_price(item.get("f18")),
                                    "量比": item.get("f10", ""),
                                    "换手率": self._format_percent(item.get("f8")),
                                    "市盈率": item.get("f9", ""),
                                    "市净率": item.get("f23", ""),
                                    "总市值": item.get("f20", ""),
                                    "流通市值": item.get("f21", ""),
                                    "采集时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                }
                                stocks.append(stock)
                    else:
                        print(f"请求失败，状态码: {response.status}")
                        
            except Exception as e:
                print(f"请求异常: {e}")
        
        return stocks
    
    def _format_price(self, value):
        """格式化价格"""
        if value is None or value == "-":
            return "-"
        try:
            return round(float(value) / 100, 2) if float(value) > 1000 else float(value)
        except:
            return value
    
    def _format_percent(self, value):
        """格式化百分比"""
        if value is None or value == "-":
            return "-"
        try:
            return f"{round(float(value) / 100, 2)}%"
        except:
            return value
    
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
    print("沪深A股数据采集工具 (API版)")
    print("=" * 50)
    
    collector = StockDataCollector()
    
    # 采集数据
    print("\n开始抓取沪深A股数据...")
    stocks = await collector.fetch_hs_a_stocks(page=1, page_size=20)
    
    if stocks:
        print(f"\n成功抓取 {len(stocks)} 条股票数据")
        
        # 保存数据
        collector.save_to_json(stocks)
        collector.save_to_csv(stocks)
        
        # 显示前5条
        print("\n前5条数据预览:")
        for stock in stocks[:5]:
            print(f"  {stock['代码']} | {stock['名称']:<8} | 最新价:{stock['最新价']:>8} | 涨跌幅:{stock['涨跌幅']:>8}")
    else:
        print("未获取到数据")
    
    print("\n采集完成!")


if __name__ == "__main__":
    asyncio.run(main())
