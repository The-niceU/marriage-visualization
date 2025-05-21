<template>
  <div ref="lineChartRef" style="width: 100%; height: 400px;"></div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';

// 示例数据：不同年份离婚率
const divorceData = [
  { year: 2000, divorce_rate: 2.8 },
  { year: 2001, divorce_rate: 2.9 },
  { year: 2002, divorce_rate: 2.7 },
  { year: 2003, divorce_rate: 2.8 },
  { year: 2004, divorce_rate: 2.9 },
  { year: 2005, divorce_rate: 2.7 },
  { year: 2006, divorce_rate: 3.0 },
  { year: 2007, divorce_rate: 3.1 },
  { year: 2008, divorce_rate: 3.1 },
  { year: 2009, divorce_rate: 2.8 }
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
    data = divorceData;
  }
  // 自动适配表头
  const yearKey = Object.keys(data[0])[0]; // 例如 'year' 或 'year(年)'
  const valueKey = Object.keys(data[0])[1]; // 例如 'divorce_rate' 或 '数据(单位：‰)'

  const chart = echarts.init(lineChartRef.value);
  const option = {
    title: {
      text: '不同年份离婚率变化'
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
      name: '离婚率'
    },
    series: [
      {
        name: '离婚率',
        type: 'line',
        smooth: true,
        data: data.map(item => item[valueKey]),
        lineStyle: {
          color: '#FF6347'
        },
        itemStyle: {
          color: '#FF6347'
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