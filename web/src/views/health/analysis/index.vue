<template>
  <div class="analysis-container">
    <!-- 患者选择器 - 顶部中间位置 -->
    <div class="patient-selector-wrapper">
      <div class="patient-selector">
        <n-select
          v-model:value="selectedPatientId"
          :options="patientOptions"
          placeholder="请选择患者"
          size="large"
          filterable
          clearable
          :loading="loadingPatients"
          @update:value="handlePatientChange"
          class="patient-select"
        >
          <template #empty>
            <div class="empty-state">
              <n-icon size="24" color="#d0d0d0">
                <Icon icon="mdi:account-search" />
              </n-icon>
              <p>暂无患者数据</p>
            </div>
          </template>
        </n-select>
        <n-button
          type="primary"
          ghost
          @click="refreshData"
          :loading="refreshing"
          class="refresh-btn"
        >
          <template #icon>
            <n-icon>
              <Icon icon="mdi:refresh" />
            </n-icon>
          </template>
          刷新数据
        </n-button>
      </div>
    </div>

    <!-- 数据大屏内容区域 -->
    <div v-if="selectedPatientId" class="dashboard-content">
      <!-- 使用栅栏系统布局 -->
      <n-grid :cols="24" :x-gap="16" :y-gap="16" responsive="screen" class="dashboard-grid">
        <!-- 患者基本信息 - 全宽 -->
        <n-grid-item :span="24">
          <div class="module-card patient-info-module">
            <PatientInfoCard
              v-if="currentPatientInfo"
              :patient-data="currentPatientInfo"
              :loading="loadingInfo"
            />
            <div v-else class="loading-placeholder">
              <n-spin size="large" />
              <p>加载患者信息中...</p>
            </div>
          </div>
        </n-grid-item>

        <!-- 健康数据趋势 -->
        <n-grid-item :span="12" :xs="24" :sm="24" :md="12">
          <div class="module-card health-trends-module">
            <HealthTrendsChart
              v-if="healthTrendsData"
              :patient-id="selectedPatientId"
              :data="healthTrendsData"
              :loading="loadingTrends"
            />
            <div v-else class="loading-placeholder">
              <n-spin size="large" />
              <p>加载健康趋势中...</p>
            </div>
          </div>
        </n-grid-item>

        <!-- 设备状态分析 -->
        <n-grid-item :span="12" :xs="24" :sm="24" :md="12">
          <div class="module-card device-status-module">
            <DeviceStatusChart
              v-if="deviceAnalysisData"
              :patient-id="selectedPatientId"
              :data="deviceAnalysisData"
              :loading="loadingDevices"
            />
            <div v-else class="loading-placeholder">
              <n-spin size="large" />
              <p>加载设备状态中...</p>
            </div>
          </div>
        </n-grid-item>

        <!-- 健康评估分析 -->
        <n-grid-item :span="12" :xs="24" :sm="24" :md="12">
          <div class="module-card assessment-module">
            <AssessmentAnalysisChart
              v-if="assessmentAnalysisData"
              :patient-id="selectedPatientId"
              :data="assessmentAnalysisData"
              :loading="loadingAssessments"
            />
            <div v-else class="loading-placeholder">
              <n-spin size="large" />
              <p>加载评估分析中...</p>
            </div>
          </div>
        </n-grid-item>

        <!-- 数字孪生分析 -->
        <n-grid-item :span="12" :xs="24" :sm="24" :md="12">
          <div class="module-card digital-twin-module">
            <DigitalTwinAnalysisChart
              v-if="digitalTwinAnalysisData"
              :patient-id="selectedPatientId"
              :data="digitalTwinAnalysisData"
              :loading="loadingDigitalTwin"
            />
            <div v-else class="loading-placeholder">
              <n-spin size="large" />
              <p>加载数字孪生中...</p>
            </div>
          </div>
        </n-grid-item>

        <!-- 告警分析 -->
        <n-grid-item :span="12" :xs="24" :sm="24" :md="12">
          <div class="module-card alert-module">
            <AlertAnalysisChart
              v-if="alertAnalysisData"
              :patient-id="selectedPatientId"
              :data="alertAnalysisData"
              :loading="loadingAlerts"
            />
            <div v-else class="loading-placeholder">
              <n-spin size="large" />
              <p>加载告警分析中...</p>
            </div>
          </div>
        </n-grid-item>

        <!-- 风险分析 -->
        <n-grid-item :span="12" :xs="24" :sm="24" :md="12">
          <div class="module-card risk-module">
            <RiskAnalysisChart
              v-if="riskAnalysisData"
              :patient-id="selectedPatientId"
              :data="riskAnalysisData"
              :loading="loadingRisk"
            />
            <div v-else class="loading-placeholder">
              <n-spin size="large" />
              <p>加载风险分析中...</p>
            </div>
          </div>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- 未选择患者时的提示 -->
    <div v-else class="empty-dashboard">
      <div class="empty-content">
        <n-icon size="64" color="#d0d0d0">
          <Icon icon="mdi:chart-line" />
        </n-icon>
        <h3>统计分析</h3>
        <p>请选择患者以查看详细的统计分析数据</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { NSelect, NButton, NGrid, NGridItem, NIcon, NSpin } from 'naive-ui'
import { Icon } from '@iconify/vue'

// 导入图表组件
import PatientInfoCard from './components/PatientInfoCard.vue'
import HealthTrendsChart from './components/HealthTrendsChart.vue'
import DeviceStatusChart from './components/DeviceStatusChart.vue'
import AssessmentAnalysisChart from './components/AssessmentAnalysisChart.vue'
import DigitalTwinAnalysisChart from './components/DigitalTwinAnalysisChart.vue'
import AlertAnalysisChart from './components/AlertAnalysisChart.vue'
import RiskAnalysisChart from './components/RiskAnalysisChart.vue'

// 响应式数据
const selectedPatientId = ref(null)
const patientOptions = ref([])
const loadingPatients = ref(false)
const refreshing = ref(false)

// 各模块数据
const currentPatientInfo = ref(null)
const healthTrendsData = ref(null)
const deviceAnalysisData = ref(null)
const assessmentAnalysisData = ref(null)
const digitalTwinAnalysisData = ref(null)
const alertAnalysisData = ref(null)
const riskAnalysisData = ref(null)

// 加载状态
const loadingInfo = ref(false)
const loadingTrends = ref(false)
const loadingDevices = ref(false)
const loadingAssessments = ref(false)
const loadingDigitalTwin = ref(false)
const loadingAlerts = ref(false)
const loadingRisk = ref(false)

// 获取患者列表 - 使用模拟数据
const fetchPatients = async () => {
  try {
    loadingPatients.value = true
    // 模拟API延迟
    await new Promise(resolve => setTimeout(resolve, 500))

    // 使用模拟患者数据
    const mockPatients = [
      { patient_id: 'P001', name: '张奶奶', age: 75, gender: 'F', phone: '138****1234' },
      { patient_id: 'P002', name: '王爷爷', age: 82, gender: 'M', phone: '139****5678' },
      { patient_id: 'P003', name: '李阿姨', age: 68, gender: 'F', phone: '137****9012' },
      { patient_id: 'P004', name: '陈大爷', age: 79, gender: 'M', phone: '136****3456' },
      { patient_id: 'P005', name: '刘奶奶', age: 73, gender: 'F', phone: '135****7890' }
    ]

    patientOptions.value = mockPatients.map(patient => ({
      label: `${patient.name} (${patient.patient_id})`,
      value: patient.patient_id,
      patient: patient
    }))
  } catch (error) {
    console.error('获取患者列表失败:', error)
    // 移除错误提示，使用默认数据
  } finally {
    loadingPatients.value = false
  }
}

// 处理患者选择变化
const handlePatientChange = (patientId) => {
  if (patientId) {
    loadPatientAnalysisData(patientId)
  } else {
    clearAnalysisData()
  }
}

// 加载患者分析数据
const loadPatientAnalysisData = async (patientId) => {
  await Promise.all([
    loadPatientInfo(patientId),
    loadHealthTrends(patientId),
    loadDeviceAnalysis(patientId),
    loadAssessmentAnalysis(patientId),
    loadDigitalTwinAnalysis(patientId),
    loadAlertAnalysis(patientId),
    loadRiskAnalysis(patientId)
  ])
}

// 加载患者基本信息 - 使用模拟数据
const loadPatientInfo = async (patientId) => {
  try {
    loadingInfo.value = true
    // 模拟API延迟
    await new Promise(resolve => setTimeout(resolve, 300))

    // 根据患者ID生成模拟数据
    const selectedPatient = patientOptions.value.find(p => p.value === patientId)?.patient
    if (selectedPatient) {
      currentPatientInfo.value = {
        ...selectedPatient,
        birth_date: '1948-05-15',
        avatar: null,
        address: '北京市朝阳区某某街道',
        emergency_contact: '家属联系方式'
      }
    }
  } catch (error) {
    console.error('获取患者信息失败:', error)
  } finally {
    loadingInfo.value = false
  }
}

// 加载健康趋势数据 - 使用模拟数据
const loadHealthTrends = async (patientId) => {
  try {
    loadingTrends.value = true
    // 模拟API延迟
    await new Promise(resolve => setTimeout(resolve, 300))
    healthTrendsData.value = generateMockHealthTrends()
  } catch (error) {
    console.error('获取健康趋势数据失败:', error)
    healthTrendsData.value = generateMockHealthTrends()
  } finally {
    loadingTrends.value = false
  }
}

// 加载设备分析数据 - 使用模拟数据
const loadDeviceAnalysis = async (patientId) => {
  try {
    loadingDevices.value = true
    // 模拟API延迟
    await new Promise(resolve => setTimeout(resolve, 300))
    deviceAnalysisData.value = generateMockDeviceAnalysis()
  } catch (error) {
    console.error('获取设备分析数据失败:', error)
    deviceAnalysisData.value = generateMockDeviceAnalysis()
  } finally {
    loadingDevices.value = false
  }
}

// 加载评估分析数据 - 使用模拟数据
const loadAssessmentAnalysis = async (patientId) => {
  try {
    loadingAssessments.value = true
    // 模拟API延迟
    await new Promise(resolve => setTimeout(resolve, 300))
    assessmentAnalysisData.value = generateMockAssessmentAnalysis()
  } catch (error) {
    console.error('获取评估分析数据失败:', error)
    assessmentAnalysisData.value = generateMockAssessmentAnalysis()
  } finally {
    loadingAssessments.value = false
  }
}

// 加载数字孪生分析数据 - 使用模拟数据
const loadDigitalTwinAnalysis = async (patientId) => {
  try {
    loadingDigitalTwin.value = true
    // 模拟API延迟
    await new Promise(resolve => setTimeout(resolve, 300))
    digitalTwinAnalysisData.value = generateMockDigitalTwinAnalysis()
  } catch (error) {
    console.error('获取数字孪生分析数据失败:', error)
    digitalTwinAnalysisData.value = generateMockDigitalTwinAnalysis()
  } finally {
    loadingDigitalTwin.value = false
  }
}

// 加载告警分析数据 - 使用模拟数据
const loadAlertAnalysis = async (patientId) => {
  try {
    loadingAlerts.value = true
    // 模拟API延迟
    await new Promise(resolve => setTimeout(resolve, 300))
    alertAnalysisData.value = generateMockAlertAnalysis()
  } catch (error) {
    console.error('获取告警分析数据失败:', error)
    alertAnalysisData.value = generateMockAlertAnalysis()
  } finally {
    loadingAlerts.value = false
  }
}

// 加载风险分析数据 - 使用模拟数据
const loadRiskAnalysis = async (patientId) => {
  try {
    loadingRisk.value = true
    // 模拟API延迟
    await new Promise(resolve => setTimeout(resolve, 300))
    riskAnalysisData.value = generateMockRiskAnalysis()
  } catch (error) {
    console.error('获取风险分析数据失败:', error)
    riskAnalysisData.value = generateMockRiskAnalysis()
  } finally {
    loadingRisk.value = false
  }
}

// 清空分析数据
const clearAnalysisData = () => {
  currentPatientInfo.value = null
  healthTrendsData.value = null
  deviceAnalysisData.value = null
  assessmentAnalysisData.value = null
  digitalTwinAnalysisData.value = null
  alertAnalysisData.value = null
  riskAnalysisData.value = null
}

// 刷新数据
const refreshData = async () => {
  refreshing.value = true
  try {
    await fetchPatients()
    if (selectedPatientId.value) {
      await loadPatientAnalysisData(selectedPatientId.value)
    }
    console.log('数据刷新成功')
  } catch (error) {
    console.error('数据刷新失败:', error)
  } finally {
    refreshing.value = false
  }
}

// 模拟数据生成函数
const generateMockHealthTrends = () => {
  return {
    heartRate: Array.from({ length: 24 }, (_, i) => ({
      time: `${i}:00`,
      value: 70 + Math.random() * 20
    })),
    bloodPressure: Array.from({ length: 24 }, (_, i) => ({
      time: `${i}:00`,
      systolic: 120 + Math.random() * 20,
      diastolic: 80 + Math.random() * 10
    })),
    temperature: Array.from({ length: 24 }, (_, i) => ({
      time: `${i}:00`,
      value: 36.5 + Math.random() * 1
    }))
  }
}

const generateMockDeviceAnalysis = () => {
  return {
    totalDevices: 3,
    onlineDevices: 2,
    offlineDevices: 1,
    deviceStatus: [
      { name: '心率监测器', status: 'online', lastUpdate: '2分钟前' },
      { name: '血压计', status: 'online', lastUpdate: '5分钟前' },
      { name: '体温计', status: 'offline', lastUpdate: '2小时前' }
    ]
  }
}

const generateMockAssessmentAnalysis = () => {
  return {
    cognitive: { score: 85, level: '良好', lastTest: '2024-01-15' },
    physiological: { score: 78, level: '一般', lastTest: '2024-01-10' },
    adl: { score: 92, level: '优秀', lastTest: '2024-01-12' }
  }
}

const generateMockDigitalTwinAnalysis = () => {
  return {
    activityLevel: 75,
    environmentScore: 88,
    safetyIndex: 92,
    recentActivities: [
      { time: '08:00', activity: '起床', location: '卧室' },
      { time: '08:30', activity: '洗漱', location: '卫生间' },
      { time: '09:00', activity: '早餐', location: '厨房' }
    ]
  }
}

const generateMockAlertAnalysis = () => {
  return {
    totalAlerts: 12,
    criticalAlerts: 2,
    warningAlerts: 5,
    infoAlerts: 5,
    recentAlerts: [
      { time: '10:30', type: 'warning', message: '心率偏高' },
      { time: '09:15', type: 'info', message: '服药提醒' }
    ]
  }
}

const generateMockRiskAnalysis = () => {
  return {
    overallRisk: 'medium',
    riskScore: 65,
    riskFactors: [
      { factor: '心血管风险', level: 'medium', score: 70 },
      { factor: '跌倒风险', level: 'low', score: 30 },
      { factor: '认知风险', level: 'low', score: 25 }
    ]
  }
}

// 生命周期
onMounted(() => {
  fetchPatients()
})
</script>

<!-- 全局样式覆盖，确保页面可以滚动 -->
<style>
/* 临时覆盖全局样式，允许滚动 */
html, body {
  overflow: auto !important;
  height: auto !important;
}

#app {
  overflow: auto !important;
  height: auto !important;
}

.n-layout {
  overflow: visible !important;
  height: auto !important;
}

.n-layout-content {
  overflow-y: auto !important;
  height: auto !important;
  max-height: none !important;
}

/* 确保主内容区域可以滚动 */
section[class*="overflow-hidden"] {
  overflow-y: auto !important;
  height: auto !important;
}

/* 确保布局容器可以滚动 */
article[class*="overflow-hidden"] {
  overflow-y: auto !important;
  height: auto !important;
}
</style>

<style scoped>
.analysis-container {
  min-height: 100vh;
  background: #f0f4f8;
  padding: 20px;
  overflow-y: auto;
  scroll-behavior: smooth;
  position: relative;
}

/* 患者选择器样式 */
.patient-selector-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  padding: 16px 0;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.patient-selector {
  display: flex;
  align-items: center;
  gap: 16px;
  max-width: 600px;
  width: 100%;
}

.patient-select {
  flex: 1;
  min-width: 300px;
}

.refresh-btn {
  flex-shrink: 0;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  color: #999;
}

.empty-state p {
  margin: 8px 0 0 0;
  font-size: 14px;
}

/* 数据大屏样式 */
.dashboard-content {
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-grid {
  min-height: calc(100vh - 200px);
}

/* 模块卡片样式 */
.module-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  overflow: hidden;
  height: 100%;
  min-height: 300px;
}

.module-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

/* 不同模块的特色边框 - 高饱和度清爽配色 */
.patient-info-module {
  border-top: 4px solid #2563eb;
  background: linear-gradient(to right, #dbeafe 0%, #ffffff 100%);
}

.health-trends-module {
  border-top: 4px solid #0891b2;
  background: linear-gradient(to right, #cffafe 0%, #ffffff 100%);
}

.device-status-module {
  border-top: 4px solid #059669;
  background: linear-gradient(to right, #d1fae5 0%, #ffffff 100%);
}

.assessment-module {
  border-top: 4px solid #d97706;
  background: linear-gradient(to right, #fed7aa 0%, #ffffff 100%);
}

.digital-twin-module {
  border-top: 4px solid #7c3aed;
  background: linear-gradient(to right, #e9d5ff 0%, #ffffff 100%);
}

.alert-module {
  border-top: 4px solid #dc2626;
  background: linear-gradient(to right, #fecaca 0%, #ffffff 100%);
}

.risk-module {
  border-top: 4px solid #ea580c;
  background: linear-gradient(to right, #fed7aa 0%, #ffffff 100%);
}

/* 空状态样式 */
.empty-dashboard {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.empty-content {
  text-align: center;
  color: #6b7280;
}

.empty-content h3 {
  margin: 16px 0 8px 0;
  font-size: 24px;
  font-weight: 600;
  color: #374151;
}

.empty-content p {
  margin: 0;
  font-size: 16px;
  color: #9ca3af;
}

/* 加载占位符样式 */
.loading-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  color: #6b7280;
}

.loading-placeholder p {
  margin: 16px 0 0 0;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .analysis-container {
    padding: 16px;
  }

  .patient-selector {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .analysis-container {
    padding: 12px;
  }

  .patient-selector {
    flex-direction: column;
    gap: 12px;
  }

  .patient-select {
    min-width: auto;
    width: 100%;
  }

  .module-card {
    min-height: 250px;
  }
}

@media (max-width: 480px) {
  .patient-selector-wrapper {
    margin-bottom: 16px;
    padding: 12px 0;
  }

  .dashboard-grid {
    min-height: calc(100vh - 150px);
  }
}
</style>