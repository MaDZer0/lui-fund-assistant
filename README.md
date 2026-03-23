# 💰 LUI Fund Assistant

> LUI基金筛选助手 - 通过自然语言对话帮用户快速找到合适的基金产品

## 项目简介

本项目是根据 PRD 文档实现的 LUI（Language User Interface）基金筛选助手原型，实现了以下核心功能（P0 优先）：

- ✅ 意图识别与槽位填充（7大槽位）
- ✅ 快捷chips引导
- ✅ 多轮对话槽位补全
- ✅ 基金列表查询与展示
- ✅ 基金详情弹窗

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Vite |
| 后端 | FastAPI (Python) |
| 接口 | RESTful API |

## 快速启动

### 1. 克隆项目

```bash
git clone https://github.com/MaDZer0/lui-fund-assistant.git
cd lui-fund-assistant
```

### 2. 启动后端

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m app.main
```

后端服务将在 `http://localhost:8000` 启动

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端将在 `http://localhost:3000` 启动

### 4. 访问

打开浏览器访问 `http://localhost:3000`

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/slots/definitions` | 获取槽位定义 |
| POST | `/nlu/extract` | 意图识别 + 槽位填充 |
| POST | `/funds/query` | 基金筛选查询 |
| GET | `/funds/{fund_code}` | 基金详情 |

## 功能演示

### 对话示例

用户输入：`"我想买稳健型的纯债基金，三个月左右"`

系统识别：
- 风险偏好 → 稳健型
- 产品类型 → 纯债
- 投资期限 → 中期(1-6个月)

返回匹配基金列表

## 后续开发

- [ ] 对接行内NLU/LLM服务（替换本地规则抽取）
- [ ] 对接真实基金数据API
- [ ] 对接客户风险等级API
- [ ] 多轮对话上下文管理优化
- [ ] 错误处理与边界情况完善

## 目录结构

```
lui-fund-assistant/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py          # FastAPI主服务
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue          # 主组件
│   │   └── style.css
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
└── README.md
```

## License

MIT
