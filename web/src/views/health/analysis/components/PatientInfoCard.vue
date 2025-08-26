<template>
  <n-card title="患者基本信息" class="patient-info-card">
    <template #header-extra>
      <n-tag type="success" size="small" v-if="patientData">
        <template #icon>
          <n-icon>
            <Icon icon="mdi:account-check" />
          </n-icon>
        </template>
        在线
      </n-tag>
    </template>

    <n-spin :show="loading">
      <div v-if="patientData" class="patient-content">
        <!-- 患者基本信息 -->
        <div class="patient-basic">
          <div class="patient-avatar">
            <n-avatar
              :size="80"
              :src="patientData.avatar"
              :fallback-src="'/avatars/default-patient.png'"
              class="avatar"
            >
              {{ patientData.name?.charAt(0) }}
            </n-avatar>
          </div>
          <div class="patient-details">
            <h3 class="patient-name">{{ patientData.name }}</h3>
            <div class="patient-meta">
              <span class="patient-id">ID: {{ patientData.patient_id }}</span>
              <span class="patient-age">{{ calculateAge(patientData.birth_date) }}岁</span>
              <span class="patient-gender">{{ patientData.gender === 'M' ? '男' : '女' }}</span>
            </div>
            <div class="patient-contact">
              <n-icon size="14">
                <Icon icon="mdi:phone" />
              </n-icon>
              {{ patientData.phone || '未填写' }}
            </div>
          </div>
        </div>

        <!-- 关键指标 -->
        <div class="vital-indicators">
          <n-grid :cols="6" :x-gap="12" :y-gap="12">
            <n-grid-item>
              <div class="indicator-card heart-rate">
                <div class="indicator-icon">
                  <n-icon size="20" color="#dc2626">
                    <Icon icon="mdi:heart-pulse" />
                  </n-icon>
                </div>
                <div class="indicator-content">
                  <div class="indicator-value">{{ latestVitals.heartRate || '--' }}</div>
                  <div class="indicator-label">心率</div>
                </div>
              </div>
            </n-grid-item>

            <n-grid-item>
              <div class="indicator-card blood-pressure">
                <div class="indicator-icon">
                  <n-icon size="20" color="#2563eb">
                    <Icon icon="mdi:heart-box" />
                  </n-icon>
                </div>
                <div class="indicator-content">
                  <div class="indicator-value">{{ latestVitals.systolic || '--' }}/{{ latestVitals.diastolic || '--' }}</div>
                  <div class="indicator-label">血压</div>
                </div>
              </div>
            </n-grid-item>

            <n-grid-item>
              <div class="indicator-card temperature">
                <div class="indicator-icon">
                  <n-icon size="20" color="#d97706">
                    <Icon icon="mdi:thermometer" />
                  </n-icon>
                </div>
                <div class="indicator-content">
                  <div class="indicator-value">{{ latestVitals.temperature || '--' }}</div>
                  <div class="indicator-label">体温</div>
                </div>
              </div>
            </n-grid-item>

            <n-grid-item>
              <div class="indicator-card oxygen">
                <div class="indicator-icon">
                  <n-icon size="20" color="#059669">
                    <Icon icon="mdi:lungs" />
                  </n-icon>
                </div>
                <div class="indicator-content">
                  <div class="indicator-value">{{ latestVitals.oxygenSaturation || '--' }}</div>
                  <div class="indicator-label">血氧</div>
                </div>
              </div>
            </n-grid-item>

            <n-grid-item>
              <div class="indicator-card steps">
                <div class="indicator-icon">
                  <n-icon size="20" color="#7c3aed">
                    <Icon icon="mdi:walk" />
                  </n-icon>
                </div>
                <div class="indicator-content">
                  <div class="indicator-value">{{ latestVitals.steps || '--' }}</div>
                  <div class="indicator-label">步数</div>
                </div>
              </div>
            </n-grid-item>

            <n-grid-item>
              <div class="indicator-card sleep">
                <div class="indicator-icon">
                  <n-icon size="20" color="#0891b2">
                    <Icon icon="mdi:sleep" />
                  </n-icon>
                </div>
                <div class="indicator-content">
                  <div class="indicator-value">{{ latestVitals.sleepHours || '--' }}</div>
                  <div class="indicator-label">睡眠</div>
                </div>
              </div>
            </n-grid-item>
          </n-grid>
        </div>

        <!-- 今日数据统计 -->
        <div class="daily-stats">
          <h4>今日数据</h4>
          <n-grid :cols="4" :x-gap="8">
            <n-grid-item>
              <div class="stat-item">
                <div class="stat-number">{{ dailyStats.measurements }}</div>
                <div class="stat-label">测量次数</div>
              </div>
            </n-grid-item>
            <n-grid-item>
              <div class="stat-item">
                <div class="stat-number">{{ dailyStats.alerts }}</div>
                <div class="stat-label">告警次数</div>
              </div>
            </n-grid-item>
            <n-grid-item>
              <div class="stat-item">
                <div class="stat-number">{{ dailyStats.activities }}</div>
                <div class="stat-label">活动记录</div>
              </div>
            </n-grid-item>
            <n-grid-item>
              <div class="stat-item">
                <div class="stat-number">{{ dailyStats.score }}</div>
                <div class="stat-label">健康评分</div>
              </div>
            </n-grid-item>
          </n-grid>
        </div>
      </div>

      <div v-else class="no-patient">
        <n-icon size="48" color="#d0d0d0">
          <Icon icon="mdi:account-question" />
        </n-icon>
        <p>暂无患者信息</p>
      </div>
    </n-spin>
  </n-card>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { NCard, NAvatar, NTag, NIcon, NSpin, NGrid, NGridItem } from 'naive-ui'
import { Icon } from '@iconify/vue'

const props = defineProps({
  patientData: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// 模拟最新生命体征数据
const latestVitals = computed(() => {
  if (!props.patientData) return {}

  return {
    heartRate: 72 + Math.floor(Math.random() * 20),
    systolic: 120 + Math.floor(Math.random() * 20),
    diastolic: 80 + Math.floor(Math.random() * 10),
    temperature: (36.5 + Math.random() * 1).toFixed(1),
    oxygenSaturation: 95 + Math.floor(Math.random() * 5),
    steps: 3500 + Math.floor(Math.random() * 2000),
    sleepHours: (6.5 + Math.random() * 2).toFixed(1)
  }
})

// 模拟今日统计数据
const dailyStats = computed(() => {
  return {
    measurements: 8 + Math.floor(Math.random() * 5),
    alerts: Math.floor(Math.random() * 3),
    activities: 12 + Math.floor(Math.random() * 8),
    score: 85 + Math.floor(Math.random() * 10)
  }
})

// 模拟最近活动数据
const recentActivities = computed(() => {
  if (!props.patientData) return []
  
  return [
    { id: 1, timestamp: new Date(Date.now() - 30 * 60 * 1000), description: '测量血压' },
    { id: 2, timestamp: new Date(Date.now() - 60 * 60 * 1000), description: '服用药物' },
    { id: 3, timestamp: new Date(Date.now() - 120 * 60 * 1000), description: '体温检测' }
  ]
})

// 计算年龄
const calculateAge = (birthDate) => {
  if (!birthDate) return '--'
  const birth = new Date(birthDate)
  const today = new Date()
  let age = today.getFullYear() - birth.getFullYear()
  const monthDiff = today.getMonth() - birth.getMonth()
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--
  }
  return age
}

// 格式化时间
const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 心率状态判断
const getHeartRateStatus = (heartRate) => {
  if (!heartRate) return 'unknown'
  if (heartRate < 60) return 'low'
  if (heartRate > 100) return 'high'
  return 'normal'
}

const getHeartRateText = (heartRate) => {
  const status = getHeartRateStatus(heartRate)
  const texts = {
    low: '偏低',
    normal: '正常',
    high: '偏高',
    unknown: '未知'
  }
  return texts[status]
}

// 血压状态判断
const getBloodPressureStatus = (systolic) => {
  if (!systolic) return 'unknown'
  if (systolic < 90) return 'low'
  if (systolic > 140) return 'high'
  return 'normal'
}

const getBloodPressureText = (systolic) => {
  const status = getBloodPressureStatus(systolic)
  const texts = {
    low: '偏低',
    normal: '正常',
    high: '偏高',
    unknown: '未知'
  }
  return texts[status]
}

// 体温状态判断
const getTemperatureStatus = (temperature) => {
  if (!temperature) return 'unknown'
  const temp = parseFloat(temperature)
  if (temp < 36) return 'low'
  if (temp > 37.5) return 'high'
  return 'normal'
}

const getTemperatureText = (temperature) => {
  const status = getTemperatureStatus(temperature)
  const texts = {
    low: '偏低',
    normal: '正常',
    high: '偏高',
    unknown: '未知'
  }
  return texts[status]
}

// 血氧状态判断
const getOxygenStatus = (oxygen) => {
  if (!oxygen) return 'unknown'
  if (oxygen < 95) return 'low'
  return 'normal'
}

const getOxygenText = (oxygen) => {
  const status = getOxygenStatus(oxygen)
  const texts = {
    low: '偏低',
    normal: '正常',
    unknown: '未知'
  }
  return texts[status]
}
</script>

<style scoped>
.patient-info-card {
  height: 100%;
}

.patient-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 患者基本信息 */
.patient-basic {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  background: #2563eb;
  border-radius: 8px;
  color: white;
}

.patient-avatar .avatar {
  border: 3px solid rgba(255, 255, 255, 0.3);
}

.patient-details {
  flex: 1;
}

.patient-name {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
}

.patient-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 8px;
  font-size: 14px;
  opacity: 0.9;
}

.patient-contact {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  opacity: 0.8;
}

/* 关键指标 */
.vital-indicators {
  margin: 12px 0;
}

.indicator-card {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #ffffff;
  border-radius: 8px;
  border: 2px solid #e5e7eb;
  transition: all 0.2s ease;
  min-height: 60px;
}

.indicator-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.indicator-card.heart-rate {
  border-color: #dc2626;
  background: #fef2f2;
}

.indicator-card.blood-pressure {
  border-color: #2563eb;
  background: #eff6ff;
}

.indicator-card.temperature {
  border-color: #d97706;
  background: #fffbeb;
}

.indicator-card.oxygen {
  border-color: #059669;
  background: #f0fdf4;
}

.indicator-card.steps {
  border-color: #7c3aed;
  background: #faf5ff;
}

.indicator-card.sleep {
  border-color: #0891b2;
  background: #f0f9ff;
}

.indicator-content {
  flex: 1;
  text-align: center;
}

.indicator-value {
  font-size: 16px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 2px;
  line-height: 1.2;
}

.indicator-label {
  font-size: 10px;
  color: #6b7280;
  font-weight: 500;
}

/* 今日数据统计 */
.daily-stats h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.stat-item {
  text-align: center;
  padding: 8px;
  background: #ffffff;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.stat-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-number {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 2px;
}

.stat-label {
  font-size: 10px;
  color: #6b7280;
  font-weight: 500;
}

/* 无患者状态 */
.no-patient {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #9ca3af;
}

.no-patient p {
  margin: 12px 0 0 0;
  font-size: 16px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .patient-basic {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }

  .patient-meta {
    justify-content: center;
  }

  .indicator-card {
    flex-direction: column;
    text-align: center;
    gap: 8px;
  }

  .indicator-content {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
}
</style>
