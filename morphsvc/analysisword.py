from flask_restful import Resource, Api, reqparse
import importlib
import morphsvc.lib.engines
from morphsvc.lib.engines.engine import Engine

class AnalysisWord(Resource):
    def __init__(self, **kwargs):
        self.cache = kwargs['cache']
        self.config = kwargs['config']

    def get_cache_key(self,engine=None, lang=None, word=None, engine_args=None):
        arg_pairs = []
        for key,value in engine_args.items():
            if value is not None:
              arg_pairs.append(key + ":" + value)
        args = '__'.join(arg_pairs)
        return engine + "." + lang + '.' + word + '.' + args

    def get_from_cache(self,engine=None,lang=None, word=None, engine_args=None):
        return self.cache.get(self.get_cache_key(engine=engine,word=word,lang=lang,engine_args=engine_args))

    def put_to_cache(self,engine=None,lang=None,word=None,analysis=None, engine_args=None):
        self.cache.set(self.get_cache_key(engine=engine,word=word,lang=lang, engine_args=engine_args),analysis)

    def get(self):
        return self.call_engine()

    def post(self):
        return self.call_engine()

    def call_engine(self):
        parser = reqparse.RequestParser()
        parser.add_argument('engine')
        parser.add_argument('lang')
        parser.add_argument('word')
        parser.add_argument('word_uri', required = False, type = str, location = 'HTTP')
        args = parser.parse_args()
        lang = args['lang']
        engine = args['engine']
        word = args['word']
        word_uri = args["word_uri"]
        config_setting = 'ENGINES_' + engine.upper() + '_CNAME'

        if not config_setting in self.config:
            return self.make_error(msg="unknown engine",code=404)

        module_name, class_name = self.config[config_setting].rsplit(".",1)
        EngineClass = getattr(importlib.import_module(module_name), class_name)
        engine_instance = EngineClass(self.config)

        engine_argparser = reqparse.RequestParser()
        engine_opts = engine_instance.options()
        for opt in engine_opts:
            engine_argparser.add_argument(opt)
        engine_args = engine_argparser.parse_args()

        if not engine_instance.supports_language(lang):
            return self.make_error(msg="unsupported language",engine=engine_instance, code=404)

        cached_word = self.get_from_cache(engine=engine,word=word,lang=lang, engine_args=args)

        if cached_word is not None:
            analysis = engine_instance.from_cache(cached_word)
            return { 'data': analysis, 'engine': engine_instance },201
        else:
            if not word_uri:
                word_uri = 'urn:word:'+word
            analysis = engine_instance.lookup(word=word,word_uri=word_uri,language=lang,request_args=engine_args)
            annotation_uri = 'urn:TuftsMorphologyService:' + word + ':' + engine
            oa = engine_instance.as_annotation(annotation_uri, word_uri,analysis)
            self.put_to_cache(engine=engine, word=word, analysis=engine_instance.to_cache(oa),lang=lang, engine_args=engine_args)
            return { 'data': oa, 'engine': engine_instance },201


    def make_error(self,engine=None, msg=None, code=None):
        if engine is None:
            # general purpose engine for errors
            engine = Engine()
        return { 'data' : msg, 'engine': engine }, code
