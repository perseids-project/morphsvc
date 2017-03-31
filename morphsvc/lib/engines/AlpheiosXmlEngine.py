from lxml import etree
from json import dumps

from xmljson import badgerfish as bf
from xmljson import yahoo as yh

from morphsvc.lib.engines.engine import Engine
from  morphsvc.lib.transformers.OaLegacyTransformer import OaLegacyTransformer


class AlpheiosXmlEngine(Engine):

    def __init__(self,config,**kwargs):
        self.oa_transformer = OaLegacyTransformer()
        self.uri = ""

    def get_uri(self):
        return self.uri

    def as_annotation(self,word_uri,analysis):
        return self.oa_transformer.wrap(word_uri,self.get_uri(), analysis)

    def output_json(self, engine_response):
        return dumps(bf.data(engine_response))

    def output_xml(self, engine_response):
        return etree.tostring(engine_response)

    def to_cache(self, engine_response):
        return etree.tostring(engine_response)

    def from_cache(self,cached_response):
        return etree.fromstring(cached_response)


