<template>
  <n-card title="数据统计总览" size="small" class="data-statistics">
    <template #header-extra>
      <n-space>
        <n-select
          v-model:value="selectedTimeRange"
          size="small"
          style="width: 100px"
          :options="timeRangeOptions"
          @update:value="refreshStatistics"
        />
        <n-button size="small" @click="refreshStatistics">
          <template #icon>
            <n-icon>
              <Icon icon="mdi:refresh" />
            </n-icon>
          </template>
        </n-button>
      </n-space>
    </template>

    <!-- MQTT统计 -->
    <div class="mqtt-statistics">
      <h4 class="section-title">
        <n-icon size="16" class="mr-2">
          <Icon icon="mdi:message-processing" />
        </n-icon>
        MQTT消息统计
      </h4>
      <n-grid :cols="4" :x-gap="12" :y-gap="8">
        <n-grid-item>
          <div class="stat-card mqtt">
            <div class="stat-icon">
              <n-icon size="20" color="#1890ff">
                <Icon icon="mdi:message-arrow-right" />
              </n-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ mqttStats.totalMessages }}</div>
              <div class="stat-label">总消息数</div>
            </div>
          </div>
        </n-grid-item>
        <n-grid-item>
          <div class="stat-card mqtt">
            <div class="stat-icon">
              <n-icon size="20" color="#52c41a">
                <Icon icon="mdi:clock-fast" />
              </n-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ mqttStats.todayMessages }}</div>
              <div class="stat-label">今日消息</div>
            </div>
          </div>
        </n-grid-item>
        <n-grid-item>
          <div class="stat-card mqtt">
            <div class="stat-icon">
              <n-icon size="20" color="#fa8c16">
                <Icon icon="mdi:heart-pulse" />
              </n-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ mqttStats.heartRateMessages }}</div>
              <div class="stat-label">心率数据</div>
            </div>
          </div>
        </n-grid-item>
        <n-grid-item>
          <div class="stat-card mqtt">
            <div class="stat-icon">
              <n-icon size="20" color="#722ed1">
                <Icon icon="mdi:thermometer" />
              </n-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ mqttStats.temperatureMessages }}</div>
              <div class="stat-label">体温数据</div>
            </div>
          </div>
        </n-grid-item>
      </n-grid>
    </div>

    <n-divider style="margin: 16px 0;" />

    <!-- 系统统计 -->
    <div class="system-statistics">
      <h4 class="section-title">
        <n-icon size="16" class="mr-2">
          <Icon icon="mdi:chart-line" />
        </n-icon>
        系统统计
      </h4>
      <n-grid :cols="3" :x-gap="12" :y-gap="8">
        <n-grid-item>
          <div class="stat-card system">
            <div class="stat-header">
              <n-icon size="16" color="#1890ff">
                <Icon icon="mdi:devices" />
              </n-icon>
              <span>设备统计</span>
            </div>
            <div class="stat-details">
              <div class="stat-item">
                <span class="label">总设备:</span>
                <span class="value">{{ deviceStats.total }}</span>
              </div>
              <div class="stat-item">
                <span class="label">已绑定:</span>
                <span class="value">{{ deviceStats.bound }}</span>
              </div>
              <div class="stat-item">
                <span class="label">在线:</span>
                <span class="value">{{ deviceStats.online }}</span>
              </div>
            </div>
          </div>
        </n-grid-item>
        <n-grid-item>
          <div class="stat-card system">
            <div class="stat-header">
              <n-icon size="16" color="#52c41a">
                <Icon icon="mdi:account-group" />
              </n-icon>
              <span>患者统计</span>
            </div>
            <div class="stat-details">
              <div class="stat-item">
                <span class="label">总患者:</span>
                <span class="value">{{ patientStats.total }}</span>
              </div>
              <div class="stat-item">
                <span class="label">活跃:</span>
                <span class="value">{{ patientStats.active }}</span>
              </div>
              <div class="stat-item">
                <span class="label">男性:</span>
                <span class="value">{{ patientStats.male }}</span>
              </div>
            </div>
          </div>
        </n-grid-item>
        <n-grid-item>
          <div class="stat-card system">
            <div class="stat-header">
              <n-icon size="16" color="#fa8c16">
                <Icon icon="mdi:database" />
              </n-icon>
              <span>数据统计</span>
            </div>
            <div class="stat-details">
              <div class="stat-item">
                <span class="label">总记录:</span>
                <span class="value">{{ healthDataStats.total }}</span>
              </div>
              <div class="stat-item">
                <span class="label">今日:</span>
                <span class="value">{{ healthDataStats.today }}</span>
              </div>
              <div class="stat-item">
                <span class="label">异常:</span>
                <span class="value">{{ healthDataStats.abnormal }}</span>
              </div>
            </div>
          </div>
        </n-grid-item>
      </n-grid>
    </div>

    <n-divider style="margin: 16px 0;" />

    <!-- 数据分类统计 -->
    <div class="category-statistics">
      <h4 class="section-title">
        <n-icon size="16" class="mr-2">
          <Icon icon="mdi:chart-pie" />
        </n-icon>
        数据分类统计
      </h4>
      <n-spin :show="loading">
        <n-grid :cols="2" :x-gap="12">
          <n-grid-item>
            <div class="chart-container">
              <div class="chart-title">数据类型分布</div>
              <div ref="dataTypeChartRef" class="chart"></div>
            </div>
          </n-grid-item>
          <n-grid-item>
            <div class="chart-container">
              <div class="chart-title">设备状态分布</div>
              <div ref="deviceStatusChartRef" class="chart"></div>
            </div>
          </n-grid-item>
        </n-grid>
      </n-spin>
    </div>
  </n-card>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, nextTick } from 'vue'
import { Icon } from '@iconify/vue'
import * as echarts from 'echarts'
import api from '@/api'

// 响应式数据
const loading = ref(false)
const selectedTimeRange = ref('today')
const dataTypeChartRef = ref(null)
const deviceStatusChartRef = ref(null)

// 统计数据
const mqttStats = reactive({
  totalMessages: 0,
  todayMessages: 0,
  heartRateMessages: 0,
  temperatureMessages: 0
})

const deviceStats = reactive({
  total: 0,
  bound: 0,
  online: 0,
  offline: 0
})

const patientStats = reactive({
  total: 0,
  active: 0,
  inactive: 0,
  male: 0,
  female: 0
})

const healthDataStats = reactive({
  total: 0,
  today: 0,
  abnormal: 0
})

// 配置选项
const timeRangeOptions = [
  { label: '今日', value: 'today' },
  { label: '本周', value: 'week' },
  { label: '本月', value: 'month' }
]

// 图表实例
let dataTypeChart = null
let deviceStatusChart = null

// 获取设备统计
const fetchDeviceStatistics = async () => {
  try {
    const response = await api.getDeviceStatistics()
    const data = response.data || {}
    
    deviceStats.total = data.total || 0
    deviceStats.bound = data.bound || 0
    deviceStats.online = (data.status_stat?.online) || 0
    deviceStats.offline = (data.status_stat?.offline) || 0
  } catch (error) {
    console.error('获取设备统计失败:', error)
  }
}

// 获取患者统计
const fetchPatientStatistics = async () => {
  try {
    const response = await api.getPatientStatistics()
    const data = response.data || {}
    
    patientStats.total = data.total || 0
    patientStats.active = (data.status_stat?.active) || 0
    patientStats.inactive = (data.status_stat?.inactive) || 0
    patientStats.male = (data.gender_stat?.male) || 0
    patientStats.female = (data.gender_stat?.female) || 0
  } catch (error) {
    console.error('获取患者统计失败:', error)
  }
}

// 获取健康数据统计
const fetchHealthDataStatistics = async () => {
  try {
    const response = await api.getHealthDataStatistics()
    const data = response.data || {}
    
    healthDataStats.total = data.total || 0
    healthDataStats.today = data.today || 0
    healthDataStats.abnormal = data.abnormal || 0
  } catch (error) {
    console.error('获取健康数据统计失败:', error)
  }
}

// 模拟MQTT统计数据
const generateMqttStatistics = () => {
  // 基于现有数据模拟MQTT统计
  const baseMessages = healthDataStats.total || 0
  mqttStats.totalMessages = baseMessages
  mqttStats.todayMessages = healthDataStats.today || 0
  mqttStats.heartRateMessages = Math.floor(baseMessages * 0.4)
  mqttStats.temperatureMessages = Math.floor(baseMessages * 0.3)
}

// 初始化数据类型图表
const initDataTypeChart = () => {
  if (!dataTypeChartRef.value) return
  
  dataTypeChart = echarts.init(dataTypeChartRef.value)
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    series: [
      {
        name: '数据类型',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '14',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: [
          { value: mqttStats.heartRateMessages, name: '心率数据', itemStyle: { color: '#fa8c16' } },
          { value: mqttStats.temperatureMessages, name: '体温数据', itemStyle: { color: '#722ed1' } },
          { value: Math.floor(mqttStats.totalMessages * 0.2), name: '血压数据', itemStyle: { color: '#1890ff' } },
          { value: Math.floor(mqttStats.totalMessages * 0.1), name: '其他数据', itemStyle: { color: '#52c41a' } }
        ]
      }
    ]
  }
  
  dataTypeChart.setOption(option)
}

// 初始化设备状态图表
const initDeviceStatusChart = () => {
  if (!deviceStatusChartRef.value) return
  
  deviceStatusChart = echarts.init(deviceStatusChartRef.value)
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    series: [
      {
        name: '设备状态',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '14',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: [
          { value: deviceStats.online, name: '在线', itemStyle: { color: '#52c41a' } },
          { value: deviceStats.offline, name: '离线', itemStyle: { color: '#f5222d' } },
          { value: deviceStats.total - deviceStats.bound, name: '未绑定', itemStyle: { color: '#d9d9d9' } }
        ]
      }
    ]
  }
  
  deviceStatusChart.setOption(option)
}

// 刷新统计数据
const refreshStatistics = async () => {
  loading.value = true
  try {
    await Promise.all([
      fetchDeviceStatistics(),
      fetchPatientStatistics(),
      fetchHealthDataStatistics()
    ])
    
    generateMqttStatistics()
    
    await nextTick()
    initDataTypeChart()
    initDeviceStatusChart()
  } catch (error) {
    console.error('刷新统计数据失败:', error)
    window.$message?.error('刷新统计数据失败')
  } finally {
    loading.value = false
  }
}

// 窗口大小变化时重新调整图表
const handleResize = () => {
  dataTypeChart?.resize()
  deviceStatusChart?.resize()
}

// 生命周期
onMounted(() => {
  refreshStatistics()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  dataTypeChart?.dispose()
  deviceStatusChart?.dispose()
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.data-statistics {
  height: 100%;
}

.section-title {
  display: flex;
  align-items: center;
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 500;
}

.stat-card {
  padding: 12px;
  border-radius: 8px;
  background: var(--n-color-hover);
  transition: all 0.2s;
}

.stat-card:hover {
  background: var(--n-color-pressed);
  transform: translateY(-2px);
}

.stat-card.mqtt {
  display: flex;
  align-items: center;
}

.stat-icon {
  margin-right: 12px;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 16px;
  font-weight: 600;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: var(--n-text-color-2);
}

.stat-card.system {
  padding: 12px;
}

.stat-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
  font-size: 13px;
  font-weight: 500;
}

.stat-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.stat-item .label {
  color: var(--n-text-color-2);
}

.stat-item .value {
  font-weight: 500;
  color: var(--n-text-color);
}

.chart-container {
  background: var(--n-color-hover);
  border-radius: 8px;
  padding: 12px;
}

.chart-title {
  text-align: center;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 8px;
  color: var(--n-text-color);
}

.chart {
  height: 160px;
}
</style>
