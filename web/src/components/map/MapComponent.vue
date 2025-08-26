<template>
  <div class="map-container">
    <div class="map-header" v-if="showHeader">
      <h3 class="map-title">{{ title }}</h3>
      <div class="map-controls">
        <n-button-group size="small">
          <n-button @click="zoomIn">
            <template #icon>
              <n-icon>
                <Icon icon="mdi:plus" />
              </n-icon>
            </template>
          </n-button>
          <n-button @click="zoomOut">
            <template #icon>
              <n-icon>
                <Icon icon="mdi:minus" />
              </n-icon>
            </template>
          </n-button>
          <n-button @click="resetView">
            <template #icon>
              <n-icon>
                <Icon icon="mdi:home" />
              </n-icon>
            </template>
          </n-button>
        </n-button-group>
      </div>
    </div>
    
    <div
      ref="mapContainer"
      class="map-wrapper"
      :style="{ height: mapHeight }"
    >
      <div v-if="loading" class="map-loading">
        <n-spin size="large">
          <template #description>
            正在加载地图...
          </template>
        </n-spin>
      </div>
      <div v-if="error" class="map-error">
        <n-result status="error" title="地图加载失败" :description="error">
          <template #footer>
            <n-button @click="initMap">重新加载</n-button>
          </template>
        </n-result>
      </div>
    </div>

    <!-- 地图提示信息 -->
    <div class="map-tips" v-if="!loading && !error">
      <n-icon class="tip-icon">
        <Icon icon="mdi:information" />
      </n-icon>
      <span class="tip-text">点击地图标记可查看患者详细位置信息</span>
    </div>
  </div>
</template>

<!--
  地图组件 - MapComponent.vue

  基于高德地图API的Vue3地图组件，专为数字孪生健康管理系统设计

  主要功能：
  - 高德地图集成和显示
  - 自定义标注点和信息窗口
  - 地图控制（缩放、平移、重置）
  - 响应式设计和深色模式支持
  - 错误处理和加载状态管理

  作者：数字孪生系统开发团队
  创建时间：2024-01-01
  最后更新：2024-01-01
-->

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { Icon } from '@iconify/vue'
import AMapLoader from '@amap/amap-jsapi-loader'

const props = defineProps({
  // 地图标题
  title: {
    type: String,
    default: '位置信息'
  },
  // 是否显示头部
  showHeader: {
    type: Boolean,
    default: true
  },
  // 地图高度
  height: {
    type: String,
    default: '400px'
  },
  // 地图中心点坐标 [经度, 纬度]
  center: {
    type: Array,
    default: () => [116.397428, 39.90923] // 默认北京天安门
  },
  // 地图缩放级别
  zoom: {
    type: Number,
    default: 13
  },
  // 标注点数据
  markers: {
    type: Array,
    default: () => []
  },
  // 是否显示地图控件
  showControls: {
    type: Boolean,
    default: true
  },
  // 地图主题样式
  mapStyle: {
    type: String,
    default: 'amap://styles/normal' // normal, dark, light, fresh, grey, graffiti, macaron, blue, darkblue, wine
  }
})

const emit = defineEmits(['map-ready', 'marker-click'])

// 响应式数据
const mapContainer = ref(null)
const loading = ref(true)
const error = ref('')
const mapHeight = ref(props.height)

// 地图实例
let map = null
let markerInstances = []
let infoWindow = null
let AMapInstance = null // 存储AMap实例

// 初始化地图
const initMap = async () => {
  try {
    loading.value = true
    error.value = ''
    
    // 获取环境变量中的API Key
    const apiKey = import.meta.env.VITE_AMAP_KEY
    if (!apiKey) {
      throw new Error('未配置高德地图API Key')
    }

    // 加载高德地图API
    const AMap = await AMapLoader.load({
      key: apiKey,
      version: '2.0',
      plugins: ['AMap.Scale', 'AMap.ToolBar', 'AMap.InfoWindow']
    })

    // 存储AMap实例供其他函数使用
    AMapInstance = AMap

    // 创建地图实例
    map = new AMap.Map(mapContainer.value, {
      center: props.center,
      zoom: props.zoom,
      mapStyle: props.mapStyle,
      viewMode: '2D',
      features: ['bg', 'road', 'building', 'point'],
      resizeEnable: true,
      rotateEnable: false,
      pitchEnable: false,
      dragEnable: true,
      zoomEnable: true,
      doubleClickZoom: true,
      keyboardEnable: true,
      scrollWheel: true,
      touchZoom: true,
      touchZoomCenter: 1
    })

    // 创建信息窗口
    infoWindow = new AMap.InfoWindow({
      isCustom: false,
      autoMove: true,
      closeWhenClickMap: true
    })

    // 添加地图控件
    if (props.showControls) {
      map.addControl(new AMap.Scale({
        position: {
          bottom: '10px',
          left: '10px'
        }
      }))

      map.addControl(new AMap.ToolBar({
        position: {
          top: '10px',
          right: '10px'
        },
        locate: false,
        noIpLocate: true
      }))
    }

    // 地图加载完成
    map.on('complete', () => {
      loading.value = false
      emit('map-ready', map)
      
      // 添加标注点
      if (props.markers.length > 0) {
        addMarkers(props.markers)
      }
    })

  } catch (err) {
    console.error('地图初始化失败:', err)
    error.value = err.message || '地图加载失败'
    loading.value = false
  }
}

// 添加标注点
const addMarkers = async (markers) => {
  if (!map || !markers.length) return

  // 清除现有标注
  clearMarkers()

  // 确保AMap已加载
  if (!AMapInstance) {
    console.error('AMap未加载')
    return
  }
  const AMap = AMapInstance

  markers.forEach((markerData, index) => {
    // 创建自定义图标
    let markerIcon = null

    if (markerData.icon) {
      // 使用自定义图标
      markerIcon = markerData.icon
    } else if (markerData.iconConfig) {
      // 使用图标配置创建图标
      markerIcon = new AMap.Icon({
        size: new AMap.Size(markerData.iconConfig.size[0], markerData.iconConfig.size[1]),
        image: markerData.iconConfig.image,
        imageSize: new AMap.Size(markerData.iconConfig.imageSize[0], markerData.iconConfig.imageSize[1]),
        imageOffset: new AMap.Pixel(-16, -32)
      })
    } else {
      // 使用默认图标 - 红色位置标记样式，更大更明显
      markerIcon = new AMap.Icon({
        size: new AMap.Size(36, 48),
        image: createMarkerIcon(markerData.level || 'critical'),
        imageSize: new AMap.Size(36, 48),
        imageOffset: new AMap.Pixel(-18, -48) // 调整偏移，使图标底部对准位置点
      })
    }

    const marker = new AMap.Marker({
      position: markerData.position,
      title: markerData.title || '',
      icon: markerIcon,
      anchor: 'bottom-center',
      animation: 'AMAP_ANIMATION_DROP',
      autoRotation: false,
      zooms: [3, 20] // 设置标记在不同缩放级别下的显示范围
    })

    // 添加点击事件
    marker.on('click', (e) => {
      // 显示信息窗口
      if (markerData.infoContent) {
        showInfoWindow(markerData, e.lnglat)
      }

      // 触发父组件事件
      emit('marker-click', markerData, index, marker)
    })

    map.add(marker)
    markerInstances.push(marker)
  })

  // 自动调整地图视野以包含所有标注点
  if (markers.length > 1) {
    map.setFitView(markerInstances)
  } else if (markers.length === 1) {
    // 如果只有一个标记，将地图中心设置为该标记位置
    map.setCenter(markers[0].position)
  }
}

// 显示信息窗口
const showInfoWindow = (markerData, position) => {
  if (!infoWindow || !markerData.infoContent) return

  let content = ''

  if (typeof markerData.infoContent === 'string') {
    content = markerData.infoContent
  } else {
    // 构建HTML内容
    content = `
      <div class="marker-info">
        <div class="marker-info-header">
          <h4>${markerData.infoContent.title || markerData.title || '位置信息'}</h4>
        </div>
        <div class="marker-info-body">
          ${markerData.infoContent.content || ''}
        </div>
      </div>
    `
  }

  infoWindow.setContent(content)
  infoWindow.open(map, position)
}

// 关闭信息窗口
const closeInfoWindow = () => {
  if (infoWindow) {
    infoWindow.close()
  }
}

// 创建标注图标 - 类似红色位置标记的样式
const createMarkerIcon = (level = 'info') => {
  const colors = {
    'critical': '#ff4757',  // 红色 - 紧急
    'warning': '#ffa502',   // 橙色 - 警告
    'info': '#3742fa',      // 蓝色 - 信息
    'success': '#2ed573'    // 绿色 - 成功
  }

  const color = colors[level] || colors.critical // 默认使用红色

  // 创建红色位置标记图标 - 经典水滴形状，更大更明显
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="36" height="48" viewBox="0 0 36 48"><defs><filter id="shadow-${level}" x="-50%" y="-50%" width="200%" height="200%"><feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="rgba(0,0,0,0.5)"/></filter></defs><path d="M18 0C8.059 0 0 8.059 0 18c0 10.941 18 30 18 30s18-19.059 18-30C36 8.059 27.941 0 18 0z" fill="${color}" filter="url(#shadow-${level})"/><circle cx="18" cy="18" r="8" fill="white" opacity="0.95"/><circle cx="18" cy="18" r="4" fill="${color}"/></svg>`

  return `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`
}

// 清除所有标注点
const clearMarkers = () => {
  if (markerInstances.length > 0) {
    map.remove(markerInstances)
    markerInstances = []
  }
}

// 地图控制方法
const zoomIn = () => {
  if (map) {
    map.zoomIn()
  }
}

const zoomOut = () => {
  if (map) {
    map.zoomOut()
  }
}

const resetView = () => {
  if (map) {
    map.setCenter(props.center)
    map.setZoom(props.zoom)
  }
}

// 监听标注点数据变化
watch(() => props.markers, (newMarkers) => {
  if (map && newMarkers) {
    addMarkers(newMarkers)
  }
}, { deep: true })

// 监听中心点变化
watch(() => props.center, (newCenter) => {
  if (map && newCenter) {
    map.setCenter(newCenter)
  }
})

// 窗口大小变化处理
const handleResize = () => {
  if (map) {
    setTimeout(() => {
      map.getSize()
      map.setFitView()
    }, 100)
  }
}

// 生命周期
onMounted(async () => {
  await nextTick()
  if (mapContainer.value) {
    initMap()
  }

  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  // 清理事件监听
  window.removeEventListener('resize', handleResize)

  // 销毁地图实例
  if (map) {
    map.destroy()
    map = null
  }

  // 清理标注实例
  markerInstances = []

  // 清理信息窗口
  if (infoWindow) {
    infoWindow.close()
    infoWindow = null
  }
})

// 暴露方法给父组件
defineExpose({
  map,
  zoomIn,
  zoomOut,
  resetView,
  addMarkers,
  clearMarkers,
  showInfoWindow,
  closeInfoWindow
})
</script>

<style scoped>
.map-container {
  border: 1px solid var(--n-border-color);
  border-radius: 8px;
  overflow: hidden;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.map-container:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--n-color-hover);
  border-bottom: 1px solid var(--n-border-color);
}

.map-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--n-text-color);
}

.map-wrapper {
  position: relative;
  width: 100%;
  min-height: 200px;
}

.map-wrapper :deep(.amap-container) {
  border-radius: 0 0 8px 8px;
}

.map-tips {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background: var(--n-color-hover);
  border-top: 1px solid var(--n-border-color);
  font-size: 12px;
  color: var(--n-text-color-disabled);
}

.tip-icon {
  margin-right: 6px;
  color: var(--n-color-primary);
}

.tip-text {
  line-height: 1.4;
}

.map-loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.9);
  z-index: 1000;
}

.map-error {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  z-index: 1000;
}

/* 信息窗口样式 */
:deep(.amap-info-content) {
  .marker-info {
    min-width: 200px;
    font-family: inherit;
  }

  .marker-info-header {
    padding: 8px 12px;
    background: var(--n-color-primary);
    color: white;
    border-radius: 4px 4px 0 0;
    margin: -8px -12px 8px -12px;
  }

  .marker-info-header h4 {
    margin: 0;
    font-size: 14px;
    font-weight: 600;
  }

  .marker-info-body {
    padding: 0 4px;
    font-size: 13px;
    line-height: 1.5;
    color: var(--n-text-color);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .map-header {
    padding: 8px 12px;
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
  }

  .map-title {
    font-size: 14px;
  }

  .map-controls {
    align-self: flex-end;
  }

  .map-wrapper {
    min-height: 250px;
  }
}

@media (max-width: 480px) {
  .map-header {
    padding: 6px 8px;
  }

  .map-title {
    font-size: 13px;
  }

  .map-wrapper {
    min-height: 200px;
  }
}

/* 深色模式适配 */
@media (prefers-color-scheme: dark) {
  .map-container {
    background: var(--n-color-base);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  }

  .map-container:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
  }

  .map-error {
    background: var(--n-color-base);
  }
}
</style>
