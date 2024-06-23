"""Wraps outgoing requests for common logging and monitoring.
"""
import time

from flask import current_app
import requests

class Session:

  def __init__(self, base_url):
    self.base_url = base_url
    self.session = requests.Session()

  def get(self, path, *args, **kwargs):
    start_time = time.time()
    url = f'{self.base_url}/api/{path}'
    response = self.session.get(url, *args, **kwargs)
    total_time = time.time() - start_time

    # Note: Loggers still use `%s` strings because of when the variables get called.
    current_app.logger.info('GET: "%s" returned %s in %s seconds', url, response.status_code, total_time)

    return response.json()
