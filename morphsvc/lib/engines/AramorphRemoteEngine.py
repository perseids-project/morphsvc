from morphsvc.lib.engines.AlpheiosRemoteEngine import AlpheiosRemoteEngine
from morphsvc.lib.transformers.BuckwalterTransformer import BuckwalterTransformer

class AramorphRemoteEngine(AlpheiosRemoteEngine):


    def __init__(self,config,**kwargs):
       super(AramorphRemoteEngine, self).__init__(config,**kwargs)
       self.config = config
       self.uri = self.config['PARSERS_ARAMORPH_URI']
       self.remote_url = self.config['PARSERS_ARAMORPH_REMOTE_URL']
       self.transformer = BuckwalterTransformer(config)

    def supports_language(self,language):
        return language == 'ara' or language == "ar"


