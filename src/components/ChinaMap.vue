<template>
  <div ref="chartRef" style="width: 100%; height: 600px;"></div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';
import Papa from 'papaparse';

const chartRef = ref(null);

onMounted(async () => {
  const response = await fetch('/data/marriage.csv');
  const csvText = await response.text();
  const rows = Papa.parse(csvText, { skipEmptyLines: true }).data;

  // 跳过前两行表头，排除空行和“全国”
  const dataRows = rows.slice(2).filter(row => row[0] && row[0].trim() && row[0].trim() !== '全国');

  // 组装地图数据，确保 value 为数字
  const mapData = dataRows.map(row => ({
    name: row[0].trim(),
    value: Number(String(row[1]).replace(/,/g, '').trim())
  })).filter(item => item.name && !isNaN(item.value));

  console.log('mapData:', mapData); // 调试用

  const geoJson = await fetch('/china.json').then(res => res.json());
  echarts.registerMap('china', geoJson);

  const myChart = echarts.init(chartRef.value);
  const option = {
    title: {
      text: '各省15岁及以上结婚人口分布',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: params => {
        if (params.value && !isNaN(params.value)) {
          return `${params.name}<br/>15岁及以上结婚人口：${params.value}`;
        } else {
          return `${params.name}<br/>无数据`;
        }
      }
    },
    visualMap: {
      min: Math.min(...mapData.map(d => d.value)),
      max: Math.max(...mapData.map(d => d.value)),
      left: 'left',
      top: 'bottom',
      text: ['高','低'],
      inRange: {
        color: ['#e0ffff', '#006edd']
      },
      show: true
    },
    series: [
      {
        name: '15岁及以上人口',
        type: 'map',
        map: 'china',
        roam: true,
        label: {
          show: true,
          formatter: params => `${params.name}\n${params.value ?? ''}`
        },
        data: mapData
      }
    ]
  };

  myChart.setOption(option);
});
</script>