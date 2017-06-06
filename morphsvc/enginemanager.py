from flask_restful import Resource
import importlib
from morphsvc.lib.engines.engine import Engine

class EngineManager():


    def __init__(self, config, **kwargs):
        """ Constructor
        :param config: The Flask App Config
        :type config: dict
        """
        self.config = config

    def getengine(self,code):
        config_setting = 'ENGINES_' + code.upper() + '_CNAME'
        if not config_setting in self.config:
            raise Exception("unknown engine")
        module_name, class_name = self.config[config_setting].rsplit(".",1)
        EngineClass = getattr(importlib.import_module(module_name), class_name)
        engine_instance = EngineClass(code,self.config)
        return engine_instance

class EngineListResource(Resource):
    def __init__(self, config, **kwargs):
        """ Constructor
        :param config: The Flask App Config
        :type config: dict
        """
        self.config = config
        self.manager = EngineManager(config)

    def get(self):
        return self.getlist()

    def post(self):
        return self.getlist()

    def getlist(self):
        data = '<enginelist>'
        for engine in self.config['ENGINES'].split(','):
            data = data + str(self.manager.getengine(engine))
        data = data + '</enginelist>'
        return {'data': data, 'engine': Engine(None, None)}, 200

class EngineResource(Resource):
    def __init__(self, config, **kwargs):
        """ Constructor
        :param config: The Flask App Config
        :type config: dict
        """
        self.config = config
        self.manager = EngineManager(config)

    def get(self, id):
        return self.getresp(id)

    def post(self, id=None):
        return self.getresp(id)

    def getresp(self, id):
        data = '<enginelist>' + str(self.manager.getengine(id)) + '</enginelist>'
        return {'data': data, 'engine': Engine(None, None)}, 200
