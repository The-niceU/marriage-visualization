<script setup>
import MV from './components/MarriageVisual.vue';
import EchartsChart from './components/EchartsChart.vue';
import ChinaMap from './components/ChinaMap.vue';
<<<<<<< HEAD
import LineMap from './components/LineMap.vue'; 
import LineMap2 from './components/LineMap2.vue'; // 这里是你新添加的组件
</script>


<template>

  <div>
    <h2>婚姻数据可视化</h2>
    <LineMap2 data_path="/src/assets/data/marriage2.csv"/>
    <LineMap data_path="/src/assets/data/divorce.csv" /> 
    <MV data_path="/src/assets/data/marriage.csv"/>
    <EchartsChart />

=======
</script>

<template>
  <div>
    <MV data_path="/src/assets/data/marriage.csv"/>
    <EchartsChart />
>>>>>>> cf9b8f26705edf91579650bea50a15c66659291f
    <ChinaMap />
  </div>
</template>

<style scoped>
<<<<<<< HEAD
</style>
=======




</style>

>>>>>>> cf9b8f26705edf91579650bea50a15c66659291f
