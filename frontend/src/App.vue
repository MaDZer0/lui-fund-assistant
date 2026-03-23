<template>
  <div class="app-container">
    <!-- 头部 -->
    <header class="header">
      <h1>💰 LUI基金筛选助手</h1>
      <p class="subtitle">描述您的需求，AI帮您找到合适的基金</p>
    </header>

    <!-- 槽位状态卡片 -->
    <div class="slot-card">
      <div class="slot-header">
        <span class="slot-title">📋 筛选条件</span>
        <span class="slot-count">{{ filledSlotsCount }}/{{ totalSlots }} 已识别</span>
      </div>
      <div class="slots-grid">
        <div
          v-for="slot in slotDefinitions"
          :key="slot.key"
          class="slot-item"
          :class="{ filled: slots[slot.key], missing: !slots[slot.key] }"
        >
          <span class="slot-name">{{ slot.name }}</span>
          <span class="slot-value">{{ slots[slot.key] || '待补充' }}</span>
        </div>
      </div>
    </div>

    <!-- 快捷chips -->
    <div class="chips-section">
      <div
        v-for="group in quickChips"
        :key="group.label"
        class="chip-group"
      >
        <span class="chip-label">{{ group.label }}</span>
        <div class="chips">
          <button
            v-for="chip in group.items"
            :key="chip.value"
            class="chip"
            :class="{ active: isChipActive(group.key, chip.value) }"
            @click="toggleChip(group.key, chip.value)"
          >
            {{ chip.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- 对话区域 -->
    <div class="chat-container" ref="chatContainer">
      <!-- 欢迎语 -->
      <div v-if="messages.length === 0" class="welcome">
        <p>👋 您好！请描述您的基金投资需求，</p>
        <p>例如：<em>"我想买稳健型的纯债基金，三个月左右"</em></p>
      </div>

      <!-- 消息列表 -->
      <div
        v-for="(msg, idx) in messages"
        :key="idx"
        class="message"
        :class="msg.role"
      >
        <div class="message-bubble">
          <div v-if="msg.type === 'slots'" class="slot-update">
            <p class="update-title">🎯 已识别您的需求：</p>
            <div class="update-slots">
              <span
                v-for="(val, key) in msg.slots"
                :key="key"
                class="update-slot-tag filled"
              >{{ val }}</span>
              <span
                v-for="name in msg.missing"
                :key="'m-' + name"
                class="update-slot-tag missing"
              >? {{ name }}</span>
            </div>
          </div>
          <div v-else-if="msg.type === 'funds'" class="fund-result">
            <p class="result-title">📊 为您找到 {{ msg.funds.length }} 只匹配基金：</p>
            <div class="fund-list">
              <div
                v-for="fund in msg.funds"
                :key="fund.fund_code"
                class="fund-item"
                @click="showFundDetail(fund)"
              >
                <div class="fund-main">
                  <span class="fund-name">{{ fund.fund_name }}</span>
                  <span class="fund-type">{{ fund.fund_type }}</span>
                </div>
                <div class="fund-meta">
                  <span class="fund-score">匹配度 {{ fund.match_score }}%</span>
                  <span class="fund-return">年化收益 {{ fund.annualized_return }}%</span>
                </div>
              </div>
            </div>
          </div>
          <div v-else-if="msg.type === 'error'" class="error-msg">
            {{ msg.text }}
          </div>
          <div v-else>
            {{ msg.text }}
          </div>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="message assistant">
        <div class="message-bubble loading">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="input-area">
      <input
        v-model="inputText"
        class="input"
        placeholder="输入您的基金需求，例如：稳健型纯债基金..."
        @keyup.enter="sendMessage"
        :disabled="loading"
      />
      <button class="send-btn" @click="sendMessage" :disabled="loading || !inputText.trim()">
        {{ loading ? '...' : '发送' }}
      </button>
    </div>

    <!-- 基金详情弹窗 -->
    <div v-if="selectedFund" class="modal-overlay" @click.self="selectedFund = null">
      <div class="modal">
        <button class="modal-close" @click="selectedFund = null">✕</button>
        <h3>{{ selectedFund.fund_name }}</h3>
        <div class="modal-info">
          <div class="info-row">
            <span>基金代码</span><span>{{ selectedFund.fund_code }}</span>
          </div>
          <div class="info-row">
            <span>基金类型</span><span>{{ selectedFund.fund_type }}</span>
          </div>
          <div class="info-row">
            <span>风险等级</span><span>{{ selectedFund.risk_level }}</span>
          </div>
          <div class="info-row">
            <span>年化收益</span><span class="highlight">{{ selectedFund.annualized_return }}%</span>
          </div>
          <div class="info-row">
            <span>费率</span><span>{{ selectedFund.fee_rate }}%</span>
          </div>
          <div class="info-row">
            <span>成立日期</span><span>{{ selectedFund.establishment_date }}</span>
          </div>
          <div class="info-row">
            <span>基金经理</span><span>{{ selectedFund.manager }}</span>
          </div>
          <div class="info-row">
            <span>匹配度</span><span class="highlight">{{ selectedFund.match_score }}%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, nextTick } from 'vue'
import axios from 'axios'

const API_BASE = '/api'

// ─── 状态 ───────────────────────────────
const inputText = ref('')
const loading = ref(false)
const messages = ref([])
const selectedFund = ref(null)
const slots = reactive({})
const chatContainer = ref(null)

// ─── 槽位定义 ───────────────────────────────
const slotDefinitions = [
  { key: 'risk_level', name: '风险偏好' },
  { key: 'product_type', name: '产品类型' },
  { key: 'investment_period', name: '投资期限' },
  { key: 'investment_goal', name: '投资目标' },
  { key: 'industry_theme', name: '行业主题' },
  { key: 'investment_method', name: '投资方式' },
  { key: 'purchase_preference', name: '购买偏好' },
]
const totalSlots = computed(() => slotDefinitions.length)
const filledSlotsCount = computed(() => Object.keys(slots).filter(k => slots[k]).length)

// ─── 快捷chips ───────────────────────────────
const quickChips = [
  {
    label: '💼 风险偏好',
    key: 'risk_level',
    items: [
      { label: '保守型', value: '保守型' },
      { label: '稳健型', value: '稳健型' },
      { label: '平衡型', value: '平衡型' },
      { label: '成长型', value: '成长型' },
      { label: '激进型', value: '激进型' },
    ],
  },
  {
    label: '📦 产品类型',
    key: 'product_type',
    items: [
      { label: '纯债', value: '纯债' },
      { label: '混合债', value: '混合债' },
      { label: '货币基金', value: '货币基金' },
      { label: '股票基金', value: '股票基金' },
      { label: '指数基金', value: '指数基金' },
    ],
  },
  {
    label: '⏱️ 投资期限',
    key: 'investment_period',
    items: [
      { label: '1个月内', value: '短期(1个月内)' },
      { label: '1-6个月', value: '中期(1-6个月)' },
      { label: '6个月以上', value: '长期(6个月以上)' },
      { label: '定投', value: '定投' },
    ],
  },
  {
    label: '🎯 投资目标',
    key: 'investment_goal',
    items: [
      { label: '稳健收益', value: '稳健收益' },
      { label: '资产增值', value: '资产增值' },
      { label: '定期储蓄', value: '定期储蓄' },
      { label: '养老规划', value: '养老规划' },
    ],
  },
]

const isChipActive = (key, value) => slots[key] === value

const toggleChip = (key, value) => {
  if (slots[key] === value) {
    delete slots[key]
  } else {
    slots[key] = value
  }
}

// ─── 发送消息 ───────────────────────────────
const sendMessage = async () => {
  const text = inputText.value.trim()
  if (!text || loading.value) return

  // 用户消息
  messages.value.push({ role: 'user', type: 'text', text })
  inputText.value = ''
  loading.value = true
  scrollToBottom()

  try {
    // 1. 意图识别 + 槽位填充
    const history = messages.value
      .filter(m => m.type === 'text')
      .map(m => ({ user: m.role === 'user' ? m.text : '', assistant: m.role === 'assistant' ? m.text : '' }))

    const extractRes = await axios.post(`${API_BASE}/nlu/extract`, {
      message: text,
      history,
    })

    // 更新本地槽位状态
    const newSlots = extractRes.data.slots
    Object.assign(slots, newSlots)

    // 显示槽位识别结果
    messages.value.push({
      role: 'assistant',
      type: 'slots',
      slots: extractRes.data.recognized,
      missing: extractRes.data.pending,
    })
    scrollToBottom()

    // 2. 如果有足够的槽位，自动查询基金
    if (Object.keys(newSlots).length >= 2) {
      const queryRes = await axios.post(`${API_BASE}/funds/query`, {
        message: text,
        history,
      })

      messages.value.push({
        role: 'assistant',
        type: 'funds',
        funds: queryRes.data.funds,
      })
    } else {
      // 追问缺失槽位
      const missingNames = extractRes.data.pending
      if (missingNames.length > 0) {
        const question = `还需要了解您的 [${missingNames.slice(0, 2).join('、')}]，请问您有什么偏好？`
        messages.value.push({ role: 'assistant', type: 'text', text: question })
      }
    }
  } catch (err) {
    messages.value.push({
      role: 'assistant',
      type: 'error',
      text: '抱歉，服务出了点问题，请稍后重试。',
    })
  } finally {
    loading.value = false
    scrollToBottom()
  }
}

// ─── 基金详情 ───────────────────────────────
const showFundDetail = (fund) => {
  selectedFund.value = fund
}

// ─── 工具 ───────────────────────────────
const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}
</script>

<style scoped>
/* ── 布局 ── */
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 600px;
  margin: 0 auto;
  background: #f5f7fa;
  font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', sans-serif;
}

/* ── 头部 ── */
.header {
  background: linear-gradient(135deg, #1a73e8, #0d47a1);
  color: white;
  padding: 20px 16px 16px;
  text-align: center;
}
.header h1 { margin: 0; font-size: 18px; font-weight: 600; }
.subtitle { margin: 4px 0 0; font-size: 12px; opacity: 0.85; }

/* ── 槽位状态卡 ── */
.slot-card {
  background: white;
  margin: 12px;
  border-radius: 12px;
  padding: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.slot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.slot-title { font-size: 13px; font-weight: 600; color: #333; }
.slot-count { font-size: 11px; color: #1a73e8; font-weight: 500; }
.slots-grid { display: flex; flex-wrap: wrap; gap: 6px; }
.slot-item {
  display: flex;
  flex-direction: column;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 11px;
  min-width: 70px;
  border: 1px solid #e0e0e0;
  background: #fafafa;
}
.slot-item.filled {
  background: #e8f0fe;
  border-color: #1a73e8;
  color: #1a73e8;
}
.slot-item.missing { color: #999; }
.slot-name { font-size: 10px; opacity: 0.7; }
.slot-value { font-weight: 600; }

/* ── Chips ── */
.chips-section {
  background: white;
  margin: 0 12px 12px;
  border-radius: 12px;
  padding: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.chip-group { margin-bottom: 8px; }
.chip-group:last-child { margin-bottom: 0; }
.chip-label { font-size: 12px; color: #666; margin-bottom: 6px; display: block; }
.chips { display: flex; flex-wrap: wrap; gap: 6px; }
.chip {
  padding: 4px 10px;
  border-radius: 20px;
  border: 1px solid #ddd;
  background: white;
  font-size: 12px;
  cursor: pointer;
  color: #555;
  transition: all 0.2s;
}
.chip:hover { border-color: #1a73e8; color: #1a73e8; }
.chip.active { background: #1a73e8; color: white; border-color: #1a73e8; }

/* ── 对话区 ── */
.chat-container {
  flex: 1;
  overflow-y: auto;
  padding: 0 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.welcome {
  text-align: center;
  color: #888;
  font-size: 13px;
  padding: 30px 0;
}
.welcome em { color: #1a73e8; }

.message { display: flex; }
.message.user { justify-content: flex-end; }
.message.assistant { justify-content: flex-start; }

.message-bubble {
  max-width: 80%;
  padding: 10px 14px;
  border-radius: 14px;
  font-size: 14px;
  line-height: 1.5;
  word-break: break-word;
}
.message.user .message-bubble {
  background: #1a73e8;
  color: white;
  border-bottom-right-radius: 4px;
}
.message.assistant .message-bubble {
  background: white;
  color: #333;
  border-bottom-left-radius: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

/* ── 槽位更新 ── */
.slot-update .update-title { margin-bottom: 8px; font-size: 13px; }
.update-slots { display: flex; flex-wrap: wrap; gap: 5px; }
.update-slot-tag {
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 12px;
}
.update-slot-tag.filled { background: #e8f0fe; color: #1a73e8; }
.update-slot-tag.missing { background: #fff3e0; color: #e65100; }

/* ── 基金结果 ── */
.fund-result .result-title { margin-bottom: 10px; font-size: 13px; font-weight: 600; }
.fund-list { display: flex; flex-direction: column; gap: 8px; }
.fund-item {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 10px 12px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}
.fund-item:hover { background: #e8f0fe; border-color: #1a73e8; }
.fund-main { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }
.fund-name { font-size: 13px; font-weight: 600; color: #333; }
.fund-type { font-size: 11px; background: #e8f0fe; color: #1a73e8; padding: 2px 6px; border-radius: 4px; }
.fund-meta { display: flex; gap: 10px; font-size: 11px; color: #888; }
.fund-score { color: #1a73e8; font-weight: 600; }
.fund-return { color: #e53935; }

/* ── 加载动画 ── */
.loading { display: flex; gap: 4px; padding: 12px 16px; align-items: center; }
.dot {
  width: 6px; height: 6px; background: #bbb; border-radius: 50%;
  animation: bounce 1.2s infinite;
}
.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}

/* ── 输入区 ── */
.input-area {
  display: flex;
  gap: 8px;
  padding: 12px;
  background: white;
  border-top: 1px solid #eee;
}
.input {
  flex: 1;
  padding: 10px 14px;
  border-radius: 24px;
  border: 1px solid #ddd;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}
.input:focus { border-color: #1a73e8; }
.send-btn {
  padding: 10px 20px;
  border-radius: 24px;
  border: none;
  background: #1a73e8;
  color: white;
  font-size: 14px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s;
}
.send-btn:hover:not(:disabled) { background: #1557b0; }
.send-btn:disabled { background: #ccc; cursor: not-allowed; }

/* ── 弹窗 ── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 16px;
}
.modal {
  background: white;
  border-radius: 16px;
  padding: 24px;
  width: 100%;
  max-width: 400px;
  position: relative;
}
.modal h3 { margin: 0 0 16px; font-size: 16px; color: #333; }
.modal-close {
  position: absolute;
  top: 12px;
  right: 12px;
  border: none;
  background: #f0f0f0;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 14px;
}
.modal-info { display: flex; flex-direction: column; gap: 10px; }
.info-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}
.info-row span:first-child { color: #888; }
.info-row span:last-child { font-weight: 600; color: #333; }
.info-row .highlight { color: #e53935; font-size: 15px; }
</style>
