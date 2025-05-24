<template>
  <div ref="lineChartRef" style="width: 100%; height: 400px;"></div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';

// 默认示例数据：不同年份结婚率
const marriageData = [
  { year: 2000, marriage_rate: 6.8 },
  { year: 2001, marriage_rate: 7.3 },
  { year: 2002, marriage_rate: 7.0 },
  { year: 2003, marriage_rate: 6.9 },
  { year: 2004, marriage_rate: 7.1 },
  { year: 2005, marriage_rate: 7.2 },
  { year: 2006, marriage_rate: 7.0 },
  { year: 2007, marriage_rate: 6.9 },
  { year: 2008, marriage_rate: 6.6 },
  { year: 2009, marriage_rate: 6.7 }
];

const lineChartRef = ref(null);

const props = defineProps({
  data_path: String
});

onMounted(async () => {
  let data = [];
  if (props.data_path) {
    data = await csvToJson(props.data_path);
  }
  if (!data || data.length === 0) {
    data = marriageData;
  }
  // 自动适配表头
  const yearKey = Object.keys(data[0])[0]; // 例如 'year' 或 'year(年)'
  const valueKey = Object.keys(data[0])[1]; // 例如 'marriage_rate' 或 '数据(单位：‰)'

  const chart = echarts.init(lineChartRef.value);
  const option = {
    title: {
      text: '不同年份结婚率变化'
    },
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item[yearKey])
    },
    yAxis: {
      type: 'value',
      name: '结婚率'
    },
    dataZoom: [
      {
        type: 'slider',
        start: 0,
        end: 100
      }
    ],
    series: [
      {
        name: '结婚率',
        type: 'line',
        smooth: true,
        data: data.map(item => item[valueKey]),
        lineStyle: {
          color: '#4CAF50'
        },
        itemStyle: {
          color: '#4CAF50'
        }
      }
    ]
  };
  chart.setOption(option);
});

async function csvToJson(path) {
  return fetch(path)
    .then(response => response.text())
    .then(data => {
      const rows = data.split('\n');
      const headers = rows[0].split(',');
      return rows.slice(1)
        .filter(row => row.trim())
        .map(row => {
          const values = row.split(',');
          for (let i = 0; i < values.length; i++) {
            values[i] = values[i].trim();
            if (!isNaN(values[i])) {
              values[i] = parseFloat(values[i]);
            }
          }
          return headers.reduce((obj, header, index) => {
            obj[header] = values[index];
            return obj;
          }, {});
        });
    })
    .catch(error => {
      console.error('Error fetching CSV:', error);
      return [];
    });
}
</script>