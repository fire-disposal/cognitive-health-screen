<template>
  <AppPage :show-footer="false">
    <div class="workbench-container">
      <!-- 主要内容区域 -->
      <div class="main-content">
        <n-grid :cols="24" :x-gap="16" :y-gap="16">
          <!-- 左侧区域 -->
          <n-grid-item :span="16">
            <n-grid :cols="1" :y-gap="16">
              <!-- 告警面板 -->
              <n-grid-item>
                <AlertPanel />
              </n-grid-item>

              <!-- 数据统计 -->
              <n-grid-item>
                <DataStatistics />
              </n-grid-item>
            </n-grid>
          </n-grid-item>

          <!-- 右侧区域 -->
          <n-grid-item :span="8">
            <DataStatistics />
          </n-grid-item>
        </n-grid>
      </div>
    </div>
  </AppPage>
</template>



<script setup>
import { onMounted } from 'vue'
import { useHealthStore } from '@/store/modules/health'
import AlertPanel from '@/components/alert/AlertPanel.vue'
import DataStatistics from '@/components/statistics/DataStatistics.vue'

const healthStore = useHealthStore()

// 生命周期
onMounted(() => {
  // 初始化健康数据
  healthStore.fetchDeviceSummaries()
})
</script>

<style scoped>
.workbench-container {
  padding: 16px;
  min-height: 100vh;
  background: var(--n-color-hover);
}

/* 主要内容区域 */
.main-content {
  flex: 1;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .workbench-container {
    padding: 8px;
  }
}

/* 深色模式适配 */
@media (prefers-color-scheme: dark) {
  .workbench-container {
    background: var(--n-color-base);
  }
}
</style>
