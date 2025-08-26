<template>
  <n-card title="设备状态分析" class="device-status-card">
    <template #header-extra>
      <n-tag :type="overallStatusType" size="small">
        {{ overallStatusText }}
      </n-tag>
    </template>

    <n-spin :show="loading">
      <div class="device-content">
        <!-- 设备概览 -->
        <div class="device-overview">
          <div class="overview-stats">
            <div class="stat-card online">
              <div class="stat-icon">
                <n-icon size="16" color="#059669">
                  <Icon icon="mdi:check-circle" />
                </n-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ deviceStats.online }}</div>
                <div class="stat-label">在线</div>
              </div>
            </div>
            <div class="stat-card offline">
              <div class="stat-icon">
                <n-icon size="16" color="#dc2626">
                  <Icon icon="mdi:close-circle" />
                </n-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ deviceStats.offline }}</div>
                <div class="stat-label">离线</div>
              </div>
            </div>
            <div class="stat-card warning">
              <div class="stat-icon">
                <n-icon size="16" color="#d97706">
                  <Icon icon="mdi:alert-circle" />
                </n-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ deviceStats.warning }}</div>
                <div class="stat-label">异常</div>
              </div>
            </div>
            <div class="stat-card total">
              <div class="stat-icon">
                <n-icon size="16" color="#2563eb">
                  <Icon icon="mdi:devices" />
                </n-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ deviceStats.total }}</div>
                <div class="stat-label">总计</div>
              </div>
            </div>
            <div class="stat-card usage">
              <div class="stat-icon">
                <n-icon size="16" color="#7c3aed">
                  <Icon icon="mdi:chart-line" />
                </n-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ deviceStats.usage }}%</div>
                <div class="stat-label">使用率</div>
              </div>
            </div>
            <div class="stat-card battery">
              <div class="stat-icon">
                <n-icon size="16" color="#0891b2">
                  <Icon icon="mdi:battery" />
                </n-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ deviceStats.avgBattery }}%</div>
                <div class="stat-label">平均电量</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 设备列表 -->
        <div class="device-list">
          <div v-for="device in deviceList" :key="device.id" class="device-item">
            <div class="device-info">
              <div class="device-icon">
                <n-icon size="24" :color="getDeviceIconColor(device.type)">
                  <Icon :icon="getDeviceIcon(device.type)" />
                </n-icon>
              </div>
              <div class="device-details">
                <div class="device-name">{{ device.name }}</div>
                <div class="device-type">{{ device.type }}</div>
              </div>
            </div>
            
            <div class="device-status">
              <n-tag
                :type="getStatusTagType(device.status)"
                size="small"
                class="status-tag"
              >
                <template #icon>
                  <n-icon>
                    <Icon :icon="getStatusIcon(device.status)" />
                  </n-icon>
                </template>
                {{ getStatusText(device.status) }}
              </n-tag>
              <div class="last-update">{{ device.lastUpdate }}</div>
            </div>
            
            <div class="device-metrics" v-if="device.metrics">
              <div class="metric" v-for="metric in device.metrics" :key="metric.name">
                <span class="metric-name">{{ metric.name }}</span>
                <span class="metric-value" :class="getMetricClass(metric.status)">
                  {{ metric.value }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 设备使用率图表 -->
        <div class="usage-chart">
          <h4>设备使用率趋势</h4>
          <div ref="usageChartRef" class="chart" style="height: 200px; width: 100%;"></div>
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

const usageChartRef = ref(null)
const usageChartInstance = ref(null)

// 生成模拟设备数据
const generateMockDeviceData = () => {
  return {
    devices: [
      {
        id: 1,
        name: '心率监测器',
        type: '心率监测',
        status: 'online',
        lastUpdate: '2分钟前',
        metrics: [
          { name: '心率', value: '72 BPM', status: 'normal' },
          { name: '电量', value: '85%', status: 'good' }
        ]
      },
      {
        id: 2,
        name: '血压计',
        type: '血压监测',
        status: 'online',
        lastUpdate: '5分钟前',
        metrics: [
          { name: '血压', value: '120/80', status: 'normal' },
          { name: '电量', value: '92%', status: 'good' }
        ]
      },
      {
        id: 3,
        name: '体温计',
        type: '体温监测',
        status: 'offline',
        lastUpdate: '2小时前',
        metrics: [
          { name: '体温', value: '--', status: 'unknown' },
          { name: '电量', value: '15%', status: 'low' }
        ]
      },
      {
        id: 4,
        name: '血氧仪',
        type: '血氧监测',
        status: 'warning',
        lastUpdate: '10分钟前',
        metrics: [
          { name: '血氧', value: '94%', status: 'low' },
          { name: '电量', value: '68%', status: 'normal' }
        ]
      }
    ],
    usageData: [
      { day: '周一', usage: 85 },
      { day: '周二', usage: 78 },
      { day: '周三', usage: 92 },
      { day: '周四', usage: 88 },
      { day: '周五', usage: 95 },
      { day: '周六', usage: 72 },
      { day: '周日', usage: 68 }
    ]
  }
}

// 当前设备数据
const currentData = computed(() => {
  const mockData = generateMockDeviceData()
  console.log('Device data computed:', mockData)
  return props.data || mockData
})

const deviceList = computed(() => {
  return currentData.value.devices || []
})

// 设备统计
const deviceStats = computed(() => {
  const devices = deviceList.value
  const online = devices.filter(d => d.status === 'online').length
  const offline = devices.filter(d => d.status === 'offline').length
  const warning = devices.filter(d => d.status === 'warning').length
  const total = devices.length
  const usage = total > 0 ? Math.round((online / total) * 100) : 0

  // 计算平均电量
  const batteries = devices.map(d => {
    const batteryMetric = d.metrics?.find(m => m.name === '电量')
    return batteryMetric ? parseInt(batteryMetric.value) : 0
  }).filter(b => b > 0)
  const avgBattery = batteries.length > 0 ? Math.round(batteries.reduce((a, b) => a + b, 0) / batteries.length) : 0

  return { online, offline, warning, total, usage, avgBattery }
})

// 整体状态
const overallStatusType = computed(() => {
  const { online, total } = deviceStats.value
  if (total === 0) return 'default'
  const ratio = online / total
  if (ratio >= 0.8) return 'success'
  if (ratio >= 0.5) return 'warning'
  return 'error'
})

const overallStatusText = computed(() => {
  const types = {
    success: '状态良好',
    warning: '部分异常',
    error: '需要关注',
    default: '无设备'
  }
  return types[overallStatusType.value]
})

// 获取设备图标
const getDeviceIcon = (type) => {
  const icons = {
    '心率监测': 'mdi:heart-pulse',
    '血压监测': 'mdi:heart-box',
    '体温监测': 'mdi:thermometer',
    '血氧监测': 'mdi:lungs',
    '血糖监测': 'mdi:water-percent',
    '体重监测': 'mdi:scale-bathroom'
  }
  return icons[type] || 'mdi:devices'
}

const getDeviceIconColor = (type) => {
  const colors = {
    '心率监测': '#ef4444',
    '血压监测': '#3b82f6',
    '体温监测': '#f59e0b',
    '血氧监测': '#10b981',
    '血糖监测': '#8b5cf6',
    '体重监测': '#06b6d4'
  }
  return colors[type] || '#6b7280'
}

// 获取状态相关
const getStatusTagType = (status) => {
  const types = {
    online: 'success',
    offline: 'error',
    warning: 'warning',
    maintenance: 'info'
  }
  return types[status] || 'default'
}

const getStatusIcon = (status) => {
  const icons = {
    online: 'mdi:check-circle',
    offline: 'mdi:close-circle',
    warning: 'mdi:alert-circle',
    maintenance: 'mdi:wrench'
  }
  return icons[status] || 'mdi:help-circle'
}

const getStatusText = (status) => {
  const texts = {
    online: '在线',
    offline: '离线',
    warning: '异常',
    maintenance: '维护中'
  }
  return texts[status] || '未知'
}

// 获取指标样式
const getMetricClass = (status) => {
  return {
    'metric-normal': status === 'normal' || status === 'good',
    'metric-warning': status === 'warning' || status === 'low',
    'metric-error': status === 'error' || status === 'critical',
    'metric-unknown': status === 'unknown'
  }
}

// 初始化使用率图表
const initUsageChart = () => {
  if (!usageChartRef.value) {
    console.log('usageChartRef.value is null')
    return
  }

  try {
    usageChartInstance.value = echarts.init(usageChartRef.value)
    console.log('Usage chart initialized successfully')
    updateUsageChart()
  } catch (error) {
    console.error('Error initializing usage chart:', error)
  }
}

const updateUsageChart = () => {
  if (!usageChartInstance.value) {
    console.log('usageChartInstance.value is null')
    return
  }

  // 直接使用模拟数据，确保数据结构正确
  const mockData = generateMockDeviceData()
  const usageData = mockData.usageData || []
  console.log('Usage data:', usageData)
  if (!usageData || usageData.length === 0) {
    console.log('No usage data available')
    return
  }

  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e2e8f0',
      textStyle: { color: '#374151' },
      formatter: function(params) {
        return `${params[0].name}<br/>${params[0].seriesName}: ${params[0].value}%`
      }
    },
    grid: {
      left: '8%',
      right: '4%',
      bottom: '8%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: usageData.map(item => item.day),
      axisLine: { lineStyle: { color: '#e5e7eb' } },
      axisTick: { lineStyle: { color: '#e5e7eb' } },
      axisLabel: { color: '#6b7280', fontSize: 9 }
    },
    yAxis: {
      type: 'value',
      name: '使用率(%)',
      min: 0,
      max: 100,
      axisLine: { lineStyle: { color: '#e5e7eb' } },
      axisTick: { lineStyle: { color: '#e5e7eb' } },
      axisLabel: { color: '#6b7280', fontSize: 9 },
      splitLine: { lineStyle: { color: '#f3f4f6' } },
      nameTextStyle: { color: '#6b7280', fontSize: 9 }
    },
    series: [{
      name: '设备使用率',
      type: 'bar',
      data: usageData.map(item => item.usage),
      itemStyle: {
        color: '#059669',
        borderRadius: [2, 2, 0, 0]
      },
      barWidth: '50%',
      emphasis: {
        itemStyle: {
          color: '#047857'
        }
      }
    }]
  }

  try {
    usageChartInstance.value.setOption(option, true)
    console.log('Usage chart updated successfully')
  } catch (error) {
    console.error('Error updating usage chart:', error)
  }
}

// 监听数据变化
watch(() => props.data, () => {
  nextTick(() => {
    updateUsageChart()
  })
})

// 监听设备数据变化
watch(() => currentData.value, (newVal) => {
  console.log('Device data changed:', newVal)
  nextTick(() => {
    updateUsageChart()
  })
}, { deep: true, immediate: true })

// 生命周期
onMounted(() => {

  nextTick(() => {
    setTimeout(() => {
      initUsageChart()
      // 再次尝试初始化，确保图表能够显示
      setTimeout(() => {
        if (usageChartInstance.value) {
          updateUsageChart()
        }
      }, 500)
      // 第三次尝试，强制使用模拟数据
      setTimeout(() => {
        if (usageChartInstance.value) {
          console.log('Force updating usage chart with mock data')
          const mockData = generateMockDeviceData()
          const usageData = mockData.usageData || []
          if (usageData.length > 0) {
            const option = {
              tooltip: {
                trigger: 'axis',
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                borderColor: '#e2e8f0',
                textStyle: { color: '#374151' },
                formatter: function(params) {
                  return `${params[0].name}<br/>${params[0].seriesName}: ${params[0].value}%`
                }
              },
              grid: {
                left: '8%',
                right: '4%',
                bottom: '0%',
                top: '5%',
                containLabel: true
              },
              xAxis: {
                type: 'category',
                data: usageData.map(item => item.day),
                axisLine: { lineStyle: { color: '#e5e7eb' } },
                axisTick: { lineStyle: { color: '#e5e7eb' } },
                axisLabel: { color: '#6b7280', fontSize: 9 }
              },
              yAxis: {
                type: 'value',
                name: '使用率(%)',
                min: 0,
                max: 100,
                axisLine: { lineStyle: { color: '#e5e7eb' } },
                axisTick: { lineStyle: { color: '#e5e7eb' } },
                axisLabel: { color: '#6b7280', fontSize: 9 },
                splitLine: { lineStyle: { color: '#f3f4f6' } },
                nameTextStyle: { color: '#6b7280', fontSize: 9 }
              },
              series: [{
                name: '设备使用率',
                type: 'bar',
                data: usageData.map(item => item.usage),
                itemStyle: {
                  color: '#059669',
                  borderRadius: [2, 2, 0, 0]
                },
                barWidth: '50%',
                emphasis: {
                  itemStyle: {
                    color: '#047857'
                  }
                }
              }]
            }
            usageChartInstance.value.setOption(option, true)
            console.log('Usage chart force updated successfully')
          }
        }
      }, 1000)
    }, 100)
  })
})

onUnmounted(() => {
  if (usageChartInstance.value) {
    usageChartInstance.value.dispose()
  }
})
</script>

<style scoped>
.device-status-card {
  height: 100%;
}

.device-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 设备概览 */
.device-overview {
  padding: 12px;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.overview-stats {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 8px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
  border: 1px solid #e5e7eb;
}

.stat-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-card.online {
  background: #f0fdf4;
  border-color: #059669;
}

.stat-card.offline {
  background: #fef2f2;
  border-color: #dc2626;
}

.stat-card.warning {
  background: #fffbeb;
  border-color: #d97706;
}

.stat-card.total {
  background: #eff6ff;
  border-color: #2563eb;
}

.stat-card.usage {
  background: #faf5ff;
  border-color: #7c3aed;
}

.stat-card.battery {
  background: #f0f9ff;
  border-color: #0891b2;
}

.stat-icon {
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
  text-align: center;
}

.stat-number {
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 1px;
  color: #1f2937;
}

.stat-label {
  font-size: 9px;
  color: #6b7280;
  font-weight: 500;
}

/* 设备列表 */
.device-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.device-item {
  display: flex;
  align-items: center;
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
  border-left: 4px solid #e2e8f0;
  transition: all 0.3s ease;
}

.device-item:hover {
  background: #f1f5f9;
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.device-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.device-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.device-details {
  flex: 1;
}

.device-name {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 4px;
}

.device-type {
  font-size: 12px;
  color: #6b7280;
}

.device-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  margin: 0 16px;
}

.last-update {
  font-size: 11px;
  color: #9ca3af;
}

.device-metrics {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 120px;
}

.metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
}

.metric-name {
  color: #6b7280;
}

.metric-value {
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
}

.metric-normal {
  background: #dcfce7;
  color: #166534;
}

.metric-warning {
  background: #fef3c7;
  color: #92400e;
}

.metric-error {
  background: #fee2e2;
  color: #dc2626;
}

.metric-unknown {
  background: #f3f4f6;
  color: #6b7280;
}

/* 使用率图表 */
.usage-chart {
  padding: 16px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.usage-chart h4 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #374151;
}

.chart {
  width: 100%;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .overview-stats {
    flex-direction: column;
    gap: 16px;
  }

  .stat-circle {
    min-width: 60px;
    min-height: 60px;
    padding: 12px;
  }

  .stat-number {
    font-size: 20px;
  }

  .device-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .device-info {
    width: 100%;
  }

  .device-status {
    flex-direction: row;
    align-items: center;
    margin: 0;
  }

  .device-metrics {
    width: 100%;
    flex-direction: row;
    justify-content: space-around;
  }
}

@media (max-width: 480px) {
  .device-content {
    gap: 16px;
  }

  .device-item {
    padding: 12px;
  }

  .device-icon {
    width: 40px;
    height: 40px;
  }

  .device-metrics {
    flex-direction: column;
  }
}
</style>
