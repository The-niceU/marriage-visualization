<script setup>
import MV from './components/MarriageVisual.vue';
import EchartsChart from './components/EchartsChart.vue';
import ChinaMap from './components/ChinaMap.vue';
</script>


<template>

  <div>
    <h2>婚姻数据可视化</h2>
    <MV data_path="/src/assets/data/marriage.csv"/>
    <EchartsChart />
    <ChinaMap />
  </div>
</template>

<style scoped>
</style>

