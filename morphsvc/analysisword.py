from flask_restful import Resource, Api, reqparse
import importlib
import morphsvc.lib.engines
from morphsvc.lib.engines.engine import Engine
from morphsvc.enginemanager import EngineManager

class AnalysisWord(Resource):
    """ Responds to a request for a word level analysis """

    def __init__(self, **kwargs):
        """ Constructor
        :param cache: The Cache to be used to store and retrieve resultss
        :type cache: flask.ext.cache.Cache
        :param config: The Flask App Config
        :type config: dict
        """
        self.cache = kwargs['cache']
        self.config = kwargs['config']

    def get_cache_key(self,engine=None, lang=None, word=None, engine_args=None):
        """ Get the cache key to use for a word lookup
        :param engine: the morphological engine key for the engine to be used
        :type engine: str
        :param lang: the language code for the word
        :type lang: str
        :param word: the word to be looked up
        :type word: str
        :param engine_args: dictionary of engine argument names and values
        :type engine_args: dict
        :return: cache key
        :rtype: str
        """
        arg_pairs = []
        for key,value in engine_args.items():
            if value is not None:
              arg_pairs.append(key + ":" + value)
        args = '__'.join(arg_pairs)
        return engine + "." + lang + '.' + word + '.' + args

    def get_from_cache(self,engine=None,lang=None, word=None, engine_args=None):
        """ Get the word analysis from the cache
        :param engine: the morphological engine key for the engine to be used
        :type engine: str
        :param lang: the language code for the word
        :type lang: str
        :param word: the word to be looked up
        :type word: str
        :param engine_args: dictionary of engine argument names and values
        :type engine_args: dict
        :return: cached analysis
        :rtype: str
        """
        return self.cache.get(self.get_cache_key(engine=engine,word=word,lang=lang,engine_args=engine_args))

    def put_to_cache(self,engine=None,lang=None,word=None,analysis=None, engine_args=None):
        """ Put the word analysis to the cache
        :param engine: the morphological engine key for the engine to be used
        :type engine: str
        :param lang: the language code for the word
        :type lang: str
        :param word: the word to be looked up
        :type word: str
        :param engine_args: dictionary of engine argument names and values
        :type engine_args: dict
        :param analysis: the analysis
        :type analysis: str
        """
        self.cache.set(self.get_cache_key(engine=engine,word=word,lang=lang, engine_args=engine_args),analysis)

    def get(self):
        """ Respond to a GET request
        :param engine: the engine code (Required)
        :param lang: the language code for the word (Required)
        :param word: the word to lookup (Required)
        :param word_uri: a uri for the word (Optional)
        :param *: per engine arguments (Optiona)
        :return: analysis
        """
        return self.call_engine()

    def post(self):
        """ Respond to a POST request
        :param engine: the engine code (Required)
        :param lang: the language code for the word (Required)
        :param word: the word to lookup (Required)
        :param word_uri: a uri for the word (Optional)
        :param *: per engine arguments (Optiona)
        :return: analysis
        """
        return self.call_engine()
        return self.call_engine()

    def call_engine(self):
        """ Execute an analysis request by calling the appropriate morphology engine
        """
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
        engine_manager = EngineManager(self.config)
        try:
            engine_instance = engine_manager.getengine(engine)
        except:
            return self.make_error(msg="<error>unknown engine</error>",code=404)


        engine_argparser = reqparse.RequestParser()
        engine_opts = engine_instance.options()
        for opt in engine_opts:
            engine_argparser.add_argument(opt)
        engine_args = engine_argparser.parse_args()

        if not engine_instance.supports_language(lang):
            return self.make_error(msg="<error>unsupported language</error>", code=404)

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
        """ Make an Error response
        :param engine: The Engine instance which generated the error
        :type engine: Engine
        :param msg: The error message
        :type msg: str
        :param code: The error code
        :type code: int
        :return: error formatted as a dict
        :rtype: dict
        """
        if engine is None:
            # general purpose engine for errors
            engine = Engine(None,None)
        return { 'data' : msg, 'engine': engine }, code
