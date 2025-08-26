# 健康数据插件化服务层设计说明

## 架构目标
- 按数据类型（如心率、血压）实现“解析-分析-告警”插件一体化
- 单一插件文件支持一种数据类型，提升内聚性与可维护性
- 动态自动加载所有插件，统一接口 pipeline 流程
- 支持异步与批量处理，异常隔离与日志记录

## 插件接口规范
所有插件需继承 [`HealthDataPlugin`](app/service/health/plugins/base.py:4)，实现如下异步方法：
- `parse(raw_data) -> parsed_data`：解析原始数据为结构化数据
- `analyze(parsed_data) -> analysis_result`：分析结构化数据，输出分析结果
- `check_alert(analysis_result) -> alert_info_list`：根据分析结果判断告警

## 插件实现示例
- [`HeartRatePlugin`](app/service/health/plugins/heart_rate.py:4)：心率数据解析、分析、告警逻辑
- [`BloodPressurePlugin`](app/service/health/plugins/blood_pressure.py:4)：血压数据解析、分析、告警逻辑

## 插件管理与自动加载
- [`PluginManager`](app/service/health/plugins/plugin_manager.py:7) 自动发现并注册所有插件，按数据类型获取插件类

## 服务层调用流程
- [`HealthDataPipeline`](app/service/health/pipeline.py:11) 通过插件统一完成解析、分析、告警
- [`AlertManager`](app/service/health/alert_manager.py:9) 通过插件统一检测告警

## 异常隔离与日志
- 插件执行异常均捕获并通过 [`logger`](app/log/log.py:25) 记录，不影响整体流程

## 单元测试
- [`test_plugins.py`](app/tests/health/test_plugins.py:1) 覆盖插件加载、心率/血压插件功能

## 扩展与维护建议
- 新增数据类型仅需实现新插件并放入 plugins 目录
- 保持接口一致，便于 pipeline/alert_manager 自动集成
- 推荐逐步迁移原有业务逻辑到插件架构
