# workers = multiprocessing.cpu_count() * 2 + 1    # 进程数
workers = 5
worker_class = "uvicorn.workers.UvicornWorker"
bind = "0.0.0.0:8000"
