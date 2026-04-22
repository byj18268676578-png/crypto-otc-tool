#!/usr/bin/env python3
"""
GitHub Pages 部署脚本
使用方法：python deploy_to_github_pages.py
"""
import subprocess
import os
import sys

def deploy():
    print("🚀 正在部署到 GitHub Pages...")
    
    # 检查 git 状态
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if result.stdout:
        print("⚠️  有未提交的更改，请先提交")
        print(result.stdout)
        return False
    
    # 推送
    print("📤 推送到 GitHub...")
    result = subprocess.run(
        ['git', 'push', '-u', 'origin', 'main'],
        capture_output=True,
        text=True,
        timeout=60
    )
    
    if result.returncode == 0:
        print("✅ 推送成功！")
        print("\n🌐 部署步骤:")
        print("1. 访问 https://github.com/byj18268676578/crypto-otc-tool")
        print("2. 进入 Settings -> Pages")
        print("3. 选择 'main' 分支作为源")
        print("4. 点击 Save")
        print("\n📍 部署地址：https://byj18268676578.github.io/crypto-otc-tool/")
        return True
    else:
        print("❌ 推送失败:")
        print(result.stderr)
        return False

if __name__ == '__main__':
    deploy()
