<template>
  <AppPage :show-footer="false">
    <div class="digital-twin-container">
      <!-- 页面标题 -->
      <div class="page-header">
        <n-space align="center">
          <n-icon size="24" color="#18a058">
            <Icon icon="mdi:cube-outline" />
          </n-icon>
          <div>
            <h1 class="page-title">数字孪生监护系统</h1>
            <p class="page-subtitle">3D可视化老人健康监护界面</p>
          </div>
        </n-space>
      </div>

      <n-grid :cols="24" :x-gap="16" :y-gap="16">
        <!-- 上半部分：3D场景 + 场景控制 -->
        <n-grid-item :span="24">
          <n-grid :cols="3" :x-gap="16">
            <!-- 3D场景显示区域 (2/3宽度) -->
            <n-grid-item :span="2">
              <n-card title="居家环境数字孪生" :bordered="false" class="scene-card">
                <template #header-extra>
                  <n-button-group>
                    <n-button
                      :type="viewMode === '3d' ? 'primary' : 'default'"
                      @click="viewMode = '3d'"
                      size="small"
                    >
                      <template #icon>
                        <Icon icon="mdi:cube-outline" />
                      </template>
                      3D视图
                    </n-button>
                    <n-button
                      :type="viewMode === '2d' ? 'primary' : 'default'"
                      @click="viewMode = '2d'"
                      size="small"
                    >
                      <template #icon>
                        <Icon icon="mdi:floor-plan" />
                      </template>
                      平面图
                    </n-button>
                  </n-button-group>
                </template>

                <div class="scene-viewer">
                  <!-- 3D场景组件 -->
                  <Scene3D
                    :selected-elderly="selectedElderly"
                    :show-sensors="showSensors"
                    :show-trajectory="showTrajectory"
                    :view-mode="viewMode"
                  />
                </div>
              </n-card>
            </n-grid-item>

            <!-- 场景控制 (1/3宽度) -->
            <n-grid-item :span="1">
              <n-card title="场景控制" :bordered="false" class="control-card">
                <template #header-extra>
                  <n-icon>
                    <Icon icon="mdi:cog" />
                  </n-icon>
                </template>

                <n-space vertical :size="20">
                  <!-- 老人搜索 -->
                  <div>
                    <n-text strong class="control-label">搜索老人/房间</n-text>
                    <n-auto-complete
                      v-model:value="searchValue"
                      :options="searchOptions"
                      placeholder="输入老人姓名或房间号"
                      @select="onElderlySelect"
                      @update:value="onSearchUpdate"
                      :loading="elderlyLoading"
                      clearable
                      class="search-input"
                    >
                      <template #prefix>
                        <n-icon>
                          <Icon icon="mdi:magnify" />
                        </n-icon>
                      </template>
                    </n-auto-complete>
                  </div>

                  <!-- 可视化显示选项 -->
                  <div>
                    <n-text strong class="control-label">场景显示</n-text>
                    <n-space vertical :size="12" class="display-options">
                      <!-- 传感器显示 -->
                      <div class="display-option">
                        <div class="option-header" @click="toggleSensors">
                          <div class="option-icon sensors" :class="{ active: showSensors }">
                            <n-icon size="20">
                              <Icon icon="mdi:radar" />
                            </n-icon>
                          </div>
                          <div class="option-content">
                            <n-text strong>传感器</n-text>
                            <n-text :depth="2" class="option-desc">显示环境传感器位置</n-text>
                          </div>
                        </div>
                        <n-switch
                          v-model:value="showSensors"
                          @update:value="onSensorsChange"
                          @click.stop
                        />
                      </div>

                      <!-- 活动轨迹显示 -->
                      <div class="display-option">
                        <div class="option-header" @click="toggleTrajectory">
                          <div class="option-icon trajectory" :class="{ active: showTrajectory }">
                            <n-icon size="20">
                              <Icon icon="mdi:map-marker-path" />
                            </n-icon>
                          </div>
                          <div class="option-content">
                            <n-text strong>活动轨迹</n-text>
                            <n-text :depth="2" class="option-desc">显示老人行动路径</n-text>
                          </div>
                        </div>
                        <n-switch
                          v-model:value="showTrajectory"
                          @update:value="onTrajectoryChange"
                          @click.stop
                        />
                      </div>
                    </n-space>
                  </div>
                </n-space>
              </n-card>
            </n-grid-item>
          </n-grid>
        </n-grid-item>

        <!-- 下半部分：监护信息面板 -->
        <n-grid-item :span="24">
          <n-grid :cols="3" :x-gap="16">
            <!-- 实时状态 -->
            <n-grid-item>
              <n-card title="实时状态" :bordered="false" class="info-card">
                <template #header-extra>
                  <n-icon>
                    <Icon icon="mdi:heart-pulse" />
                  </n-icon>
                </template>

                <n-space vertical :size="12">
                  <div class="status-item">
                    <n-space align="center" justify="space-between">
                      <n-space align="center">
                        <n-icon size="18" color="#18a058">
                          <Icon icon="mdi:heart-pulse" />
                        </n-icon>
                        <n-text strong>心率</n-text>
                      </n-space>
                      <n-text class="status-value">{{ elderlyStatus.heartRate || '--' }} BPM</n-text>
                    </n-space>
                  </div>

                  <div class="status-item">
                    <n-space align="center" justify="space-between">
                      <n-space align="center">
                        <n-icon size="18" color="#2080f0">
                          <Icon icon="mdi:lungs" />
                        </n-icon>
                        <n-text strong>呼吸</n-text>
                      </n-space>
                      <n-text class="status-value">{{ elderlyStatus.breathingRate || '--' }} 次/分</n-text>
                    </n-space>
                  </div>

                  <div class="status-item">
                    <n-space align="center" justify="space-between">
                      <n-space align="center">
                        <n-icon size="18" color="#f0a020">
                          <Icon icon="mdi:walk" />
                        </n-icon>
                        <n-text strong>活动</n-text>
                      </n-space>
                      <n-text class="status-value">{{ elderlyStatus.activityStatus || '--' }}</n-text>
                    </n-space>
                  </div>

                  <div class="status-item">
                    <n-space align="center" justify="space-between">
                      <n-space align="center">
                        <n-icon size="18" color="#d03050">
                          <Icon icon="mdi:map-marker" />
                        </n-icon>
                        <n-text strong>位置</n-text>
                      </n-space>
                      <n-text class="status-value">{{ elderlyStatus.currentLocation || '--' }}</n-text>
                    </n-space>
                  </div>
                </n-space>
              </n-card>
            </n-grid-item>

            <!-- 环境监测 -->
            <n-grid-item>
              <EnvironmentMonitor />
            </n-grid-item>

            <!-- 24小时趋势 -->
            <n-grid-item>
              <TrendChart :elderly-id="selectedElderly" />
            </n-grid-item>
          </n-grid>
        </n-grid-item>


      </n-grid>
    </div>
  </AppPage>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Icon } from '@iconify/vue'
import api from '@/api'
import AppPage from '@/components/page/AppPage.vue'
import Scene3D from './components/Scene3D.vue'
import EnvironmentMonitor from './components/EnvironmentMonitor.vue'
import TrendChart from './components/TrendChart.vue'

// 响应式数据
const viewMode = ref('3d')
const selectedElderly = ref(null)
const showSensors = ref(true)
const showTrajectory = ref(true)
const elderlyLoading = ref(false)
const searchValue = ref('')

// 数据
const elderlyList = ref([])
const searchOptions = ref([])
const elderlyStatus = ref({
  heartRate: null,
  breathingRate: null,
  activityStatus: null,
  currentLocation: null
})

// 方法
const fetchElderlyList = async () => {
  try {
    elderlyLoading.value = true
    const response = await api.getElderlyList()
    elderlyList.value = response.data.map(item => ({
      id: item.id,
      name: item.name,
      room: item.room || '客厅',
      roomNumber: item.roomNumber || `${item.id}01`
    }))

    // 默认选择第一个老人
    if (elderlyList.value.length > 0) {
      selectedElderly.value = elderlyList.value[0].id
      searchValue.value = elderlyList.value[0].name
    }
  } catch (error) {
    console.error('获取老人列表失败:', error)
    // 使用模拟数据
    elderlyList.value = [
      { id: 1, name: '张奶奶', room: '客厅', roomNumber: '101' },
      { id: 2, name: '王爷爷', room: '卧室', roomNumber: '102' },
      { id: 3, name: '吴大爷', room: '厨房', roomNumber: '103' },
      { id: 4, name: '李阿姨', room: '阳台', roomNumber: '104' },
      { id: 5, name: '陈大爷', room: '客厅', roomNumber: '105' }
    ]
    selectedElderly.value = 1
    searchValue.value = '张奶奶'
  } finally {
    elderlyLoading.value = false
  }
}

const fetchElderlyStatus = async (elderlyId) => {
  if (!elderlyId) return

  try {
    const response = await api.getElderlyStatus(elderlyId)
    elderlyStatus.value = response.data
  } catch (error) {
    console.error('获取老人状态失败:', error)
    // 使用模拟数据
    const elderly = elderlyList.value.find(e => e.id === elderlyId)
    elderlyStatus.value = {
      heartRate: 68 + Math.floor(Math.random() * 20),
      breathingRate: 14 + Math.floor(Math.random() * 6),
      activityStatus: ['静坐休息', '轻度活动', '深度睡眠', '正常行走'][Math.floor(Math.random() * 4)],
      currentLocation: elderly ? `${elderly.room}` : '客厅'
    }
  }
}

// 搜索相关方法
const onSearchUpdate = (value) => {
  searchValue.value = value
  updateSearchOptions(value)
}

const updateSearchOptions = (query) => {
  if (!query) {
    searchOptions.value = []
    return
  }

  const filtered = elderlyList.value.filter(elderly =>
    elderly.name.toLowerCase().includes(query.toLowerCase()) ||
    elderly.room.toLowerCase().includes(query.toLowerCase()) ||
    elderly.roomNumber.includes(query)
  )

  searchOptions.value = filtered.map(elderly => ({
    label: `${elderly.name} - ${elderly.room} (${elderly.roomNumber})`,
    value: elderly.id,
    elderly: elderly
  }))
}

const onElderlySelect = (value) => {
  const option = searchOptions.value.find(opt => opt.value === value)
  if (option) {
    selectedElderly.value = value
    searchValue.value = option.elderly.name
    fetchElderlyStatus(value)
    updateScene()
  }
}

// 显示选项切换方法
const toggleSensors = () => {
  showSensors.value = !showSensors.value
  console.log('点击切换传感器显示:', showSensors.value)
  updateSceneDisplay()
}

const toggleTrajectory = () => {
  showTrajectory.value = !showTrajectory.value
  console.log('点击切换活动轨迹显示:', showTrajectory.value)
  updateSceneDisplay()
}

// 开关变化处理方法
const onSensorsChange = (value) => {
  showSensors.value = value
  updateSceneDisplay()
  console.log('传感器显示状态:', value)
}

const onTrajectoryChange = (value) => {
  showTrajectory.value = value
  updateSceneDisplay()
  console.log('活动轨迹显示状态:', value)
}

const updateSceneDisplay = () => {
  updateScene()
}

const updateScene = () => {
  // 这里可以更新3D场景
  console.log('更新3D场景:', {
    elderly: selectedElderly.value,
    showSensors: showSensors.value,
    showTrajectory: showTrajectory.value
  })
}

// 监听选中的老人变化
watch(selectedElderly, (newValue) => {
  if (newValue) {
    fetchElderlyStatus(newValue)
  }
})

// 生命周期
onMounted(async () => {
  await fetchElderlyList()
})
</script>

<style scoped>
.digital-twin-container {
  padding: 16px;
}

.page-header {
  margin-bottom: 24px;
  padding: 24px 0;
  text-align: center;
}

.page-title {
  margin: 0;
  font-size: 28px;
  font-weight: 600;
  color: #333;
}

.page-subtitle {
  margin: 8px 0 0 0;
  font-size: 14px;
  color: #666;
}

.scene-card {
  height: 500px;
}

.control-card {
  height: 500px;
}

.scene-viewer {
  height: 420px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  position: relative;
  overflow: hidden;
}

.info-card {
  height: 350px;
}

.status-item {
  padding: 12px 16px;
  background: #fafafa;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.status-item:hover {
  background: #f0f0f0;
  transform: translateY(-1px);
}

.status-value {
  font-weight: 600;
  font-size: 16px;
}

/* 控制面板样式 */
.control-label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
}

.search-input {
  margin-top: 8px;
}

.display-options {
  margin-top: 8px;
}

/* 显示选项样式 */
.display-option {
  padding: 12px;
  background: #fafafa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e0e0e0;
}

.display-option:hover {
  background: #f0f0f0;
  border-color: #d0d0d0;
}

.option-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
  cursor: pointer;
  flex: 1;
}

.option-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: #e8e8e8;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

/* 传感器图标 - 蓝色 */
.option-icon.sensors {
  background: #3b82f6;
  color: white;
}

.option-icon.sensors:not(.active) {
  background: #e8e8e8;
  color: #666;
}

/* 活动轨迹图标 - 绿色 */
.option-icon.trajectory {
  background: #10b981;
  color: white;
}

.option-icon.trajectory:not(.active) {
  background: #e8e8e8;
  color: #666;
}

.option-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.option-desc {
  font-size: 11px;
  line-height: 1.3;
  color: #666;
}

.mt-2 {
  margin-top: 8px;
}
</style>
