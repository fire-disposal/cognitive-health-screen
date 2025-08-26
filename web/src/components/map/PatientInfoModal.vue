<template>
  <n-modal
    v-model:show="visible"
    preset="card"
    :title="modalTitle"
    size="medium"
    :bordered="false"
    :segmented="true"
    style="width: 500px"
  >
    <div class="patient-info-content" v-if="patientData">
      <!-- 患者基本信息 -->
      <div class="info-section">
        <h4 class="section-title">
          <n-icon class="section-icon">
            <Icon icon="mdi:account" />
          </n-icon>
          基本信息
        </h4>
        <n-descriptions :column="2" label-placement="left" size="small">
          <n-descriptions-item label="姓名">
            <n-tag type="info" size="small">{{ patientData.name }}</n-tag>
          </n-descriptions-item>
          <n-descriptions-item label="年龄">
            {{ patientData.age }}岁
          </n-descriptions-item>
          <n-descriptions-item label="性别">
            {{ patientData.gender }}
          </n-descriptions-item>
          <n-descriptions-item label="风险等级">
            <n-tag 
              :type="getRiskLevelType(patientData.riskLevel)" 
              size="small"
            >
              {{ getRiskLevelText(patientData.riskLevel) }}
            </n-tag>
          </n-descriptions-item>
        </n-descriptions>
      </div>

      <!-- 联系信息 -->
      <div class="info-section">
        <h4 class="section-title">
          <n-icon class="section-icon">
            <Icon icon="mdi:phone" />
          </n-icon>
          联系信息
        </h4>
        <n-descriptions :column="1" label-placement="left" size="small">
          <n-descriptions-item label="联系电话">
            <n-button text type="primary" @click="callPatient">
              <template #icon>
                <n-icon>
                  <Icon icon="mdi:phone" />
                </n-icon>
              </template>
              {{ patientData.phone }}
            </n-button>
          </n-descriptions-item>
          <n-descriptions-item label="紧急联系人">
            {{ patientData.emergencyContact }}
          </n-descriptions-item>
          <n-descriptions-item label="紧急联系电话">
            <n-button text type="error" @click="callEmergencyContact">
              <template #icon>
                <n-icon>
                  <Icon icon="mdi:phone-alert" />
                </n-icon>
              </template>
              {{ patientData.emergencyPhone }}
            </n-button>
          </n-descriptions-item>
          <n-descriptions-item label="居住地址" v-if="patientData.address">
            <n-text>{{ patientData.address }}</n-text>
          </n-descriptions-item>
        </n-descriptions>
      </div>

      <!-- 医疗信息 -->
      <div class="info-section" v-if="patientData.medicalHistory?.length || patientData.currentMedication?.length">
        <h4 class="section-title">
          <n-icon class="section-icon">
            <Icon icon="mdi:medical-bag" />
          </n-icon>
          医疗信息
        </h4>
        <n-descriptions :column="1" label-placement="left" size="small">
          <n-descriptions-item label="病史" v-if="patientData.medicalHistory?.length">
            <n-space size="small">
              <n-tag 
                v-for="history in patientData.medicalHistory" 
                :key="history"
                type="warning"
                size="small"
              >
                {{ history }}
              </n-tag>
            </n-space>
          </n-descriptions-item>
          <n-descriptions-item label="当前用药" v-if="patientData.currentMedication?.length">
            <n-space size="small">
              <n-tag 
                v-for="medication in patientData.currentMedication" 
                :key="medication"
                type="info"
                size="small"
              >
                {{ medication }}
              </n-tag>
            </n-space>
          </n-descriptions-item>
        </n-descriptions>
      </div>

      <!-- 告警信息 -->
      <div class="info-section" v-if="alertData">
        <h4 class="section-title">
          <n-icon class="section-icon">
            <Icon icon="mdi:alert" />
          </n-icon>
          当前告警
        </h4>
        <div class="alert-info">
          <div class="alert-level">
            <n-tag :type="getAlertLevelType(alertData.level)" size="medium">
              {{ getAlertLevelText(alertData.level) }}
            </n-tag>
          </div>
          <div class="alert-message">
            {{ alertData.message }}
          </div>
          <div class="alert-time">
            告警时间：{{ formatDateTime(alertData.created_at) }}
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <n-space justify="end">
        <n-button @click="visible = false">关闭</n-button>
        <n-button type="primary" @click="handleQuickAction" v-if="alertData && alertData.status === 'active'">
          <template #icon>
            <n-icon>
              <Icon icon="mdi:check-circle" />
            </n-icon>
          </template>
          快速处理
        </n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<!--
  患者信息弹窗组件 - PatientInfoModal.vue

  用于显示患者详细信息的模态框组件

  主要功能：
  - 患者基本信息展示（姓名、年龄、性别、风险等级）
  - 联系信息展示（电话、紧急联系人）
  - 医疗信息展示（病史、当前用药）
  - 当前告警信息展示
  - 快速处理告警功能
  - 一键拨号功能（模拟）

  作者：数字孪生系统开发团队
  创建时间：2024-01-01
  最后更新：2024-01-01
-->

<script setup>
import { ref, computed } from 'vue'
import { Icon } from '@iconify/vue'
import { useMessage } from 'naive-ui'
import { format } from 'date-fns'
import { zhCN } from 'date-fns/locale'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  patientData: {
    type: Object,
    default: null
  },
  alertData: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:show', 'quick-action'])

const message = useMessage()

const visible = computed({
  get: () => props.show,
  set: (value) => emit('update:show', value)
})

const modalTitle = computed(() => {
  if (props.patientData) {
    return `${props.patientData.name} - 详细信息`
  }
  return '患者信息'
})

// 获取风险等级类型
const getRiskLevelType = (level) => {
  const types = {
    'high': 'error',
    'medium': 'warning',
    'low': 'success'
  }
  return types[level] || 'default'
}

// 获取风险等级文本
const getRiskLevelText = (level) => {
  const texts = {
    'high': '高风险',
    'medium': '中风险',
    'low': '低风险'
  }
  return texts[level] || '未知'
}

// 获取告警级别类型
const getAlertLevelType = (level) => {
  const types = {
    'critical': 'error',
    'warning': 'warning',
    'info': 'info'
  }
  return types[level] || 'default'
}

// 获取告警级别文本
const getAlertLevelText = (level) => {
  const texts = {
    'critical': '紧急',
    'warning': '警告',
    'info': '信息'
  }
  return texts[level] || '未知'
}

// 格式化日期时间
const formatDateTime = (dateTime) => {
  if (!dateTime) return '-'
  return format(new Date(dateTime), 'yyyy-MM-dd HH:mm:ss', { locale: zhCN })
}

// 拨打患者电话
const callPatient = () => {
  message.info(`正在拨打 ${props.patientData.name} 的电话: ${props.patientData.phone}`)
  // 这里可以集成实际的拨号功能
}

// 拨打紧急联系人电话
const callEmergencyContact = () => {
  message.warning(`正在拨打紧急联系人电话: ${props.patientData.emergencyPhone}`)
  // 这里可以集成实际的拨号功能
}

// 快速处理告警
const handleQuickAction = () => {
  emit('quick-action', props.alertData)
  visible.value = false
}
</script>

<style scoped>
.patient-info-content {
  max-height: 60vh;
  overflow-y: auto;
}

.info-section {
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--n-border-color);
}

.info-section:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.section-title {
  display: flex;
  align-items: center;
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 600;
  color: var(--n-text-color);
}

.section-icon {
  margin-right: 8px;
  color: var(--n-color-primary);
}

.alert-info {
  padding: 12px;
  background: var(--n-color-hover);
  border-radius: 6px;
  border-left: 4px solid var(--n-color-primary);
}

.alert-level {
  margin-bottom: 8px;
}

.alert-message {
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 8px;
  color: var(--n-text-color);
}

.alert-time {
  font-size: 12px;
  color: var(--n-text-color-disabled);
}

/* 深色模式适配 */
@media (prefers-color-scheme: dark) {
  .alert-info {
    background: var(--n-color-pressed);
  }
}
</style>
