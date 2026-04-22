#!/usr/bin/env python3
"""
数据生成脚本 - 从 sample_data.json 生成可视化 HTML
使用方法：python generate_from_sample.py
"""
import json
import os

SAMPLE_FILE = '/root/.hermes/visualization/sample_data.json'
OUTPUT_FILE = '/root/.hermes/visualization/dashboard.html'

def generate_html():
    # 读取样本数据
    with open(SAMPLE_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    date = data['date']
    coins = data['coins']
    
    # 确定优先级币种
    priority = ['BTC', 'ETH']
    for coin in coins:
        if coin not in priority:
            if coins[coin].get('explosion', 0) > 0 or '进场期' in coins[coin].get('status', ''):
                priority.append(coin)
    
    # 构建图表数据
    chart_data = {}
    for coin in priority:
        if coin in coins:
            chart_data[coin] = {
                'date': date,
                'otc': coins[coin]['otc'],
                'explosion': coins[coin]['explosion'],
                'status': coins[coin]['status']
            }
    
    # 生成 HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto OTC Index Dashboard - {date}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f0f23; color: #fff; }}
        .container {{ display: flex; height: 100vh; }}
        .sidebar {{ width: 200px; background: #1a1a2e; padding: 20px; overflow-y: auto; }}
        .sidebar h2 {{ font-size: 18px; margin-bottom: 20px; color: #4fc3f7; }}
        .coin-item {{ padding: 10px; cursor: pointer; border-radius: 8px; margin-bottom: 8px; transition: background 0.3s; }}
        .coin-item:hover {{ background: #2a2a4e; }}
        .coin-item.active {{ background: #4fc3f7; color: #000; }}
        .main {{ flex: 1; padding: 20px; overflow-y: auto; }}
        .chart-container {{ background: #1a1a2e; border-radius: 12px; padding: 20px; margin-bottom: 20px; }}
        .chart-container h3 {{ margin-bottom: 15px; color: #4fc3f7; }}
        .status-label {{ display: inline-block; padding: 4px 12px; border-radius: 4px; font-size: 12px; margin-left: 10px; }}
        .status-entry {{ background: #4caf50; color: #fff; }}
        .status-exit {{ background: #f44336; color: #fff; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <h2>🪙 币种选择</h2>
            <div id="coin-list"></div>
        </div>
        <div class="main">
            <div class="chart-container">
                <h3>场外指数与爆破指数趋势图</h3>
                <canvas id="combinedChart"></canvas>
            </div>
        </div>
    </div>
    <script>
        const allData = {json.dumps(chart_data, ensure_ascii=False)};
        const priority = {json.dumps(priority, ensure_ascii=False)};
        
        let currentCoin = priority[0];
        
        function renderChart() {{
            const coinData = allData[currentCoin];
            if (!coinData) return;
            
            const status = coinData.status;
            const statusClass = status.includes('entry') ? 'status-entry' : 'status-exit';
            const statusText = status.includes('entry') ? '进场期' : '退场期';
            
            // 创建带进退场天数的日期标签
            const dateLabel = `${{coinData.date}} (${{statusText}})`;
            
            document.getElementById('coin-list').innerHTML = priority.map(coin => 
                `<div class="coin-item ${{coin === currentCoin ? 'active' : ''}}" onclick="selectCoin('${{coin}}')">${{coin}}</div>`
            ).join('');
            
            new Chart(document.getElementById('combinedChart'), {{
                type: 'line',
                data: {{
                    labels: [dateLabel],
                    datasets: [
                        {{
                            label: '场外指数',
                            data: [coinData.otc],
                            borderColor: '#4fc3f7',
                            backgroundColor: 'rgba(79, 195, 247, 0.1)',
                            yAxisID: 'y',
                            fill: true,
                            tension: 0.4
                        }},
                        {{
                            label: '爆破指数',
                            data: [coinData.explosion],
                            borderColor: '#ff9800',
                            backgroundColor: 'rgba(255, 152, 0, 0.1)',
                            yAxisID: 'y1',
                            fill: true,
                            tension: 0.4
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    interaction: {{
                        mode: 'index',
                        intersect: false,
                    }},
                    plugins: {{
                        legend: {{
                            labels: {{ color: '#fff' }}
                        }}
                    }},
                    scales: {{
                        x: {{
                            grid: {{ color: 'rgba(255, 255, 255, 0.1)' }},
                            ticks: {{ color: '#fff' }}
                        }},
                        y: {{
                            type: 'linear',
                            display: true,
                            position: 'left',
                            grid: {{ color: 'rgba(255, 255, 255, 0.1)' }},
                            ticks: {{ color: '#4fc3f7' }},
                            title: {{
                                display: true,
                                text: '场外指数',
                                color: '#4fc3f7'
                            }}
                        }},
                        y1: {{
                            type: 'linear',
                            display: true,
                            position: 'right',
                            grid: {{ color: 'rgba(255, 255, 255, 0.1)' }},
                            ticks: {{ color: '#ff9800' }},
                            title: {{
                                display: true,
                                text: '爆破指数',
                                color: '#ff9800'
                            }}
                        }}
                    }}
                }}
            }});
        }}
        
        function selectCoin(coin) {{
            currentCoin = coin;
            renderChart();
        }}
        
        renderChart();
    </script>
</body>
</html>'''
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 仪表盘已生成：{OUTPUT_FILE}")
    print(f"📅 数据日期：{date}")
    print(f"🪙 币种数量：{len(chart_data)}")

if __name__ == '__main__':
    generate_html()
