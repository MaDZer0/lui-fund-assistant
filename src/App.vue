<template>
  <main class="page">
    <FundCardConfigurable
      name="招商瑞智优选LOF"
      code="161728"
      yearly-return="65.93%"
      max-drawdown="9.79%"
      sharpe-ratio="3.24"
      button-text="查看详情"
    />
  </main>
</template>

<script setup>
import FundCardConfigurable from './components/FundCardConfigurable.vue'
</script>

<style scoped>
.page {
  min-height: 100vh;
  padding: 36px 20px;
  box-sizing: border-box;
  background: linear-gradient(180deg, #efefed 0%, #e8e8e6 100%);
}
</style>
