<script setup>
import MV from './components/MarriageVisual.vue';
import EchartsChart from './components/EchartsChart.vue';
import ChinaMap from './components/ChinaMap.vue';
import LineMap from './components/LineMap.vue'; 
import LineMap2 from './components/LineMap2.vue';
import sangji from './components/sangji.vue'; // 这里是你新添加的组件
</script>


<template>

  <div>
    <h2>婚姻数据可视化</h2>
    <LineMap2 data_path="/src/assets/data/marriage2.csv"/>
    <LineMap data_path="/src/assets/data/divorce.csv" /> 
    <MV data_path="/src/assets/data/marriage.csv"/>
    <sangji data_path="/src/assets/data/sankey.csv" />
    <EchartsChart />

    <ChinaMap />
  </div>
</template>

<style scoped>




</style>

