from lxml import etree
from json import dumps

from xmljson import badgerfish as bf

from morphsvc.lib.engines.engine import Engine


class AlpheiosXmlEngine(Engine):

    def output_json(self, engine_response):
        return dumps(bf.data(engine_response))

    def output_xml(self, engine_response):
        return etree.tostring(engine_response)

    def to_cache(self, engine_response):
        return etree.tostring(engine_response)

    def from_cache(self,cached_response):
        return etree.fromstring(cached_response)
