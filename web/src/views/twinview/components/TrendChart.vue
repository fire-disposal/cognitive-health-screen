<template>
  <n-card title="24小时趋势" :bordered="false" class="trend-card">
    <template #header-extra>
      <n-icon>
        <Icon icon="mdi:chart-line" />
      </n-icon>
    </template>
    
    <n-spin :show="loading">
      <!-- 指标选择 -->
      <div class="metric-selector">
        <n-button-group size="small">
          <n-button 
            v-for="metric in metrics" 
            :key="metric.key"
            :type="selectedMetric === metric.key ? 'primary' : 'default'"
            @click="selectedMetric = metric.key"
            size="small"
          >
            <template #icon>
              <n-icon>
                <Icon :icon="metric.icon" />
              </n-icon>
            </template>
            {{ metric.label }}
          </n-button>
        </n-button-group>
      </div>

      <!-- 图表容器 -->
      <div ref="chartContainer" class="chart-container" />
    </n-spin>
  </n-card>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { Icon } from '@iconify/vue'
import * as echarts from 'echarts'
import { generateMockData, getDataStatus, getStatusColor } from '../model-data'

const props = defineProps({
  elderlyId: {
    type: [String, Number],
    default: null
  }
})

// 响应式数据
const loading = ref(false)
const selectedMetric = ref('heartRate')
const chartContainer = ref(null)
let chartInstance = null

// 指标配置
const metrics = [
  {
    key: 'heartRate',
    label: '心率',
    icon: 'mdi:heart-pulse',
    color: '#ff6b6b',
    unit: 'BPM',
    desc: '每分钟心跳次数'
  },
  {
    key: 'breathingRate',
    label: '呼吸',
    icon: 'mdi:lungs',
    color: '#4ecdc4',
    unit: '次/分',
    desc: '每分钟呼吸次数'
  },
  {
    key: 'temperature',
    label: '体温',
    icon: 'mdi:thermometer',
    color: '#ff9f43',
    unit: '°C',
    desc: '体表温度'
  }
]

// 计算属性
const currentMetric = computed(() => {
  return metrics.find(m => m.key === selectedMetric.value) || metrics[0]
})

// 方法
const initChart = () => {
  if (!chartContainer.value) return
  
  chartInstance = echarts.init(chartContainer.value)
  updateChart()
}

const updateChart = () => {
  if (!chartInstance) return
  
  const data = generateMockData(selectedMetric.value, 24)
  const metric = currentMetric.value
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        label: {
          backgroundColor: metric.color
        }
      },
      formatter: function(params) {
        const point = params[0]
        const time = new Date(point.data.timestamp).toLocaleTimeString('zh-CN', {
          hour: '2-digit',
          minute: '2-digit'
        })
        const status = getDataStatus(selectedMetric.value, point.data.value)
        const statusText = status === 'normal' ? '正常' : status === 'warning' ? '警告' : '异常'
        return `
          <div style="padding: 8px;">
            <div style="margin-bottom: 4px;">${time}</div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <div style="width: 8px; height: 8px; border-radius: 50%; background: ${metric.color};"></div>
              <span>${metric.label}: ${point.data.value} ${metric.unit}</span>
            </div>
            <div style="margin-top: 4px; color: ${getStatusColor(status)};">状态: ${statusText}</div>
          </div>
        `
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: data.map(item => {
        const date = new Date(item.timestamp)
        return date.toLocaleTimeString('zh-CN', {
          hour: '2-digit',
          minute: '2-digit'
        })
      }),
      axisLabel: {
        fontSize: 10,
        color: '#666'
      },
      axisLine: {
        lineStyle: {
          color: '#e0e0e0'
        }
      }
    },
    yAxis: {
      type: 'value',
      name: metric.unit,
      nameTextStyle: {
        color: '#666',
        fontSize: 10
      },
      axisLabel: {
        fontSize: 10,
        color: '#666'
      },
      axisLine: {
        lineStyle: {
          color: '#e0e0e0'
        }
      },
      splitLine: {
        lineStyle: {
          color: '#f0f0f0'
        }
      }
    },
    series: [
      {
        name: metric.label,
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 4,
        lineStyle: {
          color: metric.color,
          width: 2
        },
        itemStyle: {
          color: metric.color
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              {
                offset: 0,
                color: metric.color + '40'
              },
              {
                offset: 1,
                color: metric.color + '10'
              }
            ]
          }
        },
        data: data.map(item => ({
          value: item.value,
          timestamp: item.timestamp
        }))
      }
    ]
  }
  
  chartInstance.setOption(option, true)
}

const fetchTrendData = async () => {
  if (!props.elderlyId) return
  
  try {
    loading.value = true
    // 这里可以调用API获取真实数据
    // const response = await api.getElderlyTrendData(props.elderlyId, selectedMetric.value)
    // 目前使用模拟数据
    await new Promise(resolve => setTimeout(resolve, 500)) // 模拟加载
  } catch (error) {
    console.error('获取趋势数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 监听指标变化
watch(selectedMetric, () => {
  updateChart()
})

// 监听老人变化
watch(() => props.elderlyId, () => {
  fetchTrendData()
})

// 窗口大小变化处理
const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize()
  }
}

// 生命周期
onMounted(async () => {
  await nextTick()
  initChart()
  fetchTrendData()
  
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose()
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.trend-card {
  height: 350px;
}

.metric-selector {
  margin-bottom: 16px;
  text-align: center;
}

.chart-container {
  height: 230px;
  margin-bottom: 16px;
}


</style>
