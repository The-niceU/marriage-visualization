<script setup>
import { ref } from 'vue';

import MV from './components/MarriageVisual.vue';
import EchartsChart from './components/EchartsChart.vue';
import ChinaMap from './components/ChinaMap.vue';
import LineMap from './components/LineMap.vue';
import LineMap2 from './components/LineMap2.vue';
import divorce_marriage from './components/divorce_marriage.vue';
import bubble from './components/bubble.vue';
import sangji from './components/sangji.vue';

const activePage = ref(0); // 当前活动页面
const bubble_show = ref(true); // 控制气泡图的显示与隐藏

const first_page = ref(true); // 用于控制首页的加载状态
// 页面切换函数
const changePage = (pageNum) => {
  activePage.value = pageNum;
};
</script>
<style scoped>
.first-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: transparent;
  font-family: 'Arial', sans-serif;
  font-size: 1.2rem;
  width: 100vw;
  overflow: hidden; 
  cursor: pointer; /* 鼠标悬停时显示手型 */
}


.day {
    position: fixed;
    z-index: 0;
    width: 100vw;
    left: 0;
    top: 0;
    height: 100vh;
    height: 100vh;
    background: radial-gradient(circle at top right, rgba(255, 255, 224, 0.6), rgba(255, 255, 224, 0) 50%), linear-gradient(to bottom, #87CEEB, #87CEEB 30%, #FFFFFF 70%, #FFFFFF 100%);

  }

  .cloud {
    position: absolute;
    background: #ffffff;
    border-radius: 50%;
    box-shadow: 0 0 20px 20px #ffffff;
    opacity: 0.8;
    animation: float-c 10s linear infinite;
    z-index: 0;
  }
  .cloud1 {
    width: 250px;
    height: 70px;
    top: 20%;
    left: -250px;
    animation-delay: 0s;
  }
  
  .cloud2 {
    width: 150px;
    height: 50px;
    top: 40%;
    left: -150px;
    animation-delay: 4s;
  }
  
  @keyframes float-c {
    0% {
        transform: translateX(0);
    }
    100% {
        transform: translateX(130vw);
    }
  }

  @keyframes drift {
    from { background-position: 0 0, 0 200px; }
    to { background-position: 100% 0, 100% 200px; }
  }

.night{
    position: fixed;
    z-index: -100;
    width: 100vw;
    height: 100vh;
    background: linear-gradient(45deg, #767574, #794545, #1f1120, #151805);

}

.star {
    position: absolute;
    width: 2px;
    height: 2px;
    background: white;
    border-radius: 50%;
    animation: twinkle 2s infinite ease-in-out;
  }
  @keyframes twinkle {
    0%, 100% {
        opacity: 0.2;
    }
    50% {
        opacity: 1;
    }
  }
  
  .star:nth-child(1) { top: 10%; left: 20%; animation-delay: 0s; }
          .star:nth-child(2) { top: 30%; left: 40%; animation-delay: 0.5s; }
          .star:nth-child(3) { top: 50%; left: 60%; animation-delay: 1s; }
          .star:nth-child(4) { top: 70%; left: 80%; animation-delay: 1.5s; }
          .star:nth-child(5) { top: 20%; left: 70%; animation-delay: 2s; }
          .star:nth-child(6) { top: 40%; left: 30%; animation-delay: 2.5s; }
          .star:nth-child(7) { top: 60%; left: 50%; animation-delay: 3s; }
          .star:nth-child(8) { top: 80%; left: 10%; animation-delay: 3.5s; }
          .star:nth-child(9) { top: 15%; left: 25%; animation-delay: 4s; }
          .star:nth-child(10) { top: 35%; left: 45%; animation-delay: 4.5s; }
          .star:nth-child(11) { top: 55%; left: 65%; animation-delay: 5s; }
          .star:nth-child(12) { top: 75%; left: 85%; animation-delay: 5.5s; }
          .star:nth-child(13) { top: 25%; left: 75%; animation-delay: 6s; }
          .star:nth-child(14) { top: 45%; left: 35%; animation-delay: 6.5s; }
  


  .line{
    transform-origin: center top;
    position: fixed;
    top: 0;
    right: 4vw;
    height: 60vh;
    width: 0.5vw;
    background-color: #000;
    z-index: 1000;
    cursor: pointer; /* 添加指针，表示可点击 */
    transition: height 1s ease; /* 平滑过渡效果 */
    animation: roll 1.5s infinite alternate; 
    border-radius: 50%; /* 圆角效果 */
    box-shadow: 
      0 0 5px rgba(0, 0, 0, 0.5), /* 阴影效果 */
      inset 0 0 5px rgba(255, 255, 255, 0.3); /* 内部阴影效果 */
  }
  .line::after{
    content: '';
    background-image: url('http://q2.qlogo.cn/headimg_dl?dst_uin=2041584846&spec=100');
    background-size: cover; /* 确保背景图片覆盖整个伪元素 */
    
    position: absolute;
    transition: 1s ease; /* 平滑过渡效果 */
    bottom: -2.5vw;
    right: -2.5vw;
    width: 5vw;
    height: 5vw;
    border-radius: 50%;
    border: 2px solid black;
    box-shadow: 0 0 5vh rgba(0, 0, 0, 0.5), inset 0 0 5px rgba(255, 255, 255, 0.3);
    animation: flowShadow 1s linear infinite;
  }

 


  .line.collapsed{
    height: 10vh;
  }
  @keyframes roll {
    0%  {
  
      transform:  rotate(-3deg);
  
      
    }
    100% {
  
      transform:  rotate(16deg);
  
      
    }
  }
  
  @keyframes flowShadow{
    0%, 100% {
      border-color: #4B0082; /* 深紫色 */
      box-shadow: 0 0 10px #4B0082, 0 0 20px #4B0082, 0 0 30px #4B0082; /* 深紫色阴影 */
    }
    50% {
      border-color: #8A2BE2; /* 亮紫色 */
      box-shadow: 0 0 10px #8A2BE2, 0 0 20px #8A2BE2, 0 0 30px #8A2BE2; /* 亮紫色阴影 */
    }
  }
  


</style>
<template>
  <div class="day" id="back">
      <div class="cloud cloud1" id="c1"></div>
      <div class="cloud cloud2" id="c2"></div>
      <div class="star"></div>
      <div class="star"></div>
      <div class="star"></div>
      <div class="star"></div>
      <div class="star"></div>
      <div class="star"></div>
      <div class="star"></div>
      <div class="star"></div>
      <div class="star"></div>
      <div class="star"></div>
      <div class="star"></div>
      <div class="star"></div>
      <div class="star"></div>
  </div>

   

 <div class="first-page" v-if="first_page" @click="first_page = false">
    <bubble data_path="/src/assets/data/province-marriage-divorce.csv" />
  </div>

  <div class="dashboard" v-if="!first_page">

    <!-- 主要内容区域 -->
    <main class="dashboard-content">
      <!-- 悬浮式导航栏 -->
      <div class="floating-nav-container">
        <div class="logo-section">
          <div class="logo">婚姻数据可视化平台</div>
          <div class="nav-underline"></div>
        </div>
        
        <nav class="floating-nav">
          <button :class="['nav-item', { active: activePage === 0 }]" @click="changePage(0)">
            <span class="nav-icon">📊</span>
            <span class="nav-text">首页</span>
          </button>
          <button :class="['nav-item', { active: activePage === 1 }]" @click="changePage(1)">
            <span class="nav-icon">🗺️</span>
            <span class="nav-text">全国概览</span>
          </button>
          <button :class="['nav-item', { active: activePage === 2 }]" @click="changePage(2)">
            <span class="nav-icon">📈</span>
            <span class="nav-text">趋势分析</span>
          </button>
          <button :class="['nav-item', { active: activePage === 3 }]" @click="changePage(3)">
            <span class="nav-icon">🔄</span>
            <span class="nav-text">关系图谱</span>
          </button>
          <button :class="['nav-item', { active: activePage === 4 }]" @click="changePage(4)">
            <span class="nav-icon">📊</span>
            <span class="nav-text">数据综合分析</span>
          </button>
          
          <button class="control-btn" @click="bubble_show = !bubble_show">
            {{ bubble_show ? '隐藏气泡图' : '显示气泡图' }}
          </button>
        </nav>
      </div>

      <section v-show="activePage === 0" class="page-content">
        <div class="card" v-show="bubble_show">
            <h3 class="card-title">气泡图</h3>
            <bubble data_path="/src/assets/data/province-marriage-divorce.csv" />
        </div>
      </section>

      <!-- 页面1: 全国概览 -->
      <section v-show="activePage === 1" class="page-content">
        
          <div class="card">
            <h3 class="card-title">全国分布</h3>
            <ChinaMap />
          </div>
      </section>

      <!-- 页面2: 趋势分析 -->
      <section v-show="activePage === 2" class="page-content">
   
     
            <h3 class="card-title">婚姻离婚对比</h3>
            <divorce_marriage data_path="/src/assets/data/divorce_marriage.csv" />
     
          
         
            <h3 class="card-title">离婚趋势</h3>
            <LineMap data_path="/src/assets/data/divorce.csv" />
        
          
         
            <h3 class="card-title">结婚趋势</h3>
            <LineMap2 data_path="/src/assets/data/marriage2.csv" />
        
          
    
      </section>

      <!-- 页面3: 关系图谱 -->
      <section v-show="activePage === 3" class="page-content">
   
          <div class="card">
            <h3 class="card-title">婚姻关系图谱</h3>
            <sangji data_path="/src/assets/data/sankey.csv" />
          </div>
          <div class="card">
            <h3 class="card-title">数据综合分析</h3>
            <EchartsChart />
          </div>
   
      </section>

      <!-- 页面4: 数据综合分析 -->
      <section v-show="activePage === 4" class="page-content">
  
          <MV data_path="/src/assets/data/marriage.csv" />
    
      </section>
    </main>

    <!-- 页脚信息 -->
    <footer class="dashboard-footer">
      <p>数据来源：国家统计局</p>
      <p>作者：张三</p>
      <p>联系邮箱：</p>
    </footer>
  </div>
</template>

<style scoped>
:root {
  --primary-color: #00a8ff;
  --secondary-color: #0097e6;
  --accent-color: #00d2d3;
  --background-dark: #1e272e;
  --background-light: #2f3640;
  --text-color: #f5f6fa;
  --border-radius: 8px;
  --card-shadow: 0 4px 25px rgba(0, 0, 0, 0.3);
  --neon-glow: 0 0 10px rgba(0, 168, 255, 0.5), 0 0 20px rgba(0, 168, 255, 0.3);
}

.dashboard {
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(135deg, var(--background-dark), var(--background-light));
  color: var(--text-color);
  font-family: 'Roboto', sans-serif;
  display: flex;
  flex-direction: column;
}

/* 顶部导航栏 */
.dashboard-content {
  flex: 1;
  padding: 0;
  overflow: hidden;
  position: relative;
}

/* 主内容区域 */
.dashboard-content {
  flex: 1;
  padding: 2rem;
  overflow: auto;
}

.page-content {
  animation: fadeIn 0.5s ease-in-out;
}

.grid-layout {
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.card {
  background-color: rgba(124, 180, 223, 0.8);
  border-radius: var(--border-radius);
  border: 1px solid rgba(28, 23, 23, 0.1);
  padding: 1.5rem;
  box-shadow: var(--card-shadow);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  height: 100%;
  width: 100%;
  
  position: relative;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
  border-color: var(--primary-color);
}

.large-card {
  grid-column: span 2;
  height: 500px;
}

.map-card {
  grid-column: span 2;
}

.card-title {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: var(--primary-color);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 0.5rem;
}

/* 页脚 */
.dashboard-footer {
  background-color: rgba(0, 0, 0, 0.3);
  padding: 1rem 2rem;
  text-align: center;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.6);
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

/* 动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}



/* 浮动导航容器 */
.floating-nav-container {
  position: relative;
  padding: 1.5rem 2rem 0.5rem;
  margin-bottom: 1rem;
  z-index: 10;
  background: linear-gradient(to bottom, 
    rgba(30, 39, 46, 0.95) 0%, 
    rgba(30, 39, 46, 0.8) 60%, 
    rgba(30, 39, 46, 0) 100%);
  backdrop-filter: blur(10px);
}

.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1.5rem;
}

.logo {
  font-size: 2rem;
  font-weight: bold;
  color: var(--primary-color);
  text-shadow: 0 0 10px rgba(0, 168, 255, 0.7);
  margin-bottom: 0.5rem;
}

.nav-underline {
  height: 2px;
  width: 150px;
  background: linear-gradient(90deg, transparent, var(--primary-color), transparent);
  margin-top: 0.5rem;
}

/* 浮动导航 */
.floating-nav {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  padding-bottom: 1rem;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.75rem 1.25rem;
  background-color: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--border-radius);
  color: var(--text-color);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.nav-icon {
  font-size: 1.5rem;
  margin-bottom: 0.25rem;
}

.nav-text {
  font-size: 0.9rem;
}

.nav-item:hover {
  background-color: rgba(0, 168, 255, 0.15);
  transform: translateY(-3px);
  box-shadow: var(--neon-glow);
}

.nav-item.active {
  background-color: rgba(0, 168, 255, 0.3);
  border-color: var(--primary-color);
  color: white;
  box-shadow: var(--neon-glow);
}

.control-btn {
  margin-left: auto;
  padding: 0.5rem 1rem;
  background-color: var(--accent-color);
  border: none;
  border-radius: var(--border-radius);
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

/* 页面内容调整 */
.page-content {
  padding: 0 2rem 2rem;
  animation: fadeIn 0.5s ease-in-out;
}

</style>