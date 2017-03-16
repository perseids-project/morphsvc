import xml.etree.ElementTree as ET
from json import dumps

from xmljson import badgerfish as bf

from morphsvc.lib.engines.engine import Engine


class AlpheiosXmlEngine(Engine):

    def output_json(self, engine_response):
        return dumps(bf.data(ET.fromstring(engine_response)))

    def output_xml(self, engine_response):
        return engine_response
