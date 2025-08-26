<template>
  <n-card title="风险分析" class="risk-card">
    <template #header-extra>
      <n-tag :type="overallRiskType" size="small">
        风险等级: {{ overallRiskText }}
      </n-tag>
    </template>

    <n-spin :show="loading">
      <div class="risk-content">
        <!-- 综合风险评分 -->
        <div class="risk-score">
          <div class="score-circle">
            <div class="score-value" :class="getRiskScoreClass(riskData.riskScore)">
              {{ riskData.riskScore }}
            </div>
            <div class="score-label">综合风险评分</div>
          </div>
        </div>

        <!-- 风险因子 -->
        <div class="risk-factors">
          <h4>风险因子分析</h4>
          <div class="factor-grid-compact">
            <div v-for="factor in riskData.riskFactors" :key="factor.factor" class="factor-item-compact">
              <div class="factor-icon-compact" :style="{ backgroundColor: getRiskProgressColor(factor.level) }">
                <n-icon size="12" color="#ffffff">
                  <Icon :icon="getRiskFactorIcon(factor.factor)" />
                </n-icon>
              </div>
              <div class="factor-content-compact">
                <div class="factor-name-compact">{{ factor.factor }}</div>
                <div class="factor-meta-compact">
                  <span class="factor-score-compact" :class="getRiskLevelClass(factor.level)">
                    {{ factor.score }}%
                  </span>
                  <span class="factor-level-compact" :class="getRiskLevelClass(factor.level)">
                    {{ getRiskLevelText(factor.level) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 风险趋势 -->
        <div class="risk-trends">
          <h4>风险趋势</h4>
          <div class="trend-grid">
            <div v-for="trend in riskTrends" :key="trend.name" class="trend-item">
              <div class="trend-header">
                <span class="trend-name">{{ trend.name }}</span>
                <span class="trend-change" :class="getTrendChangeClass(trend.change)">
                  <n-icon size="10">
                    <Icon :icon="getTrendChangeIcon(trend.change)" />
                  </n-icon>
                  {{ Math.abs(trend.change) }}%
                </span>
              </div>
              <div class="trend-chart">
                <div v-for="(value, index) in trend.values" :key="index" class="trend-bar">
                  <div class="bar-fill" :style="{ height: value + '%', backgroundColor: trend.color }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 关键指标 -->
        <div class="key-metrics">
          <h4>关键指标</h4>
          <div class="metrics-grid">
            <div v-for="metric in keyMetrics" :key="metric.name" class="metric-card">
              <div class="metric-icon" :style="{ backgroundColor: metric.color }">
                <n-icon size="14" color="#ffffff">
                  <Icon :icon="metric.icon" />
                </n-icon>
              </div>
              <div class="metric-content">
                <div class="metric-value">{{ metric.value }}</div>
                <div class="metric-name">{{ metric.name }}</div>
                <div class="metric-status" :class="getMetricStatusClass(metric.status)">
                  {{ metric.status }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </n-spin>
  </n-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { NCard, NTag, NSpin, NIcon, NProgress } from 'naive-ui'
import { Icon } from '@iconify/vue'

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

// 生成模拟风险数据
const generateMockRiskData = () => {
  return {
    overallRisk: 'medium',
    riskScore: 65,
    riskFactors: [
      { factor: '心血管风险', level: 'medium', score: 70 },
      { factor: '跌倒风险', level: 'low', score: 30 },
      { factor: '认知风险', level: 'low', score: 25 },
      { factor: '营养风险', level: 'medium', score: 60 },
      { factor: '药物风险', level: 'low', score: 35 }
    ]
  }
}

const riskData = computed(() => {
  return props.data || generateMockRiskData()
})

// 风险趋势数据
const riskTrends = computed(() => {
  return [
    {
      name: '心血管',
      change: -2,
      color: '#dc2626',
      values: [60, 65, 70, 68, 65, 62, 60]
    },
    {
      name: '跌倒',
      change: 1,
      color: '#d97706',
      values: [25, 28, 30, 32, 30, 28, 30]
    },
    {
      name: '认知',
      change: 0,
      color: '#7c3aed',
      values: [20, 22, 25, 23, 22, 24, 25]
    }
  ]
})

// 关键指标
const keyMetrics = computed(() => {
  return [
    { name: '血压', value: '正常', status: '良好', color: '#059669', icon: 'mdi:heart' },
    { name: '血糖', value: '偏高', status: '注意', color: '#d97706', icon: 'mdi:water-percent' },
    { name: '体重', value: '稳定', status: '良好', color: '#2563eb', icon: 'mdi:scale-bathroom' },
    { name: '睡眠', value: '充足', status: '良好', color: '#0891b2', icon: 'mdi:sleep' },
    { name: '运动', value: '不足', status: '需改善', color: '#dc2626', icon: 'mdi:run' },
    { name: '药物', value: '规律', status: '良好', color: '#7c3aed', icon: 'mdi:pill' }
  ]
})

// 整体风险等级
const overallRiskType = computed(() => {
  const risk = riskData.value.overallRisk
  const types = {
    low: 'success',
    medium: 'warning',
    high: 'error'
  }
  return types[risk] || 'default'
})

const overallRiskText = computed(() => {
  const risk = riskData.value.overallRisk
  const texts = {
    low: '低',
    medium: '中',
    high: '高'
  }
  return texts[risk] || '未知'
})

// 风险评分样式
const getRiskScoreClass = (score) => {
  if (score >= 80) return 'score-high'
  if (score >= 50) return 'score-medium'
  return 'score-low'
}

// 风险等级相关
const getRiskLevelClass = (level) => {
  return `level-${level}`
}

const getRiskLevelText = (level) => {
  const texts = {
    low: '低风险',
    medium: '中风险',
    high: '高风险'
  }
  return texts[level] || '未知'
}

const getRiskFactorIcon = (factor) => {
  const icons = {
    '心血管风险': 'mdi:heart-pulse',
    '糖尿病风险': 'mdi:diabetes',
    '认知风险': 'mdi:brain',
    '跌倒风险': 'mdi:human-male-height-variant',
    '营养风险': 'mdi:food-apple',
    '社交风险': 'mdi:account-group'
  }
  return icons[factor] || 'mdi:alert-circle'
}

const getRiskProgressColor = (level) => {
  const colors = {
    low: '#059669',
    medium: '#d97706',
    high: '#dc2626'
  }
  return colors[level] || '#6b7280'
}

const getTrendChangeClass = (change) => {
  if (change > 0) return 'trend-increase'
  if (change < 0) return 'trend-decrease'
  return 'trend-stable'
}

const getTrendChangeIcon = (change) => {
  if (change > 0) return 'mdi:trending-up'
  if (change < 0) return 'mdi:trending-down'
  return 'mdi:trending-neutral'
}

const getMetricStatusClass = (status) => {
  if (status === '良好') return 'status-good'
  if (status === '注意' || status === '需改善') return 'status-warning'
  return 'status-normal'
}
</script>

<style scoped>
.risk-card {
  height: 100%;
}

.risk-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 综合风险评分 */
.risk-score {
  display: flex;
  justify-content: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
}

.score-circle {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 120px;
  height: 120px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 50%;
  border: 3px solid rgba(255, 255, 255, 0.3);
}

.score-value {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 8px;
}

.score-label {
  font-size: 12px;
  opacity: 0.9;
  text-align: center;
}

/* 风险因子 */
.risk-factors h4 {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: #374151;
}

.factor-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.factor-item {
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
  border-left: 4px solid #e2e8f0;
}

.factor-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.factor-name {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.factor-level {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: 500;
}

.level-low {
  background: #dcfce7;
  color: #166534;
}

.level-medium {
  background: #fef3c7;
  color: #92400e;
}

.level-high {
  background: #fee2e2;
  color: #dc2626;
}

.factor-progress {
  display: flex;
  align-items: center;
  gap: 8px;
}

.factor-score {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
  min-width: 30px;
}

/* 风险因子紧凑三列布局 */
.factor-grid-compact {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.factor-item-compact {
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

.factor-item-compact:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.factor-icon-compact {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.factor-content-compact {
  flex: 1;
  min-width: 0;
}

.factor-name-compact {
  font-size: 12px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.factor-meta-compact {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 10px;
}

.factor-score-compact {
  font-weight: 600;
  padding: 1px 4px;
  border-radius: 3px;
}

.factor-level-compact {
  font-size: 9px;
}

/* 风险趋势 */
.risk-trends h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.trend-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.trend-item {
  padding: 8px;
  background: white;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
}

.trend-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.trend-name {
  font-size: 11px;
  font-weight: 600;
  color: #374151;
}

.trend-change {
  display: flex;
  align-items: center;
  gap: 2px;
  font-size: 9px;
  font-weight: 600;
  padding: 2px 4px;
  border-radius: 3px;
}

.trend-increase {
  background: #fee2e2;
  color: #dc2626;
}

.trend-decrease {
  background: #dcfce7;
  color: #059669;
}

.trend-stable {
  background: #f3f4f6;
  color: #6b7280;
}

.trend-chart {
  display: flex;
  align-items: end;
  gap: 2px;
  height: 30px;
}

.trend-bar {
  flex: 1;
  height: 100%;
  display: flex;
  align-items: end;
}

.bar-fill {
  width: 100%;
  min-height: 2px;
  border-radius: 1px;
}

/* 关键指标 */
.key-metrics h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.metric-card {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  background: white;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.metric-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.metric-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.metric-content {
  flex: 1;
  text-align: center;
}

.metric-value {
  font-size: 11px;
  font-weight: 700;
  color: #374151;
  margin-bottom: 1px;
}

.metric-name {
  font-size: 9px;
  color: #6b7280;
  font-weight: 500;
  margin-bottom: 1px;
}

.metric-status {
  font-size: 8px;
  font-weight: 600;
  padding: 1px 4px;
  border-radius: 2px;
}

.status-good {
  background: #dcfce7;
  color: #166534;
}

.status-warning {
  background: #fef3c7;
  color: #92400e;
}

.status-normal {
  background: #f3f4f6;
  color: #6b7280;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .score-circle {
    width: 100px;
    height: 100px;
  }
  
  .score-value {
    font-size: 28px;
  }
  
  .factor-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .factor-list {
    grid-template-columns: 1fr;
  }

  .factor-grid-compact {
    grid-template-columns: 1fr;
  }
  
  .prediction-item {
    flex-direction: column;
    text-align: center;
  }
  
  .prediction-icon {
    width: 36px;
    height: 36px;
  }
}
</style>
