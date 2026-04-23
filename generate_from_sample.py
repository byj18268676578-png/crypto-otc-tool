#!/usr/bin/env python3
"""
数据生成脚本 - 从 sample_data.json 生成可视化 HTML
使用方法：python generate_from_sample.py
"""
import json
import os

SAMPLE_FILE = 'sample_data.json'
OUTPUT_FILE = 'dashboard.html'

def generate_html():
    # 读取样本数据（现在是数组格式）
    with open(SAMPLE_FILE, 'r', encoding='utf-8') as f:
        data_list = json.load(f)
    
    # 构建图表数据
    chart_data = {}
    priority = ['BTC', 'ETH']
    
    for data in data_list:
        date = data['date']
        coins = data['coins']
        
        for coin in priority:
            if coin in coins:
                if coin not in chart_data:
                    chart_data[coin] = {
                        'dates': [],
                        'otc': [],
                        'explosion': [],
                        'statuses': []
                    }
                
                status = coins[coin]['status']
                status_text = '进场期' if '进场期' in status else '退场期'
                
                chart_data[coin]['dates'].append(f"{date} ({status_text})")
                chart_data[coin]['otc'].append(coins[coin]['otc'])
                chart_data[coin]['explosion'].append(coins[coin]['explosion'])
                chart_data[coin]['statuses'].append(status)
    
    # 生成 HTML
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto OTC Index Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f0f23; color: #fff; }
        .container { display: flex; height: 100vh; }
        .sidebar { width: 200px; background: #1a1a2e; padding: 20px; overflow-y: auto; }
        .sidebar h2 { font-size: 18px; margin-bottom: 20px; color: #4fc3f7; }
        .coin-item { padding: 10px; cursor: pointer; border-radius: 8px; margin-bottom: 8px; transition: background 0.3s; }
        .coin-item:hover { background: #2a2a4e; }
        .coin-item.active { background: #4fc3f7; color: #000; }
        .main { flex: 1; padding: 20px; overflow-y: auto; }
        .chart-container { background: #1a1a2e; border-radius: 12px; padding: 20px; margin-bottom: 20px; }
        .chart-container h3 { margin-bottom: 15px; color: #4fc3f7; }
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
        const allData = ''' + json.dumps(chart_data, ensure_ascii=False) + ''';
        const priority = ''' + json.dumps(priority, ensure_ascii=False) + ''';
        
        let currentCoin = priority[0];
        
        function renderChart() {
            const coinData = allData[currentCoin];
            if (!coinData) return;
            
            new Chart(document.getElementById('combinedChart'), {
                type: 'line',
                data: {
                    labels: coinData.dates,
                    datasets: [
                        {
                            label: '场外指数',
                            data: coinData.otc,
                            borderColor: '#4fc3f7',
                            backgroundColor: 'rgba(79, 195, 247, 0.1)',
                            yAxisID: 'y',
                            fill: true,
                            tension: 0.4
                        },
                        {
                            label: '爆破指数',
                            data: coinData.explosion,
                            borderColor: '#ff9800',
                            backgroundColor: 'rgba(255, 152, 0, 0.1)',
                            yAxisID: 'y1',
                            fill: true,
                            tension: 0.4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    interaction: {
                        mode: 'index',
                        intersect: false,
                    },
                    plugins: {
                        legend: {
                            labels: { color: '#fff' }
                        }
                    },
                    scales: {
                        x: {
                            grid: { color: 'rgba(255, 255, 255, 0.1)' },
                            ticks: { color: '#fff' }
                        },
                        y: {
                            type: 'linear',
                            display: true,
                            position: 'left',
                            grid: { color: 'rgba(255, 255, 255, 0.1)' },
                            ticks: { color: '#4fc3f7' },
                            title: {
                                display: true,
                                text: '场外指数',
                                color: '#4fc3f7'
                            }
                        },
                        y1: {
                            type: 'linear',
                            display: true,
                            position: 'right',
                            grid: { color: 'rgba(255, 255, 255, 0.1)' },
                            ticks: { color: '#ff9800' },
                            title: {
                                display: true,
                                text: '爆破指数',
                                color: '#ff9800'
                            }
                        }
                    }
                }
            });
            
            // 更新币种列表
            const coinListHTML = priority.map(coin => {
                const isActive = coin === currentCoin ? 'active' : '';
                // 使用字符串拼接来生成正确的 onclick 事件
                const quote = String.fromCharCode(39);
                return '<div class="coin-item ' + isActive + '" onclick="selectCoin(' + quote + coin + quote + ')">' + coin + '</div>';
            }).join('');
            document.getElementById('coin-list').innerHTML = coinListHTML;
        }
        
        function selectCoin(coin) {
            currentCoin = coin;
            renderChart();
        }
        
        renderChart();
    </script>
</body>
</html>'''
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 仪表盘已生成：{OUTPUT_FILE}")
    print(f"📅 数据日期范围：{data_list[0]['date']} - {data_list[-1]['date']}")
    print(f"🪙 币种数量：{len(chart_data)}")

if __name__ == '__main__':
    generate_html()
