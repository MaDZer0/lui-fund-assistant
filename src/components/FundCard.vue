<template>
  <div class="fund-card">
    <div class="fund-header">
      <div class="fund-icon">
        <span class="icon-chart">📈</span>
      </div>
      <div class="fund-info">
        <h2>招商瑞智优选LOF</h2>
        <p>161728</p>
      </div>
    </div>

    <div class="metrics">
      <div class="metric-box">
        <div class="metric-icon">📊</div>
        <div class="metric-content">
          <span class="metric-label">近一年收益</span>
          <span class="metric-value">65.93%</span>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-icon">📉</div>
        <div class="metric-content">
          <span class="metric-label">最大回撤</span>
          <span class="metric-value">9.79%</span>
        </div>
      </div>

      <div class="metric-box light">
        <div class="metric-icon">⚖️</div>
        <div class="metric-content">
          <span class="metric-label">夏普比例</span>
          <span class="metric-value">3.24</span>
        </div>
      </div>
    </div>

    <button class="detail-btn">查看详情</button>
  </div>
</template>

<script setup>
</script>

<style scoped>
.fund-card {
  width: 100%;
  max-width: 980px;
  margin: 32px auto;
  padding: 42px 40px 34px;
  background: #f7f7f5;
  border-radius: 28px;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
  box-sizing: border-box;
}

.fund-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 34px;
}

.fund-icon {
  width: 72px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 18px;
  background: linear-gradient(180deg, #ffffff, #eef3fb);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.9);
  font-size: 34px;
}

.fund-info h2 {
  margin: 0;
  font-size: 32px;
  line-height: 1.2;
  color: #1f2430;
  font-weight: 700;
}

.fund-info p {
  margin: 8px 0 0;
  font-size: 22px;
  color: #5f6573;
}

.metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 38px;
}

.metric-box {
  min-height: 132px;
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 24px 24px;
  border-radius: 18px;
  background: linear-gradient(135deg, #0e4d8a, #245f9e);
  color: #e8c08b;
  box-shadow: 0 10px 18px rgba(16, 62, 120, 0.22);
}

.metric-box.light {
  background: linear-gradient(135deg, #2d6fae, #5f9edd);
}

.metric-icon {
  font-size: 38px;
  width: 48px;
  text-align: center;
}

.metric-content {
  display: flex;
  flex-direction: column;
}

.metric-label {
  font-size: 18px;
  margin-bottom: 10px;
  color: #f3d6ae;
}

.metric-value {
  font-size: 26px;
  font-weight: 700;
  color: #f1c282;
}

.detail-btn {
  display: block;
  width: 470px;
  max-width: 100%;
  margin: 0 auto;
  height: 76px;
  border: none;
  border-radius: 999px;
  background: linear-gradient(180deg, #0d58a6, #0a4594);
  color: #ffffff;
  font-size: 34px;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 10px 18px rgba(12, 79, 155, 0.24);
}

.detail-btn:hover {
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .fund-card {
    padding: 28px 20px 24px;
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
