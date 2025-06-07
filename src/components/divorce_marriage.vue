<template>
  <div ref="chartRef" style="width: 40vw; height: 600px;"></div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import Papa from 'papaparse'

const chartRef = ref(null)

onMounted(async () => {
  // 假设你的csv表头为：year,marriage,divorce
    const response = await fetch('/src/assets/data/divorce_marriage.csv')
  const csvText = await response.text()
  const rows = Papa.parse(csvText, { header: true, skipEmptyLines: true }).data

  const yearData = rows.map(row => row.year)
  const marriageData = rows.map(row => Number(row.marriage))
  const divorceData = rows.map(row => Number(row.divorce))

  const option = {
    title: {
      text: '历年结婚率与离婚率对比',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { animation: false }
    },
    legend: {
      data: ['结婚率', '离婚率'],
      left: 10
    },
    toolbox: {
      feature: {
        dataZoom: { yAxisIndex: 'none' },
        restore: {},
        saveAsImage: {}
      }
    },
    axisPointer: {
      link: [{ xAxisIndex: 'all' }]
    },
    dataZoom: [
      { show: true, realtime: true, start: 0, end: 100, xAxisIndex: [0, 1] },
      { type: 'inside', realtime: true, start: 0, end: 100, xAxisIndex: [0, 1] }
    ],
    grid: [
      { left: 60, right: 50, height: '45%' },
      { left: 60, right: 50, top: '60%', height: '35%' }
    ],
    xAxis: [
      {
        type: 'category',
        boundaryGap: false,
        axisLine: { onZero: true },
        data: yearData
      },
      {
        gridIndex: 1,
        type: 'category',
        boundaryGap: false,
        axisLine: { onZero: true },
        data: yearData,
        position: 'top'
      }
    ],
    yAxis: [
      {
        name: '结婚率(‰)',
        type: 'value'
      },
      {
        gridIndex: 1,
        name: '离婚率(‰)',
        type: 'value',
        inverse: true
      }
    ],
    series: [
      {
        name: '结婚率',
        type: 'line',
        symbolSize: 8,
        data: marriageData
      },
      {
        name: '离婚率',
        type: 'line',
        xAxisIndex: 1,
        yAxisIndex: 1,
        symbolSize: 8,
        data: divorceData
      }
    ]
  }

  const chart = echarts.init(chartRef.value)
  chart.setOption(option)
})
</script>