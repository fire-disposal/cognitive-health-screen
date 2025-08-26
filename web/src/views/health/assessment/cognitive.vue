<template>
  <div class="cognitive-assessment">
    <!-- 页面标题 -->
    <div class="assessment-header">
      <NButton text @click="goBack" class="back-btn">
        <template #icon>
          <TheIcon icon="mdi:arrow-left" />
        </template>
        返回
      </NButton>
      <div class="header-content">
        <div class="title-section">
          <TheIcon icon="mdi:brain" class="title-icon" />
          <h1 class="page-title">认知功能评估</h1>
        </div>
        <p class="page-subtitle">MMSE量表、MoCA量表等标准化认知功能评估工具</p>
      </div>
    </div>

    <!-- 评估工具选择 -->
    <div class="assessment-tools">
      <NGrid :cols="2" :x-gap="24" :y-gap="24">
        <!-- MMSE评估 -->
        <NGridItem>
          <NCard 
            class="tool-card mmse-card" 
            hoverable 
            @click="startAssessment('mmse')"
          >
            <div class="tool-content">
              <div class="tool-header">
                <div class="tool-icon">
                  <TheIcon icon="mdi:head-cog" />
                </div>
                <div class="tool-info">
                  <h3 class="tool-title">MMSE量表</h3>
                  <p class="tool-subtitle">简易精神状态检查</p>
                </div>
              </div>
              <div class="tool-description">
                <p>评估定向力、记忆力、注意力、计算力、语言能力等认知功能</p>
                <div class="tool-stats">
                  <span class="stat-item">
                    <TheIcon icon="mdi:clock-outline" />
                    约10-15分钟
                  </span>
                  <span class="stat-item">
                    <TheIcon icon="mdi:help-circle-outline" />
                    30题
                  </span>
                </div>
              </div>
              <div class="tool-action">
                <NButton type="primary" block>
                  开始MMSE评估
                </NButton>
              </div>
            </div>
          </NCard>
        </NGridItem>

        <!-- MoCA评估 -->
        <NGridItem>
          <NCard 
            class="tool-card moca-card" 
            hoverable 
            @click="startAssessment('moca')"
          >
            <div class="tool-content">
              <div class="tool-header">
                <div class="tool-icon">
                  <TheIcon icon="mdi:brain" />
                </div>
                <div class="tool-info">
                  <h3 class="tool-title">MoCA量表</h3>
                  <p class="tool-subtitle">蒙特利尔认知评估</p>
                </div>
              </div>
              <div class="tool-description">
                <p>更敏感的轻度认知障碍筛查工具，包含视空间、执行功能等</p>
                <div class="tool-stats">
                  <span class="stat-item">
                    <TheIcon icon="mdi:clock-outline" />
                    约15-20分钟
                  </span>
                  <span class="stat-item">
                    <TheIcon icon="mdi:help-circle-outline" />
                    8个认知域
                  </span>
                </div>
              </div>
              <div class="tool-action">
                <NButton type="primary" block>
                  开始MoCA评估
                </NButton>
              </div>
            </div>
          </NCard>
        </NGridItem>
      </NGrid>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content-grid">
      <NGrid :cols="12" :x-gap="24" :y-gap="24">
        <!-- 最近评估结果 -->
        <NGridItem :span="8">
          <NCard title="最近认知评估结果" class="results-card">
            <template #header-extra>
              <NButton text @click="viewAllResults">
                查看全部
                <template #icon>
                  <TheIcon icon="mdi:arrow-right" />
                </template>
              </NButton>
            </template>

            <div class="results-list">
              <div
                v-for="result in recentResults"
                :key="result.id"
                class="result-item"
                @click="viewResultDetail(result)"
              >
                <div class="result-info">
                  <div class="result-header">
                    <span class="result-type">{{ result.type }}</span>
                    <span class="result-date">{{ formatDate(result.date) }}</span>
                  </div>
                  <div class="result-patient">{{ result.patientName }}</div>
                  <div class="result-score">
                    <span class="score-label">总分:</span>
                    <span class="score-value" :class="getScoreClass(result.score, result.maxScore)">
                      {{ result.score }}/{{ result.maxScore }}
                    </span>
                  </div>
                </div>
                <div class="result-status">
                  <NTag :type="getStatusType(result.status)" size="small">
                    {{ result.status }}
                  </NTag>
                  <div class="result-trend" v-if="result.trend">
                    <TheIcon
                      :icon="result.trend === 'up' ? 'mdi:trending-up' : result.trend === 'down' ? 'mdi:trending-down' : 'mdi:trending-neutral'"
                      :class="getTrendClass(result.trend)"
                    />
                  </div>
                </div>
              </div>
            </div>
          </NCard>
        </NGridItem>

        <!-- 认知功能统计 -->
        <NGridItem :span="4">
          <div class="statistics-grid">
            <NGrid :cols="1" :y-gap="16">
              <NGridItem>
                <NCard class="stat-card compact">
                  <NStatistic label="总评估次数" :value="statistics.totalAssessments">
                    <template #prefix>
                      <TheIcon icon="mdi:clipboard-check" class="stat-icon" />
                    </template>
                  </NStatistic>
                </NCard>
              </NGridItem>
              <NGridItem>
                <NCard class="stat-card compact">
                  <NStatistic label="平均MMSE分数" :value="statistics.avgMMSEScore" :precision="1">
                    <template #prefix>
                      <TheIcon icon="mdi:chart-line" class="stat-icon" />
                    </template>
                    <template #suffix>
                      <span class="score-suffix">/30</span>
                    </template>
                  </NStatistic>
                </NCard>
              </NGridItem>
              <NGridItem>
                <NCard class="stat-card compact">
                  <NStatistic label="平均MoCA分数" :value="statistics.avgMoCAScore" :precision="1">
                    <template #prefix>
                      <TheIcon icon="mdi:chart-bar" class="stat-icon" />
                    </template>
                    <template #suffix>
                      <span class="score-suffix">/30</span>
                    </template>
                  </NStatistic>
                </NCard>
              </NGridItem>
              <NGridItem>
                <NCard class="stat-card compact">
                  <NStatistic label="异常检出率" :value="statistics.abnormalRate" :precision="1">
                    <template #prefix>
                      <TheIcon icon="mdi:alert-circle" class="stat-icon warning" />
                    </template>
                    <template #suffix>
                      <span class="score-suffix">%</span>
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
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  NCard, NButton, NGrid, NGridItem, NTag, NStatistic
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import api from '@/api'

const router = useRouter()

// 统计数据
const statistics = ref({
  totalAssessments: 45,
  avgMMSEScore: 26.8,
  avgMoCAScore: 24.2,
  abnormalRate: 15.6
})

// 最近评估结果
const recentResults = ref([
  {
    id: 1,
    type: 'MMSE',
    patientName: '张爷爷',
    date: '2024-01-15',
    score: 26,
    maxScore: 30,
    status: '正常',
    trend: 'up'
  },
  {
    id: 2,
    type: 'MoCA',
    patientName: '李奶奶',
    date: '2024-01-14',
    score: 22,
    maxScore: 30,
    status: '轻度异常',
    trend: 'down'
  },
  {
    id: 3,
    type: 'MMSE',
    patientName: '王叔叔',
    date: '2024-01-13',
    score: 28,
    maxScore: 30,
    status: '正常',
    trend: 'neutral'
  }
])

// 返回上级页面
function goBack() {
  router.push('/health/assessment')
}

// 开始评估
function startAssessment(type) {
  router.push(`/health/assessment/cognitive/${type}`)
}

// 查看所有结果
function viewAllResults() {
  router.push('/health/assessment/cognitive/results')
}

// 查看结果详情
function viewResultDetail(result) {
  router.push(`/health/assessment/cognitive/result/${result.id}`)
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

// 获取分数样式类
function getScoreClass(score, maxScore) {
  const percentage = (score / maxScore) * 100
  if (percentage >= 80) return 'score-good'
  if (percentage >= 60) return 'score-warning'
  return 'score-poor'
}

// 获取趋势样式类
function getTrendClass(trend) {
  const classMap = {
    'up': 'trend-up',
    'down': 'trend-down',
    'neutral': 'trend-neutral'
  }
  return classMap[trend] || ''
}

// 获取统计数据
async function fetchStatistics() {
  try {
    const response = await api.getCognitiveAssessments({ statistics: true })
    if (response.data) {
      statistics.value = response.data
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 获取最近结果
async function fetchRecentResults() {
  try {
    const response = await api.getCognitiveAssessments({ limit: 5, sort: 'date_desc' })
    if (response.data) {
      recentResults.value = response.data
    }
  } catch (error) {
    console.error('获取最近结果失败:', error)
  }
}

onMounted(() => {
  fetchStatistics()
  fetchRecentResults()
})
</script>

<style scoped>
.cognitive-assessment {
  padding: 24px;
  background: var(--n-color-hover);
  min-height: 100vh;
  overflow-y: auto;
  height: 100vh;
}

/* 页面标题 */
.assessment-header {
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

/* 评估工具卡片 */
.assessment-tools {
  margin-bottom: 32px;
}

.tool-card {
  cursor: pointer;
  transition: all 0.3s ease;
  height: 100%;
}

.tool-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.tool-content {
  padding: 24px;
}

.tool-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.tool-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  background: #FF6B6B;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: white;
}

.tool-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: var(--n-text-color-base);
}

.tool-subtitle {
  font-size: 14px;
  color: var(--n-text-color-placeholder);
  margin: 4px 0 0 0;
}

.tool-description {
  margin-bottom: 24px;
}

.tool-description p {
  font-size: 14px;
  color: var(--n-text-color-base);
  line-height: 1.5;
  margin: 0 0 12px 0;
}

.tool-stats {
  display: flex;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--n-text-color-placeholder);
}

/* 最近结果 */
.recent-results {
  margin-bottom: 32px;
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: var(--n-color-hover);
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.result-item:hover {
  background: var(--n-color-pressed);
}

.result-info {
  flex: 1;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.result-type {
  font-weight: 600;
  color: var(--n-text-color-base);
}

.result-date {
  font-size: 12px;
  color: var(--n-text-color-placeholder);
}

.result-patient {
  font-size: 14px;
  color: var(--n-text-color-placeholder);
  margin-bottom: 4px;
}

.result-score {
  font-size: 14px;
  color: var(--n-text-color-base);
}

.score-label {
  margin-right: 8px;
}

.score-value {
  font-weight: 600;
}

.score-value.score-good {
  color: var(--n-color-success);
}

.score-value.score-warning {
  color: var(--n-color-warning);
}

.score-value.score-poor {
  color: var(--n-color-error);
}

.result-status {
  display: flex;
  align-items: center;
  gap: 8px;
}

.result-trend {
  font-size: 16px;
}

.trend-up {
  color: var(--n-color-success);
}

.trend-down {
  color: var(--n-color-error);
}

.trend-neutral {
  color: var(--n-text-color-placeholder);
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
  font-size: 20px;
  color: #45B7D1;
}

.stat-icon.warning {
  color: #FFA726;
}

.score-suffix {
  font-size: 14px;
  color: var(--n-text-color-placeholder);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .cognitive-assessment {
    padding: 16px;
  }
  
  .assessment-tools :deep(.n-grid) {
    grid-template-columns: 1fr !important;
  }
  
  .cognitive-statistics :deep(.n-grid) {
    grid-template-columns: repeat(2, 1fr) !important;
  }
  
  .assessment-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
