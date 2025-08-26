import { defineStore } from 'pinia'
import healthService from '@/api/services/health'
import messageService from '@/utils/health/message'

export const useHealthStore = defineStore('health', {
  state: () => ({
    // 设备相关
    deviceSummaries: [], // 初始化为空数组
    selectedDeviceId: null,
    selectedDeviceData: null,
    deviceStatistics: {
      total: 0,
      online: 0,
      offline: 0,
      bound: 0
    },

    // 患者相关
    patients: [],
    patientTotal: 0,
    patientStatistics: {
      total: 0,
      active: 0,
      inactive: 0,
      with_device: 0
    },

    // 健康数据相关
    healthData: [],
    healthDataTotal: 0,
    healthDataStatistics: {
      total: 0,
      today: 0,
      abnormal: 0,
      devices: 0
    },

    // 绑定相关
    bindings: [],
    bindingTotal: 0,
    bindingStatistics: {
      total_bindings: 0,
      active_bindings: 0,
      total_devices: 0,
      bound_patients: 0
    },

    // 加载状态
    loading: {
      devices: false,
      patients: false,
      healthData: false,
      bindings: false
    }
  }),

  getters: {
    // 设备相关
    onlineDevices: (state) => state.deviceSummaries.filter(d => d.status === 'online'),
    unboundDevices: (state) => state.deviceSummaries.filter(d => !d.current_patient_id),
    deviceById: (state) => (id) => state.deviceSummaries.find(d => d.id === id),

    // 患者相关
    activePatients: (state) => state.patients.filter(p => p.status === 'active'),
    patientById: (state) => (id) => state.patients.find(p => p.id === id),
    patientsWithDevice: (state) => state.patients.filter(p => p.device_count > 0),

    // 健康数据相关
    abnormalData: (state) => state.healthData.filter(d => d.status === 'abnormal'),
    dataByType: (state) => (type) => state.healthData.filter(d => d.data_type === type),
    todayData: (state) => state.healthData.filter(d => {
      const today = new Date().toISOString().split('T')[0]
      return d.collected_at.startsWith(today)
    }),

    // 绑定相关
    activeBindings: (state) => state.bindings.filter(b => b.status === 'active'),
    bindingsByDevice: (state) => (deviceId) => state.bindings.filter(b => b.device_id === deviceId),
    bindingsByPatient: (state) => (patientId) => state.bindings.filter(b => b.patient_id === patientId)
  },

  actions: {
    // 设备相关
    async fetchDeviceSummaries() {
      this.loading.devices = true
      try {
        const res = await healthService.getDevices()
        this.deviceSummaries = res.data || []
        return this.deviceSummaries
      } catch (error) {
        messageService.handleError(error)
        this.deviceSummaries = [] // 错误时设置为空数组
        throw error
      } finally {
        this.loading.devices = false
      }
    },

    selectDevice(deviceId) {
      this.selectedDeviceId = deviceId
      if (deviceId) {
        this.selectedDeviceData = this.deviceSummaries.find(d => d.device_id === deviceId) || null
      } else {
        this.selectedDeviceData = null
      }
    },

    getDeviceLatestValue(deviceId, dataType) {
      const device = this.deviceSummaries.find(d => d.device_id === deviceId)
      if (!device || !device.latest_data) return null
      return device.latest_data[dataType]
    },

    getHealthStatus(deviceId) {
      const device = this.deviceSummaries.find(d => d.device_id === deviceId)
      if (!device) return 'unknown'
      if (!device.latest_data) return 'unknown'

      const heartRate = device.latest_data.heart_rate
      if (heartRate && (heartRate < 60 || heartRate > 100)) return 'warning'

      const temperature = device.latest_data.temperature
      if (temperature && (temperature < 36 || temperature > 37.5)) return 'warning'

      return 'normal'
    },

    getDataFreshness(deviceId, dataType) {
      const device = this.deviceSummaries.find(d => d.device_id === deviceId)
      if (!device || !device.latest_data || !device.latest_data[`${dataType}_timestamp`]) {
        return 'stale'
      }

      const timestamp = device.latest_data[`${dataType}_timestamp`]
      const now = Date.now()
      const diff = now - new Date(timestamp).getTime()

      if (diff < 5 * 60 * 1000) return 'fresh' // 5分钟内
      if (diff < 30 * 60 * 1000) return 'recent' // 30分钟内
      return 'stale'
    },

    // 其他 actions 保持不变...
  }
})
