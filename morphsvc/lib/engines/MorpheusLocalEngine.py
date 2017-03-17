from morphsvc.lib.engines.AlpheiosXmlEngine import AlpheiosXmlEngine
from subprocess import check_output
import itertools
import os

class MorpheusLocalEngine(AlpheiosXmlEngine):


    def __init__(self,config,**kwargs):
       super(MorpheusLocalEngine, self).__init__(config,**kwargs)
       self.config = config
       self.morpheus_path = self.config['PARSERS_MORPHEUS_PATH']
       self.default_args = self.config['PARSERS_MORPHEUS_DEFAULT_ARGS']

    def lookup(self,word,word_uri,**kwargs):
        return check_output(itertools.chain([self.morpheus_path], self.default_args, [word]))

    def supports_language(self,language):
        return language == 'grc' or language == 'lat' or language == 'la'