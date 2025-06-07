<script setup>
import { ref, onMounted } from 'vue';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import * as TWEEN from '@tweenjs/tween.js';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

// 注册GSAP插件
gsap.registerPlugin(ScrollTrigger);

// 保留原有组件导入
import MV from './components/MarriageVisual.vue';
import EchartsChart from './components/EchartsChart.vue';
import ChinaMap from './components/ChinaMap.vue';
import LineMap from './components/LineMap.vue';
import LineMap2 from './components/LineMap2.vue';
import divorce_marriage from './components/divorce_marriage.vue';
import bubble from './components/bubble.vue';
import sangji from './components/sangji.vue';

// 状态管理
const activePage = ref(0);
const sceneReady = ref(false);
const loading = ref(true);
const bubble_show = ref(true);
const first_page = ref(true);

// 3D场景相关变量
let scene, camera, renderer, controls;
let particleSystem, dataPoints = [];
let raycaster, mouse, hoveredObject;

// 页面切换函数 - 使用GSAP动画
const changePage = (pageNum) => {
  // 页面切换动画
  gsap.to('.page-content', {
    opacity: 0,
    scale: 0.9,
    duration: 0.5,
    onComplete: () => {
      activePage.value = pageNum;
      
      // 激活新页面动画
      gsap.to('.page-content', {
        opacity: 1,
        scale: 1,
        duration: 0.8,
        delay: 0.1,
        ease: "power3.out"
      });
      
      // 数据可视化相关的3D动画
      animateDataTransition(pageNum);
    }
  });
};

// 入口门户点击处理函数
const enterDataverse = () => {
  // 创建过渡动画
  gsap.to('.portal-core', {
    scale: 10,
    opacity: 0.9,
    duration: 1.5,
    ease: 'power2.in'
  });
  
  gsap.to('.portal-ring', {
    scale: 2,
    opacity: 0,
    duration: 1,
    stagger: 0.1,
    ease: 'power2.in'
  });
  
  gsap.to('.portal-title, .portal-subtitle', {
    opacity: 0,
    y: -50,
    duration: 0.8,
    ease: 'power2.in'
  });
  
  // 等待动画完成后切换到主界面
  setTimeout(() => {
    first_page.value = false;
    
    // 进入主界面后的动画效果
    gsap.fromTo('.nav-system', 
      { y: -100, opacity: 0 },
      { y: 0, opacity: 1, duration: 1, ease: 'back.out(1.7)' }
    );
    
    gsap.fromTo('.page-content', 
      { scale: 0.8, opacity: 0 },
      { scale: 1, opacity: 1, duration: 1.2, delay: 0.3, ease: 'power3.out' }
    );
    
    // 触发粒子爆炸效果
    setTimeout(() => {
      explodeParticles();
    }, 800);
  }, 1800);
};

// 3D数据转场动画
// 3D数据转场动画
const animateDataTransition = (pageNum) => {
  // 先等待DOM更新完成
  setTimeout(() => {
    // 基于页码的3D效果
    switch(pageNum) {
      case 0:
        // 首页粒子爆炸效果
        explodeParticles();
        break;
      case 1:
        // 中国地图3D升起效果
        
        break;
      case 2:
        // 趋势线转化为3D曲面
        convertTo3DSurface();
        break;
      case 3:
        // 关系图谱展开
        expandRelationships();
        break;
      case 4:
        // 综合数据漩涡效果
        createDataVortex();
        break;
    }
  }, 500); // 给DOM更新足够的时间
};

// 初始化3D场景
const initThreeJS = () => {
  // 创建场景
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0a1a);
  
  // 添加大气雾气效果
  scene.fog = new THREE.FogExp2(0x0a0a1a, 0.0015);
  
  // 相机设置
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 50;
  
  // 渲染器设置
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.shadowMap.enabled = true;
  
  // 添加到DOM
  document.getElementById('three-container').appendChild(renderer.domElement);
  
  // 添加控制器
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  
  // 光源设置
  addLights();
  
  // 添加基础粒子系统
  createParticleSystem();
  
  // 添加交互射线
  raycaster = new THREE.Raycaster();
  mouse = new THREE.Vector2();
  
  // 事件监听
  window.addEventListener('resize', onWindowResize);
  window.addEventListener('mousemove', onMouseMove);
  
  // 开始动画循环
  animate();
  
  // 2秒后显示界面
  setTimeout(() => {
    loading.value = false;
    sceneReady.value = true;
    
    // 入场动画
    gsap.to(camera.position, {
      z: 30,
      duration: 2,
      ease: "power2.out"
    });
  }, 2000);
};

// 创建数据驱动的粒子系统
const createParticleSystem = () => {
  const particles = new THREE.BufferGeometry();
  const particleCount = 5000;
  
  const positions = new Float32Array(particleCount * 3);
  const colors = new Float32Array(particleCount * 3);
  const sizes = new Float32Array(particleCount);
  
  const color = new THREE.Color();
  
  for (let i = 0; i < particleCount; i++) {
    // 分布在球体上
    const radius = 40 * Math.random();
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.random() * Math.PI;
    
    positions[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
    positions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
    positions[i * 3 + 2] = radius * Math.cos(phi);
    
    // 基于位置设置颜色
    const colorIndex = Math.floor((radius / 40) * 5);
    switch(colorIndex) {
      case 0: color.setHSL(0.65, 1, 0.5); break; // 蓝色
      case 1: color.setHSL(0.55, 1, 0.5); break; // 青色
      case 2: color.setHSL(0.2, 1, 0.5); break;  // 绿色
      case 3: color.setHSL(0.1, 1, 0.5); break;  // 黄色
      case 4: color.setHSL(0.95, 1, 0.5); break; // 紫色
    }
    
    colors[i * 3] = color.r;
    colors[i * 3 + 1] = color.g;
    colors[i * 3 + 2] = color.b;
    
    sizes[i] = Math.random() * 2 + 1;
  }
  
  particles.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  particles.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  particles.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
  
  // 粒子材质
  const particleMaterial = new THREE.ShaderMaterial({
    uniforms: {
      time: { value: 0.0 },
      pointTexture: { value: new THREE.TextureLoader().load('/src/assets/textures/particle.png') }
    },
    vertexShader: `
      attribute float size;
      varying vec3 vColor;
      uniform float time;
      
      void main() {
        vColor = color;
        vec3 pos = position;
        
        // 添加波动效果
        float waveFactor = sin(time * 0.5 + position.x * 0.1 + position.y * 0.1 + position.z * 0.1) * 0.5 + 0.5;
        
        vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
        gl_PointSize = size * (300.0 / -mvPosition.z) * (0.8 + waveFactor * 0.4);
        gl_Position = projectionMatrix * mvPosition;
      }
    `,
    fragmentShader: `
      uniform sampler2D pointTexture;
      varying vec3 vColor;
      
      void main() {
        gl_FragColor = vec4(vColor, 1.0) * texture2D(pointTexture, gl_PointCoord);
        if (gl_FragColor.a < 0.3) discard;
      }
    `,
    blending: THREE.AdditiveBlending,
    depthTest: false,
    transparent: true,
    vertexColors: true
  });
  
  particleSystem = new THREE.Points(particles, particleMaterial);
  scene.add(particleSystem);
};

// 添加光源
const addLights = () => {
  // 环境光
  const ambientLight = new THREE.AmbientLight(0x333366, 0.5);
  scene.add(ambientLight);
  
  // 主光源
  const mainLight = new THREE.DirectionalLight(0xffffff, 1);
  mainLight.position.set(10, 10, 10);
  mainLight.castShadow = true;
  scene.add(mainLight);
  
  // 点光源1
  const pointLight1 = new THREE.PointLight(0x00ffff, 1, 100);
  pointLight1.position.set(20, -20, 20);
  scene.add(pointLight1);
  
  // 点光源2
  const pointLight2 = new THREE.PointLight(0xff00ff, 1, 100);
  pointLight2.position.set(-20, 20, 20);
  scene.add(pointLight2);
  
  // 光源动画
  gsap.to(pointLight1.position, {
    x: -20,
    y: 20,
    z: -20,
    duration: 20,
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut"
  });
  
  gsap.to(pointLight2.position, {
    x: 20,
    y: -20,
    z: -20,
    duration: 25,
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut"
  });
};

// 窗口调整
const onWindowResize = () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
};

// 鼠标移动交互
const onMouseMove = (event) => {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
};

// 动画循环
const animate = () => {
  requestAnimationFrame(animate);
  
  // 更新控制器
  controls.update();
  
  // 更新着色器时间
  if (particleSystem) {
    particleSystem.material.uniforms.time.value += 0.01;
  }
  
  // 旋转粒子系统
  if (particleSystem) {
    particleSystem.rotation.y += 0.001;
    particleSystem.rotation.x += 0.0005;
  }
  
  // 更新TWEEN
  TWEEN.update();
  
  // 处理射线相交
  handleRaycaster();
  
  // 渲染场景
  renderer.render(scene, camera);
};

// 射线检测
const handleRaycaster = () => {
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(dataPoints);
  
  if (intersects.length > 0) {
    if (hoveredObject !== intersects[0].object) {
      if (hoveredObject) {
        gsap.to(hoveredObject.scale, { x: 1, y: 1, z: 1, duration: 0.3 });
      }
      hoveredObject = intersects[0].object;
      gsap.to(hoveredObject.scale, { x: 1.2, y: 1.2, z: 1.2, duration: 0.3 });
      
      // 显示数据提示
      showDataTooltip(hoveredObject.userData);
    }
  } else {
    if (hoveredObject) {
      gsap.to(hoveredObject.scale, { x: 1, y: 1, z: 1, duration: 0.3 });
      hoveredObject = null;
      
      // 隐藏提示
      hideDataTooltip();
    }
  }
};

// 显示数据提示
const showDataTooltip = (data) => {
  const tooltip = document.getElementById('data-tooltip');
  tooltip.innerHTML = `
    <h3>${data.title}</h3>
    <p>${data.description}</p>
    <div class="tooltip-value">${data.value}</div>
  `;
  tooltip.style.display = 'block';
  
  // 跟随鼠标
  document.addEventListener('mousemove', moveTooltip);
};

// 移动提示框
const moveTooltip = (event) => {
  const tooltip = document.getElementById('data-tooltip');
  tooltip.style.left = `${event.clientX + 20}px`;
  tooltip.style.top = `${event.clientY + 20}px`;
};

// 隐藏提示框
const hideDataTooltip = () => {
  const tooltip = document.getElementById('data-tooltip');
  tooltip.style.display = 'none';
  document.removeEventListener('mousemove', moveTooltip);
};

// 特效动画
const explodeParticles = () => {
  if (!particleSystem) return;
  
  const positions = particleSystem.geometry.attributes.position.array;
  const originalPositions = positions.slice();
  
  for (let i = 0; i < positions.length; i += 3) {
    const x = originalPositions[i];
    const y = originalPositions[i + 1];
    const z = originalPositions[i + 2];
    
    const targetX = x * 2;
    const targetY = y * 2;
    const targetZ = z * 2;
    
    gsap.to(positions, {
      [i]: targetX,
      [i + 1]: targetY,
      [i + 2]: targetZ,
      duration: 2,
      ease: "power3.out",
      onUpdate: () => {
        particleSystem.geometry.attributes.position.needsUpdate = true;
      },
      onComplete: () => {
        gsap.to(positions, {
          [i]: x,
          [i + 1]: y,
          [i + 2]: z,
          duration: 3,
          ease: "elastic.out(1, 0.3)",
          onUpdate: () => {
            particleSystem.geometry.attributes.position.needsUpdate = true;
          }
        });
      }
    });
  }
  console.log('0 finished explodeParticles');
};

// 中国地图3D升起效果
// 中国地图3D升起效果
const elevateMap = () => {
  console.log('Elevating map with 3D effect...');
  
  // 获取地图容器
  const mapContainer = document.querySelector('.globe-section .hologram-content');
  if (!mapContainer) {
    console.warn('未找到地图容器');
    return;
  }
  
  // 添加3D视觉效果
  mapContainer.style.perspective = '1000px';
  mapContainer.style.transformStyle = 'preserve-3d';
  
  // 找到echarts容器
  const echartsContainer = mapContainer.querySelector('[style*="width: 50vw"]');
  if (!echartsContainer) {
    console.warn('未找到echarts容器');
    return;
  }
  
  // 应用3D效果到echarts容器
  gsap.fromTo(echartsContainer,
    { 
      transform: 'rotateX(0deg) rotateY(0deg) scale(0.9)',
      boxShadow: '0 0 0 rgba(0, 240, 255, 0)'
    },
    { 
      transform: 'rotateX(15deg) rotateY(-15deg) scale(1)',
      boxShadow: '0 20px 50px rgba(0, 240, 255, 0.5)',
      duration: 2,
      ease: "power3.out"
    }
  );
  
  // 获取ChinaMap组件的Vue实例，以便访问其内部echarts实例
  setTimeout(() => {
    // 寻找地图组件可能导出的chart实例
    const chartInstance = window.mapChartInstance; // 假设组件将chart实例暴露到window
    
    if (chartInstance) {
      // 使用echarts API调整地图的视觉效果
      const option = chartInstance.getOption();
      
      // 增强地图区域
      if (option.series && option.series[0]) {
        // 修改地图样式，增加高亮和投影效果
        option.series[0].itemStyle = {
          ...option.series[0].itemStyle,
          shadowBlur: 10,
          shadowColor: 'rgba(0, 240, 255, 0.5)',
          borderWidth: 2
        };
        
        // 添加涟漪效果
        option.series.push({
          type: 'effectScatter',
          coordinateSystem: 'geo',
          data: option.series[0].data,
          symbolSize: 5,
          showEffectOn: 'render',
          rippleEffect: {
            period: 4,
            scale: 4,
            brushType: 'stroke'
          },
          itemStyle: {
            color: 'rgba(0, 240, 255, 0.8)'
          },
          zlevel: 1
        });
        
        chartInstance.setOption(option);
      }
    }
    
    // 添加额外的光效装饰元素
    const glowEffect = document.createElement('div');
    glowEffect.className = 'map-3d-glow';
    glowEffect.style.cssText = `
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      background: radial-gradient(circle at center, rgba(0, 240, 255, 0.1) 0%, transparent 70%);
      z-index: 1;
    `;
    mapContainer.appendChild(glowEffect);
    
    // 添加浮动数据点效果
    const dataPoints = 8;
    for (let i = 0; i < dataPoints; i++) {
      const dataPoint = document.createElement('div');
      dataPoint.className = 'floating-data-point';
      dataPoint.style.cssText = `
        position: absolute;
        width: ${Math.random() * 10 + 5}px;
        height: ${Math.random() * 10 + 5}px;
        background: rgba(0, 240, 255, 0.8);
        border-radius: 50%;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.8);
        top: ${Math.random() * 100}%;
        left: ${Math.random() * 100}%;
        pointer-events: none;
        z-index: 2;
      `;
      mapContainer.appendChild(dataPoint);
      
      // 为数据点添加动画
      gsap.to(dataPoint, {
        y: `-=${Math.random() * 100 + 50}`,
        x: `+=${Math.random() * 40 - 20}`,
        opacity: 0,
        duration: Math.random() * 3 + 2,
        delay: Math.random() * 2,
        ease: "power1.out",
        onComplete: () => dataPoint.remove()
      });
    }
  }, 500); // 给echarts足够的时间完成渲染
};
// 趋势线转化为3D曲面
// 趋势线转化为3D曲面
const convertTo3DSurface = () => {
  console.log('Converting charts to 3D surface...');
  
  // 获取图表容器
  const timeFlowContainers = document.querySelectorAll('.time-flow .hologram-content');
  if (!timeFlowContainers.length) {
    console.warn('未找到时间流图表容器');
    return;
  }
  
  timeFlowContainers.forEach((container, containerIndex) => {
    // 给容器添加3D效果
    gsap.to(container, {
      perspective: '1000px',
      transformStyle: 'preserve-3d',
      duration: 0.1
    });
    
    // 找到echarts容器
    const chartDiv = container.querySelector('[style*="width: 40vw"]');
    if (!chartDiv) {
      console.warn('未找到echarts容器');
      return;
    }
    
    // 应用3D变换效果到图表容器
    gsap.fromTo(chartDiv,
      { 
        transform: 'rotateX(0deg) rotateY(0deg) scale(0.95)',
        boxShadow: '0 0 0 rgba(0, 240, 255, 0)'
      },
      { 
        transform: 'rotateX(12deg) rotateY(-5deg) scale(1)',
        boxShadow: '0 20px 50px rgba(0, 240, 255, 0.5)',
        duration: 1.5,
        ease: "back.out(1.2)"
      }
    );
    
    // 获取ECharts实例并修改其选项
    setTimeout(() => {
      // 尝试获取图表实例
      const chartInstance = echarts.getInstanceByDom(chartDiv);
      
      if (chartInstance) {
        // 获取当前配置
        const option = chartInstance.getOption();
        
        // 增强图表视觉效果
        if (option.series && option.series.length) {
          // 修改线条样式
          option.series.forEach(series => {
            series.lineStyle = {
              ...series.lineStyle,
              width: 4,
              shadowBlur: 15,
              shadowColor: series.name === '结婚率' ? 'rgba(0, 240, 255, 0.8)' : 'rgba(255, 0, 255, 0.8)',
              shadowOffsetY: 8
            };
            
            // 修改点样式
            series.itemStyle = {
              ...series.itemStyle,
              shadowBlur: 10,
              shadowColor: series.name === '结婚率' ? 'rgba(0, 240, 255, 0.8)' : 'rgba(255, 0, 255, 0.8)',
              borderWidth: 3
            };
            
            // 添加区域填充
            series.areaStyle = {
              ...series.areaStyle,
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 0,
                  color: series.name === '结婚率' ? 'rgba(0, 240, 255, 0.5)' : 'rgba(255, 0, 255, 0.5)'
                },
                {
                  offset: 1,
                  color: 'rgba(0, 0, 0, 0)'
                }
              ]),
              shadowBlur: 20,
              shadowColor: series.name === '结婚率' ? 'rgba(0, 240, 255, 0.5)' : 'rgba(255, 0, 255, 0.5)',
              opacity: 0.5
            };
          });
        }
        
        // 应用修改后的配置
        chartInstance.setOption(option);
      }
      
      // 添加额外的光效装饰元素
      const glowEffect = document.createElement('div');
      glowEffect.className = 'chart-3d-glow';
      glowEffect.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        background: radial-gradient(ellipse at center, 
          rgba(0, 240, 255, 0.1) 0%, 
          rgba(255, 0, 255, 0.05) 50%, 
          transparent 70%);
        z-index: 1;
        border-radius: 8px;
        opacity: 0;
      `;
      container.appendChild(glowEffect);
      
      // 添加光效动画
      gsap.to(glowEffect, {
        opacity: 0.7,
        duration: 1,
        delay: 0.5
      });
      
      // 添加浮动数据点效果
      for (let i = 0; i < 12; i++) {
        const dataPoint = document.createElement('div');
        dataPoint.className = 'floating-data-point';
        dataPoint.style.cssText = `
          position: absolute;
          width: ${Math.random() * 6 + 3}px;
          height: ${Math.random() * 6 + 3}px;
          background: ${Math.random() > 0.5 ? 'rgba(0, 240, 255, 0.8)' : 'rgba(255, 0, 255, 0.8)'};
          border-radius: 50%;
          box-shadow: 0 0 10px ${Math.random() > 0.5 ? 'rgba(0, 240, 255, 0.8)' : 'rgba(255, 0, 255, 0.8)'};
          top: ${Math.random() * 80 + 10}%;
          left: ${Math.random() * 80 + 10}%;
          pointer-events: none;
          z-index: 2;
          opacity: 0;
        `;
        container.appendChild(dataPoint);
        
        // 为数据点添加动画
        gsap.to(dataPoint, {
          y: `-=${Math.random() * 100 + 30}`,
          x: `${Math.random() > 0.5 ? '+' : '-'}=${Math.random() * 30}`,
          opacity: [0, 0.8, 0],
          duration: Math.random() * 4 + 3,
          delay: Math.random() * 2,
          ease: "power1.out",
          onComplete: () => dataPoint.remove()
        });
      }
    }, 500); // 给echarts足够的时间完成渲染
  });
  
  // 添加必要的CSS
  const style = document.createElement('style');
  style.textContent = `
    @keyframes chart-glow {
      0% { opacity: 0.3; transform: scale(0.98); }
      100% { opacity: 0.7; transform: scale(1.02); }
    }
    
    .chart-3d-glow {
      animation: chart-glow 3s infinite alternate;
    }
  `;
  document.head.appendChild(style);
};

// 关系图谱展开效果
const expandRelationships = () => {
  const networkContainers = document.querySelectorAll('.network-section .hologram-content');
  if (!networkContainers.length) return;
  
  networkContainers.forEach((container) => {
    // 获取节点和连线
    const nodes = container.querySelectorAll('circle, rect, g');
    const links = container.querySelectorAll('path:not(.node)');
    
    // 设置3D环境
    gsap.to(container, {
      perspective: '1200px',
      transformStyle: 'preserve-3d',
      duration: 0.1
    });
    
    // 让节点从中心爆发出来
    nodes.forEach((node, index) => {
      // 保存原始位置
      const originalTransform = node.getAttribute('transform') || '';
      
      // 先缩小到中心点
      gsap.set(node, {
        transform: 'scale(0.1) translateZ(0px)',
        opacity: 0
      });
      
      // 然后爆发出来
      gsap.to(node, {
        transform: `${originalTransform} scale(1) translateZ(${Math.random() * 30 + 10}px)`,
        opacity: 1,
        duration: 1.2,
        delay: index * 0.02,
        ease: "back.out(1.7)"
      });
      
      // 添加悬浮效果
      node.addEventListener('mouseenter', () => {
        gsap.to(node, {
          transform: `${originalTransform} scale(1.2) translateZ(50px)`,
          filter: 'drop-shadow(0 0 10px var(--accent-color))',
          duration: 0.3
        });
      });
      
      node.addEventListener('mouseleave', () => {
        gsap.to(node, {
          transform: `${originalTransform} scale(1) translateZ(${Math.random() * 30 + 10}px)`,
          filter: 'none',
          duration: 0.3
        });
      });
    });
    
    // 连线动画
    links.forEach((link, index) => {
      const pathLength = link.getTotalLength ? link.getTotalLength() : 500;
      
      // 设置初始状态
      gsap.set(link, {
        strokeDasharray: pathLength,
        strokeDashoffset: pathLength,
        opacity: 0
      });
      
      // 线条绘制动画
      gsap.to(link, {
        strokeDashoffset: 0,
        opacity: 0.8,
        duration: 1.5,
        delay: 0.5 + index * 0.01,
        ease: "power3.out"
      });
      
      // 添加光流效果
      gsap.to(link, {
        filter: 'drop-shadow(0 0 3px var(--primary-color))',
        duration: 2,
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut"
      });
    });
    
    // 整体图表的3D效果
    gsap.to(container, {
      rotationY: 5,
      rotationX: -3,
      duration: 3,
      ease: "power1.inOut"
    });
  });
};

// 综合数据漩涡效果
// 综合数据漩涡效果
const createDataVortex = () => {
  console.log('Creating data vortex effect...');
  
  // 给容器添加初始化动画效果的延迟，确保图表已渲染
  setTimeout(() => {
    const matrixContainer = document.querySelector('.matrix-section .hologram-content');
    if (!matrixContainer) {
      console.warn('未找到矩阵容器');
      return;
    }
    
    // 设置3D环境
    gsap.to(matrixContainer, {
      perspective: '1500px',
      transformStyle: 'preserve-3d',
      duration: 0.1
    });
    
    // 创建装饰性粒子代替直接操作图表元素
    for (let i = 0; i < 100; i++) {
      createDecorativeParticle(matrixContainer, i);
    }
    
    // 为图表容器添加 3D 效果
    const chartContainer = matrixContainer.querySelector('.marriage-visual');
    if (chartContainer) {
      // 应用整体旋转动画
      gsap.fromTo(chartContainer, 
        { rotateX: 0, rotateY: 0, scale: 0.9, opacity: 0.7 },
        { 
          rotateX: "10deg", 
          rotateY: "15deg", 
          scale: 1,
          opacity: 1,
          duration: 2,
          ease: "power3.out"
        }
      );
      
      // 添加轻微浮动动画
      gsap.to(chartContainer, {
        rotateY: "+=5",
        rotateX: "-=3",
        y: "-=10",
        duration: 4,
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut"
      });
    }
    
    // 创建光线特效
    const lightBeam = document.createElement('div');
    lightBeam.className = 'matrix-light-beam';
    lightBeam.style.cssText = `
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--primary-color);
      box-shadow: 0 0 100px 50px var(--primary-color);
      opacity: 0;
      z-index: -1;
    `;
    matrixContainer.appendChild(lightBeam);
    
    // 光线脉动动画
    gsap.to(lightBeam, {
      opacity: 0.7,
      width: '20px',
      height: '20px',
      duration: 2,
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut"
    });
    
    // 添加漩涡背景效果
    const vortexBackground = document.createElement('div');
    vortexBackground.className = 'vortex-background';
    vortexBackground.style.cssText = `
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: 
        radial-gradient(ellipse at center, 
          rgba(0,0,0,0) 30%, 
          rgba(0, 240, 255, 0.05) 60%, 
          rgba(0, 240, 255, 0.1) 100%);
      z-index: -1;
      pointer-events: none;
      border-radius: var(--border-radius);
    `;
    matrixContainer.appendChild(vortexBackground);
    
    // 创建旋转光环
    createRotatingRings(matrixContainer);
  }, 800); // 给足够的时间让图表渲染
};

// 创建装饰性粒子
const createDecorativeParticle = (container, index) => {
  const particle = document.createElement('div');
  
  // 随机位置和大小
  const size = Math.random() * 6 + 3;
  const centerX = container.clientWidth / 2;
  const centerY = container.clientHeight / 2;
  const angle = Math.random() * Math.PI * 2;
  const radius = Math.random() * (container.clientWidth / 3) + 50;
  const x = centerX + Math.cos(angle) * radius;
  const y = centerY + Math.sin(angle) * radius;
  
  // 设置粒子样式
  particle.className = 'vortex-particle';
  particle.style.cssText = `
    position: absolute;
    width: ${size}px;
    height: ${size}px;
    left: ${x}px;
    top: ${y}px;
    background: ${Math.random() > 0.5 ? 'var(--primary-color)' : 'var(--secondary-color)'};
    border-radius: 50%;
    box-shadow: 0 0 ${size * 2}px ${Math.random() > 0.5 ? 'var(--primary-color)' : 'var(--secondary-color)'};
    opacity: 0;
    z-index: 2;
    pointer-events: none;
  `;
  
  container.appendChild(particle);
  
  // 计算漩涡参数
  const distance = Math.sqrt(Math.pow(x - centerX, 2) + Math.pow(y - centerY, 2));
  const delay = distance / 300;
  const duration = Math.random() * 3 + 3;
  
  // 粒子漩涡动画
  gsap.to(particle, {
    opacity: [0, 0.8, 0],
    scale: [0, 1, 0],
    rotation: Math.random() * 360,
    duration: duration,
    delay: delay,
    ease: "power1.inOut",
    repeat: -1,
    onRepeat: () => {
      // 更新粒子位置，创造漩涡效果
      const newAngle = angle + (Math.random() * 0.5);
      const newRadius = radius * (Math.random() * 0.2 + 0.9);
      const newX = centerX + Math.cos(newAngle) * newRadius;
      const newY = centerY + Math.sin(newAngle) * newRadius;
      
      gsap.set(particle, {
        left: newX,
        top: newY
      });
    }
  });
};

// 创建旋转光环
const createRotatingRings = (container) => {
  const ringsCount = 3;
  
  for (let i = 0; i < ringsCount; i++) {
    const ring = document.createElement('div');
    const size = (i + 1) * 100 + 100;
    
    ring.className = 'vortex-ring';
    ring.style.cssText = `
      position: absolute;
      width: ${size}px;
      height: ${size}px;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      border-radius: 50%;
      border: 2px solid ${i % 2 ? 'var(--primary-color)' : 'var(--secondary-color)'};
      opacity: 0.3;
      box-shadow: 0 0 20px ${i % 2 ? 'var(--primary-color)' : 'var(--secondary-color)'};
      z-index: -1;
      pointer-events: none;
    `;
    
    container.appendChild(ring);
    
    // 光环旋转动画
    gsap.to(ring, {
      rotation: 360,
      duration: 20 + i * 10,
      repeat: -1,
      ease: "none"
    });
    
    // 光环呼吸动画
    gsap.to(ring, {
      opacity: 0.1,
      scale: 1.1,
      duration: 3 + i,
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut"
    });
  }
};
// 组件挂载时初始化
onMounted(() => {
  initThreeJS();
  
  // 监听滚动创建视差效果
  gsap.utils.toArray('.parallax-section').forEach((section, i) => {
    ScrollTrigger.create({
      trigger: section,
      start: 'top bottom',
      end: 'bottom top',
      onUpdate: (self) => {
        const speed = section.dataset.speed || 0.5;
        gsap.to(section, {
          y: self.progress * 100 * speed,
          ease: 'none',
          overwrite: 'auto'
        });
      }
    });
  });
});
</script>

<template>
  <!-- 加载页面 -->
  <div v-if="loading" class="loading-screen">
    <div class="loader">
      <div class="ring"></div>
      <div class="ring"></div>
      <div class="ring"></div>
      <span class="loading-text">构建3D婚姻数据宇宙</span>
    </div>
  </div>

  <!-- 3D背景容器 -->
  <div id="three-container"></div>
  
  <!-- 数据提示框 -->
  <div id="data-tooltip" class="data-tooltip"></div>
  
  <!-- 主内容 -->
  <div class="cosmic-container" :class="{ 'visible': sceneReady }">
    <!-- 首页 -->
    <div v-if="first_page" class="portal-entrance" @click="enterDataverse">
      <div class="portal-ring"></div>
      <div class="portal-ring"></div>
      <div class="portal-ring"></div>
      <div class="portal-core"></div>
      <h1 class="portal-title">进入婚姻数据宇宙</h1>
      <p class="portal-subtitle">点击探索未知的数据世界</p>
    </div>
    
    <!-- 主仪表板 -->
    <div v-else class="dataverse-dashboard">
      <!-- 3D导航系统 -->
      <div class="nav-system">
        <div class="nav-orbit">
          <button 
            v-for="(page, index) in ['宇宙概览', '中国地图', '时间长河', '关系网络', '数据矩阵']" 
            :key="index"
            :class="['nav-planet', { active: activePage === index }]"
            @click="changePage(index)"
            :style="`--orbit-position: ${index * 72}deg`"
          >
            <div class="planet-ring"></div>
            <div class="planet-core"></div>
            <span class="planet-name">{{ page }}</span>
          </button>
        </div>
      </div>
      
      <!-- 内容区域 -->
      <main class="content-dimension">
        <!-- 页面0: 宇宙概览 -->
        <section v-show="activePage === 0" class="page-content dimension-section">
          <div class="holographic-card parallax-section" data-speed="0.3">
            <div class="hologram-header">
              <h2>婚姻数据银河系</h2>
              <div class="hologram-controls">
                <button @click="bubble_show = !bubble_show" class="holo-btn">
                  {{ bubble_show ? '隐藏气泡' : '显示气泡' }}
                </button>
              </div>
            </div>
            <div class="hologram-content">
              <bubble v-if="bubble_show" data_path="/src/assets/data/province-marriage-divorce.csv" />
            </div>
          </div>
        </section>
        
        <!-- 页面1: 全球地图 -->
        <section v-show="activePage === 1" class="page-content dimension-section">
          <div class="holographic-card globe-section parallax-section" data-speed="0.4">
            <div class="hologram-header">
              <h2>中国婚姻分布</h2>
            </div>
            <div class="hologram-content">
              <ChinaMap />
            </div>
          </div>
        </section>
        
        <!-- 页面2: 时间长河 -->
        <section v-show="activePage === 2" class="page-content dimension-section">
          <div class="holographic-cards-container">
            <div class="holographic-card time-flow parallax-section" data-speed="0.5">
              <div class="hologram-header">
                <h2>婚姻离婚对比</h2>
              </div>
              <div class="hologram-content">
                <divorce_marriage data_path="/src/assets/data/divorce_marriage.csv" />
              </div>
            </div>
            
            <div class="holographic-card time-flow parallax-section" data-speed="0.3">
              <div class="hologram-header">
                <h2>解释</h2>
              </div>
              <div class="hologram-content">
                <p>本页面展示了中国婚姻和离婚的趋势对比。通过时间轴上的数据点，您可以观察到婚姻和离婚率的变化。</p>
                <p>点击数据点可以查看详细信息。</p>
              </div>
            </div>
            
          </div>
        </section>
        
        <!-- 页面3: 关系网络 -->
        <section v-show="activePage === 3" class="page-content dimension-section">
          <div class="holographic-card network-section parallax-section" data-speed="0.6">
            <div class="hologram-header">
              <h2>婚姻关系网络</h2>
            </div>
            <div class="hologram-content">
              <sangji data_path="/src/assets/data/sankey.csv" />
            </div>
          </div>
          
          <div class="holographic-card network-section parallax-section" data-speed="0.4">
            <div class="hologram-header">
              <h2>数据综合分析</h2>
            </div>
            <div class="hologram-content">
              <EchartsChart />
            </div>
          </div>
        </section>
        
        <!-- 页面4: 数据矩阵 -->
        <section v-show="activePage === 4" class="page-content dimension-section">
          <div class="holographic-card matrix-section parallax-section" data-speed="0.5">
            <div class="hologram-header">
              <h2>婚姻年龄矩阵</h2>
            </div>
            <div class="hologram-content">
              <MV data_path="/src/assets/data/marriage.csv" />
            </div>
          </div>
        </section>
      </main>
      
      <!-- 数据态底部 -->
      <footer class="quantum-footer">
        <div class="quantum-particles"></div>
        <div class="footer-content">
          <p>数据源：国家统计局量子数据库</p>
          <p>技术支持：婚姻数据科学研究院</p>
          <p>© 2025 宇宙婚姻观测中心</p>
        </div>
      </footer>
    </div>
  </div>
</template>

<style>
:root {
  --primary-color: #00f0ff;
  --secondary-color: #ff00e6;
  --accent-color: #ffcc00;
  --background-dark: #0a0a1a;
  --background-light: #1a1a3a;
  --text-color: #f0f0ff;
  --border-radius: 12px;
  --card-glow: 0 0 20px rgba(0, 240, 255, 0.5), 0 0 40px rgba(0, 240, 255, 0.2);
  --hologram-border: 1px solid rgba(0, 240, 255, 0.3);
  --planet-orbit-time: 60s;
}

/* 全局重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Orbitron', sans-serif;
  background-color: var(--background-dark);
  color: var(--text-color);
  overflow-x: hidden;
  min-height: 100vh;
}

/* 3D容器 */
#three-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

/* 加载屏幕 */
.loading-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: var(--background-dark);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loader {
  position: relative;
  width: 200px;
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.ring {
  position: absolute;
  border: 2px solid transparent;
  border-radius: 50%;
  animation: rotate 2s linear infinite;
}

.ring:nth-child(1) {
  width: 120px;
  height: 120px;
  border-top: 2px solid var(--primary-color);
  border-bottom: 2px solid var(--secondary-color);
  animation-delay: 0s;
}

.ring:nth-child(2) {
  width: 100px;
  height: 100px;
  border-left: 2px solid var(--secondary-color);
  border-right: 2px solid var(--accent-color);
  animation-delay: 0.2s;
}

.ring:nth-child(3) {
  width: 80px;
  height: 80px;
  border-top: 2px solid var(--accent-color);
  border-bottom: 2px solid var(--primary-color);
  animation-delay: 0.4s;
}

.loading-text {
  position: absolute;
  font-size: 1rem;
  letter-spacing: 2px;
  color: var(--text-color);
  top: calc(100% + 30px);
  white-space: nowrap;
}

@keyframes rotate {
  0% {
    transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg);
  }
  100% {
    transform: rotateX(360deg) rotateY(180deg) rotateZ(360deg);
  }
}

/* 主容器 */
.cosmic-container {
  position: relative;
  z-index: 10;
  opacity: 0;
  transition: opacity 1.5s ease;
}

.cosmic-container.visible {
  opacity: 1;
}

/* 入口门户 */
.portal-entrance {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  perspective: 1000px;
}

.portal-ring {
  position: absolute;
  border-radius: 50%;
  border: 4px solid rgba(0, 240, 255, 0.5);
  animation: portal-pulse 4s infinite alternate, portal-rotate 20s linear infinite;
}

.portal-ring:nth-child(1) {
  width: 600px;
  height: 600px;
  border-top-color: var(--primary-color);
  border-right-color: transparent;
  animation-delay: 0s;
}

.portal-ring:nth-child(2) {
  width: 400px;
  height: 400px;
  border-bottom-color: var(--secondary-color);
  border-left-color: transparent;
  animation-delay: 0.5s;
  animation-direction: alternate-reverse;
}

.portal-ring:nth-child(3) {
  width: 200px;
  height: 200px;
  border-left-color: var(--accent-color);
  border-bottom-color: transparent;
  animation-delay: 1s;
}

.portal-core {
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, #fff 0%, rgba(0, 240, 255, 0.8) 50%, transparent 100%);
  border-radius: 50%;
  box-shadow: 0 0 50px var(--primary-color);
  animation: core-pulse 2s infinite alternate;
}

.portal-title {
  margin-top: 350px;
  font-size: 3rem;
  font-weight: bold;
  text-shadow: 0 0 10px var(--primary-color);
  letter-spacing: 5px;
  animation: text-glow 2s infinite alternate;
}

.portal-subtitle {
  margin-top: 20px;
  font-size: 1.2rem;
  opacity: 0.8;
  letter-spacing: 2px;
}

@keyframes portal-pulse {
  0% {
    box-shadow: 0 0 20px rgba(0, 240, 255, 0.2);
    transform: scale3d(0.95, 0.95, 1) rotate3d(1, 1, 0, 0deg);
  }
  100% {
    box-shadow: 0 0 40px rgba(0, 240, 255, 0.6);
    transform: scale3d(1.05, 1.05, 1) rotate3d(1, 1, 0, 10deg);
  }
}

@keyframes portal-rotate {
  0% {
    transform: rotateZ(0deg) rotateX(20deg) rotateY(0deg);
  }
  100% {
    transform: rotateZ(360deg) rotateX(20deg) rotateY(360deg);
  }
}

@keyframes core-pulse {
  0% {
    transform: scale(0.8);
    box-shadow: 0 0 30px var(--primary-color);
  }
  100% {
    transform: scale(1.2);
    box-shadow: 0 0 70px var(--primary-color);
  }
}

@keyframes text-glow {
  0% {
    text-shadow: 0 0 10px var(--primary-color);
  }
  100% {
    text-shadow: 0 0 30px var(--primary-color), 0 0 40px var(--secondary-color);
  }
}

/* 数据宇宙仪表板 */
.dataverse-dashboard {
  min-height: 100vh;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

/* 3D导航系统 */
.nav-system {
  position:fixed;
  top: 80px;
  left:28%;
  transform: translateX(-50%);
  width: 90%;
  max-width: 1200px;
  height: 100px;
  z-index: 100;
  perspective: 1000px;
}

.nav-orbit {
  position: relative;
  width: 20vw;
  height: 20vh;
  transform-style: preserve-3d;
}

.nav-planet {
  position: absolute;
  width: 15vw;
  height: 4vw;
  top: 10px;
  left: calc(50% - 40px);
  transform: rotate(var(--orbit-position)) translateX(calc(50% - 40px)) rotate(calc(-1 * var(--orbit-position)));
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  cursor: pointer;
  transform-style: preserve-3d;
  transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.planet-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid rgba(0, 240, 255, 0.3);
  transition: all 0.5s ease;
  transform-style: preserve-3d;
  transform: rotateX(60deg);
}

.planet-core {
  width: 50%;
  height: 50%;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.8) 0%, var(--primary-color) 70%);
  box-shadow: 0 0 15px var(--primary-color);
  transition: all 0.5s ease;
}

.planet-name {
  position: absolute;
  bottom: -30px;
  white-space: nowrap;
  font-size: 0.8rem;
  opacity: 0.7;
  transition: all 0.5s ease;
}

.nav-planet:hover .planet-ring {
  border: 2px solid var(--primary-color);
  box-shadow: 0 0 15px var(--primary-color);
  transform: rotateX(75deg);
}

.nav-planet:hover .planet-core {
  background: radial-gradient(circle, #fff 0%, var(--secondary-color) 70%);
  box-shadow: 0 0 25px var(--secondary-color);
  transform: scale(1.2);
}

.nav-planet:hover .planet-name {
  opacity: 1;
  transform: translateY(5px);
  color: var(--accent-color);
}

.nav-planet.active .planet-ring {
  border: 3px solid var(--accent-color);
  box-shadow: 0 0 20px var(--accent-color);
  animation: planet-spin 10s linear infinite;
}

.nav-planet.active .planet-core {
  background: radial-gradient(circle, #fff 0%, var(--accent-color) 70%);
  box-shadow: 0 0 30px var(--accent-color);
  transform: scale(1.3);
  animation: core-throb 2s ease infinite alternate;
}

.nav-planet.active .planet-name {
  color: var(--accent-color);
  font-weight: bold;
  text-shadow: 0 0 10px var(--accent-color);
}

@keyframes planet-spin {
  0% {
    transform: rotateX(60deg) rotateZ(0deg);
  }
  100% {
    transform: rotateX(60deg) rotateZ(360deg);
  }
}

@keyframes core-throb {
  0% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1.4);
  }
}

/* 内容区域 */
.content-dimension {
  margin-top: 180px;
  flex: 1;
  position: relative;
}

.dimension-section {
  width: 100%;
  padding: 30px;
  transition: transform 0.8s cubic-bezier(0.68, -0.55, 0.27, 1.55), opacity 0.8s ease;
}

/* 全息卡片 */
.holographic-card {
  background: rgba(20, 30, 60, 0.7);
  border: var(--hologram-border);
  border-radius: var(--border-radius);
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: var(--card-glow);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
  transform-style: preserve-3d;
  transform: perspective(1000px);
}

.holographic-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent 0%,
    rgba(0, 240, 255, 0.1) 25%,
    transparent 50%,
    rgba(255, 0, 230, 0.1) 75%,
    transparent 100%
  );
  transform: rotate(30deg);
  animation: hologram-scan 8s linear infinite;
  z-index: -1;
}

.holographic-cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 30px;
}

.hologram-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid rgba(0, 240, 255, 0.3);
  padding-bottom: 10px;
}

.hologram-header h2 {
  color: var(--primary-color);
  font-size: 1.5rem;
  letter-spacing: 2px;
  text-shadow: 0 0 10px var(--primary-color);
}

.hologram-controls {
  display: flex;
  gap: 10px;
}

.holo-btn {
  background-color: rgba(0, 240, 255, 0.2);
  border: 1px solid var(--primary-color);
  color: var(--text-color);
  padding: 8px 15px;
  border-radius: 20px;
  font-family: 'Orbitron', sans-serif;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.holo-btn:hover {
  background-color: rgba(0, 240, 255, 0.4);
  box-shadow: 0 0 15px var(--primary-color);
}

.hologram-content {
  position: relative;
  min-height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
}

@keyframes hologram-scan {
  0% {
    transform: rotate(30deg) translateY(0%);
  }
  100% {
    transform: rotate(30deg) translateY(100%);
  }
}

/* 量子页脚 */
.quantum-footer {
  margin-top: 40px;
  padding: 20px;
  position: relative;
  overflow: hidden;
  border-top: 1px solid rgba(0, 240, 255, 0.3);
}

.quantum-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(circle at 20% 30%, rgba(0, 240, 255, 0.2) 0%, transparent 10%),
    radial-gradient(circle at 70% 60%, rgba(255, 0, 230, 0.2) 0%, transparent 10%),
    radial-gradient(circle at 40% 80%, rgba(255, 204, 0, 0.2) 0%, transparent 10%);
  filter: blur(3px);
  animation: quantum-float 10s linear infinite;
  z-index: -1;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 20px;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
}

@keyframes quantum-float {
  0% {
    background-position: 0% 0%;
  }
  100% {
    background-position: 100% 100%;
  }
}
/* 3D 地图效果 */
.map-3d-glow {
  animation: map-glow 3s infinite alternate;
}

@keyframes map-glow {
  0% {
    opacity: 0.3;
    transform: scale(0.95);
  }
  100% {
    opacity: 0.7;
    transform: scale(1.05);
  }
}

.floating-data-point {
  animation: float-pulse 1s infinite alternate;
}

@keyframes float-pulse {
  0% {
    transform: scale(0.8);
  }
  100% {
    transform: scale(1.2);
  }
}
/* 数据提示框 */
.data-tooltip {
  position: fixed;
  background: rgba(10, 20, 40, 0.9);
  border: 1px solid var(--primary-color);
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 0 20px rgba(0, 240, 255, 0.5);
  backdrop-filter: blur(10px);
  z-index: 1000;
  max-width: 300px;
  display: none;
  pointer-events: none;
  transform: translateZ(0);
}

.data-tooltip h3 {
  color: var(--accent-color);
  margin-bottom: 10px;
  font-size: 1rem;
}

.data-tooltip p {
  font-size: 0.9rem;
  margin-bottom: 8px;
  color: rgba(255, 255, 255, 0.8);
}

.tooltip-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary-color);
  text-shadow: 0 0 10px var(--primary-color);
  text-align: center;
  margin-top: 10px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .nav-system {
    width: 100%;
  }
  
  .holographic-cards-container {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .nav-planet {
    width: 60px;
    height: 60px;
    left: calc(50% - 30px);
  }
  
  .portal-title {
    font-size: 2rem;
    margin-top: 300px;
  }
  
  .portal-ring:nth-child(1) {
    width: 400px;
    height: 400px;
  }
  
  .portal-ring:nth-child(2) {
    width: 300px;
    height: 300px;
  }
  
  .portal-ring:nth-child(3) {
    width: 150px;
    height: 150px;
  }
}

@media (max-width: 480px) {
  .nav-system {
    height: 160px;
  }
  
  .nav-orbit {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
  }
  
  .nav-planet {
    position: relative;
    top: 0;
    left: 0;
    transform: none !important;
  }
  
  .planet-name {
    opacity: 1;
  }
}

/* 漩涡特效 */
.vortex-particle {
  animation: particle-pulse 2s infinite alternate;
}

.vortex-ring {
  transform-style: preserve-3d;
  backface-visibility: hidden;
}

@keyframes particle-pulse {
  0% {
    box-shadow: 0 0 5px var(--primary-color);
  }
  100% {
    box-shadow: 0 0 20px var(--primary-color);
  }
}

.matrix-light-beam {
  animation: beam-pulse 3s infinite alternate;
}

@keyframes beam-pulse {
  0% {
    opacity: 0.3;
    box-shadow: 0 0 50px var(--primary-color);
  }
  100% {
    opacity: 0.7;
    box-shadow: 0 0 100px var(--primary-color);
  }
}
</style>