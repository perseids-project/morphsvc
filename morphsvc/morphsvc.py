# coding=utf8
from flask import Flask,abort,make_response
from flask.ext.cache import Cache
from flask_restful import Resource, Api, reqparse
from flask.ext.cors import CORS
from morphsvc.analysisword import AnalysisWord


app = Flask("morphsvc")
api = Api(app=app, default_mediatype='application/xml')
cache = Cache(app,config={'CACHE_TYPE':'simple'})


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

def init_app(app=None, config_file="config.cfg",cache_config=None):
    app.config.from_pyfile(config_file,silent=False)
    if cache_config is not None:
        cache.init_app(app,config=cache_config)


#api.add_resource(EngineListAPI, '/morphologyservice/engine')
#api.add_resource(EngineAPI, '/morphologyservice/engine/<EngineId>')

api.add_resource(
    AnalysisWord,
    '/analysis/word',
    resource_class_kwargs={ 'config':app.config, 'cache': cache }
)



