import json
from morphsvc.lib.xmljson import legacy as legacy
from json import dumps
from lxml import etree

class Engine():
    """ Base Morphological Engine Wrapper Class """

    def __init__(self, code, config, **kwargs):
        """ Constructor
        :param code: the engine code
        :type code: str
        :param config: the app config
        :type config: dict
        """
        self.code = code
        self.language_codes = []

    def lookup(self,word=None,word_uri=None,language=None,request_args=None,**kwargs):
        """ Word Lookup Function
        :param word: the word to lookup
        :type word: str
        :param word_uri: a uri for the word
        :type word_uri: str
        :param language: the language code for the word
        :type language: str
        :param request_args: dict of engine specific request arguments
        :type request_args: dict
        :return: the analysis
        :rtype: str
        """
        pass

    def output_json(self,engine_response):
        """ Output Engine Response as JSON
        :param engine_response: the original engine response
        :type engine_response: object
        :return: the analysis as JSON
        :rtype: str
        """
        return dumps(legacy.data(etree.fromstring(engine_response)),ensure_ascii=False)

    def output_xml(self,engine_response):
        """ Output Engine Response as XML
        :param engine_response: the original engine response
        :type engine_response: object
        :return: the analysis as XML
        :rtype: str
        """
        return engine_response

    def supports_language(self,language):
        """ Checks to see if the engine supports the supplied language
        :param language: the language code to check
        :type language: str
        :return: True if supported, False if not
        :rtype: bool
        """
        return language in self.language_codes


    def options(self):
        """ get the engine specific request arguments
        :return: engine specific request arguments
        :rtype: dict
        """
        return {}

    def __str__(self):
        asstr = '<engine code="' + self.code + '">'
        for code in self.language_codes:
            asstr = asstr + '<supportsLanguageCode>' + code + '</supportsLanguageCode>'
        for opt,value in self.options().items():
            asstr = asstr + '<supportsOption>' + opt + '=' + value + '</supportsOption>'
        asstr = asstr + '</engine>'
        return asstr
