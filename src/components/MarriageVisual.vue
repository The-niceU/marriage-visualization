<script setup>
import { ref, onMounted } from 'vue';
import { Chart } from "@antv/g2";
import { DataSet } from '@antv/data-set';
<<<<<<< HEAD
import * as echarts from 'echarts';
=======
>>>>>>> cf9b8f26705edf91579650bea50a15c66659291f
import Plotly from 'plotly.js-dist';

// 这里可以保留你的 CSV 数据处理逻辑
const props = defineProps({
  data_path: String,
});



// 婚姻率数据
const marriage_data = [
  {year: 2000, marriage_rate: 6.8},
  {year: 2001, marriage_rate: 7.3},
  {year: 2002, marriage_rate: 7.0},
  {year: 2003, marriage_rate: 6.9},
  {year: 2004, marriage_rate: 7.1},
  {year: 2005, marriage_rate: 7.2},
  {year: 2006, marriage_rate: 7.0},
  {year: 2007, marriage_rate: 6.9},
  {year: 2008, marriage_rate: 6.6},
  {year: 2009, marriage_rate: 6.7}
];

// 离婚率数据
const divorce_data = [
  {year: 2000, divorce_rate: 2.8},
  {year: 2001, divorce_rate: 2.9},
  {year: 2002, divorce_rate: 2.7},
  {year: 2003, divorce_rate: 2.8},
  {year: 2004, divorce_rate: 2.9},
  {year: 2005, divorce_rate: 2.7},
  {year: 2006, divorce_rate: 3.0},
  {year: 2007, divorce_rate: 3.1},
  {year: 2008, divorce_rate: 3.1},
  {year: 2009, divorce_rate: 2.8}
];

// 不同国家的结婚率与离婚率对比数据
const countries = ['USA', 'China', 'India', 'UK', 'Germany'];
const marriage_rates = [6.5, 7.0, 5.5, 6.8, 7.3];
const divorce_rates = [3.1, 2.9, 1.5, 2.7, 3.2];

// 中国不同地区的婚姻数据
const regions = ['Beijing', 'Shanghai', 'Guangzhou', 'Chengdu', 'Shenzhen'];
const marriage_data_china = [
  [0.8, 0.6, 0.7, 0.5, 0.6],
  [0.6, 0.7, 0.8, 0.5, 0.6],
  [0.7, 0.6, 0.7, 0.8, 0.6],
  [0.5, 0.6, 0.7, 0.6, 0.7],
  [0.6, 0.7, 0.8, 0.7, 0.6]
];

const chartDataDouble = ref([      
    { time: "周一", vs: 1234, vk: 124 },
    { time: "周二", vs: 1245, vk: 364 },
    { time: "周三", vs: 1456, vk: 428 },
    { time: "周四", vs: 1526, vk: 523 },
    { time: "周五", vs: 1548, vk: 92 },
    { time: "周六", vs: 1798, vk: 242 },
    { time: "周日", vs: 1723, vk: 131 },
]);



async function csvToJson(path) {
  return fetch(path)
    .then(response => response.text())
    .then(data => {
      // 将CSV数据转换为JSON格式
      const rows = data.split('\n');
      const headers = rows[0].split(',');
      return rows.slice(1)
        .filter(row => row.trim()) // 过滤空行
        .map(row => {
          const values = row.split(',');
          for (let i = 0; i < values.length; i++) {
            // 去除每个值的前后空格
            values[i] = values[i].trim();
            // 检查是否是数字
            if (!isNaN(values[i])) {
              // 如果是数字，将其转换为整数
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
      return []; // 出错时返回空数组
    });
}

// 图表初始化函数
onMounted(async () => {
  renderPlotlyCharts();
  await initLineChart();
});


const renderPlotlyCharts = () => {
  if (!window.Plotly) return;
  
  // 婚姻率图表配置
  const marriage_trace = {
    x: marriage_data.map(d => d.year),
    y: marriage_data.map(d => d.marriage_rate),
    type: 'scatter',
    mode: 'lines+markers',
    name: '结婚率',
    marker: { color: '#4CAF50' }
  };

  // 离婚率图表配置
  const divorce_trace = {
    x: divorce_data.map(d => d.year),
    y: divorce_data.map(d => d.divorce_rate),
    type: 'scatter',
    mode: 'lines+markers',
    name: '离婚率',
    marker: { color: '#FF6347' }
  };

  // 不同国家的结婚率与离婚率对比
  const bar_trace = {
    x: countries,
    y: marriage_rates,
    type: 'bar',
    name: '结婚率',
    marker: { color: '#4CAF50' }
  };

  const bar_trace2 = {
    x: countries,
    y: divorce_rates,
    type: 'bar',
    name: '离婚率',
    marker: { color: '#FF6347' }
  };

  // 热力图配置：展示中国不同地区的婚姻数据
  const heatmap_trace = {
    z: marriage_data_china,
    x: regions,
    y: regions,
    type: 'heatmap',
    colorscale: 'Viridis',
    colorbar: { title: '婚姻数据' }
  };

  // 图表布局
  const layout = {
    title: '结婚/离婚数据随年份变化的趋势',
    xaxis: {
      title: '年份',
      showgrid: false
    },
    yaxis: {
      title: '率（每亿人）',
      showgrid: true,
      rangemode: 'tozero'
    },
    plot_bgcolor: '#f4f7f6',
    paper_bgcolor: '#f4f7f6',
  };

  // 渲染各个图表
  window.Plotly.newPlot('chart1', [marriage_trace], layout);
  window.Plotly.newPlot('chart2', [divorce_trace], layout);
  window.Plotly.newPlot('chart3', [bar_trace, bar_trace2], {
    title: '不同国家结婚率与离婚率对比',
    barmode: 'group',
    xaxis: { title: '国家' },
    yaxis: { title: '率（每亿人）' }
  });
  window.Plotly.newPlot('chart4', [heatmap_trace], {
    title: '中国不同地区婚姻数据热力图',
    xaxis: { title: '地区' },
    yaxis: { title: '地区' }
  });
};

const initLineChart = async () => {
  // 读取CSV文件
  const csvData=await csvToJson(props.data_path);
    
    const chart = new Chart({       // 创建一个图表
        container: "chartDiv",      // 容器是上面那个div
        autoFit: true,              // 自适应
        height: 300,             // 高度
        tooltip:{
          showCrosshairs: true,       // 展示 Tooltip 辅助线
          shared: true,
          crosshairs: {
            type: 'line'
          }
        },
      });
    const dataToUse = csvData.length > 0 ? csvData : chartDataDouble.value;
    
    const ds = new DataSet();       // 声明数据集 附官方文档 https://g2.antv.vision/zh/docs/manual/dataset/dataset
    const dv = ds.createView().source(dataToUse);    // 使用上面的数据chartDataDouble创建数据视图dv
    // fold 方式完成了行列转换，如果不想使用 DataSet 直接手工转换数据即可 --官方注释
    
    const fields = csvData.length > 0 ? ['number'] : ['vs', 'vk'];
    const xField = csvData.length > 0 ? 'year' : 'time';
    
    dv.transform({                  // 附transform API https://g2.antv.vision/zh/docs/manual/dataset/transform
        type: 'fold',
        fields: fields,       // 展开字段集
        key: 'type',         // key字段
        value: 'count'       // value字段

    });

    // 以上的数据转换后一条转为两条，eg：
    // { time: "周一", vs: 1234, vk: 124 }, 转换后=>
    // { "time": "周一", "type": "vs", "count": 1234 },{ "time": "周一", "type": "vk", "count": 124 },
    console.log(dv.rows); // 打印转换后的数据
    chart.data(dv.rows);
    chart.options({
        scales: {
            [xField]: {
                range: [0, 1]
            },
            count: {
                min: 0,
                nice: true
            }
        },
        axes: {
            count: {
                label: {
                    formatter: (val) => val
                }
            }
        }
    });            // 现在可以将dv的rows作为数据源

    chart.line()
        .encode('x', xField)
        .encode('y', 'count')
        .encode('color', 'type')
        .encode('shape', 'smooth');
        //.shape('smooth');

    // 使用G2 V5的API绘制点图
    chart.point()
        .encode('x', xField)
        .encode('y', 'count')
        .encode('color', 'type')
        .style({
            size: 4,
            shape: 'circle',
            stroke: '#fff', // 描边
            lineWidth: 1    // 宽度
        });
    chart.render();                 // 这个图表终于要被渲染展示了...
};
</script>

<<<<<<< HEAD
=======
<style scoped>
header {
  text-align: center;
  margin: 20px 0;
  animation: jump 1s ease-in-out;
  animation-iteration-count: infinite; 
}
@keyframes jump {
  0% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0); }
}
</style>
>>>>>>> cf9b8f26705edf91579650bea50a15c66659291f
<template>
  <div>
    <header>
      婚姻数据可视化
    </header>

    <div class="container">
      <!-- 页面简介 -->
      <div class="info-box">
        <h2>关于本数据</h2>
        <p>此页面展示了2000年至2009年期间婚姻率和离婚率的年度变化趋势，以及不同国家之间的结婚率与离婚率对比、中国不同地区的婚姻数据热力图和婚姻诉讼数据的分析。</p>
        <p>通过本页面，您可以深入了解不同地区与国家的婚姻情况，并进行相关的趋势分析。</p>
      </div>
      <div class="section-title">中国历年婚姻登记数量</div>
      <div id="chartDiv"></div>

      <!-- 第一部分：结婚率图表 -->
      <div class="section-title">不同年份的结婚率</div>
      <div id="chart1"></div>

      <!-- 第二部分：离婚率图表 -->
      <div class="section-title">不同年份的离婚率</div>
      <div id="chart2"></div>

      <!-- 第三部分：不同国家的结婚率与离婚率对比 -->
      <div class="section-title">不同国家结婚率与离婚率对比</div>
      <div id="chart3"></div>

      <!-- 第四部分：中国不同地区婚姻数据热力图 -->
      <div class="section-title">中国不同地区婚姻数据热力图</div>
      <div id="chart4"></div>

      <!-- 数据分析 -->
      <div class="info-box">
        <h2>数据分析</h2>
        <p>婚姻率和离婚率在2000年至2009年之间呈现一定的波动。</p>
        <p><strong>婚姻率：</strong>2001年达到最高点7.3，而2009年为最低点6.7。</p>
        <p><strong>离婚率：</strong>2008年是离婚率的高峰期，达到了3.1。</p>
        <p><strong>平均婚姻率：</strong>7.0</p>
        <p><strong>平均离婚率：</strong>2.9</p>
        <p>通过分析不同国家的结婚率和离婚率，我们可以更好地了解不同地区的婚姻状况。</p>
      </div>
      
      
    </div>

    <div class="footer">
      <p>婚姻与离婚数据可视化 | 数据来源于公开统计局</p>
    </div>
  </div>
</template>

<style scoped>
body {
  font-family: 'Roboto', sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f4f7f6;
  color: #333;
  line-height: 1.6;
}

header {
  background-color: #3e8e41;
  color: white;
  padding: 30px;
  text-align: center;
  font-size: 2.5em;
  border-bottom: 5px solid #2c6a32;
}

h1 {
  margin: 0;
}

.container {
  width: 85%;
  margin: 40px auto;
  text-align: center;
}

.section-title {
  color: #3e8e41;
  font-size: 2em;
  margin-top: 30px;
  font-weight: 600;
}

.info-box {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
  margin-top: 30px;
}

.info-box h2 {
  margin-top: 0;
  color: #3e8e41;
  font-size: 1.6em;
}

.info-box p {
  color: #555;
  font-size: 1.1em;
}

#chart1, #chart2, #chart3, #chart4, #chartDiv {
  margin: 30px 0;
  height: 500px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.footer {
  background-color: #3e8e41;
  color: white;
  padding: 15px;
  text-align: center;
  font-size: 1em;
  margin-top: 50px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .container {
    width: 90%;
  }

  #chart1, #chart2, #chart3, #chart4, #chartDiv {
    height: 350px;
  }
}
</style>