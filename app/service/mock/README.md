# 虚拟病人健康数据模拟服务重构说明

## 设计亮点

- **配置驱动**：所有虚拟病人、设备、生成频率、数据偏向均通过 [`mock_config.py`](app/service/mock/mock_config.py:1) 配置，灵活可扩展。
- **病人/设备管理**：[`patient_manager.py`](app/service/mock/patient_manager.py:1) 支持多病人多设备绑定，统一管理。
- **插件化数据生成**：[`health_mock_factory.py`](app/service/mock/health_mock_factory.py:1) 按配置自动调用健康插件生成多类型数据。
- **高性能异步调度**：[`async_scheduler.py`](app/service/mock/async_scheduler.py:1) 支持多任务并发，按设备频率自动生成数据。
- **数据插入/分发**：[`data_sink.py`](app/service/mock/data_sink.py:1) 可扩展为数据库、消息队列等。
- **主服务调度**：[`mock_service.py`](app/service/mock/mock_service.py:1) 统一生命周期管理，自动调度所有虚拟病人设备。

## 扩展建议

- 支持更多健康插件类型，配置化扩展病人/设备属性。
- 数据插入可对接数据库、MQ、WebSocket等。
- 支持异常场景、数据偏向、批量生成等高级模拟。
- 可通过配置文件或接口动态调整模拟参数。
