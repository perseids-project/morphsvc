from morphsvc.lib.engines.AlpheiosXmlEngine import AlpheiosXmlEngine
from subprocess import check_output
import itertools
from lxml import etree
from collections import Callable
import os, requests
from morphsvc.lib.transformers.BetacodeTransformer import BetacodeTransformer

class MorpheusLocalEngine(AlpheiosXmlEngine):

    def __init__(self,config,**kwargs):
       super(MorpheusLocalEngine, self).__init__(config,**kwargs)
       self.config = config
       self.uri = self.config['PARSERS_MORPHEUS_URI']
       self.morpheus_path = self.config['PARSERS_MORPHEUS_PATH']
       self.transformer = BetacodeTransformer(config)
       self.lexical_entity_svc_grc = self.config['SERVICES_LEXICAL_ENTITY_SVC_GRC']
       self.lexical_entity_svc_lat = self.config['SERVICES_LEXICAL_ENTITY_SVC_LAT']
       self.lexical_entity_base_uri = self.config['SERVICES_LEXICAL_ENTITY_BASE_URI']

    def lookup(self,word=None,word_uri=None,language=None,request_args=None,**kwargs):
        args = self.make_args(language,request_args)
        if language == 'grc':
          word = self.transformer.transform_input(word)
        parsed = self._execute_query(args,word)
        if language == 'grc':
            transformed = self.transformer.transform_output(parsed)
        else:
            transformed = etree.XML(parsed)
        self.add_lexical_entity_uris(transformed,language)
        return transformed

    def _execute_query(self,args,word):
        return check_output(itertools.chain([self.morpheus_path], args, [word]))


    def supports_language(self,language):
        return language == 'grc' or language == 'lat' or language == 'la'

    def add_lexical_entity_uris(self,analysis,language):
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
            args.append('-S')
        if 'checkPreverbs' in request_args and request_args['checkPreverbs'] == '1':
            args.append('-c')
        return args

    def options(self):
        return {'strictCase': '^1$','checkPreverbs':'^1$'}
