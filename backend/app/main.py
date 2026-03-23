"""
LUI Fund Assistant - 后端服务
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import httpx

app = FastAPI(title="LUI Fund Assistant API", version="1.0.0")

# CORS 允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# 槽位定义（来自PRD的7大槽位）
# ─────────────────────────────────────────────
SLOT_DEFINITIONS = {
    "risk_level": {
        "name": "风险偏好",
        "values": ["保守型", "稳健型", "平衡型", "成长型", "激进型"],
        "description": "用户对投资风险的接受程度",
    },
    "product_type": {
        "name": "产品类型",
        "values": ["纯债", "混合债", "货币基金", "股票基金", "指数基金", "FOF基金"],
        "description": "基金的类型分类",
    },
    "investment_period": {
        "name": "投资期限",
        "values": ["短期(1个月内)", "中期(1-6个月)", "长期(6个月以上)", "不定投"],
        "description": "用户的投资时间预期",
    },
    "investment_goal": {
        "name": "投资目标",
        "values": ["稳健收益", "资产增值", "定期储蓄", "养老规划"],
        "description": "用户的投资目标",
    },
    "industry_theme": {
        "name": "行业主题",
        "values": ["科技", "消费", "医疗", "新能源", "金融", "全市场"],
        "description": "偏好的行业或主题方向",
    },
    "investment_method": {
        "name": "投资方式",
        "values": ["一次性投资", "定投", "都行"],
        "description": "投资方式偏好",
    },
    "purchase_preference": {
        "name": "购买偏好",
        "values": ["低费率", "高收益", "长期稳健", "都行"],
        "description": "购买基金时的偏好",
    },
}


# ─────────────────────────────────────────────
# 数据模型
# ─────────────────────────────────────────────
class UserMessage(BaseModel):
    message: str
    history: list[dict] = []  # 对话历史


class SlotFillResult(BaseModel):
    slots: dict  # 已识别的槽位
    missing_slots: list[str]  # 缺失的槽位
    confidence: float  # 置信度


class Fund(BaseModel):
    fund_code: str
    fund_name: str
    fund_type: str
    risk_level: str
    annualized_return: float
    fee_rate: float
    establishment_date: str
    manager: str
    match_score: float  # 匹配度评分 0-100


class QueryResult(BaseModel):
    funds: list[Fund]
    total: int
    slots_used: dict  # 实际使用的查询槽位


# ─────────────────────────────────────────────
# 模拟基金数据（生产环境应调用真实基金API）
# ─────────────────────────────────────────────
FAKE_FUNDS = [
    {
        "fund_code": "000001",
        "fund_name": "稳盈纯债债券A",
        "fund_type": "纯债",
        "risk_level": "保守型",
        "annualized_return": 4.2,
        "fee_rate": 0.3,
        "establishment_date": "2018-03-15",
        "manager": "张伟",
        "match_score": 95,
    },
    {
        "fund_code": "000002",
        "fund_name": "成长先锋股票A",
        "fund_type": "股票基金",
        "risk_level": "激进型",
        "annualized_return": 12.5,
        "fee_rate": 1.2,
        "establishment_date": "2019-07-22",
        "manager": "李娜",
        "match_score": 88,
    },
    {
        "fund_code": "000003",
        "fund_name": "科技龙头混合A",
        "fund_type": "混合基金",
        "risk_level": "成长型",
        "annualized_return": 18.3,
        "fee_rate": 1.5,
        "establishment_date": "2020-01-10",
        "manager": "王强",
        "match_score": 92,
    },
    {
        "fund_code": "000004",
        "fund_name": "医疗健康优选A",
        "fund_type": "股票基金",
        "risk_level": "平衡型",
        "annualized_return": 9.8,
        "fee_rate": 1.0,
        "establishment_date": "2017-05-18",
        "manager": "刘芳",
        "match_score": 85,
    },
    {
        "fund_code": "000005",
        "fund_name": "新能源革命A",
        "fund_type": "股票基金",
        "risk_level": "激进型",
        "annualized_return": 22.1,
        "fee_rate": 1.5,
        "establishment_date": "2021-03-01",
        "manager": "陈明",
        "match_score": 90,
    },
    {
        "fund_code": "000006",
        "fund_name": "稳稳幸福混合债A",
        "fund_type": "混合债",
        "risk_level": "稳健型",
        "annualized_return": 5.6,
        "fee_rate": 0.6,
        "establishment_date": "2019-11-25",
        "manager": "赵静",
        "match_score": 93,
    },
    {
        "fund_code": "000007",
        "fund_name": "货币通宝A",
        "fund_type": "货币基金",
        "risk_level": "保守型",
        "annualized_return": 2.1,
        "fee_rate": 0.0,
        "establishment_date": "2016-08-30",
        "manager": "孙磊",
        "match_score": 80,
    },
    {
        "fund_code": "000008",
        "fund_name": "养老目标2040",
        "fund_type": "FOF基金",
        "risk_level": "平衡型",
        "annualized_return": 7.5,
        "fee_rate": 0.8,
        "establishment_date": "2020-06-15",
        "manager": "周婷",
        "match_score": 87,
    },
]


# ─────────────────────────────────────────────
# 关键词匹配槽位填充（演示用，生产应接NLU模型）
# ─────────────────────────────────────────────
def extract_slots(text: str) -> tuple[dict, list[str]]:
    """
    简单关键词规则抽取槽位。
    生产环境替换为行内NLU/LLM接口。
    """
    text_lower = text.lower()
    slots = {}
    missing = []

    # 风险偏好
    risk_map = {
        "保守": "保守型", "稳健": "稳健型", "平衡": "平衡型",
        "成长": "成长型", "激进": "激进型", "进取": "激进型",
        "低风险": "保守型", "中等风险": "平衡型", "高风险": "激进型",
    }
    for kw, val in risk_map.items():
        if kw in text_lower:
            slots["risk_level"] = val
            break

    # 产品类型
    type_map = {
        "纯债": "纯债", "债券": "混合债", "货币": "货币基金",
        "股票": "股票基金", "指数": "指数基金", "fof": "FOF基金",
        "养老": "FOF基金", "混合": "混合基金",
    }
    for kw, val in type_map.items():
        if kw in text_lower:
            slots["product_type"] = val
            break

    # 投资期限
    period_map = {
        "一个月": "短期(1个月内)", "3个月": "中期(1-6个月)",
        "半年": "中期(1-6个月)", "一年": "长期(6个月以上)",
        "定投": "定投", "长期": "长期(6个月以上)",
    }
    for kw, val in period_map.items():
        if kw in text_lower:
            slots["investment_period"] = val
            break

    # 投资方式
    if "定投" in text_lower:
        slots["investment_method"] = "定投"
    elif "一次" in text_lower or "一次性" in text_lower:
        slots["investment_method"] = "一次性投资"

    # 行业主题
    theme_map = {
        "科技": "科技", "消费": "消费", "医疗": "医疗",
        "新能源": "新能源", "金融": "金融",
    }
    for kw, val in theme_map.items():
        if kw in text_lower:
            slots["industry_theme"] = val
            break

    # 投资目标
    goal_map = {
        "稳健": "稳健收益", "收益": "稳健收益", "增值": "资产增值",
        "保值": "稳健收益", "养老": "养老规划", "储蓄": "定期储蓄",
    }
    for kw, val in goal_map.items():
        if kw in text_lower:
            slots["investment_goal"] = val
            break

    # 识别缺失槽位
    all_slots = list(SLOT_DEFINITIONS.keys())
    for slot in all_slots:
        if slot not in slots:
            missing.append(slot)

    confidence = len(slots) / len(all_slots) if all_slots else 0

    return slots, missing


def score_fund(fund: dict, slots: dict) -> float:
    """根据槽位计算基金匹配度评分"""
    score = 50  # 基础分

    if "risk_level" in slots and fund["risk_level"] == slots["risk_level"]:
        score += 15
    if "product_type" in slots and fund["fund_type"] == slots["product_type"]:
        score += 15
    if "investment_goal" in slots:
        goal = slots["investment_goal"]
        if goal == "稳健收益" and fund["risk_level"] in ["保守型", "稳健型"]:
            score += 10
        elif goal == "资产增值" and fund["risk_level"] in ["成长型", "激进型"]:
            score += 10
    if "purchase_preference" in slots:
        pref = slots["purchase_preference"]
        if pref == "低费率":
            score += 10 - fund["fee_rate"] * 5
        elif pref == "高收益":
            score += fund["annualized_return"] / 5

    return min(100, max(0, score))


# ─────────────────────────────────────────────
# API 接口
# ─────────────────────────────────────────────

@app.get("/")
async def root():
    return {"message": "LUI Fund Assistant API", "version": "1.0.0"}


@app.get("/slots/definitions")
async def get_slot_definitions():
    """获取槽位定义列表"""
    return SLOT_DEFINITIONS


@app.post("/nlu/extract")
async def extract_slots_api(message: UserMessage):
    """
    意图识别 + 槽位填充接口。
    生产环境：调用行内NLU/LLM服务替换本地规则。
    """
    full_text = message.message

    # 如果有历史，拼接上下文
    for turn in message.history[-3:]:
        full_text += f" {turn.get('user', '')} {turn.get('assistant', '')}"

    slots, missing = extract_slots(full_text)
    confidence = len(slots) / len(SLOT_DEFINITIONS)

    return {
        "slots": slots,
        "missing_slots": missing,
        "confidence": round(confidence, 2),
        "recognized": {SLOT_DEFINITIONS[k]["name"]: v for k, v in slots.items()},
        "pending": [SLOT_DEFINITIONS[k]["name"] for k in missing],
    }


@app.post("/funds/query")
async def query_funds(message: UserMessage):
    """
    基金筛选查询接口。
    先做意图槽位填充，再根据槽位筛选基金。
    """
    full_text = message.message
    for turn in message.history[-3:]:
        full_text += f" {turn.get('user', '')} {turn.get('assistant', '')}"

    slots, _ = extract_slots(full_text)

    if not slots:
        raise HTTPException(
            status_code=400,
            detail="未识别到有效的筛选条件，请描述您的基金需求，如：'我想买稳健型的纯债基金'"
        )

    # 筛选 + 评分
    scored = []
    for fund in FAKE_FUNDS:
        fund_copy = fund.copy()
        fund_copy["match_score"] = score_fund(fund_copy, slots)
        scored.append(fund_copy)

    # 按匹配度排序
    scored.sort(key=lambda x: x["match_score"], reverse=True)

    return {
        "funds": scored[:5],  # 返回TOP5
        "total": len(scored),
        "slots_used": {SLOT_DEFINITIONS[k]["name"]: v for k, v in slots.items()},
    }


@app.get("/funds/{fund_code}")
async def get_fund_detail(fund_code: str):
    """获取单个基金详情"""
    for fund in FAKE_FUNDS:
        if fund["fund_code"] == fund_code:
            return fund
    raise HTTPException(status_code=404, detail="未找到该基金")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# ─────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
