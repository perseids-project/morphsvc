# coding=utf8
from flask import Flask,abort,make_response
from werkzeug.contrib.cache import SimpleCache, MemcachedCache
from flask_restful import Resource, Api, reqparse
from flask.ext.cors import CORS
from morphsvc.analysisword import AnalysisWord


app = Flask("morphsvc")
api = Api(app=app, default_mediatype='application/xml')
app_cache = None

@api.representation('application/json')
def output_json(data, code, headers=None):
    output_data = data['engine'].output_json(data['data'])
    resp = make_response(output_data,code)
    resp.headers.extend(headers or {})
    return resp

@api.representation('application/xml')
def output_xml(data, code, headers=None):
    output_data = data['engine'].output_xml(data['data'])
    resp = make_response(output_data,code)
    resp.headers.extend(headers or {})
    return resp

def get_app():
    return app

def init_app(app=None, config_file="config.cfg",cache=None):
    app.config.from_pyfile(config_file,silent=False)
    if cache is not None:
        app_cache = cache
    else:
        app_cache = SimpleCache()


#api.add_resource(EngineListAPI, '/morphologyservice/engine')
#api.add_resource(EngineAPI, '/morphologyservice/engine/<EngineId>')

api.add_resource(
    AnalysisWord,
    '/analysis/word',
    resource_class_kwargs={ 'config':app.config, 'cache': SimpleCache() }
)



