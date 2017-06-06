import json

class Engine():
    """ Base Morphological Engine Wrapper Class """

    def __init__(self,*args,**kwargs):
        """ Constructor """
        pass

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
        return json.dumps(engine_response)

    def output_xml(self,engine_response):
        """ Output Engine Response as XML
        :param engine_response: the original engine response
        :type engine_response: object
        :return: the analysis as XML
        :rtype: str
        """
        return "<error>" + engine_response + "</error>"

    def supports_language(self,language):
        """ Checks to see if the engine supports the supplied language
        :param language: the language code to check
        :type language: str
        :return: True if supported, False if not
        :rtype: bool
        """
        return False

    def options(self):
        """ get the engine specific request arguments
        :return: engine specific request arguments or None if there aren't any
        :rtype: dict
        """
        return None
