// 数字孪生场景配置数据
export const SCENE_CONFIG = [
  {
    id: 'elderly_001',
    name: '张奶奶',
    type: 'elderly',
    position: { x: -3, y: 0, z: -5 },
    status: 'active',
    monitoring: {
      vitals: {
        heartRate: { min: 60, max: 100, unit: 'BPM' },
        breathingRate: { min: 12, max: 20, unit: '次/分' },
        bloodPressure: { min: 90, max: 140, unit: 'mmHg' },
        temperature: { min: 36, max: 37.5, unit: '°C' }
      },
      activity: {
        location: 'living_room',
        status: 'resting',
        lastMovement: new Date().toISOString()
      },
      charts: [
        {
          type: 'heartRate',
          title: '心率监测',
          unit: 'BPM',
          color: '#ff6b6b'
        },
        {
          type: 'breathingRate',
          title: '呼吸频率',
          unit: '次/分',
          color: '#4ecdc4'
        }
      ]
    }
  },
  {
    id: 'elderly_002',
    name: '王爷爷',
    type: 'elderly',
    position: { x: 3, y: 0, z: 0 },
    status: 'active',
    monitoring: {
      vitals: {
        heartRate: { min: 60, max: 100, unit: 'BPM' },
        breathingRate: { min: 12, max: 20, unit: '次/分' },
        bloodPressure: { min: 90, max: 140, unit: 'mmHg' },
        temperature: { min: 36, max: 37.5, unit: '°C' }
      },
      activity: {
        location: 'kitchen',
        status: 'moving',
        lastMovement: new Date().toISOString()
      },
      charts: [
        {
          type: 'heartRate',
          title: '心率监测',
          unit: 'BPM',
          color: '#ff6b6b'
        },
        {
          type: 'breathingRate',
          title: '呼吸频率',
          unit: '次/分',
          color: '#4ecdc4'
        }
      ]
    }
  },
  {
    id: 'elderly_003',
    name: '吴大爷',
    type: 'elderly',
    position: { x: 0, y: 0, z: 3 },
    status: 'active',
    monitoring: {
      vitals: {
        heartRate: { min: 60, max: 100, unit: 'BPM' },
        breathingRate: { min: 12, max: 20, unit: '次/分' },
        bloodPressure: { min: 90, max: 140, unit: 'mmHg' },
        temperature: { min: 36, max: 37.5, unit: '°C' }
      },
      activity: {
        location: 'bedroom',
        status: 'sleeping',
        lastMovement: new Date().toISOString()
      },
      charts: [
        {
          type: 'heartRate',
          title: '心率监测',
          unit: 'BPM',
          color: '#ff6b6b'
        },
        {
          type: 'breathingRate',
          title: '呼吸频率',
          unit: '次/分',
          color: '#4ecdc4'
        }
      ]
    }
  },
  {
    id: 'sensor_temp_001',
    name: '温湿度传感器-客厅',
    type: 'sensor',
    position: { x: -8, y: 6, z: -8 },
    status: 'online',
    monitoring: {
      environment: {
        temperature: { min: 18, max: 28, unit: '°C' },
        humidity: { min: 40, max: 70, unit: '%' }
      },
      charts: [
        {
          type: 'temperature',
          title: '温度变化',
          unit: '°C',
          color: '#ff9f43'
        },
        {
          type: 'humidity',
          title: '湿度变化',
          unit: '%',
          color: '#3742fa'
        }
      ]
    }
  },
  {
    id: 'sensor_light_001',
    name: '光照传感器-客厅',
    type: 'sensor',
    position: { x: 8, y: 6, z: -8 },
    status: 'online',
    monitoring: {
      environment: {
        light: { min: 100, max: 800, unit: 'lx' }
      },
      charts: [
        {
          type: 'light',
          title: '光照强度',
          unit: 'lx',
          color: '#feca57'
        }
      ]
    }
  },
  {
    id: 'sensor_air_001',
    name: '空气质量传感器-客厅',
    type: 'sensor',
    position: { x: -8, y: 6, z: 8 },
    status: 'online',
    monitoring: {
      environment: {
        airQuality: { min: 0, max: 100, unit: 'AQI' },
        pm25: { min: 0, max: 75, unit: 'μg/m³' }
      },
      charts: [
        {
          type: 'airQuality',
          title: '空气质量指数',
          unit: 'AQI',
          color: '#2ed573'
        },
        {
          type: 'pm25',
          title: 'PM2.5浓度',
          unit: 'μg/m³',
          color: '#ff6348'
        }
      ]
    }
  },
  {
    id: 'sensor_motion_001',
    name: '运动传感器-客厅',
    type: 'sensor',
    position: { x: 8, y: 6, z: 8 },
    status: 'online',
    monitoring: {
      motion: {
        detected: { type: 'boolean' },
        intensity: { min: 0, max: 100, unit: '%' }
      },
      charts: [
        {
          type: 'motion',
          title: '运动检测',
          unit: '次数',
          color: '#a55eea'
        }
      ]
    }
  }
]

// 图表配置
export const CHART_CONFIG = {
  heartRate: {
    title: '心率监测',
    unit: 'BPM',
    color: '#ff6b6b',
    normal: { min: 60, max: 100 },
    warning: { min: 50, max: 120 },
    danger: { min: 40, max: 150 }
  },
  breathingRate: {
    title: '呼吸频率',
    unit: '次/分',
    color: '#4ecdc4',
    normal: { min: 12, max: 20 },
    warning: { min: 8, max: 25 },
    danger: { min: 5, max: 30 }
  },
  temperature: {
    title: '环境温度',
    unit: '°C',
    color: '#ff9f43',
    normal: { min: 18, max: 28 },
    warning: { min: 15, max: 32 },
    danger: { min: 10, max: 40 }
  },
  humidity: {
    title: '环境湿度',
    unit: '%',
    color: '#3742fa',
    normal: { min: 40, max: 70 },
    warning: { min: 30, max: 80 },
    danger: { min: 20, max: 90 }
  },
  light: {
    title: '光照强度',
    unit: 'lx',
    color: '#feca57',
    normal: { min: 200, max: 500 },
    warning: { min: 100, max: 800 },
    danger: { min: 50, max: 1000 }
  },
  airQuality: {
    title: '空气质量',
    unit: 'AQI',
    color: '#2ed573',
    normal: { min: 80, max: 100 },
    warning: { min: 60, max: 79 },
    danger: { min: 0, max: 59 }
  },
  pm25: {
    title: 'PM2.5浓度',
    unit: 'μg/m³',
    color: '#ff6348',
    normal: { min: 0, max: 35 },
    warning: { min: 36, max: 75 },
    danger: { min: 76, max: 150 }
  },
  motion: {
    title: '运动检测',
    unit: '次数',
    color: '#a55eea',
    normal: { min: 0, max: 50 },
    warning: { min: 51, max: 100 },
    danger: { min: 101, max: 200 }
  }
}

// 房间配置
export const ROOM_CONFIG = {
  living_room: {
    id: 'living_room',
    name: '客厅',
    position: { x: 0, y: 0, z: 0 },
    size: { width: 20, height: 8, depth: 20 },
    sensors: ['sensor_temp_001', 'sensor_light_001', 'sensor_air_001', 'sensor_motion_001']
  },
  bedroom: {
    id: 'bedroom',
    name: '卧室',
    position: { x: 25, y: 0, z: 0 },
    size: { width: 15, height: 8, depth: 15 },
    sensors: ['sensor_temp_002', 'sensor_light_002']
  },
  kitchen: {
    id: 'kitchen',
    name: '厨房',
    position: { x: 0, y: 0, z: 25 },
    size: { width: 12, height: 8, depth: 10 },
    sensors: ['sensor_temp_003', 'sensor_air_002']
  },
  bathroom: {
    id: 'bathroom',
    name: '卫生间',
    position: { x: 15, y: 0, z: 25 },
    size: { width: 8, height: 8, depth: 8 },
    sensors: ['sensor_temp_004', 'sensor_motion_002']
  },
  balcony: {
    id: 'balcony',
    name: '阳台',
    position: { x: -15, y: 0, z: 0 },
    size: { width: 8, height: 8, depth: 15 },
    sensors: ['sensor_light_003', 'sensor_air_003']
  }
}

// 生成模拟数据的工具函数
export function generateMockData(type, count = 24) {
  const config = CHART_CONFIG[type]
  if (!config) return []
  
  const data = []
  const now = new Date()
  
  for (let i = count - 1; i >= 0; i--) {
    const timestamp = new Date(now.getTime() - i * 60 * 60 * 1000) // 每小时一个数据点
    let value
    
    // 根据类型生成不同的模拟数据
    switch (type) {
      case 'heartRate':
        value = 65 + Math.random() * 20 + Math.sin(i * 0.5) * 5
        break
      case 'breathingRate':
        value = 14 + Math.random() * 4 + Math.sin(i * 0.3) * 2
        break
      case 'temperature':
        value = 22 + Math.random() * 6 + Math.sin(i * 0.2) * 3
        break
      case 'humidity':
        value = 50 + Math.random() * 20 + Math.sin(i * 0.4) * 10
        break
      case 'light':
        // 模拟日夜变化
        const hour = (24 - i) % 24
        if (hour >= 6 && hour <= 18) {
          value = 300 + Math.random() * 400 + Math.sin((hour - 6) * Math.PI / 12) * 200
        } else {
          value = 50 + Math.random() * 100
        }
        break
      case 'airQuality':
        value = 75 + Math.random() * 20 + Math.sin(i * 0.1) * 5
        break
      case 'pm25':
        value = 20 + Math.random() * 30 + Math.sin(i * 0.15) * 10
        break
      case 'motion':
        value = Math.random() > 0.7 ? Math.floor(Math.random() * 10) : 0
        break
      default:
        value = Math.random() * 100
    }
    
    data.push({
      timestamp: timestamp.toISOString(),
      value: Math.round(value * 100) / 100
    })
  }
  
  return data
}

// 获取数据状态（正常/警告/危险）
export function getDataStatus(type, value) {
  const config = CHART_CONFIG[type]
  if (!config || value === null || value === undefined) return 'unknown'
  
  if (value >= config.normal.min && value <= config.normal.max) {
    return 'normal'
  } else if (value >= config.warning.min && value <= config.warning.max) {
    return 'warning'
  } else {
    return 'danger'
  }
}

// 获取状态颜色
export function getStatusColor(status) {
  switch (status) {
    case 'normal':
      return '#2ed573'
    case 'warning':
      return '#ffa502'
    case 'danger':
      return '#ff3838'
    default:
      return '#747d8c'
  }
}

// 获取状态文本
export function getStatusText(status) {
  switch (status) {
    case 'normal':
      return '正常'
    case 'warning':
      return '警告'
    case 'danger':
      return '危险'
    default:
      return '未知'
  }
}
