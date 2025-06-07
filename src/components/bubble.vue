<template>
  <div ref="chartRef" style="width: 100%; height: 600px;cursor:pointer "></div>
</template>



<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import Papa from 'papaparse'

const chartRef = ref(null)

onMounted(async () => {
  // 1. 读取csv
  const response = await fetch('/src/assets/data/merged.csv')
  const csvText = await response.text()
  const rows = Papa.parse(csvText, { header: true, skipEmptyLines: true }).data

  // 2. 整理数据结构
  const timeline = [...new Set(rows.map(row => row.year))].sort()
  const provinces = [...new Set(rows.map(row => row.province))]
  // 每年一个二维数组：[收入, 结婚/离婚率比值, 人数, 省份]
  const series = timeline.map(year =>
    rows
      .filter(row => row.year === year)
      .map(row => [
        Number(row.income),
        Number(row.divorce_rate),
        Number(row.population),
        row.province
      ])
  )

  const itemStyle = { opacity: 0.8 }
  const sizeFunction = x => (Math.sqrt(x / 10000) + 0.1) * 50
  const schema = [
    { name: 'Income', index: 0, text: '人均收入', unit: '元' },
    { name: 'Ratio', index: 1, text: '粗离婚率', unit: '%' },
    { name: 'Population', index: 2, text: '人数', unit: '万人' },
    { name: 'Province', index: 3, text: '省份', unit: '' }
  ]

  const option = {
    baseOption: {
      timeline: {
        axisType: 'category',
        orient: 'vertical',
        autoPlay: true,
        inverse: true,
        playInterval: 1200,
        right: 0,
        top: 20,
        bottom: 20,
        width: 55,
        symbol: 'none',
        checkpointStyle: { borderWidth: 2 },
        controlStyle: { showNextBtn: false, showPrevBtn: false },
        data: timeline
      },
      title: [
        {
          text: timeline[0],
          textAlign: 'center',
          left: '63%',
          top: '55%',
          textStyle: { fontSize: 80 }
        },
        {
          text: '各省粗离婚率与人均收入关系',
          left: 'center',
          top: 10,
          textStyle: { fontWeight: 'normal', fontSize: 20 }
        }
      ],
      tooltip: {
        padding: 5,
        borderWidth: 1,
        formatter: obj => {
          const value = obj.value
          return (
            schema[3].text + '：' + value[3] + '<br>' +
            schema[1].text + '：' + value[1].toFixed(2) + '<br>' +
            schema[0].text + '：' + value[0] + schema[0].unit + '<br>' +
            schema[2].text + '：' + value[2]
          )
        }
      },
      grid: {
        top: 100,
        containLabel: true,
        left: 30,
        right: '110'
      },
      xAxis: {
        type: 'value',
        name: '人均收入',
        nameGap: 25,
        nameLocation: 'middle',
        nameTextStyle: { fontSize: 18 },
        splitLine: { show: false },
        axisLabel: { formatter: '{value} 元' }
      },
      yAxis: {
        type: 'value',
        name: '粗离婚率',
        nameTextStyle: { fontSize: 18 },
        splitLine: { show: false }
      },
      visualMap: [
        {
          show: true,
          dimension: 3,
          categories: provinces,
          inRange: {
            color: [
              '#51689b', '#ce5c5c', '#fbc357', '#8fbf8f', '#659d84',
              '#fb8e6a', '#c77288', '#786090', '#91c4c5', '#6890ba',
              '#e09f9f', '#b0d87b', '#f6c85f', '#6fa3ef', '#d998cb',
              '#7f7f7f', '#c7c7c7', '#bcbd22', '#17becf', '#aec7e8',
              '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5', '#c49c94',
              '#f7b6d2', '#dbdb8d', '#9edae5', '#393b79', '#637939',
              '#8c6d31', '#843c39'
            ]
          }
        }
      ],
      series: [
        {
          type: 'scatter',
          itemStyle: itemStyle,
          data: series[0],
          symbolSize: val => sizeFunction(val[2])
        }
      ],
      animationDurationUpdate: 1000,
      animationEasingUpdate: 'quinticInOut'
    },
    options: series.map((seriesData, idx) => ({
      title: { show: true, text: timeline[idx] + '' },
      series: {
        name: timeline[idx],
        type: 'scatter',
        itemStyle: itemStyle,
        data: seriesData,
        symbolSize: val => sizeFunction(val[2])
      }
    }))
  }

  const chart = echarts.init(chartRef.value)
  chart.setOption(option)
})
</script>

