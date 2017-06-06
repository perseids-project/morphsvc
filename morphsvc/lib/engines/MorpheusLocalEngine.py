from morphsvc.lib.engines.AlpheiosXmlEngine import AlpheiosXmlEngine
from subprocess import check_output
import itertools
from lxml import etree
from collections import Callable
import os, requests, re
from morphsvc.lib.transformers.BetacodeTransformer import BetacodeTransformer
from morphsvc.lib.transformers.LatinTransformer import LatinTransformer

class MorpheusLocalEngine(AlpheiosXmlEngine):
    """ Morpheus Local Engine (Morpheus is callable locally)
    """

    def __init__(self,config,**kwargs):
       """ Constructor
       :param config: app config
       :type config: dict
       """
       super(MorpheusLocalEngine, self).__init__(config,**kwargs)
       self.config = config
       self.uri = self.config['PARSERS_MORPHEUS_URI']
       self.morpheus_path = self.config['PARSERS_MORPHEUS_PATH']
       self.transformer = BetacodeTransformer(config)
       self.latin_transformer = LatinTransformer(config)
       self.lexical_entity_svc_grc = self.config['SERVICES_LEXICAL_ENTITY_SVC_GRC']
       self.lexical_entity_svc_lat = self.config['SERVICES_LEXICAL_ENTITY_SVC_LAT']
       self.lexical_entity_base_uri = self.config['SERVICES_LEXICAL_ENTITY_BASE_URI']

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
        args = self.make_args(language,request_args)
        if language == 'grc':
          word = self.transformer.transform_input(word)
        else:
            word = self.latin_transformer.transform_input(word)
        parsed = self._execute_query(args,word)
        # this is a ridiculous hack to preserve backwards consistency - the old
        # Alpheios mod_perl wrapper stripped the # sign off the hdwds
        if not isinstance(parsed,str):
            parsed = parsed.decode('utf-8')
        parsed = re.sub(r'#(\d+)</hdwd>', '\\1</hdwd>', parsed)
        if language == 'grc':
            transformed = self.transformer.transform_output(parsed)
        else:
            transformed = etree.fromstring(parsed)
        self.add_lexical_entity_uris(transformed,language)
        return transformed

    def _execute_query(self,args,word):
        """ Spawns a local process to execute morpheus and return the output
        :param args: request argments
        :type args: list
        :param word: word to analyze
        :type worD: str
        :return: output
        :rtype: str
        """
        return check_output(itertools.chain([self.morpheus_path], args, [word]))


    def supports_language(self,language):
        """ Checks to see if the engine supports the supplied language
        :param language: the language code to check
        :type language: str
        :return: True if supported, False if not
        :rtype: bool
        """
        return language == 'grc' or language == 'lat' or language == 'la'

    def add_lexical_entity_uris(self,analysis,language):
        """ Adds lexical entity uris to morpheus output
        by calling the service configured for the language
        :param analysis: the analysis from morpheus
        :type analysis: str
        :param language: the language
        :type language: str
        """
        lemmas = analysis.xpath('//hdwd')
        for l in lemmas:
            resp = self._execute_lexical_query(language,l.text)
            uri_xml = etree.fromstring(resp)
            uri = ""
            uris = uri_xml.xpath('//cs:reply//cite:citeObject',
                                 namespaces = {'cs':'http://shot.holycross.edu/xmlns/citequery',
                                               'cite':'http://shot.holycross.edu/xmlns/cite'})
            if len(uris) > 0:
                uri = uris[0].get('urn')
            else:
                uris = uri_xml.xpath('//sparql:results/sparql:result/sparql:binding/sparql:uri',
                                      namespaces = {'sparql':'http://www.w3.org/2005/sparql-results#'})
                if len(uris) > 0:
                    uri = uris[0].text
            if uri:
                l.getparent().getparent().set('uri',self.lexical_entity_base_uri+uri)

    def _execute_lexical_query(self,language,lemma):
        """ Executes the configured lexical entity query service
        :param language: the language code
        :type language: str
        :param lemma: the lemma to lookup in the service
        :type lemma: str
        """
        if language == 'grc':
            svc = self.lexical_entity_svc_grc
        else:
            svc = self.lexical_entity_svc_lat
        url = svc + lemma
        return requests.get(url).text

    def make_args(self,lang,request_args):
        args = []
        args.append("-m"+self.config['PARSERS_MORPHEUS_STEMLIBDIR'])
        if lang == 'la' or lang == 'lat':
            args.append('-L')
        if 'strictCase' in request_args and request_args['strictCase'] == '1':
            pass
        else:
            # default behavior is case insensitive match
            args.append('-S')
        if 'checkPreverbs' in request_args and request_args['checkPreverbs'] == '1':
            args.append('-c')
        return args

    def options(self):
        """ get the engine specific request arguments
        :return: engine specific request arguments or None if there aren't any
        :rtype: dict
        """
        return {'strictCase': '^1$','checkPreverbs':'^1$'}
