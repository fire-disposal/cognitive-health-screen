import { request } from '@/utils'

export default {
  login: (data) => request.post('/base/access_token', data, { noNeedToken: true }),
  getUserInfo: () => request.get('/base/userinfo'),
  getUserMenu: () => request.get('/base/usermenu'),
  getUserApi: () => request.get('/base/userapi'),
  // profile
  updatePassword: (data = {}) => request.post('/base/update_password', data),
  updateUserTheme: (theme) => request.post('/base/update_theme', { theme }),
  updateUserLogo: (logo_type) => request.post('/base/update_logo', { logo_type }),
  // users
  getUserList: (params = {}) => request.get('/user/list', { params }),
  getUserById: (params = {}) => request.get('/user/get', { params }),
  createUser: (data = {}) => request.post('/user/create', data),
  updateUser: (data = {}) => request.post('/user/update', data),
  deleteUser: (params = {}) => request.delete(`/user/delete`, { params }),
  resetPassword: (data = {}) => request.post(`/user/reset_password`, data),
  // role
  getRoleList: (params = {}) => request.get('/role/list', { params }),
  createRole: (data = {}) => request.post('/role/create', data),
  updateRole: (data = {}) => request.post('/role/update', data),
  deleteRole: (params = {}) => request.delete('/role/delete', { params }),
  updateRoleAuthorized: (data = {}) => request.post('/role/authorized', data),
  getRoleAuthorized: (params = {}) => request.get('/role/authorized', { params }),
  // menus
  getMenus: (params = {}) => request.get('/menu/list', { params }),
  createMenu: (data = {}) => request.post('/menu/create', data),
  updateMenu: (data = {}) => request.post('/menu/update', data),
  deleteMenu: (params = {}) => request.delete('/menu/delete', { params }),
  // apis
  getApis: (params = {}) => request.get('/api/list', { params }),
  createApi: (data = {}) => request.post('/api/create', data),
  updateApi: (data = {}) => request.post('/api/update', data),
  deleteApi: (params = {}) => request.delete('/api/delete', { params }),
  refreshApi: (data = {}) => request.post('/api/refresh', data),
  // depts
  getDepts: (params = {}) => request.get('/dept/list', { params }),
  createDept: (data = {}) => request.post('/dept/create', data),
  updateDept: (data = {}) => request.post('/dept/update', data),
  deleteDept: (params = {}) => request.delete('/dept/delete', { params }),
  // auditlog
  getAuditLogList: (params = {}) => request.get('/auditlog/list', { params }),

  // device API (RESTful)
  // device API (RESTful)
  getDeviceList: (params = {}) => request.get('/health/devices', { params }),
  getDevices: (params = {}) => request.get('/health/devices', { params }),
  createDevice: (data = {}) => request.post('/health/devices', data),
  bulkCreateDevice: (data = []) => request.post('/health/devices/bulk', data),
  updateDevice: (device_id, data = {}) => request.put(`/health/devices/${Number(device_id)}`, data),
  deleteDevice: (device_id) => request.delete(`/health/devices/${Number(device_id)}`),
  getPatientDevices: (patient_id, params = {}) =>
    request.get(`/health/devices/patient/${Number(patient_id)}`, { params }),
  getDeviceStatistics: () => request.get('/health/devices/statistics'),
  // 解绑设备与用户（POST body: { username, device_id }，均为字符串，需前端保证类型正确）
  unbindDeviceByUsername: (username, device_id) =>
    request.post('/health/devices/unbind-by-username', { username, device_id }),

  // patient API (RESTful)
  getPatientList: (params = {}) => request.get('/health/patients', { params }),
  getPatients: (params = {}) => request.get('/health/patients', { params }),
  getPatient: (patient_id) => request.get(`/health/patients/${Number(patient_id)}`),
  createPatient: (data = {}) => request.post('/health/patients', data),
  updatePatient: (patient_id, data = {}) =>
    request.put(`/health/patients/${Number(patient_id)}`, data),
  deletePatient: (patient_id) => request.delete(`/health/patients/${Number(patient_id)}`),
  bulkCreatePatient: (data = []) => request.post('/health/patients/bulk', data),
  bulkDeletePatient: (patient_ids = []) =>
    request.delete('/health/patients/bulk', { data: patient_ids }),
  getPatientsByStatus: (status, params = {}) =>
    request.get(`/health/patients/by-status/${status}`, { params }),
  updatePatientStatus: (patient_id, status) =>
    request.patch(`/health/patients/${Number(patient_id)}/status`, { status }),
  getPatientStatistics: () => request.get('/health/patients/statistics'),
  // health datasheet API (RESTful)
  getHealthDataList: (params = {}) => request.get('/health/records', { params }),
  getHealthData: (datasheet_id) => request.get(`/health/records/${datasheet_id}`),
  createHealthData: (data = {}) => request.post('/health/records', data),
  bulkCreateHealthData: (data = []) => request.post('/health/records/bulk', data),
  updateHealthData: (datasheet_id, data = {}) =>
    request.put(`/health/records/${datasheet_id}`, data),
  deleteHealthData: (datasheet_id) => request.delete(`/health/records/${datasheet_id}`),
  bulkDeleteHealthData: (datasheet_ids = []) =>
    request.delete('/health/records/bulk', { data: datasheet_ids }),
  getHealthDataStatistics: () => request.get('/health/records/statistics'),
  searchHealthData: (params = {}) => request.get('/health/records', { params }),

  // alert API (告警管理)
  getAlerts: (params = {}) => request.get('/health/alerts', { params }),
  getAlert: (alert_id) => request.get(`/health/alerts/${alert_id}`),
  createAlert: (data = {}) => request.post('/health/alerts', data),
  updateAlert: (alert_id, data = {}) => request.put(`/health/alerts/${alert_id}`, data),
  deleteAlert: (alert_id) => request.delete(`/health/alerts/${alert_id}`),
  getAlertStatistics: () => request.get('/health/alerts/statistics'),

  // advanced records API (高级健康数据)
  getAdvancedRecords: (params = {}) => request.get('/health/advanced-records', { params }),
  getAdvancedRecord: (record_id) => request.get(`/health/advanced-records/${record_id}`),
  createAdvancedRecord: (data = {}) => request.post('/health/advanced-records', data),
  getAdvancedRecordStatistics: () => request.get('/health/advanced-records/statistics'),

  // health events API (健康事件)
  getHealthEventStatistics: () => request.get('/health/health-events/statistics'),
  getHealthEvents: (params = {}) => request.get('/health/health-events', { params }),

  // digital twin API (数字孪生)
  // 获取老人列表（用于数字孪生选择）
  getElderlyList: (params = {}) => request.get('/digital-twin/elderly', { params }),
  // 获取指定老人的实时状态
  getElderlyStatus: (elderly_id) => request.get(`/digital-twin/elderly/${elderly_id}/status`),
  // 获取环境传感器数据
  getEnvironmentData: (params = {}) => request.get('/digital-twin/environment', { params }),
  // 获取指定老人的活动轨迹
  getActivityTrajectory: (elderly_id, params = {}) =>
    request.get(`/digital-twin/elderly/${elderly_id}/trajectory`, { params }),
  // 获取房间列表
  getRoomList: () => request.get('/digital-twin/rooms'),
  // 获取传感器列表
  getSensorList: (params = {}) => request.get('/digital-twin/sensors', { params }),
  // 获取指定房间的传感器数据
  getRoomSensorData: (room_id) => request.get(`/digital-twin/rooms/${room_id}/sensors`),

  // health assessment API (健康评估)
  // 获取评估问卷列表
  getAssessmentQuestionnaires: (params = {}) => request.get('/health/assessments/questionnaires', { params }),
  // 获取指定问卷详情
  getAssessmentQuestionnaire: (questionnaire_id) => request.get(`/health/assessments/questionnaires/${questionnaire_id}`),
  // 提交评估结果
  submitAssessmentResult: (data = {}) => request.post('/health/assessments/results', data),
  // 获取评估结果列表
  getAssessmentResults: (params = {}) => request.get('/health/assessments/results', { params }),
  // 获取指定患者的评估结果
  getPatientAssessmentResults: (patient_id, params = {}) => request.get(`/health/assessments/results/patient/${patient_id}`, { params }),
  // 获取评估统计信息
  getAssessmentStatistics: () => request.get('/health/assessments/statistics'),

  // 认知功能评估
  getCognitiveAssessments: (params = {}) => request.get('/health/assessments/cognitive', { params }),
  submitCognitiveAssessment: (data = {}) => request.post('/health/assessments/cognitive', data),
  getCognitiveAssessmentResult: (assessment_id) => request.get(`/health/assessments/cognitive/${assessment_id}`),

  // 生理健康评估
  getPhysiologicalAssessments: (params = {}) => request.get('/health/assessments/physiological', { params }),
  submitPhysiologicalAssessment: (data = {}) => request.post('/health/assessments/physiological', data),
  getPhysiologicalAssessmentResult: (assessment_id) => request.get(`/health/assessments/physiological/${assessment_id}`),

  // 日常生活能力评估
  getADLAssessments: (params = {}) => request.get('/health/assessments/adl', { params }),
  submitADLAssessment: (data = {}) => request.post('/health/assessments/adl', data),
  getADLAssessmentResult: (assessment_id) => request.get(`/health/assessments/adl/${assessment_id}`),

  // 风险预测与AI分析
  getRiskPrediction: (patient_id, params = {}) => request.get(`/health/risk-prediction/${patient_id}`, { params }),
  getComprehensiveRiskAssessment: (patient_id) => request.get(`/health/risk-assessment/comprehensive/${patient_id}`),
  getRiskTrendPrediction: (patient_id, params = {}) => request.get(`/health/risk-prediction/trend/${patient_id}`, { params }),
  getAIPredictionResults: (patient_id, params = {}) => request.get(`/health/ai-prediction/${patient_id}`, { params }),
  getPreventionRecommendations: (patient_id) => request.get(`/health/prevention-recommendations/${patient_id}`),

  // 统计分析API
  // 获取患者综合统计数据
  getPatientAnalysisData: (patient_id) => request.get(`/health/analysis/patient/${patient_id}`),
  // 获取健康数据趋势分析
  getHealthTrendsAnalysis: (patient_id, params = {}) => request.get(`/health/analysis/health-trends/${patient_id}`, { params }),
  // 获取设备状态分析
  getDeviceAnalysis: (patient_id, params = {}) => request.get(`/health/analysis/device-status/${patient_id}`, { params }),
  // 获取评估结果分析
  getAssessmentAnalysis: (patient_id, params = {}) => request.get(`/health/analysis/assessment/${patient_id}`, { params }),
  // 获取数字孪生分析数据
  getDigitalTwinAnalysis: (patient_id, params = {}) => request.get(`/health/analysis/digital-twin/${patient_id}`, { params }),
  // 获取告警分析数据
  getAlertAnalysis: (patient_id, params = {}) => request.get(`/health/analysis/alerts/${patient_id}`, { params }),
  // 获取风险分析数据
  getRiskAnalysis: (patient_id, params = {}) => request.get(`/health/analysis/risk/${patient_id}`, { params }),
  // 获取综合分析报告
  getComprehensiveAnalysis: (patient_id, params = {}) => request.get(`/health/analysis/comprehensive/${patient_id}`, { params }),
}
