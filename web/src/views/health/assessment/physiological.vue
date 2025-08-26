<template>
  <div class="physiological-assessment">
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
          <TheIcon icon="mdi:heart-pulse" class="title-icon" />
          <h1 class="page-title">生理健康评估</h1>
        </div>
        <p class="page-subtitle">血压、心率、睡眠质量等生理指标综合评估</p>
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

    <!-- 生理指标概览 -->
    <div class="indicators-overview">
      <NGrid :cols="4" :x-gap="16" :y-gap="16">
        <NGridItem>
          <NCard class="indicator-card blood-pressure">
            <div class="indicator-content">
              <div class="indicator-icon">
                <TheIcon icon="mdi:heart" />
              </div>
              <div class="indicator-info">
                <div class="indicator-label">血压</div>
                <div class="indicator-value">120/80</div>
                <div class="indicator-unit">mmHg</div>
              </div>
              <div class="indicator-status normal">
                <TheIcon icon="mdi:check-circle" />
              </div>
            </div>
          </NCard>
        </NGridItem>
        
        <NGridItem>
          <NCard class="indicator-card heart-rate">
            <div class="indicator-content">
              <div class="indicator-icon">
                <TheIcon icon="mdi:heart-pulse" />
              </div>
              <div class="indicator-info">
                <div class="indicator-label">心率</div>
                <div class="indicator-value">72</div>
                <div class="indicator-unit">bpm</div>
              </div>
              <div class="indicator-status normal">
                <TheIcon icon="mdi:check-circle" />
              </div>
            </div>
          </NCard>
        </NGridItem>
        
        <NGridItem>
          <NCard class="indicator-card sleep-quality">
            <div class="indicator-content">
              <div class="indicator-icon">
                <TheIcon icon="mdi:sleep" />
              </div>
              <div class="indicator-info">
                <div class="indicator-label">睡眠质量</div>
                <div class="indicator-value">85</div>
                <div class="indicator-unit">分</div>
              </div>
              <div class="indicator-status good">
                <TheIcon icon="mdi:check-circle" />
              </div>
            </div>
          </NCard>
        </NGridItem>
        
        <NGridItem>
          <NCard class="indicator-card body-temp">
            <div class="indicator-content">
              <div class="indicator-icon">
                <TheIcon icon="mdi:thermometer" />
              </div>
              <div class="indicator-info">
                <div class="indicator-label">体温</div>
                <div class="indicator-value">36.5</div>
                <div class="indicator-unit">°C</div>
              </div>
              <div class="indicator-status normal">
                <TheIcon icon="mdi:check-circle" />
              </div>
            </div>
          </NCard>
        </NGridItem>
      </NGrid>
    </div>

    <!-- 详细评估报告 -->
    <div class="assessment-reports">
      <NGrid :cols="2" :x-gap="24" :y-gap="24">
        <!-- 心血管健康 -->
        <NGridItem>
          <NCard title="心血管健康评估" class="report-card">
            <template #header-extra>
              <NTag type="success" size="small">良好</NTag>
            </template>
            
            <div class="report-content">
              <NGrid :cols="2" :x-gap="16" :y-gap="12">
                <NGridItem>
                  <div class="metric-item compact">
                    <div class="metric-header">
                      <span class="metric-label">收缩压</span>
                      <span class="metric-text">120 mmHg</span>
                    </div>
                    <NProgress
                      type="line"
                      :percentage="60"
                      :show-indicator="false"
                      color="#26D0CE"
                      :height="6"
                    />
                  </div>
                </NGridItem>

                <NGridItem>
                  <div class="metric-item compact">
                    <div class="metric-header">
                      <span class="metric-label">舒张压</span>
                      <span class="metric-text">80 mmHg</span>
                    </div>
                    <NProgress
                      type="line"
                      :percentage="53"
                      :show-indicator="false"
                      color="#26D0CE"
                      :height="6"
                    />
                  </div>
                </NGridItem>

                <NGridItem :span="2">
                  <div class="metric-item compact">
                    <div class="metric-header">
                      <span class="metric-label">静息心率</span>
                      <span class="metric-text">72 bpm</span>
                    </div>
                    <NProgress
                      type="line"
                      :percentage="72"
                      :show-indicator="false"
                      color="#52c41a"
                      :height="6"
                    />
                  </div>
                </NGridItem>
              </NGrid>
              
              <div class="assessment-summary">
                <p>心血管指标均在正常范围内，建议继续保持良好的生活习惯。</p>
              </div>
            </div>
          </NCard>
        </NGridItem>

        <!-- 睡眠质量分析 -->
        <NGridItem>
          <NCard title="睡眠质量分析" class="report-card">
            <template #header-extra>
              <NTag type="success" size="small">优秀</NTag>
            </template>
            
            <div class="report-content">
              <NGrid :cols="2" :x-gap="16" :y-gap="12">
                <NGridItem>
                  <div class="metric-item compact">
                    <div class="metric-header">
                      <span class="metric-label">睡眠时长</span>
                      <span class="metric-text">7.5 小时</span>
                    </div>
                    <NProgress
                      type="line"
                      :percentage="85"
                      :show-indicator="false"
                      color="#52c41a"
                      :height="6"
                    />
                  </div>
                </NGridItem>

                <NGridItem>
                  <div class="metric-item compact">
                    <div class="metric-header">
                      <span class="metric-label">深度睡眠</span>
                      <span class="metric-text">2.3 小时</span>
                    </div>
                    <NProgress
                      type="line"
                      :percentage="78"
                      :show-indicator="false"
                      color="#52c41a"
                      :height="6"
                    />
                  </div>
                </NGridItem>

                <NGridItem :span="2">
                  <div class="metric-item compact">
                    <div class="metric-header">
                      <span class="metric-label">睡眠效率</span>
                      <span class="metric-text">88%</span>
                    </div>
                    <NProgress
                      type="line"
                      :percentage="88"
                      :show-indicator="false"
                      color="#52c41a"
                      :height="6"
                    />
                  </div>
                </NGridItem>
              </NGrid>
              
              <div class="assessment-summary">
                <p>睡眠质量良好，深度睡眠充足，建议保持规律作息。</p>
              </div>
            </div>
          </NCard>
        </NGridItem>

        <!-- 体征监测 -->
        <NGridItem>
          <NCard title="体征监测" class="report-card">
            <template #header-extra>
              <NTag type="success" size="small">稳定</NTag>
            </template>
            
            <div class="report-content">
              <div class="metric-item">
                <div class="metric-label">体温</div>
                <div class="metric-value">
                  <NProgress 
                    type="line" 
                    :percentage="65" 
                    :show-indicator="false"
                    color="#52c41a"
                  />
                  <span class="metric-text">36.5°C</span>
                </div>
              </div>
              
              <div class="metric-item">
                <div class="metric-label">血氧饱和度</div>
                <div class="metric-value">
                  <NProgress 
                    type="line" 
                    :percentage="98" 
                    :show-indicator="false"
                    color="#52c41a"
                  />
                  <span class="metric-text">98%</span>
                </div>
              </div>
              
              <div class="metric-item">
                <div class="metric-label">呼吸频率</div>
                <div class="metric-value">
                  <NProgress 
                    type="line" 
                    :percentage="70" 
                    :show-indicator="false"
                    color="#52c41a"
                  />
                  <span class="metric-text">16 次/分</span>
                </div>
              </div>
              
              <div class="assessment-summary">
                <p>各项体征指标正常，身体状况稳定。</p>
              </div>
            </div>
          </NCard>
        </NGridItem>

        <!-- 运动能力 -->
        <NGridItem>
          <NCard title="运动能力评估" class="report-card">
            <template #header-extra>
              <NTag type="warning" size="small">一般</NTag>
            </template>
            
            <div class="report-content">
              <div class="metric-item">
                <div class="metric-label">日均步数</div>
                <div class="metric-value">
                  <NProgress 
                    type="line" 
                    :percentage="45" 
                    :show-indicator="false"
                    color="#faad14"
                  />
                  <span class="metric-text">4,500 步</span>
                </div>
              </div>
              
              <div class="metric-item">
                <div class="metric-label">活动时长</div>
                <div class="metric-value">
                  <NProgress 
                    type="line" 
                    :percentage="35" 
                    :show-indicator="false"
                    color="#faad14"
                  />
                  <span class="metric-text">25 分钟</span>
                </div>
              </div>
              
              <div class="metric-item">
                <div class="metric-label">卡路里消耗</div>
                <div class="metric-value">
                  <NProgress 
                    type="line" 
                    :percentage="40" 
                    :show-indicator="false"
                    color="#faad14"
                  />
                  <span class="metric-text">180 kcal</span>
                </div>
              </div>
              
              <div class="assessment-summary">
                <p>运动量略显不足，建议适当增加日常活动量。</p>
              </div>
            </div>
          </NCard>
        </NGridItem>
      </NGrid>
    </div>

    <!-- 历史趋势 -->
    <div class="trend-analysis">
      <NCard title="生理指标趋势分析" class="trend-card">
        <div class="trend-chart" ref="trendChart"></div>
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
const trendChart = ref(null)
let trendChartInstance = null

// 患者选择
const selectedPatientId = ref('1')
const patientOptions = ref([
  { label: '张爷爷 (78岁)', value: '1' },
  { label: '李奶奶 (82岁)', value: '2' },
  { label: '王叔叔 (75岁)', value: '3' },
  { label: '陈阿姨 (80岁)', value: '4' }
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
  
  const option = {
    title: {
      text: '近7天生理指标趋势',
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
      data: ['收缩压', '舒张压', '心率', '睡眠质量'],
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
      data: ['1/9', '1/10', '1/11', '1/12', '1/13', '1/14', '1/15']
    },
    yAxis: [
      {
        type: 'value',
        name: '血压/心率',
        position: 'left',
        axisLabel: {
          formatter: '{value}'
        }
      },
      {
        type: 'value',
        name: '睡眠质量',
        position: 'right',
        axisLabel: {
          formatter: '{value}分'
        }
      }
    ],
    series: [
      {
        name: '收缩压',
        type: 'line',
        data: [118, 122, 119, 121, 120, 123, 120],
        smooth: true,
        itemStyle: { color: '#ff6b6b' }
      },
      {
        name: '舒张压',
        type: 'line',
        data: [78, 82, 79, 81, 80, 83, 80],
        smooth: true,
        itemStyle: { color: '#4ecdc4' }
      },
      {
        name: '心率',
        type: 'line',
        data: [70, 74, 71, 73, 72, 75, 72],
        smooth: true,
        itemStyle: { color: '#45b7d1' }
      },
      {
        name: '睡眠质量',
        type: 'line',
        yAxisIndex: 1,
        data: [82, 88, 85, 87, 85, 89, 85],
        smooth: true,
        itemStyle: { color: '#f9ca24' }
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
.physiological-assessment {
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

/* 指标概览 */
.indicators-overview {
  margin-bottom: 32px;
}

.indicator-card {
  height: 100%;
}

.indicator-content {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
}

.indicator-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: white;
  background: #4ECDC4;
}

.indicator-info {
  flex: 1;
}

.indicator-label {
  font-size: 14px;
  color: var(--n-text-color-placeholder);
  margin-bottom: 4px;
}

.indicator-value {
  font-size: 24px;
  font-weight: 600;
  color: var(--n-text-color-base);
  line-height: 1;
}

.indicator-unit {
  font-size: 12px;
  color: var(--n-text-color-placeholder);
  margin-top: 2px;
}

.indicator-status {
  font-size: 20px;
}

.indicator-status.normal {
  color: var(--n-color-success);
}

.indicator-status.good {
  color: var(--n-color-success);
}

.indicator-status.warning {
  color: var(--n-color-warning);
}

/* 评估报告 */
.assessment-reports {
  margin-bottom: 32px;
}

.report-card {
  height: 100%;
}

.report-content {
  padding: 16px 0;
}

.metric-item {
  margin-bottom: 16px;
}

.metric-item:last-child {
  margin-bottom: 0;
}

.metric-item.compact {
  margin-bottom: 0;
}

.metric-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.metric-label {
  font-size: 14px;
  color: var(--n-text-color-base);
  margin-bottom: 8px;
}

.metric-value {
  display: flex;
  align-items: center;
  gap: 12px;
}

.metric-value :deep(.n-progress) {
  flex: 1;
}

.metric-text {
  font-size: 14px;
  font-weight: 600;
  color: var(--n-text-color-base);
  min-width: 80px;
  text-align: right;
}

.assessment-summary {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--n-border-color);
}

.assessment-summary p {
  font-size: 14px;
  color: var(--n-text-color-placeholder);
  margin: 0;
  line-height: 1.5;
}

/* 趋势分析 */
.trend-analysis {
  margin-bottom: 24px;
}

.trend-chart {
  height: 400px;
  width: 100%;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .physiological-assessment {
    padding: 16px;
  }
  
  .indicators-overview :deep(.n-grid) {
    grid-template-columns: repeat(2, 1fr) !important;
  }
  
  .assessment-reports :deep(.n-grid) {
    grid-template-columns: 1fr !important;
  }
  
  .assessment-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
