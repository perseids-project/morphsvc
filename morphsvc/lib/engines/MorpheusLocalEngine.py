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
       self.morpheus_path = self.config['PARSERS_MORPHEUS_PATH']
       self.default_args_grc = self.config['PARSERS_MORPHEUS_DEFAULT_ARGS_GRC']
       self.default_args_lat = self.config['PARSERS_MORPHEUS_DEFAULT_ARGS_LAT']
       self.transformer = BetacodeTransformer(config)
       self.lexical_entity_svc_grc = self.config['SERVICES_LEXICAL_ENTITY_SVC_GRC']
       self.lexical_entity_svc_lat = self.config['SERVICES_LEXICAL_ENTITY_SVC_LAT']
       self.lexical_entity_base_uri = self.config['SERVICES_LEXICAL_ENTITY_BASE_URI']

    def lookup(self,word,word_uri,language,**kwargs):
        print("Word="+word)
        word = self.transformer.transform_input(word)
        if language == 'lat':
            args = self.default_args_lat
        else:
            args = self.default_args_grc
        parsed = check_output(itertools.chain([self.morpheus_path], args, [word]))
        if language == 'grc':
            transformed = self.transformer.transform_output(parsed)
        else:
            transformed = etree.XML(parsed)
        self.add_lexical_entity_uris(transformed,language)
        return transformed

    def supports_language(self,language):
        return language == 'grc' or language == 'lat' or language == 'la'

    def add_lexical_entity_uris(self,analysis,language):
        lemmas = analysis.xpath('//hdwd')
        if language == 'lat':
            svc = self.lexical_entity_svc_lat
        else:
            svc = self.lexical_entity_svc_grc
        for l in lemmas:
            url = svc + l.text
            resp = requests.get(url).text
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


