#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crypto OTC Dashboard Generator - 文本输入版本
可以直接粘贴文本数据，自动生成 dashboard.html
"""

import json
import re
import sys
from datetime import datetime

def parse_text_data(text):
    """
    从文本解析数据
    支持多种格式：
    1. 每行一个币种：BTC 1200 150 进场期第 5 天
    2. 键值对格式：BTC: 1200, 150, 进场期第 5 天
    3. 表格格式：BTC | 1200 | 150 | 进场期第 5 天
    """
    coins = {}
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # 尝试多种分隔符
        # 先尝试竖线分隔
        if '|' in line:
            parts = [p.strip() for p in line.split('|')]
        # 再尝试逗号分隔
        elif ',' in line:
            parts = [p.strip() for p in line.split(',')]
        # 最后尝试空格分隔
        else:
            parts = line.split()
        
        parts = [p.strip() for p in parts if p.strip()]
        
        if len(parts) >= 4:
            coin = parts[0].upper()
            try:
                otc = float(parts[1])
                explosion = float(parts[2])
                # 状态可能是多个词，比如"进场期第 5 天"
                status = ' '.join(parts[3:])
                
                coins[coin] = {
                    'otc': otc,
                    'explosion': explosion,
                    'status': status
                }
            except ValueError:
                continue
    
    return coins

def get_default_date():
    """获取当前日期"""
    return datetime.now().strftime('%Y-%m-%d')

def main():
    print("=" * 60)
    print("🚀 Crypto OTC Dashboard Generator (文本输入版)")
    print("=" * 60)
    print()
    
    # 询问日期
    default_date = get_default_date()
    date_input = input(f"请输入日期 (默认：{default_date}): ").strip()
    date = date_input if date_input else default_date
    
    print()
    print("📝 请输入数据（支持多种格式）：")
    print("   格式 1: BTC 1200 150 进场期第 5 天")
    print("   格式 2: BTC: 1200, 150, 进场期第 5 天")
    print("   格式 3: BTC | 1200 | 150 | 进场期第 5 天")
    print()
    print("   粘贴数据后，单独一行输入 'END' 或按 Ctrl+D 结束")
    print()
    
    # 读取多行文本
    print("粘贴数据：")
    lines = []
    try:
        while True:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
    except EOFError:
        pass
    
    text_data = '\n'.join(lines)
    
    if not text_data.strip():
        print("❌ 未输入任何数据！")
        sys.exit(1)
    
    # 解析数据
    coins = parse_text_data(text_data)
    
    if not coins:
        print("❌ 无法解析数据！请检查格式是否正确。")
        print()
        print("示例格式：")
        print("  BTC 1200 150 进场期第 5 天")
        print("  ETH 1300 180 进场期第 6 天")
        sys.exit(1)
    
    print()
    print(f"✅ 成功解析 {len(coins)} 个币种的数据：")
    for coin, data in coins.items():
        print(f"   {coin}: OTC={data['otc']}, 爆破={data['explosion']}, {data['status']}")
    
    # 生成 JSON
    data = {
        'date': date,
        'coins': coins
    }
    
    json_file = 'temp_data.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print()
    print(f"💾 数据已保存到 {json_file}")
    
    # 调用原始生成脚本
    print()
    print("🔄 正在生成 dashboard.html...")
    import subprocess
    result = subprocess.run(
        ['python3', 'generate_from_sample.py'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ dashboard.html 生成成功！")
        print()
        print("📊 打开 dashboard.html 查看图表")
        print("📁 文件位置：./dashboard.html")
    else:
        print("❌ 生成失败！")
        print(result.stderr)

if __name__ == '__main__':
    main()
