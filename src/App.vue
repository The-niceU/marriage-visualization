<script setup>
import MV from './components/MarriageVisual.vue';
import EchartsChart from './components/EchartsChart.vue';
import ChinaMap from './components/ChinaMap.vue';
</script>

<template>
  <div>
    <MV data_path="/src/assets/data/marriage.csv"/>
    <EchartsChart />
    <ChinaMap />
  </div>
</template>

<style scoped>




</style>

