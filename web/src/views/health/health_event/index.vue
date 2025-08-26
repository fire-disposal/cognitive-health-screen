<template>
  <AppPage :show-footer="false">
    <div class="event-center-container">
      <!-- 统计卡片区域 -->
      <div class="statistics-section">
        <n-grid :cols="3" :x-gap="16">
          <n-grid-item>
            <n-card class="stat-card abnormal" hoverable>
              <div class="stat-content">
                <div class="stat-icon">
                  <n-icon size="32" color="#ffffff">
                    <Icon icon="mdi:alert-decagram" />
                  </n-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ statistics.abnormal || 0 }}</div>
                  <div class="stat-label">异常事件</div>
                </div>
              </div>
            </n-card>
          </n-grid-item>
          <n-grid-item>
            <n-card class="stat-card medication" hoverable>
              <div class="stat-content">
                <div class="stat-icon">
                  <n-icon size="32" color="#ffffff">
                    <Icon icon="mdi:pill" />
                  </n-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ statistics.medication || 0 }}</div>
                  <div class="stat-label">用药事件</div>
                </div>
              </div>
            </n-card>
          </n-grid-item>
          <n-grid-item>
            <n-card class="stat-card total" hoverable>
              <div class="stat-content">
                <div class="stat-icon">
                  <n-icon size="32" color="#ffffff">
                    <Icon icon="mdi:chart-line" />
                  </n-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ statistics.total || 0 }}</div>
                  <div class="stat-label">事件总数</div>
                </div>
              </div>
            </n-card>
          </n-grid-item>
        </n-grid>
      </div>

      <!-- 筛选区域 -->
      <n-card class="filter-section" title="筛选条件">
        <n-form inline :model="filters" label-placement="left">
          <n-form-item label="关键词">
            <n-input
              v-model:value="filters.keyword"
              placeholder="搜索事件内容或类型"
              clearable
              style="width: 200px"
              @keyup.enter="handleSearch"
            >
              <template #prefix>
                <n-icon>
                  <Icon icon="mdi:magnify" />
                </n-icon>
              </template>
            </n-input>
          </n-form-item>
          <n-form-item label="类型">
            <n-select
              v-model:value="filters.event_type"
              placeholder="选择事件类型"
              clearable
              style="width: 120px"
              :options="eventTypeOptions"
            />
          </n-form-item>
          <n-form-item label="设备">
            <n-select
              v-model:value="filters.device_id"
              placeholder="选择设备"
              clearable
              filterable
              style="width: 150px"
              :options="deviceOptions"
            />
          </n-form-item>
          <n-form-item label="患者">
            <n-select
              v-model:value="filters.patient_id"
              placeholder="选择患者"
              clearable
              filterable
              style="width: 150px"
              :options="patientOptions"
            />
          </n-form-item>
          <n-form-item label="时间">
            <n-date-picker
              v-model:value="filters.dateRange"
              type="daterange"
              clearable
              style="width: 240px"
            />
          </n-form-item>
          <n-form-item>
            <n-space>
              <n-button type="primary" @click="handleSearch">
                <template #icon>
                  <n-icon>
                    <Icon icon="mdi:magnify" />
                  </n-icon>
                </template>
                搜索
              </n-button>
              <n-button @click="handleReset">
                <template #icon>
                  <n-icon>
                    <Icon icon="mdi:refresh" />
                  </n-icon>
                </template>
                重置
              </n-button>
            </n-space>
          </n-form-item>
        </n-form>
      </n-card>

      <!-- 事件列表 -->
      <n-card class="event-list-section" title="健康事件列表">
        <n-data-table
          :columns="columns"
          :data="events"
          :loading="loading"
          :pagination="pagination"
          :row-key="(row) => row.id"
          @update:page="handlePageChange"
          @update:page-size="handlePageSizeChange"
        />
      </n-card>

      <!-- 事件详情抽屉 -->
      <n-drawer
        v-model:show="drawerVisible"
        :width="600"
        placement="right"
        title="事件详情"
      >
        <n-card>
          <n-descriptions :column="2" label-placement="left">
            <n-descriptions-item label="事件类型">
              {{ selectedEvent?.event_type || '-' }}
            </n-descriptions-item>
            <n-descriptions-item label="设备ID">
              {{ selectedEvent?.device_id || '-' }}
            </n-descriptions-item>
            <n-descriptions-item label="患者">
              {{ selectedEvent?.patient_name || '-' }}
            </n-descriptions-item>
            <n-descriptions-item label="发生时间">
              {{ formatDateTime(selectedEvent?.event_time) }}
            </n-descriptions-item>
            <n-descriptions-item label="事件内容" :span="2">
              <div class="event-message">{{ selectedEvent?.description }}</div>
            </n-descriptions-item>
            <n-descriptions-item label="扩展信息" v-if="selectedEvent?.extra" :span="2">
              <n-code :code="JSON.stringify(selectedEvent.extra, null, 2)" language="json" />
            </n-descriptions-item>
          </n-descriptions>
        </n-card>
      </n-drawer>
    </div>
  </AppPage>
</template>

<script setup>
import { ref, reactive, onMounted, h } from 'vue'
import { Icon } from '@iconify/vue'
import { NButton, NTag, NSpace, useMessage } from 'naive-ui'
import api from '@/api'
import { format } from 'date-fns'
import { zhCN } from 'date-fns/locale'

const message = useMessage()

const loading = ref(false)
const events = ref([])
const statistics = ref({})
const selectedEvent = ref(null)
const drawerVisible = ref(false)

const filters = reactive({
  keyword: '',
  event_type: null,
  device_id: null,
  patient_id: null,
  dateRange: null
})

const pagination = reactive({
  page: 1,
  pageSize: 20,
  itemCount: 0,
  showSizePicker: true,
  pageSizes: [10, 20, 50, 100]
})

const eventTypeOptions = [
  { label: '异常', value: 'abnormal' },
  { label: '用药', value: 'medication' },
  { label: '跌倒', value: 'fall' },
  { label: '睡眠', value: 'sleep_stage' }
]

const deviceOptions = ref([])
const patientOptions = ref([])

const columns = [
  {
    title: '类型',
    key: 'event_type',
    width: 100
  },
  {
    title: '内容',
    key: 'description',
    ellipsis: { tooltip: true }
  },
  {
    title: '设备/患者',
    key: 'device_patient',
    width: 150,
    render: (row) => {
      return h('div', [
        h('div', { style: 'font-size: 12px; color: #666;' }, `设备: ${row.device_id || '-'}`),
        h('div', { style: 'font-size: 12px; color: #666;' }, `患者: ${row.patient_name || '-'}`)
      ])
    }
  },
  {
    title: '时间',
    key: 'event_time',
    width: 120,
    render: (row) => {
      return formatDateTime(row.event_time)
    }
  },
  {
    title: '操作',
    key: 'actions',
    width: 100,
    render: (row) => {
      return h(NButton, {
        size: 'small',
        type: 'primary',
        ghost: true,
        onClick: () => handleViewDetail(row)
      }, { default: () => '查看' })
    }
  }
]

const fetchEvents = async () => {
  try {
    loading.value = true
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      order_by: '-event_time'
    }
    if (filters.keyword) params.keyword = filters.keyword
    if (filters.event_type) params.event_type = filters.event_type
    if (filters.device_id) params.device_id = filters.device_id
    if (filters.patient_id) params.patient_id = filters.patient_id
    if (filters.dateRange && filters.dateRange.length === 2) {
      params.start_date = new Date(filters.dateRange[0]).toISOString()
      params.end_date = new Date(filters.dateRange[1]).toISOString()
    }
    const response = await api.getHealthEvents(params)
    events.value = response.data || []
    pagination.itemCount = response.total || 0
  } catch (error) {
    message.error('获取事件列表失败')
  } finally {
    loading.value = false
  }
}

const fetchStatistics = async () => {
  try {
    const response = await api.getHealthEventStatistics()
    statistics.value = response.data || {}
  } catch (error) {}
}

const fetchDeviceOptions = async () => {
  try {
    const response = await api.getDevices({ page: 1, page_size: 1000 })
    deviceOptions.value = (response.data || []).map(device => ({
      label: `${device.device_id} - ${device.name || '未命名'}`,
      value: device.device_id
    }))
  } catch (error) {}
}

const fetchPatientOptions = async () => {
  try {
    const response = await api.getPatients({ page: 1, page_size: 1000 })
    patientOptions.value = (response.data || []).map(patient => ({
      label: `${patient.name} - ${patient.phone || ''}`,
      value: patient.id
    }))
  } catch (error) {}
}

const refreshData = async () => {
  await Promise.all([
    fetchEvents(),
    fetchStatistics()
  ])
}

const handleSearch = () => {
  pagination.page = 1
  fetchEvents()
}

const handleReset = () => {
  Object.assign(filters, {
    keyword: '',
    event_type: null,
    device_id: null,
    patient_id: null,
    dateRange: null
  })
  pagination.page = 1
  fetchEvents()
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchEvents()
}

const handlePageSizeChange = (pageSize) => {
  pagination.pageSize = pageSize
  pagination.page = 1
  fetchEvents()
}

const handleViewDetail = (event) => {
  selectedEvent.value = event
  drawerVisible.value = true
}

const formatDateTime = (dateTime) => {
  if (!dateTime) return '-'
  return format(new Date(dateTime), 'yyyy-MM-dd HH:mm:ss', { locale: zhCN })
}

onMounted(async () => {
  await Promise.all([
    fetchDeviceOptions(),
    fetchPatientOptions(),
    refreshData()
  ])
})
</script>

<style scoped>
.event-center-container {
  padding: 16px;
  background: var(--n-color-hover);
  min-height: 100vh;
}
.statistics-section {
  margin-bottom: 16px;
}
.stat-card {
  border: none;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}
.stat-card.abnormal {
  background: linear-gradient(135deg, #ff4757 0%, #ff3838 100%);
  color: white;
}
.stat-card.medication {
  background: linear-gradient(135deg, #ffa502 0%, #ff9500 100%);
  color: white;
}
.stat-card.total {
  background: linear-gradient(135deg, #2ed573 0%, #1e90ff 100%);
  color: white;
}
.stat-content {
  display: flex;
  align-items: center;
  padding: 20px;
}
.stat-icon {
  margin-right: 16px;
}
.stat-info {
  flex: 1;
}
.stat-value {
  font-size: 28px;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 4px;
}
.stat-label {
  font-size: 14px;
  opacity: 0.9;
}
.filter-section {
  margin-bottom: 16px;
}
.event-list-section {
  background: white;
  border-radius: 12px;
}
.event-message {
  padding: 8px 12px;
  background: var(--n-color-hover);
  border-radius: 6px;
  border-left: 4px solid var(--n-color-primary);
  font-size: 14px;
  line-height: 1.5;
}
@media (max-width: 1200px) {
  .statistics-section :deep(.n-grid) {
    grid-template-columns: repeat(2, 1fr) !important;
  }
}
@media (max-width: 768px) {
  .event-center-container {
    padding: 8px;
  }
  .statistics-section :deep(.n-grid) {
    grid-template-columns: 1fr !important;
  }
  .stat-content {
    padding: 16px;
  }
  .stat-value {
    font-size: 24px;
  }
}
@media (prefers-color-scheme: dark) {
  .event-center-container {
    background: var(--n-color-base);
  }
  .event-message {
    background: var(--n-color-pressed);
  }
}
</style>