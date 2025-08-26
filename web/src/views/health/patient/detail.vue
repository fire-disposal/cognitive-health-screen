<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { 
  NCard, NButton, NIcon, NTag, NProgress, NGrid, NGridItem, NStatistic
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import * as echarts from 'echarts'

const route = useRoute()
const router = useRouter()

// 当前病人ID
const patientId = computed(() => Number(route.params.id))

// 图表引用
const radarChart = ref(null)
const trendChart = ref(null)
let radarChartInstance = null
let trendChartInstance = null

// 模拟病人详细数据
const patientData = {
  1: {
    id: 1,
    name: '张爷爷',
    age: 78,
    location: '1号楼101',
    status: '看电视',
    riskScore: 3,
    riskLevel: { label: '低风险', color: '#52c41a' },
    positionRisk: 1.2,
    environmentRisk: 1.0,
    physiologicalRisk: 0.8
  },
  2: {
    id: 2,
    name: '李奶奶',
    age: 82,
    location: '1号楼102',
    status: '休息',
    riskScore: 7,
    riskLevel: { label: '中等风险', color: '#faad14' },
    positionRisk: 2.4,
    environmentRisk: 2.8,
    physiologicalRisk: 1.8
  },
  6: {
    id: 6,
    name: '孙叔叔',
    age: 80,
    location: '1号楼306',
    status: '看书',
    riskScore: 12,
    riskLevel: { label: '高风险', color: '#ff4d4f' },
    positionRisk: 3.8,
    environmentRisk: 4.2,
    physiologicalRisk: 4.0
  }
}

// 当前病人信息
const patient = computed(() => patientData[patientId.value] || patientData[1])

// 异常行为指标
const behaviorRisk = computed(() => ({
  staticTime: { 
    label: '异常', 
    value: 1.5, 
    color: '#faad14',
    actualValue: '5小时/日'
  },
  turnover: { 
    label: '中度异常', 
    value: 1.8, 
    color: '#ff4d4f',
    actualValue: '1.5次/小时'
  },
  fallCount: { 
    label: '轻微异常', 
    value: 0.8, 
    color: '#faad14',
    actualValue: '1次/月'
  }
}))

// 环境因素指标
const environmentRisk = computed(() => ({
  temperature: { 
    label: '正常', 
    value: 0.8, 
    color: '#52c41a',
    actualValue: 22
  },
  humidity: { 
    label: '异常', 
    value: 1.5, 
    color: '#faad14',
    actualValue: 25
  },
  airQuality: { 
    label: '异常', 
    value: 1.2, 
    color: '#faad14',
    actualValue: 120
  }
}))

// 生理指标
const physiologicalRisk = computed(() => ({
  heartRate: { 
    label: '异常', 
    value: 1.5, 
    color: '#faad14',
    actualValue: 92
  },
  respiratoryRate: { 
    label: '异常', 
    value: 1.4, 
    color: '#faad14',
    actualValue: 22
  }
}))

// 获取状态图标
function getStatusIcon(status) {
  const iconMap = {
    '看电视': 'mdi:television',
    '休息': 'mdi:sofa',
    '睡觉': 'mdi:sleep',
    '发呆': 'mdi:head-question',
    '活动': 'mdi:walk',
    '看书': 'mdi:book-open-page-variant',
    '吃饭': 'mdi:food-fork-drink',
    '静止不动': 'mdi:timer-sand'
  }
  return iconMap[status] || 'mdi:account'
}

// 获取状态图标颜色
function getStatusIconColor(status) {
  const colorMap = {
    '看电视': '#1890ff',
    '休息': '#52c41a',
    '睡觉': '#52c41a',
    '发呆': '#faad14',
    '活动': '#1890ff',
    '看书': '#1890ff',
    '吃饭': '#52c41a',
    '静止不动': '#ff4d4f'
  }
  return colorMap[status] || '#666'
}

// 获取风险颜色
function getRiskColor(score) {
  if (score <= 5) return '#52c41a'
  if (score <= 10) return '#faad14'
  return '#ff4d4f'
}

// 返回总览页
function goBack() {
  router.push({ path: '/health/patient' })
}

// 初始化雷达图
function initRadarChart() {
  if (radarChart.value) {
    radarChartInstance = echarts.init(radarChart.value)
    updateRadarChart()
  }
}

// 更新雷达图
function updateRadarChart() {
  if (!radarChartInstance) return
  
  const radarData = [
    { name: '体位风险', value: patient.value.positionRisk },
    { name: '环境因素', value: patient.value.environmentRisk },
    { name: '生理指标', value: patient.value.physiologicalRisk },
    { name: '行为轨迹', value: 2.7 },
    { name: '睡眠质量', value: 3.1 }
  ]
  
  const option = {
    radar: {
      indicator: [
        { name: '体位风险', max: 5 },
        { name: '环境因素', max: 5 },
        { name: '生理指标', max: 5 },
        { name: '行为轨迹', max: 5 },
        { name: '睡眠质量', max: 5 }
      ],
      shape: 'polygon',
      splitNumber: 5,
      axisName: {
        color: '#666',
        fontSize: 12
      },
      splitArea: {
        areaStyle: {
          color: ['#f8f9fa', '#f2f5f8', '#e9eef3', '#e3e8ee', '#d9e2ea']
        }
      }
    },
    series: [{
      type: 'radar',
      data: [{
        value: radarData.map(item => item.value),
        name: '风险评分',
        itemStyle: {
          color: '#faad14'
        },
        areaStyle: {
          color: 'rgba(250, 173, 20, 0.3)'
        },
        lineStyle: {
          width: 2
        }
      }]
    }]
  }
  
  radarChartInstance.setOption(option)
}

// 初始化趋势图
function initTrendChart() {
  if (trendChart.value) {
    trendChartInstance = echarts.init(trendChart.value)
    updateTrendChart()
  }
}

// 更新趋势图
function updateTrendChart() {
  if (!trendChartInstance) return
  
  const dates = ['7/28', '7/29', '7/30', '7/31', '8/1', '8/2', '8/3']
  const positionData = [2.8, 2.7, 2.9, 3.0, 3.1, 3.3, 3.2]
  const environmentData = [2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 2.9]
  const physiologicalData = [2.6, 2.7, 2.7, 2.8, 2.9, 2.8, 2.9]
  const totalData = [7.9, 8.0, 8.3, 8.6, 8.9, 9.1, 9.0]
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      data: ['体位风险', '环境风险', '生理风险', '总风险']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dates
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '体位风险',
        type: 'line',
        stack: 'Total',
        areaStyle: {
          color: 'rgba(58, 132, 195, 0.3)'
        },
        data: positionData,
        itemStyle: {
          color: '#3A84C3'
        }
      },
      {
        name: '环境风险',
        type: 'line',
        stack: 'Total',
        areaStyle: {
          color: 'rgba(109, 212, 0, 0.3)'
        },
        data: environmentData,
        itemStyle: {
          color: '#6DD400'
        }
      },
      {
        name: '生理风险',
        type: 'line',
        stack: 'Total',
        areaStyle: {
          color: 'rgba(255, 77, 79, 0.3)'
        },
        data: physiologicalData,
        itemStyle: {
          color: '#FF4D4F'
        }
      },
      {
        name: '总风险',
        type: 'line',
        data: totalData,
        itemStyle: {
          color: '#FAAD14'
        },
        lineStyle: {
          width: 3
        }
      }
    ]
  }
  
  trendChartInstance.setOption(option)
}

// 处理窗口大小调整
function handleResize() {
  radarChartInstance?.resize()
  trendChartInstance?.resize()
}

onMounted(() => {
  setTimeout(() => {
    initRadarChart()
    initTrendChart()
  }, 100)
  
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  radarChartInstance?.dispose()
  trendChartInstance?.dispose()
})
</script>

<template>
  <div class="patient-detail">
    <!-- 页面标题和返回按钮 -->
    <div class="detail-header">
      <NButton text @click="goBack" class="back-btn">
        <template #icon>
          <TheIcon icon="mdi:arrow-left" />
        </template>
      </NButton>
      <h2 class="detail-title">
        <span class="patient-name">{{ patient.name || '病人详情' }}</span>
        <NTag
          :color="{ color: patient.riskLevel.color, textColor: 'white' }"
          class="risk-tag"
        >
          {{ patient.riskLevel.label }}
        </NTag>
      </h2>
    </div>

    <NGrid :cols="2" :x-gap="16" :y-gap="16" responsive="screen" :collapsed-rows="1">
      <!-- 左侧内容 -->
      <NGridItem>
        <!-- 数字孪生模型窗口 -->
        <NCard class="mb-4">
          <template #header>
            <div class="card-header">
              <TheIcon icon="mdi:human-male" color="#1890ff" />
              <span>数字孪生模型</span>
            </div>
          </template>
          <div class="scene-container">
            <div class="scene-placeholder">
              <TheIcon icon="mdi:cube-outline" size="64" color="#ccc" />
              <p>3D模型加载中...</p>
            </div>
          </div>
        </NCard>

        <!-- 基本信息和雷达图 -->
        <NGrid :cols="2" :x-gap="16">
          <!-- 基本信息卡片 -->
          <NGridItem>
            <NCard class="info-card">
              <template #header>
                <div class="card-header">
                  <TheIcon icon="mdi:card-account-details" color="#1890ff" />
                  <span>基本信息</span>
                </div>
              </template>
              <div class="info-content">
                <div class="info-item">
                  <span class="info-label">姓名</span>
                  <span class="info-value">{{ patient.name }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">年龄</span>
                  <span class="info-value">{{ patient.age }}岁</span>
                </div>
                <div class="info-item">
                  <span class="info-label">房间号</span>
                  <span class="info-value">{{ patient.location }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">当前状态</span>
                  <div class="status-value">
                    <TheIcon
                      :icon="getStatusIcon(patient.status)"
                      :color="getStatusIconColor(patient.status)"
                      size="16"
                    />
                    <span>{{ patient.status }}</span>
                  </div>
                </div>
                <div class="info-item">
                  <span class="info-label">总风险评分</span>
                  <div class="risk-score">
                    <NProgress
                      type="line"
                      :percentage="patient.riskScore * 10"
                      :color="getRiskColor(patient.riskScore)"
                      :show-indicator="false"
                      :height="12"
                    />
                    <span class="score-text" :style="{ color: getRiskColor(patient.riskScore) }">
                      {{ patient.riskScore }}
                    </span>
                  </div>
                </div>
              </div>
            </NCard>
          </NGridItem>

          <!-- 雷达图卡片 -->
          <NGridItem>
            <NCard class="radar-card">
              <template #header>
                <div class="card-header">
                  <TheIcon icon="mdi:radar" color="#1890ff" />
                  <span>风险因素雷达图</span>
                </div>
              </template>
              <div ref="radarChart" class="chart-container"></div>
            </NCard>
          </NGridItem>
        </NGrid>
      </NGridItem>

      <!-- 右侧内容 -->
      <NGridItem>
        <!-- 风险评估详情 -->
        <NCard class="mb-4">
          <template #header>
            <div class="card-header">
              <TheIcon icon="mdi:chart-line" color="#1890ff" />
              <span>风险评估详情</span>
            </div>
          </template>
          <div class="risk-assessment">
            <!-- 异常行为指标 -->
            <div class="risk-section">
              <div class="section-title">
                <TheIcon icon="mdi:run-fast" color="#3A84C3" />
                <span>异常行为指标 (权重: 40%)</span>
              </div>
              <NGrid :cols="3" :x-gap="12" class="mt-2">
                <NGridItem>
                  <div class="metric-item">
                    <div class="metric-label">长时间静止</div>
                    <NProgress
                      type="line"
                      :percentage="behaviorRisk.staticTime.value * 50"
                      :color="behaviorRisk.staticTime.color"
                      :height="8"
                      :show-indicator="false"
                    />
                    <div class="metric-info">
                      <span>{{ behaviorRisk.staticTime.label }}</span>
                      <span>{{ behaviorRisk.staticTime.value }}分</span>
                    </div>
                  </div>
                </NGridItem>
                <NGridItem>
                  <div class="metric-item">
                    <div class="metric-label">不规则翻身</div>
                    <NProgress
                      type="line"
                      :percentage="behaviorRisk.turnover.value * 50"
                      :color="behaviorRisk.turnover.color"
                      :height="8"
                      :show-indicator="false"
                    />
                    <div class="metric-info">
                      <span>{{ behaviorRisk.turnover.label }}</span>
                      <span>{{ behaviorRisk.turnover.value }}分</span>
                    </div>
                  </div>
                </NGridItem>
                <NGridItem>
                  <div class="metric-item">
                    <div class="metric-label">跌倒次数</div>
                    <NProgress
                      type="line"
                      :percentage="behaviorRisk.fallCount.value * 33.3"
                      :color="behaviorRisk.fallCount.color"
                      :height="8"
                      :show-indicator="false"
                    />
                    <div class="metric-info">
                      <span>{{ behaviorRisk.fallCount.label }}</span>
                      <span>{{ behaviorRisk.fallCount.value }}分</span>
                    </div>
                  </div>
                </NGridItem>
              </NGrid>
            </div>

            <!-- 环境因素指标 -->
            <div class="risk-section mt-4">
              <div class="section-title">
                <TheIcon icon="mdi:home-thermometer" color="#6DD400" />
                <span>环境因素指标 (权重: 30%)</span>
              </div>
              <NGrid :cols="3" :x-gap="12" class="mt-2">
                <NGridItem>
                  <div class="metric-item">
                    <div class="metric-label">温度</div>
                    <NProgress
                      type="line"
                      :percentage="environmentRisk.temperature.value * 50"
                      :color="environmentRisk.temperature.color"
                      :height="8"
                      :show-indicator="false"
                    />
                    <div class="metric-info">
                      <span>{{ environmentRisk.temperature.label }}</span>
                      <span>{{ environmentRisk.temperature.actualValue }}°C</span>
                    </div>
                  </div>
                </NGridItem>
                <NGridItem>
                  <div class="metric-item">
                    <div class="metric-label">湿度</div>
                    <NProgress
                      type="line"
                      :percentage="environmentRisk.humidity.value * 50"
                      :color="environmentRisk.humidity.color"
                      :height="8"
                      :show-indicator="false"
                    />
                    <div class="metric-info">
                      <span>{{ environmentRisk.humidity.label }}</span>
                      <span>{{ environmentRisk.humidity.actualValue }}%</span>
                    </div>
                  </div>
                </NGridItem>
                <NGridItem>
                  <div class="metric-item">
                    <div class="metric-label">空气质量</div>
                    <NProgress
                      type="line"
                      :percentage="environmentRisk.airQuality.value * 50"
                      :color="environmentRisk.airQuality.color"
                      :height="8"
                      :show-indicator="false"
                    />
                    <div class="metric-info">
                      <span>{{ environmentRisk.airQuality.label }}</span>
                      <span>{{ environmentRisk.airQuality.actualValue }} AQI</span>
                    </div>
                  </div>
                </NGridItem>
              </NGrid>
            </div>

            <!-- 生理指标 -->
            <div class="risk-section mt-4">
              <div class="section-title">
                <TheIcon icon="mdi:heart-pulse" color="#FF4D4F" />
                <span>生理指标 (权重: 30%)</span>
              </div>
              <NGrid :cols="2" :x-gap="12" class="mt-2">
                <NGridItem>
                  <div class="metric-item">
                    <div class="metric-label">心率</div>
                    <NProgress
                      type="line"
                      :percentage="physiologicalRisk.heartRate.value * 50"
                      :color="physiologicalRisk.heartRate.color"
                      :height="8"
                      :show-indicator="false"
                    />
                    <div class="metric-info">
                      <span>{{ physiologicalRisk.heartRate.label }}</span>
                      <span>{{ physiologicalRisk.heartRate.actualValue }} 次/分钟</span>
                    </div>
                  </div>
                </NGridItem>
                <NGridItem>
                  <div class="metric-item">
                    <div class="metric-label">呼吸频率</div>
                    <NProgress
                      type="line"
                      :percentage="physiologicalRisk.respiratoryRate.value * 50"
                      :color="physiologicalRisk.respiratoryRate.color"
                      :height="8"
                      :show-indicator="false"
                    />
                    <div class="metric-info">
                      <span>{{ physiologicalRisk.respiratoryRate.label }}</span>
                      <span>{{ physiologicalRisk.respiratoryRate.actualValue }} 次/分钟</span>
                    </div>
                  </div>
                </NGridItem>
              </NGrid>
            </div>
          </div>
        </NCard>

        <!-- 历史趋势图表 -->
        <NCard>
          <template #header>
            <div class="card-header">
              <TheIcon icon="mdi:chart-timeline-variant" color="#1890ff" />
              <span>风险评分趋势 (近7天)</span>
            </div>
          </template>
          <div ref="trendChart" class="chart-container trend-chart"></div>
        </NCard>
      </NGridItem>
    </NGrid>
  </div>
</template>

<style>
/* 全局样式确保滚动正常 */
html, body {
  overflow-x: hidden;
  overflow-y: auto;
  height: auto;
}

.n-layout, .n-layout-content {
  overflow-y: auto !important;
  height: auto !important;
  max-height: none !important;
}

/* 确保主容器可以滚动 */
#app, .app-container {
  overflow-y: auto !important;
  height: auto !important;
}
</style>

<style scoped>
.patient-detail {
  padding: 16px;
  height: 100vh;
  overflow-y: auto;
  box-sizing: border-box;
  width: 100%;
  position: relative;
  display: block;
}

.detail-header {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
}

.back-btn {
  margin-right: 16px;
  font-size: 18px;
}

.detail-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0;
}

.patient-name {
  color: #1890ff;
  font-size: 24px;
  font-weight: 600;
}

.risk-tag {
  font-size: 12px;
  font-weight: 500;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.scene-container {
  height: 300px;
  background: #1e1e1e;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ccc;
}

.scene-placeholder {
  text-align: center;
}

.scene-placeholder p {
  margin-top: 12px;
  font-size: 14px;
}

.info-card {
  height: auto;
  min-height: 280px;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.info-value {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.status-value {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  font-weight: 600;
}

.risk-score {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.score-text {
  font-size: 16px;
  font-weight: bold;
  min-width: 20px;
}

.radar-card {
  height: auto;
  min-height: 280px;
}

.chart-container {
  width: 100%;
  height: 280px;
}

.trend-chart {
  height: 300px;
}

.risk-assessment {
  padding: 8px 0;
}

.risk-section {
  margin-bottom: 24px;
}

.risk-section:last-child {
  margin-bottom: 0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
}

.metric-item {
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
}

.metric-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 8px;
  font-weight: 500;
}

.metric-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 6px;
  font-size: 11px;
}

.metric-info span:first-child {
  color: #666;
}

.metric-info span:last-child {
  font-weight: 600;
  color: #333;
}

/* 工具类 */
.mb-4 {
  margin-bottom: 16px;
}

.mt-2 {
  margin-top: 8px;
}

.mt-4 {
  margin-top: 16px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .detail-title {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .patient-name {
    font-size: 20px;
  }

  .chart-container {
    height: 240px;
  }

  .trend-chart {
    height: 260px;
  }
}

@media (max-width: 768px) {
  .patient-detail {
    padding: 8px;
  }

  .detail-header {
    margin-bottom: 16px;
  }

  .patient-name {
    font-size: 18px;
  }

  .scene-container {
    height: 200px;
  }

  .chart-container {
    height: 200px;
  }

  .trend-chart {
    height: 220px;
  }

  .info-content {
    gap: 12px;
  }

  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .risk-score {
    width: 100%;
  }

  .section-title {
    font-size: 14px;
  }

  .metric-item {
    padding: 8px;
  }

  .metric-label {
    font-size: 11px;
  }

  .metric-info {
    font-size: 10px;
  }
}

@media (max-width: 480px) {
  .detail-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .back-btn {
    margin-right: 0;
    margin-bottom: 8px;
  }

  .card-header {
    font-size: 14px;
  }

  .info-label,
  .info-value {
    font-size: 12px;
  }

  .status-value {
    font-size: 12px;
  }
}
</style>
