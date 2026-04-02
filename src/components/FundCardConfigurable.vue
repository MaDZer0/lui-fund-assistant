<template>
  <div class="fund-card">
    <div class="fund-header">
      <div class="fund-icon" aria-hidden="true">
        <svg viewBox="0 0 80 80" class="main-icon">
          <defs>
            <linearGradient id="cardIconBg" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#1e5f9e" />
              <stop offset="100%" stop-color="#5c90c4" />
            </linearGradient>
            <linearGradient id="coinFill" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#f6d18b" />
              <stop offset="100%" stop-color="#d7a24a" />
            </linearGradient>
          </defs>
          <path d="M12 56 L30 38 L41 46 L58 24" fill="none" stroke="url(#cardIconBg)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" />
          <path d="M50 24 H58 V32" fill="none" stroke="url(#cardIconBg)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" />
          <rect x="16" y="42" width="8" height="20" rx="2" fill="#5a6b89" />
          <rect x="29" y="34" width="8" height="28" rx="2" fill="#6a7b97" />
          <rect x="42" y="26" width="8" height="36" rx="2" fill="#7b8ca6" />
          <circle cx="58" cy="54" r="12" fill="url(#coinFill)" />
          <path d="M58 47 V61" stroke="#8f672a" stroke-width="3" stroke-linecap="round" />
          <path d="M62 50.5C61.1 49.5 59.8 49 58 49C55.4 49 54 50.2 54 52C54 53.7 55.5 54.6 58 55.1C60.5 55.6 62 56.4 62 58.2C62 60 60.3 61.2 57.9 61.2C56.1 61.2 54.6 60.6 53.4 59.4" fill="none" stroke="#8f672a" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </div>
      <div class="fund-info">
        <h2>{{ name }}</h2>
        <p>{{ code }}</p>
      </div>
    </div>

    <div class="metrics">
      <div class="metric-box">
        <div class="metric-icon" aria-hidden="true">
          <svg viewBox="0 0 64 64">
            <path d="M10 50H54" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" />
            <rect x="14" y="33" width="8" height="17" rx="2" fill="currentColor" opacity="0.75" />
            <rect x="28" y="24" width="8" height="26" rx="2" fill="currentColor" opacity="0.85" />
            <rect x="42" y="14" width="8" height="36" rx="2" fill="currentColor" />
            <path d="M14 26 L28 18 L36 24 L50 10" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M43 10 H50 V17" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </div>
        <div class="metric-content">
          <span class="metric-label">近一年收益</span>
          <span class="metric-value">{{ yearlyReturn }}</span>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-icon" aria-hidden="true">
          <svg viewBox="0 0 64 64">
            <path d="M10 50H54" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" />
            <rect x="14" y="18" width="8" height="32" rx="2" fill="currentColor" opacity="0.95" />
            <rect x="28" y="28" width="8" height="22" rx="2" fill="currentColor" opacity="0.85" />
            <rect x="42" y="37" width="8" height="13" rx="2" fill="currentColor" opacity="0.7" />
            <path d="M14 14 L28 24 L38 20 L50 31" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M43 31 H50 V24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </div>
        <div class="metric-content">
          <span class="metric-label">最大回撤</span>
          <span class="metric-value">{{ maxDrawdown }}</span>
        </div>
      </div>

      <div class="metric-box light">
        <div class="metric-icon" aria-hidden="true">
          <svg viewBox="0 0 64 64">
            <path d="M32 11V50" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" />
            <path d="M18 18H46" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" />
            <path d="M14 21 L22 34 L6 34 Z" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linejoin="round" />
            <path d="M42 21 L50 34 L34 34 Z" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linejoin="round" />
            <path d="M22 48H42" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" />
            <circle cx="11" cy="12" r="2" fill="currentColor" opacity="0.8" />
            <circle cx="53" cy="14" r="2" fill="currentColor" opacity="0.8" />
            <circle cx="48" cy="8" r="1.8" fill="currentColor" opacity="0.55" />
          </svg>
        </div>
        <div class="metric-content">
          <span class="metric-label">夏普比例</span>
          <span class="metric-value">{{ sharpeRatio }}</span>
        </div>
      </div>
    </div>

    <button class="detail-btn" type="button">{{ buttonText }}</button>
  </div>
</template>

<script setup>
defineProps({
  name: {
    type: String,
    default: '招商瑞智优选LOF'
  },
  code: {
    type: String,
    default: '161728'
  },
  yearlyReturn: {
    type: String,
    default: '65.93%'
  },
  maxDrawdown: {
    type: String,
    default: '9.79%'
  },
  sharpeRatio: {
    type: String,
    default: '3.24'
  },
  buttonText: {
    type: String,
    default: '查看详情'
  }
})
</script>

<style scoped>
.fund-card {
  width: 100%;
  max-width: 1080px;
  margin: 32px auto;
  padding: 42px 40px 34px;
  background: linear-gradient(180deg, #f8f8f6 0%, #f3f3f1 100%);
  border-radius: 28px;
  box-shadow: 0 18px 34px rgba(18, 35, 61, 0.08);
  box-sizing: border-box;
}

.fund-header {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-bottom: 34px;
}

.fund-icon {
  width: 82px;
  height: 82px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-icon {
  width: 100%;
  height: 100%;
}

.fund-info h2 {
  margin: 0;
  font-size: 32px;
  line-height: 1.18;
  color: #1d2433;
  font-weight: 700;
}

.fund-info p {
  margin: 8px 0 0;
  font-size: 22px;
  line-height: 1;
  color: #646d79;
}

.metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 22px;
  margin-bottom: 38px;
}

.metric-box {
  min-height: 132px;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 22px 22px;
  border-radius: 18px;
  background: linear-gradient(135deg, #0d4d89 0%, #2b669f 100%);
  color: #e5b980;
  box-shadow: 0 12px 20px rgba(16, 62, 120, 0.24);
}

.metric-box.light {
  background: linear-gradient(135deg, #2869a9 0%, #6fa8de 100%);
}

.metric-icon {
  width: 52px;
  height: 52px;
  color: #e5b980;
  flex-shrink: 0;
}

.metric-icon svg {
  width: 100%;
  height: 100%;
}

.metric-content {
  display: flex;
  flex-direction: column;
}

.metric-label {
  font-size: 18px;
  line-height: 1.2;
  margin-bottom: 10px;
  color: #f4d5ad;
}

.metric-value {
  font-size: 26px;
  line-height: 1.1;
  font-weight: 700;
  color: #f0bf7b;
}

.detail-btn {
  display: block;
  width: 470px;
  max-width: 100%;
  margin: 0 auto;
  height: 76px;
  border: none;
  border-radius: 999px;
  background: linear-gradient(180deg, #095aa9 0%, #084895 100%);
  color: #ffffff;
  font-size: 34px;
  font-weight: 500;
  letter-spacing: 1px;
  cursor: pointer;
  box-shadow: 0 12px 20px rgba(12, 79, 155, 0.22);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.detail-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 15px 24px rgba(12, 79, 155, 0.26);
}

@media (max-width: 768px) {
  .fund-card {
    padding: 28px 20px 24px;
    border-radius: 24px;
  }

  .fund-icon {
    width: 66px;
    height: 66px;
  }

  .fund-info h2 {
    font-size: 24px;
  }

  .fund-info p {
    font-size: 18px;
  }

  .metrics {
    grid-template-columns: 1fr;
  }

  .detail-btn {
    height: 62px;
    font-size: 26px;
  }
}
</style>
