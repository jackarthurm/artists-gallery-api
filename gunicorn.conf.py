import multiprocessing

workers = 3  # multiprocessing.cpu_count() * 2 + 1
secure_scheme_headers = {'X-FORWARDED-PROTO': 'https'}
keepalive = 75
timeout = 90
worker_class = 'gevent'
