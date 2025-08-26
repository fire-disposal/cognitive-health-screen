<template>
  <n-card title="健康数据趋势" class="health-trends-card">
    <template #header-extra>
      <n-select
        v-model:value="selectedMetric"
        :options="metricOptions"
        size="small"
        style="width: 120px"
        @update:value="updateChart"
      />
    </template>

    <n-spin :show="loading">
      <div class="chart-container">
        <div ref="chartRef" class="chart" style="height: 300px;"></div>
        
        <!-- 数据统计 -->
        <div class="trend-stats">
          <div class="stat-item avg">
            <div class="stat-value">{{ currentStats.average }}</div>
            <div class="stat-label">平均</div>
          </div>
          <div class="stat-item max">
            <div class="stat-value">{{ currentStats.max }}</div>
            <div class="stat-label">最高</div>
          </div>
          <div class="stat-item min">
            <div class="stat-value">{{ currentStats.min }}</div>
            <div class="stat-label">最低</div>
          </div>
          <div class="stat-item trend">
            <div class="stat-value" :class="trendClass">
              <n-icon size="12">
                <Icon :icon="trendIcon" />
              </n-icon>
              {{ trendText }}
            </div>
            <div class="stat-label">趋势</div>
          </div>
          <div class="stat-item variance">
            <div class="stat-value">{{ currentStats.variance }}</div>
            <div class="stat-label">波动</div>
          </div>
          <div class="stat-item count">
            <div class="stat-value">{{ currentStats.count }}</div>
            <div class="stat-label">记录</div>
          </div>
        </div>
      </div>
    </n-spin>
  </n-card>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { NCard, NSelect, NSpin, NIcon } from 'naive-ui'
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

const chartRef = ref(null)
const chartInstance = ref(null)
const selectedMetric = ref('heartRate')

// 指标选项
const metricOptions = [
  { label: '心率', value: 'heartRate' },
  { label: '血压', value: 'bloodPressure' },
  { label: '体温', value: 'temperature' },
  { label: '血氧', value: 'oxygenSaturation' }
]

// 生成模拟数据
const generateMockData = () => {
  const now = new Date()
  const data = {
    heartRate: [],
    bloodPressure: [],
    temperature: [],
    oxygenSaturation: []
  }

  for (let i = 23; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 60 * 60 * 1000)
    const timeStr = time.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
    
    data.heartRate.push({
      time: timeStr,
      value: 70 + Math.random() * 20
    })
    
    data.bloodPressure.push({
      time: timeStr,
      systolic: 120 + Math.random() * 20,
      diastolic: 80 + Math.random() * 10
    })
    
    data.temperature.push({
      time: timeStr,
      value: 36.5 + Math.random() * 1
    })
    
    data.oxygenSaturation.push({
      time: timeStr,
      value: 95 + Math.random() * 5
    })
  }
  
  return data
}

// 当前数据
const currentData = computed(() => {
  return props.data || generateMockData()
})

// 当前指标数据
const currentMetricData = computed(() => {
  const data = currentData.value[selectedMetric.value]
  if (!data) return []
  
  if (selectedMetric.value === 'bloodPressure') {
    return data.map(item => ({
      time: item.time,
      systolic: item.systolic,
      diastolic: item.diastolic
    }))
  }
  
  return data.map(item => ({
    time: item.time,
    value: item.value
  }))
})

// 统计数据
const currentStats = computed(() => {
  const data = currentMetricData.value
  if (!data.length) return { average: '--', max: '--', min: '--', variance: '--', count: 0 }

  if (selectedMetric.value === 'bloodPressure') {
    const systolicValues = data.map(item => item.systolic)
    const diastolicValues = data.map(item => item.diastolic)
    const avgSys = systolicValues.reduce((a, b) => a + b, 0) / systolicValues.length
    const avgDia = diastolicValues.reduce((a, b) => a + b, 0) / diastolicValues.length
    const variance = Math.sqrt(systolicValues.reduce((sum, val) => sum + Math.pow(val - avgSys, 2), 0) / systolicValues.length)

    return {
      average: `${Math.round(avgSys)}/${Math.round(avgDia)}`,
      max: `${Math.max(...systolicValues).toFixed(0)}/${Math.max(...diastolicValues).toFixed(0)}`,
      min: `${Math.min(...systolicValues).toFixed(0)}/${Math.min(...diastolicValues).toFixed(0)}`,
      variance: variance.toFixed(1),
      count: data.length
    }
  }

  const values = data.map(item => item.value)
  const avg = values.reduce((a, b) => a + b, 0) / values.length
  const variance = Math.sqrt(values.reduce((sum, val) => sum + Math.pow(val - avg, 2), 0) / values.length)

  return {
    average: avg.toFixed(1),
    max: Math.max(...values).toFixed(1),
    min: Math.min(...values).toFixed(1),
    variance: variance.toFixed(1),
    count: data.length
  }
})

// 趋势分析
const trendAnalysis = computed(() => {
  const data = currentMetricData.value
  if (data.length < 2) return { trend: 'stable', change: 0 }
  
  let values
  if (selectedMetric.value === 'bloodPressure') {
    values = data.map(item => item.systolic)
  } else {
    values = data.map(item => item.value)
  }
  
  const firstHalf = values.slice(0, Math.floor(values.length / 2))
  const secondHalf = values.slice(Math.floor(values.length / 2))
  
  const firstAvg = firstHalf.reduce((a, b) => a + b, 0) / firstHalf.length
  const secondAvg = secondHalf.reduce((a, b) => a + b, 0) / secondHalf.length
  
  const change = ((secondAvg - firstAvg) / firstAvg) * 100
  
  if (Math.abs(change) < 2) return { trend: 'stable', change }
  return { trend: change > 0 ? 'rising' : 'falling', change }
})

const trendClass = computed(() => {
  const trend = trendAnalysis.value.trend
  return {
    'trend-rising': trend === 'rising',
    'trend-falling': trend === 'falling',
    'trend-stable': trend === 'stable'
  }
})

const trendIcon = computed(() => {
  const trend = trendAnalysis.value.trend
  const icons = {
    rising: 'mdi:trending-up',
    falling: 'mdi:trending-down',
    stable: 'mdi:trending-neutral'
  }
  return icons[trend]
})

const trendText = computed(() => {
  const trend = trendAnalysis.value.trend
  const texts = {
    rising: '上升',
    falling: '下降',
    stable: '稳定'
  }
  return texts[trend]
})

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return
  
  chartInstance.value = echarts.init(chartRef.value)
  updateChart()
}

// 更新图表
const updateChart = () => {
  if (!chartInstance.value) return
  
  const data = currentMetricData.value
  const times = data.map(item => item.time)
  
  let series = []
  let yAxisConfig = {}
  
  if (selectedMetric.value === 'bloodPressure') {
    series = [
      {
        name: '收缩压',
        type: 'line',
        data: data.map(item => item.systolic),
        smooth: true,
        lineStyle: { color: '#ef4444', width: 3 },
        itemStyle: { color: '#ef4444' },
        areaStyle: { color: 'rgba(239, 68, 68, 0.1)' }
      },
      {
        name: '舒张压',
        type: 'line',
        data: data.map(item => item.diastolic),
        smooth: true,
        lineStyle: { color: '#3b82f6', width: 3 },
        itemStyle: { color: '#3b82f6' },
        areaStyle: { color: 'rgba(59, 130, 246, 0.1)' }
      }
    ]
    yAxisConfig = { name: 'mmHg', min: 60, max: 180 }
  } else {
    const colors = {
      heartRate: '#ef4444',
      temperature: '#f59e0b',
      oxygenSaturation: '#10b981'
    }
    
    series = [{
      name: metricOptions.find(opt => opt.value === selectedMetric.value)?.label,
      type: 'line',
      data: data.map(item => item.value),
      smooth: true,
      lineStyle: { color: colors[selectedMetric.value], width: 3 },
      itemStyle: { color: colors[selectedMetric.value] },
      areaStyle: { color: `${colors[selectedMetric.value]}20` }
    }]
    
    const units = {
      heartRate: 'BPM',
      temperature: '°C',
      oxygenSaturation: '%'
    }
    yAxisConfig = { name: units[selectedMetric.value] }
  }
  
  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e2e8f0',
      textStyle: { color: '#374151' }
    },
    legend: {
      data: series.map(s => s.name),
      bottom: 0,
      textStyle: { color: '#6b7280' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: times,
      axisLine: { lineStyle: { color: '#e2e8f0' } },
      axisTick: { lineStyle: { color: '#e2e8f0' } },
      axisLabel: { color: '#6b7280', fontSize: 11 }
    },
    yAxis: {
      type: 'value',
      ...yAxisConfig,
      axisLine: { lineStyle: { color: '#e2e8f0' } },
      axisTick: { lineStyle: { color: '#e2e8f0' } },
      axisLabel: { color: '#6b7280', fontSize: 11 },
      splitLine: { lineStyle: { color: '#f3f4f6' } }
    },
    series
  }
  
  chartInstance.value.setOption(option)
}

// 监听数据变化
watch(() => props.data, () => {
  nextTick(() => {
    updateChart()
  })
})

watch(() => props.patientId, () => {
  nextTick(() => {
    updateChart()
  })
})

// 生命周期
onMounted(() => {
  nextTick(() => {
    initChart()
  })
})

onUnmounted(() => {
  if (chartInstance.value) {
    chartInstance.value.dispose()
  }
})
</script>

<style scoped>
.health-trends-card {
  height: 100%;
}

.chart-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chart {
  width: 100%;
  min-height: 300px;
}

/* 趋势统计 */
.trend-stats {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 8px;
  padding: 12px;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.stat-item {
  text-align: center;
  padding: 6px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.stat-item:hover {
  transform: translateY(-1px);
}

.stat-item.avg {
  background: #eff6ff;
  border: 1px solid #2563eb;
}

.stat-item.max {
  background: #fef2f2;
  border: 1px solid #dc2626;
}

.stat-item.min {
  background: #f0fdf4;
  border: 1px solid #059669;
}

.stat-item.trend {
  background: #faf5ff;
  border: 1px solid #7c3aed;
}

.stat-item.variance {
  background: #fffbeb;
  border: 1px solid #d97706;
}

.stat-item.count {
  background: #f0f9ff;
  border: 1px solid #0891b2;
}

.stat-label {
  font-size: 10px;
  color: #6b7280;
  margin-bottom: 2px;
  font-weight: 500;
}

.stat-value {
  font-size: 14px;
  font-weight: 700;
  color: #374151;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2px;
  line-height: 1.2;
}

/* 趋势指示器 */
.trend-rising {
  color: #ef4444;
}

.trend-falling {
  color: #3b82f6;
}

.trend-stable {
  color: #10b981;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .trend-stats {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    padding: 12px;
  }

  .stat-value {
    font-size: 14px;
  }

  .chart {
    min-height: 250px;
  }
}

@media (max-width: 480px) {
  .trend-stats {
    grid-template-columns: 1fr;
  }
}
</style>
