<template>
  <n-card title="告警中心" size="small" class="alert-panel">
    <template #header-extra>
      <n-space>
        <n-badge :value="unprocessedCount" :max="99" :show="unprocessedCount > 0">
          <n-button size="small" @click="refreshAlerts">
            <template #icon>
              <n-icon>
                <Icon icon="mdi:refresh" />
              </n-icon>
            </template>
            刷新
          </n-button>
        </n-badge>
        <n-button size="small" type="primary" @click="goToAlertCenter">
          查看全部
        </n-button>
      </n-space>
    </template>

    <!-- 告警统计 -->
    <div class="alert-stats" v-if="statistics">
      <n-grid :cols="3" :x-gap="12">
        <n-grid-item>
          <n-statistic label="总告警" :value="statistics.total">
            <template #prefix>
              <n-icon size="16" color="#666">
                <Icon icon="mdi:alert-circle-outline" />
              </n-icon>
            </template>
          </n-statistic>
        </n-grid-item>
        <n-grid-item>
          <n-statistic label="未处理" :value="statistics.active">
            <template #prefix>
              <n-icon size="16" color="#f5222d">
                <Icon icon="mdi:alert" />
              </n-icon>
            </template>
          </n-statistic>
        </n-grid-item>
        <n-grid-item>
          <n-statistic label="已处理" :value="statistics.resolved">
            <template #prefix>
              <n-icon size="16" color="#52c41a">
                <Icon icon="mdi:check-circle" />
              </n-icon>
            </template>
          </n-statistic>
        </n-grid-item>
      </n-grid>
    </div>

    <n-divider style="margin: 16px 0;" />

    <!-- 最新告警列表 -->
    <div class="alert-list">
      <div class="alert-list-header">
        <span class="alert-list-title">最新告警</span>
        <n-space>
          <n-select
            v-model:value="selectedLevel"
            size="small"
            placeholder="告警级别"
            clearable
            style="width: 100px"
            :options="levelOptions"
            @update:value="fetchAlerts"
          />
          <n-select
            v-model:value="selectedStatus"
            size="small"
            placeholder="状态"
            clearable
            style="width: 80px"
            :options="statusOptions"
            @update:value="fetchAlerts"
          />
        </n-space>
      </div>

      <n-spin :show="loading">
        <div v-if="alerts.length === 0" class="empty-alerts">
          <n-empty size="small" description="暂无告警">
            <template #icon>
              <n-icon size="32" color="#ccc">
                <Icon icon="mdi:shield-check" />
              </n-icon>
            </template>
          </n-empty>
        </div>

        <div v-else class="alert-items">
          <div
            v-for="alert in displayAlerts"
            :key="alert.id"
            class="alert-item"
            :class="`alert-${alert.level}`"
            @click="handleAlertClick(alert)"
          >
            <div class="alert-icon">
              <n-icon :size="16" :color="getAlertColor(alert.level)">
                <Icon :icon="getAlertIcon(alert.level)" />
              </n-icon>
            </div>
            <div class="alert-content">
              <div class="alert-message">{{ alert.message }}</div>
              <div class="alert-meta">
                <span class="alert-rule">{{ alert.rule_name }}</span>
                <span class="alert-time">{{ formatTime(alert.created_at) }}</span>
              </div>
            </div>
            <div class="alert-status">
              <n-tag
                :type="alert.status === 'active' ? 'error' : 'success'"
                size="small"
              >
                {{ alert.status === 'active' ? '未处理' : '已处理' }}
              </n-tag>
            </div>
          </div>
        </div>
      </n-spin>
    </div>

    <!-- 查看更多 -->
    <div class="alert-footer" v-if="alerts.length > maxDisplay">
      <n-button text size="small" @click="goToAlertCenter">
        查看全部 {{ totalCount }} 条告警
      </n-button>
    </div>
  </n-card>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Icon } from '@iconify/vue'
import { useMessage } from 'naive-ui'
import api from '@/api'
import { formatDistanceToNow } from 'date-fns'
import { zhCN } from 'date-fns/locale'

const message = useMessage()

// 响应式数据
const alerts = ref([])
const statistics = ref(null)
const loading = ref(false)
const totalCount = ref(0)
const selectedLevel = ref(null)
const selectedStatus = ref('active') // 默认只显示未处理的告警

// 配置
const maxDisplay = 8
const refreshInterval = 30000 // 30秒刷新一次

// 选项
const levelOptions = [
  { label: '信息', value: 'info' },
  { label: '警告', value: 'warning' },
  { label: '严重', value: 'critical' }
]

const statusOptions = [
  { label: '未处理', value: 'active' },
  { label: '已处理', value: 'resolved' }
]

// 计算属性
const displayAlerts = computed(() => {
  return alerts.value.slice(0, maxDisplay)
})

const unprocessedCount = computed(() => {
  return statistics.value?.active || 0
})

// 定时器
let refreshTimer = null

// 获取告警列表
const fetchAlerts = async () => {
  try {
    loading.value = true
    const params = {
      page: 1,
      page_size: 20,
      order_by: '-created_at'
    }
    
    if (selectedLevel.value) {
      params.level = selectedLevel.value
    }
    if (selectedStatus.value) {
      params.status = selectedStatus.value
    }

    const response = await api.getAlerts(params)
    alerts.value = response.data || []
    totalCount.value = response.total || 0
  } catch (error) {
    console.error('获取告警列表失败:', error)
    message.error('获取告警列表失败')
  } finally {
    loading.value = false
  }
}

// 获取告警统计
const fetchStatistics = async () => {
  try {
    const response = await api.getAlertStatistics()
    statistics.value = response.data || { total: 0, active: 0, resolved: 0 }
  } catch (error) {
    console.error('获取告警统计失败:', error)
  }
}

// 刷新告警数据
const refreshAlerts = async () => {
  await Promise.all([
    fetchAlerts(),
    fetchStatistics()
  ])
}

// 处理告警点击
const handleAlertClick = (alert) => {
  // 跳转到告警中心并显示该告警详情
  window.open(`/health/alert?id=${alert.id}`, '_blank')
}

// 跳转到告警中心
const goToAlertCenter = () => {
  // 跳转到健康管理的告警中心页面
  window.open('/health/alert', '_blank')
}

// 获取告警图标
const getAlertIcon = (level) => {
  switch (level) {
    case 'critical':
      return 'mdi:alert-circle'
    case 'warning':
      return 'mdi:alert'
    case 'info':
      return 'mdi:information'
    default:
      return 'mdi:bell'
  }
}

// 获取告警颜色
const getAlertColor = (level) => {
  switch (level) {
    case 'critical':
      return '#f5222d'
    case 'warning':
      return '#fa8c16'
    case 'info':
      return '#1890ff'
    default:
      return '#666'
  }
}

// 格式化时间
const formatTime = (timestamp) => {
  return formatDistanceToNow(new Date(timestamp), {
    addSuffix: true,
    locale: zhCN
  })
}

// 启动定时刷新
const startAutoRefresh = () => {
  refreshTimer = setInterval(refreshAlerts, refreshInterval)
}

// 停止定时刷新
const stopAutoRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
}

// 生命周期
onMounted(() => {
  refreshAlerts()
  startAutoRefresh()
})

onUnmounted(() => {
  stopAutoRefresh()
})
</script>

<style scoped>
.alert-panel {
  height: 100%;
}

.alert-stats {
  margin-bottom: 8px;
}

.alert-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.alert-list-title {
  font-weight: 500;
  font-size: 14px;
}

.alert-items {
  max-height: 300px;
  overflow-y: auto;
}

.empty-alerts {
  padding: 20px;
  text-align: center;
}

.alert-item {
  display: flex;
  align-items: flex-start;
  padding: 8px 12px;
  margin-bottom: 8px;
  border-radius: 6px;
  border-left: 3px solid #ddd;
  background: var(--n-color-hover);
  cursor: pointer;
  transition: all 0.2s;
}

.alert-item:hover {
  background: var(--n-color-pressed);
  transform: translateX(2px);
}

.alert-item.alert-critical {
  border-left-color: #f5222d;
  background: rgba(245, 34, 45, 0.05);
}

.alert-item.alert-warning {
  border-left-color: #fa8c16;
  background: rgba(250, 140, 22, 0.05);
}

.alert-item.alert-info {
  border-left-color: #1890ff;
  background: rgba(24, 144, 255, 0.05);
}

.alert-icon {
  margin-right: 8px;
  margin-top: 2px;
}

.alert-content {
  flex: 1;
  min-width: 0;
}

.alert-message {
  font-size: 13px;
  line-height: 1.4;
  margin-bottom: 4px;
  color: var(--n-text-color);
}

.alert-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 11px;
  color: var(--n-text-color-3);
}

.alert-rule {
  background: rgba(0, 0, 0, 0.1);
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 10px;
}

.alert-status {
  margin-left: 8px;
}

.alert-footer {
  text-align: center;
  padding-top: 12px;
  border-top: 1px solid var(--n-border-color);
  margin-top: 12px;
}
</style>
