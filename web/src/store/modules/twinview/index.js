import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { SCENE_CONFIG, CHART_CONFIG } from '~/src/views/twinview/model-data'
import api from '@/api' // 引入 api

export const useTwinviewStore = defineStore('twinview', () => {
  // 状态
  const selectedId = ref(null)
  const modelData = ref(new Map())
  const isInitialized = ref(false)
  // 已删除：let sseConnection = null // 用于存储 SSE 连接实例

  // Getters
  const selectedData = computed(() => {
    return selectedId.value ? modelData.value.get(selectedId.value) : null
  })

  const selectedConfig = computed(() => {
    if (!selectedId.value) return null
    const sceneObject = SCENE_CONFIG.find(obj => obj.id === selectedId.value)
    return sceneObject?.monitoring || null
  })

  const selectedObject = computed(() => {
    if (!selectedId.value) return null
    return SCENE_CONFIG.find(obj => obj.id === selectedId.value) || null
  })

  // Actions
  function init() {
    if (isInitialized.value) {
      console.warn('[TwinviewStore] already initialized.')
      return
    }
    
    isInitialized.value = true
    console.log('[TwinviewStore] initialized.')
    
    // 初始化每个场景对象的数据结构
    SCENE_CONFIG.forEach(obj => {
      if (!modelData.value.has(obj.id)) {
        modelData.value.set(obj.id, {})
      }
    })

    // 已删除：订阅 SSE 数据流的代码块
  }

  function dispose() {
    modelData.value.clear()
    selectedId.value = null
    isInitialized.value = false
    // 已删除：断开 SSE 连接的代码块
    console.log('[TwinviewStore] disposed.')
  }

  function setSelected(id) {
    if (!id) {
      selectedId.value = null
      return
    }
    selectedId.value = id
  }

  function updateData(id, newData) {
    if (!modelData.value.has(id)) {
      console.warn(`[TwinviewStore] Attempted to update data for unknown ID: ${id}`)
      return
    }

    try {
      const config = SCENE_CONFIG.find(obj => obj.id === id)?.monitoring
      if (!config) {
        console.warn(`[TwinviewStore] No configuration found for ID: ${id}`)
        return
      }

      const currentData = modelData.value.get(id) || {}
      const mergedData = mergeData(currentData, newData)
      
      if (config.charts?.length > 0) {
        config.charts.forEach(chart => {
          trimHistoryData(mergedData, chart.type)
        })
      }
      
      modelData.value.set(id, mergedData)
      console.log(`[TwinviewStore] Data updated for ID: ${id}`, mergedData)
    } catch (error) {
      console.error(`[TwinviewStore] Error updating data for ID ${id}:`, error)
    }
  }

  // 辅助函数
  function mergeData(currentData, newData) {
    const merged = { ...currentData }
    
    Object.entries(newData).forEach(([key, value]) => {
      if (Array.isArray(value)) {
        merged[key] = [...(currentData[key] || []), ...value]
      } else {
        merged[key] = value
      }
    })

    return merged
  }

  function trimHistoryData(data, chartType = 'line') {
    const maxLength = CHART_CONFIG.maxDataPoints[chartType] || 100
    Object.keys(data).forEach(key => {
      if (Array.isArray(data[key])) {
        if (chartType === 'heatmap' && key === 'pressure') {
          data[key] = data[key].slice(-9)
        } else if (data[key].length > maxLength) {
          data[key] = data[key].slice(-maxLength)
        }
      }
    })
  }

  // 公共API
  function getDataById(id) {
    return id ? modelData.value.get(id) : null
  }

  function getConfigById(id) {
    if (!id) return null
    const sceneObject = SCENE_CONFIG.find(obj => obj.id === id)
    return sceneObject?.monitoring || null
  }

  function getObjectById(id) {
    if (!id) return null
    return SCENE_CONFIG.find(obj => obj.id === id) || null
  }

  return {
    // 状态
    selectedId,
    modelData,
    isInitialized,
    
    // Getters
    selectedData,
    selectedConfig,
    selectedObject,
    
    // Actions
    init,
    dispose,
    setSelected,
    updateData,
    getDataById,
    getConfigById,
    getObjectById
  }
})
