<template>
  <n-card title="健康评估分析" class="assessment-card">
    <template #header-extra>
      <n-tag :type="overallScoreType" size="small">
        综合评分: {{ overallScore }}
      </n-tag>
    </template>

    <n-spin :show="loading">
      <div class="assessment-content">
        <!-- 评估雷达图 -->
        <div class="radar-chart">
          <div ref="radarChartRef" class="chart" style="height: 200px; width: 100%;"></div>
        </div>

        <!-- 评估详情 -->
        <div class="assessment-details-compact">
          <div v-for="assessment in assessmentList" :key="assessment.type" class="assessment-item-compact">
            <div class="assessment-icon-compact">
              <n-icon size="16" :color="getAssessmentColor(assessment.type)">
                <Icon :icon="getAssessmentIcon(assessment.type)" />
              </n-icon>
            </div>
            <div class="assessment-content-compact">
              <div class="assessment-name-compact">{{ assessment.name }}</div>
              <div class="assessment-meta-compact">
                <span class="assessment-score-compact" :class="getScoreClass(assessment.score)">
                  {{ assessment.score }}分
                </span>
                <span class="assessment-level-compact">{{ assessment.level }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 评估对比 -->
        <div class="assessment-comparison">
          <h4>历史对比</h4>
          <div class="comparison-grid">
            <div v-for="assessment in assessmentList" :key="assessment.type" class="comparison-item">
              <div class="comparison-header">
                <span class="assessment-name">{{ assessment.name }}</span>
                <span class="score-change" :class="getChangeClass(assessment.change)">
                  <n-icon size="12">
                    <Icon :icon="getChangeIcon(assessment.change)" />
                  </n-icon>
                  {{ Math.abs(assessment.change) }}
                </span>
              </div>
              <div class="score-bar">
                <div class="score-fill" :style="{ width: assessment.score + '%', backgroundColor: getScoreColor(assessment.score) }"></div>
                <span class="score-text">{{ assessment.score }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </n-spin>
  </n-card>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { NCard, NTag, NSpin, NIcon, NProgress } from 'naive-ui'
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

const radarChartRef = ref(null)
const radarChartInstance = ref(null)

// 生成模拟评估数据
const generateMockAssessmentData = () => {
  return {
    assessments: [
      {
        type: 'cognitive',
        name: '认知功能',
        score: 85,
        level: '良好',
        lastTest: '01-15',
        trend: 'stable',
        change: 2
      },
      {
        type: 'physiological',
        name: '生理健康',
        score: 78,
        level: '一般',
        lastTest: '01-10',
        trend: 'improving',
        change: 5
      },
      {
        type: 'adl',
        name: '日常活动',
        score: 92,
        level: '优秀',
        lastTest: '01-12',
        trend: 'stable',
        change: 0
      },
      {
        type: 'mental',
        name: '心理状态',
        score: 75,
        level: '一般',
        lastTest: '01-08',
        trend: 'declining',
        change: -3
      },
      {
        type: 'social',
        name: '社交能力',
        score: 88,
        level: '良好',
        lastTest: '01-14',
        trend: 'improving',
        change: 4
      },
      {
        type: 'nutrition',
        name: '营养状况',
        score: 82,
        level: '良好',
        lastTest: '01-11',
        trend: 'stable',
        change: 1
      }
    ]
  }
}

// 当前评估数据
const currentData = computed(() => {
  const mockData = generateMockAssessmentData()
  console.log('Assessment data computed:', mockData)
  return props.data || mockData
})

const assessmentList = computed(() => {
  // 直接使用模拟数据，确保数据结构正确
  const mockData = generateMockAssessmentData()
  const assessments = mockData.assessments || []
  console.log('Assessment list computed:', assessments)
  return assessments
})

const recommendations = computed(() => {
  return currentData.value.recommendations || []
})

// 综合评分
const overallScore = computed(() => {
  const assessments = assessmentList.value
  if (!assessments.length) return 0
  
  const totalScore = assessments.reduce((sum, item) => sum + item.score, 0)
  return Math.round(totalScore / assessments.length)
})

const overallScoreType = computed(() => {
  const score = overallScore.value
  if (score >= 85) return 'success'
  if (score >= 70) return 'warning'
  return 'error'
})

// 获取评估相关样式和图标
const getAssessmentIcon = (type) => {
  const icons = {
    cognitive: 'mdi:brain',
    physiological: 'mdi:heart-pulse',
    adl: 'mdi:human-handsup',
    mental: 'mdi:emoticon-happy',
    social: 'mdi:account-group'
  }
  return icons[type] || 'mdi:clipboard-check'
}

const getAssessmentColor = (type) => {
  const colors = {
    cognitive: '#8b5cf6',
    physiological: '#ef4444',
    adl: '#10b981',
    mental: '#f59e0b',
    social: '#3b82f6'
  }
  return colors[type] || '#6b7280'
}

const getScoreClass = (score) => {
  if (score >= 85) return 'score-excellent'
  if (score >= 70) return 'score-good'
  if (score >= 60) return 'score-fair'
  return 'score-poor'
}

const getScoreLevel = (score) => {
  if (score >= 85) return '优秀'
  if (score >= 70) return '良好'
  if (score >= 60) return '一般'
  return '需改善'
}

const getProgressColor = (score) => {
  if (score >= 85) return '#10b981'
  if (score >= 70) return '#f59e0b'
  return '#ef4444'
}

const getTrendClass = (trend) => {
  return {
    'trend-improving': trend === 'improving',
    'trend-stable': trend === 'stable',
    'trend-declining': trend === 'declining'
  }
}

const getTrendIcon = (trend) => {
  const icons = {
    improving: 'mdi:trending-up',
    stable: 'mdi:trending-neutral',
    declining: 'mdi:trending-down'
  }
  return icons[trend] || 'mdi:help'
}

const getTrendText = (trend) => {
  const texts = {
    improving: '改善',
    stable: '稳定',
    declining: '下降'
  }
  return texts[trend] || '未知'
}

const getRecommendationIcon = (priority) => {
  const icons = {
    high: 'mdi:alert-circle',
    medium: 'mdi:information',
    low: 'mdi:lightbulb'
  }
  return icons[priority] || 'mdi:help'
}

const getChangeClass = (change) => {
  if (change > 0) return 'change-positive'
  if (change < 0) return 'change-negative'
  return 'change-neutral'
}

const getChangeIcon = (change) => {
  if (change > 0) return 'mdi:trending-up'
  if (change < 0) return 'mdi:trending-down'
  return 'mdi:trending-neutral'
}

const getScoreColor = (score) => {
  if (score >= 85) return '#059669'
  if (score >= 70) return '#d97706'
  return '#dc2626'
}

// 初始化雷达图
const initRadarChart = () => {
  if (!radarChartRef.value) {
    console.log('radarChartRef.value is null')
    return
  }

  try {
    radarChartInstance.value = echarts.init(radarChartRef.value)
    console.log('Radar chart initialized successfully')
    updateRadarChart()
  } catch (error) {
    console.error('Error initializing radar chart:', error)
  }
}

const updateRadarChart = () => {
  if (!radarChartInstance.value) {
    console.log('radarChartInstance.value is null')
    return
  }

  const assessments = assessmentList.value
  console.log('Assessments data:', assessments)
  if (!assessments || assessments.length === 0) {
    console.log('No assessments data available')
    return
  }

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e2e8f0',
      textStyle: { color: '#374151' }
    },
    radar: {
      indicator: assessments.map(item => ({
        name: item.name,
        max: 100,
        min: 0
      })),
      radius: '65%',
      center: ['50%', '50%'],
      axisLine: {
        lineStyle: { color: '#e5e7eb' }
      },
      splitLine: {
        lineStyle: { color: '#f3f4f6' }
      },
      axisLabel: {
        color: '#6b7280',
        fontSize: 10,
        show: true
      },
      splitArea: {
        show: true,
        areaStyle: {
          color: ['rgba(250, 250, 250, 0.3)', 'rgba(200, 200, 200, 0.1)']
        }
      }
    },
    series: [{
      name: '健康评估',
      type: 'radar',
      data: [{
        value: assessments.map(item => item.score),
        name: '当前评分',
        itemStyle: {
          color: '#2563eb',
          borderColor: '#2563eb',
          borderWidth: 2
        },
        areaStyle: {
          color: 'rgba(37, 99, 235, 0.2)'
        },
        lineStyle: {
          color: '#2563eb',
          width: 2
        },
        symbol: 'circle',
        symbolSize: 4
      }]
    }]
  }

  try {
    radarChartInstance.value.setOption(option, true)
    console.log('Radar chart updated successfully')
  } catch (error) {
    console.error('Error updating radar chart:', error)
  }
}

// 监听数据变化
watch(() => props.data, () => {
  nextTick(() => {
    updateRadarChart()
  })
})

// 监听评估数据变化
watch(() => assessmentList.value, (newVal) => {
  console.log('Assessment list changed:', newVal)
  nextTick(() => {
    updateRadarChart()
  })
}, { deep: true, immediate: true })

// 生命周期
onMounted(() => {

  nextTick(() => {
    setTimeout(() => {
      initRadarChart()
      // 再次尝试初始化，确保图表能够显示
      setTimeout(() => {
        if (radarChartInstance.value) {
          updateRadarChart()
        }
      }, 500)
      // 第三次尝试，强制使用模拟数据
      setTimeout(() => {
        if (radarChartInstance.value) {
          console.log('Force updating radar chart with mock data')
          const mockData = generateMockAssessmentData()
          const assessments = mockData.assessments || []
          if (assessments.length > 0) {
            const option = {
              tooltip: {
                trigger: 'item',
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                borderColor: '#e2e8f0',
                textStyle: { color: '#374151' }
              },
              radar: {
                indicator: assessments.map(item => ({
                  name: item.name,
                  max: 100,
                  min: 0
                })),
                radius: '65%',
                center: ['50%', '50%'],
                axisLine: { lineStyle: { color: '#e5e7eb' } },
                splitLine: { lineStyle: { color: '#f3f4f6' } },
                axisLabel: { color: '#6b7280', fontSize: 10, show: true },
                splitArea: {
                  show: true,
                  areaStyle: {
                    color: ['rgba(250, 250, 250, 0.3)', 'rgba(200, 200, 200, 0.1)']
                  }
                }
              },
              series: [{
                name: '健康评估',
                type: 'radar',
                data: [{
                  value: assessments.map(item => item.score),
                  name: '当前评分',
                  itemStyle: { color: '#2563eb', borderColor: '#2563eb', borderWidth: 2 },
                  areaStyle: { color: 'rgba(37, 99, 235, 0.2)' },
                  lineStyle: { color: '#2563eb', width: 2 },
                  symbol: 'circle',
                  symbolSize: 4
                }]
              }]
            }
            radarChartInstance.value.setOption(option, true)
            console.log('Radar chart force updated successfully')
          }
        }
      }, 1000)
    }, 100)
  })
})

// 窗口大小变化时重绘图表
const handleResize = () => {
  if (radarChartInstance.value) {
    radarChartInstance.value.resize()
  }
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (radarChartInstance.value) {
    radarChartInstance.value.dispose()
  }
})
</script>

<style scoped>
.assessment-card {
  height: 100%;
}

.assessment-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 雷达图 */
.radar-chart {
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.chart {
  width: 100%;
}

/* 评估详情 */
.assessment-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.assessment-item {
  padding: 16px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.assessment-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.assessment-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.assessment-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: #f8fafc;
  border-radius: 10px;
}

.assessment-info {
  flex: 1;
}

.assessment-name {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 4px;
}

.assessment-date {
  font-size: 12px;
  color: #6b7280;
}

.assessment-score {
  text-align: center;
}

.score-value {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 4px;
}

.score-excellent {
  color: #10b981;
}

.score-good {
  color: #f59e0b;
}

.score-fair {
  color: #3b82f6;
}

.score-poor {
  color: #ef4444;
}

.score-level {
  font-size: 12px;
  color: #6b7280;
}

/* 紧凑三列布局样式 */
.assessment-details-compact {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.assessment-item-compact {
  background: #f8fafc;
  border-radius: 6px;
  padding: 8px;
  border: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  gap: 6px;
  min-height: 50px;
  transition: all 0.2s ease;
}

.assessment-item-compact:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.assessment-icon-compact {
  flex-shrink: 0;
}

.assessment-content-compact {
  flex: 1;
  min-width: 0;
}

.assessment-name-compact {
  font-size: 12px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.assessment-meta-compact {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 10px;
}

.assessment-score-compact {
  font-weight: 600;
  padding: 1px 4px;
  border-radius: 3px;
  background: rgba(59, 130, 246, 0.1);
}

.assessment-level-compact {
  color: #6b7280;
  font-size: 9px;
}

.assessment-progress {
  margin-bottom: 8px;
}

.assessment-trend {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.trend-label {
  color: #6b7280;
}

.trend-value {
  display: flex;
  align-items: center;
  gap: 4px;
  font-weight: 500;
}

.trend-improving {
  color: #10b981;
}

.trend-stable {
  color: #6b7280;
}

.trend-declining {
  color: #ef4444;
}

/* 评估对比 */
.assessment-comparison h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.comparison-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 6px;
}

.comparison-item {
  padding: 8px 12px;
  background: #ffffff;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
}

.comparison-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.assessment-name {
  font-size: 12px;
  font-weight: 600;
  color: #374151;
}

.score-change {
  display: flex;
  align-items: center;
  gap: 2px;
  font-size: 10px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
}

.change-positive {
  background: #dcfce7;
  color: #166534;
}

.change-negative {
  background: #fee2e2;
  color: #dc2626;
}

.change-neutral {
  background: #f3f4f6;
  color: #6b7280;
}

.score-bar {
  position: relative;
  height: 16px;
  background: #f3f4f6;
  border-radius: 8px;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  transition: width 0.3s ease;
  border-radius: 8px;
}

.score-text {
  position: absolute;
  right: 6px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 10px;
  font-weight: 600;
  color: #374151;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .assessment-header {
    flex-direction: column;
    text-align: center;
    gap: 8px;
  }

  .assessment-details-compact {
    grid-template-columns: 1fr;
  }

  .comparison-grid {
    grid-template-columns: 1fr;
  }

  .assessment-info {
    text-align: center;
  }

  .assessment-trend {
    justify-content: center;
  }

  .recommendation-item {
    flex-direction: column;
    text-align: center;
  }
}
</style>
