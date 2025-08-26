<template>
  <AppPage :show-footer="false">
    <div class="health-assessment">
      <!-- 页面标题 -->
      <div class="assessment-header">
        <div class="header-content">
          <div class="title-section">
            <TheIcon icon="mdi:clipboard-check-multiple" class="title-icon" />
            <h1 class="page-title">健康评估</h1>
          </div>
          <p class="page-subtitle">AI智能评估与健康状态分析</p>
        </div>
      </div>

    <!-- 评估模块卡片 -->
    <div class="assessment-modules">
      <NGrid :cols="3" :x-gap="24" :y-gap="24" responsive="screen">
        <!-- 认知功能评估 -->
        <NGridItem>
          <NCard 
            class="assessment-card cognitive-card" 
            hoverable 
            @click="navigateToAssessment('cognitive')"
          >
            <div class="card-content">
              <div class="card-icon cognitive-icon">
                <TheIcon icon="mdi:brain" />
              </div>
              <h3 class="card-title">认知功能评估</h3>
              <p class="card-description">
                MMSE量表、MoCA量表等标准化认知功能评估工具
              </p>
              <div class="card-action">
                <NButton type="primary" ghost>
                  评估结果
                  <template #icon>
                    <TheIcon icon="mdi:arrow-right" />
                  </template>
                </NButton>
              </div>
            </div>
          </NCard>
        </NGridItem>

        <!-- 生理健康评估 -->
        <NGridItem>
          <NCard 
            class="assessment-card physiological-card" 
            hoverable 
            @click="navigateToAssessment('physiological')"
          >
            <div class="card-content">
              <div class="card-icon physiological-icon">
                <TheIcon icon="mdi:heart-pulse" />
              </div>
              <h3 class="card-title">生理健康评估</h3>
              <p class="card-description">
                血压、心率、睡眠质量等生理指标综合评估
              </p>
              <div class="card-action">
                <NButton type="primary" ghost>
                  查看报告
                  <template #icon>
                    <TheIcon icon="mdi:arrow-right" />
                  </template>
                </NButton>
              </div>
            </div>
          </NCard>
        </NGridItem>

        <!-- 日常生活能力评估 -->
        <NGridItem>
          <NCard
            class="assessment-card adl-card"
            hoverable
            @click="navigateToAssessment('adl')"
          >
            <div class="card-content">
              <div class="card-icon adl-icon">
                <TheIcon icon="mdi:account-check" />
              </div>
              <h3 class="card-title">日常生活能力</h3>
              <p class="card-description">
                ADL量表评估老人日常生活自理能力
              </p>
              <div class="card-action">
                <NButton type="primary" ghost>
                  评估记录
                  <template #icon>
                    <TheIcon icon="mdi:arrow-right" />
                  </template>
                </NButton>
              </div>
            </div>
          </NCard>
        </NGridItem>
      </NGrid>
    </div>

    <!-- 风险预测模块 -->
    <div class="risk-prediction-section">
      <NCard
        class="risk-prediction-card"
        hoverable
        @click="navigateToRiskPrediction"
      >
        <div class="risk-card-content">
          <div class="risk-header">
            <div class="risk-icon">
              <TheIcon icon="mdi:chart-timeline-variant" />
            </div>
            <div class="risk-info">
              <h3 class="risk-title">AI风险预测与分析</h3>
              <p class="risk-description">基于评估结果的综合风险评估、趋势预测和AI分析</p>
            </div>
          </div>
          <div class="risk-stats">
            <div class="risk-stat-item">
              <span class="stat-label">综合风险指数</span>
              <span class="stat-value">65</span>
              <span class="stat-level medium">中等风险</span>
            </div>
            <div class="risk-factors-preview">
              <div class="factor-preview">
                <span class="factor-name">跌倒风险</span>
                <span class="factor-value high">75%</span>
              </div>
              <div class="factor-preview">
                <span class="factor-name">认知退化</span>
                <span class="factor-value medium">60%</span>
              </div>
              <div class="factor-preview">
                <span class="factor-name">心血管风险</span>
                <span class="factor-value low">45%</span>
              </div>
            </div>
          </div>
          <div class="risk-action">
            <NButton type="primary" size="large">
              查看详细分析
              <template #icon>
                <TheIcon icon="mdi:arrow-right" />
              </template>
            </NButton>
          </div>
        </div>
      </NCard>
    </div>





    <!-- 主要内容区域 -->
    <div class="main-content-grid">
      <NGrid :cols="12" :x-gap="24" :y-gap="24">
        <!-- 最近评估记录 -->
        <NGridItem :span="8">
          <NCard title="最近评估记录" class="recent-card">
            <template #header-extra>
              <NButton text @click="viewAllRecords">
                查看全部
                <template #icon>
                  <TheIcon icon="mdi:arrow-right" />
                </template>
              </NButton>
            </template>

            <div class="assessment-list">
              <div
                v-for="record in recentRecords"
                :key="record.id"
                class="assessment-record"
                @click="viewRecordDetail(record)"
              >
                <div class="record-info">
                  <div class="record-header">
                    <span class="record-type">{{ record.type }}</span>
                    <span class="record-date">{{ formatDate(record.date) }}</span>
                  </div>
                  <div class="record-patient">{{ record.patientName }}</div>
                  <div class="record-score">
                    评分: <span class="score-value">{{ record.score }}</span>
                  </div>
                </div>
                <div class="record-status">
                  <NTag :type="getStatusType(record.status)">
                    {{ record.status }}
                  </NTag>
                </div>
              </div>
            </div>
          </NCard>
        </NGridItem>

        <!-- 统计概览 -->
        <NGridItem :span="4">
          <div class="statistics-grid">
            <NGrid :cols="1" :y-gap="16">
              <NGridItem>
                <NCard class="stat-card compact">
                  <NStatistic label="总评估次数" :value="statistics.totalAssessments">
                    <template #prefix>
                      <TheIcon icon="mdi:clipboard-list" class="stat-icon" />
                    </template>
                  </NStatistic>
                </NCard>
              </NGridItem>
              <NGridItem>
                <NCard class="stat-card compact">
                  <NStatistic label="本月评估" :value="statistics.monthlyAssessments">
                    <template #prefix>
                      <TheIcon icon="mdi:calendar-month" class="stat-icon" />
                    </template>
                  </NStatistic>
                </NCard>
              </NGridItem>
              <NGridItem>
                <NCard class="stat-card compact">
                  <NStatistic label="高风险患者" :value="statistics.highRiskPatients">
                    <template #prefix>
                      <TheIcon icon="mdi:alert-circle" class="stat-icon high-risk" />
                    </template>
                  </NStatistic>
                </NCard>
              </NGridItem>
              <NGridItem>
                <NCard class="stat-card compact">
                  <NStatistic label="待评估患者" :value="statistics.pendingAssessments">
                    <template #prefix>
                      <TheIcon icon="mdi:clock-outline" class="stat-icon" />
                    </template>
                  </NStatistic>
                </NCard>
              </NGridItem>
            </NGrid>
          </div>
        </NGridItem>
      </NGrid>
    </div>
    </div>
  </AppPage>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  NCard, NButton, NGrid, NGridItem, NTag, NStatistic
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import AppPage from '@/components/page/AppPage.vue'
import api from '@/api'

const router = useRouter()

// 统计数据
const statistics = ref({
  totalAssessments: 156,
  monthlyAssessments: 23,
  highRiskPatients: 8,
  pendingAssessments: 12
})

// 最近评估记录
const recentRecords = ref([
  {
    id: 1,
    type: '认知功能评估',
    patientName: '张爷爷',
    date: '2024-01-15',
    score: '26/30',
    status: '正常'
  },
  {
    id: 2,
    type: '生理健康评估',
    patientName: '李奶奶',
    date: '2024-01-14',
    score: '良好',
    status: '轻度异常'
  },
  {
    id: 3,
    type: 'ADL评估',
    patientName: '王叔叔',
    date: '2024-01-13',
    score: '85/100',
    status: '正常'
  }
])

// 导航到具体评估页面
function navigateToAssessment(type) {
  router.push(`/health/assessment/${type}`)
}

// 导航到风险预测页面
function navigateToRiskPrediction() {
  router.push('/health/assessment/risk-prediction')
}

// 查看所有记录
function viewAllRecords() {
  router.push('/health/assessment/records')
}

// 查看记录详情
function viewRecordDetail(record) {
  router.push(`/health/assessment/record/${record.id}`)
}

// 格式化日期
function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

// 获取状态类型
function getStatusType(status) {
  const typeMap = {
    '正常': 'success',
    '轻度异常': 'warning',
    '异常': 'error'
  }
  return typeMap[status] || 'default'
}

// 获取统计数据
async function fetchStatistics() {
  try {
    const response = await api.getAssessmentStatistics()
    if (response.data) {
      statistics.value = response.data
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 获取最近记录
async function fetchRecentRecords() {
  try {
    const response = await api.getAssessmentResults({ limit: 5, sort: 'date_desc' })
    if (response.data) {
      recentRecords.value = response.data
    }
  } catch (error) {
    console.error('获取最近记录失败:', error)
  }
}

onMounted(() => {
  fetchStatistics()
  fetchRecentRecords()
})
</script>

<!-- 全局样式修复 -->
<style>
/* 确保主容器可以滚动 */
html, body {
  overflow: auto !important;
}

#app {
  overflow: auto !important;
}

.n-layout, .n-layout-content {
  overflow-y: auto !important;
  height: auto !important;
  max-height: none !important;
}
</style>

<style scoped>
.health-assessment {
  padding: 24px;
  min-height: 100vh;
  overflow-y: auto;
}

/* 页面标题 */
.assessment-header {
  margin-bottom: 32px;
  text-align: center;
}

.header-content {
  max-width: 600px;
  margin: 0 auto;
}

.title-section {
  display: flex;
  align-items: center;
  justify-content: center;
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

/* 评估模块卡片 */
.assessment-modules {
  margin-bottom: 32px;
}

.assessment-card {
  cursor: pointer;
  transition: all 0.3s ease;
  height: 100%;
}

.assessment-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.card-content {
  text-align: center;
  padding: 24px 16px;
}

.card-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  font-size: 36px;
  color: white;
}

.cognitive-icon {
  background: #FF6B6B;
}

.physiological-icon {
  background: #4ECDC4;
}

.adl-icon {
  background: #45B7D1;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: var(--n-text-color-base);
}

.card-description {
  font-size: 14px;
  color: var(--n-text-color-placeholder);
  margin: 0 0 24px 0;
  line-height: 1.5;
}

.card-action {
  margin-top: auto;
}

/* 最近评估记录 */
.recent-assessments {
  margin-bottom: 32px;
}

.assessment-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.assessment-record {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: var(--n-color-hover);
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.assessment-record:hover {
  background: var(--n-color-pressed);
}

.record-info {
  flex: 1;
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.record-type {
  font-weight: 600;
  color: var(--n-text-color-base);
}

.record-date {
  font-size: 12px;
  color: var(--n-text-color-placeholder);
}

.record-patient {
  font-size: 14px;
  color: var(--n-text-color-placeholder);
  margin-bottom: 4px;
}

.record-score {
  font-size: 14px;
  color: var(--n-text-color-base);
}

.score-value {
  font-weight: 600;
  color: var(--n-color-primary);
}

/* 主要内容区域 */
.main-content-grid {
  margin-bottom: 24px;
}

/* 统计概览 */
.statistics-grid {
  height: 100%;
}

.stat-card {
  text-align: center;
  height: 100%;
}

.stat-card.compact {
  padding: 8px;
}

.stat-card.compact :deep(.n-card__content) {
  padding: 12px;
}

.stat-icon {
  font-size: 18px;
  color: #45B7D1;
}

.stat-icon.high-risk {
  color: #FF6B6B;
}

/* 风险预测卡片 */
.risk-prediction-section {
  margin-bottom: 32px;
}

.risk-prediction-card {
  cursor: pointer;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #2C3E50 0%, #34495E 100%);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.risk-prediction-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(52, 73, 94, 0.3);
}

.risk-card-content {
  padding: 32px;
}

.risk-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 24px;
}

.risk-icon {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  color: white;
}

.risk-info {
  flex: 1;
}

.risk-title {
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: white;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
}

.risk-description {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.95);
  margin: 0;
  line-height: 1.5;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.risk-stats {
  margin-bottom: 24px;
}

.risk-stat-item {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.stat-label {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.95);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.stat-value {
  font-size: 32px;
  font-weight: 600;
  color: white;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
}

.stat-level {
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 500;
}

.stat-level.medium {
  background: rgba(250, 173, 20, 0.2);
  color: #faad14;
}

.risk-factors-preview {
  display: flex;
  gap: 24px;
  margin-top: 16px;
}

.factor-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.factor-name {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.9);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.factor-value {
  font-size: 16px;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.factor-value.high {
  color: #ff7875;
}

.factor-value.medium {
  color: #faad14;
}

.factor-value.low {
  color: #73d13d;
}

.risk-action {
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .health-assessment {
    padding: 16px;
  }
  
  .assessment-modules :deep(.n-grid) {
    grid-template-columns: 1fr !important;
  }
  
  .assessment-statistics :deep(.n-grid) {
    grid-template-columns: repeat(2, 1fr) !important;
  }
}
</style>
