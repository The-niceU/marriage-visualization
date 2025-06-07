<template>
  <div class="container">
    <div ref="chartRef" style="width: 50vw; height: 600px;"></div>
    <div v-if="selectedAreas.length > 0" class="comparison-panel">
      <h3>已选择区域比较</h3>
      <div class="selected-areas">
        <div v-for="(area, index) in selectedAreas" :key="index" class="area-tag">
          {{ area.name }}: {{ area.value.toLocaleString() }}
          <span class="remove-tag" @click="removeSelectedArea(index)">×</span>
        </div>
      </div>
      <div ref="comparisonChartRef" style="width: 100%; height: 300px;" v-if="selectedAreas.length > 0"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import * as echarts from 'echarts';
import Papa from 'papaparse';

const chartRef = ref(null);
const comparisonChartRef = ref(null);
const selectedAreas = ref([]);
let myChart = null;
let comparisonChart = null;

function removeSelectedArea(index) {
  selectedAreas.value.splice(index, 1);
  // 如果选中列表已清空，清除地图的选中状态
  if (selectedAreas.value.length === 0 && myChart) {
    myChart.dispatchAction({
      type: 'unselect',
      seriesIndex: 0
    });
  }
}

// 绘制比较图表
function renderComparisonChart() {
  if (!comparisonChartRef.value || selectedAreas.value.length === 0) return;
  
  if (!comparisonChart) {
    comparisonChart = echarts.init(comparisonChartRef.value);
  }
  
  const option = {
    title: {
      text: '选中区域结婚人口比较',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'category',
      data: selectedAreas.value.map(item => item.name),
      axisLabel: {
        interval: 0,
        rotate: 30
      }
    },
    yAxis: {
      type: 'value',
      name: '人口数量'
    },
    series: [
      {
        name: '结婚人口',
        type: 'bar',
        data: selectedAreas.value.map(item => item.value),
        itemStyle: {
          color: '#007bff'
        },
        label: {
          show: true,
          position: 'top',
          formatter: '{c}'
        }
      }
    ]
  };
  
  comparisonChart.setOption(option);
}

// 监听选中区域变化，更新比较图表
watch(selectedAreas, () => {
  setTimeout(renderComparisonChart, 0);
}, { deep: true });

onMounted(async () => {
  const response = await fetch('/data/marriage.csv');
  const csvText = await response.text();
  const rows = Papa.parse(csvText, { skipEmptyLines: true }).data;

  // 跳过前两行表头，排除空行和"全国"
  const dataRows = rows.slice(2).filter(row => row[0] && row[0].trim() && row[0].trim() !== '全国');

  // 组装地图数据，确保 value 为数字
  const mapData = dataRows.map(row => ({
    name: row[0].trim(),
    value: Number(String(row[1]).replace(/,/g, '').trim())
  })).filter(item => item.name && !isNaN(item.value));

  console.log('mapData:', mapData); // 调试用

  const geoJson = await fetch('/china.json').then(res => res.json());
  echarts.registerMap('china', geoJson);

  myChart = echarts.init(chartRef.value);
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
      min: 0,
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
        selectedMode: 'multiple', // 开启多选模式
        select: {
          itemStyle: {
            areaColor: '#ff9800',
            borderColor: '#000'
          }
        },
        label: {
          show: true,
          formatter: params => `${params.name}\n${params.value ?? ''}`
        },
        data: mapData
      }
    ]
  };

  myChart.setOption(option);
  
  // 监听地图选择变化
  myChart.on('selectchanged', params => {
    if (params.from === 'series') {
      const selectedIndices = params.selected[0].dataIndex || [];
      selectedAreas.value = selectedIndices.map(index => mapData[index]);
    }
  });

  // 监听点击事件，实现点击切换选择状态
  myChart.on('click', params => {
    const clickedItem = mapData.find(item => item.name === params.name);
    if (!clickedItem) return;
    
    const existingIndex = selectedAreas.value.findIndex(item => item.name === params.name);
    
    if (existingIndex >= 0) {
      // 如果已选中，则取消选中
      selectedAreas.value.splice(existingIndex, 1);
    } else {
      // 如果未选中，则添加到选中列表
      selectedAreas.value.push(clickedItem);
    }
    
    // 更新地图选中状态
    const selectedIndices = mapData
      .map((item, index) => selectedAreas.value.some(a => a.name === item.name) ? index : -1)
      .filter(index => index !== -1);
    
    myChart.dispatchAction({
      type: 'select',
      seriesIndex: 0,
      dataIndex: selectedIndices
    });
  });

  // 监听窗口大小变化，调整图表大小
  window.addEventListener('resize', () => {
    myChart.resize();
    if (comparisonChart) {
      comparisonChart.resize();
    }
  });
});
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comparison-panel {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.selected-areas {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 15px;
}

.area-tag {
  background-color: #e1f5fe;
  padding: 5px 10px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  font-size: 14px;
}

.remove-tag {
  margin-left: 5px;
  cursor: pointer;
  font-weight: bold;
  color: #666;
}

.remove-tag:hover {
  color: #f44336;
}
</style>
