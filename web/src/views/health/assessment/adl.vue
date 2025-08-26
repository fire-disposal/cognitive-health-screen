<template>
  <div class="adl-assessment">
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
          <TheIcon icon="mdi:account-check" class="title-icon" />
          <h1 class="page-title">日常生活能力评估</h1>
        </div>
        <p class="page-subtitle">ADL量表评估老人日常生活自理能力</p>
      </div>
      <div class="header-actions">
        <NSelect
          v-model:value="selectedPatientId"
          :options="patientOptions"
          placeholder="选择老人"
          class="patient-selector"
          @update:value="handlePatientChange"
        >
          <template #prefix>
            <TheIcon icon="mdi:account" />
          </template>
        </NSelect>
      </div>
    </div>

    <!-- ADL评估分类 -->
    <div class="adl-categories">
      <NGrid :cols="2" :x-gap="24" :y-gap="24">
        <!-- 基本日常生活活动 -->
        <NGridItem>
          <NCard title="基本日常生活活动 (BADL)" class="category-card">
            <template #header-extra>
              <NTag type="success" size="small">85/100</NTag>
            </template>
            
            <div class="activities-list">
              <div 
                v-for="activity in basicActivities" 
                :key="activity.id"
                class="activity-item"
              >
                <div class="activity-info">
                  <div class="activity-icon">
                    <TheIcon :icon="activity.icon" />
                  </div>
                  <div class="activity-details">
                    <div class="activity-name">{{ activity.name }}</div>
                    <div class="activity-description">{{ activity.description }}</div>
                  </div>
                </div>
                <div class="activity-score">
                  <NTag :type="getScoreType(activity.score)" size="small">
                    {{ getScoreLabel(activity.score) }}
                  </NTag>
                  <div class="score-value">{{ activity.score }}/4</div>
                </div>
              </div>
            </div>
            
            <div class="category-summary">
              <NProgress 
                type="line" 
                :percentage="85" 
                color="#52c41a"
                :show-indicator="false"
              />
              <p class="summary-text">基本生活自理能力良好，大部分活动可独立完成</p>
            </div>
          </NCard>
        </NGridItem>

        <!-- 工具性日常生活活动 -->
        <NGridItem>
          <NCard title="工具性日常生活活动 (IADL)" class="category-card">
            <template #header-extra>
              <NTag type="warning" size="small">65/100</NTag>
            </template>
            
            <div class="activities-list">
              <div 
                v-for="activity in instrumentalActivities" 
                :key="activity.id"
                class="activity-item"
              >
                <div class="activity-info">
                  <div class="activity-icon">
                    <TheIcon :icon="activity.icon" />
                  </div>
                  <div class="activity-details">
                    <div class="activity-name">{{ activity.name }}</div>
                    <div class="activity-description">{{ activity.description }}</div>
                  </div>
                </div>
                <div class="activity-score">
                  <NTag :type="getScoreType(activity.score)" size="small">
                    {{ getScoreLabel(activity.score) }}
                  </NTag>
                  <div class="score-value">{{ activity.score }}/4</div>
                </div>
              </div>
            </div>
            
            <div class="category-summary">
              <NProgress 
                type="line" 
                :percentage="65" 
                color="#faad14"
                :show-indicator="false"
              />
              <p class="summary-text">复杂活动需要一定协助，建议加强训练和支持</p>
            </div>
          </NCard>
        </NGridItem>
      </NGrid>
    </div>

    <!-- 综合评估结果 -->
    <div class="comprehensive-assessment">
      <NCard title="综合评估结果" class="result-card">
        <div class="result-content">
          <div class="overall-score">
            <div class="score-circle">
              <div class="score-number">75</div>
              <div class="score-label">总分</div>
            </div>
            <div class="score-interpretation">
              <h3>轻度功能障碍</h3>
              <p>日常生活基本能够自理，但在复杂活动方面需要适当协助</p>
            </div>
          </div>
          
          <div class="assessment-details">
            <NGrid :cols="3" :x-gap="16" :y-gap="16">
              <NGridItem>
                <div class="detail-item">
                  <div class="detail-label">独立完成</div>
                  <div class="detail-value">8项</div>
                  <div class="detail-percentage">67%</div>
                </div>
              </NGridItem>
              <NGridItem>
                <div class="detail-item">
                  <div class="detail-label">需要协助</div>
                  <div class="detail-value">3项</div>
                  <div class="detail-percentage">25%</div>
                </div>
              </NGridItem>
              <NGridItem>
                <div class="detail-item">
                  <div class="detail-label">无法完成</div>
                  <div class="detail-value">1项</div>
                  <div class="detail-percentage">8%</div>
                </div>
              </NGridItem>
            </NGrid>
          </div>
        </div>
      </NCard>
    </div>

    <!-- 改善建议 -->
    <div class="improvement-suggestions">
      <NCard title="改善建议" class="suggestions-card">
        <div class="suggestions-content">
          <NGrid :cols="3" :x-gap="24" :y-gap="24">
            <!-- 重点关注领域 -->
            <NGridItem>
              <div class="suggestion-category-card">
                <div class="category-header">
                  <div class="category-icon-wrapper">
                    <TheIcon icon="mdi:target" class="category-icon" />
                  </div>
                  <h4 class="category-title">重点关注领域</h4>
                </div>
                <div class="suggestion-list">
                  <div class="suggestion-item priority-high">
                    <TheIcon icon="mdi:alert-circle" class="suggestion-icon" />
                    <div class="suggestion-text">
                      <strong>购物能力：</strong>建议家属陪同购物，逐步培养独立购物能力
                    </div>
                  </div>
                  <div class="suggestion-item priority-medium">
                    <TheIcon icon="mdi:information" class="suggestion-icon" />
                    <div class="suggestion-text">
                      <strong>交通出行：</strong>可考虑使用辅助工具，如手杖或助行器
                    </div>
                  </div>
                </div>
              </div>
            </NGridItem>

            <!-- 康复训练建议 -->
            <NGridItem>
              <div class="suggestion-category-card">
                <div class="category-header">
                  <div class="category-icon-wrapper">
                    <TheIcon icon="mdi:lightbulb" class="category-icon" />
                  </div>
                  <h4 class="category-title">康复训练建议</h4>
                </div>
                <div class="suggestion-list">
                  <div class="suggestion-item">
                    <TheIcon icon="mdi:dumbbell" class="suggestion-icon" />
                    <div class="suggestion-text">
                      每日进行15-20分钟的平衡训练和肌力练习
                    </div>
                  </div>
                  <div class="suggestion-item">
                    <TheIcon icon="mdi:brain" class="suggestion-icon" />
                    <div class="suggestion-text">
                      参与认知训练活动，如拼图、记忆游戏等
                    </div>
                  </div>
                  <div class="suggestion-item">
                    <TheIcon icon="mdi:account-group" class="suggestion-icon" />
                    <div class="suggestion-text">
                      增加社交活动，参与社区老年活动中心的集体活动
                    </div>
                  </div>
                </div>
              </div>
            </NGridItem>

            <!-- 复评计划 -->
            <NGridItem>
              <div class="suggestion-category-card">
                <div class="category-header">
                  <div class="category-icon-wrapper">
                    <TheIcon icon="mdi:calendar-check" class="category-icon" />
                  </div>
                  <h4 class="category-title">复评计划</h4>
                </div>
                <div class="suggestion-list">
                  <div class="suggestion-item">
                    <TheIcon icon="mdi:calendar" class="suggestion-icon" />
                    <div class="suggestion-text">
                      建议3个月后进行复评，监测功能变化趋势
                    </div>
                  </div>
                  <div class="suggestion-item">
                    <TheIcon icon="mdi:phone" class="suggestion-icon" />
                    <div class="suggestion-text">
                      如有功能明显下降，请及时联系医护人员
                    </div>
                  </div>
                </div>
              </div>
            </NGridItem>
          </NGrid>
        </div>
      </NCard>
    </div>

    <!-- 历史评估记录 -->
    <div class="history-records">
      <NCard title="历史评估记录" class="history-card">
        <template #header-extra>
          <NButton text @click="viewAllHistory">
            查看全部
            <template #icon>
              <TheIcon icon="mdi:arrow-right" />
            </template>
          </NButton>
        </template>
        
        <div class="history-chart" ref="historyChart"></div>
      </NCard>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  NCard, NButton, NGrid, NGridItem, NTag, NProgress
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import * as echarts from 'echarts'
import api from '@/api'

const router = useRouter()
const historyChart = ref(null)
let historyChartInstance = null

// 患者选择
const selectedPatientId = ref('1')
const patientOptions = ref([
  { label: '张爷爷 (78岁)', value: '1' },
  { label: '李奶奶 (82岁)', value: '2' },
  { label: '王叔叔 (75岁)', value: '3' },
  { label: '陈阿姨 (80岁)', value: '4' }
])

// 基本日常生活活动
const basicActivities = ref([
  {
    id: 1,
    name: '进食',
    description: '独立进食，使用餐具',
    icon: 'mdi:food-fork-drink',
    score: 4
  },
  {
    id: 2,
    name: '洗澡',
    description: '独立洗澡或淋浴',
    icon: 'mdi:shower',
    score: 3
  },
  {
    id: 3,
    name: '穿衣',
    description: '选择和穿脱衣物',
    icon: 'mdi:tshirt-crew',
    score: 4
  },
  {
    id: 4,
    name: '如厕',
    description: '独立使用厕所',
    icon: 'mdi:toilet',
    score: 4
  },
  {
    id: 5,
    name: '行走',
    description: '室内外行走能力',
    icon: 'mdi:walk',
    score: 3
  }
])

// 工具性日常生活活动
const instrumentalActivities = ref([
  {
    id: 6,
    name: '购物',
    description: '独立购买日用品',
    icon: 'mdi:shopping',
    score: 2
  },
  {
    id: 7,
    name: '做饭',
    description: '准备简单餐食',
    icon: 'mdi:chef-hat',
    score: 3
  },
  {
    id: 8,
    name: '家务',
    description: '清洁和整理家务',
    icon: 'mdi:broom',
    score: 2
  },
  {
    id: 9,
    name: '交通',
    description: '使用交通工具出行',
    icon: 'mdi:bus',
    score: 2
  },
  {
    id: 10,
    name: '用药',
    description: '按时按量服药',
    icon: 'mdi:pill',
    score: 4
  }
])

// 返回上级页面
function goBack() {
  router.push('/health/assessment')
}

// 处理患者切换
function handlePatientChange(patientId) {
  console.log('切换到患者:', patientId)
  // 这里可以重新加载该患者的数据
  // 实际项目中会调用API获取新患者的数据
}

// 查看全部历史记录
function viewAllHistory() {
  router.push('/health/assessment/adl/history')
}

// 获取分数类型
function getScoreType(score) {
  if (score >= 4) return 'success'
  if (score >= 3) return 'warning'
  if (score >= 2) return 'error'
  return 'default'
}

// 获取分数标签
function getScoreLabel(score) {
  const labels = {
    4: '独立',
    3: '轻度协助',
    2: '中度协助',
    1: '重度协助',
    0: '完全依赖'
  }
  return labels[score] || '未评估'
}

// 初始化历史图表
function initHistoryChart() {
  if (historyChart.value) {
    historyChartInstance = echarts.init(historyChart.value)
    updateHistoryChart()
  }
}

// 更新历史图表
function updateHistoryChart() {
  if (!historyChartInstance) return
  
  const option = {
    title: {
      text: 'ADL评分趋势',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        return `${params[0].name}<br/>
                BADL: ${params[0].value}<br/>
                IADL: ${params[1].value}<br/>
                总分: ${params[2].value}`
      }
    },
    legend: {
      data: ['BADL', 'IADL', '总分'],
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
      data: ['3个月前', '2个月前', '1个月前', '本次']
    },
    yAxis: {
      type: 'value',
      name: '评分',
      min: 0,
      max: 100
    },
    series: [
      {
        name: 'BADL',
        type: 'line',
        data: [88, 87, 86, 85],
        smooth: true,
        itemStyle: { color: '#52c41a' }
      },
      {
        name: 'IADL',
        type: 'line',
        data: [70, 68, 66, 65],
        smooth: true,
        itemStyle: { color: '#faad14' }
      },
      {
        name: '总分',
        type: 'line',
        data: [79, 77.5, 76, 75],
        smooth: true,
        itemStyle: { color: '#1890ff' },
        lineStyle: { width: 3 }
      }
    ]
  }
  
  historyChartInstance.setOption(option)
}

// 处理窗口大小变化
function handleResize() {
  historyChartInstance?.resize()
}

onMounted(() => {
  setTimeout(() => {
    initHistoryChart()
  }, 100)
  
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  historyChartInstance?.dispose()
})
</script>

<style scoped>
.adl-assessment {
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

.header-actions {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-top: 8px;
}

.patient-selector {
  min-width: 200px;
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

/* ADL分类 */
.adl-categories {
  margin-bottom: 32px;
}

.category-card {
  height: 100%;
}

.activities-list {
  margin-bottom: 16px;
}

.activity-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--n-border-color);
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.activity-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: #45B7D1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  color: white;
}

.activity-details {
  flex: 1;
}

.activity-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--n-text-color-base);
  margin-bottom: 2px;
}

.activity-description {
  font-size: 12px;
  color: var(--n-text-color-placeholder);
}

.activity-score {
  display: flex;
  align-items: center;
  gap: 8px;
}

.score-value {
  font-size: 12px;
  color: var(--n-text-color-placeholder);
}

.category-summary {
  padding-top: 16px;
  border-top: 1px solid var(--n-border-color);
}

.summary-text {
  font-size: 14px;
  color: var(--n-text-color-placeholder);
  margin: 8px 0 0 0;
  line-height: 1.5;
}

/* 综合评估结果 */
.comprehensive-assessment {
  margin-bottom: 32px;
}

.result-content {
  padding: 24px 0;
}

.overall-score {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 24px;
}

.score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF9F43 0%, #FF6B6B 100%);
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

.score-interpretation {
  flex: 1;
}

.score-interpretation h3 {
  font-size: 20px;
  font-weight: 600;
  color: var(--n-text-color-base);
  margin: 0 0 8px 0;
}

.score-interpretation p {
  font-size: 16px;
  color: var(--n-text-color-placeholder);
  margin: 0;
  line-height: 1.5;
}

.assessment-details {
  padding-top: 24px;
  border-top: 1px solid var(--n-border-color);
}

.detail-item {
  text-align: center;
}

.detail-label {
  font-size: 14px;
  color: var(--n-text-color-placeholder);
  margin-bottom: 4px;
}

.detail-value {
  font-size: 24px;
  font-weight: 600;
  color: var(--n-text-color-base);
  margin-bottom: 2px;
}

.detail-percentage {
  font-size: 12px;
  color: var(--n-text-color-placeholder);
}

/* 改善建议 */
.improvement-suggestions {
  margin-bottom: 32px;
}

.suggestions-content {
  padding: 16px 0;
}

.suggestion-category-card {
  background: var(--n-color-hover);
  border-radius: 12px;
  padding: 20px;
  height: 100%;
  border: 1px solid var(--n-border-color);
}

.category-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.category-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: #45B7D1;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

.category-icon {
  font-size: 24px;
  color: white;
}

.category-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--n-text-color-base);
  margin: 0;
  text-align: center;
}

.suggestion-category {
  margin-bottom: 24px;
}

.suggestion-category:last-child {
  margin-bottom: 0;
}

.suggestion-category h4 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: var(--n-text-color-base);
  margin: 0 0 12px 0;
}

.suggestion-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.suggestion-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  background: var(--n-color-hover);
  border-radius: 8px;
}

.suggestion-item.priority-high {
  border-left: 4px solid var(--n-color-error);
}

.suggestion-item.priority-medium {
  border-left: 4px solid var(--n-color-warning);
}

.suggestion-icon {
  font-size: 16px;
  color: var(--n-color-primary);
  margin-top: 2px;
}

.suggestion-text {
  font-size: 14px;
  color: var(--n-text-color-base);
  line-height: 1.5;
}

/* 历史记录 */
.history-records {
  margin-bottom: 24px;
}

.history-chart {
  height: 300px;
  width: 100%;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .adl-assessment {
    padding: 16px;
  }
  
  .adl-categories :deep(.n-grid) {
    grid-template-columns: 1fr !important;
  }
  
  .assessment-details :deep(.n-grid) {
    grid-template-columns: 1fr !important;
  }
  
  .overall-score {
    flex-direction: column;
    text-align: center;
  }
  
  .assessment-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
