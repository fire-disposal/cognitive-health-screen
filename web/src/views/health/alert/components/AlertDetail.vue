<template>
  <div class="alert-detail">
    <!-- 告警基本信息 -->
    <n-card title="告警信息" size="small" class="detail-card">
      <n-descriptions :column="2" label-placement="left">
        <n-descriptions-item label="告警级别">
          <n-tag :type="getLevelTagType(alert.level)" size="medium">
            <template #icon>
              <n-icon>
                <Icon :icon="getLevelIcon(alert.level)" />
              </n-icon>
            </template>
            {{ getLevelText(alert.level) }}
          </n-tag>
        </n-descriptions-item>
        <n-descriptions-item label="告警状态">
          <n-tag :type="getStatusTagType(alert.status)" size="medium">
            {{ getStatusText(alert.status) }}
          </n-tag>
        </n-descriptions-item>
        <n-descriptions-item label="规则名称">
          {{ alert.rule_name || '-' }}
        </n-descriptions-item>
        <n-descriptions-item label="设备ID">
          {{ alert.device_id || '-' }}
        </n-descriptions-item>
        <n-descriptions-item label="患者信息">
          {{ alert.patient_name || '-' }}
        </n-descriptions-item>
        <n-descriptions-item label="创建时间">
          {{ formatDateTime(alert.created_at) }}
        </n-descriptions-item>
        <n-descriptions-item label="告警内容" :span="2">
          <div class="alert-message">{{ alert.message }}</div>
        </n-descriptions-item>
      </n-descriptions>
    </n-card>

    <!-- 告警详细数据 -->
    <n-card title="详细数据" size="small" class="detail-card" v-if="alert.data">
      <n-code :code="JSON.stringify(alert.data, null, 2)" language="json" />
    </n-card>

    <!-- 位置信息 -->
    <n-card title="位置信息" size="small" class="detail-card">
      <div class="location-section">
        <MapComponent
          v-if="mapCenter && mapCenter.length === 2"
          ref="mapRef"
          :title="'告警位置'"
          :height="'350px'"
          :center="mapCenter"
          :zoom="15"
          :markers="mapMarkers"
          @marker-click="handleMarkerClick"
          @map-ready="handleMapReady"
        />
        <div v-else class="no-location">
          <n-empty description="暂无位置信息" />
        </div>
        <div class="location-info" v-if="locationInfo">
          <n-descriptions :column="2" label-placement="left" size="small">
            <n-descriptions-item label="经度">
              {{ locationInfo.lng?.toFixed(6) || '-' }}
            </n-descriptions-item>
            <n-descriptions-item label="纬度">
              {{ locationInfo.lat?.toFixed(6) || '-' }}
            </n-descriptions-item>
            <n-descriptions-item label="地址" :span="2">
              {{ locationInfo.address || '正在获取地址信息...' }}
            </n-descriptions-item>
          </n-descriptions>
        </div>
      </div>
    </n-card>

    <!-- 处理历史 -->
    <n-card title="处理历史" size="small" class="detail-card">
      <n-timeline>
        <n-timeline-item
          type="success"
          :title="`告警创建`"
          :time="formatDateTime(alert.created_at)"
          content="系统自动创建告警"
        />
        <n-timeline-item
          v-if="alert.resolved_at"
          type="info"
          :title="`告警${getStatusText(alert.status)}`"
          :time="formatDateTime(alert.resolved_at)"
          :content="`由 ${alert.resolved_by || '系统'} 处理`"
        />
      </n-timeline>
    </n-card>

    <!-- 操作区域 -->
    <div class="action-section" v-if="alert.status === 'active'">
      <n-space>
        <n-button type="success" @click="handleResolve">
          <template #icon>
            <n-icon>
              <Icon icon="mdi:check-circle" />
            </n-icon>
          </template>
          标记为已处理
        </n-button>
        <n-button type="warning" @click="handleIgnore">
          <template #icon>
            <n-icon>
              <Icon icon="mdi:eye-off" />
            </n-icon>
          </template>
          忽略告警
        </n-button>
        <n-button type="error" @click="handleDelete">
          <template #icon>
            <n-icon>
              <Icon icon="mdi:delete" />
            </n-icon>
          </template>
          删除告警
        </n-button>
      </n-space>
    </div>

    <!-- 处理备注模态框 -->
    <n-modal
      v-model:show="remarkModalVisible"
      preset="dialog"
      title="添加处理备注"
      positive-text="确认"
      negative-text="取消"
      @positive-click="confirmAction"
    >
      <n-form-item label="处理备注">
        <n-input
          v-model:value="remark"
          type="textarea"
          placeholder="请输入处理备注（可选）"
          :rows="4"
        />
      </n-form-item>
    </n-modal>

    <!-- 患者信息弹窗 -->
    <PatientInfoModal
      v-model:show="patientModalVisible"
      :patient-data="selectedPatientData"
      :alert-data="props.alert"
      @quick-action="handleQuickActionFromModal"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Icon } from '@iconify/vue'
import { useMessage } from 'naive-ui'
import api from '@/api'
import { format } from 'date-fns'
import { zhCN } from 'date-fns/locale'
import MapComponent from '@/components/map/MapComponent.vue'
import PatientInfoModal from '@/components/map/PatientInfoModal.vue'
import { generateMapMarkersFromAlert, getBeijingCenter } from '@/utils/map/mockData.js'

const props = defineProps({
  alert: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update', 'close'])

const message = useMessage()
const remarkModalVisible = ref(false)
const remark = ref('')
const currentAction = ref('')

// 地图相关数据
const mapRef = ref(null)
const locationInfo = ref(null)

// 患者信息弹窗相关数据
const patientModalVisible = ref(false)
const selectedPatientData = ref(null)

// 计算地图中心点和标注点
const mapCenter = computed(() => {
  // 如果告警数据中有位置信息，使用该位置作为中心点
  if (props.alert.location) {
    return props.alert.location
  }
  // 否则使用北京市中心
  return getBeijingCenter()
})

const mapMarkers = computed(() => {
  // 根据告警数据生成地图标注点
  return generateMapMarkersFromAlert(props.alert)
})

// 获取级别标签类型
const getLevelTagType = (level) => {
  const types = {
    critical: 'error',
    warning: 'warning',
    info: 'info'
  }
  return types[level] || 'default'
}

// 获取级别图标
const getLevelIcon = (level) => {
  const icons = {
    critical: 'mdi:alert-circle',
    warning: 'mdi:alert',
    info: 'mdi:information'
  }
  return icons[level] || 'mdi:bell'
}

// 获取级别文本
const getLevelText = (level) => {
  const texts = {
    critical: '紧急',
    warning: '警告',
    info: '信息'
  }
  return texts[level] || '未知'
}

// 获取状态标签类型
const getStatusTagType = (status) => {
  const types = {
    active: 'error',
    resolved: 'success',
    ignored: 'default'
  }
  return types[status] || 'default'
}

// 获取状态文本
const getStatusText = (status) => {
  const texts = {
    active: '未处理',
    resolved: '已处理',
    ignored: '已忽略'
  }
  return texts[status] || '未知'
}

// 格式化日期时间
const formatDateTime = (dateTime) => {
  if (!dateTime) return '-'
  return format(new Date(dateTime), 'yyyy-MM-dd HH:mm:ss', { locale: zhCN })
}

// 处理告警
const handleResolve = () => {
  currentAction.value = 'resolve'
  remarkModalVisible.value = true
}

// 忽略告警
const handleIgnore = () => {
  currentAction.value = 'ignore'
  remarkModalVisible.value = true
}

// 删除告警
const handleDelete = () => {
  currentAction.value = 'delete'
  remarkModalVisible.value = true
}

// 地图事件处理
const handleMapReady = (mapInstance) => {
  console.log('地图加载完成:', mapInstance)
  // 初始化位置信息
  updateLocationInfo()
}

const handleMarkerClick = (markerData, index, marker) => {
  console.log('标注点击:', markerData)

  // 显示患者信息弹窗
  if (markerData.patientData) {
    selectedPatientData.value = markerData.patientData
    patientModalVisible.value = true
  } else {
    message.info(`点击了位置标注`)
  }
}

// 更新位置信息
const updateLocationInfo = () => {
  const center = mapCenter.value
  if (center && center.length === 2) {
    locationInfo.value = {
      lng: center[0],
      lat: center[1],
      address: '正在获取地址信息...'
    }

    // 尝试从标注数据中获取患者地址
    const markers = mapMarkers.value
    if (markers.length > 0 && markers[0].patientData?.address) {
      locationInfo.value.address = markers[0].patientData.address
    } else {
      // 这里可以调用逆地理编码API获取详细地址
      // 暂时使用模拟地址
      setTimeout(() => {
        if (locationInfo.value) {
          locationInfo.value.address = '浙江省杭州市西湖区'
        }
      }, 1000)
    }
  }
}

// 确认操作
const confirmAction = async () => {
  try {
    const updateData = {
      resolved_at: new Date().toISOString(),
      resolved_by: 'current_user' // 这里应该是当前用户ID
    }

    if (remark.value) {
      updateData.remark = remark.value
    }

    if (currentAction.value === 'resolve') {
      updateData.status = 'resolved'
      await api.updateAlert(props.alert.id, updateData)
      message.success('告警已标记为已处理')
    } else if (currentAction.value === 'ignore') {
      updateData.status = 'ignored'
      await api.updateAlert(props.alert.id, updateData)
      message.success('告警已忽略')
    } else if (currentAction.value === 'delete') {
      await api.deleteAlert(props.alert.id)
      message.success('告警已删除')
    }

    remarkModalVisible.value = false
    remark.value = ''
    emit('update')
  } catch (error) {
    console.error('操作失败:', error)
    message.error('操作失败')
  }
}

// 从患者信息弹窗快速处理告警
const handleQuickActionFromModal = async (alertData) => {
  try {
    const updateData = {
      status: 'resolved',
      resolved_at: new Date().toISOString(),
      resolved_by: 'current_user',
      remark: '通过患者信息弹窗快速处理'
    }

    await api.updateAlert(alertData.id, updateData)
    message.success('告警已快速处理')
    emit('update')
  } catch (error) {
    console.error('快速处理失败:', error)
    message.error('快速处理失败')
  }
}

// 生命周期
onMounted(() => {
  updateLocationInfo()
})
</script>

<style scoped>
.alert-detail {
  padding: 16px;
}

.detail-card {
  margin-bottom: 16px;
}

.detail-card:last-of-type {
  margin-bottom: 0;
}

.alert-message {
  padding: 8px 12px;
  background: var(--n-color-hover);
  border-radius: 6px;
  border-left: 4px solid var(--n-color-primary);
  font-size: 14px;
  line-height: 1.5;
}

.location-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.location-info {
  padding: 12px;
  background: var(--n-color-hover);
  border-radius: 6px;
  border: 1px solid var(--n-border-color);
}

.no-location {
  padding: 40px;
  text-align: center;
}

.action-section {
  padding: 16px;
  border-top: 1px solid var(--n-border-color);
  background: var(--n-color-hover);
  border-radius: 0 0 6px 6px;
}

/* 深色模式适配 */
@media (prefers-color-scheme: dark) {
  .alert-message {
    background: var(--n-color-pressed);
  }

  .location-info {
    background: var(--n-color-pressed);
  }

  .action-section {
    background: var(--n-color-pressed);
  }
}
</style>
