import multiprocessing

# Gunicorn configuration file
bind = "0.0.0.0:$PORT"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
timeout = 60
