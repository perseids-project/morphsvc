#!/usr/bin/env python
from flask import Flask
from morphsvc.morphsvc import init_app, get_app
import morphsvc.morphsvc
from werkzeug.contrib.cache import RedisCache

app = get_app()

init_app(app,"config.cfg", cache_config = { 'CACHE_TYPE': 'redis', 'CACHE_REDIS_HOST':'localhost','CACHE_REDIS_PORT':6379})

app.run(debug=True, host="0.0.0.0", port=5000)

