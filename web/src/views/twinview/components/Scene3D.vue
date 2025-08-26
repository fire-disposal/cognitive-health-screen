<template>
  <div ref="sceneContainer" class="scene-container">
    <div v-if="loading" class="loading-overlay">
      <n-spin size="large" />
      <p class="loading-text">正在加载3D场景...</p>
    </div>
    
    <!-- 场景控制面板 -->
    <div class="scene-controls">
      <n-space>
        <n-button size="small" @click="resetCamera">
          <template #icon>
            <Icon icon="mdi:camera-retake" />
          </template>
          重置视角
        </n-button>
        <n-button size="small" @click="toggleAnimation">
          <template #icon>
            <Icon :icon="animationPlaying ? 'mdi:pause' : 'mdi:play'" />
          </template>
          {{ animationPlaying ? '暂停' : '播放' }}
        </n-button>
      </n-space>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { Icon } from '@iconify/vue'
import * as THREE from 'three'

const props = defineProps({
  selectedElderly: {
    type: [String, Number],
    default: null
  },
  showSensors: {
    type: Boolean,
    default: true
  },
  showTrajectory: {
    type: Boolean,
    default: true
  },
  viewMode: {
    type: String,
    default: '3d'
  }
})

// 响应式数据
const sceneContainer = ref(null)
const loading = ref(true)
const animationPlaying = ref(true)

// Three.js 相关变量
let scene, camera, renderer, controls
let animationId = null
let elderlyModel = null
let sensorObjects = []
let trajectoryLine = null

// 初始化3D场景
const initScene = () => {
  if (!sceneContainer.value) return

  // 创建场景
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0xf0f0f0)

  // 创建相机
  const width = sceneContainer.value.clientWidth
  const height = sceneContainer.value.clientHeight
  camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000)
  camera.position.set(10, 10, 10)
  camera.lookAt(0, 0, 0)

  // 创建渲染器
  renderer = new THREE.WebGLRenderer({ antialias: true })
  renderer.setSize(width, height)
  renderer.shadowMap.enabled = true
  renderer.shadowMap.type = THREE.PCFSoftShadowMap
  sceneContainer.value.appendChild(renderer.domElement)

  // 添加光源
  addLights()
  
  // 创建房间
  createRoom()
  
  // 创建老人模型
  createElderlyModel()
  
  // 创建传感器
  createSensors()
  
  // 创建活动轨迹
  createTrajectory()

  // 开始渲染循环
  animate()

  // 添加窗口大小变化监听
  window.addEventListener('resize', onWindowResize)

  // 应用初始显示设置
  updateSceneDisplay()

  loading.value = false
}

// 添加光源
const addLights = () => {
  // 环境光
  const ambientLight = new THREE.AmbientLight(0x404040, 0.6)
  scene.add(ambientLight)

  // 方向光
  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
  directionalLight.position.set(10, 10, 5)
  directionalLight.castShadow = true
  directionalLight.shadow.mapSize.width = 2048
  directionalLight.shadow.mapSize.height = 2048
  scene.add(directionalLight)

  // 点光源
  const pointLight = new THREE.PointLight(0xffffff, 0.5, 100)
  pointLight.position.set(0, 8, 0)
  scene.add(pointLight)
}

// 创建房间
const createRoom = () => {
  // 地板
  const floorGeometry = new THREE.PlaneGeometry(20, 20)
  const floorMaterial = new THREE.MeshLambertMaterial({ color: 0xffffff })
  const floor = new THREE.Mesh(floorGeometry, floorMaterial)
  floor.rotation.x = -Math.PI / 2
  floor.receiveShadow = true
  scene.add(floor)

  // 墙壁
  const wallMaterial = new THREE.MeshLambertMaterial({ color: 0xe0e0e0 })
  
  // 后墙
  const backWallGeometry = new THREE.PlaneGeometry(20, 8)
  const backWall = new THREE.Mesh(backWallGeometry, wallMaterial)
  backWall.position.set(0, 4, -10)
  scene.add(backWall)

  // 左墙
  const leftWallGeometry = new THREE.PlaneGeometry(20, 8)
  const leftWall = new THREE.Mesh(leftWallGeometry, wallMaterial)
  leftWall.rotation.y = Math.PI / 2
  leftWall.position.set(-10, 4, 0)
  scene.add(leftWall)

  // 添加一些家具
  createFurniture()
}

// 创建家具
const createFurniture = () => {
  // 沙发
  const sofaGeometry = new THREE.BoxGeometry(4, 1, 2)
  const sofaMaterial = new THREE.MeshLambertMaterial({ color: 0x8B4513 })
  const sofa = new THREE.Mesh(sofaGeometry, sofaMaterial)
  sofa.position.set(-3, 0.5, -5)
  sofa.castShadow = true
  scene.add(sofa)

  // 茶几
  const tableGeometry = new THREE.BoxGeometry(2, 0.5, 1)
  const tableMaterial = new THREE.MeshLambertMaterial({ color: 0x654321 })
  const table = new THREE.Mesh(tableGeometry, tableMaterial)
  table.position.set(-3, 0.25, -2)
  table.castShadow = true
  scene.add(table)

  // 电视
  const tvGeometry = new THREE.BoxGeometry(3, 2, 0.2)
  const tvMaterial = new THREE.MeshLambertMaterial({ color: 0x000000 })
  const tv = new THREE.Mesh(tvGeometry, tvMaterial)
  tv.position.set(0, 3, -9.8)
  scene.add(tv)
}

// 创建老人模型
const createElderlyModel = () => {
  // 简单的老人模型（圆柱体代表身体，球体代表头部）
  const bodyGeometry = new THREE.CylinderGeometry(0.3, 0.4, 1.5, 8)
  const bodyMaterial = new THREE.MeshLambertMaterial({ color: 0x4169E1 })
  const body = new THREE.Mesh(bodyGeometry, bodyMaterial)
  body.position.y = 0.75
  body.castShadow = true

  const headGeometry = new THREE.SphereGeometry(0.25, 8, 6)
  const headMaterial = new THREE.MeshLambertMaterial({ color: 0xFFDBB3 })
  const head = new THREE.Mesh(headGeometry, headMaterial)
  head.position.y = 1.75
  head.castShadow = true

  elderlyModel = new THREE.Group()
  elderlyModel.add(body)
  elderlyModel.add(head)
  elderlyModel.position.set(-3, 0, -5) // 初始位置在沙发上
  scene.add(elderlyModel)
}

// 创建传感器
const createSensors = () => {
  const sensorPositions = [
    { x: -8, y: 6, z: -8, type: '温湿度传感器' },
    { x: 8, y: 6, z: -8, type: '光照传感器' },
    { x: -8, y: 6, z: 8, type: '空气质量传感器' },
    { x: 8, y: 6, z: 8, type: '运动传感器' }
  ]

  sensorPositions.forEach(pos => {
    const sensorGeometry = new THREE.BoxGeometry(0.3, 0.3, 0.3)
    const sensorMaterial = new THREE.MeshLambertMaterial({ color: 0x00FF00 })
    const sensor = new THREE.Mesh(sensorGeometry, sensorMaterial)
    sensor.position.set(pos.x, pos.y, pos.z)
    sensor.userData = { type: pos.type }
    
    // 添加发光效果
    const glowGeometry = new THREE.SphereGeometry(0.2, 8, 6)
    const glowMaterial = new THREE.MeshBasicMaterial({ 
      color: 0x00FF00, 
      transparent: true, 
      opacity: 0.3 
    })
    const glow = new THREE.Mesh(glowGeometry, glowMaterial)
    sensor.add(glow)
    
    // 设置初始可见性
    sensor.visible = props.showSensors

    sensorObjects.push(sensor)
    scene.add(sensor)
  })
}

// 创建活动轨迹
const createTrajectory = () => {
  const points = [
    new THREE.Vector3(-3, 1, -5), // 沙发
    new THREE.Vector3(0, 1, -2),  // 客厅中央
    new THREE.Vector3(3, 1, 0),   // 厨房方向
    new THREE.Vector3(0, 1, 3),   // 阳台方向
    new THREE.Vector3(-3, 1, -5)  // 回到沙发
  ]

  const geometry = new THREE.BufferGeometry().setFromPoints(points)
  const material = new THREE.LineBasicMaterial({ 
    color: 0xff0000, 
    linewidth: 3,
    transparent: true,
    opacity: 0.7
  })
  
  trajectoryLine = new THREE.Line(geometry, material)
  // 设置初始可见性
  trajectoryLine.visible = props.showTrajectory
  scene.add(trajectoryLine)
}

// 动画循环
const animate = () => {
  if (!animationPlaying.value) return
  
  animationId = requestAnimationFrame(animate)
  
  // 传感器闪烁效果
  sensorObjects.forEach((sensor, index) => {
    const time = Date.now() * 0.001
    sensor.children[0].material.opacity = 0.3 + 0.2 * Math.sin(time * 2 + index)
  })
  
  // 老人模型轻微摆动
  if (elderlyModel) {
    const time = Date.now() * 0.001
    elderlyModel.rotation.y = Math.sin(time * 0.5) * 0.1
  }
  
  renderer.render(scene, camera)
}

// 重置相机
const resetCamera = () => {
  camera.position.set(10, 10, 10)
  camera.lookAt(0, 0, 0)
}

// 切换动画
const toggleAnimation = () => {
  animationPlaying.value = !animationPlaying.value
  if (animationPlaying.value) {
    animate()
  } else if (animationId) {
    cancelAnimationFrame(animationId)
  }
}

// 窗口大小变化处理
const onWindowResize = () => {
  if (!sceneContainer.value || !camera || !renderer) return
  
  const width = sceneContainer.value.clientWidth
  const height = sceneContainer.value.clientHeight
  
  camera.aspect = width / height
  camera.updateProjectionMatrix()
  renderer.setSize(width, height)
}

// 更新场景显示
const updateSceneDisplay = () => {
  if (!scene) {
    console.log('场景未初始化，跳过显示更新')
    return
  }

  console.log('更新场景显示:', {
    showSensors: props.showSensors,
    showTrajectory: props.showTrajectory,
    sensorCount: sensorObjects.length,
    hasTrajectory: !!trajectoryLine
  })

  // 显示/隐藏传感器
  sensorObjects.forEach((sensor, index) => {
    sensor.visible = props.showSensors
    console.log(`传感器 ${index + 1} 可见性:`, sensor.visible)
  })

  // 显示/隐藏轨迹
  if (trajectoryLine) {
    trajectoryLine.visible = props.showTrajectory
    console.log('活动轨迹可见性:', trajectoryLine.visible)
  } else {
    console.log('活动轨迹对象未找到')
  }
}

// 监听属性变化
watch([
  () => props.showSensors,
  () => props.showTrajectory
], updateSceneDisplay)

// 生命周期
onMounted(() => {
  setTimeout(() => {
    initScene()
  }, 100)
})

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  
  window.removeEventListener('resize', onWindowResize)
  
  if (renderer && sceneContainer.value) {
    sceneContainer.value.removeChild(renderer.domElement)
    renderer.dispose()
  }
})
</script>

<style scoped>
.scene-container {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  border-radius: 8px;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.loading-text {
  margin-top: 16px;
  color: #666;
  font-size: 14px;
}

.scene-controls {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 5;
}
</style>
