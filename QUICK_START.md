# 🚀 快速开始指南

## 下载工具

工具包已打包在：`/root/.hermes/visualization/crypto-otc-tool.tar.gz`

## 解压工具

```bash
tar -xzf /root/.hermes/visualization/crypto-otc-tool.tar.gz
```

解压后会得到 `crypto-otc-tool` 文件夹。

## 使用工具

### 1. 编辑数据

打开 `crypto-otc-tool/sample_data.json`，填入你的数据：

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

### 2. 生成图表

进入工具目录，运行：

```bash
cd crypto-otc-tool
python3 generate_from_sample.py
```

### 3. 查看结果

打开 `dashboard.html` 文件即可在浏览器中查看。

## 示例数据

你可以使用已有的示例数据：

- BTC: 场外指数 1200, 爆破指数 150, 进场期第 5 天
- ETH: 场外指数 1300, 爆破指数 180, 进场期第 6 天

## 常见问题

**Q: 需要安装什么依赖？**
A: 只需要 Python 3.6+，不需要额外安装库。

**Q: 如何部署到网上？**
A: 将生成的 `dashboard.html` 上传到 GitHub Pages 或其他静态网站托管服务。

**Q: 可以批量生成多天的图表吗？**
A: 可以！修改 `sample_data.json` 中的日期，每次生成新的 HTML 文件。
