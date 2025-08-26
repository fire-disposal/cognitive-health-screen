

// 杭州市区域内的一些坐标点（经度，纬度）
const HANGZHOU_LOCATIONS = [
  [120.153576, 30.287459], // 西湖
  [120.161693, 30.279429], // 断桥残雪
  [120.148792, 30.259244], // 雷峰塔
  [120.171031, 30.244197], // 钱江新城
  [120.219375, 30.259244], // 滨江区
  [120.131261, 30.279429], // 西溪湿地
  [120.188999, 30.315085], // 拱墅区
  [120.201416, 30.287459], // 下城区
  [120.169373, 30.315085], // 上城区
  [120.126343, 30.244197]  // 之江
]

// 模拟患者基础信息 - 与告警内容匹配
const MOCK_PATIENTS = [
  {
    id: 'patient_001',
    name: '张伟',
    age: 75,
    gender: '男',
    phone: '138****1234',
    emergencyContact: '张小明 (儿子)',
    emergencyPhone: '139****5678',
    medicalHistory: ['慢性阻塞性肺疾病', '高血压'],
    currentMedication: ['支气管扩张剂', '降压药'],
    riskLevel: 'high',
    address: '浙江省杭州市西湖区文三路269号',
    location: [120.153576, 30.287459], // 西湖附近
    deviceId: 3,
    currentAlert: '血氧浓度低于92%，请注意呼吸状况'
  },
  {
    id: 'patient_002',
    name: '李丽',
    age: 68,
    gender: '女',
    phone: '136****9876',
    emergencyContact: '李小华 (女儿)',
    emergencyPhone: '137****4321',
    medicalHistory: ['高血压', '糖尿病'],
    currentMedication: ['降压药', '胰岛素'],
    riskLevel: 'high',
    address: '浙江省杭州市上城区延安路126号',
    location: [120.169373, 30.315085], // 上城区
    deviceId: 2,
    currentAlert: '收缩压高于160mmHg，需紧急干预'
  },
  {
    id: 'patient_003',
    name: '王强',
    age: 72,
    gender: '男',
    phone: '135****5555',
    emergencyContact: '王小红 (女儿)',
    emergencyPhone: '138****7777',
    medicalHistory: ['心律不齐', '高血压'],
    currentMedication: ['抗心律失常药', '降压药'],
    riskLevel: 'medium',
    address: '浙江省杭州市滨江区江南大道588号',
    location: [120.219375, 30.259244], // 滨江区
    deviceId: 1,
    currentAlert: '心率超过120次/分，建议休息并复查'
  }
  
]

// 告警类型对应的位置信息
const ALERT_LOCATION_TYPES = {
  'heart_rate_abnormal': '心率异常告警',
  'fall_detection': '跌倒检测告警',
  'medication_reminder': '用药提醒',
  'emergency_call': '紧急呼叫',
  'device_offline': '设备离线',
  'location_abnormal': '位置异常'
}

/**
 * 生成随机位置坐标（杭州市区域内）
 */
export const generateRandomLocation = () => {
  const baseLocation = HANGZHOU_LOCATIONS[Math.floor(Math.random() * HANGZHOU_LOCATIONS.length)]
  // 在基础位置附近随机偏移（约1公里范围内）
  const offsetLng = (Math.random() - 0.5) * 0.01
  const offsetLat = (Math.random() - 0.5) * 0.01

  return [
    baseLocation[0] + offsetLng,
    baseLocation[1] + offsetLat
  ]
}

/**
 * 根据告警数据生成地图标注点数据
 */
export const generateMapMarkersFromAlert = (alertData) => {
  if (!alertData) return []

  // 根据告警消息中的姓名直接匹配患者信息
  let patient = null

  if (alertData.message && alertData.message.includes('张伟')) {
    patient = MOCK_PATIENTS.find(p => p.name === '张伟')
  } else if (alertData.message && alertData.message.includes('李丽')) {
    patient = MOCK_PATIENTS.find(p => p.name === '李丽')
  } else if (alertData.message && alertData.message.includes('王强')) {
    patient = MOCK_PATIENTS.find(p => p.name === '王强')
  }

  // 如果没有匹配到，使用第一个患者作为默认
  if (!patient) {
    patient = MOCK_PATIENTS[0]
  }
  
  // 生成位置信息（优先使用患者的具体位置，其次是告警数据中的位置，最后随机生成）
  const position = patient.location || alertData.location || generateRandomLocation()
  
  // 根据告警级别确定图标颜色（返回红色位置标记图标配置）
  const getMarkerIconConfig = (level) => {
    const iconColors = {
      'critical': '#ff4757', // 红色
      'warning': '#ffa502',  // 橙色
      'info': '#3742fa'      // 蓝色
    }

    const color = iconColors[level] || '#ff4757' // 默认使用红色

    // 创建红色位置标记图标
    const svgContent = `<svg xmlns="http://www.w3.org/2000/svg" width="36" height="48" viewBox="0 0 36 48"><defs><filter id="shadow-${level}" x="-50%" y="-50%" width="200%" height="200%"><feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="rgba(0,0,0,0.5)"/></filter></defs><path d="M18 0C8.059 0 0 8.059 0 18c0 10.941 18 30 18 30s18-19.059 18-30C36 8.059 27.941 0 18 0z" fill="${color}" filter="url(#shadow-${level})"/><circle cx="18" cy="18" r="8" fill="white" opacity="0.95"/><circle cx="18" cy="18" r="4" fill="${color}"/></svg>`

    return {
      size: [36, 48],
      image: `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svgContent)}`,
      imageSize: [36, 48]
    }
  }
  
  // 构建信息窗口内容
  const infoContent = {
    title: `${patient.name} - ${ALERT_LOCATION_TYPES[alertData.rule_name] || '告警信息'}`,
    content: `
      <div style="padding: 8px 0;">
        <div style="margin-bottom: 8px;">
          <strong>告警内容：</strong>${alertData.message}
        </div>
        <div style="margin-bottom: 8px;">
          <strong>患者信息：</strong>${patient.name} (${patient.age}岁 ${patient.gender})
        </div>
        <div style="margin-bottom: 8px;">
          <strong>联系电话：</strong>${patient.phone}
        </div>
        <div style="margin-bottom: 8px;">
          <strong>紧急联系人：</strong>${patient.emergencyContact}
        </div>
        <div style="margin-bottom: 8px;">
          <strong>紧急联系电话：</strong>${patient.emergencyPhone}
        </div>
        <div style="margin-bottom: 8px;">
          <strong>居住地址：</strong>${patient.address || '地址信息暂无'}
        </div>
        <div style="margin-bottom: 8px;">
          <strong>风险等级：</strong>
          <span style="color: ${patient.riskLevel === 'high' ? '#ff4757' : patient.riskLevel === 'medium' ? '#ffa502' : '#2ed573'}">
            ${patient.riskLevel === 'high' ? '高风险' : patient.riskLevel === 'medium' ? '中风险' : '低风险'}
          </span>
        </div>
        ${patient.medicalHistory.length > 0 ? `
          <div style="margin-bottom: 8px;">
            <strong>病史：</strong>${patient.medicalHistory.join('、')}
          </div>
        ` : ''}
        <div style="font-size: 12px; color: #666; margin-top: 8px;">
          告警时间：${new Date(alertData.created_at).toLocaleString()}
        </div>
      </div>
    `
  }
  
  return [{
    id: `marker_${alertData.id}`,
    position: position,
    title: `${patient.name} - ${alertData.message}`,
    iconConfig: getMarkerIconConfig(alertData.level),
    level: alertData.level,
    infoContent: infoContent,
    patientData: patient,
    alertData: alertData
  }]
}



/**
 * 生成多个测试标注点
 */
export const generateTestMarkers = (count = 3) => {
  const markers = []
  
  for (let i = 0; i < count; i++) {
    const patient = MOCK_PATIENTS[i % MOCK_PATIENTS.length]
    const position = generateRandomLocation()
    
    const mockAlert = {
      id: `alert_${i + 1}`,
      level: ['critical', 'warning', 'info'][Math.floor(Math.random() * 3)],
      message: `模拟告警信息 ${i + 1}`,
      rule_name: Object.keys(ALERT_LOCATION_TYPES)[Math.floor(Math.random() * Object.keys(ALERT_LOCATION_TYPES).length)],
      patient_id: patient.id,
      created_at: new Date().toISOString(),
      location: position
    }
    
    markers.push(...generateMapMarkersFromAlert(mockAlert))
  }
  
  return markers
}

/**
 * 获取所有模拟患者数据
 */
export const getAllMockPatients = () => {
  return [...MOCK_PATIENTS]
}

/**
 * 获取杭州市中心坐标
 */
export const getHangzhouCenter = () => {
  return [120.153576, 30.287459] // 西湖坐标
}


export const getBeijingCenter = () => {
  return getHangzhouCenter()
}
