import multiprocessing
import os

PORT = os.environ["PORT"]

bind = f":{PORT}"
workers = multiprocessing.cpu_count() * 2 + 1
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
timeout = 0
