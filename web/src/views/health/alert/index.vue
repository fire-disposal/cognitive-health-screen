<template>
  <AppPage :show-footer="false">
    <div class="alert-center-container">
      <!-- 统计卡片区域 -->
      <div class="statistics-section">
        <n-grid :cols="4" :x-gap="16">
          <n-grid-item>
            <n-card class="stat-card critical" hoverable>
              <div class="stat-content">
                <div class="stat-icon">
                  <n-icon size="32" color="#ffffff">
                    <Icon icon="mdi:alert-circle" />
                  </n-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ statistics.critical || 0 }}</div>
                  <div class="stat-label">紧急告警</div>
                </div>
              </div>
            </n-card>
          </n-grid-item>
          <n-grid-item>
            <n-card class="stat-card warning" hoverable>
              <div class="stat-content">
                <div class="stat-icon">
                  <n-icon size="32" color="#ffffff">
                    <Icon icon="mdi:alert" />
                  </n-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ statistics.warning || 0 }}</div>
                  <div class="stat-label">警告告警</div>
                </div>
              </div>
            </n-card>
          </n-grid-item>
          <n-grid-item>
            <n-card class="stat-card info" hoverable>
              <div class="stat-content">
                <div class="stat-icon">
                  <n-icon size="32" color="#ffffff">
                    <Icon icon="mdi:information" />
                  </n-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ statistics.info || 0 }}</div>
                  <div class="stat-label">信息提示</div>
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
                  <div class="stat-label">今日总计</div>
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
              placeholder="搜索告警内容或规则名"
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
          <n-form-item label="级别">
            <n-select
              v-model:value="filters.level"
              placeholder="选择告警级别"
              clearable
              style="width: 120px"
              :options="levelOptions"
            />
          </n-form-item>
          <n-form-item label="状态">
            <n-select
              v-model:value="filters.status"
              placeholder="选择状态"
              clearable
              style="width: 120px"
              :options="statusOptions"
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

      <!-- 告警列表 -->
      <n-card class="alert-list-section" title="告警列表">
        <template #header-extra>
          <n-space>
            <n-button
              type="primary"
              :disabled="!selectedRowKeys.length"
              @click="handleBatchProcess"
            >
              <template #icon>
                <n-icon>
                  <Icon icon="mdi:check-all" />
                </n-icon>
              </template>
              批量处理 ({{ selectedRowKeys.length }})
            </n-button>
            <n-button @click="refreshData">
              <template #icon>
                <n-icon>
                  <Icon icon="mdi:refresh" />
                </n-icon>
              </template>
              刷新
            </n-button>
          </n-space>
        </template>

        <n-data-table
          :columns="columns"
          :data="alerts"
          :loading="loading"
          :pagination="pagination"
          :row-key="(row) => row.id"
          v-model:checked-row-keys="selectedRowKeys"
          @update:page="handlePageChange"
          @update:page-size="handlePageSizeChange"
        />
      </n-card>

      <!-- 告警详情抽屉 -->
      <n-drawer
        v-model:show="drawerVisible"
        :width="600"
        placement="right"
        title="告警详情"
      >
        <AlertDetail
          v-if="selectedAlert"
          :alert="selectedAlert"
          @update="handleAlertUpdate"
          @close="drawerVisible = false"
        />
      </n-drawer>

      <!-- 批量处理模态框 -->
      <n-modal
        v-model:show="batchModalVisible"
        preset="dialog"
        title="批量处理告警"
        positive-text="确认"
        negative-text="取消"
        @positive-click="confirmBatchProcess"
      >
        <div class="batch-process-content">
          <p>您选择了 {{ selectedRowKeys.length }} 条告警，请选择处理方式：</p>
          <n-radio-group v-model:value="batchAction">
            <n-space direction="vertical">
              <n-radio value="resolve">标记为已处理</n-radio>
              <n-radio value="ignore">忽略告警</n-radio>
              <n-radio value="delete">删除告警</n-radio>
            </n-space>
          </n-radio-group>
          <n-form-item label="处理备注" style="margin-top: 16px">
            <n-input
              v-model:value="batchRemark"
              type="textarea"
              placeholder="请输入处理备注（可选）"
              :rows="3"
            />
          </n-form-item>
        </div>
      </n-modal>
    </div>
  </AppPage>
</template>

<script setup>
import { ref, reactive, computed, onMounted, h } from 'vue'
import { Icon } from '@iconify/vue'
import { NButton, NTag, NSpace, useMessage } from 'naive-ui'
import api from '@/api'
import AlertDetail from './components/AlertDetail.vue'
import { formatDistanceToNow } from 'date-fns'
import { zhCN } from 'date-fns/locale'

const message = useMessage()

// 响应式数据
const loading = ref(false)
const alerts = ref([])
const statistics = ref({})
const selectedRowKeys = ref([])
const selectedAlert = ref(null)
const drawerVisible = ref(false)
const batchModalVisible = ref(false)
const batchAction = ref('resolve')
const batchRemark = ref('')

// 筛选条件
const filters = reactive({
  keyword: '',
  level: null,
  status: 'active', // 默认显示未处理的告警
  device_id: null,
  patient_id: null,
  dateRange: null
})

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  itemCount: 0,
  showSizePicker: true,
  pageSizes: [10, 20, 50, 100]
})

// 选项数据
const levelOptions = [
  { label: '紧急', value: 'critical' },
  { label: '警告', value: 'warning' },
  { label: '信息', value: 'info' }
]

const statusOptions = [
  { label: '未处理', value: 'active' },
  { label: '已处理', value: 'resolved' },
  { label: '已忽略', value: 'ignored' }
]

const deviceOptions = ref([])
const patientOptions = ref([])

// 表格列定义
const columns = [
  {
    type: 'selection'
  },
  {
    title: '级别',
    key: 'level',
    width: 80,
    render: (row) => {
      const levelConfig = {
        critical: { type: 'error', label: '紧急' },
        warning: { type: 'warning', label: '警告' },
        info: { type: 'info', label: '信息' }
      }
      const config = levelConfig[row.level] || { type: 'default', label: '未知' }
      return h(NTag, { type: config.type, size: 'small' }, { default: () => config.label })
    }
  },
  {
    title: '告警内容',
    key: 'message',
    ellipsis: {
      tooltip: true
    }
  },
  {
    title: '规则名称',
    key: 'rule_name',
    width: 120
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
    title: '状态',
    key: 'status',
    width: 80,
    render: (row) => {
      const statusConfig = {
        active: { type: 'error', label: '未处理' },
        resolved: { type: 'success', label: '已处理' },
        ignored: { type: 'default', label: '已忽略' }
      }
      const config = statusConfig[row.status] || { type: 'default', label: '未知' }
      return h(NTag, { type: config.type, size: 'small' }, { default: () => config.label })
    }
  },
  {
    title: '创建时间',
    key: 'created_at',
    width: 120,
    render: (row) => {
      return formatDistanceToNow(new Date(row.created_at), {
        addSuffix: true,
        locale: zhCN
      })
    }
  },
  {
    title: '操作',
    key: 'actions',
    width: 150,
    render: (row) => {
      return h(NSpace, { size: 'small' }, {
        default: () => [
          h(NButton, {
            size: 'small',
            type: 'primary',
            ghost: true,
            onClick: () => handleViewDetail(row)
          }, { default: () => '查看' }),
          h(NButton, {
            size: 'small',
            type: row.status === 'active' ? 'success' : 'default',
            ghost: true,
            disabled: row.status !== 'active',
            onClick: () => handleQuickProcess(row)
          }, { default: () => row.status === 'active' ? '处理' : '已处理' })
        ]
      })
    }
  }
]

// 获取告警列表
const fetchAlerts = async () => {
  try {
    loading.value = true
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      order_by: '-created_at'
    }

    // 添加筛选条件
    if (filters.keyword) params.keyword = filters.keyword
    if (filters.level) params.level = filters.level
    if (filters.status) params.status = filters.status
    if (filters.device_id) params.device_id = filters.device_id
    if (filters.patient_id) params.patient_id = filters.patient_id
    if (filters.dateRange && filters.dateRange.length === 2) {
      params.start_date = new Date(filters.dateRange[0]).toISOString()
      params.end_date = new Date(filters.dateRange[1]).toISOString()
    }

    const response = await api.getAlerts(params)
    alerts.value = response.data || []
    pagination.itemCount = response.total || 0
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
    statistics.value = response.data || {}
  } catch (error) {
    console.error('获取告警统计失败:', error)
  }
}

// 获取设备选项
const fetchDeviceOptions = async () => {
  try {
    const response = await api.getDeviceList({ page: 1, page_size: 1000 })
    deviceOptions.value = (response.data || []).map(device => ({
      label: `${device.device_id} - ${device.name || '未命名'}`,
      value: device.device_id
    }))
  } catch (error) {
    console.error('获取设备列表失败:', error)
  }
}

// 获取患者选项
const fetchPatientOptions = async () => {
  try {
    const response = await api.getPatientList({ page: 1, page_size: 1000 })
    patientOptions.value = (response.data || []).map(patient => ({
      label: `${patient.name} - ${patient.phone || ''}`,
      value: patient.id
    }))
  } catch (error) {
    console.error('获取患者列表失败:', error)
  }
}

// 刷新数据
const refreshData = async () => {
  await Promise.all([
    fetchAlerts(),
    fetchStatistics()
  ])
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchAlerts()
}

// 重置筛选条件
const handleReset = () => {
  Object.assign(filters, {
    keyword: '',
    level: null,
    status: 'active',
    device_id: null,
    patient_id: null,
    dateRange: null
  })
  pagination.page = 1
  fetchAlerts()
}

// 分页处理
const handlePageChange = (page) => {
  pagination.page = page
  fetchAlerts()
}

const handlePageSizeChange = (pageSize) => {
  pagination.pageSize = pageSize
  pagination.page = 1
  fetchAlerts()
}

// 查看详情
const handleViewDetail = (alert) => {
  selectedAlert.value = alert
  drawerVisible.value = true
}

// 快速处理
const handleQuickProcess = async (alert) => {
  try {
    await api.updateAlert(alert.id, {
      status: 'resolved',
      resolved_at: new Date().toISOString(),
      resolved_by: 'current_user' // 这里应该是当前用户ID
    })
    message.success('告警已处理')
    refreshData()
  } catch (error) {
    console.error('处理告警失败:', error)
    message.error('处理告警失败')
  }
}

// 批量处理
const handleBatchProcess = () => {
  if (!selectedRowKeys.value.length) {
    message.warning('请选择要处理的告警')
    return
  }
  batchModalVisible.value = true
}

// 确认批量处理
const confirmBatchProcess = async () => {
  try {
    const updateData = {
      resolved_at: new Date().toISOString(),
      resolved_by: 'current_user'
    }

    if (batchAction.value === 'resolve') {
      updateData.status = 'resolved'
    } else if (batchAction.value === 'ignore') {
      updateData.status = 'ignored'
    }

    if (batchRemark.value) {
      updateData.remark = batchRemark.value
    }

    // 批量更新告警
    const promises = selectedRowKeys.value.map(id => {
      if (batchAction.value === 'delete') {
        return api.deleteAlert(id)
      } else {
        return api.updateAlert(id, updateData)
      }
    })

    await Promise.all(promises)

    message.success(`成功${batchAction.value === 'delete' ? '删除' : '处理'}了 ${selectedRowKeys.value.length} 条告警`)
    selectedRowKeys.value = []
    batchModalVisible.value = false
    batchRemark.value = ''
    refreshData()
  } catch (error) {
    console.error('批量处理失败:', error)
    message.error('批量处理失败')
  }
}

// 告警更新回调
const handleAlertUpdate = () => {
  refreshData()
  drawerVisible.value = false
}

// 生命周期
onMounted(async () => {
  await Promise.all([
    fetchDeviceOptions(),
    fetchPatientOptions(),
    refreshData()
  ])
})
</script>

<style scoped>
.alert-center-container {
  padding: 16px;
  background: var(--n-color-hover);
  min-height: 100vh;
}

/* 统计卡片样式 */
.statistics-section {
  margin-bottom: 16px;
}

.stat-card {
  border: none;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.stat-card.critical {
  background: linear-gradient(135deg, #ff4757 0%, #ff3838 100%);
  color: white;
}

.stat-card.warning {
  background: linear-gradient(135deg, #ffa502 0%, #ff9500 100%);
  color: white;
}

.stat-card.info {
  background: linear-gradient(135deg, #3742fa 0%, #2f3542 100%);
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

/* 筛选区域样式 */
.filter-section {
  margin-bottom: 16px;
}

/* 告警列表样式 */
.alert-list-section {
  background: white;
  border-radius: 12px;
}

/* 批量处理模态框样式 */
.batch-process-content {
  padding: 16px 0;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .statistics-section :deep(.n-grid) {
    grid-template-columns: repeat(2, 1fr) !important;
  }
}

@media (max-width: 768px) {
  .alert-center-container {
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

/* 深色模式适配 */
@media (prefers-color-scheme: dark) {
  .alert-center-container {
    background: var(--n-color-base);
  }
}
</style>
