<template>
  <n-card title="数字孪生分析" class="digital-twin-card">
    <template #header-extra>
      <n-tag type="info" size="small">
        <template #icon>
          <n-icon>
            <Icon icon="mdi:cube-scan" />
          </n-icon>
        </template>
        实时监控
      </n-tag>
    </template>

    <n-spin :show="loading">
      <div class="twin-content">
        <!-- 活动指标 -->
        <div class="activity-metrics">
          <div class="metric-card activity">
            <div class="metric-icon">
              <n-icon size="24" color="#10b981">
                <Icon icon="mdi:run" />
              </n-icon>
            </div>
            <div class="metric-info">
              <div class="metric-value">{{ twinData.activityLevel }}%</div>
              <div class="metric-label">活动水平</div>
            </div>
          </div>
          
          <div class="metric-card environment">
            <div class="metric-icon">
              <n-icon size="24" color="#3b82f6">
                <Icon icon="mdi:home-thermometer" />
              </n-icon>
            </div>
            <div class="metric-info">
              <div class="metric-value">{{ twinData.environmentScore }}</div>
              <div class="metric-label">环境评分</div>
            </div>
          </div>
          
          <div class="metric-card safety">
            <div class="metric-icon">
              <n-icon size="24" color="#f59e0b">
                <Icon icon="mdi:shield-check" />
              </n-icon>
            </div>
            <div class="metric-info">
              <div class="metric-value">{{ twinData.safetyIndex }}</div>
              <div class="metric-label">安全指数</div>
            </div>
          </div>
        </div>

        <!-- 活动分布 -->
        <div class="activity-distribution">
          <h4>活动分布</h4>
          <div class="activity-chart">
            <div v-for="activity in activityDistribution" :key="activity.name" class="activity-bar">
              <div class="activity-info">
                <span class="activity-name">{{ activity.name }}</span>
                <span class="activity-percentage">{{ activity.percentage }}%</span>
              </div>
              <div class="activity-progress">
                <div class="progress-fill" :style="{ width: activity.percentage + '%', backgroundColor: activity.color }"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- 环境监测 -->
        <div class="environment-monitor">
          <h4>环境数据</h4>
          <div class="env-grid">
            <div class="env-item temp">
              <div class="env-icon">
                <n-icon size="16" color="#dc2626">
                  <Icon icon="mdi:thermometer" />
                </n-icon>
              </div>
              <div class="env-content">
                <div class="env-value">{{ mockEnvData.temperature }}°C</div>
                <div class="env-label">温度</div>
              </div>
            </div>
            <div class="env-item humidity">
              <div class="env-icon">
                <n-icon size="16" color="#2563eb">
                  <Icon icon="mdi:water-percent" />
                </n-icon>
              </div>
              <div class="env-content">
                <div class="env-value">{{ mockEnvData.humidity }}%</div>
                <div class="env-label">湿度</div>
              </div>
            </div>
            <div class="env-item light">
              <div class="env-icon">
                <n-icon size="16" color="#d97706">
                  <Icon icon="mdi:white-balance-sunny" />
                </n-icon>
              </div>
              <div class="env-content">
                <div class="env-value">{{ mockEnvData.light }}</div>
                <div class="env-label">光照</div>
              </div>
            </div>
            <div class="env-item air">
              <div class="env-icon">
                <n-icon size="16" color="#059669">
                  <Icon icon="mdi:air-filter" />
                </n-icon>
              </div>
              <div class="env-content">
                <div class="env-value">{{ mockEnvData.airQuality }}</div>
                <div class="env-label">空气</div>
              </div>
            </div>
            <div class="env-item noise">
              <div class="env-icon">
                <n-icon size="16" color="#7c3aed">
                  <Icon icon="mdi:volume-high" />
                </n-icon>
              </div>
              <div class="env-content">
                <div class="env-value">{{ mockEnvData.noise }}dB</div>
                <div class="env-label">噪音</div>
              </div>
            </div>
            <div class="env-item motion">
              <div class="env-icon">
                <n-icon size="16" color="#0891b2">
                  <Icon icon="mdi:motion-sensor" />
                </n-icon>
              </div>
              <div class="env-content">
                <div class="env-value">{{ mockEnvData.motion }}</div>
                <div class="env-label">活动</div>
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
import { NCard, NTag, NSpin, NIcon } from 'naive-ui'
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

// 生成模拟数字孪生数据
const generateMockTwinData = () => {
  return {
    activityLevel: 75,
    environmentScore: 88,
    safetyIndex: 92,
    recentActivities: [
      { time: '08:00', activity: '起床', location: '卧室' },
      { time: '08:30', activity: '洗漱', location: '卫生间' },
      { time: '09:00', activity: '早餐', location: '厨房' },
      { time: '10:00', activity: '阅读', location: '客厅' },
      { time: '11:30', activity: '散步', location: '阳台' }
    ]
  }
}

const twinData = computed(() => {
  return props.data || generateMockTwinData()
})

// 模拟环境数据
const mockEnvData = computed(() => {
  return {
    temperature: (22 + Math.random() * 4).toFixed(1),
    humidity: Math.round(50 + Math.random() * 20),
    light: Math.round(300 + Math.random() * 200) + 'lx',
    airQuality: '优',
    noise: Math.round(35 + Math.random() * 15),
    motion: Math.random() > 0.5 ? '检测到' : '静止'
  }
})

// 活动分布数据
const activityDistribution = computed(() => {
  return [
    { name: '睡眠', percentage: 35, color: '#2563eb' },
    { name: '静坐', percentage: 25, color: '#059669' },
    { name: '轻度活动', percentage: 20, color: '#d97706' },
    { name: '中度活动', percentage: 15, color: '#dc2626' },
    { name: '高强度', percentage: 5, color: '#7c3aed' }
  ]
})
</script>

<style scoped>
.digital-twin-card {
  height: 100%;
}

.twin-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 活动指标 */
.activity-metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.metric-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
  border-left: 4px solid #e2e8f0;
}

.metric-card.activity {
  border-left-color: #10b981;
}

.metric-card.environment {
  border-left-color: #3b82f6;
}

.metric-card.safety {
  border-left-color: #f59e0b;
}

.metric-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.metric-info {
  flex: 1;
}

.metric-value {
  font-size: 20px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 4px;
}

.metric-label {
  font-size: 12px;
  color: #6b7280;
}

/* 活动分布 */
.activity-distribution h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.activity-chart {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.activity-bar {
  padding: 6px 8px;
  background: #ffffff;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
}

.activity-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.activity-name {
  font-size: 11px;
  font-weight: 600;
  color: #374151;
}

.activity-percentage {
  font-size: 10px;
  font-weight: 600;
  color: #6b7280;
}

.activity-progress {
  height: 8px;
  background: #f3f4f6;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  transition: width 0.3s ease;
  border-radius: 4px;
}

/* 环境监测 */
.environment-monitor h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.env-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.env-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px;
  background: white;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.env-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.env-item.temp {
  background: #fef2f2;
  border-color: #dc2626;
}

.env-item.humidity {
  background: #eff6ff;
  border-color: #2563eb;
}

.env-item.light {
  background: #fffbeb;
  border-color: #d97706;
}

.env-item.air {
  background: #f0fdf4;
  border-color: #059669;
}

.env-item.noise {
  background: #faf5ff;
  border-color: #7c3aed;
}

.env-item.motion {
  background: #f0f9ff;
  border-color: #0891b2;
}

.env-icon {
  flex-shrink: 0;
}

.env-content {
  flex: 1;
  text-align: center;
}

.env-value {
  font-size: 12px;
  font-weight: 700;
  color: #374151;
  margin-bottom: 1px;
}

.env-label {
  font-size: 9px;
  color: #6b7280;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .activity-metrics {
    grid-template-columns: 1fr;
  }
  
  .env-grid {
    grid-template-columns: 1fr;
  }
  
  .metric-card {
    padding: 12px;
  }
  
  .metric-icon {
    width: 40px;
    height: 40px;
  }
}
</style>
