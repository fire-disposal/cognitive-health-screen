import api from '../index'

// 数据类型定义
export const DATA_TYPES = {
  HEART_RATE: {
    value: 'heart_rate',
    label: '心率',
    unit: 'bpm',
    thresholds: { min: 60, max: 100 }
  },
  BLOOD_PRESSURE: {
    value: 'blood_pressure',
    label: '血压',
    unit: 'mmHg',
    thresholds: { min: 90, max: 140 }
  },
  BLOOD_OXYGEN: {
    value: 'blood_oxygen',
    label: '血氧',
    unit: '%',
    thresholds: { min: 95, max: 100 }
  },
  TEMPERATURE: {
    value: 'temperature',
    label: '体温',
    unit: '°C',
    thresholds: { min: 36, max: 37.3 }
  },
  BLOOD_GLUCOSE: {
    value: 'blood_glucose',
    label: '血糖',
    unit: 'mmol/L',
    thresholds: { min: 3.9, max: 6.1 }
  }
}

// 患者状态定义
export const PATIENT_STATUS = {
  ACTIVE: { value: 'active', label: '活跃' },
  INACTIVE: { value: 'inactive', label: '非活跃' }
}

class HealthService {
  // 设备相关
  async getDevices(params = {}) {
    const res = await api.getDeviceList(params)
    return {
      ...res,
      data: res.data?.map(this._formatDeviceData) || []
    }
  }

  async getDeviceById(id) {
    const res = await api.getDeviceById(id)
    return this._formatDeviceData(res)
  }

  async createDevice(data) {
    return api.createDevice(this._formatDeviceInput(data))
  }

  async updateDevice(id, data) {
    return api.updateDevice(id, this._formatDeviceInput(data))
  }

  async deleteDevice(id) {
    return api.deleteDevice(id)
  }

  async bulkCreateDevices(devices) {
    return api.bulkCreateDevice(devices.map(this._formatDeviceInput))
  }

  async getDeviceStatistics() {
    return api.getDeviceStatistics()
  }

  // 患者相关
  async getPatients(params = {}) {
    const res = await api.getPatientList(params)
    return {
      ...res,
      data: res.data?.map(this._formatPatientData) || []
    }
  }

  async getPatientById(id) {
    const res = await api.getPatient(id)
    return this._formatPatientData(res)
  }

  async createPatient(data) {
    return api.createPatient(this._formatPatientInput(data))
  }

  async updatePatient(id, data) {
    return api.updatePatient(id, this._formatPatientInput(data))
  }

  async deletePatient(id) {
    return api.deletePatient(id)
  }

  async bulkCreatePatients(patients) {
    return api.bulkCreatePatient(patients.map(this._formatPatientInput))
  }

  async updatePatientStatus(id, status) {
    return api.updatePatientStatus(id, status)
  }

  async getPatientStatistics() {
    return api.getPatientStatistics()
  }

  // 健康数据相关
  async getHealthData(params = {}) {
    const res = await api.getHealthDataList(params)
    return {
      ...res,
      data: res.data?.map(this._formatHealthData) || []
    }
  }

  async createHealthData(data) {
    return api.createHealthData(this._formatHealthDataInput(data))
  }

  async bulkCreateHealthData(dataList) {
    return api.bulkCreateHealthData(dataList.map(this._formatHealthDataInput))
  }

  async deleteHealthData(id) {
    return api.deleteHealthData(id)
  }

  async getHealthDataStatistics() {
    return api.getHealthDataStatistics()
  }

  /**
   * 通过用户名和设备ID解绑设备
   * @param {string} username 用户名
   * @param {string} deviceId 设备ID
   */
  async unbindDeviceFromPatientByUsername(username, deviceId) {
    const res = await api.unbindDeviceByUsername(username, deviceId)
    return res
  }

  // 数据格式化方法
  _formatDeviceData(device) {
    if (!device) return null
    return {
      ...device,
      status: device.online ? 'online' : 'offline',
      statusText: device.online ? '在线' : '离线',
      boundStatus: device.current_patient_id ? 'bound' : 'unbound',
      boundStatusText: device.current_patient_id ? '已绑定' : '未绑定'
    }
  }

  _formatDeviceInput(data) {
    const { id, created_at, updated_at, status, statusText, boundStatus, boundStatusText, ...input } = data
    return input
  }

  _formatPatientData(patient) {
    if (!patient) return null
    return {
      ...patient,
      statusText: PATIENT_STATUS[patient.status?.toUpperCase()]?.label || '未知',
      genderText: patient.gender === 'male' ? '男' : patient.gender === 'female' ? '女' : '未知',
      createdAtText: patient.created_at ? new Date(patient.created_at).toLocaleString() : '-'
    }
  }

  _formatPatientInput(data) {
    const { id, created_at, updated_at, statusText, genderText, createdAtText, ...input } = data
    return input
  }

  _formatHealthData(data) {
    if (!data) return null
    const dataType = Object.values(DATA_TYPES).find(t => t.value === data.data_type)
    const value = data.payload?.value
    const isNormal = this._checkDataNormal(data.data_type, value)

    return {
      ...data,
      dataTypeText: dataType?.label || data.data_type,
      unit: dataType?.unit || '',
      valueText: value ? `${value} ${dataType?.unit || ''}` : '-',
      status: isNormal ? 'normal' : 'abnormal',
      statusText: isNormal ? '正常' : '异常',
      collectedAtText: data.collected_at ? new Date(data.collected_at).toLocaleString() : '-'
    }
  }

  _formatHealthDataInput(data) {
    const { id, created_at, updated_at, dataTypeText, unit, valueText, status, statusText, collectedAtText, ...input } = data
    return input
  }

  _formatBindingData(binding) {
    if (!binding) return null
    const isActive = !binding.end_time
    return {
      ...binding,
      status: isActive ? 'active' : 'inactive',
      statusText: isActive ? '绑定中' : '已解绑',
      startTimeText: binding.start_time ? new Date(binding.start_time).toLocaleString() : '-',
      endTimeText: binding.end_time ? new Date(binding.end_time).toLocaleString() : '-'
    }
  }

  _checkDataNormal(type, value) {
    const dataType = Object.values(DATA_TYPES).find(t => t.value === type)
    if (!dataType || !value) return true
    return value >= dataType.thresholds.min && value <= dataType.thresholds.max
  }
}

export default new HealthService()