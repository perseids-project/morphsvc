from morphsvc.lib.engines.AlpheiosRemoteEngine import AlpheiosRemoteEngine

class WhitakersRemoteEngine(AlpheiosRemoteEngine):


    def __init__(self,config,**kwargs):
       super(WhitakersRemoteEngine, self).__init__(config,**kwargs)
       self.config = config
       self.uri = self.config['PARSERS_WHITAKERS_URI']
       self.remote_url = self.config['PARSERS_WHITAKERS_REMOTE_URL']

    def supports_language(self,language):
        return language == 'lat' or language == "la"


