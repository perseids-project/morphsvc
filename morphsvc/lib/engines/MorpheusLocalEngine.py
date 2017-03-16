from morphsvc.lib.engines.AlpheiosXmlEngine import AlpheiosXmlEngine
import os

class MorpheusLocalEngine(AlpheiosXmlEngine):
    def lookup(self,word,word_uri):
        file = os.path.join('/home/balmas/workspace/morphsvc/tests', 'fixture.xml')
        return open(file).read()

    def supports_language(self,language):
        return language == 'grc' or language == 'lat' or language == 'la'