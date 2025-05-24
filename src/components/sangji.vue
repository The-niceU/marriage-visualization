<template>
  <div id="main" style="width: 600px; height: 400px;"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import * as echarts from 'echarts';

// props: 传入csv路径
const props = defineProps({
  data_path: {
    type: String,
    required: true
  }
});

const chart = ref(null);

function csvToSankey(csv) {
  // 假设csv格式: source,target,value
  const lines = csv.trim().split('\n');
  const nodesSet = new Set();
  const links = [];
  for (let i = 0; i < lines.length; i++) {
    const [source, target, value] = lines[i].split(',');
    nodesSet.add(source);
    nodesSet.add(target);
    links.push({ source, target, value: Number(value) });
  }
  const nodes = Array.from(nodesSet).map(name => ({ name }));
  return { nodes, links };
}

async function loadDataAndRender() {
  const res = await fetch(props.data_path);
  const csv = await res.text();
  const { nodes, links } = csvToSankey(csv);

  if (!chart.value) {
    chart.value = echarts.init(document.getElementById('main'));
  }
  const option = {
    title: {
      text: 'Sankey Diagram'
    },
    tooltip: {
      trigger: 'item',
      triggerOn: 'mousemove'
    },
    series: [
      {
        type: 'sankey',
        layout: 'none',
        data: nodes,
        links: links,
        emphasis: {
          focus: 'adjacency'
        },
        levels: [
          {
            depth: 0,
            itemStyle: {
              color: '#fbb4ae'
            },
            lineStyle: {
              color: 'source',
              opacity: 0.6
            }
          },
          {
            depth: 1,
            itemStyle: {
              color: '#b3cde3'
            },
            lineStyle: {
              color: 'source',
              opacity: 0.6
            }
          },
          {
            depth: 2,
            itemStyle: {
              color: '#ccebc5'
            },
            lineStyle: {
              color: 'source',
              opacity: 0.6
            }
          },
          {
            depth: 3,
            itemStyle: {
              color: '#decbe4'
            },
            lineStyle: {
              color: 'source',
              opacity: 0.6
            }
          }
        ],
        lineStyle: {
          curveness: 0.5
        }
      }
    ]
  };
  chart.value.setOption(option);
}

onMounted(loadDataAndRender);
watch(() => props.data_path, loadDataAndRender);
</script>