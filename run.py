#!/usr/bin/env python
from flask import Flask
from morphsvc.morphsvc import init_app, get_app
import morphsvc.morphsvc

app = get_app()
init_app(app,"config.cfg")

app.run(debug=True, host="0.0.0.0", port=5000)

