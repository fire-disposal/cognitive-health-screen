import { useMessage } from 'naive-ui'

class MessageService {
  constructor() {
    this.messageApi = null
  }

  init() {
    this.messageApi = useMessage()
  }

  success(message) {
    this.messageApi?.success(message)
  }

  error(message) {
    this.messageApi?.error(message)
  }

  warning(message) {
    this.messageApi?.warning(message)
  }

  info(message) {
    this.messageApi?.info(message)
  }

  // 预定义的消息
  static MESSAGES = {
    CREATE_SUCCESS: '创建成功',
    UPDATE_SUCCESS: '更新成功',
    DELETE_SUCCESS: '删除成功',
    BIND_SUCCESS: '绑定成功',
    UNBIND_SUCCESS: '解绑成功',
    IMPORT_SUCCESS: '导入成功',
    EXPORT_SUCCESS: '导出成功',
    OPERATION_SUCCESS: '操作成功',

    CREATE_ERROR: '创建失败',
    UPDATE_ERROR: '更新失败',
    DELETE_ERROR: '删除失败',
    BIND_ERROR: '绑定失败',
    UNBIND_ERROR: '解绑失败',
    IMPORT_ERROR: '导入失败',
    EXPORT_ERROR: '导出失败',
    OPERATION_ERROR: '操作失败',

    NETWORK_ERROR: '网络错误，请稍后重试',
    SERVER_ERROR: '服务器错误，请稍后重试',
    VALIDATION_ERROR: '请检查输入是否正确',
    PERMISSION_ERROR: '没有权限执行此操作',
    
    DATA_LOADING: '数据加载中...',
    NO_DATA: '暂无数据',
    CONFIRM_DELETE: '确认删除？',
    CONFIRM_UNBIND: '确认解绑？',

    REQUIRED_FIELD: '此字段为必填项',
    INVALID_FORMAT: '格式不正确',
    VALUE_OUT_OF_RANGE: '数值超出范围'
  }

  // 错误处理
  handleError(error) {
    if (error.response) {
      // 服务器响应错误
      switch (error.response.status) {
        case 400:
          this.error(error.response.data?.message || MessageService.MESSAGES.VALIDATION_ERROR)
          break
        case 401:
          this.error('登录已过期，请重新登录')
          // 可以触发登出操作
          break
        case 403:
          this.error(MessageService.MESSAGES.PERMISSION_ERROR)
          break
        case 404:
          this.error('请求的资源不存在')
          break
        case 500:
          this.error(MessageService.MESSAGES.SERVER_ERROR)
          break
        default:
          this.error(error.response.data?.message || MessageService.MESSAGES.OPERATION_ERROR)
      }
    } else if (error.request) {
      // 请求发送失败
      this.error(MessageService.MESSAGES.NETWORK_ERROR)
    } else {
      // 其他错误
      this.error(error.message || MessageService.MESSAGES.OPERATION_ERROR)
    }
  }

  // 确认操作
  confirm(message, onConfirm, onCancel) {
    if (window.confirm(message)) {
      onConfirm?.()
    } else {
      onCancel?.()
    }
  }
}

export default new MessageService()