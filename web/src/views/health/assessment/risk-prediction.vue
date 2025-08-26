<template>
  <div class="risk-prediction">
    <!-- 页面标题 -->
    <div class="prediction-header">
      <NButton text @click="goBack" class="back-btn">
        <template #icon>
          <TheIcon icon="mdi:arrow-left" />
        </template>
        返回
      </NButton>
      <div class="header-content">
        <div class="title-section">
          <TheIcon icon="mdi:chart-timeline-variant" class="title-icon" />
          <h1 class="page-title">风险预测</h1>
        </div>
        <p class="page-subtitle">AI驱动的健康风险预测与分析</p>
      </div>
    </div>

    <!-- 综合风险评估 -->
    <div class="comprehensive-risk">
      <NCard title="综合风险评估" class="risk-overview-card">
        <div class="risk-overview">
          <div class="risk-score-section">
            <div class="risk-score-circle">
              <div class="score-number">65</div>
              <div class="score-label">风险指数</div>
            </div>
            <div class="risk-level">
              <NTag type="warning" size="large">中等风险</NTag>
              <p class="risk-description">基于多维度数据分析的综合风险评估</p>
            </div>
          </div>
          
          <div class="risk-factors">
            <h3>主要风险因子</h3>
            <div class="factors-list">
              <div class="factor-item high-risk">
                <div class="factor-info">
                  <span class="factor-name">跌倒风险</span>
                  <span class="factor-score">75/100</span>
                </div>
                <NProgress 
                  type="line" 
                  :percentage="75" 
                  color="#ff4d4f"
                  :show-indicator="false"
                />
              </div>
              
              <div class="factor-item medium-risk">
                <div class="factor-info">
                  <span class="factor-name">认知退化</span>
                  <span class="factor-score">60/100</span>
                </div>
                <NProgress 
                  type="line" 
                  :percentage="60" 
                  color="#faad14"
                  :show-indicator="false"
                />
              </div>
              
              <div class="factor-item medium-risk">
                <div class="factor-info">
                  <span class="factor-name">社交孤立</span>
                  <span class="factor-score">55/100</span>
                </div>
                <NProgress 
                  type="line" 
                  :percentage="55" 
                  color="#faad14"
                  :show-indicator="false"
                />
              </div>
              
              <div class="factor-item low-risk">
                <div class="factor-info">
                  <span class="factor-name">心血管风险</span>
                  <span class="factor-score">45/100</span>
                </div>
                <NProgress 
                  type="line" 
                  :percentage="45" 
                  color="#52c41a"
                  :show-indicator="false"
                />
              </div>
              
              <div class="factor-item low-risk">
                <div class="factor-info">
                  <span class="factor-name">营养不良</span>
                  <span class="factor-score">30/100</span>
                </div>
                <NProgress 
                  type="line" 
                  :percentage="30" 
                  color="#52c41a"
                  :show-indicator="false"
                />
              </div>
            </div>
          </div>
        </div>
      </NCard>
    </div>

    <!-- 风险趋势预测 -->
    <div class="risk-trend">
      <NCard title="风险趋势预测" class="trend-card">
        <template #header-extra>
          <NSelect 
            v-model:value="trendPeriod" 
            :options="trendOptions" 
            size="small"
            @update:value="updateTrendChart"
          />
        </template>
        
        <div class="trend-chart" ref="trendChart"></div>
        
        <div class="trend-summary">
          <p>显示未来{{ trendPeriod === '7' ? '7天' : trendPeriod === '30' ? '30天' : '90天' }}的风险变化趋势</p>
        </div>
      </NCard>
    </div>

    <!-- AI预测结果 -->
    <div class="ai-predictions">
      <NCard title="AI预测结果" class="predictions-card">
        <div class="predictions-list">
          <NGrid :cols="3" :x-gap="24" :y-gap="24">
            <!-- 跌倒风险 -->
            <NGridItem>
              <div class="prediction-item high-priority">
                <div class="prediction-header">
                  <div class="prediction-icon">
                    <TheIcon icon="mdi:alert-circle" />
                  </div>
                  <div class="prediction-info">
                    <h4>跌倒风险</h4>
                    <span class="prediction-probability">75%</span>
                  </div>
                  <div class="prediction-timeline">
                    <NTag type="error" size="small">未来7天</NTag>
                  </div>
                </div>
                <p class="prediction-description">
                  基于步态分析和环境因素，预测跌倒风险较高
                </p>
              </div>
            </NGridItem>

            <!-- 认知退化 -->
            <NGridItem>
              <div class="prediction-item medium-priority">
                <div class="prediction-header">
                  <div class="prediction-icon">
                    <TheIcon icon="mdi:brain" />
                  </div>
                  <div class="prediction-info">
                    <h4>认知退化</h4>
                    <span class="prediction-probability">40%</span>
                  </div>
                  <div class="prediction-timeline">
                    <NTag type="warning" size="small">未来30天</NTag>
                  </div>
                </div>
                <p class="prediction-description">
                  认知功能评估显示轻度下降趋势
                </p>
              </div>
            </NGridItem>

            <!-- 健康恶化 -->
            <NGridItem>
              <div class="prediction-item low-priority">
                <div class="prediction-header">
                  <div class="prediction-icon">
                    <TheIcon icon="mdi:heart-pulse" />
                  </div>
                  <div class="prediction-info">
                    <h4>健康恶化</h4>
                    <span class="prediction-probability">25%</span>
                  </div>
                  <div class="prediction-timeline">
                    <NTag type="success" size="small">未来14天</NTag>
                  </div>
                </div>
                <p class="prediction-description">
                  生命体征稳定，短期内健康状况良好
                </p>
              </div>
            </NGridItem>
          </NGrid>
        </div>
      </NCard>
    </div>

    <!-- 预防建议 -->
    <div class="prevention-recommendations">
      <NGrid :cols="2" :x-gap="24" :y-gap="24">
        <!-- 立即执行建议 -->
        <NGridItem>
          <NCard title="立即执行" class="recommendations-card immediate">
            <template #header-extra>
              <TheIcon icon="mdi:clock-alert" class="urgent-icon" />
            </template>
            
            <div class="recommendations-list">
              <div class="recommendation-item">
                <div class="recommendation-icon">
                  <TheIcon icon="mdi:shield-check" />
                </div>
                <div class="recommendation-text">
                  增加防跌倒设施检查
                </div>
              </div>
              
              <div class="recommendation-item">
                <div class="recommendation-icon">
                  <TheIcon icon="mdi:pill" />
                </div>
                <div class="recommendation-text">
                  调整药物服用时间
                </div>
              </div>
              
              <div class="recommendation-item">
                <div class="recommendation-icon">
                  <TheIcon icon="mdi:eye" />
                </div>
                <div class="recommendation-text">
                  加强日常活动监护
                </div>
              </div>
              
              <div class="recommendation-item">
                <div class="recommendation-icon">
                  <TheIcon icon="mdi:phone" />
                </div>
                <div class="recommendation-text">
                  联系家属增加陪伴时间
                </div>
              </div>
            </div>
          </NCard>
        </NGridItem>

        <!-- 长期关注建议 -->
        <NGridItem>
          <NCard title="长期关注" class="recommendations-card long-term">
            <template #header-extra>
              <TheIcon icon="mdi:calendar-check" class="plan-icon" />
            </template>
            
            <div class="recommendations-list">
              <div class="recommendation-item">
                <div class="recommendation-icon">
                  <TheIcon icon="mdi:dumbbell" />
                </div>
                <div class="recommendation-text">
                  制定个性化康复计划
                </div>
              </div>
              
              <div class="recommendation-item">
                <div class="recommendation-icon">
                  <TheIcon icon="mdi:brain" />
                </div>
                <div class="recommendation-text">
                  定期认知功能评估
                </div>
              </div>
              
              <div class="recommendation-item">
                <div class="recommendation-icon">
                  <TheIcon icon="mdi:food-apple" />
                </div>
                <div class="recommendation-text">
                  营养状况监测
                </div>
              </div>
              
              <div class="recommendation-item">
                <div class="recommendation-icon">
                  <TheIcon icon="mdi:account-group" />
                </div>
                <div class="recommendation-text">
                  社交活动安排
                </div>
              </div>
            </div>
          </NCard>
        </NGridItem>
      </NGrid>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  NCard, NButton, NGrid, NGridItem, NTag, NProgress, NSelect
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import * as echarts from 'echarts'
import api from '@/api'

const router = useRouter()
const trendChart = ref(null)
let trendChartInstance = null

// 趋势预测时间段
const trendPeriod = ref('7')
const trendOptions = [
  { label: '7天', value: '7' },
  { label: '30天', value: '30' },
  { label: '90天', value: '90' }
]

// 返回上级页面
function goBack() {
  router.push('/health/assessment')
}

// 初始化趋势图表
function initTrendChart() {
  if (trendChart.value) {
    trendChartInstance = echarts.init(trendChart.value)
    updateTrendChart()
  }
}

// 更新趋势图表
function updateTrendChart() {
  if (!trendChartInstance) return
  
  const period = trendPeriod.value
  let xAxisData, seriesData
  
  if (period === '7') {
    xAxisData = ['今天', '明天', '后天', '第4天', '第5天', '第6天', '第7天']
    seriesData = {
      overall: [65, 67, 68, 70, 69, 71, 72],
      fall: [75, 76, 77, 78, 77, 79, 80],
      cognitive: [60, 61, 61, 62, 62, 63, 63],
      cardiovascular: [45, 44, 45, 46, 45, 47, 46]
    }
  } else if (period === '30') {
    xAxisData = ['第1周', '第2周', '第3周', '第4周']
    seriesData = {
      overall: [65, 68, 71, 74],
      fall: [75, 78, 81, 84],
      cognitive: [60, 62, 64, 66],
      cardiovascular: [45, 46, 47, 48]
    }
  } else {
    xAxisData = ['第1月', '第2月', '第3月']
    seriesData = {
      overall: [65, 72, 78],
      fall: [75, 82, 88],
      cognitive: [60, 65, 70],
      cardiovascular: [45, 48, 52]
    }
  }
  
  const option = {
    title: {
      text: `未来${period === '7' ? '7天' : period === '30' ? '30天' : '90天'}风险趋势`,
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      data: ['综合风险', '跌倒风险', '认知风险', '心血管风险'],
      bottom: 10
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: xAxisData
    },
    yAxis: {
      type: 'value',
      name: '风险指数',
      min: 0,
      max: 100
    },
    series: [
      {
        name: '综合风险',
        type: 'line',
        data: seriesData.overall,
        smooth: true,
        itemStyle: { color: '#1890ff' },
        lineStyle: { width: 3 }
      },
      {
        name: '跌倒风险',
        type: 'line',
        data: seriesData.fall,
        smooth: true,
        itemStyle: { color: '#ff4d4f' }
      },
      {
        name: '认知风险',
        type: 'line',
        data: seriesData.cognitive,
        smooth: true,
        itemStyle: { color: '#faad14' }
      },
      {
        name: '心血管风险',
        type: 'line',
        data: seriesData.cardiovascular,
        smooth: true,
        itemStyle: { color: '#52c41a' }
      }
    ]
  }
  
  trendChartInstance.setOption(option)
}

// 处理窗口大小变化
function handleResize() {
  trendChartInstance?.resize()
}

onMounted(() => {
  setTimeout(() => {
    initTrendChart()
  }, 100)
  
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  trendChartInstance?.dispose()
})
</script>

<style scoped>
.risk-prediction {
  padding: 24px;
  background: var(--n-color-hover);
  min-height: 100vh;
  overflow-y: auto;
  height: 100vh;
}

/* 页面标题 */
.prediction-header {
  margin-bottom: 32px;
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.back-btn {
  margin-top: 8px;
}

.header-content {
  flex: 1;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.title-icon {
  font-size: 32px;
  color: var(--n-color-primary);
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: var(--n-text-color-base);
  margin: 0;
}

.page-subtitle {
  font-size: 16px;
  color: var(--n-text-color-placeholder);
  margin: 0;
}

/* 综合风险评估 */
.comprehensive-risk {
  margin-bottom: 32px;
}

.risk-overview {
  padding: 24px 0;
}

.risk-score-section {
  display: flex;
  align-items: center;
  gap: 32px;
  margin-bottom: 32px;
}

.risk-score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FFA726 0%, #FF6B6B 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
}

.score-number {
  font-size: 36px;
  font-weight: 600;
  line-height: 1;
}

.score-label {
  font-size: 14px;
  margin-top: 4px;
}

.risk-level h3 {
  font-size: 20px;
  font-weight: 600;
  color: var(--n-text-color-base);
  margin: 0 0 8px 0;
}

.risk-description {
  font-size: 16px;
  color: var(--n-text-color-placeholder);
  margin: 8px 0 0 0;
  line-height: 1.5;
}

.risk-factors h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--n-text-color-base);
  margin: 0 0 16px 0;
}

.factors-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.factor-item {
  padding: 16px;
  background: var(--n-color-hover);
  border-radius: 8px;
}

.factor-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.factor-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--n-text-color-base);
}

.factor-score {
  font-size: 14px;
  color: var(--n-text-color-placeholder);
}

/* 风险趋势 */
.risk-trend {
  margin-bottom: 32px;
}

.trend-chart {
  height: 400px;
  width: 100%;
}

.trend-summary {
  margin-top: 16px;
  text-align: center;
}

.trend-summary p {
  font-size: 14px;
  color: var(--n-text-color-placeholder);
  margin: 0;
}

/* AI预测结果 */
.ai-predictions {
  margin-bottom: 32px;
}

.predictions-list {
  padding: 16px 0;
}

.prediction-item {
  padding: 20px;
  background: var(--n-color-hover);
  border-radius: 12px;
  border-left: 4px solid;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.prediction-item.high-priority {
  border-left-color: var(--n-color-error);
}

.prediction-item.medium-priority {
  border-left-color: var(--n-color-warning);
}

.prediction-item.low-priority {
  border-left-color: var(--n-color-success);
}

.prediction-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 8px;
}

.prediction-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: #45B7D1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: white;
}

.prediction-info {
  flex: 1;
}

.prediction-info h4 {
  font-size: 16px;
  font-weight: 600;
  color: var(--n-text-color-base);
  margin: 0;
}

.prediction-probability {
  font-size: 24px;
  font-weight: 600;
  color: var(--n-color-primary);
}

.prediction-description {
  font-size: 14px;
  color: var(--n-text-color-placeholder);
  margin: 0;
  line-height: 1.5;
  flex: 1;
  margin-top: 12px;
}

/* 预防建议 */
.prevention-recommendations {
  margin-bottom: 24px;
}

.recommendations-card.immediate {
  border-top: 3px solid var(--n-color-error);
}

.recommendations-card.long-term {
  border-top: 3px solid var(--n-color-primary);
}

.urgent-icon {
  color: var(--n-color-error);
  font-size: 18px;
}

.plan-icon {
  color: var(--n-color-primary);
  font-size: 18px;
}

.recommendations-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px 0;
}

.recommendation-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--n-color-hover);
  border-radius: 8px;
}

.recommendation-icon {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: #26D0CE;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  color: white;
}

.recommendation-text {
  font-size: 14px;
  color: var(--n-text-color-base);
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .risk-prediction {
    padding: 16px;
  }
  
  .prevention-recommendations :deep(.n-grid) {
    grid-template-columns: 1fr !important;
  }
  
  .risk-score-section {
    flex-direction: column;
    text-align: center;
  }
  
  .prediction-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .prediction-header {
    flex-direction: row;
    align-items: center;
  }
}
</style>
