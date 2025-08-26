<template>
  <n-card title="环境监测" :bordered="false" class="env-card">
    <template #header-extra>
      <n-icon>
        <Icon icon="mdi:home-thermometer" />
      </n-icon>
    </template>

    <n-spin :show="loading">
      <n-grid :cols="2" :x-gap="12" :y-gap="12">
        <!-- 温度 -->
        <n-grid-item>
          <div class="env-item">
            <div class="env-icon">
              <n-icon size="32" :color="getTemperatureColor(environmentData.temperature)">
                <Icon icon="mdi:thermometer" />
              </n-icon>
            </div>
            <div class="env-content">
              <div class="env-value">{{ formatValue(environmentData.temperature) }}°C</div>
              <div class="env-label">温度</div>
              <n-tag
                :type="getTemperatureStatus(environmentData.temperature).type"
                size="small"
              >
                {{ getTemperatureStatus(environmentData.temperature).text }}
              </n-tag>
            </div>
          </div>
        </n-grid-item>

        <!-- 湿度 -->
        <n-grid-item>
          <div class="env-item">
            <div class="env-icon">
              <n-icon size="32" :color="getHumidityColor(environmentData.humidity)">
                <Icon icon="mdi:water-percent" />
              </n-icon>
            </div>
            <div class="env-content">
              <div class="env-value">{{ formatValue(environmentData.humidity, 0) }}%</div>
              <div class="env-label">湿度</div>
              <n-tag
                :type="getHumidityStatus(environmentData.humidity).type"
                size="small"
              >
                {{ getHumidityStatus(environmentData.humidity).text }}
              </n-tag>
            </div>
          </div>
        </n-grid-item>

        <!-- 光照 -->
        <n-grid-item>
          <div class="env-item">
            <div class="env-icon">
              <n-icon size="32" :color="getLightColor(environmentData.light)">
                <Icon icon="mdi:lightbulb" />
              </n-icon>
            </div>
            <div class="env-content">
              <div class="env-value">{{ formatValue(environmentData.light, 0) }}lx</div>
              <div class="env-label">光照</div>
              <n-tag
                :type="getLightStatus(environmentData.light).type"
                size="small"
              >
                {{ getLightStatus(environmentData.light).text }}
              </n-tag>
            </div>
          </div>
        </n-grid-item>

        <!-- 空气质量 -->
        <n-grid-item>
          <div class="env-item">
            <div class="env-icon">
              <n-icon size="32" :color="getAirQualityColor(environmentData.airQuality)">
                <Icon icon="mdi:air-filter" />
              </n-icon>
            </div>
            <div class="env-content">
              <div class="env-value">{{ getAirQualityText(environmentData.airQuality) }}</div>
              <div class="env-label">空气质量</div>
              <n-tag 
                :type="getAirQualityStatus(environmentData.airQuality).type" 
                size="small"
              >
                {{ getAirQualityStatus(environmentData.airQuality).text }}
              </n-tag>
            </div>
          </div>
        </n-grid-item>
      </n-grid>
    </n-spin>
  </n-card>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { Icon } from '@iconify/vue'
import * as echarts from 'echarts'
import api from '@/api'

// 移除props，使用固定的环境数据

// 响应式数据
const loading = ref(false)
const environmentData = ref({
  temperature: null,
  humidity: null,
  light: null,
  airQuality: null
})

// 方法
const fetchEnvironmentData = async () => {
  try {
    loading.value = true
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 300))

    // 使用模拟数据，添加一些随机变化
    environmentData.value = {
      temperature: 22 + Math.random() * 6,
      humidity: 50 + Math.random() * 30,
      light: 200 + Math.random() * 400,
      airQuality: 70 + Math.random() * 25
    }
  } catch (error) {
    console.error('获取环境数据失败:', error)
    // 使用默认模拟数据
    environmentData.value = {
      temperature: 24,
      humidity: 65,
      light: 350,
      airQuality: 85
    }
  } finally {
    loading.value = false
  }
}

// 温度相关方法
const getTemperatureColor = (temp) => {
  if (!temp) return '#d0d0d0'
  if (temp < 18) return '#2080f0'
  if (temp > 28) return '#d03050'
  return '#f0a020'
}

const getTemperatureStatus = (temp) => {
  if (!temp) return { type: 'default', text: '未知' }
  if (temp < 18) return { type: 'info', text: '偏低' }
  if (temp > 28) return { type: 'error', text: '偏高' }
  return { type: 'success', text: '适宜' }
}

// 湿度相关方法
const getHumidityColor = (humidity) => {
  if (!humidity) return '#d0d0d0'
  if (humidity < 40 || humidity > 70) return '#f0a020'
  return '#18a058'
}

const getHumidityStatus = (humidity) => {
  if (!humidity) return { type: 'default', text: '未知' }
  if (humidity < 40) return { type: 'warning', text: '偏低' }
  if (humidity > 70) return { type: 'warning', text: '偏高' }
  return { type: 'success', text: '适宜' }
}

// 光照相关方法
const getLightColor = (light) => {
  if (!light) return '#d0d0d0'
  if (light < 200) return '#2080f0'
  if (light > 500) return '#f0a020'
  return '#18a058'
}

const getLightStatus = (light) => {
  if (!light) return { type: 'default', text: '未知' }
  if (light < 200) return { type: 'info', text: '偏暗' }
  if (light > 500) return { type: 'warning', text: '偏亮' }
  return { type: 'success', text: '适宜' }
}

// 空气质量相关方法
const getAirQualityColor = (quality) => {
  if (!quality) return '#d0d0d0'
  if (quality >= 80) return '#18a058'
  if (quality >= 60) return '#f0a020'
  return '#d03050'
}

const getAirQualityText = (quality) => {
  if (!quality) return '--'
  if (quality >= 80) return '优秀'
  if (quality >= 60) return '良好'
  if (quality >= 40) return '一般'
  return '较差'
}

const getAirQualityStatus = (quality) => {
  if (!quality) return { type: 'default', text: '未知' }
  if (quality >= 80) return { type: 'success', text: '优秀' }
  if (quality >= 60) return { type: 'warning', text: '良好' }
  return { type: 'error', text: '需改善' }
}

// 格式化数值显示
const formatValue = (value, decimals = 1) => {
  if (value === null || value === undefined) return '--'
  return Number(value).toFixed(decimals)
}

// 生命周期
onMounted(async () => {
  await fetchEnvironmentData()

  // 定时更新数据
  const interval = setInterval(() => {
    fetchEnvironmentData()
  }, 30000) // 30秒更新一次

  // 组件卸载时清除定时器
  onUnmounted(() => {
    clearInterval(interval)
  })
})
</script>

<style scoped>
.env-card {
  height: 350px;
}

.env-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: #fafafa;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.env-item:hover {
  background: #f0f0f0;
  transform: translateY(-1px);
}

.env-icon {
  flex-shrink: 0;
}

.env-content {
  flex: 1;
  text-align: center;
}

.env-value {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
  color: #333;
}

.env-label {
  font-size: 11px;
  color: #666;
  margin-bottom: 6px;
}
</style>
