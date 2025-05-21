<script setup>
import { ref, onMounted } from 'vue';
import { Chart } from "@antv/g2";   //或者只引入需要用到的G2组件，我要用Chart
import { DataSet } from '@antv/data-set'; //antV中用DataSet作为数据集，可以对原始数据进行操作，比如格式转换之类的，以供图表方法使用，当然也可以不用，不管什么方法只要把数据格式转变成它需要的格式就可以了

const props=defineProps({
  data_path: String,
});

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


const chartDataDouble = ref([      
    { time: "周一", vs: 1234, vk: 124 },
    { time: "周二", vs: 1245, vk: 364 },
    { time: "周三", vs: 1456, vk: 428 },
    { time: "周四", vs: 1526, vk: 523 },
    { time: "周五", vs: 1548, vk: 92 },
    { time: "周六", vs: 1798, vk: 242 },
    { time: "周日", vs: 1723, vk: 131 },
]);


//图表
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

onMounted(async () => {
  await initLineChart();
});


</script>


<template>
<div id="chartDiv"></div>
</template>

<style scoped>
</style>
