<script setup>
import MV from './components/MarriageVisual.vue';
import EchartsChart from './components/EchartsChart.vue';
import ChinaMap from './components/ChinaMap.vue';
import LineMap from './components/LineMap.vue';
import LineMap2 from './components/LineMap2.vue';
import divorce_marriage from './components/divorce_marriage.vue';
import bubble from './components/bubble.vue';
import sangji from './components/sangji.vue'; // 这里是你新添加的组件
</script>

<template>
  <div>
    <bubble data_path="/src/assets/data/province-marriage-divorce.csv" />
    <divorce_marriage data_path="/src/assets/data/divorce_marriage.csv" />
    <LineMap data_path="/src/assets/data/divorce.csv" />
    <LineMap2 data_path="/src/assets/data/marriage2.csv" />
    <MV data_path="/src/assets/data/marriage.csv" />
    <sangji data_path="/src/assets/data/sankey.csv" />
    <EchartsChart />
    <ChinaMap />
  </div>
</template>

<style scoped>




</style>

