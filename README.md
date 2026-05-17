# HW8: Monitoring and Observability for ML Service

Домашнее задание выполнено в рамках модуля 8 «Мониторинг и наблюдаемость в продакшене».

Цель работы — построить систему наблюдаемости для ML-сервиса, определить SLO, настроить сбор метрик через Prometheus, визуализацию через Grafana, алертинг при нарушении SLO, а также продемонстрировать data drift, инцидент качества данных через DQOps и архитектуру ML-системы для Virtual Product Placement.

## Состав репозитория

```text
.
├── app/
│   ├── main.py                  # FastAPI ML-сервис с /predict, /health, /metrics
│   └── requirements.txt          # зависимости ML-сервиса
├── doc/
│   └── adr/                      # Architecture Decision Records
├── reports/
│   └── iris_data_drift_report.html
├── screenshots/
│   ├── metrics_tree.png
│   ├── prometheus_targets_up.png
│   ├── grafana_prometheus_datasource_settings.png
│   ├── grafana_prometheus_datasource_success.png
│   ├── grafana_p95_latency_panel_1.png
│   ├── grafana_alert_rule_normal.png
│   ├── grafana_alert_rule_firing_1.png
│   ├── grafana_alert_rule_firing_2.png
│   ├── evidently_data_drift_report.png
│   ├── dqops_postgres_connection_success.png
│   ├── dqops_iris_table_imported.png
│   ├── dqops_initial_table_statistics.png
│   ├── dqops_incident_schema_check.png
│   └── virtual_product_placement_architecture.png
├── sloth/
│   ├── ml_service_slo.yaml
│   └── prometheus_slo_rules.yaml
├── docker-compose.yml
├── prometheus.yml
├── grafana.yaml
├── .env.example
└── HW8_Monitoring_Фрейдина_Алена.ipynb
```
## ВАЖНО: Почему не все ячейки ноутбука перезапускались

При финальной проверке ноутбука были перезапущены только безопасные ячейки: ячейки с построением диаграмм, генерацией статических артефактов, проверкой метрик и сохраненными результатами.

Некоторые ячейки намеренно не перезапускались, потому что они являются интерактивными, тяжелыми или могут разрушить уже полученные артефакты:

1. Ячейки с adr init и adr new не перезапускались, потому что повторный запуск создает дублирующие ADR-файлы.
2. Ячейки установки Python-пакета dqops не перезапускались, потому что актуальная версия DQOps требовала license/API key, а старая версия нарушала зависимости Python-окружения. В итоговом решении DQOps запускается через Docker image dqops/dqo:1.6.2.
3. Colab-ячейки с apt-get, /content, google.colab, tuna, redis-server, YOLO/Ultralytics и обработкой видео не перезапускались локально, так как они предназначены для Colab/Linux-среды, а работа выполнялась локально на macOS.
4. Ячейки, пересоздающие Docker Compose или базы данных в промежуточном состоянии, не перезапускались без необходимости, чтобы не потерять уже зафиксированные Docker-логи, состояния Grafana alert, DQOps incident и сохраненные скриншоты.
5. Ячейки, искусственно замедляющие ML-сервис и вызывающие alert firing, не запускались повторно при финальной проверке, потому что состояние алерта уже было получено, заскриншочено и сохранено в репозитории.
6. Ячейки, изменяющие структуру таблицы PostgreSQL, запускались только в контролируемом порядке. Повторный запуск ALTER TABLE DROP COLUMN petal_width без восстановления таблицы может привести к ошибке, так как столбец уже удален.

Финальный ноутбук сохраняет важные outputs, логи и скриншоты, подтверждающие выполнение задания. Полный Run All для такого ноутбука не является безопасным, так как часть ячеек воспроизводит инфраструктурные и интерактивные действия, которые не должны выполняться повторно без ручного контроля.

