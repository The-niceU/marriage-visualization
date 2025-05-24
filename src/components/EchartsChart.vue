<template>
  <div ref="chartRef" style="width: 100%; height: 400px;"></div>
</template>

<script>
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';
import Papa from 'papaparse';

export default {
  setup() {
    const chartRef = ref(null);
    const chartData = ref({ years: [], values: [] });

    // 解析 CSV 文件
    const loadCSVData = async () => {
      const response = await fetch('/data/marriage.csv');
      const csvText = await response.text();

      Papa.parse(csvText, {
        header: true,
        skipEmptyLines: true,
        complete: (result) => {
          chartData.value.years = result.data.map(row => row.年份);
          chartData.value.values = result.data.map(row => Number(row.结婚人数));

          // 初始化 ECharts
          if (chartRef.value) {
          const myChart = echarts.init(chartRef.value, 'macarons');
            
            const option = {
              title: {
                text: '婚姻数据趋势',
              },
              tooltip: {},
              xAxis: {
                type: 'category',
                data: chartData.value.years,
              },
              yAxis: {
                type: 'value',
              },
              series: [
                {
                  data: chartData.value.values,
                  type: 'line',
                },
              ],
            };
            myChart.setOption(option);
          }
        },
      });
    };

    onMounted(() => {
      loadCSVData();
    });

    return {
      chartRef,
    };
  },
};
</script>
