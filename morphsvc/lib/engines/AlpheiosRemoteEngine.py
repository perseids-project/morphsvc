from morphsvc.lib.engines.AlpheiosXmlEngine import AlpheiosXmlEngine
from subprocess import check_output
import itertools
from lxml import etree
from collections import Callable
import os, requests

class AlpheiosRemoteEngine(AlpheiosXmlEngine):


    def __init__(self,config,**kwargs):
       super(AlpheiosRemoteEngine, self).__init__(config,**kwargs)
       self.config = config
       self.uri = ''
       self.remote_url = ''
       self.transformer = None

    def lookup(self,word,word_uri,language,**kwargs):
        if self.transformer is not None:
          word = self.transformer.transform_input(word)
        parsed = self._execute_query(word)
        if self.transformer is not None:
            transformed = self.transformer.transform_output(parsed)
        else:
            transformed = etree.XML(parsed)
        return transformed

    def supports_language(self,language):
        return False

    def _execute_query(self,word,language):
        url = self.remote_url + word
        return requests.get(url).text



