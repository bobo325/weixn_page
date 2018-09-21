# 使用说明
注：以下命令都在项目下执行
- 运行celery worker，处理当前任务
    ```shell
    # prod
    celery worker -A proj -l info
    # dev
    celery -A proj worker --pool=solo -l info
    ```
- 运行celery beat，主要用于处理周期性任务
    ```shell
    celery beat -A proj
    ```
- 运行flower监控器
    ```shell
    celery flower -A proj --address=0.0.0.0 --port=5555
    ```