/**
 * WebSocketClient
 * - 支持自动重连、主题订阅、消息分发
 * - 支持流式响应（onmessage分片）、错误回调
 * - 通过wsClient单例与useWebSocket组合式函数供全局/组件使用
 * 
 * 主要方法：
 *   connect()         建立连接并自动重连
 *   subscribe(topics, callback)   主题订阅，支持onMessage/onError对象
 *   unsubscribe(topics, callback) 取消订阅
 *   disconnect()      主动断开
 * 
 * 扩展点：
 *   - onmessage支持流式片段（如data.chunk/stream）
 *   - callback可为函数或{onMessage,onError}对象
 */
import { ref } from 'vue'

class WebSocketClient {
  constructor() {
    this.ws = null
    this.isConnected = ref(false)
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = Number.MAX_SAFE_INTEGER
    this.reconnectDelay = 3000
    this.subscriptions = new Map() // 主题订阅回调映射
  }

  async connect() {
    try {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const wsUrl = `${protocol}//${window.location.host}/ws/health`
      
      this.ws = new WebSocket(wsUrl)
      
      this.ws.onopen = () => {
        console.log('WebSocket连接已建立')
        this.isConnected.value = true
        this.reconnectAttempts = 0
        
        // 重新订阅之前的主题
        if (this.subscriptions.size > 0) {
          const topics = Array.from(this.subscriptions.keys())
          this.subscribe(topics)
        }
      }
      
      this.ws.onclose = () => {
        console.log('WebSocket连接已关闭')
        this.isConnected.value = false
        this._reconnect()
      }
      
      this.ws.onerror = (error) => {
        console.error('WebSocket错误:', error)
        this.isConnected.value = false
      }
      
      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          const topic = data.topic
          // 流式响应支持：若data.chunk/stream字段存在，视为流式片段
          if (this.subscriptions.has(topic)) {
            this.subscriptions.get(topic).forEach(callback => {
              if (typeof callback === 'function') {
                callback(data)
              } else if (callback && typeof callback.onMessage === 'function') {
                callback.onMessage(data)
              }
            })
          }
        } catch (error) {
          // 回调onError
          const topic = (event && event.data && JSON.parse(event.data).topic) || 'unknown'
          if (this.subscriptions.has(topic)) {
            this.subscriptions.get(topic).forEach(callback => {
              if (callback && typeof callback.onError === 'function') {
                callback.onError(error)
              }
            })
          }
          console.error('处理WebSocket消息时出错:', error)
        }
      }
    } catch (error) {
      console.error('建立WebSocket连接时出错:', error)
      this._reconnect()
    }
  }

  _reconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('WebSocket重连次数超过最大限制')
      return
    }
    
    this.reconnectAttempts++
    console.log(`尝试重新连接... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
    
    setTimeout(() => {
      this.connect()
    }, this.reconnectDelay)
  }

  subscribe(topics, callback) {
    if (!Array.isArray(topics)) {
      topics = [topics]
    }
    
    // 保存订阅回调
    topics.forEach(topic => {
      if (!this.subscriptions.has(topic)) {
        this.subscriptions.set(topic, new Set())
      }
      if (callback) {
        this.subscriptions.get(topic).add(callback)
      }
    })
    
    // 如果已连接，发送订阅请求
    if (this.isConnected.value) {
      this.ws.send(JSON.stringify({
        action: 'subscribe',
        topics
      }))
    }
  }

  unsubscribe(topics, callback) {
    if (!Array.isArray(topics)) {
      topics = [topics]
    }
    
    topics.forEach(topic => {
      if (callback && this.subscriptions.has(topic)) {
        this.subscriptions.get(topic).delete(callback)
        // 如果没有其他回调，则从Map中删除该主题
        if (this.subscriptions.get(topic).size === 0) {
          this.subscriptions.delete(topic)
        }
      } else {
        // 如果没有提供callback，删除该主题的所有订阅
        this.subscriptions.delete(topic)
      }
    })
    
    // 如果已连接，发送取消订阅请求
    if (this.isConnected.value) {
      this.ws.send(JSON.stringify({
        action: 'unsubscribe',
        topics
      }))
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close()
      this.ws = null
      this.isConnected.value = false
      this.subscriptions.clear()
    }
  }
}

// 创建单例实例
export const wsClient = new WebSocketClient()

// 在组件中使用的组合式函数
export function useWebSocket() {
  const subscribe = (topics, callback) => {
    wsClient.subscribe(topics, callback)
  }
  
  const unsubscribe = (topics, callback) => {
    wsClient.unsubscribe(topics, callback)
  }
  
  return {
    isConnected: wsClient.isConnected,
    subscribe,
    unsubscribe
  }
}