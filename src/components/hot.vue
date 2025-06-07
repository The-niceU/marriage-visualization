<template>
  <div id="main" style="width: 100%; height: 600px;"></div>
</template>

<script setup>
import { onMounted } from 'vue'
import * as echarts from 'echarts'

// 年份和月份
const years = Array.from({ length: 2024 - 1978 + 1 }, (_, i) => (1978 + i).toString())
const months = Array.from({ length: 12 }, (_, i) => (i + 1).toString())

// 读取CSV并渲染
onMounted(async () => {
  // 读取CSV
  const res = await fetch('/src/assets/data/birthrate.csv')
  const text = await res.text()
  const lines = text.trim().split('\n')
  const data = []

  // 跳过表头
  for (let i = 1; i < lines.length; i++) {
    const [year, month, birthrate] = lines[i].split(',')
    const yearIdx = years.indexOf(year)
    const monthIdx = months.indexOf(month)
    if (yearIdx !== -1 && monthIdx !== -1) {
      data.push([yearIdx, monthIdx, parseFloat(birthrate)])
    }
  }

  // 渲染ECharts
  const chartDom = document.getElementById('main')
  const myChart = echarts.init(chartDom)
  const option = {
    tooltip: {
      position: 'top',
      formatter: params => `${years[params.data[0]]}年${months[params.data[1]]}月<br/>出生率: ${params.data[2]}`
    },
    grid: {
      height: '60%',
      top: '10%'
    },
    xAxis: {
      type: 'category',
      data: years,
      splitArea: { show: true },
      name: '年份'
    },
    yAxis: {
      type: 'category',
      data: months,
      splitArea: { show: true },
      name: '月份'
    },
    visualMap: {
      min: 0,
      max: 25, // 根据实际出生率调整
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '15%'
    },
    series: [
      {
        name: '出生率',
        type: 'heatmap',
        data: data,
        label: { show: false },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  myChart.setOption(option)
})
</script>