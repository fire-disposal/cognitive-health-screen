<template>
  <n-card title="告警分析" class="alert-card">
    <template #header-extra>
      <n-tag :type="alertStatusType" size="small">
        {{ alertStatusText }}
      </n-tag>
    </template>

    <n-spin :show="loading">
      <div class="alert-content">
        <!-- 告警统计 -->
        <div class="alert-stats">
          <div class="stat-item critical">
            <div class="stat-icon">
              <n-icon size="20" color="#ffffff">
                <Icon icon="mdi:alert-circle" />
              </n-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ alertData.criticalAlerts }}</div>
              <div class="stat-label">紧急告警</div>
            </div>
          </div>
          
          <div class="stat-item warning">
            <div class="stat-icon">
              <n-icon size="20" color="#ffffff">
                <Icon icon="mdi:alert" />
              </n-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ alertData.warningAlerts }}</div>
              <div class="stat-label">警告告警</div>
            </div>
          </div>
          
          <div class="stat-item info">
            <div class="stat-icon">
              <n-icon size="20" color="#ffffff">
                <Icon icon="mdi:information" />
              </n-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ alertData.infoAlerts }}</div>
              <div class="stat-label">信息告警</div>
            </div>
          </div>
        </div>

        <!-- 告警分类统计 -->
        <div class="alert-categories">
          <h4>告警分类</h4>
          <div class="category-grid">
            <div v-for="category in alertCategories" :key="category.name" class="category-item">
              <div class="category-icon" :style="{ backgroundColor: category.color }">
                <n-icon size="14" color="#ffffff">
                  <Icon :icon="category.icon" />
                </n-icon>
              </div>
              <div class="category-content">
                <div class="category-count">{{ category.count }}</div>
                <div class="category-name">{{ category.name }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 告警趋势图 -->
        <div class="alert-trend">
          <h4>告警趋势</h4>
          <div ref="trendChartRef" class="chart" style="height: 200px; width: 100%;"></div>
        </div>
      </div>
    </n-spin>
  </n-card>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { NCard, NTag, NSpin, NIcon } from 'naive-ui'
import { Icon } from '@iconify/vue'
import * as echarts from 'echarts'

const props = defineProps({
  patientId: {
    type: [String, Number],
    required: true
  },
  data: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const trendChartRef = ref(null)
const trendChartInstance = ref(null)

// 生成模拟告警数据
const generateMockAlertData = () => {
  return {
    totalAlerts: 12,
    criticalAlerts: 2,
    warningAlerts: 5,
    infoAlerts: 5,
    recentAlerts: [
      { id: 1, time: '10:30', type: 'warning', message: '心率偏高，当前值：105 BPM' },
      { id: 2, time: '09:15', type: 'info', message: '服药提醒：降压药' },
      { id: 3, time: '08:45', type: 'critical', message: '血压异常：160/95 mmHg' },
      { id: 4, time: '08:00', type: 'info', message: '设备连接正常' }
    ],
    trendData: [
      { day: '周一', critical: 1, warning: 3, info: 2 },
      { day: '周二', critical: 0, warning: 2, info: 4 },
      { day: '周三', critical: 2, warning: 4, info: 3 },
      { day: '周四', critical: 1, warning: 1, info: 5 },
      { day: '周五', critical: 0, warning: 3, info: 2 },
      { day: '周六', critical: 1, warning: 2, info: 3 },
      { day: '周日', critical: 0, warning: 1, info: 4 }
    ]
  }
}

const alertData = computed(() => {
  const mockData = generateMockAlertData()
  console.log('Alert data computed:', mockData)
  return props.data || mockData
})

// 告警分类统计
const alertCategories = computed(() => {
  return [
    { name: '生命体征', count: 3, color: '#dc2626', icon: 'mdi:heart-pulse' },
    { name: '设备异常', count: 2, color: '#d97706', icon: 'mdi:alert-circle' },
    { name: '药物提醒', count: 4, color: '#2563eb', icon: 'mdi:pill' },
    { name: '活动异常', count: 1, color: '#7c3aed', icon: 'mdi:run' },
    { name: '环境告警', count: 2, color: '#059669', icon: 'mdi:home-alert' }
  ]
})

// 告警状态
const alertStatusType = computed(() => {
  if (alertData.value.criticalAlerts > 0) return 'error'
  if (alertData.value.warningAlerts > 0) return 'warning'
  return 'success'
})

const alertStatusText = computed(() => {
  if (alertData.value.criticalAlerts > 0) return '需要关注'
  if (alertData.value.warningAlerts > 0) return '有警告'
  return '状态正常'
})

// 获取告警相关样式
const getAlertClass = (type) => {
  return `alert-${type}`
}

const getAlertTagType = (type) => {
  const types = {
    critical: 'error',
    warning: 'warning',
    info: 'info'
  }
  return types[type] || 'default'
}

const getAlertTypeText = (type) => {
  const texts = {
    critical: '紧急',
    warning: '警告',
    info: '信息'
  }
  return texts[type] || '未知'
}

// 初始化趋势图
const initTrendChart = () => {
  if (!trendChartRef.value) {
    console.log('trendChartRef.value is null')
    return
  }

  try {
    trendChartInstance.value = echarts.init(trendChartRef.value)
    console.log('Trend chart initialized successfully')
    updateTrendChart()
  } catch (error) {
    console.error('Error initializing trend chart:', error)
  }
}

const updateTrendChart = () => {
  if (!trendChartInstance.value) {
    console.log('trendChartInstance.value is null')
    return
  }

  // 直接使用模拟数据，确保数据结构正确
  const mockData = generateMockAlertData()
  const trendData = mockData.trendData || []
  console.log('Trend data:', trendData)
  if (!trendData || trendData.length === 0) {
    console.log('No trend data available')
    return
  }

  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e2e8f0',
      textStyle: { color: '#374151' }
    },
    legend: {
      data: ['紧急', '警告', '信息'],
      bottom: 0,
      textStyle: { color: '#6b7280', fontSize: 11 }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '20%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: trendData.map(item => item.day),
      axisLine: { lineStyle: { color: '#e2e8f0' } },
      axisTick: { lineStyle: { color: '#e2e8f0' } },
      axisLabel: { color: '#6b7280', fontSize: 10 }
    },
    yAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: '#e2e8f0' } },
      axisTick: { lineStyle: { color: '#e2e8f0' } },
      axisLabel: { color: '#6b7280', fontSize: 10 },
      splitLine: { lineStyle: { color: '#f3f4f6' } }
    },
    series: [
      {
        name: '紧急',
        type: 'bar',
        stack: 'alerts',
        data: trendData.map(item => item.critical),
        itemStyle: { color: '#dc2626' },
        barWidth: '60%'
      },
      {
        name: '警告',
        type: 'bar',
        stack: 'alerts',
        data: trendData.map(item => item.warning),
        itemStyle: { color: '#d97706' }
      },
      {
        name: '信息',
        type: 'bar',
        stack: 'alerts',
        data: trendData.map(item => item.info),
        itemStyle: { color: '#2563eb' }
      }
    ]
  }
  
  try {
    trendChartInstance.value.setOption(option, true)
    console.log('Trend chart updated successfully')
  } catch (error) {
    console.error('Error updating trend chart:', error)
  }
}

// 监听数据变化
watch(() => props.data, () => {
  nextTick(() => {
    updateTrendChart()
  })
})

// 监听告警数据变化
watch(() => alertData.value, (newVal) => {
  console.log('Alert data changed:', newVal)
  nextTick(() => {
    updateTrendChart()
  })
}, { deep: true, immediate: true })

// 生命周期
onMounted(() => {

  nextTick(() => {
    setTimeout(() => {
      initTrendChart()
      // 再次尝试初始化，确保图表能够显示
      setTimeout(() => {
        if (trendChartInstance.value) {
          updateTrendChart()
        }
      }, 500)
      // 第三次尝试，强制使用模拟数据
      setTimeout(() => {
        if (trendChartInstance.value) {
          console.log('Force updating trend chart with mock data')
          const mockData = generateMockAlertData()
          const trendData = mockData.trendData || []
          if (trendData.length > 0) {
            const option = {
              tooltip: {
                trigger: 'axis',
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                borderColor: '#e2e8f0',
                textStyle: { color: '#374151' }
              },
              legend: {
                data: ['紧急', '警告', '信息'],
                bottom: 0,
                textStyle: { color: '#6b7280', fontSize: 10 },
                itemWidth: 12,
                itemHeight: 8
              },
              grid: {
                left: '8%',
                right: '4%',
                bottom: '25%',
                top: '10%',
                containLabel: true
              },
              xAxis: {
                type: 'category',
                data: trendData.map(item => item.day),
                axisLine: { lineStyle: { color: '#e5e7eb' } },
                axisTick: { lineStyle: { color: '#e5e7eb' } },
                axisLabel: { color: '#6b7280', fontSize: 9 }
              },
              yAxis: {
                type: 'value',
                axisLine: { lineStyle: { color: '#e5e7eb' } },
                axisTick: { lineStyle: { color: '#e5e7eb' } },
                axisLabel: { color: '#6b7280', fontSize: 9 },
                splitLine: { lineStyle: { color: '#f3f4f6' } }
              },
              series: [
                {
                  name: '紧急',
                  type: 'bar',
                  stack: 'alerts',
                  data: trendData.map(item => item.critical),
                  itemStyle: { color: '#dc2626' },
                  barWidth: '60%'
                },
                {
                  name: '警告',
                  type: 'bar',
                  stack: 'alerts',
                  data: trendData.map(item => item.warning),
                  itemStyle: { color: '#d97706' }
                },
                {
                  name: '信息',
                  type: 'bar',
                  stack: 'alerts',
                  data: trendData.map(item => item.info),
                  itemStyle: { color: '#2563eb' }
                }
              ]
            }
            trendChartInstance.value.setOption(option, true)
            console.log('Trend chart force updated successfully')
          }
        }
      }, 1000)
    }, 100)
  })
})

// 窗口大小变化时重绘图表
const handleResize = () => {
  if (trendChartInstance.value) {
    trendChartInstance.value.resize()
  }
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (trendChartInstance.value) {
    trendChartInstance.value.dispose()
  }
})
</script>

<style scoped>
.alert-card {
  height: 100%;
}

.alert-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 告警统计 */
.alert-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-radius: 12px;
  color: white;
}

.stat-item.critical {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.stat-item.warning {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.stat-item.info {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  opacity: 0.9;
}

/* 告警分类统计 */
.alert-categories h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
}

.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 8px;
  background: #ffffff;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.category-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.category-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.category-content {
  text-align: center;
}

.category-count {
  font-size: 16px;
  font-weight: 700;
  color: #374151;
  margin-bottom: 2px;
}

.category-name {
  font-size: 9px;
  color: #6b7280;
  font-weight: 500;
}

/* 告警趋势 */
.alert-trend h4 {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: #374151;
}

.chart {
  width: 100%;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .alert-stats {
    grid-template-columns: 1fr;
  }
  
  .stat-item {
    padding: 12px;
  }
  
  .stat-icon {
    width: 36px;
    height: 36px;
  }
  
  .stat-value {
    font-size: 20px;
  }
}
</style>
