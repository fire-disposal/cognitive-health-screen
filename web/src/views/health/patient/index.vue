<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  NCard, NSpace, NForm, NFormItem, NInput, NButton, NSelect,
  NStatistic, NGrid, NGridItem, NTag, NPagination, NIcon
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import api from '@/api'

const router = useRouter()

// 搜索和筛选
const search = ref('')
const communityFilter = ref('全部')
const riskFilter = ref('全部')
const locationFilter = ref('全部')

// 分页
const page = ref(1)
const pageSize = ref(12)

// 统计数据
const statistics = ref({
  total: 24,
  active: 18,
  warning: 7,
  alert: 2
})

// 筛选选项
const communityOptions = [
  { label: '全部', value: '全部' },
  { label: '阳光养老院', value: '阳光养老院' },
  { label: '和谐社区', value: '和谐社区' },
  { label: '康乐老年公寓', value: '康乐老年公寓' },
  { label: '幸福家园', value: '幸福家园' }
]

const riskLevels = [
  { label: '全部', value: '全部' },
  { label: '低风险', value: '低风险' },
  { label: '中等风险', value: '中等风险' },
  { label: '高风险', value: '高风险' }
]

const locationOptions = [
  { label: '全部', value: '全部' },
  { label: '1号楼', value: '1号楼' },
  { label: '2号楼', value: '2号楼' },
  { label: '3号楼', value: '3号楼' }
]

// 模拟病人数据
const patientsData = ref([
  {
    id: 1,
    name: '张爷爷',
    age: 78,
    location: '1号楼101',
    status: '看电视',
    riskScore: 3,
    riskLevel: { label: '低风险', color: '#52c41a', class: 'risk-low' },
    positionRisk: 1.2,
    environmentRisk: 1.0,
    physiologicalRisk: 0.8,
    community: '阳光养老院'
  },
  {
    id: 2,
    name: '李奶奶',
    age: 82,
    location: '1号楼102',
    status: '休息',
    riskScore: 7,
    riskLevel: { label: '中等风险', color: '#faad14', class: 'risk-medium' },
    positionRisk: 2.4,
    environmentRisk: 2.8,
    physiologicalRisk: 1.8,
    community: '阳光养老院'
  },
  {
    id: 3,
    name: '王大爷',
    age: 85,
    location: '1号楼103',
    status: '睡觉',
    riskScore: 4,
    riskLevel: { label: '低风险', color: '#52c41a', class: 'risk-low' },
    positionRisk: 1.5,
    environmentRisk: 1.2,
    physiologicalRisk: 1.3,
    community: '阳光养老院'
  },
  {
    id: 4,
    name: '赵婆婆',
    age: 76,
    location: '1号楼204',
    status: '发呆',
    riskScore: 8,
    riskLevel: { label: '中等风险', color: '#faad14', class: 'risk-medium' },
    positionRisk: 2.8,
    environmentRisk: 2.6,
    physiologicalRisk: 2.6,
    community: '阳光养老院'
  },
  {
    id: 5,
    name: '钱阿姨',
    age: 73,
    location: '1号楼205',
    status: '活动',
    riskScore: 2,
    riskLevel: { label: '低风险', color: '#52c41a', class: 'risk-low' },
    positionRisk: 0.8,
    environmentRisk: 0.7,
    physiologicalRisk: 0.5,
    community: '阳光养老院'
  },
  {
    id: 6,
    name: '孙叔叔',
    age: 80,
    location: '1号楼306',
    status: '看书',
    riskScore: 12,
    riskLevel: { label: '高风险', color: '#ff4d4f', class: 'risk-high' },
    positionRisk: 3.8,
    environmentRisk: 4.2,
    physiologicalRisk: 4.0,
    community: '阳光养老院'
  }
])

// 过滤后的病人数据
const filteredPatients = computed(() => {
  let result = patientsData.value

  // 搜索过滤
  if (search.value) {
    const searchLower = search.value.toLowerCase()
    result = result.filter(patient =>
      patient.name.toLowerCase().includes(searchLower) ||
      patient.location.toLowerCase().includes(searchLower)
    )
  }

  // 风险等级过滤
  if (riskFilter.value !== '全部') {
    result = result.filter(patient => patient.riskLevel.label === riskFilter.value)
  }

  // 位置过滤
  if (locationFilter.value !== '全部') {
    result = result.filter(patient => patient.location.includes(locationFilter.value))
  }

  // 社区/养老院过滤
  if (communityFilter.value !== '全部') {
    result = result.filter(patient => patient.community === communityFilter.value)
  }

  return result
})

// 分页后的数据
const paginatedPatients = computed(() => {
  const startIndex = (page.value - 1) * pageSize.value
  return filteredPatients.value.slice(startIndex, startIndex + pageSize.value)
})

// 总页数
const totalPages = computed(() => {
  return Math.ceil(filteredPatients.value.length / pageSize.value)
})

// 跳转到详情页
function goToDetail(patient) {
  router.push({ path: `/health/patient/detail/${patient.id}` })
}

// 获取状态图标
function getStatusIcon(status) {
  const iconMap = {
    '看电视': 'mdi:television',
    '休息': 'mdi:sofa',
    '睡觉': 'mdi:sleep',
    '发呆': 'mdi:head-question',
    '活动': 'mdi:walk',
    '看书': 'mdi:book-open-page-variant',
    '吃饭': 'mdi:food-fork-drink',
    '静止不动': 'mdi:timer-sand'
  }
  return iconMap[status] || 'mdi:account'
}

// 获取状态图标颜色
function getStatusIconColor(status) {
  const colorMap = {
    '看电视': '#1890ff',
    '休息': '#52c41a',
    '睡觉': '#52c41a',
    '发呆': '#faad14',
    '活动': '#1890ff',
    '看书': '#1890ff',
    '吃饭': '#52c41a',
    '静止不动': '#ff4d4f'
  }
  return colorMap[status] || '#666'
}

// 获取风险文字颜色类
function getRiskTextClass(score) {
  if (score <= 1.5) return 'text-green-600'
  if (score <= 3.0) return 'text-yellow-600'
  return 'text-red-600'
}

onMounted(() => {
  // 初始化数据
})
</script>

<template>
  <div class="patient-overview">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="subtitle-container">
        <div class="subtitle-badge">
          <TheIcon icon="mdi:monitor-eye" size="16" />
          实时监测
        </div>
        <div class="subtitle-badge">
          <TheIcon icon="mdi:shield-check" size="16" />
          预防风险
        </div>
        <div class="subtitle-badge">
          <TheIcon icon="mdi:heart-pulse" size="16" />
          健康呵护
        </div>
        <div class="subtitle-badge">
          <TheIcon icon="mdi:human-greeting-variant" size="16" />
          智能陪伴
        </div>
      </div>
    </div>

    <!-- 统计卡片 -->
    <NGrid :cols="4" :x-gap="16" :collapsed-rows="1" responsive="screen" class="mb-4">
      <NGridItem>
        <NCard class="status-card status-card-blue">
          <div class="status-card-content">
            <div class="status-icon">
              <TheIcon icon="mdi:account-group" size="32" color="white" />
            </div>
            <div class="status-info">
              <div class="status-number">{{ statistics.total }}</div>
              <div class="status-label">监护老人总数</div>
            </div>
          </div>
        </NCard>
      </NGridItem>
      <NGridItem>
        <NCard class="status-card status-card-light-blue">
          <div class="status-card-content">
            <div class="status-icon">
              <TheIcon icon="mdi:walk" size="32" color="white" />
            </div>
            <div class="status-info">
              <div class="status-number">{{ statistics.active }}</div>
              <div class="status-label">当前活动人数</div>
            </div>
          </div>
        </NCard>
      </NGridItem>
      <NGridItem>
        <NCard class="status-card status-card-orange">
          <div class="status-card-content">
            <div class="status-icon">
              <TheIcon icon="mdi:alert-circle-outline" size="32" color="white" />
            </div>
            <div class="status-info">
              <div class="status-number">{{ statistics.warning }}</div>
              <div class="status-label">中高风险人数</div>
            </div>
          </div>
        </NCard>
      </NGridItem>
      <NGridItem>
        <NCard class="status-card status-card-red">
          <div class="status-card-content">
            <div class="status-icon">
              <TheIcon icon="mdi:alarm-light-outline" size="32" color="white" />
            </div>
            <div class="status-info">
              <div class="status-number">{{ statistics.alert }}</div>
              <div class="status-label">紧急预警人数</div>
            </div>
          </div>
        </NCard>
      </NGridItem>
    </NGrid>
    <!-- 搜索和筛选 -->
    <NCard class="search-card mb-4">
      <NForm inline>
        <NFormItem>
          <NInput
            v-model:value="search"
            placeholder="搜索老人姓名、房间号或编号"
            clearable
            style="width: 300px;"
          >
            <template #prefix>
              <TheIcon icon="mdi:magnify" />
            </template>
          </NInput>
        </NFormItem>
        <NFormItem label="养老院/社区">
          <NSelect
            v-model:value="communityFilter"
            :options="communityOptions"
            placeholder="全部"
            style="width: 150px;"
          />
        </NFormItem>
        <NFormItem label="风险等级">
          <NSelect
            v-model:value="riskFilter"
            :options="riskLevels"
            placeholder="全部"
            style="width: 120px;"
          />
        </NFormItem>
        <NFormItem label="位置">
          <NSelect
            v-model:value="locationFilter"
            :options="locationOptions"
            placeholder="全部"
            style="width: 120px;"
          />
        </NFormItem>
        <NFormItem>
          <NButton type="primary" circle>
            <template #icon>
              <TheIcon icon="mdi:filter-variant" />
            </template>
          </NButton>
        </NFormItem>
      </NForm>
    </NCard>
    <!-- 病人卡片网格 -->
    <NGrid
      :cols="6"
      :x-gap="16"
      :y-gap="16"
      responsive="screen"
      :collapsed-rows="2"
      class="mb-4"
    >
      <NGridItem v-for="patient in paginatedPatients" :key="patient.id">
        <NCard
          class="patient-card"
          :class="patient.riskLevel.class"
          hoverable
          @click="goToDetail(patient)"
        >
          <!-- 风险等级标签 -->
          <div
            class="risk-badge"
            :style="{ backgroundColor: patient.riskLevel.color }"
          >
            {{ patient.riskLevel.label }}
          </div>

          <!-- 病人信息 -->
          <div class="patient-info">
            <div class="patient-name">
              {{ patient.name }}
              <span class="patient-age">({{ patient.age }}岁)</span>
            </div>

            <div class="patient-status">
              <TheIcon
                :icon="getStatusIcon(patient.status)"
                :color="getStatusIconColor(patient.status)"
                size="16"
              />
              <span>{{ patient.status }}</span>
            </div>

            <div class="patient-location">
              <TheIcon icon="mdi:map-marker" size="14" color="#999" />
              <span>{{ patient.location }}</span>
            </div>

            <!-- 风险指标 -->
            <div class="risk-metrics">
              <div class="risk-item">
                <span class="risk-label">体位风险值</span>
                <span class="risk-value" :class="getRiskTextClass(patient.positionRisk)">
                  {{ patient.positionRisk }}
                </span>
              </div>
              <div class="risk-item">
                <span class="risk-label">环境因素</span>
                <span class="risk-value" :class="getRiskTextClass(patient.environmentRisk)">
                  {{ patient.environmentRisk }}
                </span>
              </div>
              <div class="risk-item">
                <span class="risk-label">生理指标</span>
                <span class="risk-value" :class="getRiskTextClass(patient.physiologicalRisk)">
                  {{ patient.physiologicalRisk }}
                </span>
              </div>
            </div>

            <!-- 查看详情按钮 -->
            <NButton
              type="primary"
              size="small"
              block
              class="detail-btn"
              @click.stop="goToDetail(patient)"
            >
              <template #icon>
                <TheIcon icon="mdi:eye" />
              </template>
              查看详情
            </NButton>
          </div>
        </NCard>
      </NGridItem>
    </NGrid>

    <!-- 分页 -->
    <div class="pagination-container">
      <NPagination
        v-model:page="page"
        :page-count="totalPages"
        :page-size="pageSize"
        show-size-picker
        :page-sizes="[6, 12, 18, 24]"
        @update:page-size="(size) => pageSize = size"
      />
    </div>
  </div>
</template>

<style scoped>
.patient-overview {
  padding: 16px;
  height: 100vh;
  overflow-y: auto;
}

.page-header {
  background: linear-gradient(to right, rgba(22, 75, 135, 0.1), rgba(58, 132, 195, 0.05));
  padding: 16px;
  border-radius: 8px;
  border-left: 4px solid #164B87;
  margin-bottom: 16px;
}

.subtitle-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.subtitle-badge {
  background-color: rgba(22, 75, 135, 0.1);
  color: #164B87;
  border-radius: 20px;
  padding: 4px 12px;
  font-size: 12px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: all 0.3s;
}

.subtitle-badge:hover {
  background-color: rgba(22, 75, 135, 0.2);
  transform: translateY(-2px);
}

/* 状态卡片样式 */
.status-card {
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.status-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.status-card-blue {
  background: #164B87;
  color: white;
}

.status-card-light-blue {
  background: #3A84C3;
  color: white;
}

.status-card-orange {
  background: #FAAD14;
  color: white;
}

.status-card-red {
  background: #FF4D4F;
  color: white;
}

.status-card-content {
  display: flex;
  align-items: center;
  padding: 16px;
}

.status-icon {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.status-info {
  flex: 1;
}

.status-number {
  font-size: 24px;
  font-weight: bold;
  line-height: 1;
  margin-bottom: 4px;
}

.status-label {
  font-size: 12px;
  opacity: 0.9;
}

/* 搜索卡片样式 */
.search-card {
  background-color: #fafafa;
  border-radius: 8px;
}

/* 病人卡片样式 */
.patient-card {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  border-left: 4px solid transparent;
}

.patient-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

.patient-card.risk-low {
  border-left-color: #52c41a;
}

.patient-card.risk-medium {
  border-left-color: #faad14;
}

.patient-card.risk-high {
  border-left-color: #ff4d4f;
}

.risk-badge {
  position: absolute;
  top: 0;
  right: 0;
  color: white;
  font-size: 10px;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 0 8px 0 8px;
  z-index: 1;
}

.patient-info {
  padding: 12px;
}

.patient-name {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #333;
}

.patient-age {
  font-size: 12px;
  font-weight: normal;
  color: #666;
  margin-left: 4px;
}

.patient-status {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #666;
  margin-bottom: 6px;
}

.patient-location {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #999;
  margin-bottom: 12px;
}

.risk-metrics {
  background-color: #f8f9fa;
  padding: 8px;
  border-radius: 6px;
  margin-bottom: 12px;
}

.risk-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 11px;
  margin-bottom: 4px;
}

.risk-item:last-child {
  margin-bottom: 0;
}

.risk-label {
  color: #666;
}

.risk-value {
  font-weight: 600;
}

.detail-btn {
  font-size: 12px;
}

/* 分页容器 */
.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

/* 工具类 */
.mb-4 {
  margin-bottom: 16px;
}

.text-green-600 {
  color: #52c41a;
}

.text-yellow-600 {
  color: #faad14;
}

.text-red-600 {
  color: #ff4d4f;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .patient-card {
    font-size: 12px;
  }

  .status-number {
    font-size: 20px;
  }

  .status-label {
    font-size: 11px;
  }
}

@media (max-width: 768px) {
  .patient-overview {
    padding: 8px;
  }

  .page-header {
    padding: 12px;
    margin-bottom: 12px;
  }

  .subtitle-container {
    flex-direction: column;
    gap: 4px;
  }

  .status-card-content {
    padding: 12px;
  }

  .status-icon {
    width: 36px;
    height: 36px;
    margin-right: 12px;
  }

  .status-number {
    font-size: 18px;
  }

  .status-label {
    font-size: 10px;
  }

  .patient-card {
    font-size: 11px;
  }

  .patient-name {
    font-size: 13px;
  }

  .risk-metrics {
    padding: 6px;
  }

  .risk-item {
    font-size: 10px;
  }
}

@media (max-width: 480px) {
  .search-card .n-form {
    flex-direction: column;
  }

  .search-card .n-form-item {
    margin-bottom: 8px;
  }

  .pagination-container {
    margin-top: 16px;
  }
}
</style>