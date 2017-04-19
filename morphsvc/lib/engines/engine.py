import json

class Engine():

    def __init__(self,*args,**kwargs):
        pass

    def lookup(self,word=None,word_uri=None,language=None,request_args=None,**kwargs):
        pass

    def output_json(self,engine_response):
        return json.dumps(engine_response)

    def output_xml(self,engine_response):
        return "<error>" + engine_response + "</error>"

    def supports_language(self,language):
        return False

    def options(self):
        return None
