<<<<<<< HEAD
# Crypto OTC Dashboard Generator

一个简单的工具，用于将 OTC 指数数据转换为可视化 HTML 图表。

## 📦 文件说明

- `sample_data.json` - 数据输入模板
- `generate_from_sample.py` - 数据生成脚本
- `dashboard.html` - 生成的可视化页面

## 🚀 使用方法

### 1. 准备数据

编辑 `sample_data.json` 文件，填入你的数据：

```json
{
  "date": "2026-04-22",
  "coins": {
    "BTC": {
      "otc": 1200,
      "explosion": 150,
      "status": "进场期第 5 天"
    },
    "ETH": {
      "otc": 1300,
      "explosion": 180,
      "status": "进场期第 6 天"
    }
  }
}
```

### 2. 运行生成脚本

```bash
python3 generate_from_sample.py
```

### 3. 查看结果

打开 `dashboard.html` 文件即可在浏览器中查看可视化图表。

## 📋 数据格式说明

- `date`: 数据日期 (格式：YYYY-MM-DD)
- `coins`: 币种数据对象
  - `otc`: 场外指数 (数字)
  - `explosion`: 爆破指数 (数字)
  - `status`: 进退场状态 (如："进场期第 5 天" 或 "退场期第 12 天")

## 🌐 部署到 GitHub Pages (可选)

```bash
# 1. 初始化 git (如果还没有)
git init

# 2. 添加文件
git add .

# 3. 提交
git commit -m "Update dashboard"

# 4. 推送到 GitHub
git push origin main
```

然后在 GitHub 仓库设置中启用 GitHub Pages。

## ⚠️ 注意事项

- 需要 Python 3.6+ 环境
- 生成的 HTML 使用 Chart.js 库，需要联网加载
- 建议定期备份 `sample_data.json` 文件
=======
# crypto-otc-tool
>>>>>>> 97aa2f1990c9f28f7ab1c75b1c320a7068ca4654
