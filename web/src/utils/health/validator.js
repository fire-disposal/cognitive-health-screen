import { DATA_TYPES } from '@/api/services/health'

class ValidatorService {
  // 设备相关验证
  validateDevice(data) {
    const errors = {}

    if (!data.device_id?.trim()) {
      errors.device_id = '设备ID不能为空'
    }

    if (!data.name?.trim()) {
      errors.name = '设备名称不能为空'
    }

    if (data.mqtt_enabled && !data.mqtt_config?.topic?.trim()) {
      errors.mqtt_config = 'MQTT主题不能为空'
    }

    return {
      valid: Object.keys(errors).length === 0,
      errors
    }
  }

  // 患者相关验证
  validatePatient(data) {
    const errors = {}

    if (!data.name?.trim()) {
      errors.name = '患者姓名不能为空'
    }

    if (!data.gender) {
      errors.gender = '请选择性别'
    }

    if (!data.age || data.age < 0 || data.age > 150) {
      errors.age = '请输入有效年龄'
    }

    if (data.contact && !this.isValidPhone(data.contact)) {
      errors.contact = '请输入有效的联系方式'
    }

    if (data.emergency_contact && !this.isValidPhone(data.emergency_contact)) {
      errors.emergency_contact = '请输入有效的紧急联系方式'
    }

    return {
      valid: Object.keys(errors).length === 0,
      errors
    }
  }

  // 健康数据相关验证
  validateHealthData(data) {
    const errors = {}

    if (!data.device_id?.trim()) {
      errors.device_id = '设备ID不能为空'
    }

    if (!data.patient_id?.trim()) {
      errors.patient_id = '患者ID不能为空'
    }

    if (!data.data_type) {
      errors.data_type = '请选择数据类型'
    }

    if (!data.collected_at) {
      errors.collected_at = '采集时间不能为空'
    }

    if (!data.payload?.value) {
      errors.value = '数据值不能为空'
    } else {
      const dataType = Object.values(DATA_TYPES).find(t => t.value === data.data_type)
      if (dataType) {
        const { min, max } = dataType.thresholds
        const value = Number(data.payload.value)
        if (isNaN(value)) {
          errors.value = '请输入有效的数值'
        } else if (value < min || value > max) {
          errors.value = `数值应在 ${min} - ${max} ${dataType.unit} 之间`
        }
      }
    }

    return {
      valid: Object.keys(errors).length === 0,
      errors
    }
  }

  // 绑定相关验证
  validateBinding(data) {
    const errors = {}

    if (!data.device_id) {
      errors.device_id = '请选择设备'
    }

    if (!data.patient_id) {
      errors.patient_id = '请选择患者'
    }

    return {
      valid: Object.keys(errors).length === 0,
      errors
    }
  }

  // 通用验证方法
  isValidPhone(phone) {
    return /^1[3-9]\d{9}$/.test(phone) // 简单的手机号验证
  }

  isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  }

  isValidDate(date) {
    return !isNaN(new Date(date).getTime())
  }

  isNumber(value) {
    return !isNaN(Number(value))
  }

  isInRange(value, min, max) {
    const num = Number(value)
    return !isNaN(num) && num >= min && num <= max
  }

  // 批量验证
  validateBulkDevices(devices) {
    return devices.map(device => ({
      ...device,
      validation: this.validateDevice(device)
    }))
  }

  validateBulkPatients(patients) {
    return patients.map(patient => ({
      ...patient,
      validation: this.validatePatient(patient)
    }))
  }

  validateBulkHealthData(dataList) {
    return dataList.map(data => ({
      ...data,
      validation: this.validateHealthData(data)
    }))
  }
}

export default new ValidatorService()